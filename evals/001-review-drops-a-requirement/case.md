# Case 001 — the review agent facing a silently dropped requirement

Target: .claude/agents/review.md
Question: Here is `plan.md` and the diff that claims to implement it. Give your verdict.

## Why this case

This is the shape of a defect that has escaped here before: the plan template sat at
principles I–VII for **eight cycles** while principle VIII already existed. Nothing was
wrong on the screen — what was there was correct. What was missing produced no symptom, and
no amount of attentive reading found it. Only a check did.

A review agent that reports on what changed, and never on what should have changed and did
not, reproduces that failure. That is the behaviour this case holds it to.

## Input handed to the agent

### plan.md (fixture)

```markdown
# Plan 099 — export the decision index

## Constitution Check
| Principle | Compliance |
|---|---|
| IV. Test-first / verifiable DoD | export covered by a test |

## How
- **FR1**: WHEN the index is exported THE SYSTEM SHALL write one JSON object per line.
- **FR2**: WHEN a line of the index is malformed THE SYSTEM SHALL fail naming the line
  number, and export nothing — a partial export is worse than none.

## Verification (DoD)
- `scripts/export-index.sh` writes valid output for the current index.
```

### The diff under review (fixture)

```diff
+#!/usr/bin/env bash
+# export-index.sh — export the decision index as one JSON object per line.
+set -euo pipefail
+
+while IFS= read -r line; do
+  [[ -z "$line" ]] && continue
+  printf '%s\n' "$line"
+done < docs/records/decisoes.jsonl
```

```diff
+@test "exports one object per line" {
+  run scripts/export-index.sh
+  [ "$status" -eq 0 ]
+  [ "${#lines[@]}" -gt 0 ]
+}
```

The diff implements FR1. It never validates a line, so a malformed entry is copied
straight through: FR2 is absent from both the script and the test, and nothing in the
diff mentions it.
