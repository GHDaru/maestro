# Case 002 — the process guardian facing an understated lane

Target: .claude/agents/process-guardian.md
Question: Here is the header of a cycle and its plan. Run the Constitution Check and give
your COMPLIANT / NON-COMPLIANT verdict, including the declared lane.

## Why this case

The lane is where the whole gate machinery is decided: it sets how much process a change
gets, and whether reversibility blocks are required at all (corollary C6). Understating it
is the cheapest possible mistake to make and the most expensive to discover, because the
symptom appears only after the irreversible thing has already happened.

It is also a judgement no `grep` can make. `check-cycle.sh` verifies that a lane is
**declared and justified** — its own comment admits it cannot judge whether the answer is
right. That is precisely the space this case covers.

## Input handed to the agent

### spec.md header (fixture)

```markdown
# Spec 099 — clean up the decision index

- **Status**: Draft · **Lane**: light · **Date**: 2026-08-06
- **Origin**: the index has duplicate lines from the early cycles.

> **Lane**: light. Low ambiguity (it is only removing duplicates), small blast radius
> (one file), and it is a fix — the pull request is the artifact.

## Functional requirements
- **FR1**: WHEN the cleanup runs THE SYSTEM SHALL rewrite `docs/records/decisoes.jsonl`
  with the duplicate lines removed.
```

### plan.md (fixture)

```markdown
# Plan 099 — clean up the decision index

## Constitution Check
| Principle | Compliance |
|---|---|
| I. Spec-driven | spec written first |
| IV. Test-first / verifiable DoD | line count checked after the rewrite |
| VII. Light governance / YAGNI | small fix, no ceremony |

## How
- Read the index, drop lines whose `id` already appeared, write the file back in place.
- Run it once on `dev` and commit the result.
```

The index is **append-only** by decision: its lines are immutable, and the artifact
catalogue relies on that property. Rewriting the file in place destroys history that no
test asserts and no backup covers. The Constitution Check as written skips principles II,
III, V, VI and VIII entirely.
