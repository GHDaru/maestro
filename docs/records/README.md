# Decision records — the machine-queryable index

> This index is **versioned**: it is governance, not session state.

## The protocol

- **The prose lives in the ADR** (Architecture Decision Record, `docs/adr/`): context,
  alternatives, rationale, consequences.
- **`decisoes.jsonl` is the machine index**: one JSON object per line, **append-only** —
  never edit a past line; a correction is a new line (`status: "superada por ..."`). That is
  how an agent can query "the last N decisions" without loading whole ADRs into context.

## Line format

```json
{"id":"adr-0008","data":"2026-07-31","titulo":"SDD ecosystem evaluation","status":"aceita","registro":"docs/adr/0008-avaliacao-ecossistema-sdd.md","ciclo":"007"}
```

The field names stay in Portuguese even though the installable method is in English
(ADR 0014): the file is append-only, and renaming keys would require rewriting immutable
lines — which is exactly what this file exists to prevent.

| Field | Required | Content |
|---|---|---|
| `id` | ✅ | `adr-NNNN` · `gate-NNN-<slug>` (cycle gate) · `gate-main-<sha>` (merge, **automatic** via `promote-main.sh`, ADR 0009) |
| `data` | ✅ | date, `YYYY-MM-DD` |
| `titulo` | ✅ | title, one line |
| `status` | ✅ | `aceita` (accepted) · `proposta` (proposed) · `superada por <id>` (superseded by) |
| `registro` | ✅ | path of the prose document (ADR, qa report, spec) |
| `ciclo` | — | cycle `NNN` when it comes from one |
| `fecha` | — | the id of the **finding this line closes** (see below) |

## Findings and the retrospective trigger

A finding that did not fit inside its cycle is recorded here with an id starting with
`achado-` and status `aberta`. It is what makes the retrospective a **debt**, not a date:
`scripts/check-retro.sh` fails with four or more open findings, or with one open for six
cycles or longer.

Closing does not edit the old line (append-only): a **new** line names the finding it closes
in the `fecha` field. The link is a field, not prose — a closing recognised by matching words
would be a check measuring the text instead of the fact.

```json
{"id":"retro-034-fecha-027","fecha":"achado-027-retro-sem-gatilho","data":"2026-08-03","titulo":"Closed: check-retro.sh …","status":"fechada por retro-034","registro":"specs/034-…/qa-report.md","ciclo":"034"}
```

### A finding found and fixed inside the same cycle

It gets **one** line, with status `fechada no mesmo ciclo` and **no `fecha` field**. There is
nothing to close: no line was ever open.

```json
{"id":"achado-041-retro-mentindo","data":"2026-08-07","titulo":"Found and fixed here: retro.sh …","status":"fechada no mesmo ciclo","registro":"specs/041-…/qa-report.md","ciclo":"041"}
```

This form exists because its absence produced the same defect twice. With no shape for
"found and fixed here", the improvisation was a line whose `fecha` pointed at its own `id` —
a self-closure of a finding that was never open, which the index then had to correct with a
further line. Cycles 039 and 041, the second written while retrospecting the first. A gap in
a protocol is not a lapse of attention: it is a shape the protocol failed to offer.

### A finding whose remedy became a trigger

Some findings are answered by deciding **not to act yet**, under a named condition. The
decision is complete the moment the condition is written down somewhere that will be
consulted — an `observar` verdict in `docs/ecosystem/`, a trigger row in the roadmap. The
finding closes **then**, with `fecha` pointing at it and the trigger quoted in the title, so
the deferral is auditable where it lives instead of ageing here.

```json
{"id":"retro-055-fecha-047","fecha":"achado-047-…","data":"2026-08-16","titulo":"Closed: … remedy is a trigger — 'first real intention that does not fit one cycle' …","status":"fechada por retro-055","registro":"specs/055-…/qa-report.md","ciclo":"055"}
```

This shape exists because its absence made a gate lie. `achado-047` was remedied inside cycle
047 — five ideas reclassified to `observar`, each with a trigger, all on disk — and stayed
open anyway. Nothing in the world would close it — the trigger had not fired and might never
— and the `fecha` mechanism was available the whole time: what was missing was the decision
to use it, not the event. It aged to **seven cycles** and turned `check-retro.sh` red, so the debt gauge
was measuring the **calendar**, not the debt. A finding waiting on a condition is not an open
finding; it is a closed decision with a condition. Say which, or the gauge stops meaning
anything. *(cycle 055.)*

## How to record

```bash
scripts/record-decision.sh '{"id":"gate-008-merge","data":"2026-07-31","titulo":"...","status":"aceita","registro":"specs/008-.../qa-report.md"}'
```

The script validates the JSON and the required fields and **only appends** — it never
rewrites. Quick query: `tail -5 docs/records/decisoes.jsonl`.
