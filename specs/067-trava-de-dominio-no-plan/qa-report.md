# QA report 067 — Trava de domínio no plan

- **Date**: 2026-10-20 · **Lane**: full · **Verdict**: DoD green · independent review APPROVE_WITH_NOTES (the two gate-blocking notes treated: ADR 0023 written, CHANGELOG and roadmap updated) · security: low class, green · awaits the human gate

> Retroactive cycle: the code is `trava-dominio-plan` `db6b89c` (3 commits, 02–03/10/2026,
> Hindiana team), merged `--no-ff` as `b5775ac`. Everything below was **run on this Windows
> machine** (Git Bash, `python3` shim, `PYTHONUTF8=1`, `core.autocrlf=false`), in the worktree
> `integra/linha-paralela-066`, through scripts kept in the session scratchpad
> (`mutate-dom.sh`, `gate067.sh`) because PowerShell mangles `|` and `$(` inside quoted bash.

## Fitness functions (DoD)

| Check | Expected | Result |
|---|---|---|
| `grep -c 'DOM:' .specify/templates/plan-template.md` | 4 | 4 (`plan-template.md:66-69`) ✅ |
| `scripts/check-conformance.sh 066` | green; prints the floor notice | `· domain-model declarations: not checked below cycle 67`; `✓ every cycle checked …` ✅ |
| `MAESTRO_MIN_CYCLE_DOMAIN=abc scripts/check-conformance.sh 066` | exit 2, "is not a number" | `✗ MAESTRO_MIN_CYCLE_DOMAIN='abc' is not a number — refusing to run with an unreadable floor.` rc=2 ✅ |
| `MAESTRO_MIN_CYCLE_DOMAIN=99 scripts/check-conformance.sh 066` | exit 2, "above the built-in floor" | `✗ MAESTRO_MIN_CYCLE_DOMAIN=99 is above the built-in floor 67 — this knob may only tighten the rule, never relax it.` rc=2 ✅ |
| `scripts/check-conformance.sh 067` (plan intact, qa-report present) | "domain model declared … with a reason" | `✓ Constitution Check complete (8/8)`, `✓ acceptance criteria …`, `✓ all 5 conditional artifacts …`, `✓ domain model declared (aggregate, invariants, glossary, ports) with a reason` ✅ (red only on the tail placeholders before this file was filled) |
| `python -m unittest discover -s painel/tests -p test_painel.py` | Ran 12, OK | `OK` (12) ✅ |
| `grep -c 'DORA counts production only' painel/server.py` | 1 | `server.py:158` `_ambiente(e) in ("", "production", "producao", "produção")` ✅ |
| `grep -c 'sem plan ou tasks' painel/index.html` | 1 | `index.html:293` (and `:299`) ✅ |
| `grep -c 'Cycle 067' docs/governance/glossary.md` | 5 | 5 (aggregate root, declared domain model, invariant, port/adapter, ubiquitous language) ✅ |
| `scripts/check-language.sh` · `check-boundary.sh` · `check-links.sh` | green | ✓ ✓ ✓ (after the merge) ✅ |
| `git diff --stat fafae7d b5775ac` | 4 files, no conflict | `.specify/templates/plan-template.md` +22, `scripts/check-conformance.sh` +62, `painel/server.py` +12/−5, `painel/index.html`; `git merge-tree` → 0 CONFLICT ✅ |

## Closing tail — the evidence

