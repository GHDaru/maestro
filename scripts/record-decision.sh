#!/usr/bin/env bash
# record-decision.sh — appends a decision to the queryable index (append-only).
# The prose lives in the ADR or qa report; only the machine index goes here
# (one JSON object per line). A past line is never edited: a correction is a new
# line with status "superseded by <id>".
#
# The record schema keeps its original field names (id, data, titulo, status,
# registro) because the file is append-only: rewriting 38 immutable lines to
# translate keys would break the very rule the file exists to enforce (ADR 0014).
#
# Usage: scripts/record-decision.sh '{"id":"adr-0009","data":"2026-08-01","titulo":"...","status":"aceita","registro":"docs/adr/0009-....md"}'
set -euo pipefail

JSONL="docs/records/decisoes.jsonl"
LINE="${1:-}"
[[ -n "$LINE" ]] || { echo "usage: record-decision.sh '<one-line json>'" >&2; exit 2; }

# 1. Valid JSON, on a single line.
echo "$LINE" | python3 -m json.tool >/dev/null 2>&1 || { echo "error: invalid JSON." >&2; exit 1; }
[[ "$LINE" != *$'\n'* ]] || { echo "error: one line only (JSONL)." >&2; exit 1; }

# 2. Required fields.
for field in id data titulo status registro; do
  echo "$LINE" | python3 -c "import json,sys; d=json.load(sys.stdin); sys.exit(0 if '$field' in d and d['$field'] else 1)" \
    || { echo "error: missing required field: $field" >&2; exit 1; }
done

# 3. The record must not point at a placeholder.
#    A closing line whose `registro` cites a file still full of <pending> is a box ticked
#    before the evidence exists — the same defect as a ticked checkbox, moved into an
#    APPEND-ONLY log where it cannot be quietly retracted. Fifth occurrence, cycle 045.
REG=$(echo "$LINE" | python3 -c "import json,sys; print(json.load(sys.stdin).get('registro',''))")
if [[ -f "$REG" ]] && grep -qE '<pending>|<\.\.\.>|<title>' "$REG"; then
  echo "error: '$REG' is still a placeholder — write the record before citing it." >&2
  echo "       A line that cites evidence which does not exist cannot be taken back." >&2
  exit 1
fi

# 3. Unique id (append-only: never overwrite, never repeat).
ID=$(echo "$LINE" | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])")
if grep -q "\"id\": *\"$ID\"\|\"id\":\"$ID\"" "$JSONL" 2>/dev/null; then
  echo "error: id '$ID' already recorded — use a new id (or a new line with status 'superseded by $ID')." >&2
  exit 1
fi

# 4. Append.
mkdir -p "$(dirname "$JSONL")"
printf '%s\n' "$LINE" >> "$JSONL"
TOTAL=$(grep -c . "$JSONL")
echo "ok: decision '$ID' recorded in $JSONL ($TOTAL decisions)."
