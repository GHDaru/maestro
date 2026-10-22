# QA report 069 — Conferidor pela data

- **Date**: 2026-10-20 · **Lane**: full · **Verdict**: DoD green · independent review APPROVE_WITH_NOTES (two items fixed) · security OK (one pre-existing medium as debt) · awaits the human gate

> Retroactive cycle: Hindiana chamado 070, slice `2796cbf..aa0efd1` of the parallel branch
> `067-painel-chamados` (21 commits, 09/10/2026), merged `--no-ff` as `23f8325`. Measured on
> this Windows machine (Git Bash, `python3` shim, `PYTHONUTF8=1`, `core.autocrlf=false`) in the
> worktree `integra/linha-paralela-066`, via `mut069.sh` in the session scratchpad.

## Fitness functions (DoD)

| Check | Expected | Result |
|---|---|---|
| `python -m unittest discover -s painel/tests -p test_chamados.py` | Ran 10, OK | `Ran 10 tests in 0.009s` / `OK` ✅ |
| `python -m unittest discover -s painel/tests -p test_painel.py` | Ran 12, OK | `OK` ✅ |
| `ls specs/070-conferidor-ordem-veredito/` | 10 files | `00-chamado.md`, `G0-reproducao.md`, `G1-W11.md`, `G2-vermelho-W13-6741315.md`, `G3-codigo-W10.md`, `G3-criterio-W01-d2822ef.md`, `G3-runner2-W13-98a62a1.md`, `G3-runner2-W13-d2822ef-8adb545a.md`, `GD-risco.md`, `spec.md` ✅ |
| `git diff --stat 2796cbf aa0efd1` | 12 files, +485 | 12 files changed, 485 insertions, 1 deletion ✅ |
| `git merge-base --is-ancestor 2796cbf aa0efd1` | yes (clean descendant) | rc=0 ✅ |
| `git diff --stat aa0efd1 699bddb -- specs/070-*` | the side branch adds nothing | 8 files, **344 deletions, 0 insertions** — `699bddb` only lacks files; left out, kept in tag `arquivo/paralela/w10-070-g3-codigo` ✅ |
| the new rule in code | one pure function | `MINIMO` `chamados.py:112`; `ordem_veredito` `:115-118`; applied `:151`; `grep -c ordem_veredito` → 2 ✅ |
| `grep -c 'Cycle 069' docs/governance/glossary.md` | 2 | 2 ✅ |
| `scripts/check-conformance.sh 066/067/068` after the 068 edits | green ×3 | rc=0 ×3 ✅ |
| `git merge-base --is-ancestor 6741315 d2822ef` | 0 (red before green) | rc=0 ✅ |
| `git show --stat 6741315` / `d2822ef` | red touches only tests; green only the code | red: `test_chamados.py` +27, `spec.md` +30; green: `chamados.py` +11/−1 ✅ |
| `grep -c 'veredito: FALHA_ESPERADA' specs/070-*/G2-*.md` · `APPROVE` in G3-* · `escopo: correcao` · `def test_` | 1 · ≥2 · 1 · 10 | 1 · 2 · 1 · 10 ✅ |
| `git diff --stat aa0efd1 HEAD -- specs/070-conferidor-ordem-veredito` | empty (evidence unedited) | 0 lines ✅ |
| `git diff --exit-code -- painel/chamados.py` after the mutations | clean | clean ✅ |
| `scripts/check-conformance.sh 069` | green after the plan and this file | re-run recorded at the end |

## Closing tail — the evidence

