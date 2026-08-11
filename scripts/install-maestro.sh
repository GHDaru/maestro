#!/usr/bin/env bash
# install-maestro.sh — installs Maestro (agents + skills + scripts + templates) into
# another repository, so the AI follows the method there.
#
# Usage (from inside the Maestro repository):
#   scripts/install-maestro.sh /path/to/project           # installs
#   scripts/install-maestro.sh /path/to/project --dry-run # shows what it would do
#   scripts/install-maestro.sh --block                    # prints the CLAUDE.md block
#
# Installing is also UPGRADING. A file we wrote and you never touched is refreshed; a file
# you modified is kept, with the new version beside it as *.maestro-new; a file the method
# no longer ships is removed only while it is still untouched. Nothing you wrote is ever
# overwritten without --force, and --force saves your version as *.maestro-old first.
set -euo pipefail

TARGET=""
SOURCE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

ARG_DRY=0; ARG_FORCE=0; ARG_BLOCK=0
for a in "$@"; do
  case "$a" in
    --dry-run) ARG_DRY=1 ;;
    --force)   ARG_FORCE=1 ;;
    --block)   ARG_BLOCK=1 ;;
    -*)        echo "error: unknown flag '$a'" >&2; exit 2 ;;
    *)         [[ -z "$TARGET" ]] && TARGET="$a" || { echo "error: more than one target given" >&2; exit 2; } ;;
  esac
done

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
if [[ "$ARG_BLOCK" -eq 1 ]]; then method_block; exit 0; fi

[[ -n "$TARGET" ]] || { echo "usage: scripts/install-maestro.sh <target> [--dry-run|--force|--block]" >&2; exit 2; }
[[ -d "$TARGET" ]] || { echo "error: target '$TARGET' does not exist." >&2; exit 1; }
# Every flag, in any order and any combination. The first version read only $2, so
# `--force --dry-run` silently became FORCE=1 DRY=0 — the destructive flag winning while the
# brake was ignored, in the one script that deletes files in someone else's repository.
DRY="$ARG_DRY"; FORCE="$ARG_FORCE"

echo "Maestro: $SOURCE  →  $TARGET"
[[ "$DRY" -eq 1 ]] && echo "(dry-run: nothing will be written)"
echo

# ---------------------------------------------------------------------------------
# INSTALLING IS ALSO UPGRADING.
#
# The first version skipped any destination that already existed. A directory always exists
# after the first install, so re-running the installer delivered NOTHING — and `--force`,
# the documented way out, ran `cp -r src dst` onto an existing directory and NESTED it
# (.claude/agents/agents). Whoever installed v0.1.0 kept the /speckit.constitution that told
# an agent to overwrite the constitution, and the escape hatch broke the layout.
#
# The fix is not a flag, it is a fact: a manifest of what WE wrote, with a hash per file.
# With it, three states become distinguishable, and only the middle one is ours to change:
#
#   the file is ours and unchanged since we wrote it  -> ours to update
#   the file was modified by the project              -> theirs; keep it, offer the new one
#   the file is gone from the method                  -> remove it, if still unchanged
#
# Without the manifest, "differs from the source" cannot tell an OLD version from an EDITED
# one, and an installer that guesses that wrong either delivers nothing or destroys work.
# Paths the method shipped once and ships no more. The prune loop removes them when the
# manifest proves they are untouched; on an installation older than the manifest there is no
# such proof, so they are NAMED to the human instead (never deleted on a guess).
RETIRED=(".specify/memory/constitution.md")

