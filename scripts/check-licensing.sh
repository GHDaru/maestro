#!/usr/bin/env bash
# check-licensing.sh — what is redistributed carries the notices it is obliged to carry.
#
# Why this exists: for 45 cycles Maestro rejected a CC BY-NC-SA catalogue on licence grounds
# while having NO LICENSE file of its own, no third-party notices, and a plugin manifest
# declaring "MIT" whose text existed nowhere. The installer copied that into other people's
# repositories. Rejecting someone else's licence while ignoring your own is the shape of
# defect this repository keeps finding in itself (anti-pattern 22).
#
# What this actually measures (anti-pattern 13): NOT legal compliance — no script can judge
# that. It measures that the ARTIFACTS a permissive licence requires exist, agree with each
# other, and travel with what is shipped. A lawyer answers the rest.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

fail=0
ok()  { printf '  ✓ %s\n' "$1"; }
bad() { printf '  ✗ %s\n' "$1"; fail=1; }

echo "── Licensing: does what we ship carry its notices? ──"

# 1. The licence exists as text, not as a claim in a manifest.
if [[ ! -f LICENSE ]]; then
  bad "no LICENSE file — a repository without one is 'all rights reserved', which is worse than the licence we rejected"
else
  DECLARED="$(grep -m1 -oE '^(MIT|Apache|BSD|GPL|MPL)[A-Za-z0-9 .-]*' LICENSE || true)"
  [[ -n "$DECLARED" ]] && ok "LICENSE present: ${DECLARED}" || bad "LICENSE present but its licence name is unreadable"
fi

# 2. The plugin manifest must not declare a licence the repository does not carry.
MANIFEST="plugin/maestro/.claude-plugin/plugin.json"
if [[ ! -f "$MANIFEST" ]]; then
  # A missing input is a finding, never a pass. The first version of this gate wrapped every
  # block in a bare `if [[ -f … ]]` with no `else`: deleting install-maestro.sh entirely made
  # the gate exit 0. A gate that cannot tell "clean" from "did not look" is anti-pattern 16.
  bad "$MANIFEST is missing — the plugin's licence claim cannot be checked"
else
  CLAIMED="$(grep -oE '"license"[[:space:]]*:[[:space:]]*"[^"]+"' "$MANIFEST" | grep -oE '"[^"]+"$' | tr -d '"' || true)"
  if [[ -z "$CLAIMED" ]]; then
    bad "$MANIFEST declares no licence while shipping the method"
  # -F: the manifest value is data, not a pattern. A metacharacter in that field would
  # otherwise be interpreted as a regex and could match a licence we do not carry.
  elif [[ -f LICENSE ]] && head -1 LICENSE | grep -qiF -- "$CLAIMED"; then
    ok "plugin manifest claims ${CLAIMED} and LICENSE says so"
  else
    bad "plugin manifest claims '${CLAIMED}' and LICENSE does not say so — a claim is not a licence"
  fi
fi

# 3. Third-party notices exist and name every upstream the provenance file names.
if [[ ! -f THIRD-PARTY-NOTICES.md ]]; then
  bad "no THIRD-PARTY-NOTICES.md — MIT has exactly one obligation and this is where it is met"
