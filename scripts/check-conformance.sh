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
#   tasks.md  TAIL:review · TAIL:security · TAIL:gate · TAIL:mutation (from cycle 055)
#             present, or "n/a" with a reason — and TAIL:mutation's n/a is checked
#             against the diff, never against the sentence
#   qa-report.md   each TAIL token that is not n/a, with its evidence
#
# Usage:  scripts/check-conformance.sh                # every cycle from the floor onward
#         scripts/check-conformance.sh 042            # one cycle, verbose
#         scripts/check-conformance.sh --ticked-only  # the half that can BLOCK (cycle 061)
#
# Why --ticked-only exists. This gate is advisory by design, and the reason is good: an open
# cycle carries unticked TAIL boxes and a placeholder qa-report.md, so a blocking version
# would be red for the whole life of every branch — and a gate that is always red is one
# people learn to scroll past (cycle 043). The cost of that was measured: in FOUR consecutive
# cycles (057, 058, 059, 060) the four boxes were ticked with no qa-report.md in existence,
# and only the human review caught it. Four times is not inattention; it is that nothing
# charges for it.
#
# But half of the rule is checkable at any moment and never red on work in progress: IF YOU
# TICKED IT, THE EVIDENCE MUST EXIST. A cycle with nothing ticked passes. A cycle that ticked
# and can show it passes. Only a claim without backing fails — anti-pattern 13 read backwards:
# instead of measuring the phrase, measure whether the phrase has anything under it.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# Retroactivity turns a gate into noise: the rule applies from the cycle that introduced it.
# The debt of older cycles is declared, not erased (same precedent as check-cycle.sh).
FLOOR="${MAESTRO_MIN_CYCLE_CONFORMANCE:-42}"
# The no-checkbox rule starts at 045 (cycle that introduced it); older cycles keep theirs.
CRIT_FLOOR="${MAESTRO_MIN_CYCLE_CRITERIA:-45}"
TICKED_ONLY=0
ONLY=""
for arg in "$@"; do
  case "$arg" in
    --ticked-only) TICKED_ONLY=1 ;;
    -*) echo "usage: check-conformance.sh [--ticked-only] [NNN]" >&2; exit 2 ;;
    *)  ONLY="$arg" ;;
  esac
done

ARTIFACTS=(research data-model contracts checklist ux-design)
TAIL=(review security gate)
# TAIL:mutation joins the tail from cycle 055 (the retrospective that created it). Older
# cycles are evidence, not target — same precedent as FLOOR above.
#
# A knob that fails OPEN is not a knob, it is a switch: `MAESTRO_MIN_CYCLE_MUTATION=999`
# excused every cycle and still printed the success line, and a typo (`=abc`) blew up the
# arithmetic, dropped the step and ALSO exited 0. Both found by the independent review of
# this cycle. It is now validated, and a floor above the newest cycle is a failure, not a
# quiet exemption — the same protection FLOOR got in cycle 048.
# The declared-absence half of is_placeholder starts at 061 (the cycle whose promotion
# exposed it). Validated like MUT_FLOOR below: a floor that fails OPEN is not a knob.
ABSENCE_FLOOR="${MAESTRO_MIN_CYCLE_ABSENCE:-61}"
ABSENCE_FLOOR_DEFAULT=61
[[ "$ABSENCE_FLOOR" =~ ^[0-9]+$ ]] || {
  echo "✗ MAESTRO_MIN_CYCLE_ABSENCE='${ABSENCE_FLOOR}' is not a number — refusing to run with an unreadable floor." >&2
  exit 1
}
# A knob that only TIGHTENS cannot be an off switch. Guarding only "above the newest cycle"
# left `=61+n` free: setting the floor to the cycle in progress excuses every cycle already
# written, and prints success. Raising it is now refused outright (review of cycle 063).
[[ "$((10#$ABSENCE_FLOOR))" -le "$ABSENCE_FLOOR_DEFAULT" ]] || {
  echo "✗ MAESTRO_MIN_CYCLE_ABSENCE=${ABSENCE_FLOOR} is above the built-in floor ${ABSENCE_FLOOR_DEFAULT} — this knob may only tighten the rule, never relax it." >&2
  exit 1
}

