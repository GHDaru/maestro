#!/usr/bin/env bash
# check-conformance.sh — the executable answer to "are you following Maestro?".
#
# That question must never be answered from memory. An agent asked in conversation reports
# its INTENTION, not the facts: in cycle 041 this repository's own agent would have answered
# "yes" while two commits cited a cycle that had no spec at all — the gate found it, the
# memory did not. And a companion agent on another repository reported "CI green" before
# checking it. Memory is not a witness.
#
# What this actually measures (anti-pattern 13): NOT quality, and not whether the human read
# anything. It measures whether the method survived into the artifacts the executor consumes
# — which is the defect that keeps recurring (anti-pattern 22, the installed method as a
# lossy copy). Everything here is a fact readable from disk and git.
#
# It does not re-check what other gates own: lane rationale is check-cycle.sh, roles are
# check-roles.sh, findings debt is check-retro.sh. Duplicating a function already served
# would violate Principle VI.
#
# Machine-readable tokens, not prose, so the check survives translation and rewording
# (the same reasoning as the `fecha` field and the `PT-DATA` marker):
#
#   plan.md   ART:<artifact>=yes|no   for research · data-model · contracts · checklist · ux-design
#             declaring =yes means the file must exist in the cycle directory
#   tasks.md  TAIL:review · TAIL:security · TAIL:gate      (present, or "n/a:" with a reason)
#   qa-report.md   each TAIL token that is not n/a, with its evidence
#
# Usage:  scripts/check-conformance.sh          # every cycle from the floor onward
#         scripts/check-conformance.sh 042      # one cycle, verbose
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# Retroactivity turns a gate into noise: the rule applies from the cycle that introduced it.
# The debt of older cycles is declared, not erased (same precedent as check-cycle.sh).
FLOOR="${MAESTRO_MIN_CYCLE_CONFORMANCE:-42}"
ONLY="${1:-}"

ARTIFACTS=(research data-model contracts checklist ux-design)
TAIL=(review security gate)

fail=0
checked=0

# A placeholder is not content. The generator writes <...>, the vendored templates write
# [...] — and the templates WIN on divergence (.specify/UPSTREAM.md), so both must be
# rejected. The first version of this gate knew only about <...>, which let a freshly
# generated skeleton pass entirely green: zero work, exit 0. Found by the independent
# review of this very cycle.
is_placeholder() {  # $1 = candidate text
  local t="${1//[\`|*_ ]/}"
  [[ -z "$t" || "$t" == *"<"* || "$t" == *"["* ]]
}

ok()   { printf '    ✓ %s\n' "$1"; }
bad()  { printf '    ✗ %s\n' "$1"; fail=1; }
note() { printf '    · %s\n' "$1"; }

echo "── Conformance: did the method survive into the artifacts? ──"
echo "   (floor: cycle ${FLOOR}; older cycles carry declared debt — see the roadmap)"

