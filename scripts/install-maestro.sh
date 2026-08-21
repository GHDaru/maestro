#!/usr/bin/env bash
# install-maestro.sh — installs Maestro (agents + skills + scripts + templates) into
# another repository, so the AI follows the method there.
#
# Usage (from inside the Maestro repository):
#   scripts/install-maestro.sh /path/to/project               # installs, for --ai claude
#   scripts/install-maestro.sh /path/to/project --dry-run     # shows what it would do
#   scripts/install-maestro.sh --ai list                      # which agents it can serve
#   scripts/install-maestro.sh <dir> --ai codex               # install for another agent
#   scripts/install-maestro.sh <dir> --write-block            # also write the method block
#   scripts/install-maestro.sh <dir> --no-hooks               # skip the enforcement layer
#   scripts/install-maestro.sh <dir> --force                  # take our version (saves theirs)
#   scripts/install-maestro.sh --block                        # print the block and stop
#
# Easier: `bin/maestro init <dir> --ai <id>` walks the same steps and verifies at the end.
#
# Installing is also UPGRADING. A file we wrote and you never touched is refreshed; a file
# you modified is kept, with the new version beside it as *.maestro-new; a file the method
# no longer ships is removed only while it is still untouched. Nothing you wrote is ever
# overwritten without --force, and --force saves your version as *.maestro-old first.
set -euo pipefail

TARGET=""
SOURCE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

ARG_DRY=0; ARG_FORCE=0; ARG_BLOCK=0; ARG_NO_HOOKS=0; ARG_WRITE_BLOCK=0
USER_NO_HOOKS=0   # did the PERSON ask, or did the agent's row decide? The reason differs.
ARG_AI="claude"   # the historical behaviour, now SAID OUT LOUD instead of assumed
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)     ARG_DRY=1 ;;
    --force)       ARG_FORCE=1 ;;
    --block)       ARG_BLOCK=1 ;;
    --no-hooks)    ARG_NO_HOOKS=1; USER_NO_HOOKS=1 ;;
    --write-block) ARG_WRITE_BLOCK=1 ;;
    --ai)          shift; ARG_AI="${1:-}"
                   [[ -n "$ARG_AI" && "$ARG_AI" != -* ]] || { echo "error: --ai needs an agent id, got '${ARG_AI:-nothing}' (try: --ai list)" >&2; exit 2; } ;;
    --ai=*)        ARG_AI="${1#--ai=}" ;;
    -*)            echo "error: unknown flag '$1'" >&2; exit 2 ;;
    *)             [[ -z "$TARGET" ]] && TARGET="$1" || { echo "error: more than one target given" >&2; exit 2; } ;;
  esac
  shift
done

# ── The agent is a DECLARED CHOICE, not an assumption ──────────────────────────────────────
# Until cycle 057 this installer copied `.claude/*` and printed a CLAUDE.md block whatever you
# used: a method whose installer silently assumed one tool. The upstream solved this long ago
# — `.specify/init-options.json` records `"ai"`, and 27 agents each have their own instruction
# file. The table below is the whole of our support, and adding an agent is a row plus a test.
AGENTS_TSV="$SOURCE/scripts/install-agents.tsv"
[[ -f "$AGENTS_TSV" ]] || { echo "error: the agent table is missing ($AGENTS_TSV) — nothing can be installed without it." >&2; exit 1; }
# `\r` is stripped for the same reason the manifest reader strips it: a table saved on Windows
# turned `yes` into `yes\r`, which silently disabled the whole enforcement layer for Claude
# Code while the summary explained that Claude Code does not run hooks (independent review).
agent_rows() { tr -d '\r' < "$AGENTS_TSV" | grep -v '^#'; }
agent_row() { agent_rows | awk -F'\t' -v id="$1" 'NF>=5 && $1==id {print; exit}'; }
agent_ids() { agent_rows | awk -F'\t' 'NF>=5 {printf "%s ", $1}'; }

if [[ "$ARG_AI" == "list" ]]; then
  # Listing is not installing. Combined with a target it printed the table and exited 0,
  # turning an install command into a silent no-op with a success code.
  [[ -z "$TARGET" ]] || { echo "error: --ai list only lists; drop the target, or pick an agent id." >&2; exit 2; }
  printf '%-14s %-66s %-34s %-18s %s\n' id name "instruction file" "commands" "harness"
  agent_rows | awk -F'\t' 'NF>=5 {printf "%-14s %-66s %-34s %-18s %s\n",$1,$2,$3,$4,$5}'
  echo
  echo "'-' under commands means the format was not verified for that agent, so nothing is"
  echo "installed there — shipping files nobody reads is not support."
  exit 0
