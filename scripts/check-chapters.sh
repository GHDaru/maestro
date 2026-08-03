#!/usr/bin/env bash
# check-chapters.sh — turns the editorial Iron Law into an executable.
#
#   NO CHAPTER SHIPS WITHOUT OBJECTIVES, A REAL EXAMPLE AND VERIFICATION
#
# Chapter 01 was migrated in cycle 016 and its nine sections were counted BY HAND in the
# qa report. Counting by hand works once; there were eleven chapters left. This script
# enforces the skeleton on every chapter already migrated and lists the ones still
# pending — so the pending number is a fact, not a memory.
#
# The book itself is written in Portuguese (see ADR 0014); the section names below are
# the ones the editorial guide defines.
set -euo pipefail

DIR="${1:-docs/handbook}"
fail=0
migrated=0; pending=()

# the nine sections of the editorial guide (docs/livro/guia-editorial.md §2), in order.
# The section names are Portuguese because the book is Portuguese — PT-DATA by design.
SECTIONS=("Objetivos" "O problema" "A ideia central" "A regra vigente" "Fundamentos" \
          "Na prática" "Erros e anti-padrões" "Verificação" "O que roubar")  # PT-DATA

for f in "$DIR"/[0-9][0-9]-*.md; do
  [[ -e "$f" ]] || continue
  name="$(basename "$f")"
  # "migrated" means it HAS the v2 structure, not that it contains the words "migrated to
  # v2": with a textual marker, deleting the header line silently removed the chapter from
  # the check (found while proving this script failing — anti-pattern 13).
  if ! grep -q '^## 1\. Objetivos' "$f"; then pending+=("$name"); continue; fi
  migrated=$((migrated + 1))

  # mandatory dating (guide §4): captured + last revision + cycle
  grep -qE '^> \*\*Capturado em\*\* [0-9]{4}-[0-9]{2} · última revisão [0-9]{4}-[0-9]{2}-[0-9]{2} · ciclo [0-9]{3}' "$f" \
    || { echo "  ✗ $name: dating header out of pattern (captured · revision · cycle)" >&2; fail=$((fail + 1)); }

  # the nine sections, in order
  read_order="$(grep -oE '^## [0-9]+\. .*' "$f" | sed 's/^## [0-9]*\. //; s/⭐ //; s/ —.*//')"
  i=0
  while IFS= read -r title; do
    expected="${SECTIONS[$i]:-}"
    [[ "$title" == "$expected"* ]] || { echo "  ✗ $name: section $((i+1)) is '$title', expected '$expected'" >&2; fail=$((fail + 1)); }
    i=$((i + 1))
  done <<< "$read_order"
  [[ "$i" -eq 9 ]] || { echo "  ✗ $name: $i numbered sections (the skeleton has 9)" >&2; fail=$((fail + 1)); }

  # the real example is our trademark: section 6 marked and carrying cycle evidence
  grep -q '^## 6\. ⭐ Na prática' "$f" || { echo "  ✗ $name: missing section 6 marked '⭐ Na prática'" >&2; fail=$((fail + 1)); }
  grep -qE 'ciclo [0-9]{3}|spec [0-9]{3}|gate-main|\$ ' "$f" \
    || { echo "  ✗ $name: 'Na prática' section without real evidence (cycle, spec, gate or command output)" >&2; fail=$((fail + 1)); }

  [[ "$fail" -eq 0 ]] && echo "  ok: $name"
done

# A rule born in a skill must reach the chapter that teaches it. The second law of
# verifiable-dod lived ten cycles inside the skill and never entered the book (cycle 029).
# The check compares the last change of each SKILL.md with the "última revisão" date of the
# chapters that cite it — if the skill moved after the chapter, the chapter is behind.
echo ""
echo "── Skill freshness × chapter that teaches it ──"
for d in skills/*/; do
  skill="$(basename "$d")"
  skill_date=$(git log -1 --format=%ad --date=short -- "$d/SKILL.md" 2>/dev/null || true)
  [[ -n "$skill_date" ]] || continue
  for f in "$DIR"/[0-9][0-9]-*.md; do
    grep -q "$skill" "$f" 2>/dev/null || continue
    chapter_date=$(grep -oE 'última revisão [0-9]{4}-[0-9]{2}-[0-9]{2}' "$f" | head -1 | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' || true)
    [[ -n "$chapter_date" ]] || continue
    if [[ "$skill_date" > "$chapter_date" ]]; then
      echo "  ✗ skill '$skill' changed on $skill_date; $(basename "$f") was revised on $chapter_date — the chapter is behind" >&2
      fail=$((fail + 1))
    else
      echo "  ok: $skill ($skill_date) ≤ $(basename "$f") ($chapter_date)"
    fi
  done
done

echo ""
echo "migrated to v2: $migrated · pending: ${#pending[@]} (${pending[*]:-none})"
if [[ "$fail" -ne 0 ]]; then
  echo "✗ $fail violation(s) of the editorial Iron Law." >&2
  exit 1
fi
echo "✓ every migrated chapter follows the nine-section skeleton, dated and with a real example."
