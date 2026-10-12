# QA report 065 — O método se cobra sozinho e bate o ponto

> **Renumbered from 064 to 065** on 2026-10-12, when rebased on `dev`: 064 was already
> cycle `064-capa-para-a-ia-que-instala`. ADR 0021 and roadmap phase F29 were free and stay.
> The ledger `docs/records/tarefas.jsonl` is append-only: this cycle's events **keep
> `cycle: "064"` and ids `064-*`** — `report-tasks.py --cycle 064` is the query that finds them.

- **Date**: 2026-10-12 · **Lane**: full · **Verdict**: DoD green · independent review R1 rejected → R2 approved with notes, notes treated · human gate granted 2026-10-12

## Prototype evidence (before the cycle's implementation)

What the prototype on branch `064-auto-checagem-e-livro-de-ponto` showed, on Claude Code
2.1.296. This is NOT the closing tail: no TAIL box is ticked by it.

### Mutations of the ledger mod (`mods/maestro-ledger/hooks/register.ts`)

Each applied to a copy; `claude plugin test` on the copy.

| # | Mutation | Result |
|---|---|---|
| M1 | tokens are not added to the task | 5 pass · 2 fail |
| M2 | the audit verdict is not recorded | 6 pass · 1 fail |
| M3 | `session.end` ignores the open task | 6 pass · 1 fail |
| M4 | no de-duplication (receive + prompt) | 6 pass · 1 fail |
| M5 | subagent tokens are not separated | 6 pass · 1 fail |
| M6 | a `[[DONE]]` for another id closes the active task | **survived the first test (7 pass)** → test strengthened → 6 pass · 1 fail |
| M7 | requests outside a task are counted | 6 pass · 1 fail |

### Stop hook (`scripts/hooks/stop-conformance.py`), stdin simulated

| Case | Output |
|---|---|
| green repository | nothing (may stop) |
| TAIL ticked, `qa-report.md` deleted | `decision: block` with the two `✗` lines |
| same, `stop_hook_active: true` | `systemMessage` to the human, no block |
| repository without the method | nothing |
| broken stdin | fails open, reason on stderr |

First run found a defect: the gate truncates evidence by bytes, strict UTF-8 decoding raised,
and the hook failed open — silently never checking. Fixed (`errors="replace"`), commented.

### Live runs (`claude -p`, Haiku)

- Stop hook: the agent said "terminei", was blocked, investigated, could not restore the file
  (no permission), reported; the hook then let it stop and warned the human. US$ 0.017.
- Ledger mod: recorded `requests 2 · in 4 · out 350 · cache_read 71578 · cache_write 23396 ·
  cost_usd 0.005827` — identical to the session's own `result` usage and `total_cost_usd`.

### Recorder concurrency

50 simultaneous appends of ~2 KB → 51 lines, 51 valid JSON objects, 51 distinct ids.

## Fitness functions (Definition of Done, DoD)

Run on the final tree of branch `064-auto-checagem-e-livro-de-ponto`.

| Check | Expected | Result |
|---|---|---|
| `scripts/check-ledger.sh` (new) | green | ✓ 77 checks (recorder, report, Stop hook, settings merge) |
| `claude plugin validate` + `claude plugin test mods/maestro-ledger` | green | ✓ validation passed · 16 pass, 0 fail |
| `scripts/check-installed.sh` | green | ✓ fresh install runs every gate it ships; every hook named in `settings.json` exists and is executable |
| `check-install` · `check-language` · `check-links` · `check-flags` · `check-boundary` · `check-version` · `check-adr` · `check-agents` · `check-roles` · `check-retro` | green | ✓ all ten |
| `check-conformance.sh --ticked-only` | green | ✓ 23 cycles |
| `package-plugin.sh --verify` | green | ✓ 33 files in sync |
| `check-evals.sh` · `check-chapters.sh` | — | ✗ **red on `main` before this cycle** (stale eval baseline; open finding `achado-063-quatro-skills-sem-capitulo`); not touched here |
| `check-cycle.sh` (advisory in CI) | — | ✗ the first four commits are prefixed `064:`, which the gate does not read as a citation (it needs `ciclo 064`). Rewriting published history needs a force push — not done without the owner's order. A squash merge titled with `ciclo 064` closes it. |
| CI step for the mod | runs where `claude` exists | **declared absence**: GitHub's `ubuntu-latest` runner has no Claude Code CLI, so `claude plugin validate/test` prints `skipped` there. The mod's tests ran in this session, on Claude Code 2.1.296 (above). |

