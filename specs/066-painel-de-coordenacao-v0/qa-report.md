# QA report 066 — Painel de coordenação v0

- **Date**: 2026-10-20 · **Lane**: full · **Verdict**: DoD green · independent review APPROVE_WITH_NOTES (notes treated) · security: medium class confirmed, two medium findings declared as debt · awaits the human gate

> Retroactive cycle: the code is `painel-controle` `a1172a2` (12 commits, 01–03/10/2026, Hindiana
> team), merged `--no-ff` as `023694b`. Everything below was **run on this Windows machine**
> (Git Bash, `python3` shim, `PYTHONUTF8=1`, `core.autocrlf=false`), in the worktree
> `integra/linha-paralela-066`. Nothing here is claimed from memory.

## Fitness functions (DoD)

| Check | Expected | Result |
|---|---|---|
| `python -m unittest discover -s painel/tests -p test_painel.py` | Ran 12, OK | `Ran 12 tests in 3.406s` / `OK` ✅ |
| `python -m pytest .maestro/controle/git-hooks/test_veredito_hook.py -q` | 34 passed | `34 passed in 22.74s` ✅ |
| `git diff --stat a1172a2 HEAD -- painel .maestro` | only the fixture swap and the moved ADR | 7 files: `mcp_painel.py` 2, `registrar.py` 8, `server.py` 2 (docstring paths), `hindiana.json` −42, `exemplo.json` +39, `adr-rascunho-painel.md` moved, README ✅ |
| `python painel/ingest.py painel/projetos/exemplo.json` | runs without error on this repository | OK: `specs 64`, `decisoes 155`, `commits 143`, `worktrees 3`, `documentos 33`, `desvios 0` (no retro source declared), `eventos 0` ✅ |
| `git status -s -- painel/dados` after ingest | empty (`.db` ignored) | 0 lines — `painel/.gitignore:1` `dados/` ✅ |
| `grep -c 'ThreadingHTTPServer(("127.0.0.1"' painel/server.py` | 1 | `server.py:473` ✅ (confirmed by the security pass) |
| triggers on `eventos` | `eventos_sem_update`, `eventos_sem_delete` | `ingest.py:76-79`, covered by `test_painel.py:102` ✅ |
| `registrar.py … peca` without `--evidencia` | exit 2 before INSERT | `valida_evento` `server.py:383-388` → `registrar.py:39-41` returns 2 ✅ (CLI test itself: debt, cycle 072) |
| `grep -rin "hindiana\|Gilsiley" painel/*.py` | **declared debt, not green** | 4, all in `server.py` (25 comment, 87 `"Hindiana Office"`, 275 and 342 `"Gilsiley"`); the 4 in `registrar.py` and 1 in `mcp_painel.py` of `a1172a2` were docstring paths, gone with the fixture ✅ (measured, recorded) |
| `grep -c proxy painel/server.py` / `painel/index.html` | ≥ 1 each | `server.py:156,176` `proxy_entregas_por_repo`; `index.html:437` "proxy, não é deploy" ✅ |
| `scripts/check-boundary.sh` | green | ✓ every file has a domain (`painel/`, `.maestro/` in `toolkit.owns`) ✅ |
| `scripts/check-language.sh` | green | ✓ the installable surface is in English ✅ |
| `scripts/check-adr.sh` | green | ✓ 19 ADR(s), index agreeing ✅ |
| `scripts/check-links.sh` | green | ✓ 336 relative links resolve ✅ |
| `scripts/check-version.sh` | green | ✓ every place states 0.3.0 ✅ |
| `scripts/check-conformance.sh 066` | green after this file | before: `✗ missing qa-report.md` only; re-run recorded at the bottom |
| `git log --follow --oneline docs/adr/0022-*` | history of the draft preserved | **only `4919f4a`**: `git mv` was used, but the content was rewritten in the same commit beyond the rename threshold, so `--follow` does not reach `painel/docs/adr-rascunho-painel.md` (`6f5214b`, 01/10). Declared, not hidden: the origin is written in the ADR header and the draft stays reachable at `arquivo/paralela/painel-controle` ⚠️ |

## Closing tail — the evidence

