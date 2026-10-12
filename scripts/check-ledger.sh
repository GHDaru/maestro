#!/usr/bin/env bash
# check-ledger.sh — the task ledger and the self-check hook are tested, not trusted.
#
# Hermetic: every test runs in a temporary directory with fixtures written HERE, so the gate
# does not depend on the state of the repository (nor on the real ledger). The expected
# numbers of the report fixture are computed by hand, in the comments next to it.
#
# The scripts under test can be pointed elsewhere, so a mutation runs on a COPY:
#   LEDGER_RECORDER=<record-task.py>  LEDGER_REPORT=<report-tasks.py>
#   LEDGER_STOP_HOOK=<stop-conformance.py>  LEDGER_MERGE=<merge-settings.py>
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RECORDER="${LEDGER_RECORDER:-$ROOT/scripts/record-task.py}"
REPORT="${LEDGER_REPORT:-$ROOT/scripts/report-tasks.py}"
STOP_HOOK="${LEDGER_STOP_HOOK:-$ROOT/scripts/hooks/stop-conformance.py}"
MERGE="${LEDGER_MERGE:-$ROOT/scripts/hooks/merge-settings.py}"

WORK="$(mktemp -d "${TMPDIR:-/tmp}/check-ledger.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT

PASS=0
FAIL=0
ok()  { PASS=$((PASS + 1)); echo "  ✓ $1"; }
bad() { FAIL=$((FAIL + 1)); echo "  ✗ $1" >&2; }
expect() {  # expect <description> <expected> <actual>
  if [[ "$2" == "$3" ]]; then ok "$1"; else bad "$1 (expected '$2', got '$3')"; fi
}

# ── a. record-task.py ─────────────────────────────────────────────────────────────────
echo "── a. recorder ──"
L="$WORK/a.jsonl"
rec() { MAESTRO_TASK_LEDGER="$L" python3 "$RECORDER" "$1" >/dev/null 2>&1; echo $?; }

expect "valid record is written" 0 "$(rec '{"ts":"2026-01-01T00:00:00Z","event":"start","task_id":"X-1","kind":"implement","attempt":1}')"
expect "the valid record is one line" 1 "$(wc -l < "$L" | tr -d ' ')"
expect "invalid kind is refused" 1 "$(rec '{"ts":"2026-01-01T00:00:00Z","event":"start","task_id":"X-1","kind":"nonsense"}')"
expect "attempt 0 is refused" 1 "$(rec '{"ts":"2026-01-01T00:00:00Z","event":"start","task_id":"X-1","attempt":0}')"
expect "verdict event without a verdict is refused" 1 "$(rec '{"ts":"2026-01-01T00:00:00Z","event":"verdict","task_id":"X-1"}')"
expect "broken JSON is refused" 1 "$(rec '{"ts": broken')"
expect "refusals wrote nothing" 1 "$(wc -l < "$L" | tr -d ' ')"

expect "attempt true is refused (bool is not an integer)" 1 "$(rec '{"ts":"2026-01-01T00:00:00Z","event":"start","task_id":"X-1","attempt":true}')"
expect "attempt 1.0 is refused" 1 "$(rec '{"ts":"2026-01-01T00:00:00Z","event":"start","task_id":"X-1","attempt":1.0}')"
expect "task_id as an object is refused" 1 "$(rec '{"ts":"2026-01-01T00:00:00Z","event":"start","task_id":{"a":1}}')"
expect "session as a number is refused" 1 "$(rec '{"ts":"2026-01-01T00:00:00Z","event":"start","task_id":"X-1","session":7}')"
expect "ts that is not ISO 8601 is refused" 1 "$(rec '{"ts":"not-a-date","event":"start","task_id":"X-1"}')"
expect "verdict without by is refused" 1 "$(rec '{"ts":"2026-01-01T00:00:00Z","event":"verdict","task_id":"X-1","verdict":"approved"}')"
expect "event as a list is refused, no traceback" 1 "$(rec '{"ts":"2026-01-01T00:00:00Z","event":["start"],"task_id":"X-1"}')"
expect "ts with the Z suffix and milliseconds is accepted" 0 "$(rec '{"ts":"2026-01-01T00:00:00.123Z","event":"start","task_id":"X-2","attempt":1}')"
expect "verdict with by is accepted" 0 "$(rec '{"ts":"2026-01-01T00:00:00Z","event":"verdict","task_id":"X-1","verdict":"approved","by":"AUD-1"}')"