fi

AGENT_ROW="$(agent_row "$ARG_AI")"
if [[ -z "$AGENT_ROW" ]]; then
  # An unknown id NEVER falls back to the default: a silent default is how somebody installs
  # for the wrong tool and finds out later.
  echo "error: unknown agent '$ARG_AI'. Known: $(agent_ids)" >&2
  echo "       see them with:  scripts/install-maestro.sh --ai list" >&2
  exit 2
fi
AGENT_NAME="$(cut -f2 <<<"$AGENT_ROW")"
AGENT_INSTRUCTION="$(cut -f3 <<<"$AGENT_ROW")"
AGENT_COMMANDS="$(cut -f4 <<<"$AGENT_ROW")"
AGENT_HARNESS="$(cut -f5 <<<"$AGENT_ROW")"
[[ "$AGENT_HARNESS" == "yes" ]] || ARG_NO_HOOKS=1

# The instruction block is GENERATED from the skills that exist on disk — a hand-written
# list ages silently (that was the failure mode of Maestro's own repository, cycle 021).
method_block() {
  echo '## Method: Maestro'
  # An @-import INLINES the file into every session of this repository; a citation only asks.
  # The constitution is imported because it is the binding text (6,072 B, ~1,518 tokens per
  # load, measured in cycle 056). The operating model is NOT (~4,551 tokens): it is reference
  # consulted on demand, and automatic context is a cost imposed on every session here.
  echo '@docs/governance/principles.md'
  echo ''
  echo '- The constitution above is loaded automatically. Read'
  echo '  `docs/governance/operating-model.md` before any work — it is not.'
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
  echo '  (`TAIL:review`, `TAIL:security`, `TAIL:mutation`, `TAIL:gate`) in `tasks.md`, with'
  echo '  the evidence in'
  echo '  `qa-report.md`. Catalogue: `docs/governance/artifacts.md`.'
  echo '- **Asked "are you following the method?" — do NOT answer from memory.** Run'
  echo '  `scripts/check-conformance.sh <NNN>` and read it: memory reports intention, not fact.'
  # The enforcement sentence is printed ONLY when the harness is actually active. Claiming a
  # force function that is not installed is the defect this cycle exists to fix, inverted —
  # and every non-Claude agent, --no-hooks run and refused merge lands on that branch
  # (independent review of cycle 056).
  echo '- Never REWRITE what the method keeps as history: the body of a committed ADR,'
  echo '  `docs/records/decisoes.jsonl`, and the dated idea cards under `docs/ecosystem/ideias/`.'
  echo '  The route is always to APPEND — a new ADR that supersedes, `scripts/record-decision.sh`,'
  if [[ "${HOOKS_ACTIVE:-0}" -eq 1 ]]; then
    echo '  a new state line. **A `PreToolUse` guard refuses the rewrite**, so this is enforced,'
    echo '  not asked.'
  else
    echo '  a new state line. **Nothing enforces this in this installation** — no guard is'
    echo '  installed here, so it holds only while it is followed.'
  fi
}

# --block: prints only the instruction for the AI (redirect it into the agent's file).
# The enforcement sentence depends on whether the harness will actually be there, so --block
# answers for the install it describes: this agent, these flags. Without this it always
# printed the weaker branch, and the block in a real installation never matched the generator
# — which is precisely the drift check-install.sh now refuses (cycle 057).
if [[ "$ARG_BLOCK" -eq 1 ]]; then
  [[ "$AGENT_HARNESS" == "yes" && "$ARG_NO_HOOKS" -eq 0 ]] && HOOKS_ACTIVE=1 || HOOKS_ACTIVE=0
  method_block; exit 0
fi

[[ -n "$TARGET" ]] || { echo "usage: scripts/install-maestro.sh <target> [--ai <id>|list] [--dry-run|--force|--block|--no-hooks|--write-block]" >&2; exit 2; }
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

