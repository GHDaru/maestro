# Plan NNN — [TITLE]

- **Spec**: `spec.md` · **Lane**: [full|infra] · **Date**: [YYYY-MM-DD]

## Constitution Check (governance/principles.md)

<!--
  MANDATORY and COMPLETE — one row per principle, never skip one (skill constitution-check).
  ✅ = compliant (one sentence of why). Violated = the plan ONLY works by breaking the
  principle; discomfort is not violation. A real violation → rework the plan OR record it in
  Complexity Tracking (which principle, why it is unavoidable, what makes it reversible) →
  the human gate decides.
-->

| Principle | Compliance |
|---|---|
| I. Spec-driven | [does it come from an approved spec?] |
| II. Human-governed orchestration | [is the human Accountable preserved?] |
| III. Reversibility / risk gates | [can it be undone? is the gate proportional?] |
| IV. Test-first / verifiable DoD | [is success autonomously verifiable?] |
| V. Context economy / boundary | [narrow slices, cut along a boundary?] |
| VI. Living artifacts | [docs and code in the same pull request?] |
| VII. Light governance / YAGNI | [only what is needed now?] |
| VIII. Intelligible communication | [acronym expanded on first occurrence; readable by someone arriving today?] |

**[No violations. | Complexity Tracking: ...]**

## Artifacts of this cycle (declare all five — silence is not a decision)

<!--
  MANDATORY. Every conditional artifact is DECLARED, never merely absent. An omission
  violates nothing visibly, which is how a plan quietly becomes a lossy copy of the method
  (anti-pattern 22): the executor follows the plan faithfully, and the missing step produces
  no symptom. "Does not apply, because X" is auditable; silence is not.

  The token is machine-readable so the check survives translation and rewording —
  `scripts/check-conformance.sh` reads it. Declaring `=yes` means the file MUST exist in
  this cycle directory. What each artifact is for: `docs/governance/artifacts.md`.
-->

| Artifact | Declaration | Why |
|---|---|---|
| `research.md` | `ART:research=no` | [a technical unknown to resolve before deciding? if none, say so] |
| `data-model.md` | `ART:data-model=no` | [entities and their relations — code features] |
| `contracts/` | `ART:contracts=no` | [interfaces between parts: routes, ports, events] |
| `checklist.md` | `ART:checklist=no` | [a quality checklist specific to this cycle] |
| `ux-design.md` | `ART:ux-design=no` | [**touches a screen? then it is not optional** — semantic role before component] |

## How

<!--
  The HOW: architecture, cutting by boundary (bounded context — which makes parallel work
  safe), decisions (an architectural decision becomes an ADR, immutable).
  Infra lane: put backup, dry run and rollback HERE (the reversibility block of §7).
-->

- [...]

## Verification (DoD)

<!-- The commands that prove the criteria of the spec, each with its expected result.
     The /dod command runs them; here you WRITE them (design time — skill verifiable-dod). -->

- `[command]` → [expected]

<!--
  GATE (not delegable): the plan is approved by a human before it becomes tasks.
  Handoff: plan-architect → (approval) → tasks → dev-implementer.
-->