else
  ok "THIRD-PARTY-NOTICES.md present"
  UP=".specify/UPSTREAM.md"
  if [[ ! -f "$UP" ]]; then
    bad "$UP is missing — without the provenance file there is no list of upstreams to attribute"
  else
    # Upstreams are named as owner/repo in the "Origens" section. Extracted GENERICALLY, on
    # purpose: the first version hard-coded `spec-kit`, so a new vendored upstream — a GPL one,
    # say — entered the redistribution and the gate stayed green. FR5 says EVERY upstream.
    ups="$(sed -n '/^## Origens/,/^## /p' "$UP" \
           | grep -oE '\b[A-Za-z0-9][A-Za-z0-9_.-]*/[A-Za-z0-9][A-Za-z0-9_.-]*\b' \
           | grep -vE '^(https?|docs|scripts|specs|skills)/' | sort -u || true)"
    if [[ -z "$ups" ]]; then
      # Renaming `github/spec-kit` to "Spec Kit (by GitHub)" made the loop run zero times and
      # the summary still said "upstreams attributed". Empty is a finding, never a pass.
      bad "no owner/repo recognised under '## Origens' in $UP — the gate found nothing to check, which is not the same as finding nothing wrong"
    else
      while read -r proj; do
        [[ -n "$proj" ]] || continue
        if grep -qF -- "$proj" THIRD-PARTY-NOTICES.md; then
          ok "attributed: $proj"
        else
          bad "named in $UP but absent from THIRD-PARTY-NOTICES.md: $proj"
        fi
      done <<<"$ups"
    fi
  fi
  # A notice with no copyright line attributes nothing — and the holder is needed PER
  # PROJECT, not once per file. Two earlier versions were vacuous here: an unanchored
  # `Copyright ` matched this file's own prose ("the copyright notice and the permission
  # notice travel…"), and then a file-wide anchored match was satisfied by ANOTHER
  # project's holder while the one under test had none. Every `## owner/repo` heading owns
  # its own attribution.
  holderless="$(awk '
    /^## [A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+[[:space:]]*$/ {
      if (sec != "" && !seen) print sec
      sec = substr($0, 4); sub(/[[:space:]]+$/, "", sec); seen = 0; next
    }
    /^## / { if (sec != "" && !seen) print sec; sec = ""; seen = 0; next }
    /^- \*\*Copyright\*\*: .+/ { if (sec != "") seen = 1 }
    END { if (sec != "" && !seen) print sec }
  ' THIRD-PARTY-NOTICES.md)"
  n_proj="$(grep -cE '^## [A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+[[:space:]]*$' THIRD-PARTY-NOTICES.md || true)"
  if [[ "$n_proj" -eq 0 ]]; then
    bad "THIRD-PARTY-NOTICES.md has no '## owner/repo' section — nothing is attributed to anyone"
  elif [[ -n "$holderless" ]]; then
    while read -r s; do
      [[ -n "$s" ]] && bad "attributed with no holder: '${s}' has no '- **Copyright**: …' line — attribution without a holder is decoration"
    done <<<"$holderless"
  else
    ok "all ${n_proj} attributed project(s) name a copyright holder"
  fi
fi

# 4. The obligation travels: the installer must copy both into the target repository.
# Match the CALL, never the mention. Matching the bare word `LICENSE` was satisfied by the
# script's own comment and by the string `MAESTRO-LICENSE`, so deleting the copy_as line —
# the MIT obligation literally ceasing to travel — left the gate green.
INST="scripts/install-maestro.sh"
if [[ ! -f "$INST" ]]; then
  bad "$INST is missing — the installer is one of the two redistribution channels; it cannot be unverifiable"
else
  miss=()
  grep -qE '^[[:space:]]*copy_as "LICENSE"' "$INST" || miss+=("LICENSE")
  grep -qE '^[[:space:]]*copy_as "THIRD-PARTY-NOTICES.md"' "$INST" || miss+=("THIRD-PARTY-NOTICES.md")
  if [[ ${#miss[@]} -gt 0 ]]; then
    bad "the installer copies the method but not: ${miss[*]} — the notice must travel with the copy"
  else
    ok "installer carries LICENSE and THIRD-PARTY-NOTICES.md into the target"
  fi
fi

# 5. The plugin is the OTHER redistribution channel, and it ships ten commands derived from
# github/spec-kit. Shipping them with a manifest field and no text anywhere in the package is
# the same defect this cycle opened by accusing — one channel fixed, one left broken.
PKG="plugin/maestro"
if [[ ! -d "$PKG" ]]; then
  bad "$PKG is missing — run scripts/package-plugin.sh"
else
  miss=()
  [[ -f "$PKG/LICENSE" ]] || miss+=("LICENSE")
  [[ -f "$PKG/THIRD-PARTY-NOTICES.md" ]] || miss+=("THIRD-PARTY-NOTICES.md")
  if [[ ${#miss[@]} -gt 0 ]]; then
    bad "the packaged plugin ships without: ${miss[*]} — a manifest field is not a licence text"
  else
    ok "packaged plugin carries LICENSE and THIRD-PARTY-NOTICES.md"
  fi
fi

echo "──"
if [[ $fail -ne 0 ]]; then
  echo "✗ what is shipped does not carry the notices it owes."
  exit 1
fi
echo "✓ licence present, manifest agrees, upstreams attributed, notices travel with the copy."
