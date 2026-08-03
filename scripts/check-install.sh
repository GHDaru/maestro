#!/usr/bin/env bash
# check-install.sh — is the method installed in THIS repository, and does the
# instruction the AI reads still match what is on disk?
#
# Installing is copying files; *being installed* is the AI knowing it must follow them.
# This fitness function checks both halves — and the coherence between them, which is
# the part that rots silently (a new skill on disk and absent from CLAUDE.md is an
# invisible skill).
#
# Usage:  scripts/check-install.sh [directory]   (default: current directory)
set -euo pipefail

ROOT="${1:-.}"
cd "$ROOT"
fail=0
alert() { echo "  ✗ $1" >&2; fail=$((fail + 1)); }

echo "── Method layers (what was copied) ──"
for pair in ".claude/agents:subagents" \
            "skills:skills" \
            "scripts/new-cycle.sh:cycle script" \
            "scripts/promote-main.sh:promotion script" \
            ".specify/templates:spec-driven templates" \
            "docs/governance/principles.md:constitution" \
            "docs/governance/operating-model.md:operating model"; do
  target="${pair%%:*}"; name="${pair##*:}"
  if [[ -e "$target" ]]; then echo "  ok: $name ($target)"; else alert "$name missing: $target"; fi
done

# The instruction the AI reads. Either file is enough, but whichever exists must point
# at the method — a present, silent file is worse than a missing one: it looks installed.
echo ""
echo "── Instruction for the AI (what makes the AI follow it) ──"
INSTRUCTIONS=()
for f in CLAUDE.md AGENTS.md; do [[ -f "$f" ]] && INSTRUCTIONS+=("$f"); done
if [[ ${#INSTRUCTIONS[@]} -eq 0 ]]; then
  alert "neither CLAUDE.md nor AGENTS.md — the AI has no way to learn about the method"
else
  for f in "${INSTRUCTIONS[@]}"; do
    grep -q "principles" "$f"          || alert "$f does not point to docs/governance/principles.md"
    grep -qi "skills" "$f"             || alert "$f does not require checking the skills before acting"
    grep -qi "spec.*plan.*tasks" "$f"  || alert "$f does not describe the spec → plan → tasks → … flow"
    grep -qiE "lane|raia" "$f"         || alert "$f does not mention the lanes (light/full/infra)"
    echo "  checked: $f"
  done
fi

# Coherence: if the document enumerates skills, it must enumerate ALL of them. A partial
# list is the real failure mode — the new skill lands on disk and vanishes from the
# instruction (cycle 021).
echo ""
echo "── Coherence: skills on disk × skills cited ──"
if [[ -d skills ]]; then
  for d in skills/*/; do
    name="$(basename "$d")"
    [[ -f "$d/SKILL.md" ]] || { alert "skills/$name has no SKILL.md"; continue; }
    cited=0
    for f in "${INSTRUCTIONS[@]:-}"; do
      [[ -n "$f" && -f "$f" ]] && grep -q "$name" "$f" && cited=1
    done
    if [[ "$cited" -eq 1 ]]; then echo "  ok: $name"; else alert "skill '$name' exists but is not cited in CLAUDE.md/AGENTS.md"; fi
  done
fi

echo ""
if [[ "$fail" -ne 0 ]]; then
  echo "✗ $fail problem(s): the method is on disk, but it is not actually installed." >&2
  exit 1
fi
echo "✓ method installed and coherent: layers present, AI instructed, every skill visible."
