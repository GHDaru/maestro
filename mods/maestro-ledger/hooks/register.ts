import type { EngineInterface, Register } from 'claude-code'
import { parseTag, positiveInt, type TagFields } from './tags.ts'

// The recorder is the method's own script: one place validates and appends (Principle VI).
const RECORDER = 'scripts/record-task.py'
// The kinds whose [[DONE]] may carry a verdict on another task.
const JUDGES = new Set(['audit', 'review'])

type Counts = { input: number; output: number; cacheRead: number; cacheWrite: number; requests: number }
type Active = {
  id: string
  fields: TagFields
  startedAt: number
  costStartUsd?: number
  total: Counts
  subagents: Counts
  byModel: Record<string, Counts>
}

const zero = (): Counts => ({ input: 0, output: 0, cacheRead: 0, cacheWrite: 0, requests: 0 })

// One task at a time per session: the active one receives every request's tokens.
// A module variable: a hot reload of the mod loses it, and the ledger then shows a start
// with no stop — an orphan, visible, never a made-up stop.
let active: Active | undefined

async function base($: EngineInterface) {
  const [now, sessionId, model] = await Promise.all([$.clock.now(), $.session.id(), $.session.model()])
  return { ts: new Date(now).toISOString(), session: sessionId, model, now }
}

async function costUsd($: EngineInterface): Promise<number | undefined> {
  try {
    return (await $.session.usage()).cost?.usd
  } catch {
    return undefined
  }
}

async function record($: EngineInterface, rec: Record<string, unknown>) {
  try {
    const out = await $.process.run(['python3', RECORDER, JSON.stringify(rec)], { cwd: await $.session.root() })
    if (out.exitCode !== 0) {
      $.ui.log(`not recorded: ${(out.stderr.trim().split('\n')[0] || `exit ${out.exitCode}`)}`)
    }
  } catch {
    $.ui.log(`not recorded: ${RECORDER} could not run (is the method installed here?)`)
  }
}

function common(fields: TagFields) {
  return {
    task_id: fields.id,
    kind: fields.kind,
    attempt: positiveInt(fields.attempt),
    cycle: fields.cycle,
    redoes: fields.redoes,
  }
}

// Who may replace an open task with a different one (independent review of cycle 064): only
// the person — at the terminal, through Remote Control, or as the host of a `claude -p` run.
// Another session's message cannot: anyone on the machine can send one, and its sender name
// is whatever the sender wrote, so a forged [[TASK]] would otherwise steal the open task's
// tokens. It is refused, and the refusal is visible.
const PERSON = new Set(['composer', 'bridge', 'sdk'])

async function start($: EngineInterface, fields: TagFields, fromPerson: boolean) {
  if (active?.id === fields.id) {
    // The same delivery seen twice (receive + prompt) — unless it is the NEXT attempt of the
    // same task, which is new work: clock the old attempt out and the new one in.
    if ((active.fields.attempt ?? '') === (fields.attempt ?? '')) return
    // Another session may only move a task FORWARD (second independent review of cycle 064):
    // resending the same id with a lower or unreadable attempt would close the open one.
    const open = positiveInt(active.fields.attempt) ?? 0
    const next = positiveInt(fields.attempt) ?? 0
    if (!fromPerson && next <= open) {
      $.ui.log(`task ${fields.id} attempt ${fields.attempt ?? '?'} refused: attempt ${active.fields.attempt ?? '?'} is open and only a higher attempt replaces it`)
      return
    }
  } else if (active && !fromPerson) {
    $.ui.log(`task ${fields.id} refused: ${active.id} is still open — it ends with its [[DONE]], or the person replaces it`)
    return
  }
  if (active) await stop($, { id: active.id, outcome: 'superseded' })
  const b = await base($)
  active = { id: fields.id, fields, startedAt: b.now, costStartUsd: await costUsd($), total: zero(), subagents: zero(), byModel: {} }
  $.ui.status(`task ${fields.id} · ${fields.kind ?? '?'} · attempt ${fields.attempt ?? '?'}`)
  await record($, { ts: b.ts, event: 'start', ...common(fields), session: b.session, model: b.model, cost_start_usd: active.costStartUsd })
}