- **TAIL:review** — independent review in fresh context (agent `review`, read-only, no shell: rules of block 3b applied by hand to the plan's table), on `b5775ac` against `plan.md` and `spec.md`. **APPROVE_WITH_NOTES.** Two notes blocked the human gate and were treated here: (1) no ADR came with the merge although the cycle adds a rule to the method — `principles.md` § Governance requires one → **ADR 0023** written, indexed, decision recorded in `decisoes.jsonl`; (2) CHANGELOG Unreleased and `docs/roadmap.md` had no 067 → entry and phase **F31** added. Non-blocking, confirmed: FR1–FR6 ↔ diff ↔ tasks complete, undeclared scope (the "sem qa-report" counter) declared in the spec; the plan's DOM table passes block 3b as written (`edge(...)` captured as `edge`, reason = parenthesised text + Why cell); Constitution Check 8/8 with IV justified and VII traced to T6, T4, C7, C12 in `axioms.md` (all exist); one criterion without a grep (FR5 "falta" in the Plan column) — added as debt; the DORA filter test debt is the **second consecutive** Principle IV violation (066, 067), which T6 says should become a rule — left to the Darú.
- **TAIL:security** — pass by agent `security` in fresh context (read-only), full text in `security-pass.md`. Risk class **low** confirmed (effective class: read). Findings: (baixa) block 3b has no injection path — plan content enters `sed` only via stdin, `${k}` is a constant; a `)` in a code span or a `|` in the Why cell yields a false red, never a false green; the only false-green path is `grep -m1` taking a prose mention before the table, and `edge(x)` accepting a one-character reason — fix for the next cycle touching 3b. (baixa) The floor knob fails closed: `10#` handles leading zeros, out-of-range only tightens or exits 2. (média, inherited) DORA can be inflated by a forged `deploy` event whose `ambiente` is free text and whose absence counts as production — same class as 066 finding 2, already debt of 072; 067 only subtracts deploys. No secret, network or write in the diff.
- **TAIL:mutation** — the gate this cycle created (block 3b of `check-conformance.sh`) was broken on purpose through the cycle's own plan, each time restored byte-identical (`cmp`): (a) the `DOM:glossary=` line deleted → `✗ domain model never declared in plan.md: glossary`, rc=1; (b) `DOM:invariants=edge` with the Why cell emptied → `✗ domain invariants: declared DOM:invariants=edge with no reason — a declaration without a why is silence`, rc=1; (b') itemized `regra_portao=domain | regra_dora=edge` → `✗ domain invariants: 'regra_dora=edge' is edge with no reason — write regra_dora=edge(why …)` **and** a second line treating the Why cell as a bogus item (`'Borda **decidida** …' — each item is rule=domain or rule=edge(why)`), which **measures the known defect** of the itemized form in a table row (ADR 0023 § Consequências); (c) `MAESTRO_MIN_CYCLE_DOMAIN=abc` → rc=2, `=99` → rc=2 (above). First observation: with `qa-report.md` absent the gate stops at "missing qa-report.md" and never reaches block 3b — the mutations only became observable after this file existed, which is itself a fact about the gate's order (recorded, not hidden).
- **TAIL:gate** — DoD green above. Guardian work: conformance `067` re-run after this file. **What awaits the human (Darú)**: the merge of `integra/linha-paralela-066` into `dev` (now carrying cycles 066 and 067), the `TAIL:gate` tick, the acceptance of ADR 0023 as written, and the decision the review raised: two consecutive cycles with tests after code (Principle IV) — rule or exception.

## Requirement coverage

- **FR1** (four DOM declarations with a reason in the plan template): `plan-template.md:49-69`.
- **FR2** (gate reads them from 067 on, soft-fails): block 3b `check-conformance.sh:353-399`; mutations (a), (b), (b').
- **FR3** (floor numeric, tighten-only, fail-closed): `:57-67`; mutations (c).
- **FR4** (itemized invariants): `:369-389`; mutation (b'); defect with the table's `|` declared.
- **FR5** (panel marks spec without plan/tasks): `index.html:293,299`; "falta" in the Plan column has no grep yet — debt.
- **FR6** (DORA counts production only): `server.py:158`; no test for the filter — debt (second consecutive Principle IV violation).
- **Out of scope respected**: no hard gate in CI; no validation of the reason's content; no separate domain-model file; the "sem qa-report" counter declared as delivered.

## Findings and fixes inside the cycle

- The merge brought no ADR for a change to the method. Caught by the review; **ADR 0023** written in this cycle, not deferred.
- The itemized invariants form breaks on the Markdown table's `|`: caught by the planner reading block 3b, confirmed by mutation (b') printing a bogus-item line. Recorded in ADR 0023 with an owner.
- The gate's order hides block 3b behind "missing qa-report.md": three mutation runs produced identical logs until the qa-report existed. Lesson for 068–071: create the qa-report skeleton before running mutations.
- PowerShell rewrites `|`, `\|` and `$(` inside quoted bash commands on this machine; every gate run and mutation went through a `.sh` file in the scratchpad. Same retrospective finding as `record-decision.sh` in 066.
