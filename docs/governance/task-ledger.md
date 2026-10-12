# Task Ledger — the tag protocol and the record of what each task cost

> How a manager session and its worker sessions tag tasks, and how the `maestro-ledger` mod
> turns those tags into an append-only record of tokens, money and attempts.
>
> **Version**: 1.0.0 · **Date**: 2026-10-12 · **Cycle**: 065
> · Constitution: [principles.md](principles.md) · Acronyms: [glossary](glossary.md)
> · Operating model: [operating-model.md](operating-model.md)

## Why this exists

Maestro runs one human, one manager session and several worker sessions. In that shape nobody
can answer: what did implementing cost versus auditing? How many attempts until a task was
approved? How much was spent on rework? Reconstructing it afterwards from chat logs is
guesswork; the **task ledger** records it at the moment it happens.

The ledger is `docs/records/tarefas.jsonl` — JSON Lines (JSONL; JSON is JavaScript Object Notation), one event per line, **only
appended, never rewritten** (a correction is a new event, like `decisoes.jsonl`). It is
written by the `maestro-ledger` mod through `scripts/record-task.py`, which validates every
line against the closed vocabularies below and appends it with `O_APPEND`, repeating the
write until the whole line is out. On Linux and macOS that keeps concurrent sessions from
interleaving (measured: 30 simultaneous ~2 KB lines, all intact). **On Windows it does not**:
Python's `O_APPEND` there is a seek to the end followed by a write, with no atomicity between
processes — run one writer at a time there, or accept a rare damaged line, which the report
counts as invalid instead of crashing.

## The two tags

A tag is **alone on its own line** (leading and trailing spaces are fine; text before or after
it on the same line is not). A value with spaces goes in double quotes, and a quoted value may
contain `]`. Field names are lowercase.

Which tag counts when a message holds several: the **first** `[[TASK]]` and the **last**
`[[DONE]]`. The real assignment heads the message and the real delivery closes it, so an
example of the protocol quoted in the middle of the text — in an answer that explains the tags —
is ignored. A line such as `see [[DONE id=x]] above` is not a tag at
all, because it is not alone on its line.

**Limit: pasting this document.** A `[[TASK]]` example alone on its line (in a code block, as
below) that the **person** pastes while a task is open *is* a tag: it is the first `[[TASK]]` of
the message, and the person may replace the open task, which then closes as `superseded`. Do not
paste protocol examples while a task is open, or quote the example inside a sentence.

The manager tags the task it hands out:

```text
[[TASK id=064-T03 kind=implement attempt=2 cycle=064 redoes=064-T03#1]]
```

The worker ends its delivery with:

```text
[[DONE id=064-T03 outcome=delivered]]
```

An audit or review names the task it judged, and carries the verdict:

```text
[[DONE id=064-A01 outcome=delivered target=064-T03 verdict=rejected reason="no mutation evidence"]]
```

## Fields and vocabularies

The vocabularies are closed: `scripts/record-task.py` rejects any other value.

| Field | On | Values |
|---|---|---|
| `id` | `TASK`, `DONE` | required; the **same id on every attempt** of a task |
| `kind` | `TASK` | `spec` · `plan` · `implement` · `test` · `review` · `audit` · `fix` · `docs` · `research` |
| `attempt` | `TASK` | integer ≥ 1 (not "first" / "second") |
| `cycle` | `TASK` | the `NNN` of the cycle |
| `redoes` | `TASK` | the rejected attempt this one redoes, as `<id>#<attempt>` |
| `outcome` | `DONE` | `delivered` · `blocked` · `failed` — the mod itself also writes `interrupted` and `superseded` |
| `target` | `DONE` of `audit` / `review` | the `id` of the task being judged |
| `verdict` | `DONE` of `audit` / `review` | `approved` · `approved_with_notes` · `rejected` |
| `reason` | `DONE` of `audit` / `review` | free text, quoted |

## Attempt, outcome, verdict — three different things

- **Attempt** — how many times the task was tried (`attempt=1`, `2`, …).
- **Outcome** — could the session do it? (`delivered`, `blocked`, `failed`.)
- **Verdict** — was the work accepted? (`approved`, `approved_with_notes`, `rejected`.)

The verdict **never comes from whoever executed the task**. It comes from a separate `audit`
or `review` task that points at the judged one through `target`. This is Principle II: who
executes does not verify. The mod writes a `verdict` event only when a `DONE` carries both
`target` and `verdict`, and it writes it **on the target**; a plain `DONE` has no way to grade
its own work. The mod **enforces** this: a `DONE` carrying `target` and `verdict` writes a
`verdict` event only when the active task has kind `audit` or `review`; for any other kind it
records nothing and logs "verdict ignored: only audit/review tasks judge".

The same rule holds on the reading side: every `verdict` event names who gave it in `by`
(required; the recorder rejects a verdict without it), and the report counts only verdicts whose
`by` is an `audit` or `review` task of the ledger **and** whose `session` is the session of a
`start` of that task (whoever judged is whoever ran the audit). A verdict signed by a manager
session, by any other name, or by a session that never ran that audit, is not counted.

**A whole cycle can be judged.** A review of the cycle as a whole points `target` at
`<NNN>-cycle` (for example `target=064-cycle`), which is not a task. The report shows it in a
"Cycle verdicts" section: the last valid verdict is the current one and the history is kept
(064 `rejected` by 064-R1, then `approved_with_notes` by 064-R2). It is not a verdict on a task
with no `start`, and it does not enter the first-pass rate. Ids ending in `-cycle` are reserved.

```text
[[DONE id=064-R2 outcome=delivered target=064-cycle verdict=approved_with_notes reason="no blocking findings"]]
```