# A symlink in the target is a door out of it. `cp` writes THROUGH a symlinked file, and a
# symlinked DIRECTORY makes every path under it land somewhere else entirely — so the prune
# loop would delete outside the repository it was pointed at. Inherited from `cp -r`, and it
# grew teeth in cycle 051 when this script gained the power to remove. Nothing is written or
# removed through a link: refused, named, and the run continues (cycle 052).
escapes_via_symlink() {  # $1 = relative path; 0 = it or a parent is a symlink
  local rel="$1" cur="$TARGET"
  [[ -L "$TARGET/$rel" ]] && return 0
  local IFS=/ part
  for part in $rel; do
    [[ -n "$part" ]] || continue
    cur="$cur/$part"
    [[ "$cur" == "$TARGET/$rel" ]] && break
    [[ -L "$cur" ]] && return 0
  done
  return 1
}

n_new=0; n_upd=0; n_same=0; n_kept=0; n_gone=0; n_refused=0

# The manifest must record what WE wrote — nothing else. The first version stamped every
# path it looked at, so a file the project already had, byte-identical to ours (a project
# that ran `specify init` on its own has exactly that), was adopted as ours without a word
# — and the prune loop later DELETED it. Claiming is now a consequence of writing.
install_file() {  # $1 = source file, $2 = relative destination
  local src="$1" rel="$2" dst="$TARGET/$2" hs hd
  if escapes_via_symlink "$rel"; then
    echo "  ! refused (a symlink on this path leads outside the target): $rel" >&2
    n_refused=$((n_refused+1)); return
  fi
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
if [[ "$ARG_AI" == "claude" ]]; then
  copy ".claude/agents"
else
  echo "  · subagent definitions: not installed — .claude/agents is a Claude Code format, and ${AGENT_NAME} does not read it"
fi

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
if [[ "$AGENT_COMMANDS" == "-" ]]; then
  echo "  · commands: not installed — the format was not verified for ${AGENT_NAME}"
elif [[ "$AGENT_COMMANDS" == ".claude/commands" ]]; then
  copy ".claude/commands"
else
  # find -type f, never a glob: a glob hands DIRECTORIES to copy_as, hash_of fails on one,
  # and under `set -e` + pipefail the run dies mid-install leaving NO manifest — the exact
  # failure the manifest was built to prevent (independent review of cycle 057).
  while IFS= read -r c; do
    rel="${c#"$SOURCE"/.claude/commands/}"
    copy_as ".claude/commands/$rel" "$AGENT_COMMANDS/$rel"
  done < <(find "$SOURCE/.claude/commands" -type f | sort)
fi
copy ".specify/templates"
copy ".specify/UPSTREAM.md"
# The /speckit.* commands we ship CALL these; shipping the commands without them was the
# defect of cycle 048 — a thing that points at something we do not send. The notices file
# already declared this directory as redistributed, so sending it also makes that true.
copy ".specify/scripts"
# The upstream's options file travels because /speckit.specify reads `branch_numbering` from
# it — but its `ai` field shipped as "claude" into every target, contradicting our own
# .maestro/install-options.json in the same directory tree (independent review of cycle 057).
# It is materialised with the CHOSEN agent instead of copied, so the two never disagree.
_init_tmp="$(mktemp)"
python3 -c 'import json,sys
d=json.load(open(sys.argv[1])); d["ai"]=sys.argv[2]
json.dump(d, open(sys.argv[3],"w"), indent=2, sort_keys=True); open(sys.argv[3],"a").write("\n")' \
  "$SOURCE/.specify/init-options.json" "$ARG_AI" "$_init_tmp"
install_file "$_init_tmp" ".specify/init-options.json"
rm -f "$_init_tmp"

echo "── Governance (the source of truth) ──"
copy "docs/governance/principles.md"
copy "docs/governance/operating-model.md"
copy "docs/governance/glossary.md"
copy "docs/governance/axioms.md"
copy "docs/governance/artifacts.md"
copy "docs/records/README.md"

# ── Harness: the layer that ENFORCES instead of asking ────────────────────────────────────
# Everything above is text an agent has to read and remember. This is the first part of the
# method that refuses BEFORE the damage: a PreToolUse guard on the artifacts the method keeps
# as history, and a SessionStart hook that loads the measured state instead of letting the
# agent reconstruct it. Cycle 056 measured the gap that justifies it: NOTHING enforced any of
# them, in the middle of this method's own governance.
HOOKS_STATE="skipped (--no-hooks)"
[[ "$AGENT_HARNESS" == "yes" ]] || HOOKS_STATE="not installed — hooks are a Claude Code mechanism, and ${AGENT_NAME} does not run them"
HOOKS_ACTIVE=0
SETTINGS_REL=".claude/settings.json"
if [[ "$ARG_NO_HOOKS" -eq 1 ]]; then
  # --no-hooks does NOT uninstall.
  # The REASON is not the flag: when the agent's row says `no`, saying "skipped (--no-hooks)"
  # hides the only thing the person needs to know (independent review of cycle 057). The files are claimed so the prune loop leaves them alone:
  # deleting the scripts while settings.json still names them pointed a third party's every
  # write at a missing command, and the summary called that "skipped" (independent review).
  for kept in scripts/hooks/guard-immutables.py scripts/hooks/session-state.sh; do
    [[ -e "$TARGET/$kept" ]] && NOW["$kept"]="${PREV[$kept]:-unmanaged}"
  done
  live=0
  [[ -f "$TARGET/$SETTINGS_REL" ]] && grep -q 'guard-immutables' "$TARGET/$SETTINGS_REL" 2>/dev/null \
    && [[ -e "$TARGET/scripts/hooks/guard-immutables.py" ]] && live=1
  if [[ "$USER_NO_HOOKS" -eq 1 ]]; then
    [[ "$live" -eq 1 ]] && HOOKS_STATE="left as they were (--no-hooks does not uninstall)"
  elif [[ "$live" -eq 1 ]]; then
    # Honest, and it is the awkward case: a previous Claude install left the layer live in a
    # repository now being installed for another agent. Claiming "not installed" would be
    # false, and the person has to decide.
    HOOKS_STATE="STILL LIVE from an earlier install — ${AGENT_NAME} does not run hooks; remove ${SETTINGS_REL} and scripts/hooks/ if you want them gone"
  fi
else
  echo "── Harness (rules that are enforced, not remembered) ──"
  # Copied file by file, not as a directory: merge-settings.py is installer-side plumbing and
  # has no business in a target that never calls it (anti-pattern 22, the shipping half).
  copy "scripts/hooks/guard-immutables.py"
  copy "scripts/hooks/session-state.sh"

  if escapes_via_symlink "$SETTINGS_REL"; then
    echo "  ! refused (a symlink on this path leads outside the target): $SETTINGS_REL" >&2
    n_refused=$((n_refused+1)); HOOKS_STATE="refused (symlink)"
  else
    # The verdict comes from one place, testable on its own: scripts/hooks/merge-settings.py.
    MERGE_OUT="$(python3 "$SOURCE/scripts/hooks/merge-settings.py" "$TARGET/$SETTINGS_REL" "$SOURCE/$SETTINGS_REL" 2>/dev/null || echo "ERROR merge helper failed")"
    MERGE_VERDICT="${MERGE_OUT%%$'\n'*}"
    # Never a raw redirect: under `set -e` a read-only target killed the run AFTER 78 files
    # and BEFORE the manifest, disowning the whole installation forever (independent review).
    write_settings() {  # stdin = content; echoes ok|fail
      local tmp="$TARGET/$SETTINGS_REL.tmp.$$"
      mkdir -p "$TARGET/.claude" 2>/dev/null || { echo fail; return 0; }
      if cat > "$tmp" 2>/dev/null && mv "$tmp" "$TARGET/$SETTINGS_REL" 2>/dev/null; then
        echo ok
      else
        rm -f "$tmp" 2>/dev/null || true; echo fail
      fi
    }
    case "$MERGE_VERDICT" in
      CURRENT)
        HOOKS_ACTIVE=1; HOOKS_STATE="already current"
        echo "  = already current: $SETTINGS_REL" ;;
      WRITE|MERGED)
        if [[ "$ARG_DRY" -eq 1 ]]; then
          echo "  + would install: $SETTINGS_REL"; HOOKS_ACTIVE=1; HOOKS_STATE="would be installed"
        else
          if [[ "$MERGE_VERDICT" == WRITE ]]; then payload="$(cat "$SOURCE/$SETTINGS_REL")"
          else payload="${MERGE_OUT#MERGED$'\n'}"; fi
          if [[ "$(printf '%s\n' "$payload" | write_settings)" == ok ]]; then
            echo "  + installed: $SETTINGS_REL"
            n_new=$((n_new+1)); HOOKS_ACTIVE=1
            HOOKS_STATE="installed"
            [[ "$MERGE_VERDICT" == MERGED ]] && HOOKS_STATE="added to your settings.json"
          else
            echo "  ! refused: cannot write $SETTINGS_REL (permissions?) — nothing changed." >&2
            n_refused=$((n_refused+1)); HOOKS_STATE="refused (cannot write settings.json)"
          fi
        fi ;;
      CONFLICT)
        echo "  ! refused: $SETTINGS_REL already configures other hooks — yours stay, ours are not installed." >&2
        echo "    To enable them, merge this into your settings.json:" >&2
        python3 "$SOURCE/scripts/hooks/merge-settings.py" "$TARGET/$SETTINGS_REL" "$SOURCE/$SETTINGS_REL" --snippet 2>/dev/null | sed 's/^/      /' >&2
        n_refused=$((n_refused+1)); HOOKS_STATE="refused (you already configure other hooks)" ;;
      *)
        echo "  ! refused: ${MERGE_OUT#ERROR } — $SETTINGS_REL unchanged." >&2
        n_refused=$((n_refused+1)); HOOKS_STATE="refused (unreadable settings.json)" ;;
    esac
  fi
