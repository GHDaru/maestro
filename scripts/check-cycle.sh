#!/usr/bin/env bash
# check-cycle.sh — hygiene of the cycle artifacts and of the traceability link.
#
# Two findings turned into one gate (retrospective of cycle 034):
#   * cycle 023: 19 of 22 specs were marked "full" and 2 "light" — a router that sends almost
#     everything to the same treatment is not routing. The gate cannot decide the lane for
#     you, so it demands the JUSTIFICATION (the three factors) and prints the distribution.
#     It forces the thinking and makes the skew visible; it cannot judge the answer.
#   * cycle 031: the `spec NNN` citation in the commit subject held for 28 commits by habit
#     alone. Habit is what fails first.
#
# History is evidence, not a target: only cycles from MIN_CYCLE onwards are required to carry
# the lane rationale.
set -euo pipefail

MIN_CYCLE="${MAESTRO_MIN_CYCLE_RATIONALE:-34}"
BASE="${MAESTRO_TRACE_BASE:-main}"
fail=0

echo "── Lane declared and justified (from cycle $(printf '%03d' "$MIN_CYCLE")) ──"
declare -A LANES=()
for d in specs/[0-9][0-9][0-9]-*/; do
  [[ -f "$d/spec.md" ]] || continue
  n=$(basename "$d" | cut -d- -f1 | sed 's/^0*//')
  line=$(grep -m1 -E '^\- \*\*Status\*\*' "$d/spec.md" || true)
  # the substitution may find nothing (a skeleton spec); with pipefail that would kill
  # the script silently — `|| true` keeps the check reporting instead of dying.
  lane=$(echo "$line" | grep -oiE 'raia\*\*: *[A-Za-zç]+|lane\*\*: *[A-Za-z]+' | sed 's/.*: *//' | tr 'A-Z' 'a-z' || true)
  LANES["${lane:-?}"]=$(( ${LANES["${lane:-?}"]:-0} + 1 ))
  [[ "${n:-0}" -ge "$MIN_CYCLE" ]] || continue
  if [[ -z "$lane" ]]; then
    echo "  ✗ $(basename "$d"): no lane declared in the spec header" >&2; fail=$((fail + 1)); continue
  fi
  # the rationale must name the three factors that decide the lane
  if ! grep -qiE 'ambiguidade|ambiguity' "$d/spec.md" || ! grep -qiE 'irreversib' "$d/spec.md"; then
    echo "  ✗ $(basename "$d"): lane '$lane' declared without justification (name ambiguity × blast radius × irreversibility)" >&2
    fail=$((fail + 1))
  else
    echo "  ok: $(basename "$d") — lane '$lane' with rationale"
  fi
done

echo ""
echo "── Lane distribution (visibility, never a verdict) ──"
for k in "${!LANES[@]}"; do echo "  $k: ${LANES[$k]}"; done

echo ""
echo "── Traceability: every commit ahead of '$BASE' cites its cycle ──"
if git rev-parse --verify --quiet "$BASE" >/dev/null; then
  while IFS= read -r subject; do
    [[ -n "$subject" ]] || continue
    if echo "$subject" | grep -qiE 'spec [0-9]{3}|ADR [0-9]{4}|chore\(records\)'; then
      echo "  ok: $subject"
    else
      echo "  ✗ commit without a cycle citation: $subject" >&2
      echo "      (use 'spec NNN' or 'ADR NNNN' in the subject — the traceability link is not a habit, it is a gate)" >&2
      fail=$((fail + 1))
    fi
  done < <(git log --format=%s "$BASE"..HEAD 2>/dev/null)
else
  echo "  ⚠ branch '$BASE' not found — skipping the traceability check" >&2
fi

echo ""
if [[ "$fail" -ne 0 ]]; then
  echo "✗ $fail problem(s) in the cycle artifacts or the traceability link." >&2
  exit 1
fi
echo "✓ lanes justified and every commit ahead of '$BASE' carries its cycle."
