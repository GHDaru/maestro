import { describe, expect, test } from 'claude-code/testing'
import type { On } from 'claude-code'
import { parseTag, parseTags, positiveInt } from './tags.ts'

type Rec = Record<string, any>

// Everything beneath the mod, played by the test: the session's identity, a clock that moves
// 1 s per call, a cost ledger that grows, and a recorder that keeps what it was asked to append.
function world(on: On) {
  const recorded: Rec[] & { logs?: string[] } = []
  let now = Date.UTC(2026, 9, 12, 4, 0, 0)
  let usd = 1.0
  on('session.id', async () => ({ value: 'sess-worker' }))
  on('session.model', async () => ({ value: 'claude-opus-5-5' }))
  on('session.root', async () => ({ value: '/repo' }))
  on('clock.now', async () => ({ value: (now += 1000) }))
  on('session.usage', async () => ({
    value: { startedAt: 0, context: { tokens: 0, window: 200000, percent: 0 }, rateLimits: [], cost: { usd: (usd += 0.25) } } as any,
  }))
  on('process.run', async (_$, e) => {
    recorded.push(JSON.parse(e.argv[2]))
    return { value: { exitCode: 0, stdout: 'ok', stderr: '', isStdoutTruncated: false, isStderrTruncated: false } }
  })
  on('ui.status', async () => ({ value: undefined }) as any)
  const logs: string[] = []
  on('ui.log', async (_$, e: any) => {
    logs.push(JSON.stringify(e))
    return { value: undefined } as any
  })
  recorded.logs = logs
  on('session.receive', async (_$, e) => ({ text: e.text }))
  on('session.send', async () => ({ isDelivered: true }))
  on('turn.complete', async (_$, e) => ({ text: e.answer }))
  on('session.end', async (_$, e) => ({ sessionId: e.sessionId }))
  on('prompt.submit', async (_$, e) => ({ text: e.text, context: e.context }))
  return recorded as Rec[] & { logs: string[] }
}

// One request to the model, with the usage the API would report.
async function step($: any, usage: Rec | null, agentId?: string) {
  const stream = $.turn.step({ turnId: 't1', index: 0, model: usage?.model ?? 'claude-opus-5-5', messageCount: 1, agentId })
  for await (const _ of stream) {
    /* drain */
  }
  return stream.result
}

function requestUsage(input: number, output: number, cacheRead: number, cacheWrite: number, model = 'claude-opus-5-5') {
  return { input_tokens: input, output_tokens: output, cache_read_input_tokens: cacheRead, cache_creation_input_tokens: cacheWrite, model }
}

const PEER = { kind: 'peer-send-message' } as any
const receive = ($: any, text: string) => $.session.receive({ origin: PEER, text })
const send = ($: any, text: string) => $.session.send({ to: 'manager', text, origin: { kind: 'model' } })
const answer = ($: any, text: string) =>
  $.turn.complete({ answer: text, durationMs: 5, isAborted: false, turnId: 't', reason: 'answer' } as any)
function stepsAnswer(on: On, usage: () => Rec | null) {
  on('turn.step', async function* (_$, e) {
    return { turnId: e.turnId, index: e.index, answer: '', toolUses: [], stopReason: 'end_turn', usage: usage() } as any
  })
}

describe('tags', () => {
  test('a tag counts only alone on its line; quoted values may hold ]; id-less is ignored', () => {
    expect(parseTag('[[TASK id=064-T03 kind=implement attempt=2]]\nwork', 'TASK')).toEqual({ id: '064-T03', kind: 'implement', attempt: '2' })
    expect(parseTag('see [[TASK id=X kind=docs]] inline', 'TASK')).toBeUndefined()
    expect(parseTag('see [[TASK id=X kind=docs]]', 'TASK')).toBeUndefined()
    expect(parseTag('[[TASK id=X kind=docs]] and then some words', 'TASK')).toBeUndefined()
    expect(parseTag('[[DONE id=A1 verdict=rejected reason="x[1] broken"]]', 'DONE')?.reason).toBe('x[1] broken')
    expect(parseTag('[[TASK kind=test]]', 'TASK')).toBeUndefined()
    expect(parseTag('no tag here', 'DONE')).toBeUndefined()
    expect(positiveInt('2')).toBe(2)
    expect(positiveInt('two')).toBeUndefined()
    expect(positiveInt('0')).toBeUndefined()
  })

  test('the first own-line TASK and the last own-line DONE are the ones that count', () => {
    const text = '[[TASK id=REAL kind=fix attempt=1]]\nthe protocol example:\n[[TASK id=EXAMPLE kind=docs]]\n[[DONE id=EXAMPLE]]\nwork\n[[DONE id=REAL outcome=delivered]]'
    expect(parseTag(text, 'TASK')?.id).toBe('REAL')
    expect(parseTag(text, 'DONE')?.id).toBe('REAL')
    expect(parseTags(text, 'DONE').map(t => t.id)).toEqual(['EXAMPLE', 'REAL'])
  })
})