fi

# What we shipped once and ship no longer must GO — otherwise the installation accumulates
# the method's own mistakes. `.specify/memory/constitution.md` is the case that named this:
# it was dropped in cycle 048 and would otherwise sit there forever, telling an agent to
# overwrite the constitution. Only removed while still untouched: an edited file is theirs.
for rel in "${!PREV[@]}"; do
  [[ -n "${NOW[$rel]:-}" ]] && continue
  dst="$TARGET/$rel"
  [[ -e "$dst" ]] || continue
  if escapes_via_symlink "$rel"; then
    echo "  ! not removed (a symlink on this path leads outside the target): $rel" >&2
    n_refused=$((n_refused+1)); continue
  fi
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

# ── The choice, written down ───────────────────────────────────────────────────────────────
# Same idea as the upstream's `.specify/init-options.json`: a project should be able to answer
# "which agent was this installed for?" without anyone remembering. `harness` records the
# FACT of this run, not what the table permits — with --no-hooks on an agent that supports
# them, the table says yes and this says false. A state file that stores the intention instead
# of the result is the lie this method has chased since cycle 042.
OPTIONS_REL=".maestro/install-options.json"
if [[ "$ARG_DRY" -eq 0 ]] && escapes_via_symlink "$OPTIONS_REL"; then
  echo "  ! refused (a symlink on this path leads outside the target): $OPTIONS_REL" >&2
  n_refused=$((n_refused+1))
