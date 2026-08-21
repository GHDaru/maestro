#!/usr/bin/env bash
# SessionStart hook: load the state of the method instead of remembering it.
#
# SessionStart is the one event whose plain stdout becomes context the agent can see. So this
# prints FACTS, measured now, by the same scripts a human would run: which cycle is open,
# whether it conforms, what findings are outstanding and how old, and where the tree stands.
#
# It exists because of a specific failure shape this repository keeps producing: an agent
# answering "am I following the method?" from memory, and answering INTENTION. Memory is not a
# witness (corollary C13). Nothing here is new information — it is the same information,
# loaded rather than recalled.
#
# It never fails the session: every command is guarded, and the hook always exits 0.
set -uo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT" 2>/dev/null || exit 0
[[ -d scripts ]] || exit 0   # method not installed here; say nothing

echo "── Maestro: state measured at session start ──"

# `git rev-parse --abbrev-ref HEAD` prints "HEAD" AND exits non-zero on an unborn branch, so
# `|| echo '?'` used to CONCATENATE both — a two-line broken fact injected into the context of
# every session in a freshly `git init`ed repository, which is exactly the state the
# installer's own next-steps produce (independent review of cycle 056).
branch="$(git symbolic-ref --short -q HEAD 2>/dev/null || true)"
[[ -n "$branch" ]] || branch="(no commit yet)"
dirty="$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')"
echo "  branch: ${branch} · uncommitted paths: ${dirty}"

# The cycle being written is the newest directory; naming it removes a guess.
shopt -s nullglob
cycles=(specs/[0-9][0-9][0-9]-*/)
shopt -u nullglob
if [[ ${#cycles[@]} -eq 0 ]]; then
  echo "  cycles: none yet — open one with scripts/new-cycle.sh 001 <slug>"
else
  newest="$(basename "${cycles[${#cycles[@]}-1]}")"
  n="${newest%%-*}"
  echo "  newest cycle: ${newest}"
  if [[ -x scripts/check-conformance.sh ]]; then
    if out="$(scripts/check-conformance.sh "$n" 2>&1)"; then
      echo "  conformance (${n}): green"
    else
      # The first failing line is the actionable one; the rest is the same story in detail.
      first="$(grep -m1 '✗' <<<"$out" | sed 's/^ *//')"
      echo "  conformance (${n}): RED — ${first:-see scripts/check-conformance.sh $n}"
    fi
  fi
fi

if [[ -x scripts/check-retro.sh ]]; then
  if out="$(scripts/check-retro.sh 2>&1)"; then
    echo "  retrospective debt: under control"
  else
    echo "  retrospective debt: DUE — $(grep -m1 '✗' <<<"$out" | sed 's/^ *//')"
  fi
  # Open findings are the queue; naming them beats "there is some debt".
  grep -E '^\s+achado-' <<<"${out:-}" | sed 's/^ */  · /' || true
fi

echo "  rules that are enforced, not remembered: ADR bodies, docs/records/decisoes.jsonl and"
echo "  docs/ecosystem/ideias/* are refused by a PreToolUse guard — append, never rewrite."
exit 0
