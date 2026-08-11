#!/usr/bin/env bash
# check-adr.sh — the decision index tells the truth about the decisions.
#
# Why it exists: in cycle 046 the index at docs/adr/README.md was found FROZEN since 0017.
# Two ADRs (0018 and 0019) had been written and never listed, and 0017 was still shown as
# "Aceito" seven cycles after 0018 superseded it. Anyone reading the index — a human or an
# agent — would have taken a reversed decision as current. It was fixed by hand and recorded
# as an open finding precisely because NOTHING measured it: the same defect could return the
# next time someone wrote an ADR in a hurry.
#
# This is the same shape as check-roles.sh (profile index × agents on disk): a hand-written
# index of machine-readable files ages in silence. Anti-pattern 15.
#
# What this actually measures (anti-pattern 13): NOT whether a decision is wise, and NOT
# whether the prose is good. It measures three facts: every ADR is listed, every listing
# points at a real file, and the status in the index agrees with the status in the ADR.
#
# Usage:  scripts/check-adr.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

DIR="docs/adr"
INDEX="$DIR/README.md"

fail=0
ok()  { printf '  ✓ %s\n' "$1"; }
bad() { printf '  ✗ %s\n' "$1"; fail=1; }

echo "── Decision index × ADRs on disk ──"

# A project that installed the method may not have written an ADR yet: absent is legitimate
# THERE, and said out loud, never in silence. Not HERE, though — a repository that declares
# docs/adr/ in boundary.json owns one, and its deletion is a defect, not a fresh start.
# Same guard, same words as check-ecosystem.sh and check-roles.sh (cycles 047 and 048).
if [[ ! -d "$DIR" ]]; then
  if [[ -f boundary.json ]] && grep -qF '"docs/adr/"' boundary.json; then
    bad "$DIR/ is declared in boundary.json and does not exist — this repository owns a decision record"
    echo "──"; echo "✗ the decision record is not readable."; exit 1
  fi
  echo "  · no $DIR/ in this repository — no architectural decision recorded yet."
  echo "    (the method records them as ADRs: context → decision → consequences, immutable)"
  exit 0
fi
# From here the record exists, so a missing index IS a finding (anti-pattern 16, cycle 046).
if [[ ! -f "$INDEX" ]]; then
  # With a recipe, like check-ecosystem.sh gives. Failing with no way forward is how a gate
  # teaches people to work around it — found by the review of this cycle, in the exact
  # moment a fresh installation writes its FIRST ADR.
  bad "$INDEX is missing — the index IS the entry point to the decisions"
  echo "    (to create it: cp .specify/templates/adr-index-template.md $INDEX — it carries the" >&2
  echo "     table shape and the status vocabulary this gate reads)" >&2
fi
[[ $fail -eq 0 ]] || { echo "──"; echo "✗ the decision record is not readable."; exit 1; }

shopt -s nullglob
adrs=("$DIR"/[0-9][0-9][0-9][0-9]-*.md)
strays=("$DIR"/*.md "$DIR"/*.markdown)
shopt -u nullglob
if [[ ${#adrs[@]} -eq 0 ]]; then
  bad "no ADR in $DIR/ — an empty record is not a clean one"
  echo "──"; echo "✗ nothing to check."; exit 1
fi

# A file that is an ADR in spirit and not in name is invisible to the glob above, so it is
# invisible to every check here. Naming is the contract that makes the record checkable.
for f in "${strays[@]}"; do
  b="$(basename "$f")"
  [[ "$b" == "README.md" ]] && continue
  [[ "$b" =~ ^[0-9]{4}-.+\.md$ ]] && continue
  bad "${b} is in $DIR/ and is not named NNNN-slug.md — it would be invisible to this gate"
done

# ---- the status vocabulary ------------------------------------------------------
# The first version compared only the word "superseded", and claimed in its green line to
# check "every status". A synonym any Portuguese writer would reach for — Substituído,
# Revogado, Obsoleto — switched the whole invariant off, and an index reading `Rejeitado`
# against an ADR reading `Aceito` passed. That is the gate measuring the phrase instead of
# the fact (anti-pattern 13). Both sides are now mapped to a state, and the states compared.
state_of() {  # $1 = free text (index cell or ADR status line) -> a state, or "" if unknown
  local t; t="$(tr '[:upper:]' '[:lower:]' <<<"$1")"
  # A legitimate status links to the ADR that superseded it — "[ADR 0018](0018-….md)" — and
  # brackets are how markdown writes a link, not only how a template writes a hole. Strip
  # links first, or ADR 0017 (the very row this cycle exists to protect) reads as unfilled.
  t="$(sed -E 's/\[([^]]*)\]\([^)]*\)/\1/g' <<<"$t")"
  # An UNFILLED template still carries the whole menu on one line — "Proposed | Accepted |
  # Superseded by ADR NNNN" — and matching the first synonym in it would report the ADR as
  # superseded, which is both wrong and baffling to whoever just wrote it. A menu is not a
  # status: it is an ADR nobody finished.
  case "$t" in *'|'*|*'['*|*'<'*) echo "unfilled"; return ;; esac
  case "$t" in                                                          # PT-DATA
    *superad*|*superseded*|*substitu*|*revogad*|*obsolet*|*replaced*) echo superseded ;;
    *aceit*|*accepted*)                                                echo accepted ;;
    *propost*|*proposed*|*rascunho*|*draft*)                           echo proposed ;;
    *rejeit*|*rejected*|*recusad*)                                     echo rejected ;;
    *)                                                                 echo "" ;;
  esac
}

# The status an ADR declares about ITSELF. Found by grep, never by line number: ADRs 0005 and
# 0008 carry a migration note above the header, and a fixed line would read the note.
adr_status() {  # $1 = file
  grep -m1 -E '^- \*\*Status\*\*:' "$1" | sed 's/^- \*\*Status\*\*:[[:space:]]*//' || true
}

