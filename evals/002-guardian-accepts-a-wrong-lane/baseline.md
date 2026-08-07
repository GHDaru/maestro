# Baseline — case 002

Date: 2026-08-07
Target-commit: pending
First-red: pending
Verdict: not proven — two fixtures, two failed discrimination runs, and a factual defect
found in the second fixture by the ablated target

## Why this stays pending after a redesign

The case has now been written twice and run four times. Both fixtures were passed by the
real target **and by an ablated target**, so neither version separates a target that judges
lanes from one that does not. `Target-commit` also stays `pending` on purpose: filling it
would make `check-evals.sh` treat this as a valid baseline, and it is not one.

## Fixture v1 — flagrant (discarded 2026-08-07)

A destructive in-place rewrite of a file documented as append-only. Real target: 7 of 7.
Ablated target (same agent minus *"check the declared lane"*): rejected the lane just as
firmly, arriving at it through Principle III alone —

> *"the 'light' lane classification is invalid until reversibility is built in"*

Diagnosis: the violation was flagrant, so the case tested "spot an obvious destructive
operation" rather than "judge a lane".

## Fixture v2 — borderline (this run)

Rebuilt so that every surface signal honestly says *light*: a fix, one line, one file,
trivially reversible. The defect is that the edited line is a **gate's matching rule**, so
the blast radius is the fifteen paths the gate covers, not the diff.

**Real target** — 3 of 4 MUST-FIND, 4 of 4 MUST-NOT-CLAIM. It rejected the blast radius
(*"the correct unit of blast radius is the surface the changed component governs"*), called
the requirement over-general, and re-declared the lane as infra.

It failed the assertion demanding that the low-ambiguity premise be challenged — and on
inspection **the assertion was wrong, not the answer**. The agent examined the specific line
and concluded the gloss is legitimate, giving a reason the assertion had not anticipated:
the glossary line exists *to satisfy* Principle VIII, so the gate was penalising conformance
to the constitution. That assertion was replaced with one drawn from the fixture's own
structure rather than from any run: the Definition of Done is **circular**, because the
criterion is that the gate exits 0 and the change under review is a change to that gate.

**Ablated target** — same ablation as v1. Passed everything the real target passed: named
the blast radius over 14 target paths, named the circular Definition of Done in the
principle's own words, returned NON-COMPLIANT.

## What v2 proved instead — a finding about the toolkit, not the eval

Two fixtures, two ablations, same result: removing *"Check the declared **lane**"* from
`process-guardian.md` changes nothing. The lane finding is **over-determined** — Principle
III produces it without the instruction. That is evidence about the agent definition (the
bullet may be redundant), and it is the reason this case cannot be made to discriminate by
adjusting the fixture: there is no version of a wrong lane that Principle III does not
already catch.

## The defect the ablated target found in the fixture

Unprompted, it checked whether the premise even holds:

> *"On the flagged line … **no alternative in the quoted `PATTERN` matches**: `raia` is not
> in the alternation … Either the diagnosis is wrong … or the true alternation is unknown
> and the causal claim is simply unverified."*

It is right. The fixture asserts the gate flags that line, and the pattern shown does not
match it. So fixture v2 is **factually broken**, and the strong run did not catch it. Two
fixtures written by hand, two defects found by the agents being evaluated: in v1 the prose
stated the findings outright, in v2 the premise does not hold.

## Methodological hazard, recorded on purpose

`expect.md` was edited **after** seeing run 1 of v2. That is fitting the case to the answer
unless the change is defensible independently, and here it is: the replaced assertion was
factually wrong (it demanded a challenge to a premise that turned out to be true), and its
replacement is derivable from the fixture alone, with no run needed. Recording the hazard
because the next person editing an `expect.md` after a run will have a weaker excuse.