# 30 SIMULTANEOUS writers, each line ~2 KB: small lines would pass even with interleaving.
C="$WORK/concurrent.jsonl"
PAD="$(python3 -c 'print("x" * 2000)')"
for i in $(seq 1 30); do
  MAESTRO_TASK_LEDGER="$C" python3 "$RECORDER" \
    "{\"ts\":\"2026-01-01T00:00:00Z\",\"event\":\"start\",\"task_id\":\"C-$i\",\"attempt\":1,\"note\":\"$PAD\"}" >/dev/null 2>&1 &
done
wait
CONC="$(python3 - "$C" <<'PY'
import json, sys
ids, whole = [], 0
for l in open(sys.argv[1]):
    if l.strip():
        d = json.loads(l)
        ids.append(d["task_id"])
        whole += len(d["note"]) == 2000
print(len(ids), len(set(ids)), whole)
PY
)"
expect "30 simultaneous ~2 KB writes → 30 valid, distinct, intact lines" "30 30 30" "$CONC"

# ── b. report-tasks.py ────────────────────────────────────────────────────────────────
# Fixture, answers worked out by hand (tokens = in + out + cache_read + cache_write):
#   T-A  implement, attempt 1, m1 : 10+20+100+50  = 180 tokens, $0.10 · verdict approved
#   T-B  implement, attempt 1, m1 : 5+5+0+0       =  10 tokens, $0.05 · verdict rejected …
#   T-B  implement, attempt 2, m2 : 10+40+200+50  = 300 tokens, $0.20 · … then approved (last wins)
#   T-AUD audit,    attempt 1, m2 : 1+2+0+0       =   3 tokens, $0.01 · emits the 3 verdicts
#   T-ORF started, never stopped → 1 orphan · one non-JSON line → 1 invalid
# First-pass approval: tasks with verdict = T-A, T-B (2); only-attempt-1 and approved = T-A → 1/2
# Rework (attempt >= 2): 300 tokens, $0.20 · cache: read 300 ÷ (in 26 + read 300 + write 100) = 0.7042
# By kind: implement 490 tokens, audit 3 · By model: m1 190, m2 303
echo "── b. report ──"
has()  { if [[ "$1" == *"$2"* ]]; then echo yes; else echo no; fi; }   # has <haystack> <needle>
F="$WORK/fixture.jsonl"
cat > "$F" <<'EOF'
{"ts":"2026-01-01T10:00:00Z","event":"start","task_id":"T-A","kind":"implement","attempt":1,"cycle":"900","session":"s1","model":"m1"}
{"ts":"2026-01-01T10:01:00Z","event":"stop","task_id":"T-A","kind":"implement","attempt":1,"cycle":"900","session":"s1","outcome":"delivered","tokens_in":10,"tokens_out":20,"tokens_cache_read":100,"tokens_cache_write":50,"tokens_by_model":{"m1":{"input":10,"output":20,"cacheRead":100,"cacheWrite":50}},"cost_usd":0.10,"future_field":"ignored"}
{"ts":"2026-01-01T10:02:00Z","event":"start","task_id":"T-B","kind":"implement","attempt":1,"cycle":"900","session":"s2","model":"m1"}
{"ts":"2026-01-01T10:03:00Z","event":"stop","task_id":"T-B","kind":"implement","attempt":1,"cycle":"900","session":"s2","outcome":"delivered","tokens_in":5,"tokens_out":5,"tokens_cache_read":0,"tokens_cache_write":0,"tokens_by_model":{"m1":{"input":5,"output":5,"cacheRead":0,"cacheWrite":0}},"cost_usd":0.05}
this line is not json
{"ts":"2026-01-01T10:04:00Z","event":"start","task_id":"T-AUD","kind":"audit","attempt":1,"cycle":"900","session":"s4","model":"m2"}
{"ts":"2026-01-01T10:05:00Z","event":"stop","task_id":"T-AUD","kind":"audit","attempt":1,"cycle":"900","session":"s4","outcome":"delivered","tokens_in":1,"tokens_out":2,"tokens_cache_read":0,"tokens_cache_write":0,"tokens_by_model":{"m2":{"input":1,"output":2,"cacheRead":0,"cacheWrite":0}},"cost_usd":0.01}
{"ts":"2026-01-01T10:05:10Z","event":"verdict","task_id":"T-A","verdict":"approved","by":"T-AUD","session":"s4"}
{"ts":"2026-01-01T10:05:11Z","event":"verdict","task_id":"T-B","verdict":"rejected","by":"T-AUD","session":"s4","reason":"missing test"}
{"ts":"2026-01-01T10:06:00Z","event":"start","task_id":"T-B","kind":"implement","attempt":2,"cycle":"900","session":"s3","model":"m2","redoes":"T-B#1"}
{"ts":"2026-01-01T10:07:00Z","event":"stop","task_id":"T-B","kind":"implement","attempt":2,"cycle":"900","session":"s3","outcome":"delivered","tokens_in":10,"tokens_out":40,"tokens_cache_read":200,"tokens_cache_write":50,"tokens_by_model":{"m2":{"input":10,"output":40,"cacheRead":200,"cacheWrite":50}},"cost_usd":0.20,"redoes":"T-B#1"}
{"ts":"2026-01-01T10:08:00Z","event":"verdict","task_id":"T-B","verdict":"approved","by":"T-AUD","session":"s4"}
{"ts":"2026-01-01T10:09:00Z","event":"start","task_id":"T-ORF","kind":"implement","attempt":1,"cycle":"900","session":"s5","model":"m1"}
EOF
JSON="$(python3 "$REPORT" --ledger "$F" --json 2>/dev/null)"
field() {  # field <python expression over d>
  python3 -c 'import json,sys; d=json.load(sys.stdin); print('"$1"')' <<<"$JSON" 2>/dev/null
}
expect "first-pass approval is 1/2" "1/2" "$(field '"%d/%d" % (d["first_pass_approval"]["approved_first_pass"], d["first_pass_approval"]["tasks_with_verdict"])')"
expect "rework tokens (attempt >= 2) = 300" 300 "$(field 'd["rework"]["tokens"]')"
expect "rework cost = 0.2" 0.2 "$(field 'd["rework"]["cost_usd"]')"
expect "orphans = 1" 1 "$(field 'len(d["orphans"])')"
expect "the orphan is T-ORF" T-ORF "$(field 'd["orphans"][0]["task_id"]')"
expect "invalid lines = 1" 1 "$(field 'd["invalid_lines"]')"
expect "implement tokens = 490" 490 "$(field 'd["by_kind"]["implement"]["tokens"]')"
expect "audit tokens = 3" 3 "$(field 'd["by_kind"]["audit"]["tokens"]')"
expect "model m1 tokens = 190" 190 "$(field 'd["by_model"]["m1"]["tokens"]')"
expect "model m2 tokens = 303" 303 "$(field 'd["by_model"]["m2"]["tokens"]')"
expect "cache rate = 0.7042" 0.7042 "$(field 'd["cache_rate"]')"
expect "--cycle filters (no events for cycle 901)" 0 "$(python3 "$REPORT" --ledger "$F" --cycle 901 --json | python3 -c 'import json,sys; print(json.load(sys.stdin)["events"])')"
python3 "$REPORT" --ledger "$F" >/dev/null 2>&1 && ok "text output exits 0" || bad "text output exits 0"

