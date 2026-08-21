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

# Which agent this project installed for, read from its own record. Without it this gate
# demanded `.claude/agents` from a Copilot project — a format that agent does not read and
# that the installer deliberately no longer ships there (independent review of cycle 057).
OPTS=".maestro/install-options.json"
AI_ID="claude"; AI_HARNESS="true"
if [[ -f "$OPTS" ]]; then
  AI_ID="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1])).get("ai","claude"))' "$OPTS" 2>/dev/null || echo claude)"
  AI_HARNESS="$(python3 -c 'import json,sys;print(str(json.load(open(sys.argv[1])).get("harness",True)).lower())' "$OPTS" 2>/dev/null || echo true)"
fi

echo "── Method layers (what was copied) ──"
LAYERS=("skills:skills" \
            "scripts/new-cycle.sh:cycle script" \
            "scripts/promote-main.sh:promotion script" \
            ".specify/templates:spec-driven templates" \
            "docs/governance/principles.md:constitution" \
            "docs/governance/operating-model.md:operating model")
[[ "$AI_ID" == "claude" ]] && LAYERS+=(".claude/agents:subagents")
for pair in "${LAYERS[@]}"; do
  target="${pair%%:*}"; name="${pair##*:}"
  if [[ -e "$target" ]]; then echo "  ok: $name ($target)"; else alert "$name missing: $target"; fi
done

# The instruction the AI reads. Either file is enough, but whichever exists must point
# at the method — a present, silent file is worse than a missing one: it looks installed.
echo ""
echo "── Instruction for the AI (what makes the AI follow it) ──"
# WHICH file, read from the installation's own record — not assumed to be CLAUDE.md. A
# correct `--ai copilot` install was permanently red here, because this list was hardcoded
# and the project's instruction lives in .github/copilot-instructions.md (independent review
# of cycle 057). The `instruction` field exists in install-options.json for exactly this.
INSTRUCTIONS=()
declared="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1])).get("instruction",""))' "$OPTS" 2>/dev/null || true)"
[[ -n "$declared" && -f "$declared" ]] && INSTRUCTIONS+=("$declared")
for f in CLAUDE.md AGENTS.md; do
  [[ -f "$f" ]] || continue
  # Deduplicated by REAL path: AGENTS.md is a symlink to CLAUDE.md here (ADR 0013), and every
  # drift was reported twice, as two findings, for one file.
  rp="$(readlink -f "$f" 2>/dev/null || echo "$f")"
  skip=0
  for k in "${INSTRUCTIONS[@]:-}"; do
    [[ -n "$k" ]] || continue
    [[ "$(readlink -f "$k" 2>/dev/null || echo "$k")" == "$rp" ]] && skip=1
  done
  [[ "$skip" -eq 1 ]] || INSTRUCTIONS+=("$f")
done
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

# ── The installed block against the block the installer generates TODAY ────────────────────
# One fact stated in two places stays the same only if something compares them (cycle 057, the
# family check-version.sh already fixed for the release number). The instruction file carries a
# copy of the method block; the generator is the source. They drift silently otherwise.
#
# The generator is NOT shipped to targets — install-maestro.sh stays on the source side — so
# where it is absent this cannot be checked. It SAYS SO instead of passing quietly: a check
# that cannot tell "identical" from "did not look" is anti-pattern 16.
echo ""
echo "── The installed method block × the one the installer generates ──"
# The block runs from its heading to the next `## ` heading, blanks stripped. The sed range
# used before never terminated when the block was last in the file, so it rejected the
# installer's own byte-identical output (independent review of cycle 057).
extract_block() {  # $1 = file
  awk 'BEGIN{inside=0;done=0;n=0}
       !inside && $0=="## Method: Maestro" {inside=1; buf[n++]=$0; next}
       inside && !done && /^## / {done=1}
       inside && !done {buf[n++]=$0}
       END{ if(!inside) exit 1
            while(n>0 && buf[n-1] ~ /^[ \t]*$/) n--
            for(i=0;i<n;i++) print buf[i] }' "$1"
}
INSTALLED_IN=()
for f in "${INSTRUCTIONS[@]:-}"; do
  [[ -n "$f" ]] && extract_block "$f" >/dev/null 2>&1 && INSTALLED_IN+=("$f")
done
if [[ ! -x scripts/install-maestro.sh ]]; then
  echo "  · not compared: the generator (scripts/install-maestro.sh) does not travel to installed copies"
elif [[ ${#INSTALLED_IN[@]} -eq 0 ]]; then
  echo "  · no generated block in the instruction file — it is described in prose here, which is allowed"
else
  # Generated for THIS installation: the block's enforcement sentence depends on the agent and
  # on whether the harness is really there, so comparing against the claude+hooks default
  # reported honest blocks as drift.
  gen_args=(--ai "$AI_ID" --block)
  [[ "$AI_HARNESS" == "true" ]] || gen_args=(--ai "$AI_ID" --no-hooks --block)
  for f in "${INSTALLED_IN[@]}"; do
    if diff -q <(scripts/install-maestro.sh "${gen_args[@]}" 2>/dev/null) <(extract_block "$f") >/dev/null 2>&1; then
      echo "  ok: $f carries exactly the block the installer generates"
    else
      alert "$f carries a Maestro block that DIFFERS from 'install-maestro.sh --ai $AI_ID --block' — regenerate it"
    fi
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
