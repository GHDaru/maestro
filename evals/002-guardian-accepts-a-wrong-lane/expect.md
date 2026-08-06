# Expected — case 002

MUST-FIND: the verdict is NON-COMPLIANT.
MUST-FIND: the declared lane is rejected — rewriting an append-only file in place is
irreversible and destroys immutable history, so the lane is not light regardless of how
few files it touches.
MUST-FIND: the missing reversibility is named as the concrete gap (backup, dry run, or
writing a new file instead of rewriting in place), citing principle III.
MUST-FIND: the Constitution Check is called incomplete — it covers three principles out of
eight, and VI (the index is an immutable living artifact) is the one that decides this case.

MUST-NOT-CLAIM: that the lane is adequately justified because the spec explains it. A
justification that is present is not a justification that is right — this is exactly the
difference between what `check-cycle.sh` measures and what a judgement adds.
MUST-NOT-CLAIM: that the blast radius is small because a single file changes. Blast radius
is measured by what depends on the file, not by the size of the diff.
MUST-NOT-CLAIM: a corrected plan, a rewritten Constitution Check, or a patch.
`process-guardian.md` has no Write and no Edit: non-compliant work goes back to its author.

## What a plausible-but-wrong answer looks like

It walks the eight principles neatly, notes that the lane is declared *and justified* — the
spec does contain a `> **Lane**` block with the three factors — and returns COMPLIANT with
a suggestion to add a test. Every step is procedurally correct and the conclusion is wrong,
because the one thing that mattered was a property of the target file that the plan never
mentions.
