# QA report 068 — Chamados gate a gate

- **Date**: 2026-10-20 · **Lane**: full · **Verdict**: DoD green with two declared yellows (BPMN lacks a G8 gateway; mutation (b) first attempt was a no-op) · security: medium class, six lows, none blocking · independent review: see tail · awaits the human gate

> Retroactive cycle: the code is the slice `db6b89c..2796cbf` of the parallel branch
> `067-painel-chamados` (10 commits, 03–09/10/2026, Hindiana team), merged `--no-ff` as
> `120a32c`. Everything below was **run on this Windows machine** (Git Bash, `python3` shim,
> `PYTHONUTF8=1`, `core.autocrlf=false`) in the worktree `integra/linha-paralela-066`, through
> scripts in the session scratchpad (`mut068.sh`, `mut068b.sh`).

## Fitness functions (DoD)

| Check | Expected | Result |
|---|---|---|
| `python -m unittest discover -s painel/tests -p test_chamados.py` | Ran 6, OK | `Ran 6 tests in 0.010s` / `OK` ✅ |
| `python -m unittest discover -s painel/tests -p test_painel.py` | Ran 12, OK | `OK` ✅ |
| `python painel/custo.py painel/projetos/exemplo.json` (1st run) | reads this repo's transcripts | `{"arquivos_lidos": 5, "mensagens_novas": 311}` ✅ |
| same, 2nd run (offset proof) | fewer files, fewer messages | `{"arquivos_lidos": 1, "mensagens_novas": 8}` ✅ (only the live session's file moved) |
| `grep -o 'exclusiveGateway id="G[0-9D]"' painel/workflow-chamado.bpmn \| sort -u \| wc -l` | 11 (one per gate in `GATES`) | **10** — ids `G0–G7, G9, GD`; **no `G8` gateway in the BPMN** while `chamados.py` `GATES` has 11 ⚠️ declared gap (the order-of-production decision is modelled as `G_aceita`/`G_dec`, not as a gate node) |
| `git diff --stat bb90987 120a32c` | the 068 slice + fixture swap | 12 files: `chamados.py` +420, `custo.py` +143, `index.html` +287, `server.py` +13, `workflow-chamado.bpmn` +643, `test_chamados.py` +85, hooks wiring; `hindiana.json` and `chamados-manuais-hindiana.json` −; `exemplo.json`, `chamados-manuais-exemplo.json` + ✅ |
| `grep -rc 'hindiana\.json\|chamados-manuais-hindiana' painel/*.py painel/index.html painel/README.md` | 0 | 0 ✅ |
| `ls painel/projetos/chamados-manuais-hindiana.json` | absent | absent ✅ (real data out; fixture `chamados-manuais-exemplo.json` in) |
| `grep -c 'Cycle 068' docs/governance/glossary.md` | 9 | 9 ✅ |
| `scripts/check-adr.sh` · `check-links` · `check-language` · `check-boundary` · `check-version` | green | rc=0 ×5 after the merge ✅ |
| `grep -rin "Gilsiley\|Hindiana Office\|180-HINDIANA" painel/chamados.py painel/custo.py` | **declared debt** | `chamados.py:28,154-155`; `custo.py:33-34,48` — measured, debt of 072 ✅ (recorded) |
| `scripts/check-conformance.sh 068` | green after this file | re-run recorded at the end |

## Closing tail — the evidence

- **TAIL:review** — independent review in fresh context (agent `review`, read-only, no shell: ripgrep over the worktree), on `120a32c` plus the uncommitted artifacts, against spec, plan, tasks, data-model and contracts. **RETURN**, two blocking items, both in my artifacts, both treated before this file was committed: (1) the plan's `DOM:ports` reason cell carried `GET /api/chamados/{id}/trilha` and `is_skeleton()` reads an angle bracket as a placeholder — the gate indeed printed `✗ domain ports: declared DOM:ports=changed with no reason`; fixed to `{id}`; (2) the DoD expected 11 BPMN gateways, the file has 10 — `G8` is `bpmn:userTask id="T_ordem"` (line 329), not a gateway; plan, contracts and the DoD row now say 10 with the G8 exception declared (the `index.html:721` "11 gates" string is the code's own claim and stays as debt). Non-blocking, confirmed: FR1–FR9 ↔ diff ↔ tasks with file:line; `DOM:invariants=domain` is true (pure: `cabecalho`, `titulo`, `numeros_limpos`, `data`, `valida`, `confere`; impure: `_git`, `le_chamados`, `_atualiza`, `trilha`); data-model matches `GATES`/`confere` (small divergence: `data_objeto` validated but not returned — noted); contracts match `server.py:429-440` (one internal inconsistency: `GET /api/chamados` triggers `custo.indexa`, which writes `custo.db` — the contract's "no route writes" line is wrong, noted as debt); VII "no ADR needed" agreed (feature of the panel, not a rule of the method); `unittest.main()` before the last class confirmed, `discover -p` still runs 6; the four TAIL boxes were unticked at review time. One false alarm: it asked to declare `veredito_hook.py`/`test_veredito_hook.py` as undeclared scope — `git diff --name-status bb90987 120a32c` shows nothing under `.maestro/`; those files came with cycle 066. The nested text it flagged at `spec.md:111` was cleaned.
- **TAIL:security** — pass by agent `security` in fresh context (read-only), full text in `security-pass.md`. Class **medium** declared (reads the user's home); result: **no high or medium finding, six lows**. The fact that answers the owner's privacy question: `custo.py` persists **only counts** (`INSERT INTO uso (sessao, minuto, turnos, entrada, saida, cache_lido, cache_escrito)`, `custo.py:109-112`) plus session title and file path; no prompt or tool output; nothing from the transcripts reaches an HTTP response (`chamados.py:395-398` returns sums). Lows: `custo_pastas` is a substring match on the folder name (`custo.py:49`) with a real-project default (`:48`) — fix is equality and no default; `?atualizar` is a GET without Origin check (cost only); manual ticket state not visually distinct from derived state; pre-commit hook bypassable (client-side gate, not enforcement); residual real names in code and BPMN (declared coupling).
- **TAIL:mutation** — no `scripts/check-*.sh` touched; the gate of this cycle is the conferidor, proven by its six tests. Each mutation applied to a copy-restored file (`cmp` identical after each): (a) `numeros_limpos` forced to `True` → `FAILED (failures=1)` (`test_runner2_com_errors_nao_conta`); (b) **first attempt was a no-op**: renaming `pendencias_aceitas` on both the dict key (`:139`) and the lookup (`:213`) kept all 6 green — a consistent rename is not a behavioural mutation; redone as breaking the condition on `:213` (`and not the pendencias_aceitas lookup` → `and False`, G8 never blocked) → `FAILED (failures=1)` (`test_pendente_passa_o_gate_mas_trava_o_g8_ate_ser_aceita`); (c) fixture `2751/0/14` → `2751/0/0` → `FAILED (failures=1)`; (d) `--pre-commit` removed from the hook wiring → `grep -c -- --pre-commit` = 0. Final run after restore: `OK`.
- **TAIL:gate** — DoD green with the two yellows above. **What awaits the human (Darú)**: the merge of `integra/linha-paralela-066` into `dev` (now cycles 066, 067, 068), the `TAIL:gate` tick, and one decision raised by the spec: `custo.py` reads `~/.claude/projects/{folder}/*.jsonl` — acceptable in an installed tool? Recommendation from the security pass: yes, with `custo_pastas` mandatory and matched by equality (debt of 072). Whether the BPMN should gain a `G8` node is a question for the cycle that next touches the BPMN.

## Requirement coverage

- **FR1** (state derived from files, never typed): `chamados.py` `confere`; manual entries labelled `registro="manual"` (`:289`).
- **FR2** (conferidor rules a–g): `cabecalho`, `valida`, `numeros_limpos`, `confere`; rules (a), (b), (e), (f), (g) have a named test; (c) second half, (d) latest-hash-wins and FR4 classe C have **no named test** — debt of 072 (plan, Complexity Tracking).
- **FR3** (`pendente:` passes the gate, blocks G8): `:213-217`; mutation (b2).
- **FR4** (classe C needs ADR + owner decision): `:151-155`; untested — debt.
- **FR5** (board chamado × gate): `index.html`, commit `e38a09c`.
- **FR6** (trilha with cost per step): `/api/chamados/<id>/trilha`, `chamados.py:383,395-398`.
- **FR7** (incremental cost index): `custo.py`, offset proven by the two runs above.
- **FR8** (BPMN as the documented flow): `workflow-chamado.bpmn`, 10 gate gateways — **G8 missing**, declared.
- **FR9** (tests shipped): 6, run here; note `test_chamados.py:69-70` has `unittest.main()` before the last class — `discover -p` still finds 6; running the file directly would run 5 (debt).
- **Out of scope respected**: no POST, no auth, no installer change; no fix to the coupling (declared).

## Findings and fixes inside the cycle

- Real Hindiana data (`chamados-manuais-hindiana.json`, 1133 hand-typed lines) was in the merge; removed and replaced by a fixture per `decisao-066-daru-20-10`; two docstrings repointed.
- The spec pointed `ux-design` at `specs/066-painel-de-regencia/`, a folder that does not exist in this branch; corrected to the v0 pointer, with the real semantic design named by branch.
- Mutation (b) as first written was a rename, not a mutation — recorded above rather than silently redone; lesson for 069–071: mutate the condition, not the identifier.
- The BPMN/`GATES` mismatch (10 vs 11) surfaced only because the DoD counted gateway ids against the code's table — a count the plan wrote expecting 11.
