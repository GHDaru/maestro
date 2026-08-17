#!/usr/bin/env bash
# new-cycle.sh — creates the skeleton of a Maestro cycle (a spec).
# Standardises specs/NNN-slug/ with the four mandatory artifacts, headers already
# filled in and an empty Constitution Check to complete. Never overwrites a cycle.
# This skeleton is the MINIMUM shortcut; the full reference (with guidance) lives in
# the vendored templates under .specify/templates/ — if they diverge, they win
# (.specify/UPSTREAM.md, rule 4).
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
<!-- No checkboxes: this states what must hold; whether it held is the qa-report's job. -->
- <verifiable criterion — see the verifiable-dod skill>

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

## Artifacts of this cycle (declare all five — silence is not a decision)

<!-- Read by scripts/check-conformance.sh. Declaring =yes means the file MUST exist here.
     What each one is for: docs/governance/artifacts.md -->

| Artifact | Declaration | Why |
|---|---|---|
| \`research.md\` | \`ART:research=no\` | <technical unknown to resolve first?> |
| \`data-model.md\` | \`ART:data-model=no\` | <entities and relations — code features> |
| \`contracts/\` | \`ART:contracts=no\` | <interfaces: routes, ports, events> |
| \`checklist.md\` | \`ART:checklist=no\` | <quality checklist for this cycle> |
| \`ux-design.md\` | \`ART:ux-design=no\` | <touches a screen? then NOT optional> |

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

## Closing tail — MANDATORY, one line each, never delete
<!-- TICK ONLY WHILE WRITING THE EVIDENCE, never in advance: the box records what happened.
     Do not delete a line to say it does not apply: write \`n/a: <reason>\` on it.
     check-conformance.sh requires the evidence of every non-n/a step in qa-report.md. -->
- [ ] TAIL:review — independent review in fresh context, by whoever did not execute
- [ ] TAIL:security — security pass proportional to the risk class
- [ ] TAIL:mutation — every gate created or changed here, broken on purpose and seen refusing
- [ ] TAIL:gate — DoD green -> guardian verdict -> human merge gate (not delegable)
EOF

write_if_absent "$DIR/qa-report.md" <<EOF
# QA report ${NNN} — <title>

- **Date**: ${DATE} · **Lane**: <...> · **Verdict**: <pending>

## Fitness functions (DoD)
| Check | Expected | Result |
|---|---|---|
|  |  |  |

## Closing tail — the evidence
<!-- One entry per non-n/a TAIL token. What was OBSERVED, never the intention restated. -->
- TAIL:review — <who reviewed, fresh context, verdict, what was done with the findings>
- TAIL:security — <the pass and its result, or the n/a reason mirrored from tasks.md>
- TAIL:mutation — <the gate broken on purpose, the command, the refusal it printed>
- TAIL:gate — <what awaits the human, or the recorded gate-main-<sha>>

## Requirement coverage
- FR1: <...>

## Pending gate
- dev -> main promotion awaits human approval.
EOF

echo "cycle ${NNN}-${SLUG} ready in $DIR/"