- **TAIL:review** — independent review in fresh context (agent `review`, read-only, no shell: measured by file reading and the worktree reflog), on HEAD `5161449` against `plan.md` and `spec.md`. **APPROVE_WITH_NOTES**, three notes, all treated in the next commit: (1) `spec.md:135` promised a CLI test the plan had moved to debt → spec now says "adiado para o 072, tarefa T9"; (2) the plan cited one hook test for the refusal case and none for the acceptance case → `plan.md` DoD row now names three refusal tests and three acceptance tests (`test_normal_aceita`, `test_hora_texto_igual_commit_aceita`, `test_hora_texto_dentro_tolerancia_aceita`); (3) `exemplo.json` pointed `decisoes` at the JSONL under the markdown-table key, so the example panel would show zero decisions → key changed to `decisoes_jsonl`; ingest now reads **155** decisions (above). The reviewer also confirmed: fixture swap complete, ADR 0022 content = plan decisions 1–7, index/operating-model/boundary/CHANGELOG/roadmap coherent, Constitution Check 8/8 with Principle IV violation justified, all four TAIL boxes unticked at review time. It asked for three measurements it could not run — pasted in the DoD table above (`git diff --stat`, `git log --follow`, `ingest.py`).
- **TAIL:security** — pass by agent `security` in fresh context (read-only), full text in `security-pass.md`. Risk class **medium** confirmed. Findings: (média) CSRF/DNS-rebinding on `POST /api/eventos` and `/api/reingerir` — `127.0.0.1` bind (`server.py:473`) and `client_address` check (`:438`) do not stop a page in the user's own browser; no `Host`/`Origin` check. (média) `autor` is a free string via MCP (`mcp_painel.py:31-41`) and HTTP (`server.py:364`): a connected model can impersonate the human gate (Principle II). (baixa) `PROIBIDOS` (`ingest.py:25`) covers `.env*` but `expande()` follows symlinks and `..` outside `raiz`. (baixa) `/api/meta` exposes `contatos`. OK: SQL parameterized, `subprocess` as list, `esc()` on every injected string, file whitelist, hook executes nothing from the commit. **Decision of this cycle**: retroactive, code of `a1172a2` enters as is; findings 1, 2, 3 and 6 are **debt with an owner** (cycle 072 rewrites the HTTP/MCP surface). Until then: do not connect the panel's MCP to a model session; do not browse other pages while the panel is open.
- **TAIL:mutation** — two gates touched. (a) `boundary.json` (input of `check-boundary.sh`): `painel/` removed from `toolkit.owns` → `scripts/check-boundary.sh` exit **1** (unclassified path); file restored byte-identical (`git status -s -- boundary.json` → 0 lines) → green again. (b) `veredito_hook.py`: a verdict file without `Objeto:`/timestamp must be refused — proven by the hook's own suite (`test_sem_linha_objeto_rejeita`, `test_hash_inexistente_rejeita`, `test_veredito_anterior_ao_objeto_rejeita` → exit ≠ 0; `test_normal_aceita` → 0), `34 passed`. A standalone mutation in a temporary repository was attempted and **refused by the session's permission classifier** (creating a git repo under `%TEMP%`); the suite is the evidence, and the refusal is recorded here rather than worked around.
- **TAIL:gate** — DoD green above, with the two declared yellows (ADR history not followable by `git log --follow`; Hindiana coupling as measured debt). Guardian work: conformance `066` re-run after this file. **What awaits the human (Darú)**: the merge of `integra/linha-paralela-066` into `dev` (the push of this branch is itself blocked by the `deny` rule in `.claude/settings.local.json` written for the Workers — the Darú decides the exception for the MAESTRO session or pushes by hand), the TAIL:gate tick, and the acceptance of the two medium security findings as debt of cycle 072.

## Requirement coverage

- **FR1** (rebuildable ingestion): `ingest.py` on the fixture, 64 specs / 155 decisions / 143 commits, re-runnable; `painel/dados/` ignored.
- **FR2** (append-only `eventos`, verifiable timestamp): triggers `ingest.py:76-79`; `--ts` option of `registrar.py` lets the author supply the timestamp — **declared debt** (plan §escopo), not fixed here.
- **FR3** (evidence-gated `registrar.py`): exit 2 without `--evidencia`; CLI-level test is debt of 072.
- **FR4** (localhost server + `/api/estado-ia`): bind `server.py:473`; `voce.estado`, `voce.peca`, `voce.proximo` at `:315-316`; 13 GET + 2 POST routes in `contracts/interfaces.md`.
- **FR5** (MCP stdio): three tools in `mcp_painel.py`; `autor` forgeable — debt (security finding 2).
- **FR6** (eleven screens): `index.html`, unchanged from `a1172a2`.
- **FR7** (per-project JSON config, nothing project-specific in code): `exemplo.json` replaces `hindiana.json`; 4 literals remain in `server.py` — debt, measured above.
- **FR8** (veredito pre-commit hook): 34 tests, six named for the two cases.
- **FR9** (tests shipped with the code): 12 + 34, run here.
- **Out of scope respected**: no promotion/merge/deploy from the panel; no auth or network exposure added; no installer packaging; no book rewrite. Undeclared scope decided in the plan: `auditoria_metodo.py`, `arquitetura.html`, `roteiro-painel.md`, types `nota`/`recuperacao` **delivered as is**; `--ts` **debt**.

## Findings and fixes inside the cycle

- The first version of the retroactive spec claimed four things the code does not do (hook suite is pytest; "hindiana" absent from `painel/*.py`; `/api/estado-ia` returns `proximo_passo`; a localhost grep that matched `or ""`). Caught by the first fresh-context review (RETURN), each confirmed with `git show` on `a1172a2`, corrected in `ad90927` before the plan was written. Root cause: the spec author could not read the branch; the criteria were written from the proposal document, not from the code.
- `exemplo.json` used the markdown-table key for a JSONL source (zero decisions on screen). Caught by TAIL:review; one-key fix; ingest now reads 155.
- A PowerShell here-string put a literal `` `n `` inside `exemplo.json` (invalid JSON for one minute); caught by `json.load`, fixed with a plain edit.
- `git log --follow` does not connect ADR 0022 to its draft: rename + rewrite in one commit. Recorded as a yellow; the lesson for cycles 067–071 is to `git mv` in one commit and rewrite in the next.
- `record-decision.sh` cannot be called from PowerShell on this machine (BOM and quoting); a Python helper with the same validations was used — finding for the retrospective (`achado` to open), not silenced.