# --cycle must keep the verdicts: a verdict event has no cycle, it belongs to its TARGET's cycle.
fp() {  # fp <report args…> → "approved/judged"
  python3 "$REPORT" "$@" --json | python3 -c 'import json,sys; d=json.load(sys.stdin)["first_pass_approval"]; print("%d/%d" % (d["approved_first_pass"], d["tasks_with_verdict"]))'
}
expect "--cycle 900 gives the same first-pass approval as no filter (1/2)" "1/2" "$(fp --ledger "$F" --cycle 900)"

# Second fixture (cycle 910), by hand:
#   G-AUD audit (the judge) · G-A 1 attempt, approved by G-AUD → first pass
#   G-W   attempt 1 measured; attempt 2 stop with NO token/cost field (not measured); approved
#         by G-AUD → NOT first pass (2 attempts)
#   G-M   approved by "G-MGR" (not a task) and by G-A (an implement task) → 2 non-judge verdicts
#   G-N   verdict by G-AUD but no start at all → listed apart, not counted
#   G-D   rejected then approved by G-AUD (last wins), 1 attempt → first pass, counted once
#   G-F   1 attempt; "approved" signed by G-AUD but from session "evil", which never ran G-AUD
#         → not the judge's session → ignored (so G-F has no verdict and is not judged)
#   910-cycle  verdict on the whole cycle: rejected, then approved_with_notes, both by G-AUD from
#         its own session; a later "rejected" from session "evil" is ignored → current =
#         approved_with_notes, history of 2, and it is NOT a "verdict with no start"
#   non-judge verdicts: G-MGR, G-A, the forged G-F, the forged cycle one = 4
#   4 badly typed lines (task_id object · attempt true · event list · verdict list) → invalid
# Expected: first pass 2/3 (judged: G-A, G-W, G-D; first pass: G-A, G-D) · rework null · 1 not measured
G="$WORK/g.jsonl"
cat > "$G" <<'EOF'
{"ts":"2026-02-01T10:00:00Z","event":"start","task_id":"G-AUD","kind":"audit","attempt":1,"cycle":"910","session":"a1"}
{"ts":"2026-02-01T10:01:00Z","event":"stop","task_id":"G-AUD","kind":"audit","attempt":1,"cycle":"910","session":"a1","outcome":"delivered","tokens_in":1,"tokens_out":1,"cost_usd":0.01}
{"ts":"2026-02-01T10:02:00Z","event":"start","task_id":"G-A","kind":"implement","attempt":1,"cycle":"910","session":"s1"}
{"ts":"2026-02-01T10:03:00Z","event":"stop","task_id":"G-A","kind":"implement","attempt":1,"cycle":"910","session":"s1","outcome":"delivered","tokens_in":10,"tokens_out":10,"cost_usd":0.10}
{"ts":"2026-02-01T10:04:00Z","event":"start","task_id":"G-W","kind":"implement","attempt":1,"cycle":"910","session":"s2"}
{"ts":"2026-02-01T10:05:00Z","event":"stop","task_id":"G-W","kind":"implement","attempt":1,"cycle":"910","session":"s2","outcome":"delivered","tokens_in":10,"tokens_out":20,"cost_usd":0.20}
{"ts":"2026-02-01T10:06:00Z","event":"start","task_id":"G-W","kind":"implement","attempt":2,"cycle":"910","session":"mgr"}
{"ts":"2026-02-01T10:07:00Z","event":"stop","task_id":"G-W","kind":"implement","attempt":2,"cycle":"910","session":"mgr","outcome":"delivered"}
{"ts":"2026-02-01T10:08:00Z","event":"start","task_id":"G-M","kind":"implement","attempt":1,"cycle":"910","session":"s3"}
{"ts":"2026-02-01T10:09:00Z","event":"stop","task_id":"G-M","kind":"implement","attempt":1,"cycle":"910","session":"s3","outcome":"delivered","tokens_in":1,"tokens_out":1,"cost_usd":0.01}
{"ts":"2026-02-01T10:10:00Z","event":"start","task_id":"G-D","kind":"implement","attempt":1,"cycle":"910","session":"s4"}
{"ts":"2026-02-01T10:11:00Z","event":"stop","task_id":"G-D","kind":"implement","attempt":1,"cycle":"910","session":"s4","outcome":"delivered","tokens_in":2,"tokens_out":2,"cost_usd":0.02}
{"ts":"2026-02-01T10:12:00Z","event":"verdict","task_id":"G-A","verdict":"approved","by":"G-AUD","session":"a1"}
{"ts":"2026-02-01T10:12:01Z","event":"verdict","task_id":"G-W","verdict":"approved","by":"G-AUD","session":"a1"}
{"ts":"2026-02-01T10:12:02Z","event":"verdict","task_id":"G-M","verdict":"approved","by":"G-MGR"}
{"ts":"2026-02-01T10:12:03Z","event":"verdict","task_id":"G-M","verdict":"approved","by":"G-A"}
{"ts":"2026-02-01T10:12:04Z","event":"verdict","task_id":"G-N","verdict":"approved","by":"G-AUD","session":"a1"}
{"ts":"2026-02-01T10:12:05Z","event":"verdict","task_id":"G-D","verdict":"rejected","by":"G-AUD","session":"a1"}
{"ts":"2026-02-01T10:12:06Z","event":"verdict","task_id":"G-D","verdict":"approved","by":"G-AUD","session":"a1"}
{"ts":"2026-02-01T10:12:07Z","event":"start","task_id":"G-F","kind":"implement","attempt":1,"cycle":"910","session":"s6"}
{"ts":"2026-02-01T10:12:08Z","event":"stop","task_id":"G-F","kind":"implement","attempt":1,"cycle":"910","session":"s6","outcome":"delivered","tokens_in":3,"tokens_out":3,"cost_usd":0.03}
{"ts":"2026-02-01T10:12:09Z","event":"verdict","task_id":"G-F","verdict":"approved","by":"G-AUD","session":"evil"}
{"ts":"2026-02-01T10:12:10Z","event":"verdict","task_id":"910-cycle","verdict":"rejected","by":"G-AUD","session":"a1"}
{"ts":"2026-02-01T10:12:11Z","event":"verdict","task_id":"910-cycle","verdict":"approved_with_notes","by":"G-AUD","session":"a1"}
{"ts":"2026-02-01T10:12:12Z","event":"verdict","task_id":"910-cycle","verdict":"rejected","by":"G-AUD","session":"evil"}
{"ts":"2026-02-01T10:13:00Z","event":"start","task_id":{"a":1}}
{"ts":"2026-02-01T10:13:01Z","event":"start","task_id":"G-X","attempt":true}
{"ts":"2026-02-01T10:13:02Z","event":["start"],"task_id":"G-X"}
{"ts":"2026-02-01T10:13:03Z","event":"verdict","task_id":"G-X","verdict":["approved"],"by":"G-AUD"}
EOF
GJ="$(python3 "$REPORT" --ledger "$G" --json 2>"$WORK/g.err")"; GRC=$?
gfield() { python3 -c 'import json,sys; d=json.load(sys.stdin); print('"$1"')' <<<"$GJ" 2>/dev/null; }
expect "badly typed lines: exit 0" 0 "$GRC"
expect "badly typed lines: no traceback on stderr" "" "$(cat "$WORK/g.err")"
expect "badly typed lines are counted as invalid (4)" 4 "$(gfield 'd["invalid_lines"]')"
expect "first-pass approval is 2/3 (G-A, G-D; G-W had 2 attempts)" "2/3" "$(fp --ledger "$G")"
expect "verdicts from non-judges = 4 (manager, executor, forged session ×2; ignored)" 4 "$(gfield 'd["first_pass_approval"]["verdicts_from_non_judges"]')"
expect "verdict on a task with no start is listed apart" "['G-N']" "$(gfield 'd["first_pass_approval"]["verdicts_without_start"]')"
expect "a stop without tokens is listed as not measured" "[('G-W', 2)]" "$(gfield '[(n["task_id"], n["attempt"]) for n in d["not_measured"]]')"
expect "rework made only of an unmeasured attempt is null, not 0" "None None" "$(gfield '"%s %s" % (d["rework"]["tokens"], d["rework"]["cost_usd"])')"
expect "the unmeasured stop is not an attempt of the cycle" "6 1" "$(gfield '"%d %d" % (d["by_cycle"]["910"]["attempts"], d["by_cycle"]["910"]["unmeasured"])')"
expect "--cycle 910 keeps the verdicts (same 2/3)" "2/3" "$(fp --ledger "$G" --cycle 910)"
expect "a verdict from a session that did not run the audit is ignored (G-F not judged)" "2/3" "$(fp --ledger "$G")"
expect "cycle verdict: the last valid one is the current (forged one ignored)" "approved_with_notes by G-AUD" "$(gfield '"%s by %s" % (d["cycle_verdicts"]["910"]["current"], d["cycle_verdicts"]["910"]["by"])')"
expect "cycle verdict: the history keeps both valid verdicts, in order" "['rejected', 'approved_with_notes']" "$(gfield '[h["verdict"] for h in d["cycle_verdicts"]["910"]["history"]]')"
expect "cycle verdict is not a 'verdict with no start'" "['G-N']" "$(gfield 'd["first_pass_approval"]["verdicts_without_start"]')"
expect "--cycle 910 keeps the cycle verdict" approved_with_notes "$(python3 "$REPORT" --ledger "$G" --cycle 910 --json | python3 -c 'import json,sys; print(json.load(sys.stdin)["cycle_verdicts"]["910"]["current"])')"
expect "--cycle 999 drops it" "{}" "$(python3 "$REPORT" --ledger "$G" --cycle 999 --json | python3 -c 'import json,sys; print(json.load(sys.stdin)["cycle_verdicts"])')"
expect "the text report has a 'Cycle verdicts' section with the history" yes "$(has "$(python3 "$REPORT" --ledger "$G")" "910: approved_with_notes by G-AUD  (history: rejected by G-AUD → approved_with_notes by G-AUD)")"
expect "the text report says 'not measured'" yes "$(has "$(python3 "$REPORT" --ledger "$G")" "not measured")"

