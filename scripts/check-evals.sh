#!/usr/bin/env bash
# check-evals.sh — an evaluation case must discriminate, name a target, and stay fresh.
#
# What this actually measures (anti-pattern 13: know what your check measures): it does
# NOT judge any agent output — it cannot, and pretending otherwise would be the proxy
# trap. It measures the **health of the corpus**: whether each case names a target that
# exists, whether its assertions can tell a good answer from a plausible one, whether its
# baseline still refers to the target as it is today, and whether the case has ever been
# seen failing.
#
# The judging itself needs a model in the loop and runs on demand (`/eval`), never here —
# a gate everybody must be able to run cannot depend on an interface key.
#
# Anatomy of a case, under evals/<NNN-slug>/:
#   case.md      Target: · Question: · Axis: (the capability the case separates)
#                optional: Status: retired + Retired-because:
#   expect.md    >=1 "MUST-FIND:"  and  >=1 "MUST-NOT-CLAIM:"
#   baseline.md  Date: · Target-commit: · First-red: · Verdict: · Ablation: · Premise-checked:
#
# Exit 0 only when every case passes every condition.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

fail=0
pending=0
cases=0
retired=0

note() { printf '  %s\n' "$1"; }
bad()  { printf '  ✗ %s\n' "$1"; fail=1; }

echo "── Evaluation corpus (T7 / C11) ──"

if [[ ! -d evals ]]; then
  echo "✗ evals/ does not exist — there is no corpus to keep honest."
  exit 1
fi

for dir in evals/*/; do
  [[ -d "$dir" ]] || continue
  name="${dir%/}"; name="${name#evals/}"
  cases=$((cases + 1))
  echo "• $name"

  # ---- 1. structure -------------------------------------------------------
  missing=0
  for f in case.md expect.md baseline.md; do
    if [[ ! -f "$dir$f" ]]; then bad "missing $f"; missing=1; fi
  done
  [[ $missing -eq 0 ]] || continue

  # ---- 1b. retired cases are visible, never silent ------------------------
  # A case proved non-discriminating is retired, not deleted: the learning is the point.
  # Retirement is declared and carries its reason, so it cannot be used to hide a red.
  if grep -q '^Status: retired' "$dir/case.md"; then
    reason="$(grep -m1 '^Retired-because:' "$dir/case.md" | sed 's/^Retired-because:[[:space:]]*//' || true)"
    if [[ -z "$reason" ]]; then
      bad "retired with no 'Retired-because:' — retirement without a reason is deletion"
    else
      note "RETIRED — $reason"
      retired=$((retired + 1))
    fi
    continue
  fi

  # ---- 2. the target exists ----------------------------------------------
  target="$(grep -m1 '^Target:' "$dir/case.md" 2>/dev/null | sed 's/^Target:[[:space:]]*//' || true)"
  if [[ -z "$target" ]]; then
    bad "case.md has no 'Target:' line — an eval with no target measures nothing"
    continue
  elif [[ ! -e "$target" ]]; then
    bad "target does not exist: $target"
    continue
  else
    note "target: $target"
  fi

  if ! grep -q '^Question:' "$dir/case.md"; then
    bad "case.md has no 'Question:' line — the agent must be asked something specific"
  fi

  # The axis is the capability the case claims to separate. Without it there is nothing to
  # ablate, and a pass proves only that the target is competent — not that the case measures
  # anything (anti-pattern 19).
  if ! grep -q '^Axis:' "$dir/case.md"; then
    bad "case.md has no 'Axis:' line — a case with no axis has nothing to ablate"
  fi

  # ---- 3. the assertions discriminate ------------------------------------
  # A case that only asks "did it find something?" passes on any verbose answer.
  # The negative side is what separates a right answer from a plausible one.
  n_find="$(grep -c '^MUST-FIND:' "$dir/expect.md" || true)"
  n_not="$(grep -c '^MUST-NOT-CLAIM:' "$dir/expect.md" || true)"
  if [[ "$n_find" -lt 1 ]]; then
    bad "expect.md has no MUST-FIND: — nothing says what a correct answer contains"
  fi
  if [[ "$n_not" -lt 1 ]]; then
    bad "expect.md has no MUST-NOT-CLAIM: — with no negative side the case does not discriminate"
  fi
  [[ "$n_find" -ge 1 && "$n_not" -ge 1 ]] && note "assertions: ${n_find} must-find / ${n_not} must-not-claim"

  # ---- 4. the baseline is honest and fresh --------------------------------
  # Ablation and Premise-checked are required because both were learned the hard way:
  # a case nobody failed proves nothing (19), and a fixture whose symptom does not
  # reproduce tests the author rather than the target (20).
  for field in Date Target-commit First-red Verdict Ablation Premise-checked; do
    grep -q "^${field}:" "$dir/baseline.md" || bad "baseline.md has no '${field}:' line"
  done

  first_red="$(grep -m1 '^First-red:' "$dir/baseline.md" 2>/dev/null | sed 's/^First-red:[[:space:]]*//' || true)"
  recorded="$(grep -m1 '^Target-commit:' "$dir/baseline.md" 2>/dev/null | sed 's/^Target-commit:[[:space:]]*//' || true)"

  if [[ "$first_red" == "pending" ]]; then
    # Second law of verifiable-dod: a check nobody has ever seen complain is a hope.
    bad "never seen failing (First-red: pending) — run /eval and record the run"
    pending=$((pending + 1))
    continue
  fi

  if [[ "$recorded" == "pending" ]]; then
    bad "Target-commit: pending while First-red is set — the baseline is not attributable"
    continue
  fi

  current="$(git log -1 --format=%h -- "$target" 2>/dev/null || true)"
  if [[ -z "$current" ]]; then
    note "target not in git history yet — freshness not checked"
  elif [[ "$recorded" != "$current" ]]; then
    # The real failure mode: somebody improves (or breaks) an agent and never re-evaluates.
    bad "stale baseline — target moved ${recorded} → ${current}; re-run /eval"
  else
    note "baseline fresh at ${current}"
  fi
done

echo "──"
echo "cases: ${cases} · retired: ${retired} · pending baselines: ${pending}"

if [[ $fail -ne 0 ]]; then
  echo "✗ evaluation corpus is not healthy (see above)."
  exit 1
fi
if [[ $cases -eq 0 ]]; then
  # Not the same as coverage. A fresh install has no cases, and saying "green" without
  # this line would read as "the agents are evaluated" — which is the proxy trap.
  echo "✓ corpus is well formed — and empty. Nothing here is evaluated yet."
  exit 0
fi
echo "✓ every case names a real target, discriminates, and is fresh."
