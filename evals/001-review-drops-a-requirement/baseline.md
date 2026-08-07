# Baseline — case 001

Date: 2026-08-07
Target-commit: 7caefbc
First-red: 2026-08-07 — the ablated target failed MUST-FIND #1: it found the missing
validation but never framed it as a requirement gap, and proposed dropping the claim
Verdict: pass — 6 of 6 assertions, with two wording defects found in the case itself
Ablation: 2026-08-07 — target minus the compare-against-the-plan instruction FAILED the case
Premise-checked: yes — the fixture diff genuinely implements FR1 and omits FR2; verified by
reading the script, which has no validation of any kind

## Run 1 — the real target (`.claude/agents/review.md` at 7caefbc)

| Assertion | Result | Evidence from the answer |
|---|---|---|
| MUST-FIND: FR2 named as not implemented | ✅ | *"FR2 … is entirely absent, in both the code and the tests"* |
| MUST-FIND: gap attributed to code **and** test | ✅ | *"there is no malformed-input test at all, so FR2 has zero coverage"* |
| MUST-FIND: verdict blocks the merge | ✅ | *"Changes required — back to `dev-implementer`. Not mergeable."* |
| MUST-NOT-CLAIM: the diff implements the plan | ✅ not claimed | *"Roughly half the plan is implemented"* |
| MUST-NOT-CLAIM: the tests give meaningful coverage | ✅ not claimed | *"a script that printed `hello` would pass it"* |
| MUST-NOT-CLAIM: the agent fixed anything | ⚠️ borderline | contained one inline remedy: the standard `read` guard idiom |

It also produced a finding the case did not anticipate and which is better than what the
case asks for: that emitting inside the read loop makes FR2 **unimplementable without a
redesign**, because lines 1..N-1 are already on stdout by the time line N is rejected. A
fix at the current structure would look green and still violate the requirement.

## Run 2 — discrimination, against an ablated target

Rather than write a strawman answer, the same case was run against the **same agent minus
the instruction to compare the diff with the plan** (and with the plan withheld). Everything
else identical. This tests the axis the case exists for: reviewing *against the plan* versus
reviewing *the code*.

The ablated target produced a strong code review — five real defects, including two the
real run also found — and **failed the case**:

- it did notice there is no validation, but attributed it to the script's own header comment
  rather than to a requirement, and offered as a remedy *"drop the claim from the
  description so callers do not rely on a guarantee that is not enforced"*. That is the
  precise inversion of FR2: deleting the promise instead of implementing it.
- FR2 is never named, and nothing in the verdict says a required behaviour is missing.

So the case discriminates, and it discriminates on substance rather than vocabulary: the
weaker target was not sloppier, it was *plan-blind*, and the case caught exactly that.

## What running it changed in the case

Two wording defects, both found only by running:

1. **MUST-FIND #1 conflated two different things** — "FR2 is named as not implemented"
   (which discriminates) and "no validation, so a malformed entry passes silently" (which
   does not: the plan-blind target found that too). Tightened so the discriminating part is
   the assertion.
2. **MUST-NOT-CLAIM #3 was stricter than the role it protects.** `review.md` says *judge, do
   not fix* — meaning do not apply edits. Both runs named a one-line standard idiom inline,
   which is a useful verdict, not a role violation. Rewritten to forbid what is actually
   forbidden: applied edits or a rewritten file.

Both edits loosen nothing about what the case demands; they move the demand onto the part
that separates a right answer from a plausible one.
