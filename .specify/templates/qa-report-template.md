# QA report NNN — [TITLE]

- **Date**: [YYYY-MM-DD] · **Lane**: [light|full|infra] · **Verdict**: ✅ COMPLIANT | ❌ NON-COMPLIANT

## Fitness functions (DoD)

<!-- Every row is a (command, expected, REAL result) triple. "Prove it, don't claim it":
     the result is copied from the run, never assumed. A check nobody has seen fail is not
     yet a check (second law of the verifiable-dod skill). -->

| Check | Expected | Result |
|---|---|---|
| `[command]` | [expected] | [real] ✅/❌ |

## Closing tail — the evidence

<!-- One entry per TAIL token declared in `tasks.md` that is not `n/a`. The token must appear
     here: `scripts/check-conformance.sh` requires it, because a ticked box in tasks.md only
     proves that somebody ticked a box. What goes here is what was OBSERVED — the verdict,
     the command and its output — never a restatement of the intention. -->

- **TAIL:review** — [who reviewed, in which fresh context, the verdict, and what was done
  with the findings]
- **TAIL:security** — [the pass that was run and its result, or the `n/a` reason mirrored
  from `tasks.md`]
- **TAIL:mutation** — [each gate this cycle created or changed, broken on purpose: the
  mutation, the command, and the refusal it printed. Or the `n/a` reason — but the gate
  reads the diff, not the sentence]
- **TAIL:gate** — [what awaits the human, or the recorded `gate-main-<sha>`]

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
