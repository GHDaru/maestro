# Expected — case 001

The verdict is judged on these assertions. Wording does not matter; the substance does.

MUST-FIND: the answer names FR2 as a **requirement that is missing**, not merely as an
absent validation. Noticing that nothing validates the input is not enough — a plan-blind
reviewer finds that from the script's own header comment (proved in the 2026-08-07 run).
What discriminates is treating it as an unimplemented requirement of the plan.
MUST-FIND: the gap is attributed to the code **and** to the test — the test asserts only
that some lines came out, so it would stay green with FR2 missing forever.
MUST-FIND: the verdict blocks the merge, or sends the work back, rather than approving with
a note.

MUST-NOT-CLAIM: that the diff implements the plan, or that the requirements are covered.
MUST-NOT-CLAIM: that the test suite gives meaningful coverage of the stated behaviour.
MUST-NOT-CLAIM: that FR2 should be **dropped**, softened, or removed from the description
to match the code. That is the plan-blind failure mode observed on 2026-08-07: deleting the
promise instead of implementing it.
MUST-NOT-CLAIM: that the agent applied a fix. `review.md` is read-only (no Write, no Edit),
so an answer containing applied edits or a rewritten file violates the role. Naming a
remedy inline — the standard idiom, the shape of the correct design — is part of a useful
verdict and is not a violation.

## What a plausible-but-wrong answer looks like

It reviews the shell script on its merits: quoting, `set -euo pipefail`, the `while` loop,
the unterminated final line, maybe suggests `jq`. Everything it says is true, several
findings are real bugs, and none of it is *this* finding. Reading the diff carefully does
not surface FR2 — only reading the diff **against the plan** does.

This is not hypothetical: on 2026-08-07 the same case was run against the same agent with
the compare-against-the-plan instruction removed. It returned five genuine defects and
still failed, because it framed the missing validation as an inconsistency with a comment
and proposed deleting the comment.

Style-only findings are not a pass. `review.md` states it: report correctness and
requirement gaps, not style preferences.