async function stop($: EngineInterface, done: TagFields) {
  const task = active
  if (!task) {
    $.ui.log(`[[DONE id=${done.id}]] ignored: no task is open in this session`)
    return
  }
  if (task.id !== done.id) {
    $.ui.log(`[[DONE id=${done.id}]] ignored: the open task is ${task.id}`)
    return
  }
  active = undefined
  $.ui.status(undefined)
  const b = await base($)
  const costEnd = await costUsd($)
  const t = task.total
  await record($, {
    ts: b.ts,
    event: 'stop',
    ...common(task.fields),
    session: b.session,
    outcome: done.outcome ?? 'delivered',
    duration_s: Math.round((b.now - task.startedAt) / 1000),
    requests: t.requests,
    tokens_in: t.input,
    tokens_out: t.output,
    tokens_cache_read: t.cacheRead,
    tokens_cache_write: t.cacheWrite,
    tokens_subagents: task.subagents.input + task.subagents.output + task.subagents.cacheRead + task.subagents.cacheWrite,
    tokens_by_model: task.byModel,
    cost_usd:
      costEnd !== undefined && task.costStartUsd !== undefined
        ? Math.round((costEnd - task.costStartUsd) * 1e6) / 1e6
        : undefined,
  })
  // An audit or review names the task it judged: its verdict becomes that task's event.
  // Only those two kinds judge (Principle II: whoever executes does not verify) — a verdict
  // carried by any other task is dropped, visibly, never recorded.
  if (done.target && done.verdict) {
    if (JUDGES.has(task.fields.kind ?? '')) {
      await record($, { ts: b.ts, event: 'verdict', task_id: done.target, verdict: done.verdict, reason: done.reason, by: task.id, session: b.session })
    } else {
      $.ui.log(`verdict ignored: only audit/review tasks judge (${task.id} is ${task.fields.kind ?? 'kind-less'})`)
    }
  }
}

export const register: Register = on => {
  // ── clock in ── the task arrives from another session (the manager) …
  on('session.receive', async ($, e, next) => {
    const task = parseTag(e.text, 'TASK')
    if (task && !e.agentId) await start($, task, false)
    return next(e)
  })
  // … or is typed / submitted as a prompt.
  on('prompt.submit', async ($, e, next) => {
    const task = parseTag(e.text, 'TASK')
    if (task) await start($, task, PERSON.has(e.origin?.kind ?? ''))
    return next(e)
  })

  // ── every request to the model: add its tokens to the active task ──
  on('turn.step', async function* ($, e, next) {
    const result = yield* next(e)
    const u = result.usage
    if (active && u) {
      const add = (c: Counts) => {
        c.input += u.input_tokens
        c.output += u.output_tokens
        c.cacheRead += u.cache_read_input_tokens
        c.cacheWrite += u.cache_creation_input_tokens
        c.requests += 1
      }
      add(active.total)
      add((active.byModel[u.model || 'unknown'] ??= zero()))
      if (e.agentId) add(active.subagents)
    }
    return result
  })

  // ── outgoing messages: the manager assigns, or the worker hands back ──
  on('session.send', async ($, e, next) => {
    const assigned = parseTag(e.text, 'TASK')
    const done = parseTag(e.text, 'DONE')
    const sent = await next(e)
    if (assigned) {
      const b = await base($)
      await record($, { ts: b.ts, event: 'assigned', ...common(assigned), session: b.session, to: e.to })
    }
    if (done && !e.agentId) await stop($, done)
    return sent
  })

  // ── the worker may also hand back in its final answer ──
  on('turn.complete', async ($, e, next) => {
    const result = await next(e)
    const done = e.agentId ? undefined : parseTag(e.answer, 'DONE')
    if (done) await stop($, done)
    return result
  })

  // ── a session that ends with a task open: interrupted, never silently lost ──
  on('session.end', async ($, e, next) => {
    if (active) await stop($, { id: active.id, outcome: 'interrupted' })
    return next(e)
  })
}