elif [[ "$ARG_DRY" -eq 0 ]]; then
  # The FACT, not the flag: with --no-hooks over an install whose hooks are present AND wired,
  # the layer is live, and writing `false` would assert an absence that is not true
  # (independent review of cycle 057).
  harness_fact=false
  if [[ "$HOOKS_ACTIVE" -eq 1 ]]; then harness_fact=true
  elif [[ -f "$TARGET/.claude/settings.json" && -x "$TARGET/scripts/hooks/guard-immutables.py" ]] \
       && grep -q 'guard-immutables' "$TARGET/.claude/settings.json" 2>/dev/null; then harness_fact=true; fi
  mkdir -p "$TARGET/.maestro" 2>/dev/null || true
  # Built by a JSON writer, not printf: a quote or a backslash in any field produced a file
  # that json.load refuses to read (independent review of cycle 057).
  python3 -c 'import json,sys; json.dump(dict(zip(["ai","instruction","harness","maestro_version","installed"],[sys.argv[1],sys.argv[2],sys.argv[3]=="true",sys.argv[4],sys.argv[5]])), sys.stdout); print()' \
    "$ARG_AI" "$AGENT_INSTRUCTION" "$harness_fact" "$(sed -n '/^## \[Unreleased\]/,$p' "$SOURCE/CHANGELOG.md" | grep -m1 -oE '^## \[[0-9]+\.[0-9]+\.[0-9]+\]' | tr -d '#[] ' || echo unknown)" "$(date +%Y-%m-%d)" \
    > "$TARGET/$OPTIONS_REL" 2>/dev/null || echo "  ! could not write $OPTIONS_REL" >&2
fi

# ── --write-block: append if absent, REFUSE if a different one is already there ─────────────
# The instruction file belongs to the project, so the default stays "print it". When asked to
# write, the rule is the one settings.json got in cycle 056: add what is missing, never
# replace what somebody else put there.
# The block runs from its heading to the next `## ` heading, with trailing blanks stripped.
# The sed range that did this before never terminated when the block was last in the file, so
# `sed '$d'` ate the block's own last line and the "already current" branch was unreachable:
# the installer refused its own byte-identical output on every re-run (independent review).
extract_block() {  # $1 = file; prints the installed block, or fails
  awk 'BEGIN{inside=0;done=0;n=0}
       !inside && $0=="## Method: Maestro" {inside=1; buf[n++]=$0; next}
       inside && !done && /^## / {done=1}
       inside && !done {buf[n++]=$0}
       END{ if(!inside) exit 1
            while(n>0 && buf[n-1] ~ /^[ \t]*$/) n--
            for(i=0;i<n;i++) print buf[i] }' "$1"
}