MUT_FLOOR="${MAESTRO_MIN_CYCLE_MUTATION:-55}"
[[ "$MUT_FLOOR" =~ ^[0-9]+$ ]] || {
  echo "✗ MAESTRO_MIN_CYCLE_MUTATION='${MUT_FLOOR}' is not a number — refusing to run with an unreadable floor." >&2
  exit 1
}

# What counts as a gate for this rule. The first version listed only `scripts/check-*.sh`
# and the book engine, and the review walked straight through the gap: `boundary.json`
# (read by four checks), `publicar/sumario.json` (the DECLARED SET whose blind spot was
# cycle 054's own defect), `package-plugin.sh --verify` and the CI workflow are all gates
# in practice. `companion/` is excluded on purpose — it is another domain, and charging it
# would cross the boundary this repository enforces.
GATE_PATHS_RE='(^|/)scripts/check-[A-Za-z0-9_-]+\.sh$|(^|/)scripts/package-plugin\.sh$|(^|/)publicar/(build\.mjs|sumario\.json)$|(^|/)boundary\.json$|(^|/)\.github/workflows/[^/]+\.ya?ml$'
GATE_PATHS_SKIP_RE='^companion/'

# Did this cycle touch a gate? Answered by the FACT — the files its commits changed, plus
# the working tree when the cycle's own artifacts are themselves uncommitted — never by
# what the plan says it did. Reading the prose would be measuring the phrase inside the
# gate built to stop exactly that (anti-pattern 13).
#
# `-i` on the subject search because check-cycle.sh accepts the citation case-insensitively:
# a commit reading `(Spec 055)` satisfied the traceability gate and matched nothing here,
# so the two gates disagreed about which commits belong to a cycle.
#
# The working tree is attributed to every cycle whose own directory is dirty, not to "the
# newest cycle": scaffolding the NEXT cycle used to make the current one's uncommitted gate
# change stop counting — one `new-cycle.sh` away from the dispensation.
DIRTY_PATHS="$(git status --porcelain -uall 2>/dev/null | cut -c4- || true)"

