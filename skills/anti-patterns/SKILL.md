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

## Process (continued)

17. **A ceremony with no trigger** — a rule that says "do X regularly" and leaves *when* to
    memory. The retrospective, the highest-return ceremony of the method, had no clock for
    thirty-three cycles: it happened when somebody noticed. **Antidote**: every recurring
    ceremony declares its trigger as a **measurable condition** (open findings, cycles
    elapsed, size of a queue) and a check fails when the condition is met and the ceremony
    did not happen. *(cycle 034, from the finding of cycle 027.)*

## Verification (continued)

18. **Mass rename by text substitution** — a global search and replace matches the
    *pattern*, not the *target*: renaming `operating-model.md` also rewrote
    `0004-operating-model.md` (a file that was never renamed) and turned a research path into
    one that does not exist, in fourteen files. **Antidote**: after any rename touching more
    than a handful of files, run a link check over the **whole repository** — not only over
    the pages that get published, because that is where the silent breakage hides.
    *(cycle 034, from the finding of cycle 033.)*

19. **An evaluation case proved by nobody failing it** — a case the target passes looks like
    evidence and is not: it may be measuring a capability the target cannot lose. Case 002
    was written twice, and both times an **ablated** target — the same agent minus the
    instruction the case existed to test — passed identically. The finding was
    over-determined: another principle produced it without the instruction. **Antidote**: a
    case declares the **axis** it separates, and a pass counts only once an ablation on that
    axis has been seen failing. No ablation, no baseline.
    *(cycle 041, from the finding of cycle 040.)*

20. **A fixture that carries its own verdict, or whose premise was never checked** — the
    input handed to the target is not neutral. One version of case 002 ended by stating two
    of its own four required findings in prose; its replacement asserted that a gate flags a
    line the gate's pattern does not match. Both defects were found by the agents under
    evaluation, not by the author. **Antidote**: facts go into a fixture, conclusions come
    out of the target — and before any run, reproduce the premise. A fixture whose symptom
    does not reproduce tests the author's imagination. *(cycle 041, from cycle 040.)*

21. **`grep -q` ending a pipe under `pipefail`** — `grep -q` exits at the first match, the
    upstream command takes SIGPIPE, and `set -o pipefail` turns a successful match into a
    failed pipeline. The condition then reads as "no match", silently and always. It killed
    `check-cycle.sh` once, and `retro.sh` a second time — where it reported every cycle from
    011 on as an open gate, for twenty-nine cycles. **Antidote**: capture once into a
    variable and match against that (`grep -q … <<<"$var"`); never end a pipe in `grep -q`
    inside a condition. *(cycle 041 — the second occurrence is what made it a rule.)*

## Process (continued)

22. **The installed method as a lossy copy of the method** — the executor follows the
    artifact it is given, faithfully, and the artifact is a subset. On a companion repository
    a `plan.md` listed the implementation steps and stopped at "docs and fitness green": the
    closing tail (independent review, security, human gate) lived in the spec and in working
    memory. Context compaction promoted the truncated version to source of truth, and the
    agent drove straight to a pull request — obeying perfectly. In this repository the same
    defect measured **35 of 40** cycles whose `tasks.md` had lost the human gate the template
    carries, and a catalogue of conditional artifacts that shipped in a document the installer
    never copies. Omission is invisible: it violates nothing you can see. **Antidote**: every
    mandatory step exists as a machine-readable token in the artifact the executor consumes,
    a conditional artifact is **declared** rather than merely absent (`=yes`/`=no` with a
    reason), and a gate compares the two. *(cycle 042, from a companion repository's cycle 029.)*

23. **A new door, and the old guard never told** — a cycle grants a new power or opens a new
    channel, and the gate that watched the old one is left reading half the world. It reports
    green, and green now means "I did not look over there". The book engine gained a second
    publication channel and `check-boundary.sh` kept reading only the first: a toolkit-owned
    file went out to the reader-facing site with the boundary gate saying all clear — the
    exact failure that script exists to prevent, arriving through the door it was not
    watching. In the same cycle the page-collision map stayed keyed on declared items only,
    so a material named `index.html` overwrote the hand-maintained cover while the build
    printed a success line. **Antidote**: when a change adds a way in, name every gate that
    guards the old way and extend it in the same cycle — then prove the extension by
    mutation. Ask it out loud: *what was this gate's world, and did it just get bigger?*
    *(cycle 054; both found by independent review before merge.)*

## How to use it

- **Designing**: walk the catalogue as a negative checklist (is any item present?).
- **Reviewing**: name the anti-pattern by number — "this is number 4" shortens the argument.
- **In the retrospective**: a new recurring mistake becomes a new entry here, with the cycle
  it came from.

**Sources:** retrospectives of cycles 001–008 and 017–020 · the "workflow slop" catalogue of
[maestro-02/sharpdeveye](https://github.com/GHDaru/maestro-02) (adapted) · Principles I–VIII.