BLOCK_STATE="printed only (use --write-block to append it)"
if [[ "$ARG_WRITE_BLOCK" -eq 1 ]] && escapes_via_symlink "$AGENT_INSTRUCTION"; then
  echo "  ! refused (a symlink on this path leads outside the target): $AGENT_INSTRUCTION" >&2
  n_refused=$((n_refused+1)); BLOCK_STATE="refused (symlink)"
elif [[ "$ARG_WRITE_BLOCK" -eq 1 ]]; then
  dst="$TARGET/$AGENT_INSTRUCTION"
  if grep -q '^## Method: Maestro' "$dst" 2>/dev/null; then
    if diff -q <(method_block) <(extract_block "$dst") >/dev/null 2>&1; then
      BLOCK_STATE="already current in ${AGENT_INSTRUCTION}"
    else
      echo "  ! refused: ${AGENT_INSTRUCTION} already carries a DIFFERENT Maestro block — yours stays." >&2
      echo "    Compare with:  scripts/install-maestro.sh --block" >&2
      n_refused=$((n_refused+1)); BLOCK_STATE="refused (a different block is already there)"
    fi
  elif [[ "$ARG_DRY" -eq 1 ]]; then
    BLOCK_STATE="would be appended to ${AGENT_INSTRUCTION}"
  else
    mkdir -p "$(dirname "$dst")" 2>/dev/null || true
    { echo; method_block; } >> "$dst" 2>/dev/null \
      && BLOCK_STATE="appended to ${AGENT_INSTRUCTION}" \
      || { echo "  ! refused: cannot write ${AGENT_INSTRUCTION}" >&2; n_refused=$((n_refused+1)); BLOCK_STATE="refused (cannot write)"; }
  fi
fi

if true; then
  echo
  echo "── Summary ──"
  echo "  installed ${n_new} · updated ${n_upd} · already current ${n_same} · kept because you modified them ${n_kept} · removed ${n_gone} · refused ${n_refused}"
  echo "  harness (hooks that refuse before the damage): ${HOOKS_STATE}"
  echo "  agent: ${AGENT_NAME} (--ai ${ARG_AI}) · instruction file: ${AGENT_INSTRUCTION}"
  echo "  method block: ${BLOCK_STATE}"
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
      [[ "$rel" == scripts/*.sh || "$rel" == scripts/hooks/* ]] && chmod +x "$TARGET/$rel" 2>/dev/null || true
    done
  fi
  # the decision index starts empty in a new project (history belongs to each project)
  # Not on a dry run: `--dry-run` is documented as writing nothing, and this line was the one
  # exception — outside the guard since before cycle 057, and the reason `find` on a dry-run
  # target came back with one file (independent review of cycle 058).
  [[ "$ARG_DRY" -eq 1 ]] || [[ -f "$TARGET/docs/records/decisoes.jsonl" ]] \
    || { mkdir -p "$TARGET/docs/records"; : > "$TARGET/docs/records/decisoes.jsonl"; }
fi


echo
echo "── Next steps (in the target project) ──"
echo "  1. Add the block below to ${AGENT_INSTRUCTION} — the file ${AGENT_NAME} reads"
echo "     (or let the installer do it:  --ai ${ARG_AI} --write-block):"
echo
method_block | sed 's/^/     /'
if [[ "$ARG_AI" == "claude" ]]; then
  echo "     (tip: keep ONE source — \`ln -s CLAUDE.md AGENTS.md\` — so the two instructions"
  echo "     cannot diverge.)"
fi
cat <<'FIM'

  2. Prove it is installed:  scripts/check-install.sh
     (it fails while the instruction file does not point at the method: copying files is
     not installing — installed is when the AI knows it must follow them.)
  3. Open the first cycle:   scripts/new-cycle.sh 001 <slug>
  4. When promoting:         scripts/promote-main.sh
  5. In the retrospective:   scripts/retro.sh
  6. "Am I following it?":   scripts/check-conformance.sh

FIM
echo "done."
