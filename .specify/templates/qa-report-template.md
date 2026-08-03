# QA report NNN — [TITLE]

- **Date**: [YYYY-MM-DD] · **Lane**: [light|full|infra] · **Verdict**: ✅ COMPLIANT | ❌ NON-COMPLIANT

## Fitness functions (DoD)

<!-- Every row is a (command, expected, REAL result) triple. "Prove it, don't claim it":
     the result is copied from the run, never assumed. A check nobody has seen fail is not
     yet a check (second law of the verifiable-dod skill). -->

| Check | Expected | Result |
|---|---|---|
| `[command]` | [expected] | [real] ✅/❌ |

## Requirement coverage

- **FR1**: [delivered? where?]
- **FR2**: [...]
- **Out of scope respected**: [what was left out, per the spec]

## Findings and fixes inside the cycle

<!-- A defect found DURING the cycle goes here with its root cause — it is evidence that the
     verification worked. Silencing a finding is worse than having one. -->

## Lesson for the retrospective

<!-- Recurring mistake? Name it. If this is the second or third occurrence, it MUST become a
     versioned rule now — writing "candidate" and moving on is anti-pattern 14. -->

## Pending gate

- [what awaits a human decision, or "none"]