for d in specs/[0-9][0-9][0-9]-*/; do
  [[ -d "$d" ]] || continue
  n="$(basename "$d" | cut -d- -f1)"
  if [[ -n "$ONLY" ]]; then
    [[ "$((10#$n))" -eq "$((10#$ONLY))" ]] || continue
  else
    [[ "$((10#$n))" -ge "$((10#$FLOOR))" ]] || continue
  fi
  checked=$((checked + 1))
  echo "• $(basename "$d")"

  # ---- 1. the four artifacts of a cycle exist ------------------------------
  incomplete=0
  for f in spec.md plan.md tasks.md qa-report.md; do
    [[ -f "$d$f" ]] || { bad "missing $f"; incomplete=1; }
  done
  [[ $incomplete -eq 0 ]] || continue

  # ---- 2. the Constitution Check is complete ------------------------------
  # Omission violates nothing visibly, which is exactly why it needs a count.
  rows="$(grep -cE '^\| *[IVX]+\. ' "$d/plan.md" || true)"
  principles="$(grep -cE '^### [IVX]+\. ' docs/governance/principles.md || true)"
  if [[ "$rows" -ne "$principles" ]]; then
    bad "Constitution Check has ${rows} of ${principles} principles — a partial check is not a check"
  else
    ok "Constitution Check complete (${rows}/${principles})"
  fi

  # ---- 3. every conditional artifact is DECLARED, never merely absent ------
  # Silence is not auditable; "does not apply because X" is. This is the antidote to the
  # lossy copy: the author has to look at all five and decide in writing.
  missing_decl=()
  art_bad=0
  for a in "${ARTIFACTS[@]}"; do
    line="$(grep -m1 "ART:${a}=" "$d/plan.md" || true)"
    if [[ -z "$line" ]]; then
      missing_decl+=("$a")
      continue
    fi
    value="$(sed -E "s/.*ART:${a}=([A-Za-z]*).*/\1/" <<<"$line")"
    if [[ "$value" != "yes" && "$value" != "no" ]]; then
      bad "${a}: ART:${a}=${value:-<empty>} — the only declarations are yes and no"
      art_bad=1; continue
    fi
    # The reason is what makes a `no` a decision instead of a shrug. Five copied
    # placeholders were a conformant plan until the review of cycle 042 said so.
    reason="$(sed -E "s/.*ART:${a}=[A-Za-z]*//" <<<"$line" | tr -d '|')"
    if is_placeholder "$reason"; then
      bad "${a}: declared ART:${a}=${value} with no reason — a declaration without a why is silence"
      art_bad=1; continue
    fi
    if [[ "$value" == "yes" ]]; then
      # Declaring an artifact and not producing it is worse than not declaring it.
      if [[ -e "$d${a}.md" || -e "$d${a}" ]]; then
        ok "${a}: declared and present"
      else
        bad "${a}: declared ART:${a}=yes but no ${a}.md in the cycle"; art_bad=1
      fi
    fi
  done
  if [[ ${#missing_decl[@]} -gt 0 ]]; then
    bad "artifacts never declared (neither yes nor no): ${missing_decl[*]}"
  elif [[ "$art_bad" -eq 0 ]]; then
    ok "all ${#ARTIFACTS[@]} conditional artifacts declared with a reason"
  fi

  # ---- 4. the closing tail survived into tasks.md -------------------------
  # This is the defect that broke a cycle on another repository: the tail lived in the
  # spec and in working memory, never in the checklist the executor follows — and context
  # compaction promoted the truncated version to source of truth (corollary C12).
  for t in "${TAIL[@]}"; do
    line="$(grep -m1 "TAIL:${t}" "$d/tasks.md" || true)"
    if [[ -z "$line" ]]; then
      bad "tasks.md has no TAIL:${t} — the step is not in the list the executor follows"
      continue
    fi
    if [[ "$line" == *"n/a:"* ]]; then
      reason="$(sed 's/.*n\/a: *//' <<<"$line" | sed 's/[`).]*$//' | cut -c1-60)"
      if is_placeholder "$reason"; then
        bad "TAIL:${t} says n/a with a placeholder reason — write why, or do the step"
      else
        note "TAIL:${t} not applicable — ${reason}"
      fi
      continue
    fi
    # ---- 5. an applicable tail step needs evidence, not a ticked box -------
    # Presence of the token is NOT evidence: new-cycle.sh writes the tokens into every
    # generated qa-report.md, so testing for presence made the generator pre-satisfy the
    # check. What is read is what comes AFTER the token on its line.
    ev="$(grep -m1 "TAIL:${t}" "$d/qa-report.md" || true)"
    if [[ -z "$ev" ]]; then
      bad "TAIL:${t} applies but is absent from qa-report.md — a tick is not a witness"
      continue
    fi
    # Strip ONLY the separator (spaces, dashes, em dash, colon) — stripping every
    # non-alphanumeric ate the leading "<" of the placeholder and blinded the test.
    ev="$(sed -E "s/.*TAIL:${t}//; s/^[[:space:]*_—–:-]*//" <<<"$ev")"
    if is_placeholder "$ev"; then
      bad "TAIL:${t} in qa-report.md is still the placeholder — nobody wrote what happened"
    else
      ok "TAIL:${t} evidence: $(cut -c1-58 <<<"$ev")"
    fi
  done
done

echo "──"
if [[ "$checked" -eq 0 ]]; then
  # Exiting 0 here turned the floor knob into an off switch with a success code.
  echo "✗ no cycle in range (floor ${FLOOR}${ONLY:+, filter ${ONLY}}) — the gate checked nothing."
  exit 1
fi
echo "cycles checked: ${checked}"
if [[ $fail -ne 0 ]]; then
  echo "✗ the method did not survive into the artifacts of at least one cycle."
  exit 1
fi
echo "✓ every cycle checked declares its artifacts and carries the closing tail with evidence."
