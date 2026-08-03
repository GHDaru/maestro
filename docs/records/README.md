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

## How to record

```bash
scripts/record-decision.sh '{"id":"gate-008-merge","data":"2026-07-31","titulo":"...","status":"aceita","registro":"specs/008-.../qa-report.md"}'
```

The script validates the JSON and the required fields and **only appends** — it never
rewrites. Quick query: `tail -5 docs/records/decisoes.jsonl`.
