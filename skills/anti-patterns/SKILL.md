---
name: anti-patterns
description: Catalogue of what NOT to do when one human runs many agents — the recurring mistakes observed in our own retrospectives and in the ecosystem. Use it when designing a flow, prompt or orchestration, when reviewing an agent's work, or when something "works but smells wrong" and you need to name the anti-pattern before fixing it.
---

# Anti-patterns (the "do not do this" catalogue)

## Iron Law

```
NAME THE ANTI-PATTERN BEFORE FIXING IT
```

**Violating the letter of this rule violates its spirit.** Fixing without naming repairs the
symptom once; naming it ("this is number 4") links to the catalogue, shortens the
conversation and feeds the retrospective — which decides whether it becomes a rule.

A positive rule shows the path; an anti-pattern marks the cliff. This catalogue is **alive**:
every new anti-pattern enters through a retrospective (an observed recurring mistake), never
through speculation.

## Context

1. **Context dump** — pasting the whole codebase or document into the prompt. Slice by role
   or task (Principle V); report the saving when possible.
2. **Tribal context** — intent that exists only in the operator's head. If it is not in the
   spec, the agent does not know it — and neither does the next human.
3. **Lazy reset** — `/clear` is not always the answer; resetting too much loses learning,
   resetting too little accumulates noise. The trigger is the role changing, not the turn.

## Orchestration

4. **Multi-agent for a single-agent problem** — orchestration costs handoffs and
   reconciliation. Use the **least autonomy that solves it**.
5. **Blind retry** — repeating the same prompt expecting a different result. If it failed
   twice, the problem is the prompt, the context or the task — change something first.
6. **Author as reviewer** — the agent that wrote the code approving its own work. Review
   happens in **fresh context**, always.

## Quality

7. **"Seems to work"** — delivering without executable evaluation. Prove it, do not claim
   it: green tests, clean build, evidence attached.
8. **Happy path only** — no failure test, no error handling. Minimum: one happy plus one
   failure test per use case.
9. **Gameable numeric target** — "coverage ≥ X%" invites useless tests. The criterion is
   verifiable behaviour, not a percentage.

## Process

10. **Silent scope change** — the agent "takes the opportunity" to refactor. Small, focused
    diff; a larger problem becomes a record, not a detour.
11. **Ceremony theatre** — a process that changes no decision (a stand-up of one, an endless
    backlog). If a gate never rejects anything, it is theatre — prune it (YAGNI).
12. **Fixing the same thing twice** — a recurring fix that never became a versioned rule.
    That is what the retrospective is for; repeating a fix is a process failure, not an
    agent failure.

## Verification

13. **A check that measures the proxy, not the fact** — the command passes but proves
    something else. Symptoms: it matches the *text* instead of the artifact (`grep -l
    companion` finds the word written on the page, not the injected widget); it counts
    *lines* instead of items (`grep -c "https://"` reports 5 where there are 6 sources); it
    confirms that a *section exists* instead of that it *was updated* ("heuristic evaluation
    present" ≠ "revisited with a new date"). **Antidote**: prove the check **failing** before
    trusting it — if you have never seen the check complain, you do not know what it measures
    (see the `verifiable-dod` skill).

## Process (continued)

14. **A finding that dies as a "candidate"** — recording "candidate rule" in a report and
    never running the retrospective. The `retro → versioned rule` loop only exists if it is
    **run**; a note without the ceremony is silent debt.
15. **A planning artifact that freezes** — a roadmap or map that stops being updated while
    the cycles move on. It becomes fiction: it describes a project that is no longer yours
    (Principle VI — an artifact is alive or dead, there is no middle ground).

## Verification (continued)

16. **A gate that covers one format and ignores its siblings** — the check is born for one
    case and never enumerates the rest of the family. The site's link gate validated
    `<a href>` and ignored `<img src>` (a broken image passed green); once fixed, it still
    ignored an unrewritten `href` ending in `.md`. **Antidote**: when writing a gate, list
    **the whole family** it guards — in HTML, every attribute that becomes a request
    (`href`, `src`, `srcset`, `poster`); in a schema, every required field; in a directory,
    every published extension — and prove the gate failing **for each** listed format.
    *(cycle 020, third recurrence of number 13.)*

## How to use it

- **Designing**: walk the catalogue as a negative checklist (is any item present?).
- **Reviewing**: name the anti-pattern by number — "this is number 4" shortens the argument.
- **In the retrospective**: a new recurring mistake becomes a new entry here, with the cycle
  it came from.

**Sources:** retrospectives of cycles 001–008 and 017–020 · the "workflow slop" catalogue of
[maestro-02/sharpdeveye](https://github.com/GHDaru/maestro-02) (adapted) · Principles I–VIII.
