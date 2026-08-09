# Spec NNN — [TITLE]

- **Status**: Draft · **Lane**: [light|full|infra] · **Date**: [YYYY-MM-DD]
- **Origin**: [where this demand comes from — Steward request, roadmap, retrospective, bug]

<!--
  LANE (operating model §3): the value of a spec ∝ ambiguity × blast radius × irreversibility.
  - light: the diff fits in one sentence → you do NOT need this spec (the pull request is the artifact).
  - full: ambiguous feature, contract, cross-feature change → this whole template.
  - infra: infrastructure, migration, deployment → ALWAYS full plus reversibility gates (§7).
  In doubt between light and full → full. Infra is never light.
-->

## What and why

[The problem and the business value. The WHAT and the WHY — never the HOW (that belongs to
the plan). The journey(s) served, if any.]

## Functional requirements

- **FR1**: [...]
- **FR2**: [...]

## Out of scope

<!-- As important as the scope: what this cycle does NOT do, so nobody "takes the chance". -->
- [...]

## Acceptance criteria (DoD)

<!--
  AUTONOMOUSLY VERIFIABLE (Principle IV; skill verifiable-dod):
  - Behaviour → EARS form: "WHEN <condition> THE SYSTEM SHALL <observable behaviour>"
    (becomes a test almost 1:1: condition = arrange/act, behaviour = assert).
  - Structure or invariant → (command, expected) pair: grep/ls/test with empty or non-empty
    output, or an exit code.
  - If you cannot answer "which command proves this?", the criterion is still vague — rewrite it.
  - Forbidden: gameable numeric targets ("coverage ≥ X%"), "it is clear", "it works well".

  NO CHECKBOXES HERE, ON PURPOSE. This section states what MUST HOLD; whether it held is
  recorded in `qa-report.md`, which is the artifact that owns that question. A checkbox
  invites ticking, and a box ticked before the work exists turns the criterion into a plan —
  four times in cycles 042 to 044, in two different tokens, by the same author with the same
  good intention. A form the method failed to offer is not a lapse of attention
  (Principle VI: never duplicate a function already served).
-->
- WHEN [condition] THE SYSTEM SHALL [observable behaviour].
- `[command]` → [expected: empty | = N | exit 0].

## Clarify

<!-- Ambiguity is NOT invented — it becomes a question for the Steward. Once resolved, record the answer here. -->
1. [question] → [answer or decision, once resolved]

<!--
  GATE (DoR — not delegable): this spec only becomes a plan after human approval.
  Handoff: spec-agent → (approval) → plan-architect.
-->
