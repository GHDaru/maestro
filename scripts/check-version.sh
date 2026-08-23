#!/usr/bin/env bash
# check-version.sh — the repository states ONE version, in every place it states one.
#
# Why it exists: closing v0.1.0 in cycle 045 wrote the number into four places — the
# CHANGELOG heading, README.md, the roadmap header and the packaged plugin's README. Nothing
# compared them. Four copies of one fact, kept in agreement by memory, is the shape this
# repository has now found five times: the profile index, the ADR index, the provenance
# table, the installed copy, and this. Memory is not a witness (corollary C13).
#
# The failure it prevents is specific and embarrassing: a release note announcing 0.2.0 while
# the front page still greets everyone with 0.1.0.
#
# What this actually measures (anti-pattern 13): NOT that the version number is the RIGHT one
# — semantic versioning is a human judgement about what changed. It measures that the
# repository does not tell two stories about which version it is.
#
# Usage:  scripts/check-version.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

fail=0
ok()  { printf '  ✓ %s\n' "$1"; }
bad() { printf '  ✗ %s\n' "$1"; fail=1; }

echo "── One version, in every place that states one ──"

# The source of truth is the newest RELEASED heading in the CHANGELOG — never [Unreleased],
# which by definition is not a version yet.
[[ -f CHANGELOG.md ]] || { bad "CHANGELOG.md is missing — there is no released version to agree with"; }
[[ $fail -eq 0 ]] || { echo "──"; echo "✗ cannot determine the version."; exit 1; }

# The newest released version is the first `## [X.Y.Z]` heading BELOW `## [Unreleased]`.
# Reading the first one anywhere let a `## [0.3.0] — planejada` written under [Unreleased] be
# adopted as released: the first version excluded the LABEL, not the region.
RELEASED="$(sed -n '/^## \[Unreleased\]/,$p' CHANGELOG.md | grep -m1 -oE '^## \[[0-9]+\.[0-9]+\.[0-9]+\]' | tr -d '#[] ' || true)"
if [[ -z "$RELEASED" ]]; then
  bad "CHANGELOG.md has no released version heading (## [X.Y.Z]) below [Unreleased] — only [Unreleased] is not a version"
  echo "──"; echo "✗ cannot determine the version."; exit 1
fi
ok "CHANGELOG declares ${RELEASED} as the newest released version"

# "Newest" is POSITIONAL in Keep a Changelog — newest on top. If the file is not actually in
# descending order, the position lies: a `## [0.10.0]` added below `## [0.2.0]` would be the
# real newest and invisible here. Cheap to check, and it keeps the rule above honest.
prev=""
while read -r v; do
  [[ -n "$v" ]] || continue
  if [[ -n "$prev" ]]; then
    newer="$(printf '%s\n%s\n' "$prev" "$v" | sort -t. -k1,1n -k2,2n -k3,3n | tail -1)"
    [[ "$newer" == "$prev" ]] || bad "CHANGELOG headings are out of order: ${v} appears below ${prev} — 'newest' is the top one, so the order is what makes it true"
  fi
  prev="$v"
done < <(grep -oE '^## \[[0-9]+\.[0-9]+\.[0-9]+\]' CHANGELOG.md | tr -d '#[] ')

# Every other place that states a version must state THIS one — read from the line that
# DECLARES it, never from the first version-looking string in the file. Reading the file let
# a historical mention ("gates exist since v0.2.0") satisfy the check while the header still
# greeted everyone with v0.1.0 — the exact failure this gate claims to prevent — and let an
# unrelated number on the header line ("fork do spec-kit 0.4.3") turn a coherent repository
# red. Both found by the independent review of this cycle.
claims() {  # $1 = file, $2 = human name, $3 = regex of the DECLARING line
  local f="$1" name="$2" re="$3" line found
  [[ -f "$f" ]] || { bad "${name} (${f}) is missing"; return; }
  line="$(grep -m1 -E "$re" "$f" || true)"
  if [[ -z "$line" ]]; then
    bad "${name} (${f}) has no line matching its version declaration — it is one of the places a reader looks first"
    return
  fi
  found="$(grep -m1 -oE 'v?[0-9]+\.[0-9]+\.[0-9]+' <<<"$line" | head -1 | tr -d 'v' || true)"
  if [[ -z "$found" ]]; then
    bad "${name} (${f}) declares no version on its declaration line"
  elif [[ "$found" != "$RELEASED" ]]; then
    bad "${name} says ${found} and the CHANGELOG says ${RELEASED} — the repository tells two stories about which version it is"
  else
    ok "${name} agrees: ${found}"
  fi
}

# The shape of each declaration is a contract, so it is written here and nowhere else.
claims "README.md"                 "the front page"        '^> \*\*v[0-9]'
claims "docs/roadmap.md"           "the roadmap header"    '\*\*Versão\*\*:'          # PT-DATA
claims "plugin/maestro/README.md"  "the packaged plugin"   '^> \*\*v[0-9]'

# NOT checked here, on purpose: plugin/maestro/.claude-plugin/plugin.json and
# .claude-plugin/marketplace.json carry a DIFFERENT axis — the plugin manifest tracks the
# constitution's version (1.3.0), not the release. Undeclared until the review of cycle 050
# asked why the same directory shows 1.3.0 and v0.2.0. Written down so the next reader does
# not have to ask, and so that making them one axis stays a decision, not an accident.

# Keep a Changelog puts ONE section per type inside a version. [Unreleased] had accumulated
# FOUR `### Adicionado`, one per cycle — which turns a release note into a ship's log, and
# leaves the version cut to merge them by hand at the worst possible moment. Nothing read the
# structure of this file, only the fact that it had changed (achado-060, closed by 061).
#
# Scope: [Unreleased] ONLY. It is the section still being written, and the one that
# accumulates — a cycle per bullet. The released sections below carry the same debt (v0.1.0
# repeats `### Changed` twice), and it stays declared rather than erased: a released changelog
# entry is a historical record, and retroactivity turns a gate into noise (same precedent as
# the FLOOR knobs in check-cycle.sh and check-conformance.sh). A version cut renames
# [Unreleased] to [X.Y.Z], so what this checks while it is being written is what ships.
echo ""
echo "── One section per type inside [Unreleased] ──"
dup="$(awk '
  /^## \[Unreleased\]/ { version = $0; delete seen; next }
  /^## \[/ { version = ""; next }
  /^### / {
    if (version == "") next
    t = $0; sub(/^### +/, "", t); sub(/[ \t]+$/, "", t)
    if (t in seen) printf "%s repeats \"### %s\" (first at line %d, again at line %d)\n", version, t, seen[t], NR
    else seen[t] = NR
  }
' CHANGELOG.md || true)"
if [[ -n "$dup" ]]; then
  while IFS= read -r d; do [[ -n "$d" ]] && bad "$d"; done <<<"$dup"
else
  ok "no version repeats a section type"
fi

echo "──"
if [[ $fail -ne 0 ]]; then
  echo "✗ the version is stated more than once, and not the same way."
  exit 1
fi
echo "✓ every place that states a version states ${RELEASED}."
