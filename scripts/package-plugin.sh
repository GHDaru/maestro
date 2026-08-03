#!/usr/bin/env bash
# package-plugin.sh — builds the Claude Code plugin from the canonical sources.
#
# Claude Code expects `agents/`, `commands/` and `skills/` at the ROOT of the plugin; our
# canonical sources live in `.claude/agents`, `.claude/commands` and `skills/` (where the
# repository uses them for itself and where the `npx skills add` standard looks for them).
# This script reconciles both layouts — and `--verify` proves they are in sync.
#
# Usage:  scripts/package-plugin.sh           # (re)builds plugin/maestro/
#         scripts/package-plugin.sh --verify  # fails if the package is stale
set -euo pipefail

TARGET="plugin/maestro"
MODE="${1:-}"

build() {  # $1 = output directory
  local out="$1"
  rm -rf "$out"
  mkdir -p "$out/.claude-plugin"
  cp -r .claude/agents "$out/agents"
  cp -r .claude/commands "$out/commands"
  cp -r skills "$out/skills"
  rm -f "$out/skills/README.md"   # the catalogue index is not a skill
  local version
  version=$(grep -m1 -E '^> \*\*Version\*\*|Version\*\*:' docs/governance/principles.md 2>/dev/null | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+' | head -1)
  cat > "$out/.claude-plugin/plugin.json" <<JSON
{
  "name": "maestro",
  "description": "The method of one human conducting many AI agents: the spec as the source of truth, gates proportional to risk, and reversibility that buys speed. Ships the spec-driven subagents, the skills with their Iron Laws and the cycle commands.",
  "version": "${version:-1.0.0}",
  "author": { "name": "GHDaru" },
  "homepage": "https://ghdaru.github.io/maestro/",
  "repository": "https://github.com/GHDaru/maestro",
  "license": "MIT"
}
JSON
  cp README.md "$out/README.md" 2>/dev/null || true
}

if [[ "$MODE" == "--verify" || "$MODE" == "--verificar" ]]; then
  TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
  build "$TMP/maestro"
  if [[ ! -d "$TARGET" ]]; then
    echo "✗ package missing — run: scripts/package-plugin.sh" >&2
    exit 1
  fi
  if ! diff -rq "$TMP/maestro" "$TARGET" >/dev/null 2>&1; then
    echo "✗ plugin out of date with the sources. Differences:" >&2
    diff -rq "$TMP/maestro" "$TARGET" 2>&1 | sed 's/^/   /' >&2
    echo "   → run: scripts/package-plugin.sh" >&2
    exit 1
  fi
  echo "✓ plugin in sync with the sources ($(find "$TARGET" -name '*.md' | wc -l | tr -d ' ') files)."
  exit 0
fi

build "$TARGET"
echo "✓ plugin built in $TARGET/"
echo "   agents: $(find "$TARGET/agents" -name '*.md' | wc -l | tr -d ' ') · skills: $(find "$TARGET/skills" -name 'SKILL.md' | wc -l | tr -d ' ') · commands: $(find "$TARGET/commands" -name '*.md' | wc -l | tr -d ' ')"
echo "   local test:  claude --plugin-dir ./$TARGET"
