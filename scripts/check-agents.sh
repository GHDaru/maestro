#!/usr/bin/env bash
# check-agents.sh — structural fitness functions for the subagents.
# Runs the invariants that used to be checked by hand.
# Exit 0 when everything passes; exit 1 when any invariant breaks.
set -euo pipefail

AGENTS_DIR=".claude/agents"
EXPECTED_COUNT="${MAESTRO_AGENTS_EXPECTED:-13}"
READONLY_AGENTS=(review security process-guardian)
fail=0

# 1. Expected count.
count=$(find "$AGENTS_DIR" -maxdepth 1 -name '*.md' | wc -l | tr -d ' ')
if [[ "$count" -ne "$EXPECTED_COUNT" ]]; then
  echo "FAIL: expected $EXPECTED_COUNT agents, found $count." >&2
  fail=1
else
  echo "ok: $count agents."
fi

# 2. Every agent has a 'name:' front matter field.
missing_name=$(grep -L "^name:" "$AGENTS_DIR"/*.md || true)
if [[ -n "$missing_name" ]]; then
  echo "FAIL: missing 'name:' in front matter:" >&2
  echo "$missing_name" >&2
  fail=1
else
  echo "ok: every agent has 'name:' front matter."
fi

# 3. Security invariant: a read-only agent must NOT have Write/Edit.
for a in "${READONLY_AGENTS[@]}"; do
  f="$AGENTS_DIR/$a.md"
  [[ -e "$f" ]] || { echo "FAIL: missing $f." >&2; fail=1; continue; }
  if grep -qE "tools:.*(Write|Edit)" "$f"; then
    echo "FAIL: read-only agent '$a' has Write/Edit in its tools." >&2
    fail=1
  fi
done
[[ "$fail" -eq 0 ]] && echo "ok: no read-only agent with Write/Edit."

if [[ "$fail" -ne 0 ]]; then
  echo "agent invariants BROKEN." >&2
  exit 1
fi
echo "all agent invariants OK."
