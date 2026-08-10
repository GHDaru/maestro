#!/usr/bin/env bash
# install-maestro.sh — installs Maestro (agents + skills + scripts + templates) into
# another repository, so the AI follows the method there.
#
# Usage (from inside the Maestro repository):
#   scripts/install-maestro.sh /path/to/project           # installs
#   scripts/install-maestro.sh /path/to/project --dry-run # shows what it would do
#   scripts/install-maestro.sh --block                    # prints the CLAUDE.md block
#
# It does NOT overwrite existing files without --force (reversibility, Principle III).
set -euo pipefail

TARGET="${1:-}"
MODE="${2:-}"
SOURCE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# The instruction block is GENERATED from the skills that exist on disk — a hand-written
# list ages silently (that was the failure mode of Maestro's own repository, cycle 021).
method_block() {
  echo '## Method: Maestro'
  echo '- Read `docs/governance/principles.md` (the constitution) and'
  echo '  `docs/governance/operating-model.md` before any work.'
  echo '- **Skills first**: before acting, check whether one of the skills below applies; if'
  echo '  there is a reasonable chance, follow it (each carries its Iron Law):'
  for d in "$SOURCE"/skills/*/; do
    name="$(basename "$d")"
    # first sentence of the description, without cutting a word in half
    desc="$(sed -n 's/^description: *//p' "$d/SKILL.md" 2>/dev/null | head -1 | sed 's/\([.:] \).*/\1/' | sed 's/ *$//')"
    echo "  - \`$name\`${desc:+ — $desc}"
  done
  echo '- Flow: `spec → plan (Constitution Check) → tasks → implement → DoD → review in'
  echo '  fresh context → human gate → merge`.'
  echo '- Lanes: light (the pull request is the artifact) · full (complete spec) · infra (full +'
  echo '  reversibility).'
  echo '- Every cycle declares its conditional artifacts and carries the closing tail'
  echo '  (`TAIL:review`, `TAIL:security`, `TAIL:gate`) in `tasks.md`, with the evidence in'
  echo '  `qa-report.md`. Catalogue: `docs/governance/artifacts.md`.'
  echo '- **Asked "are you following the method?" — do NOT answer from memory.** Run'
  echo '  `scripts/check-conformance.sh <NNN>` and read it: memory reports intention, not fact.'
}

# --block: prints only the instruction for the AI (redirect it into the project CLAUDE.md)
if [[ "$TARGET" == "--block" || "$MODE" == "--block" ]]; then method_block; exit 0; fi

[[ -n "$TARGET" ]] || { echo "usage: scripts/install-maestro.sh <target> [--dry-run|--force|--block]" >&2; exit 2; }
[[ -d "$TARGET" ]] || { echo "error: target '$TARGET' does not exist." >&2; exit 1; }
DRY=0; FORCE=0
[[ "$MODE" == "--dry-run" ]] && DRY=1
[[ "$MODE" == "--force" ]] && FORCE=1

echo "Maestro: $SOURCE  →  $TARGET"
[[ "$DRY" -eq 1 ]] && echo "(dry-run: nothing will be written)"
echo

copy() {  # $1 = relative path (file or directory)
  local rel="$1" src="$SOURCE/$1" dst="$TARGET/$1"
  [[ -e "$src" ]] || { echo "  ⚠ missing in the source: $rel"; return; }
  if [[ -e "$dst" && "$FORCE" -ne 1 ]]; then
    echo "  = exists (kept): $rel"
    return
  fi
  if [[ "$DRY" -eq 1 ]]; then
    echo "  + would copy: $rel"
  else
    mkdir -p "$(dirname "$dst")"
    cp -r "$src" "$dst"
    echo "  + installed: $rel"
  fi
}

# The MIT obligation travels with the copy. Renamed on purpose: dropping a bare LICENSE in
# someone else's repository root would assert that THEIR whole project is MIT-Maestro, which
# is false. These two files describe only the Maestro material installed here.
copy_as() {  # $1 = source, $2 = destination path inside the target
  local src="$SOURCE/$1" dst="$TARGET/$2"
  [[ -e "$src" ]] || { echo "  ⚠ missing in the source: $1"; return; }
  if [[ -e "$dst" && "$FORCE" -ne 1 ]]; then echo "  = exists (kept): $2"; return; fi
  if [[ "$DRY" -eq 1 ]]; then
    echo "  + would copy: $1 -> $2"
  else
    mkdir -p "$(dirname "$dst")"; cp "$src" "$dst"; echo "  + installed: $2"
  fi
}

echo "── Licence and attribution (travels with the copy) ──"
copy_as "LICENSE" "docs/governance/MAESTRO-LICENSE"
copy_as "THIRD-PARTY-NOTICES.md" "docs/governance/MAESTRO-THIRD-PARTY-NOTICES.md"

echo "── Agents (who does what) ──"
copy ".claude/agents"

echo "── Skills (how to do it) ──"
copy "skills"

echo "── Scripts (the ritual) ──"
for s in new-cycle.sh promote-main.sh retro.sh record-decision.sh check-agents.sh check-roles.sh check-install.sh check-evals.sh check-conformance.sh; do
  copy "scripts/$s"
done
copy "scripts/README.md"

echo "── Evaluations (the baseline for judgement) ──"
# Only the anatomy travels. The cases stay behind: each one names a target file in the
# repository that owns it, so an imported case would arrive stale (corollary C11).
copy "evals/README.md"

echo "── Commands and templates (the spec-driven engine) ──"
copy ".claude/commands"
copy ".specify/templates"
copy ".specify/UPSTREAM.md"

echo "── Governance (the source of truth) ──"
copy "docs/governance/principles.md"
copy "docs/governance/operating-model.md"
copy "docs/governance/glossary.md"
copy "docs/governance/axioms.md"
copy "docs/governance/artifacts.md"
copy "docs/records/README.md"

if [[ "$DRY" -eq 0 ]]; then
  chmod +x "$TARGET"/scripts/*.sh 2>/dev/null || true
  # the decision index starts empty in a new project (history belongs to each project)
  [[ -f "$TARGET/docs/records/decisoes.jsonl" ]] || { mkdir -p "$TARGET/docs/records"; : > "$TARGET/docs/records/decisoes.jsonl"; }
fi

echo
echo "── Next steps (in the target project) ──"
echo "  1. Add the block below to the project CLAUDE.md (or AGENTS.md)"
echo "     (to paste it directly:  scripts/install-maestro.sh --block >> CLAUDE.md):"
echo
method_block | sed 's/^/     /'
cat <<'FIM'

     (tip: keep ONE source — `ln -s CLAUDE.md AGENTS.md` — so the two instructions
     cannot diverge.)

  2. Prove it is installed:  scripts/check-install.sh
     (it fails while CLAUDE.md/AGENTS.md does not point at the method: copying files is
     not installing — installed is when the AI knows it must follow them.)
  3. Open the first cycle:   scripts/new-cycle.sh 001 <slug>
  4. When promoting:         scripts/promote-main.sh
  5. In the retrospective:   scripts/retro.sh
  6. "Am I following it?":   scripts/check-conformance.sh

FIM
echo "done."
