#!/usr/bin/env bash
# new-cycle.sh — creates the skeleton of a Maestro cycle (a spec).
# Standardises specs/NNN-slug/ with the four mandatory artifacts, headers already
# filled in and an empty Constitution Check to complete. Never overwrites a cycle.
# This skeleton is the MINIMUM shortcut; the full reference (with guidance) lives in
# the vendored templates under .specify/templates/ — if they diverge, they win
# (.specify/UPSTREAM.md, rule 2).
#
# Usage:  scripts/new-cycle.sh <NNN> <slug>
#         scripts/new-cycle.sh 007 vendor-spec-kit
set -euo pipefail

NNN="${1:-}"; SLUG="${2:-}"
if [[ -z "$NNN" || -z "$SLUG" ]]; then
  echo "usage: scripts/new-cycle.sh <NNN> <slug>" >&2
  exit 2
fi
[[ "$NNN" =~ ^[0-9]{3}$ ]] || { echo "error: NNN must have 3 digits (e.g. 007)." >&2; exit 2; }
[[ "$SLUG" =~ ^[a-z0-9-]+$ ]] || { echo "error: slug must be kebab-case (a-z 0-9 -)." >&2; exit 2; }

DIR="specs/${NNN}-${SLUG}"
DATE="$(date +%Y-%m-%d)"
mkdir -p "$DIR"

write_if_absent() {  # $1 = file, stdin = content
  if [[ -e "$1" ]]; then
    echo "exists (kept): $1"
  else
    cat > "$1"
    echo "created: $1"
  fi
}

write_if_absent "$DIR/spec.md" <<EOF
# Spec ${NNN} — <title>

- **Status**: Draft · **Lane**: <light|full|infra> · **Date**: ${DATE}
- **Origin**: <where this demand comes from>

## What and why
<business value; the problem>

## Functional requirements
- **FR1**: <WHEN ... THE SYSTEM SHALL ...>

## Out of scope
- <...>

## Acceptance criteria (DoD)
- [ ] <verifiable check — see the verifiable-dod skill>

## Clarify
1. <ambiguity to resolve before the plan>
EOF

write_if_absent "$DIR/plan.md" <<EOF
# Plan ${NNN} — <title>

- **Spec**: \`spec.md\` · **Lane**: <...> · **Date**: ${DATE}

## Constitution Check (governance/principles.md)
<fill in I–VIII — see the constitution-check skill>

| Principle | Compliance |
|---|---|
| I. Spec-driven |  |
| II. Human-governed orchestration |  |
| III. Reversibility / risk gates |  |
| IV. Test-first / verifiable DoD |  |
| V. Context economy / boundary |  |
| VI. Living artifacts |  |
| VII. Light governance / YAGNI |  |
| VIII. Intelligible communication |  |

## How
<...>

## Verification (DoD)
<commands and expected output>
EOF

write_if_absent "$DIR/tasks.md" <<EOF
# Tasks ${NNN} — <title>

## Verification first
- [ ] T0 — define the DoD checks

## Implementation
- [ ] T1 — <...>

## Gate
- [ ] Tn — DoD green -> guardian verdict -> human merge gate
EOF

write_if_absent "$DIR/qa-report.md" <<EOF
# QA report ${NNN} — <title>

- **Date**: ${DATE} · **Lane**: <...> · **Verdict**: <pending>

## Fitness functions (DoD)
| Check | Expected | Result |
|---|---|---|
|  |  |  |

## Requirement coverage
- FR1: <...>

## Pending gate
- dev -> main promotion awaits human approval.
EOF

echo "cycle ${NNN}-${SLUG} ready in $DIR/"
