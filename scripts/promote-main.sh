#!/usr/bin/env bash
# promote-main.sh — promotes dev -> main (Maestro's "merge gate").
#
# THE GATE IS HUMAN (Principle II): this script only performs the MECHANICAL step
# after your decision. It asks for confirmation and aborts if anything is out of
# place. It decides nothing — it just removes typos from a repeated ritual.
#
# Usage:  scripts/promote-main.sh          # asks before promoting
#         scripts/promote-main.sh --yes    # skips the question (you already decided)
set -euo pipefail

DEV="${MAESTRO_DEV_BRANCH:-dev}"
MAIN="${MAESTRO_MAIN_BRANCH:-main}"
ASSUME_YES=0
[[ "${1:-}" == "--yes" ]] && ASSUME_YES=1

# 1. Clean tree (never promote uncommitted work).
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "aborted: dirty working tree — commit or clean it before promoting." >&2
  exit 1
fi

# 2. dev must be ahead of main.
git rev-parse --verify --quiet "$DEV" >/dev/null || { echo "aborted: branch '$DEV' does not exist." >&2; exit 1; }
git rev-parse --verify --quiet "$MAIN" >/dev/null || { echo "aborted: branch '$MAIN' does not exist." >&2; exit 1; }
AHEAD=$(git rev-list --count "$MAIN".."$DEV")
if [[ "$AHEAD" -eq 0 ]]; then
  echo "nothing to promote: '$MAIN' already matches '$DEV'." >&2
  exit 1
fi

# 3. Conformance is enforced HERE, not in continuous integration.
#    A cycle's qa-report.md is a placeholder from new-cycle.sh until the cycle ends, so a
#    blocking conformance gate in CI would be red for the whole life of every branch — and
#    a gate that is always red is one people learn to scroll past. Promotion is the moment
#    a cycle is actually finished, so it is the moment the claim has to hold (cycle 043).
if [[ -x scripts/check-conformance.sh ]]; then
  if ! scripts/check-conformance.sh; then
    echo "" >&2
    echo "aborted: conformance is red — a cycle is being promoted with its method missing" >&2
    echo "         from its own artifacts. Fix it above, or promote by hand if you have" >&2
    echo "         decided the debt is acceptable and recorded why." >&2
    exit 1
  fi
  echo ""
fi

# 4. Show what goes to main.
echo "going to '$MAIN' ($AHEAD commit(s) from '$DEV'):"
git --no-pager log --oneline "$MAIN".."$DEV"
echo

# 4. Human gate: explicit confirmation.
if [[ "$ASSUME_YES" -ne 1 ]]; then
  read -r -p "promote '$DEV' -> '$MAIN' and push? [y/N] " ans
  [[ "$ans" == "y" || "$ans" == "Y" ]] || { echo "cancelled."; exit 1; }
fi

# 5. Record the gate in the decision index (ADR 0009 — automatic, so the queryable
#    record is the source of truth for the gate state).
#    The record schema keeps its original field names: the file is append-only and
#    its past lines must not be rewritten (see ADR 0014).
SHORT=$(git rev-parse --short "$DEV")
CURRENT=$(git symbolic-ref --short HEAD 2>/dev/null || echo "")
if [[ "$CURRENT" == "$DEV" && -f docs/records/decisoes.jsonl ]] && command -v python3 >/dev/null; then
  TITLE=$(git log -1 --format=%s "$DEV" | tr '"' "'")
  TODAY=$(date +%Y-%m-%d)
  LINE=$(python3 -c "import json;print(json.dumps({'id':'gate-main-$SHORT','data':'$TODAY','titulo':'Gate de merge: $TITLE','status':'aceita','registro':'commit $SHORT'},ensure_ascii=False))")
  if scripts/record-decision.sh "$LINE" >/dev/null 2>&1; then
    git add docs/records/decisoes.jsonl
    git commit -q -m "chore(records): merge gate gate-main-$SHORT"
    echo "gate recorded: gate-main-$SHORT"
  else
    echo "warning: gate not recorded (id already there?); continuing." >&2
  fi
else
  echo "warning: record unavailable (docs/records/ or python3 missing); continuing." >&2
fi

# 6. Run the mechanical step, with exponential backoff on the push (dev + main together).
git branch -f "$MAIN" "$DEV"
delay=2
for attempt in 1 2 3 4 5; do
  if git push origin "$DEV" "$MAIN"; then
    echo "ok: '$MAIN' promoted to $(git rev-parse --short "$DEV")."
    exit 0
  fi
  if [[ "$attempt" -lt 5 ]]; then
    echo "push failed (attempt $attempt); retrying in ${delay}s..." >&2
    sleep "$delay"; delay=$((delay * 2))
  fi
done
echo "error: pushing '$MAIN' failed after 5 attempts." >&2
exit 1