## Closing tail — the evidence
<!-- One entry per non-n/a TAIL token. What was OBSERVED, never the intention restated. -->
- TAIL:review — two independent reviews in fresh context, each by an Opus session that executed nothing in this cycle, read-only, recorded in the ledger as `kind=review`. **R1 rejected** (3 blocking, 10 important, 7 minor — the Stop hook charged in-flight work of old cycles and told the agent to untick boxes; the UPGRADE test was tautological; `--cycle` dropped every verdict). All twenty were treated in F1–F5. **R2 approved with notes**: confirmed each blocking finding resolved by re-running its own mutations, and raised N1–N7 (the spec's test script broke under the own-line rule; a verdict's `by` was self-declared; cycle-level verdicts did not fit the model; three rules without tests). All treated in F6–F7 and proved by mutation below. Full texts: R1 and R2 results kept by the manager; summary in `tasks.md`.
- TAIL:security — risk class **medium**: the cycle writes into third-party `settings.json`, runs a hook at every response, and reads text from other sessions. Checked: the recorder is called with an argument vector, never a shell, and serialises with `json.dumps` (no line injection); the Stop hook runs a conformance script only under `$CLAUDE_PROJECT_DIR`, never from the event's `cwd` (test: a foreign `check-conformance.sh` is not executed); `UPGRADE` replaces only a `hooks` object identical to one we shipped (third-party hooks: `CONFLICT`, file byte-identical, `cmp`); a forged TASK tag from another session cannot take over an open task, cannot move it to a lower attempt, and a verdict counts only when its session is the auditor's own. Declared, not fixed: tags are not authenticated; the mod runs the open repository's `record-task.py`, so `--scope user` is advised against in the installed protocol. The workers' sandbox refused to edit the mod's hook files — observed and respected, not bypassed.
- TAIL:mutation — every gate created or changed here was broken on purpose and seen refusing. `check-ledger.sh`: UPGRADE M-a/M-b/M-c (wrong matcher, hooks not replaced, third-party keys dropped), Stop hook without the cycle argument, ignoring `$CLAUDE_PROJECT_DIR`, `errors="strict"`, report counting attempt 2 as first pass, `--cycle` dropping verdicts, non-judge verdicts counted, session check removed, `-cycle` not recognised, pairing without attempt (R-f) and without session (R-g), unmeasured stop counted as zero, recorder accepting `attempt: true` and `attempt: 0` — each made the gate exit 1. `check-installed.sh`: `stop-conformance.py` and `report-tasks.py` removed from the copy list → red. Mod tests: 19 mutations of `register.ts`/`tags.ts`, 18 killed; M16 (`origin?.kind` → `origin.kind`) is equivalent — the engine always stamps `origin`. Two survivors were found on the way and closed by stronger tests (M6, M4, M13 in the mod; the comment-only `errors=` mutation in F1).
- TAIL:gate — DoD green (table above, with the two pre-existing reds and the advisory `check-cycle` declared). Guardian work done by the manager: every worker delivery re-run before its verdict. **Human gate granted** by the owner on 2026-10-12, in chat: "Pode mandar para dev e main esta do mod" — after the competing cycle-064 branch (educational material) was cancelled. Merged into `dev` and promoted to `main` by `scripts/promote-main.sh`, which records the gate in `decisoes.jsonl`. Still open, declared: the live two-session test (`spec.md`, test script, steps 4–5).

## Requirement coverage
- FR1 (Stop hook in the installer): `install-maestro.sh` copies and keeps it; `check-installed.sh` proves it executable in a fresh install.
- FR2 (`UPGRADE`): `merge-settings.py` + installer; real install over v0.3.0 → `upgraded`, third-party → refused; `--dry-run` → `would upgrade`.
- FR3 (recorder travels): `record-task.py` and `report-tasks.py` installed and executable.
- FR4 (mod through the marketplace): second entry, `claude plugin validate .` ✓; the installer prints the optional step for Claude Code only.
- FR5 (installable protocol): `docs/governance/task-ledger.md`, glossary, one line in the generated `CLAUDE.md` block.
- FR6 (report): `report-tasks.py` — by kind, cycle, model; first-pass approval; rework; cache rate; orphans; unmeasured; cycle verdicts.
- FR7 (gates): `check-ledger.sh`, the hook check in `check-installed.sh`, CI steps (the mod step declared absent on the runner).

## Cost of this cycle — measured by the ledger it built

`python3 scripts/report-tasks.py --cycle 064`: **13 measured attempts, 29,454,615 tokens, US$ 12.36**
(implement 2.15 · docs 1.31 · fix 2.56 · review 6.34), cache rate **96.7%**, rework US$ 0.13. Three
attempts are **not measured** — 064-T7#2, 064-F3#1, 064-F7#1, run by the manager session, which had no
mod loaded — and are shown as such, never as zero.

## Errors of the executor, recorded

- The manager wrote a duplicate `verdict` line attributed to `064-R1` after the mod had already
  recorded it. The ledger is append-only, so the line stays; the report now ignores it (its session
  is not the auditor's). It was this error that made finding N2 concrete.
- Commit `0ac6c77` was needed because the first push shipped a `settings.json` naming a hook the
  installer did not copy — every response of an installed project would have run a missing file.
- The executor's own Stop hook caught this report: `TAIL:security` was ticked with an evidence
  quoting the TASK tag in double brackets, and `is_placeholder` reads any `[` as an unfilled
  skeleton — the hook blocked the hand-over, the evidence was reworded. Observation for a later
  cycle: that rule also refuses a legitimate evidence that quotes brackets.
- Nested worker sessions inherited the manager's session id (measured; `env -u` did not change it);
  pairing therefore keys on task, session **and** attempt, and the limit is declared.

## Pending gate
- dev -> main promotion awaits human approval.