# The newest cycle on disk — used only to catch a mutation floor set above every cycle
# there is. Kept assigned even when there is none: under `set -u` an unset name aborts the
# script at the closing check, which is how the floor sanity block silently died the first
# time it ran (found by the mutation this cycle mandates, on its own code).
gate_claimed=0
gate_claimed_by=""
NEWEST_CYCLE=""
{ shopt -s nullglob; _all=(specs/[0-9][0-9][0-9]-*/); shopt -u nullglob
  [[ ${#_all[@]} -gt 0 ]] && NEWEST_CYCLE="$(basename "${_all[${#_all[@]}-1]}" | cut -d- -f1)"; } || true

cycle_touched_a_gate() {  # $1 = NNN
  local n="$1" files="" sha
  while IFS= read -r sha; do
    [[ -n "$sha" ]] || continue
    files+="$(git show --pretty=format: --name-only "$sha" 2>/dev/null)"$'\n'
  # `spec NNN` OR `ciclo NNN` OR `cycle NNN`. Matching only "spec" left the dispensation
  # buyable by writing the OTHER word this repository uses for the same thing: no commit of
  # cycle 061 says "spec 061" — they all say "ciclo 061" — so the cycle that changed FIVE
  # gates could have written `TAIL:mutation — n/a` and passed. Found by the independent
  # review of 061-062, in the function whose own comment brags about closing this hole.
  done < <(git log --all -i --format=%H --grep="spec ${n}" --grep="ciclo ${n}" --grep="cycle ${n}" 2>/dev/null || true)
  if grep -qE "^specs/0*${n}-" <<<"$DIRTY_PATHS"; then
    files+="${DIRTY_PATHS}"$'\n'
  fi
  # Here-string, never a pipe into `grep -q`: that shape is anti-pattern 21, and it has
  # already killed two scripts in this repository.
  files="$(grep -vE "$GATE_PATHS_SKIP_RE" <<<"$files" || true)"
  grep -qE "$GATE_PATHS_RE" <<<"$files"
}

fail=0
checked=0

# A placeholder is not content. The generator writes <...>, the vendored templates write
# [...] — and the templates WIN on divergence (.specify/UPSTREAM.md), so both must be
# rejected. The first version of this gate knew only about <...>, which let a freshly
# generated skeleton pass entirely green: zero work, exit 0. Found by the independent
# review of this very cycle.
# is_placeholder(): text that is NOT evidence. THREE shapes, and the last two each cost a cycle.
#
#   (a) the generated skeleton — empty, or carrying a `<marker>` / `[marker]`;
#   (b) TOO SHORT TO BE EVIDENCE. Measured, not guessed: across the 54 tail evidences in this
#       repository the shortest legitimate one is 65 characters, and every fake found so far is
#       20 or less (`pendente.`, `(pendente)`, `NÃO EXECUTADA.`, `n/a`, `ok`). The floor sits at
#       40 — a wide gap on both sides — and it is the half that CANNOT be reworded around. That
#       matters: the first version of this rule was a word list, and the independent review of
#       cycle 063 walked through it five times — with an adverb in front, with the plural, in
#       parentheses, behind a quote marker, and in capitals;
#   (c) DECLARED ABSENCE opening a LONGER sentence — `pendente. DoD verde; falta o parecer…`
#       is 70 characters and is still the absence of the step.
#
# What the word list also got wrong: it REFUSED the truth. `todo` was in it, and it opens an
# ordinary Portuguese sentence meaning "the whole". A gate that rejects a true
# statement is worse than one that accepts a false one. `todo` is gone; `to do` and `todo:`
# stay. `em aberto`, `falta` and `faltou` went the same way: "Em aberto ficou apenas a dívida
# editorial; a revisão rodou" opens with the phrase and reports that the step HAPPENED. The
# short forms of all three are caught by the length floor anyway, which is the point of having
# a rule that does not depend on wording.
#
# And the stripping used a bracket class holding `—` and `–` — a set of BYTES in the C locale,
# not characters — so `• pendente` had two of its three bytes eaten and passed. That is the
# `[├└]` defect of cycle 060, reintroduced in the cycle that quotes it. Leading markup is now
# removed by its COMPLEMENT (`[^[:alnum:]]`), which needs no multibyte class at all, and the
# accents are folded by ALTERNATION, never by a bracket class — so the rule no longer depends
# on the locale either (nothing here exports LC_ALL).
#
# The vocabulary is DATA, not prose: this gate reads qa-reports, and the book side of this
# repository is written in Portuguese by decision (ADR 0014). Both languages, one list.
DECLARED_ABSENCE='pendente|pendentes|pendencia|aguardando|aguarda|a fazer|por fazer|nao (foi |sera |vai )?(execut|feit|rod|realiz|hav)|sem (revisao|parecer|evidencia)|nenhuma evidencia|tbd|a definir|n/d|to do|todo:|pending|not (run|executed|done)'   # PT-DATA (evidence is read in both languages)
EVIDENCE_MIN_CHARS=40

fold_pt() {  # accents by ALTERNATION — a bracket class of multibyte chars is a byte class
  sed -E 's/(á|à|ã|â|Á|À|Ã|Â)/a/g; s/(é|ê|É|Ê)/e/g; s/(í|Í)/i/g; s/(ó|ô|õ|Ó|Ô|Õ)/o/g; s/(ú|Ú)/u/g; s/(ç|Ç)/c/g' <<<"$1" \
    | tr '[:upper:]' '[:lower:]'
}

# is_skeleton(): shape (a) alone. This is the right test for a SHORT, legitimate phrase — the
# reason behind an `ART:x=no` ("Nenhuma entidade.", 17 characters) or behind an `n/a`. The
# length floor below was measured on TAIL EVIDENCE, which is prose about what happened; using
# it on a reason would reject every honest one. One of the three call sites also passed no
# cycle number, so the absence rule reached every cycle ever through it, against FR3 — that
# call site is this function now, and the floor argument stopped being optional by accident.
is_skeleton() {  # $1 = candidate text
  local t="${1//[\`|*_ ]/}"
  [[ -z "$t" || "$t" == *"<"* || "$t" == *"["* ]]
}

is_placeholder() {  # $1 = candidate text, $2 = cycle number (REQUIRED)
  local t="${1//[\`|*_ ]/}"
  [[ -z "$t" || "$t" == *"<"* || "$t" == *"["* ]] && return 0
  [[ -n "${2:-}" ]] || { echo "✗ internal: is_placeholder called with no cycle number" >&2; return 0; }
  # (b) and (c) apply from the cycle that introduced them. Cycles 042-045 wrote a
  # declared-absence sentence in TAIL:gate when it WAS true, and were promoted afterwards;
  # failing them today would make the gate noise. Same precedent as FLOOR, CRIT_FLOOR and
  # MUT_FLOOR — the debt of older cycles is declared, not erased.
  [[ "$((10#$2))" -lt "$((10#$ABSENCE_FLOOR))" ]] && return 1
  local head; head="$(fold_pt "$(sed -E 's/^[^[:alnum:]]+//' <<<"$1")")"
  [[ "${#head}" -lt "$EVIDENCE_MIN_CHARS" ]] && return 0
  grep -qE "^(${DECLARED_ABSENCE})" <<<"$head"
}

ok()   { printf '    ✓ %s\n' "$1"; }
bad()  { printf '    ✗ %s\n' "$1"; fail=1; }
note() { printf '    · %s\n' "$1"; }
# soft(): a rule that is true of a FINISHED cycle but not of one in progress. In the default
# (advisory) run it fails like any other; under --ticked-only it is reported and does NOT
# fail, because that mode blocks on exactly one thing — a tick with nothing under it. A
# freshly generated cycle fails every one of these (the skeleton declares ART:*=no with no
# reason), so leaving them hard would rebuild the always-red gate the mode exists to avoid.
soft() { if [[ "${TICKED_ONLY:-0}" -eq 1 ]]; then printf '    · %s\n' "$1"; else bad "$1"; fi; }

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
  # A cycle between /speckit.specify and /speckit.tasks has spec.md and nothing else — the
  # spec-kit flow this repository documents creates them one at a time. Under --ticked-only
  # that is work in progress, not a violation: `new-cycle.sh` writing all four at once was
  # the only reason this never showed, and the mode's own promise ("a cycle with nothing
  # ticked passes") was false for anyone following the other documented path.
  # Found by the independent review of cycles 061-062 — in the gate written to avoid exactly
  # the always-red shape it had.
  incomplete=0
  for f in spec.md plan.md tasks.md qa-report.md; do
    [[ -f "$d$f" ]] || { soft "missing $f"; incomplete=1; }
  done
  # Softening the four artifacts opened a hole CHEAPER than the one it closed: `rm qa-report.md`
  # made --ticked-only skip the whole cycle — tail rows, evidence, everything — and exit 0,
  # with four boxes ticked. That is precisely the 057-060 defect this mode was built for.
  # A ticked box is a claim; deleting the file the claim points at is not work in progress.
  if [[ -f "$d/tasks.md" && ! -f "$d/qa-report.md" ]] \
     && grep -qE '^[[:space:]]*- \[[xX]\] \**TAIL:' "$d/tasks.md"; then
    bad "tasks.md ticks a TAIL box and there is no qa-report.md — deleting the record is not the same as writing it"
  fi
  [[ $incomplete -eq 0 ]] || continue

  # ---- 2. the Constitution Check is complete ------------------------------
  # Omission violates nothing visibly, which is exactly why it needs a count.
  rows="$(grep -cE '^\| *[IVX]+\. ' "$d/plan.md" || true)"
  principles="$(grep -cE '^### [IVX]+\. ' docs/governance/principles.md || true)"
  if [[ "$rows" -ne "$principles" ]]; then
    soft "Constitution Check has ${rows} of ${principles} principles — a partial check is not a check"
  else
    ok "Constitution Check complete (${rows}/${principles})"
  fi

  # ---- 2b. the spec states criteria; the qa-report says whether they held ---
  # A checkbox in the spec duplicates a function the qa-report already owns, and a box
  # ticked before the work exists turns the criterion into a plan. Four occurrences across
  # cycles 042-044, in two different tokens, by the same author. The form is the fix.
  # -E for portability: `\|` alternation in a BRE is a GNU extension, and on BSD sed the
  # range would never open — the gate would go green on every spec, forever, on a laptop.
  crit="$(sed -nE '/^## (Critérios de aceite|Acceptance criteria)/,/^## /p' "$d/spec.md" || true)"  # PT-DATA (older cycles)
  if [[ -z "$crit" ]]; then
    # A gate that cannot tell "clean" from "did not look" is the failure this repository has
    # already named twice (corollary C5, anti-pattern 16). Not finding the section is a
    # finding, never a pass.
    soft "spec.md has no acceptance-criteria section the gate can locate — rename it to '## Acceptance criteria' or '## Critérios de aceite'"
  else
    # The WHOLE family of checkbox spellings: -, *, +, any indentation, [ ] or [x] or [X].
    boxes="$(grep -cE '^[[:space:]]*[-*+] \[' <<<"$crit" || true)"
    if [[ "$((10#$n))" -lt "$((10#$CRIT_FLOOR))" ]]; then
      note "acceptance-criteria checkboxes: not checked below cycle ${CRIT_FLOOR}"
    elif [[ "$boxes" -gt 0 ]]; then
      soft "spec.md has ${boxes} checkbox(es) in the acceptance criteria — the spec states what must hold; the qa report says whether it did"
    else
      ok "acceptance criteria located and stated without checkboxes"
    fi
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
      soft "${a}: ART:${a}=${value:-<empty>} — the only declarations are yes and no"
      art_bad=1; continue
    fi
    # The reason is what makes a `no` a decision instead of a shrug. Five copied
    # placeholders were a conformant plan until the review of cycle 042 said so.
    reason="$(sed -E "s/.*ART:${a}=[A-Za-z]*//" <<<"$line" | tr -d '|')"
    if is_skeleton "$reason"; then
      soft "${a}: declared ART:${a}=${value} with no reason — a declaration without a why is silence"
      art_bad=1; continue
    fi
    if [[ "$value" == "yes" ]]; then
      # Declaring an artifact and not producing it is worse than not declaring it.
      if [[ -e "$d${a}.md" || -e "$d${a}" ]]; then
        ok "${a}: declared and present"
      else
        soft "${a}: declared ART:${a}=yes but no ${a}.md in the cycle"; art_bad=1
      fi
    fi
  done
  if [[ ${#missing_decl[@]} -gt 0 ]]; then
    soft "artifacts never declared (neither yes nor no): ${missing_decl[*]}"
  elif [[ "$art_bad" -eq 0 ]]; then
    ok "all ${#ARTIFACTS[@]} conditional artifacts declared with a reason"
  fi

  # ---- 4. the closing tail survived into tasks.md -------------------------
  # This is the defect that broke a cycle on another repository: the tail lived in the
  # spec and in working memory, never in the checklist the executor follows — and context
  # compaction promoted the truncated version to source of truth (corollary C12).
  # Recorded per cycle, so scaffolding a newer one cannot make an older claim stop counting.
  if grep -qE "^[[:space:]]*- \[[xX]\] \**TAIL:gate" "$d/tasks.md" 2>/dev/null; then
    gate_claimed=$((gate_claimed + 1)); gate_claimed_by="$n"   # newest claimer wins the label
  fi

  tail_steps=("${TAIL[@]}")
  [[ "$((10#$n))" -ge "$((10#$MUT_FLOOR))" ]] && tail_steps+=(mutation)

  for t in "${tail_steps[@]}"; do
    # The TAIL ROW, not the first line that happens to name the token. Unanchored, a task
    # line that merely MENTIONS `TAIL:mutation` (this cycle's own T3 does) was matched
    # first, and the real row — carrying the `n/a:` — was never read: the n/a refusal
    # silently could not fire. Found by running the mutation this very cycle makes
    # mandatory, which is the whole argument for the rule (anti-pattern 13, again).
    line="$(grep -m1 -E "^[[:space:]]*- \[[ xX]\] \**TAIL:${t}\**" "$d/tasks.md" || true)"
    if [[ -z "$line" ]]; then
      # NOT soft. The template says `never delete`, and under --ticked-only a deleted row used
      # to be a dot: four `sed -i /TAIL:/d` silenced the blocking gate completely. Removing the
      # question is not the same as leaving it unanswered — an absent row is the one shape that
      # cannot be work in progress, because `new-cycle.sh` writes all four rows on day one.
      bad "tasks.md has no TAIL:${t} — the row was deleted, and the template says never delete"
      continue
    fi
    # An UNTICKED box is a step not yet done, which is what an open cycle looks like. In
    # --ticked-only mode that is not a violation and must not be one, or the blocking gate
    # becomes the always-red gate this mode exists to avoid.
    ticked=0; [[ "$line" =~ ^[[:space:]]*-[[:space:]]\[[xX]\] ]] && ticked=1
    if [[ "$TICKED_ONLY" -eq 1 && "$ticked" -eq 0 ]]; then
      note "TAIL:${t} not ticked yet — nothing claimed, nothing owed"
      continue
    fi
    # `n/a` is recognised however it is spelled and however it is separated from its
    # reason. Matching the literal `n/a:` meant `N/A:` and `n/a — ` fell through to the
    # evidence branch, where the sentence WAS the evidence: a capital letter bought the
    # dispensation. Found by the review of this cycle, in the gate written to stop a gate
    # from measuring the phrase.
    lower="$(tr '[:upper:]' '[:lower:]' <<<"$line")"
    if [[ "$lower" == *"n/a"* ]]; then
      # The dispensation exists for a cycle that did not touch a gate. A cycle that DID
      # touch one and writes n/a is declining to prove exactly what independent review
      # found vacuous in six of the nine cycles 046-054 — so the answer comes from the
      # diff, not from the sentence.
      if [[ "$t" == "mutation" ]] && cycle_touched_a_gate "$n"; then
        bad "TAIL:mutation says n/a, but this cycle changed a gate — break it on purpose and show it failing"
        continue
      fi
      reason="$(sed -E 's/.*[nN]\/[aA][[:space:]]*[:—–-]*[[:space:]]*//' <<<"$line" | sed 's/[`).]*$//' | cut -c1-60)"
      if is_skeleton "$reason"; then
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
    # Same anchoring on this side: the evidence is a BULLET that opens with the token, not
    # any sentence that names it. Prose in a qa-report discussing `TAIL:review` used to be
    # accepted as the evidence for it.
    ev="$(grep -m1 -E "^[[:space:]]*[-*][[:space:]]+\**TAIL:${t}\**" "$d/qa-report.md" || true)"
    if [[ -z "$ev" ]]; then
      bad "TAIL:${t} applies but is absent from qa-report.md — a tick is not a witness"
      continue
    fi
    # Strip ONLY the separator (spaces, dashes, em dash, colon) — stripping every
    # non-alphanumeric ate the leading "<" of the placeholder and blinded the test.
    ev="$(sed -E "s/.*TAIL:${t}//; s/^[[:space:]*_—–:-]*//" <<<"$ev")"
    if is_placeholder "$ev" "$n"; then
      bad "TAIL:${t} in qa-report.md is still the placeholder — nobody wrote what happened"
    else
      ok "TAIL:${t} evidence: $(cut -c1-58 <<<"$ev")"
    fi
  done
done

# ---- 6. TAIL:gate ticked is the claim "the battery passed" (cycle 061) ------
# The plugin fell out of sync in FOUR consecutive cycles — 057, 058, 059, 060 — always the
# same way: the cycle edited a file that package-plugin.sh packages, and nobody repackaged.
# It never reached main, because ci.yml already runs `--verify`; what it cost was four rounds
# of human review. This is not that step duplicated. CI catches it at PUSH time; this catches
# it at CLAIM time, which is the moment the false sentence gets written into the qa-report.
#
# It used to look only at $NEWEST_CYCLE, and that was the exact hole cycle_touched_a_gate's own
# comment brags about closing: opening the next cycle with new-cycle.sh made the claim of the
# previous one stop being charged — one scaffold away from the dispensation. And `-z "$ONLY"`
# switched it off for a single-cycle run too. The plugin is ONE state for the whole repository,
# so the question is not "which cycle claimed it": if any cycle in range ticked TAIL:gate, the
# battery that claim names must actually pass. (Independent review of cycles 061-062.)
if [[ "$TICKED_ONLY" -eq 1 && "$gate_claimed" -gt 0 ]]; then
  echo ""
  echo "── TAIL:gate is ticked on ${gate_claimed_by} (${gate_claimed} cycle(s) claim it): the battery must actually pass ──"
  if [[ -x scripts/package-plugin.sh ]]; then
    if scripts/package-plugin.sh --verify >/dev/null 2>&1; then
      ok "plugin in sync with its sources"
    else
      bad "TAIL:gate says the battery passed, and package-plugin.sh --verify disagrees — repackage"
    fi
  else
    # An installed copy does not carry package-plugin.sh. Saying so is the difference between
    # "checked and clean" and "did not look" — the silence here was the same failure shape
    # this whole cycle is about.
    note "package-plugin.sh is not here (installed copy?) — the plugin half of the claim was not checked"
  fi
fi

echo "──"
if [[ "$checked" -eq 0 ]]; then
  # A project with NO cycle at all has nothing to be non-conformant about — it just installed
  # the method. That is different from "there are cycles and none is in range", which is the
  # floor knob being used as an off switch with a success code (the reason this block exists).
  # Both are said out loud; only the second is a failure. (cycle 048)
  shopt -s nullglob; all=(specs/[0-9][0-9][0-9]-*/); shopt -u nullglob
  if [[ ${#all[@]} -eq 0 && -z "$ONLY" ]]; then
    echo "· no cycle in this repository yet — nothing to check. Open one: scripts/new-cycle.sh 001 <slug>"
    exit 0
  fi
  echo "✗ no cycle in range (floor ${FLOOR}${ONLY:+, filter ${ONLY}}) — the gate checked nothing."
  exit 1
fi
echo "cycles checked: ${checked}"
# The mutation floor gets the same protection FLOOR got: a floor above every cycle that
# exists excuses the whole rule, and doing that silently with exit 0 is the off-switch
# shape (cycle 048). Saying it out loud is the difference between a knob and a switch.
if [[ -n "$NEWEST_CYCLE" && "$((10#$MUT_FLOOR))" -gt "$((10#$NEWEST_CYCLE))" ]]; then
  echo "✗ mutation floor ${MUT_FLOOR} is above the newest cycle ${NEWEST_CYCLE} — TAIL:mutation was charged to nobody." >&2
  fail=1
fi
if [[ -n "$NEWEST_CYCLE" && "$((10#$ABSENCE_FLOOR))" -gt "$((10#$NEWEST_CYCLE))" ]]; then
  echo "✗ declared-absence floor ${ABSENCE_FLOOR} is above the newest cycle ${NEWEST_CYCLE} — 'pendente' would pass as evidence everywhere." >&2
  fail=1
fi
if [[ $fail -ne 0 ]]; then
  echo "✗ the method did not survive into the artifacts of at least one cycle."
  exit 1
fi
echo "✓ every cycle checked declares its artifacts and carries the closing tail with evidence."
