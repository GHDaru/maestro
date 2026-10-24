# QA report 072 — Painel de regência, rodada 1: kanban por gate e fila de decisões

- **Date**: 2026-10-24 · **Lane**: full · **Status**: **open — rodada 1 in progress** (this file
  is the skeleton created before the mutations, as the regent session asked; every section below
  is filled by whoever delivers, with command output, never intention)
- **Verdict**: to be written by the independent review (Worker06, fresh context) after the
  slices integrate

> Ruler of the cycle: the DoD of `plan.md § Verification` (**`Ran 15 tests`** — the 13 named
> tests of `c1eb802` plus the two FR16 proofs the plan gate added; the supersession
> `Ran 13 → Ran 15` is declared there, not silent). Each Worker leaves **green its own slice**
> and pastes here the hash where the red was captured and the hash of the green.
> Measured on this Windows machine, `PYTHONUTF8=1`, branch `066-painel-de-regencia`.

## Evidence per task

> One subsection per task. The worker who delivers appends the real command output under its
> subsection (hash of red, hash of green, test names). Nothing is written here before it
> happened.

### 072-T03b — tests reconciled and widened (Worker03)

- **Delivered** (`[[DONE id=072-T03b outcome=delivered]]`, 24/10): commit `42e24f4` on `w/worker03`
  ("ciclo 072: testes reconciliados e ampliados (gate do plano)"), integrated into the working
  branch in `2b0b768`. One file: `painel/tests/test_regencia.py` (+355/−97). No implementation.
- **Red captured at `42e24f4`**: `PYTHONUTF8=1 python -m pytest painel/tests/test_regencia.py -q`
  → **24 failed in 7.51s**, every one for the right reason (the `regencia/` package, the
  `fila_registro.py` adapter and the regency routes do not exist yet): F1 (served HTML has no
  `.metrica`), F9 (no labeled regency control), F2 (`painel/regencia/` missing), F3 (404 ≠ 422,
  route missing), F4-fila, F5-ruling, F4-independencia, F5-parser (`confere` does not expose
  `autor_da_peca`), F6, F7, F8, F10, F14-so-cresce (`fila_registro.py` missing), dívida5
  (schema has no TRIGGER; UPDATE passed), portão-do-regente, F20-autor-fora, F20-pedido-inexistente,
  F14-AST, F14-concorrente (404), F15-ordena, F23-cabecalho, F1-dez-colunas (404),
  F7-frentes (`frentes` absent from `/api/meta`), F11-valida-pedido.
- **Regressions**: old suite `python -m pytest painel/tests -q --ignore=painel/tests/test_regencia.py`
  → **48 passed in 15.68s**; `python painel/chamados.py painel/projetos/exemplo.json` → **exit 0**.
- **Temp files** `rg_new.txt`/`rg_old.txt` removed from the worktree (`bash rm`, exit 0).
- **Divergences reported by the worker (rule V0b iii) and decided by the regent session (MAESTRO,
  no new gate):** (a) `cabecalho_fila(itens, agora) -> {n, idade_mais_velha}` entered the
  "Nomes fixados" table of `plan.md`; (b) the plan DoD now says **`Ran 24 tests`** — declared
  supersession of `Ran 13` (spec) and `Ran 15` (plan gate); (c) the three old `index.html`
  buttons with `${…}` and no `aria-label` (`#ch-atualiza`, `.ch-cartao`, `.botoes[data-el]`)
  are labeled by Worker04 in slice A — D-072-8 keeps declaring only the JS-rendering limit;
  (d) the dispatch text `task-072-t03b.md` was untracked — committed by the MAESTRO in `dd98ad6`.

### 072-T09 — ADR 0027 + index line + glossary (Worker01 + MAESTRO)

- **Delivered in two parts, closed 24/10** — the split is by design, not accident: worker
  sessions cannot write under `docs/adr/` (permission rule `Edit/Write(docs/adr/**)`), and the
  worker **refused to route around it via shell**, reporting the block instead
  (`[[DONE id=072-T09 outcome=blocked]]` → reopened by the regent session).