- **TAIL:review** — independent review in fresh context (agent `review`, read-only, no shell), on `23f8325` plus the uncommitted artifacts. **APPROVE_WITH_NOTES**, two items to fix before the gate, both in this file and both fixed: (1) the mutation (a) line named `test_r4` as a failing test without an observed output — plan, tasks and the real G2 file name `test_empate` and `test_mais_novo`; re-run with the names captured (above) confirms the reviewer; (2) the DoD lacked the measurements the plan requires (merge-base of the red/green pair, the gate greps, the diff of the 070 folder, the post-mutation diff) — added above, all green. Notes treated: the `or MINIMO` branch is dead code through `confere()` in every scenario, not only the tested one (plan wording fixed); the glossary Veredito line now points at "veredito vigente". Noted, immutable: `G3-codigo-W10.md:4` says classe B while `GD-risco.md:4` says classe A. Confirmed by the reviewer: FR1 to FR5 with file:line, scope exactly 12 files, DOM table passes block 3b by hand, Principle IV holds for FR1 (G2 by W13, non-author), four TAIL boxes unticked at review time.
- **TAIL:security** — pass by agent `security` in fresh context (read-only), full text in `security-pass.md`. Class **low** declared; result OK, no blocker. One pre-existing **medium**: `data()` (`chamados.py:74-78`) lets `strptime` raise on a calendar-invalid date such as 2026-13-01, and the exception propagates through `confere()` and `le_chamados()` into the `except` of `_atualiza` (`:323`), so the whole panel view goes to error, not just one ticket — one-line fix (try/except returning None), debt of 072. Low: the author date that the "typed hour" check trusts (`:139-142`) is forgeable via GIT_AUTHOR_DATE, inside the declared trust model (whoever commits is already a critic). The ten gate files carry no secret, token, IP or personal data; they name another project (repo name, a spec id, hashes) and session roles only.
- **TAIL:mutation** — no `scripts/check-*.sh` touched; the gate of this cycle is the sort rule, proven by its tests. Each mutation applied to a copy-restored `chamados.py` (`cmp` identical after each): (a) `ordem_veredito` returns a one-element tuple of the file name — the old alphabetical behaviour restored → `FAILED (failures=2)` (observed names: `test_empate_de_data_desempata_pelo_commit_do_arquivo`, `test_mais_novo_vence_mesmo_vindo_antes_no_alfabeto` — the first version of this line named `test_r4` without having read the output; corrected after the review, see Findings); (b) `or MINIMO` replaced by a year-2999 date, so an unreadable date would count as newest → `Ran 10 tests` **OK — the mutant survives**. Diagnosed, not hidden: `valida()` (`:86`) appends "data fora do formato" for any unparseable `data:` and such a verdict never reaches the sort, so and `data` is a mandatory header field (`:36-37`), so an absent date is rejected by `valida()` too (`:84-85`): the `MINIMO` branch is dead code through `confere()` in every scenario, reachable only by calling `ordem_veredito` directly. Recorded as an equivalent mutant, plus one declared test gap for the direct call (proposed `test_veredito_sem_campo_data_e_o_mais_antigo`, debt of 072). Final run after restore: `OK`.
- **TAIL:gate** — DoD green above with one declared gap (the absent-date test). Guardian work: conformance 069 re-run after the review line. **What awaits the human (Darú)**: the merge of `integra/linha-paralela-066` into `dev` (now cycles 066 to 069, 36 commits), the `TAIL:gate` tick, and the one ambiguity the spec raises for him: whether Maestro adopts the Hindiana per-cycle gate-file standard (G0 to G9 as files) as its own, now that this cycle proves it works inside the Maestro repository — that decision would get its own ADR in its own cycle.

## Requirement coverage

- **FR1** (latest header date wins, tie by file commit then name): ordem_veredito :115-118, applied :151; red 6741315 → green d2822ef; mutation (a).
- **FR2** (unreadable date never wins): enforced by alida() :86, test 	est_r3_veredito_sem_data_legivel_nao_vence; regression test on behaviour already in the base, as the G3-criterio file states.
- **FR3** (trilha in date order): eventos.sort :393, test 	est_r4_trilha_em_ordem_de_data_nao_de_nome; regression test, same note.
- **FR4** (red test before the fix): the pair above; git merge-base --is-ancestor 6741315 d2822ef → 0.
- **FR5** (the chamado folder as immutable evidence): specs/070-conferidor-ordem-veredito/, 10 files, unedited since a0efd1.
- **Out of scope respected**: no route, no reader, no ADR; the stale side branch 699bddb left out, kept in its tag.

## Findings and fixes inside the cycle

- **The imported folder broke the full gate — and the fix is in the gate, not the folder (decision B1, 21/10).** `specs/070-conferidor-ordem-veredito/` matches `specs/NNN-*`, so `check-conformance.sh` charged it for plan, tasks and qa-report and `promote-main.sh` would have aborted on `dev`. Copying 069's artifacts into it (the owner's first idea) was rejected: it would duplicate function (Principle VI) and claim evidence for a cycle that is not one. The gate now exempts **by shape** — a folder with `00-chamado.md` and `G*-*.md` and no `tasks.md` is imported evidence (ADR 0024), listed with its reason and counted as inspected. Mutation observed: adding an empty `tasks.md` to the folder → `✗ missing plan.md`, `✗ missing qa-report.md` (charged again); removed → 0 changes in the folder. A first version of the exemption made a single-cycle run (`check-conformance.sh 070`) report "checked nothing" because it skipped before counting — fixed by counting the exempt folder as inspected.

- **CI caught what I ran too early locally.** The push of the integration branch (20/10, after the Darú's decision 1) failed `check-version.sh` on `7d57e27`: this cycle's CHANGELOG entry opened a second `### Corrigido` under Unreleased (line 12) while the one from cycle 065 still existed (line 68); the gate requires one section per type. My local `gates-after.sh` run had passed because it ran before the 069 entry was written. Fixed by merging the two sections; re-run and pushed. Lesson for 070 and 071: run the index gates AFTER the CHANGELOG entry, not before.

- **I claimed, then had to prove.** The first mutation (a) line in this file named `test_r4` as one of the two failing tests; I had inferred it from the test list instead of reading the runner output. The fresh-context review caught it from the code alone. The line now carries the observed names, and the lesson is recorded for the retrospective: a test name in a qa-report is a measurement, not a guess.

- Mutation (b) survived; diagnosed as equivalent in every path through `confere()` (dead branch) and as a test gap only for a direct call of `ordem_veredito` — recorded, test proposed for 072.
- The planner reported CHANGELOG and roadmap as already in 23f8325; they were written after the merge and enter with this commit — corrected here, not in the plan.
- 699bddb looked like the tip of 069 by date but descends from the old 534a088 and only lacks files relative to a0efd1; measured with git merge-base and git diff --stat before deciding.
