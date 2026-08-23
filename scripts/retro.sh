#!/usr/bin/env bash
# retro.sh — pre-computes the retrospective material from the repository artifacts.
# Read-only: it never writes anything. The retrospective itself stays a human ceremony;
# this script only removes the "reload the context from memory" part.
set -euo pipefail

echo "══════════════════════════════════════════════"
echo "  RETRO — pre-computed material"
echo "══════════════════════════════════════════════"

# 1. Cycles and verdicts.
echo ""
echo "── Cycles (specs/) and QA verdict ──"
for d in specs/[0-9][0-9][0-9]-*/; do
  [[ -d "$d" ]] || continue
  name=$(basename "$d")
  verdict=$(grep -m1 -oE "Veredito[^|]*|Verdict[^|]*" "$d/qa-report.md" 2>/dev/null | sed 's/Ver[a-z]*[^ ]*: *//' | tr -d '*' || true)
  echo "  $name — ${verdict:-no qa-report}"
done

# 2. Gates: pending items from the qa reports crossed with the record (ADR 0009 —
#    the index docs/records/decisoes.jsonl is the source of truth for gate state).
#
#    This block lied for twenty-nine cycles. It matched ids shaped `gate-<cycle>-*`, which
#    only seven early gates ever used: since ADR 0009 automated the record, promote-main.sh
#    writes `gate-main-<sha>`. Every cycle from 011 on was therefore reported PENDING
#    forever — a check measuring a *format* instead of the fact (anti-pattern 13), inside
#    the very tool that feeds the retrospective. Found by the retrospective of cycle 041.
#
#    The fact, now: a cycle is promoted when a commit citing it sits on the main line.
echo ""
echo "── Gates (qa-report × record) ──"
MAIN="${MAESTRO_MAIN_BRANCH:-main}"
# Captured ONCE, never piped into `grep -q`: under `set -o pipefail`, grep -q exits at the
# first match, git log takes SIGPIPE, and the whole pipeline reports failure — so the test
# silently reads as "no match". That bug already killed check-cycle.sh once; second time
# here. See anti-pattern 21.
SUBJECTS="$(git log "$MAIN" --format=%s 2>/dev/null || true)"
found=0
for f in $(grep -rlE "Pendência de gate|Pending gate" specs/*/qa-report.md 2>/dev/null); do  # PT-DATA (older cycles)
  cycle=$(dirname "$f" | xargs basename | cut -d- -f1)
  # awk, not `sed | grep -m1 | sed`: `grep -m1` closes the pipe on its first match and the
  # upstream dies of SIGPIPE under `pipefail`, so `|| true` silently produced an EMPTY pending
  # gate — the field simply vanished from the retrospective material (anti-pattern 21).
  pending=$(awk '/Pendência de gate|Pending gate/{s=1} s && /^- /{sub(/^- /,""); print; exit}' "$f" || true)  # PT-DATA
  [[ -n "$pending" ]] || continue
  if grep -q "\"gate-$cycle" docs/records/decisoes.jsonl 2>/dev/null; then
    echo "  $(dirname "$f" | xargs basename): ✅ closed in the record (legacy id gate-$cycle-*)"
  elif grep -qiE "spec[ .]?$cycle\b" <<<"$SUBJECTS"; then
    echo "  $(dirname "$f" | xargs basename): ✅ on the main line (a commit cites spec $cycle)"
  else
    echo "  $(dirname "$f" | xargs basename): ⏳ PENDING — $pending"
    found=1
  fi
done
[[ "$found" -eq 0 ]] && echo "  (no pending gate)"

# 3. Latest recorded decisions.
echo ""
echo "── Last 5 decisions (docs/records/decisoes.jsonl) ──"
if [[ -f docs/records/decisoes.jsonl ]]; then
  tail -5 docs/records/decisoes.jsonl | python3 -c "
import json,sys
for line in sys.stdin:
    d=json.loads(line)
    print(f\"  {d['data']}  [{d['status']}]  {d['id']}: {d['titulo']}\")"
else
  echo "  (no record — see docs/records/README.md)"
fi

# 4. Open findings waiting for this ceremony.
echo ""
echo "── Open findings (qa reports) ──"
grep -rhE "^[0-9]+\. \*\*" specs/*/qa-report.md 2>/dev/null | sed 's/^/  /' | tail -8 || echo "  (none)"

# 5. Toolkit inventory.
echo ""
echo "── Inventory ──"
echo "  agents:   $(find .claude/agents -name '*.md' 2>/dev/null | wc -l | tr -d ' ')"
echo "  skills:   $(find skills -name 'SKILL.md' 2>/dev/null | wc -l | tr -d ' ')"
echo "  scripts:  $(find scripts -name '*.sh' 2>/dev/null | wc -l | tr -d ' ')"
echo "  ADRs:     $(find docs/adr -name '0*.md' 2>/dev/null | wc -l | tr -d ' ')"

# 6. The retrospective questions (the human part).
echo ""
echo "── Retrospective questions (answer them and turn them into rules) ──"
echo "  1. Which mistake or fix REPEATED itself in these cycles? → becomes a versioned rule"
echo "     (CLAUDE.md, a skill, a principle) — never fix the same thing twice."
echo "  2. Which existing rule did NOT pay for itself? → prune it (YAGNI)."
echo "  3. Which manual step repeated identically? → candidate for a script or skill."
echo ""
echo "Done. This is input material; the retrospective is yours."