# A cell of a markdown table row, trimmed and stripped of emphasis.
cell() {  # $1 = row, $2 = index (1-based, after the leading pipe)
  awk -F'|' -v i="$(( $2 + 1 ))" '{print $i}' <<<"$1" | sed 's/[*`]//g; s/^ *//; s/ *$//'
}

# ---- the index rows, and ONLY the rows -----------------------------------------
# The first version grepped the whole file for "(filename)". A commented-out row, a
# struck-through row, or a mention in prose all satisfied it — so an ADR could vanish from
# the rendered table and still count as listed. That is the cycle-046 defect surviving its
# own gate. A row is now a table line whose FIRST cell is the ADR number.
rows="$(grep -E '^\|' "$INDEX" | grep -vE '^\|[[:space:]]*:?-{2,}' || true)"

n=0
for f in "${adrs[@]}"; do
  n=$((n + 1))
  base="$(basename "$f")"
  num="${base%%-*}"

  mine="$(awk -F'|' -v n="$num" '
    { c=$2; gsub(/[*` ]/,"",c); if (c+0 == n+0 && c ~ /^[0-9]+$/) print }' <<<"$rows" || true)"
  count="$(grep -c . <<<"$mine" || true)"
  [[ -n "$mine" ]] || count=0

  if [[ "$count" -eq 0 ]]; then
    bad "ADR ${num} is on disk and has no row in the index — an unlisted decision is one nobody finds"
    continue
  fi
  if [[ "$count" -gt 1 ]]; then
    # Two rows for one ADR is worse than none: one of them is wrong and nothing says which.
    bad "ADR ${num} has ${count} rows in the index — one of them is wrong, and the reader cannot tell which"
    continue
  fi

  # the row must LINK to this ADR's own file (a bare number in the cell is not a reference)
  if ! grep -qE "\((\./)?${base}(#[A-Za-z0-9._-]+)?\)" <<<"$mine"; then
    bad "ADR ${num} has a row that does not link to ${base} — the index names it without pointing at it"
    continue
  fi

  own="$(adr_status "$f")"
  if [[ -z "$own" ]]; then
    bad "${base} declares no '- **Status**:' line — the index has nothing to agree with"
    continue
  fi
  own_state="$(state_of "$own")"
  idx_state="$(state_of "$(cell "$mine" 3)")"
  if [[ "$own_state" == "unfilled" ]]; then
    bad "${base} still carries the template's list of options as its status — pick one (accepted · proposed · rejected · superseded)"
  elif [[ "$idx_state" == "unfilled" ]]; then
    bad "the index row for ADR ${num} still carries a placeholder status — pick one"
  elif [[ -z "$own_state" ]]; then
    bad "${base} declares status '${own}', outside the vocabulary (accepted · proposed · rejected · superseded)"
  elif [[ -z "$idx_state" ]]; then
    bad "the index shows ADR ${num} as '$(cell "$mine" 3)', outside the vocabulary (accepted · proposed · rejected · superseded)"
  elif [[ "$own_state" != "$idx_state" ]]; then
    bad "ADR ${num}: the index says '${idx_state}' and the ADR says '${own_state}' — a reversed or undecided decision reading as current is the worst row in the table"
  fi
done

# ---- every row is backed by a file ---------------------------------------------
while IFS= read -r row; do
  [[ -n "$row" ]] || continue
  rnum="$(cell "$row" 1)"
  [[ "$rnum" =~ ^[0-9]{1,4}$ ]] || continue
  target="$(grep -oE '\((\./)?[0-9]{4}-[A-Za-z0-9._-]+\.md(#[A-Za-z0-9._-]+)?\)' <<<"$row" \
            | head -1 | tr -d '()' | sed 's|^\./||; s|#.*||' || true)"
  if [[ -z "$target" ]]; then
    bad "the index has a row for ADR ${rnum} with no link to a file — a decision announced and unreachable"
  elif [[ ! -f "$DIR/$target" ]]; then
    bad "the index links to '${target}', which does not exist in $DIR/"
  fi
done <<<"$rows"

echo "──"
if [[ $fail -ne 0 ]]; then
  echo "✗ the decision index does not match the decisions."
  exit 1
fi
echo "✓ ${n} ADR(s): one row each, every row linked to a real file, and the status in the"
echo "  index agreeing with the status the ADR declares about itself."