# Pairing fixture (data-model rule 1: a stop closes the most recent open start of the same
# task_id AND session AND attempt). Two mutations survived without it: a key without the attempt
# and a key without the session.
#   P  session sp: start #1, start #2, stop #1 → the stop must close #1, leaving P#2 orphan
#      (without the attempt in the key it closes the most recent, #2, and #1 stays orphan)
#   Q  start #1 in session sa; its stop comes from session sb → does NOT close it: Q/sa orphan
#      (without the session in the key the stop closes it and Q vanishes from the orphans)
# Expected orphans, in ledger order: P attempt 2 (sp) and Q attempt 1 (sa).
H="$WORK/pairing.jsonl"
cat > "$H" <<'EOF'
{"ts":"2026-03-01T10:00:00Z","event":"start","task_id":"P","kind":"implement","attempt":1,"cycle":"920","session":"sp"}
{"ts":"2026-03-01T10:01:00Z","event":"start","task_id":"P","kind":"implement","attempt":2,"cycle":"920","session":"sp"}
{"ts":"2026-03-01T10:02:00Z","event":"stop","task_id":"P","kind":"implement","attempt":1,"cycle":"920","session":"sp","outcome":"delivered","tokens_in":1,"tokens_out":1,"cost_usd":0.01}
{"ts":"2026-03-01T10:03:00Z","event":"start","task_id":"Q","kind":"implement","attempt":1,"cycle":"920","session":"sa"}
{"ts":"2026-03-01T10:04:00Z","event":"stop","task_id":"Q","kind":"implement","attempt":1,"cycle":"920","session":"sb","outcome":"delivered","tokens_in":1,"tokens_out":1,"cost_usd":0.01}
EOF
expect "pairing: orphans are P#2 (sp) and Q#1 (sa) — attempt and session are part of the key" \
  "[('P', 2, 'sp'), ('Q', 1, 'sa')]" \
  "$(python3 "$REPORT" --ledger "$H" --json | python3 -c 'import json,sys; print([(o["task_id"], o["attempt"], o["session"]) for o in json.load(sys.stdin)["orphans"]])')"