## Events the mod writes

Every line has `ts` (a timestamp in ISO 8601, the International Organization for
Standardization date format), `event` and `task_id`. Events are `assigned`, `start`, `stop`
and `verdict`.

| Event | Written by | When | Fields besides `ts`, `event`, `task_id` |
|---|---|---|---|
| `assigned` | the manager's session | it sends a message carrying `[[TASK]]` | `kind`, `attempt`, `cycle`, `redoes`, `session`, `to` (the recipient) |
| `start` | the worker's session | it receives (or is prompted with) `[[TASK]]` | `kind`, `attempt`, `cycle`, `redoes`, `session`, `model`, `cost_start_usd` |
| `stop` | the worker's session | it sends or answers with `[[DONE]]`; also `interrupted` / `superseded` | `kind`, `attempt`, `cycle`, `redoes`, `session`, `outcome`, `duration_s`, `requests`, `tokens_in`, `tokens_out`, `tokens_cache_read`, `tokens_cache_write`, `tokens_subagents`, `tokens_by_model`, `cost_usd` |
| `verdict` | the session that closes an `audit` / `review` | its `DONE` has both `target` and `verdict` | `verdict`, `reason`, `by` (the audit task's id), `session` |

Meaning of the `stop` measures:

- `requests` — model requests made while the task was active.
- `tokens_in`, `tokens_out` — input and output tokens, summed over those requests.
- `tokens_cache_read`, `tokens_cache_write` — prompt-cache tokens read and written.
- `tokens_subagents` — the share of the total spent inside subagents (all four kinds summed).
- `tokens_by_model` — an object per model with `input`, `output`, `cacheRead`, `cacheWrite`
  and `requests`.
- `cost_usd` — spend between `start` and `stop`, in US dollars, from the session's own usage
  report.
- `duration_s` — wall-clock seconds from `start` to `stop`.

A `stop` pairs with the most recent open `start` of the same `task_id`, the same session **and**
the same attempt (when both events carry one). A session id is not a safe key on its own: in
nested sessions it can repeat — the workers of this cycle inherited the manager's id — so the
attempt number is part of the key. A `start` with no `stop` is an **orphan**: paid work that was
not delivered. It is never completed by inference.

## Installing the mod

The method installer does **not** install the mod: `claude plugin install` writes to the
user's own Claude Code settings, outside the target project. Run it yourself, once:

```bash
claude plugin install maestro-ledger --marketplace GHDaru/maestro --scope project
```

**Install with `--scope project` only, and only in repositories you trust.** The mod runs the
`scripts/record-task.py` of whichever repository is open, so with `--scope user` any repository
you open can make it execute its own script.

It needs Claude Code 2.1.292 or newer (the `--marketplace` flag in the shell) and mods enabled
(2.1.287 or newer). The recorder `scripts/record-task.py` travels with the method, so install
the method first.

## Reading the ledger

```bash
scripts/report-tasks.py                  # whole ledger
scripts/report-tasks.py --cycle 064      # one cycle
scripts/report-tasks.py --json           # machine-readable
```

The report gives tokens and cost per `kind` and per cycle, and tokens per model; the **first-pass
approval rate** (tasks approved on attempt 1, counting only verdicts from `audit` / `review`
tasks); the **rework cost** (attempts ≥ 2); the **cache rate** (`tokens_cache_read` ÷ total
input) and the **orphans**.

**Cost is per attempt, never per model.** The session's usage report gives one dollar figure
for the whole attempt, so the per-model table carries tokens only and its cost column shows `-`
rather than an invented split.

## Declared limits

So nobody mistakes this for full coverage:

- **Cloud sessions** (`claude.ai/code`) do not load plugins enabled in the repository's
  `.claude/settings.json`: the mod does not run there.
- **WSL (Windows Subsystem for Linux) sessions** in the Desktop app do not load plugins: the
  mod does not run there either.
- **Hot reload** of the mod loses the active task, which is a module variable. The ledger then
  shows a `start` with no `stop` — a visible orphan, never an invented `stop`.
- **`session.end`** gives all mods 1.5 s in total, so the `interrupted` record is best effort;
  the report finds orphans regardless.
- **One active task per session.** A `[[TASK]]` with a different id from the person closes the
  open one as `superseded`. A `[[TASK]]` arriving from **another session** never replaces an open
  task: it is refused and the refusal is logged, because anyone on the machine can send a
  message and its sender name is whatever the sender wrote. Only the person replaces — at the
  terminal, through Remote Control, or as the host of a `claude -p` run. The next attempt of the
  **same** id (a higher `attempt`) is new work, not a replacement: the previous attempt is
  closed as `superseded` and the new one starts.
- **A `[[DONE]]` with another id** than the open task's is ignored and logged.
- **The judge's label is not authenticated.** With the session holding no open task, another
  session can open a `kind=audit` task and issue a verdict. The report counts only verdicts whose
  `session` is that of the audit task's `start`, but that proves who ran the audit, not who typed
  the tag. The check also assumes distinct session ids per executor: in nested sessions they
  repeat (measured in cycle 065), and then it cannot tell executors apart.
- **A new, empty `specs/NNN-*` directory** makes the `Stop` hook measure the new cycle, which is
  green, and so stay silent about a ticked `TAIL` box without evidence in the previous one. The
  continuous integration (CI) job, which runs `--ticked-only` over every cycle, still catches it.
- **`cost_usd` on a subscription plan** is the equivalent at Application Programming Interface (API) prices (the same number as
  `/cost`). **Tokens** are exact on any plan and are the primary measure.
- The exchange between sessions (`session.receive` / `session.send`) is covered by the engine's
  test kit; a live two-session run is a manual check.
