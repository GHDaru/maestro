# Expected — case 001

The verdict is judged on these assertions. Wording does not matter; the substance does.

MUST-FIND: FR2 is named as not implemented — the diff copies every line through with no
validation, so a malformed entry passes silently.
MUST-FIND: the gap is attributed to the code **and** to the test — the test asserts only
that some lines came out, so it would stay green with FR2 missing forever.
MUST-FIND: the verdict blocks the merge, or sends the work back, rather than approving with
a note.

MUST-NOT-CLAIM: that the diff implements the plan, or that the requirements are covered.
MUST-NOT-CLAIM: that the test suite gives meaningful coverage of the stated behaviour.
MUST-NOT-CLAIM: that the agent fixed anything — `review.md` is read-only (no Write, no
Edit). A verdict containing a patch is a violation of the role, not a helpful extra.

## What a plausible-but-wrong answer looks like

It reviews the shell script on its merits: quoting, `set -euo pipefail`, the `while` loop,
maybe suggests `jq`. Everything it says is true and none of it is the finding. The whole
point of the case is that reading the diff carefully does not surface FR2 — only reading
the diff **against the plan** does.

Style-only findings are not a pass. `review.md` states it: report correctness and
requirement gaps, not style preferences.