# ── c. stop-conformance.py ────────────────────────────────────────────────────────────
# Fixtures are projects with a fake scripts/check-conformance.sh and a specs/ directory. The
# fakes are strict about the ARGUMENTS they receive, because the claim under test is "the hook
# measures the newest cycle only, with --ticked-only", and a fake that ignores its arguments
# cannot witness that. The hook reads $CLAUDE_PROJECT_DIR, which a real Claude Code session
# sets — so every call below clears it unless the test sets it on purpose.
echo "── c. Stop hook ──"
mkfix() {  # mkfix <name> <script body> — a project with cycles 041 and 064
  mkdir -p "$WORK/$1/scripts" "$WORK/$1/specs/041-old" "$WORK/$1/specs/064-new"
  printf '#!/usr/bin/env bash\n%s\n' "$2" > "$WORK/$1/scripts/check-conformance.sh"
}
mkfix red   'echo "✗ TAIL:review has no evidence (args: $*)"; exit 1'
mkfix green 'echo "✓ all good"; exit 0'
# Green ONLY for `--ticked-only 064`: any other invocation is the shape of a closed cycle, or
# the plugin check of an old TAIL:gate, going red while the newest cycle is fine.
mkfix oldred 'if [[ "$*" == "--ticked-only 064" ]]; then echo "✓ cycle 064 is fine"; exit 0; fi
echo "✗ package-plugin.sh --verify disagrees (args: $*)"; exit 1'
# The review's scenario: red when called WITHOUT a cycle number (every cycle from the floor).
mkfix nocycle 'for a in "$@"; do [[ "$a" =~ ^[0-9]+$ ]] && { echo "✓ one cycle"; exit 0; }; done
echo "✗ an old cycle is red"; exit 1'
# UTF-8 cut in half, as the real gate does (it truncates evidence lines by bytes): \xc3 is the
# first byte of an accented character and the second never comes.
mkfix halfutf 'printf "✗ TAIL:review evidence cut mid-char: caf\xc3\n"; exit 1'
mkdir -p "$WORK/none"
# A foreign project the agent has wandered into: its script must NEVER run.
mkfix evil 'touch "$(dirname "$0")/EXECUTED"; echo "✗ foreign script ran"; exit 1'
mkdir -p "$WORK/nocyc/scripts"
cp "$WORK/red/scripts/check-conformance.sh" "$WORK/nocyc/scripts/"

