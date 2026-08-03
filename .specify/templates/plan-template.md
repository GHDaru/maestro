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

## How

<!--
  The HOW: architecture, cutting by boundary (bounded context — which makes parallel work
  safe), decisions (an architectural decision becomes an ADR, immutable). For CODE features,
  also produce the data model and contracts; for docs work they do not apply.
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
