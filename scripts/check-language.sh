#!/usr/bin/env bash
# check-language.sh — the installable method is written in English (ADR 0014).
#
# What this actually measures: **Portuguese residue** in the installable surface. That is
# the real failure mode — a file half translated, or a new file written in the language of
# whoever was typing. It does not "detect English"; it detects the leftovers, which is what
# a translation misses (anti-pattern 13: know what your check measures).
#
# Out of scope, on purpose: the book (docs/handbook, docs/receitas, docs/livro,
# docs/diagramas, docs/research, docs/jornada), the cycle records under specs/, and the
# append-only decision index — the book is written in Portuguese by decision, and the index
# keeps its original field names because its lines are immutable.
#
# A line that legitimately CARRIES Portuguese (a pattern matched against the Portuguese book,
# a label of a Portuguese artifact) declares it with the marker `PT-DATA` in the same line.
# The exemption is visible where it applies — never a silent allowlist elsewhere.
set -euo pipefail

# Installable surface: what scripts/install-maestro.sh copies into another repository.
TARGETS=(
  ".claude/agents"
  ".claude/commands/dod.md"
  ".claude/commands/eval.md"
  "skills"
  "scripts"
  "evals"
  "docs/governance"
  "docs/records/README.md"
  ".specify/templates/spec-template.md"
  ".specify/templates/plan-template.md"
  ".specify/templates/tasks-template.md"
  ".specify/templates/qa-report-template.md"
  ".specify/templates/adr-template.md"
  ".specify/templates/ux-design-template.md"
  ".specify/templates/journey-template.md"
  ".specify/templates/evaluation-template.md"
  # Added to the installable surface in cycle 048 (the /speckit.* commands call them).
  ".specify/scripts"
  # Became installable surface in cycle 046: both travel with every copy and are packaged
  # into the plugin. They were English already — the gap was that nothing kept them so.
  "LICENSE"
  "THIRD-PARTY-NOTICES.md"
)

# High-frequency Portuguese tokens that practically never appear in English prose.
PATTERN='\b(não|são|está|estão|também|então|porque|você|nós|isso|esta|este|essa|esse|pelo|pela|dos|das|uma|uns|para o|para a|com o|com a|que o|que a|ção|ções|ário|ência)\b'  # PT-DATA (the pattern itself)

fail=0
echo "── Portuguese residue in the installable surface ──"
for t in "${TARGETS[@]}"; do
  [[ -e "$t" ]] || { echo "  ⚠ missing: $t" >&2; continue; }
  hits=$(grep -rIniE "$PATTERN" "$t" 2>/dev/null | grep -v "decisoes.jsonl" | grep -v "PT-DATA" || true)
  if [[ -n "$hits" ]]; then
    echo "  ✗ $t" >&2
    echo "$hits" | head -5 | sed 's/^/      /' >&2
    n=$(echo "$hits" | wc -l | tr -d ' ')
    [[ "$n" -gt 5 ]] && echo "      … and $((n - 5)) more line(s)" >&2
    fail=$((fail + 1))
  else
    echo "  ok: $t"
  fi
done

echo ""
if [[ "$fail" -ne 0 ]]; then
  echo "✗ $fail installable path(s) with Portuguese residue — the method installs in English (ADR 0014)." >&2
  exit 1
fi
echo "✓ the installable surface is in English; the book stays in Portuguese, by decision."