stop() {  # stop <cwd> <stop_hook_active> [CLAUDE_PROJECT_DIR]
  if [[ -n "${3:-}" ]]; then
    printf '{"hook_event_name":"Stop","cwd":"%s","stop_hook_active":%s}' "$1" "$2" \
      | CLAUDE_PROJECT_DIR="$3" python3 "$STOP_HOOK" 2>/dev/null
  else
    printf '{"hook_event_name":"Stop","cwd":"%s","stop_hook_active":%s}' "$1" "$2" \
      | env -u CLAUDE_PROJECT_DIR python3 "$STOP_HOOK" 2>/dev/null
  fi
}
jkey() { python3 -c 'import json,sys; d=json.load(sys.stdin); print(sorted(d))' 2>/dev/null; }
jget() { python3 -c 'import json,sys; print(json.load(sys.stdin)[sys.argv[1]])' "$1" 2>/dev/null; }
yn()   { if "$@"; then echo yes; else echo no; fi; }
has()  { if [[ "$1" == *"$2"* ]]; then echo yes; else echo no; fi; }   # has <haystack> <needle>

expect "green → empty output" "" "$(stop "$WORK/green" false)"
expect "red → decision block" "['decision', 'reason']" "$(stop "$WORK/red" false | jkey)"
expect "red, decision value is block" block "$(stop "$WORK/red" false | jget decision)"
expect "red + stop_hook_active → systemMessage and NO decision" "['systemMessage']" "$(stop "$WORK/red" true | jkey)"
expect "no script in the directory → empty output" "" "$(stop "$WORK/none" false)"

