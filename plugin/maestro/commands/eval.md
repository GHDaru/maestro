---
description: Runs an evaluation case against its target in fresh context and records the baseline. Use when a case is pending, when its target changed, or when an agent seems to have regressed.
---

Run the evaluation case named in the argument (a directory under `evals/`) and **record
what happened**. The deterministic health of the corpus is `scripts/check-evals.sh`; this
command is the part that needs a model in the loop.

## Before anything — two pre-flight checks, in this order

1. Run `scripts/check-evals.sh` and read the line for this case. If it is structurally
   broken, fix the case first — evaluating against loose assertions produces a green that
   means nothing.
2. **Reproduce the premise.** The fixture claims a symptom; confirm the symptom actually
   occurs from the inputs shown. A fixture whose premise does not hold tests the author's
   imagination, not the target — and two of the first fixtures written here failed this,
   both caught by the agents under evaluation rather than by their author (anti-pattern 20).
   Also read `case.md` for leaked conclusions: if the prose already states what the target is
   supposed to find, the run proves nothing. Record the outcome in `Premise-checked:`.

## Running it

1. **Read `case.md`** and take the `Target:` file as the instruction under evaluation. Read
   nothing else about how it "should" behave — the case is the whole input.
2. **Answer the `Question:` in fresh context**, obeying the target as written. Whoever runs
   the case must not be the agent under evaluation (Theorem 2: whoever executes does not
   verify). In practice: dispatch it to a subagent whose instruction is the target file, or
   run it in a cleared session. Do not carry this file's expectations into that context —
   knowing the answers invalidates the run.
3. **Read `expect.md` only after the answer exists.** Judge assertion by assertion:
   - every `MUST-FIND:` — is that substance present? Wording does not matter, substance does.
   - every `MUST-NOT-CLAIM:` — did the answer assert it anyway? One of these is a fail.

## Then ablate — this is not optional

A run where the target does well proves nothing on its own: the case may be measuring a
capability the target cannot lose. Run the case a second time against an **ablated target**
— the same instruction with the specific bullet the case's `Axis:` names removed, and
nothing else changed.

- The ablated target **fails** the case → the case discriminates on its declared axis.
  That failure is the `First-red`, and it is earned rather than staged.
- The ablated target **passes** → the case does not measure the target. Do not adjust the
  fixture until something goes red; that is fishing. Either the axis is over-determined
  (another rule produces the finding anyway) and the case should be **retired** with its
  reason, or the axis is wrong and needs rechoosing. Case 002 was retired exactly this way,
  after two fixtures and two ablations (anti-pattern 19).

Record the outcome in `Ablation:` either way.

## Recording it

Rewrite `baseline.md` with what was observed, never with what was hoped:

```
Date: <today>
Target-commit: <git log -1 --format=%h -- TARGET>
First-red: <date and the assertion that rejected an answer, or keep `pending`>
Verdict: <pass | fail> — <assertion by assertion>
```

Then state, in the body, which assertions passed and which failed, with the quoted fragment
of the answer that decided each one. An assertion judged with no quotable evidence is a
judgement about a judgement.

## The rule that matters most

**`First-red` only moves off `pending` when the case has genuinely rejected an answer.** If
the first run passes everything, the case is not proven — it is untested. Weaken a candidate
answer deliberately (drop the finding the case exists to catch) and confirm the case catches
it. A case that accepts the weakened answer has assertions that are too loose: tighten them
and say so in `baseline.md`.

A run that only shows the agent doing well proves nothing. That is the second law:

```
A CHECK YOU HAVE NEVER SEEN COMPLAIN IS NOT A CHECK — IT IS A HOPE
```

## What this command does not do

It does not approve or block a cycle. It produces a verdict per assertion; reading the
verdict and deciding what it means stays with the human (principle II, axiom A2).