- **Glossary** (Worker01, commit `d8c63b6` on `w/worker01`, integrated in `d8aa60f`):
  `docs/governance/glossary.md` with the five "Cycle 072" terms — regency panel, decision
  request, ruling, normalized verdict, regent's gate. Evidence: `grep -c 'Cycle 072'
  docs/governance/glossary.md` → **5**; `scripts/check-language.sh` → **green**.
- **ADR 0027 + ADR index + decision index** (MAESTRO, bypass, commit `fe74587`, from the
  committed draft `adr-0027-rascunho.md`): `docs/adr/0027-registro-da-fila-e-append-only-mecanico.md`
  written, line added to `docs/adr/README.md`, and the `adr-0027` line appended to
  `docs/records/decisoes.jsonl` (**171 decisions** now). Evidence: `scripts/check-adr.sh` →
  **green (24 ADRs)**. The order held: the ADR and its index line entered **before** any code of
  the queue register (W05), as the plan gate requires.
- Environment notes for the record: `python3` on this machine is the Microsoft Store alias (the
  script needs a real one in the PATH), and `scripts/check-adr.sh` here is slow (msys
  subprocesses; a worker-side run was interrupted past 120 s — environment, not a block).

### 072-T03 — pure domain + parser FR5 (Worker03)

- Dispatched (after the T03b integration; no evidence yet).

### 072-T07 — append-only triggers in the base, FR17 (Worker02)

- Dispatched (after the T03b integration; no evidence yet).

### 072-T04 — kanban routes and screen (Worker04)

- Pending (depends on T03).

### 072-T05 — decision queue: register, routes and screen (Worker05)

- Pending (depends on T03 and on the ADR 0027 index line of T09).

### 072-T08 — living journey (Worker01)

- Pending (depends on T09 and on the screens of T04/T05).

### 072-T10 — living artifacts of the closing (Worker01)

- Pending (depends on T09).

## Fitness functions (DoD) — filled by Worker06 with real output

| Check | Expected | Result |
|---|---|---|
| `python -m unittest discover -s painel/tests -p test_regencia.py` | `Ran 15 tests`, `OK`, exit 0 (supersession of `Ran 13` declared in `plan.md`) | — |
| 48 tests of the old suite (`--ignore=test_regencia.py`) | green, untouched | — |
| `python painel/chamados.py painel/projetos/exemplo.json` | exit 0 (FR5 only adds a field) | — |
| `python -m unittest discover -s painel/tests -p 'test_*.py'` | green (regression 068/069/070) | — |
| `ls specs/070-conferidor-ordem-veredito/` | 10 files (immutable folder) | — |
| `ls painel/projetos/*hindiana*` | empty (fixture rule) | — |
| `grep -rn '\.env\|settings.local.json' painel/` | no **read** path | — |
| `ls docs/journeys/072-*.md` / `grep -c 'F11'` | exists / ≥ 1 | — |
| `scripts/check-language.sh` / `check-boundary.sh` / `check-links.sh` | green | — |
| `scripts/check-conformance.sh 072` | green after plan, tasks and this file carry the evidence | — |

## Closing tail — the evidence

> The four steps below all **apply** to this cycle (none is n/a). Their evidence bullets are
> appended by Worker06 as each step actually runs; the boxes in `tasks.md` are ticked only
> while the evidence is being written. Until then this section intentionally carries no
> evidence bullets — an open cycle is red by design, and a placeholder that passes the gate
> would be the exact defect the gate exists to catch.

## Requirement coverage

- To be written by the independent review: the 25 FR of `spec.md` (revisão T01b) against the
  integrated diff, plus the "Nomes fixados" table of `plan.md` and the anti-rules 1–8 of
  `specs/066-painel-de-regencia/ux-design.md` §4.

## Findings inside the cycle

- **SendMessage to workers keeps falling (classifier unavailable).** The T03b dispatch went
  through on the second try; the T09 dispatch fell twice and was committed as
  `task-072-t09.md` (`e276f83`), which the MAESTRO relayed — the same fallback that saved T03b
  in the previous session. Rule confirmed: after two failures, the dispatch text is committed
  to `specs/072-painel-de-regencia/task-<id>.md`.
- **F9 measured consequence of the literal `${…}` rule (D-072-8).** The reconciled F9 does not
  count a template literal as button text, so three **old** `index.html` buttons
  (`#ch-atualiza`, `.ch-cartao`, `.botoes[data-el]`) fail it even though they render text at
  runtime. Decided by the regent session: Worker04 labels them with `aria-label` in slice A;
  the limitation itself stays declared in D-072-8, unchanged.