RSN="$(stop "$WORK/red" false | jget reason)"
expect "the block reason carries the gate's own ✗ line" yes "$(has "$RSN" "✗ TAIL:review has no evidence")"
expect "the block reason never says to untick a box" no "$(has "${RSN,,}" untick)"
expect "the hook asks for the NEWEST cycle only, --ticked-only (064, not 041)" yes "$(has "$RSN" "(args: --ticked-only 064)")"
expect "a project with no cycle yet → empty output" "" "$(stop "$WORK/nocyc" false)"

# Finding 1: closed cycles red, the newest one fine → the hook stays quiet.
expect "old cycles red, newest fine → empty output (work in progress is not charged)" "" "$(stop "$WORK/oldred" false)"
expect "red only when called with NO cycle number → empty output" "" "$(stop "$WORK/nocycle" false)"

# Finding 4: the root is $CLAUDE_PROJECT_DIR, never wherever the agent's cwd wandered.
expect "cwd in a subdirectory + CLAUDE_PROJECT_DIR → still measures (block)" block "$(stop "$WORK/red/scripts" false "$WORK/red" | jget decision)"
expect "cwd in a foreign project, CLAUDE_PROJECT_DIR elsewhere → green" "" "$(stop "$WORK/evil" false "$WORK/green")"
expect "…and the foreign script was never executed" no "$(yn test -e "$WORK/evil/scripts/EXECUTED")"
expect "CLAUDE_PROJECT_DIR without the method + foreign cwd → silent" "" "$(stop "$WORK/evil" false "$WORK/none")"
expect "…and the foreign script was still not executed" no "$(yn test -e "$WORK/evil/scripts/EXECUTED")"
expect "without CLAUDE_PROJECT_DIR the cwd is the reserve" block "$(stop "$WORK/red" false | jget decision)"

