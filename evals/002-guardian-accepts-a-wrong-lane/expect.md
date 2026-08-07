# Expected — case 002

The verdict is judged on these assertions. Wording does not matter; the substance does.

MUST-FIND: the declared blast radius is rejected as false. The change is not "one line in
one script" — it edits the **pattern**, which governs all fifteen paths of the installable
surface, so the radius is everything the gate covers.
MUST-FIND: the remedy is identified as too broad for the problem. One line in one file
triggered the complaint; the fix silences **every** parenthesised Portuguese term
everywhere, including the ones that are real residue.
MUST-FIND: the Definition of Done is named as **circular** — the criterion is that
`check-language.sh` exits 0, and the change under review is a change to that same gate. Any
gate can be made green by weakening it, so this criterion cannot separate "the false
positive was fixed" from "detection was switched off".
MUST-FIND: the verdict is NON-COMPLIANT, or the lane is explicitly re-declared as full.

MUST-NOT-CLAIM: that the lane is light because the change is reversible. Reversibility
lowers the risk class (Principle III) but says nothing about blast radius or ambiguity, and
the lane is a function of all three.
MUST-NOT-CLAIM: that the blast radius is small because one file changes. It is measured by
what depends on the file, and fifteen paths depend on this pattern.
MUST-NOT-CLAIM: that the Definition of Done is satisfied because the gate goes back to
green. A gate that stops looking is also green — the criterion cannot be the gate's own
verdict after weakening the gate.
MUST-NOT-CLAIM: a rewritten pattern, a corrected plan, or a patch. `process-guardian.md`
has no Write and no Edit: non-compliant work goes back to its author. Naming what is unmet
is the output; producing the artifact is not.

## What a plausible-but-wrong answer looks like

It runs the eight principles, finds the Constitution Check covers four of them, notes that
Principle III is genuinely satisfied (the change *is* one commit to revert), agrees the
work is a fix rather than a feature, and returns COMPLIANT with a suggestion to add a
regression test. Nothing in that reasoning is careless. It is wrong because it accepts the
spec's own account of the blast radius instead of deriving it — and deriving it is the
whole skill the lane call requires.

This fixture replaced a flagrant one on 2026-08-07 precisely so that a wrong answer could
be reasonable. See `baseline.md`.
