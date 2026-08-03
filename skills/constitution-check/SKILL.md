---
name: constitution-check
description: Produces the Constitution Check table (Maestro Principles I–VIII) inside a plan.md, decides when a principle counts as violated and what to do with the violation. Use it when writing or reviewing a plan.md, when opening a cycle, or whenever a plan must be checked against Maestro's non-negotiable principles.
---

# Constitution Check

## Iron Law

```
NO PLAN WITHOUT THE EIGHT ROWS — ONE PER PRINCIPLE, NONE EMPTY
```

**Violating the letter of this rule violates its spirit.** This is NOT an excuse:
- "this principle obviously does not apply" — then write ✅ with the sentence saying why;
  the row stays.
- "the cycle is small" — a small cycle with a hidden violation becomes large debt.

Every Maestro `plan.md` carries a table checking the plan against the **eight non-negotiable
principles** (`docs/governance/principles.md`). This skill standardises that table.

## When to fire

Writing or reviewing a `plan.md`; during `/speckit.plan`; before releasing a plan to tasks.

## Step by step

1. For **each** principle I–VIII write one row: `✅` (compliant) or `⚠️/❌` (tension or
   violation) plus **one sentence** of why. Never skip a principle — the table is always
   complete.
2. A principle counts as **violated** when the plan only works by **breaking it** (for
   example: a read-only agent would need `Write`; an irreversible decision without a human
   gate; a documentation artifact with no living counterpart). Discomfort is not violation;
   impossible-without-breaking is.
3. A real violation has **two exits, never "ignore"**:
   - **Rework** the plan so it does not violate (preferred); or
   - Record it under **Complexity Tracking**: which principle, why it is unavoidable here,
     and what makes it reversible or bounded. The human gate decides.
4. Close with the verdict: **"No violations."** or the list of what went to Complexity
   Tracking.

## The eight principles (anchor)

| # | Principle | Checking question |
|---|---|---|
| I | Spec-driven | Does it come from an approved spec? |
| II | Human-governed orchestration | Is the human **Accountable** preserved? |
| III | Reversibility / risk-proportional gates | Can it be undone? Is the gate proportional? |
| IV | Test-first / verifiable DoD | Is success autonomously verifiable? |
| V | Context economy / cut by boundary | Is each slice narrow and cut along a boundary? |
| VI | Living artifacts | Do docs and code evolve together, in the same pull request? |
| VII | Light governance / YAGNI | Only what is needed now, no speculative rule? |
| VIII | Intelligible communication | Every acronym expanded on first occurrence? |

## Example

> III. Reversibility / risk gates — ✅ **narrow tools** mean a smaller risk surface per
> agent (read-only wherever it fits).

**Consumed by:** `plan-architect` (produces it), `process-guardian` (verifies it).