# Finding 9: broken UTF-8 in the gate's output must still BLOCK. errors="strict" raised, the
# hook failed open and the check silently never ran.
expect "half a UTF-8 character in the output → block, not fail-open" block "$(stop "$WORK/halfutf" false | jget decision)"

# ── d. merge-settings.py ──────────────────────────────────────────────────────────────
echo "── d. settings merge ──"
OURS="$WORK/ours.json"
echo '{"hooks":{"Stop":[{"hooks":[{"type":"command","command":"ours"}]}]}}' > "$OURS"
# The verdict is the first word of the first line. No pipe into `head`: that is anti-pattern 21.
verdict() {  # verdict <target> [source]
  local out first
  out="$(python3 "$MERGE" "$1" "${2:-$OURS}")"
  first="${out%%$'\n'*}"
  echo "${first%% *}"
}

expect "WRITE when the target is absent" WRITE "$(verdict "$WORK/absent.json")"
cp "$OURS" "$WORK/same.json"
expect "CURRENT when it carries our hooks" CURRENT "$(verdict "$WORK/same.json")"
echo '{"model":"x","hooks":{}}' > "$WORK/empty.json"
expect "MERGED when hooks are empty" MERGED "$(verdict "$WORK/empty.json")"
expect "MERGED keeps their other keys" x "$(python3 "$MERGE" "$WORK/empty.json" "$OURS" | tail -n +2 | python3 -c 'import json,sys; print(json.load(sys.stdin)["model"])')"
echo '{"hooks":{"Stop":[{"hooks":[{"type":"command","command":"theirs"}]}]}}' > "$WORK/theirs.json"
expect "CONFLICT when they configure different hooks" CONFLICT "$(verdict "$WORK/theirs.json")"

# UPGRADE is tested against a LITERAL copy of what v0.3.0 shipped (`git show 534a088:.claude/
# settings.json`), written here and not rebuilt from merge-settings.py's own PREVIOUS_HOOKS:
# a test that derives its input from the list under test passes when the list is wrong
# (anti-pattern 13). It is a literal and not a `git show` so a shallow clone cannot make the
# gate skip and read green while testing nothing. The third-party keys ("model", "permissions")
# are what a real project has next to our hooks; they must come out untouched.
cat > "$WORK/v030.json" <<'JSON'
{
  "model": "claude-opus-4",
  "permissions": {"allow": ["Bash(git status)"], "deny": ["Read(./.env)"]},
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write|NotebookEdit|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR/scripts/hooks/guard-immutables.py\""
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "startup|resume|clear|compact",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR/scripts/hooks/session-state.sh\""
          }
        ]
      }
    ]
  }
}
JSON
REAL_SETTINGS="$ROOT/.claude/settings.json"
expect "UPGRADE for the v0.3.0 settings" UPGRADE "$(verdict "$WORK/v030.json" "$REAL_SETTINGS")"
python3 "$MERGE" "$WORK/v030.json" "$REAL_SETTINGS" > "$WORK/upgrade.out"
FACTS="$(python3 - "$WORK/upgrade.out" "$WORK/v030.json" "$REAL_SETTINGS" <<'PY'
import json, sys
lines = open(sys.argv[1], encoding="utf-8").read().split("\n", 1)
merged = json.loads(lines[1])
before = json.load(open(sys.argv[2], encoding="utf-8"))
ours = json.load(open(sys.argv[3], encoding="utf-8"))
print("hooks-are-ours" if merged["hooks"] == ours["hooks"] else "hooks-differ")
print("keys-kept" if all(merged.get(k) == before[k] for k in ("model", "permissions")) else "keys-lost")
print("no-extra-keys" if set(merged) == set(before) else "extra-keys")
PY
)"
expect "UPGRADE: the resulting hooks are the repository's own" hooks-are-ours "$(sed -n 1p <<<"$FACTS")"
expect "UPGRADE: model and permissions come out identical" keys-kept "$(sed -n 2p <<<"$FACTS")"
expect "UPGRADE: no key appears or disappears" no-extra-keys "$(sed -n 3p <<<"$FACTS")"

echo
if [[ $FAIL -gt 0 ]]; then
  echo "✗ ledger gate: $FAIL failed, $PASS passed." >&2
  exit 1
fi
echo "✓ ledger gate: $PASS checks passed (recorder, report, Stop hook, settings merge)."