describe('ledger', () => {
  test('clock in on [[TASK]], sum every request, clock out on [[DONE]]', async ($, on) => {
    const recorded = world(on)
    let usage: Rec | null = null
    stepsAnswer(on, () => usage)

    await receive($, '[[TASK id=064-T03 kind=implement attempt=2 cycle=064 redoes=064-T03#1]]\nImplement the parser.')
    usage = requestUsage(1200, 800, 45000, 3000)
    await step($, usage)
    usage = requestUsage(300, 2100, 47000, 0)
    await step($, usage)
    usage = requestUsage(5000, 1500, 0, 0, 'claude-haiku-5-5')
    await step($, usage, 'sub-1')
    await send($, 'parser done\n[[DONE id=064-T03 outcome=delivered]]')

    expect(recorded.map(r => r.event)).toEqual(['start', 'stop'])
    const [start, stop] = recorded
    expect(start).toMatchObject({ task_id: '064-T03', kind: 'implement', attempt: 2, cycle: '064', redoes: '064-T03#1', session: 'sess-worker' })
    expect(stop).toMatchObject({
      task_id: '064-T03', outcome: 'delivered', requests: 3,
      tokens_in: 6500, tokens_out: 4400, tokens_cache_read: 92000, tokens_cache_write: 3000, tokens_subagents: 6500,
    })
    expect(Object.keys(stop.tokens_by_model).sort()).toEqual(['claude-haiku-5-5', 'claude-opus-5-5'])
    expect(stop.cost_usd).toBe(0.25)
    expect(stop.duration_s).toBeGreaterThan(0)
  })

  test('requests outside a task are not counted; a DONE for another id is ignored, visibly', async ($, on) => {
    const recorded = world(on)
    stepsAnswer(on, () => requestUsage(999, 999, 0, 0))
    await step($, {})
    await receive($, '[[TASK id=T1 kind=test attempt=1]]')
    await send($, '[[DONE id=OTHER]]')
    // still T1's: the DONE above named another task, so this request must land on T1
    await step($, {})
    await answer($, 'all good\n[[DONE id=T1 outcome=delivered]]')

    expect(recorded.map(r => r.event)).toEqual(['start', 'stop'])
    // one request, not two: the one before [[TASK]] is nobody's
    expect(recorded[1]).toMatchObject({ task_id: 'T1', requests: 1, tokens_in: 999 })
    expect(recorded.logs.some((l: string) => l.includes('ignored: the open task is T1'))).toBe(true)
  })

  test('quoting the protocol does not close the task: the last own-line DONE does', async ($, on) => {
    const recorded = world(on)
    await receive($, '[[TASK id=REAL kind=docs attempt=1]]')
    await answer($, 'Example of a closing line:\n[[DONE id=064-T03 outcome=delivered]]\nand mine:\n[[DONE id=REAL outcome=delivered]]')
    expect(recorded.map(r => `${r.event}:${r.task_id}`)).toEqual(['start:REAL', 'stop:REAL'])
  })

  test('an audit hands back a verdict on the task it judged', async ($, on) => {
    const recorded = world(on)
    await receive($, '[[TASK id=064-A01 kind=audit attempt=1]]')
    await send($, '[[DONE id=064-A01 outcome=delivered target=064-T03 verdict=rejected reason="no mutation evidence"]]')

    expect(recorded.map(r => r.event)).toEqual(['start', 'stop', 'verdict'])
    expect(recorded[2]).toMatchObject({ task_id: '064-T03', verdict: 'rejected', reason: 'no mutation evidence', by: '064-A01' })
  })

  test('a task that is not an audit or review cannot write a verdict', async ($, on) => {
    const recorded = world(on)
    await receive($, '[[TASK id=064-T9 kind=implement attempt=1]]')
    await send($, '[[DONE id=064-T9 outcome=delivered target=064-T3 verdict=approved]]')

    expect(recorded.map(r => r.event)).toEqual(['start', 'stop'])
    expect(recorded.logs.some((l: string) => l.includes('verdict ignored'))).toBe(true)
  })

  test('the manager assigning is recorded', async ($, on) => {
    const recorded = world(on)
    await $.session.send({ to: 'worker-a', text: '[[TASK id=064-T04 kind=test attempt=1]]\nwrite the tests', origin: { kind: 'model' } })
    expect(recorded.map(r => `${r.event}:${r.task_id}`)).toEqual(['assigned:064-T04'])
    expect(recorded[0].to).toBe('worker-a')
  })

  test("another session's [[TASK]] cannot take over an open task — its tokens stay put", async ($, on) => {
    const recorded = world(on)
    stepsAnswer(on, () => requestUsage(10, 10, 0, 0))
    await receive($, '[[TASK id=MINE kind=implement attempt=1]]')
    await receive($, '[[TASK id=FORGED kind=audit attempt=1]]')
    await step($, {})
    await answer($, '[[DONE id=MINE outcome=delivered]]')

    expect(recorded.map(r => `${r.event}:${r.task_id}`)).toEqual(['start:MINE', 'stop:MINE'])
    expect(recorded[1].requests).toBe(1)
    expect(recorded.logs.some((l: string) => l.includes('task FORGED refused'))).toBe(true)
  })

  test('the person may replace an open task', async ($, on) => {
    const recorded = world(on)
    await receive($, '[[TASK id=X1 kind=docs attempt=1]]')
    await $.prompt.submit({ text: '[[TASK id=X2 kind=docs attempt=1]]', origin: { kind: 'composer' } } as any)
    expect(recorded.map(r => `${r.event}:${r.task_id}:${r.outcome ?? ''}`)).toEqual(['start:X1:', 'stop:X1:superseded', 'start:X2:'])
  })

  test('the person through Remote Control or as the host of claude -p may also replace an open task', async ($, on) => {
    const recorded = world(on)
    await receive($, '[[TASK id=B1 kind=docs attempt=1]]')
    await $.prompt.submit({ text: '[[TASK id=B2 kind=docs attempt=1]]', origin: { kind: 'bridge' } } as any)
    await $.prompt.submit({ text: '[[TASK id=B3 kind=docs attempt=1]]', origin: { kind: 'sdk' } } as any)
    expect(recorded.map(r => `${r.event}:${r.task_id}:${r.outcome ?? ''}`)).toEqual([
      'start:B1:', 'stop:B1:superseded', 'start:B2:', 'stop:B2:superseded', 'start:B3:',
    ])
  })

  test("another session cannot move an open task back: a lower attempt is refused", async ($, on) => {
    const recorded = world(on)
    await receive($, '[[TASK id=T3 kind=implement attempt=2]]')
    await receive($, '[[TASK id=T3 kind=implement attempt=1]]')
    expect(recorded.map(r => `${r.event}:${r.attempt}`)).toEqual(['start:2'])
    expect(recorded.logs.some((l: string) => l.includes('only a higher attempt replaces it'))).toBe(true)
  })

  test('the next attempt of the same task is new work: attempt 1 clocks out, attempt 2 gets the tokens', async ($, on) => {
    const recorded = world(on)
    stepsAnswer(on, () => requestUsage(7, 7, 0, 0))
    await receive($, '[[TASK id=T2 kind=implement attempt=1]]')
    await receive($, '[[TASK id=T2 kind=implement attempt=2 redoes=T2#1]]')
    await step($, {})
    await answer($, '[[DONE id=T2 outcome=delivered]]')

    expect(recorded.map(r => `${r.event}:${r.attempt}:${r.outcome ?? ''}`)).toEqual(['start:1:', 'stop:1:superseded', 'start:2:', 'stop:2:delivered'])
    expect(recorded[3].requests).toBe(1)
  })

  test('a session that ends with a task open records it as interrupted', async ($, on) => {
    const recorded = world(on)
    await receive($, '[[TASK id=T9 kind=implement attempt=1]]')
    await $.session.end({ reason: 'other', sessionId: 'sess-worker', resume: {} as any })
    expect(recorded.map(r => `${r.event}:${r.outcome ?? ''}`)).toEqual(['start:', 'stop:interrupted'])
  })

  test('the same delivery seen twice clocks in once', async ($, on) => {
    const recorded = world(on)
    const text = '[[TASK id=T5 kind=fix attempt=1]]'
    await receive($, text)
    await $.prompt.submit({ text, origin: { kind: 'sdk' } } as any)
    expect(recorded.map(r => r.event)).toEqual(['start'])
  })

  test('a request with no model name lands under "unknown", never "undefined"', async ($, on) => {
    const recorded = world(on)
    stepsAnswer(on, () => ({ ...requestUsage(1, 1, 0, 0), model: '' }))
    await receive($, '[[TASK id=T6 kind=fix attempt=1]]')
    await step($, {})
    await answer($, '[[DONE id=T6]]')
    expect(Object.keys(recorded[1].tokens_by_model)).toEqual(['unknown'])
  })
})
