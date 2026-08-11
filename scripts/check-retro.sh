#!/usr/bin/env bash
# check-retro.sh — the retrospective has a trigger, and the trigger is checkable.
#
# Cycle 027 found that the highest-return ceremony had no clock: it happened when someone
# remembered. A ceremony that depends on memory is the same failure mode as a norm without a
# forcing function — and memory is what fails first.
#
# The trigger is NOT the calendar: it is the debt of open findings. A finding is recorded in
# the decision index (docs/records/decisoes.jsonl) with an id starting with "achado-" and
# status "aberta". The retrospective closes it with a NEW line (the index is append-only, so
# ids are unique) that names the finding it closes in the field `fecha`:
#   {"id":"retro-034-achado-023","fecha":"achado-023-raias","status":"fechada por retro-034",...}
# The link is structural (a field), never textual — a closing recognised by prose would be a
# check measuring the words instead of the fact (anti-pattern 13).
#
# Fails when: open findings ≥ MAX_OPEN, or the oldest open finding is ≥ MAX_AGE cycles old.
set -euo pipefail

INDEX="docs/records/decisoes.jsonl"
MAX_OPEN="${MAESTRO_MAX_OPEN_FINDINGS:-4}"
MAX_AGE="${MAESTRO_MAX_FINDING_AGE:-6}"   # in cycles

[[ -f "$INDEX" ]] || { echo "✗ decision index missing: $INDEX" >&2; exit 1; }

# A glob, not `ls` in a pipe: with no specs/ directory `ls` exits 2, pipefail propagates it,
# and `set -e` killed this script SILENTLY — exit 2, no output. Invisible here, where specs
# always exist; fatal on a fresh installation, which is where cycle 048 found it.
# Anti-pattern 21, third occurrence.
shopt -s nullglob; _cycles=(specs/[0-9][0-9][0-9]-*/); shopt -u nullglob
CURRENT_CYCLE=0
if [[ ${#_cycles[@]} -gt 0 ]]; then
  CURRENT_CYCLE="$(basename "${_cycles[${#_cycles[@]}-1]}" | cut -d- -f1 | sed 's/^0*//')"
fi
CURRENT_CYCLE="${CURRENT_CYCLE:-0}"

python3 - "$INDEX" "$MAX_OPEN" "$MAX_AGE" "$CURRENT_CYCLE" <<'PY'
import json, sys, re
index, max_open, max_age, current = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
lines = [json.loads(l) for l in open(index) if l.strip()]
closed = {d["fecha"] for d in lines if d.get("fecha")}
open_ones = []
for d in lines:
    fid = d["id"]
    if not fid.startswith("achado-") or fid in closed:
        continue
    if not d["status"].startswith("aberta"):
        continue
    m = re.match(r"achado-(\d{3})", fid)
    cycle = int(m.group(1)) if m else 0
    open_ones.append((fid, cycle, d["titulo"]))

print("── Open findings × retrospective debt ──")
if not open_ones:
    print("  no open finding recorded.")
else:
    for fid, cycle, title in sorted(open_ones, key=lambda x: x[1]):
        age = current - cycle
        print(f"  {fid}  (cycle {cycle:03d}, {age} cycle(s) old)  {title[:70]}")

fail = 0
if len(open_ones) >= max_open:
    print(f"\n✗ {len(open_ones)} open findings (limit {max_open}) — run the retrospective and turn them into rules.", file=sys.stderr)
    fail = 1
oldest = max((current - c for _, c, _ in open_ones), default=0)
if oldest >= max_age:
    print(f"✗ the oldest open finding is {oldest} cycles old (limit {max_age}) — anti-pattern 14 in progress.", file=sys.stderr)
    fail = 1
if fail:
    sys.exit(1)
print(f"\n✓ retrospective debt under control ({len(open_ones)} open, limit {max_open}).")
PY
