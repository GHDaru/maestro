#!/usr/bin/env bash
# check-links.sh — every relative link in the repository points at a file that exists.
#
# Cycle 033 renamed 20+ files with a text substitution and broke references in two places.
# What caught it was the site build — which only validates the PUBLISHED pages. A broken
# link inside specs/, inside an ADR or inside a skill passed silently.
#
# This is the whole-family version of that gate (anti-pattern 16): every Markdown file in the
# repository, every relative link, including images.
set -euo pipefail

ROOTS=("docs" "specs" "skills" "scripts" ".claude" ".specify" "README.md" "CLAUDE.md" "CHANGELOG.md")
broken=0
checked=0

while IFS= read -r file; do
  dir="$(dirname "$file")"
  # markdown links and images: [...](target) and ![...](target)
  while IFS= read -r target; do
    [[ -n "$target" ]] || continue
    case "$target" in
      http*|mailto:*|"#"*|"//"*) continue ;;
    esac
    clean="${target%%#*}"          # drop the anchor
    [[ -n "$clean" ]] || continue
    checked=$((checked + 1))
    if [[ ! -e "$dir/$clean" && ! -e "$clean" ]]; then
      echo "  ✗ $file → $target" >&2
      broken=$((broken + 1))
    fi
    # inline code spans are stripped first: `![...](...)` inside backticks is an EXAMPLE in
    # prose, not a link — counting it would be measuring the text, not the fact.
  done < <(sed 's/`[^`]*`//g' "$file" 2>/dev/null | grep -oE '\]\([^)]+\)' | sed 's/^](//; s/)$//' | sed 's/ .*//')
done < <(find "${ROOTS[@]}" -name '*.md' -type f 2>/dev/null | grep -v '/site/')

echo "── Relative links across the repository ──"
echo "  checked: $checked"
if [[ "$broken" -ne 0 ]]; then
  echo "✗ $broken broken relative link(s)." >&2
  exit 1
fi
echo "✓ every relative link resolves."
