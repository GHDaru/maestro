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

- Pending (task dispatched; no evidence yet).

### 072-T09 — ADR 0027 + index line + glossary (Worker01)

- Pending (task dispatched; no evidence yet).

### 072-T03 — pure domain + parser FR5 (Worker03)

- Pending (not dispatched yet; runs after T03b is integrated).

### 072-T07 — append-only triggers in the base, FR17 (Worker02)

- Pending (not dispatched yet; runs after T03b is integrated).

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