MANIFEST_REL=".maestro/manifest.tsv"
MANIFEST="$TARGET/$MANIFEST_REL"
declare -A PREV=()      # relative path -> hash recorded at the previous install
declare -A NOW=()       # relative path -> hash written by this run
FIRST_UPGRADE=0
if [[ -f "$MANIFEST" ]]; then
  # The manifest lives INSIDE someone else's repository and is committable: one line in a
  # pull request is enough. It is data, never a command — so every path is validated before
  # it can reach `rm`. A `../` entry deleted a file outside the target in the review of this
  # cycle. Also tolerant of CRLF and of a missing final newline, which used to drop lines.
  while IFS= read -r line || [[ -n "$line" ]]; do
    line="${line%$'\r'}"
    [[ -n "$line" ]] || continue
    h="${line%%$'\t'*}"; rel="${line#*$'\t'}"
    [[ -n "$rel" && "$rel" != "$line" ]] || continue
    case "$rel" in /*|*..*) echo "  ⚠ manifest entry ignored (escapes the target): $rel" >&2; continue ;; esac
    PREV["$rel"]="$h"
  done < "$MANIFEST"
elif [[ -f "$TARGET/docs/governance/operating-model.md" && -f "$TARGET/skills/verifiable-dod/SKILL.md" ]]; then
  # Method files are here and no manifest is: this is an installation from BEFORE the
  # manifest existed (v0.2.0 and earlier). There is no honest way to tell an old file from an
  # edited one, so nothing is overwritten — everything different arrives as *.maestro-new and
  # the human decides. Said out loud, because silence here would look like "nothing to do".
  FIRST_UPGRADE=1
fi

hash_of() { sha256sum "$1" 2>/dev/null | cut -d' ' -f1; }

n_new=0; n_upd=0; n_same=0; n_kept=0; n_gone=0

# The manifest must record what WE wrote — nothing else. The first version stamped every
# path it looked at, so a file the project already had, byte-identical to ours (a project
# that ran `specify init` on its own has exactly that), was adopted as ours without a word
# — and the prune loop later DELETED it. Claiming is now a consequence of writing.
install_file() {  # $1 = source file, $2 = relative destination
  local src="$1" rel="$2" dst="$TARGET/$2" hs hd
  hs="$(hash_of "$src")"
  if [[ ! -e "$dst" ]]; then
    [[ "$DRY" -eq 1 ]] && { echo "  + would install: $rel"; NOW["$rel"]="$hs"; return; }
    mkdir -p "$(dirname "$dst")"; cp "$src" "$dst"; NOW["$rel"]="$hs"
    n_new=$((n_new+1)); echo "  + installed: $rel"; return
  fi
  hd="$(hash_of "$dst")"
  if [[ "$hd" == "$hs" ]]; then
    # Identical — but ours only if we had written it. Otherwise it is the project's file
    # that happens to match, and it is not ours to update or to remove, ever.
    [[ -n "${PREV[$rel]:-}" ]] && NOW["$rel"]="$hs"
    n_same=$((n_same+1)); return
  fi
  if [[ "$FORCE" -eq 1 || "${PREV[$rel]:-}" == "$hd" ]]; then
    # ours, and untouched since we wrote it: this is an OLD version, not someone's work
    [[ "$DRY" -eq 1 ]] && { echo "  ↑ would update: $rel"; NOW["$rel"]="$hs"; return; }
    # --force also lands here for files the project DID modify, so the old content is kept
    # beside the new one: a flag that silently destroys work is not an escape hatch.
    if [[ "$FORCE" -eq 1 && "${PREV[$rel]:-}" != "$hd" ]]; then
      cp "$dst" "${dst}.maestro-old"
      echo "  ! your version saved as ${rel}.maestro-old"
    fi
    cp "$src" "$dst"; NOW["$rel"]="$hs"; n_upd=$((n_upd+1)); echo "  ↑ updated: $rel"; return
  fi
  # modified by the project (or installed before this manifest existed): never clobbered.
  # The manifest keeps the hash WE last wrote — not the source, not the disk — so the file
  # stays known-modified and keeps being offered instead of being silently adopted.
  [[ "$DRY" -eq 1 ]] && { echo "  = would keep (modified): $rel"; }
  if [[ "$DRY" -eq 0 ]]; then
    cp "$src" "${dst}.maestro-new"
    echo "  = kept (you modified it): $rel  → new version beside it as ${rel}.maestro-new"
  fi
  [[ -n "${PREV[$rel]:-}" ]] && NOW["$rel"]="${PREV[$rel]}"
  n_kept=$((n_kept+1))
}

copy() {  # $1 = relative path (file or directory) — walked file by file
  local rel="$1" src="$SOURCE/$1"
  [[ -e "$src" ]] || { echo "  ⚠ missing in the source: $rel"; return; }
  if [[ -f "$src" ]]; then install_file "$src" "$rel"; return; fi
  local f sub
  while IFS= read -r f; do
    sub="${f#$SOURCE/}"
    install_file "$f" "$sub"
  done < <(find "$src" -type f | sort)
}

# The MIT obligation travels with the copy. Renamed on purpose: dropping a bare LICENSE in
# someone else's repository root would assert that THEIR whole project is MIT-Maestro, which
# is false. These two files describe only the Maestro material installed here.
copy_as() {  # $1 = source, $2 = destination path inside the target
  local src="$SOURCE/$1"
  [[ -e "$src" ]] || { echo "  ⚠ missing in the source: $1"; return; }
  install_file "$src" "$2"
}

echo "── Licence and attribution (travels with the copy) ──"
copy_as "LICENSE" "docs/governance/MAESTRO-LICENSE"
copy_as "THIRD-PARTY-NOTICES.md" "docs/governance/MAESTRO-THIRD-PARTY-NOTICES.md"

echo "── Agents (who does what) ──"
copy ".claude/agents"

echo "── Skills (how to do it) ──"
copy "skills"

echo "── Scripts (the ritual) ──"
for s in new-cycle.sh promote-main.sh retro.sh record-decision.sh check-agents.sh check-roles.sh check-install.sh check-evals.sh check-conformance.sh check-ecosystem.sh check-retro.sh check-links.sh check-adr.sh; do
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
# The /speckit.* commands we ship CALL these; shipping the commands without them was the
# defect of cycle 048 — a thing that points at something we do not send. The notices file
# already declared this directory as redistributed, so sending it also makes that true.
copy ".specify/scripts"
copy ".specify/init-options.json"

echo "── Governance (the source of truth) ──"
copy "docs/governance/principles.md"
copy "docs/governance/operating-model.md"
copy "docs/governance/glossary.md"
copy "docs/governance/axioms.md"
copy "docs/governance/artifacts.md"
copy "docs/records/README.md"

# What we shipped once and ship no longer must GO — otherwise the installation accumulates
# the method's own mistakes. `.specify/memory/constitution.md` is the case that named this:
# it was dropped in cycle 048 and would otherwise sit there forever, telling an agent to
# overwrite the constitution. Only removed while still untouched: an edited file is theirs.
for rel in "${!PREV[@]}"; do
  [[ -n "${NOW[$rel]:-}" ]] && continue
  dst="$TARGET/$rel"
  [[ -e "$dst" ]] || continue
  if [[ "$(hash_of "$dst")" == "${PREV[$rel]}" ]]; then
    [[ "$DRY" -eq 1 ]] && { echo "  - would remove (no longer shipped): $rel"; continue; }
    rm -f "$dst"; n_gone=$((n_gone+1)); echo "  - removed (no longer shipped): $rel"
  else
    echo "  = kept (no longer shipped, but you modified it): $rel"
  fi
done

if [[ "$DRY" -eq 0 ]]; then
  # Written whole and moved into place: a `cp` that fails mid-run used to kill the script
  # after writing dozens of files and leave NO manifest, so the next run treated everything
  # we had just written as somebody else's. Truncating in place had the same defect.
  mkdir -p "$(dirname "$MANIFEST")"
  for rel in "${!NOW[@]}"; do printf '%s\t%s\n' "${NOW[$rel]}" "$rel"; done | sort -k2 > "${MANIFEST}.tmp"
  mv "${MANIFEST}.tmp" "$MANIFEST"
fi

if true; then
  echo
  echo "── Summary ──"
  echo "  installed ${n_new} · updated ${n_upd} · already current ${n_same} · kept because you modified them ${n_kept} · removed ${n_gone}"
  [[ "$n_kept" -gt 0 ]] && echo "  (each kept file has the new version beside it as *.maestro-new — diff and merge at will)"
  if [[ "$FIRST_UPGRADE" -eq 1 ]]; then
    echo
    echo "  NOTE: this installation predates the manifest, so this run could not tell an old"
    echo "  file from one you edited, and overwrote nothing. From now on it can: the manifest"
    echo "  was just written. To take the method's version of everything instead, re-run with"
    echo "  --force (it overwrites file by file, saving your version as *.maestro-old first)."
    # The prune loop below only knows what the manifest recorded, and there is none — so the
    # files the method RETIRED are named here instead of being deleted blind. This is the
    # one that matters: it tells an agent to overwrite the ratified constitution.
    for r in "${RETIRED[@]}"; do
      [[ -e "$TARGET/$r" ]] && echo "  ALSO: '$r' is no longer part of the method and is still here — review and delete it."
    done
  fi
  # Only what WE wrote gets the executable bit: the project's own scripts are not ours to
  # touch, and the first version chmod'ed every .sh in the directory.
  if [[ "$DRY" -eq 0 ]]; then
    for rel in "${!NOW[@]}"; do
      [[ "$rel" == scripts/*.sh ]] && chmod +x "$TARGET/$rel" 2>/dev/null || true
    done
  fi
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
