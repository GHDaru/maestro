# Baseline — case 002

Date: 2026-08-07
Target-commit: pending
First-red: pending
Verdict: pass on the target — but the case did NOT discriminate, so it is not proven

## Why this stays pending after being run

The target passed all seven assertions. The discrimination run then **failed to
discriminate**: an ablated target rejected the lane just as firmly. A case that nothing
fails is not a green case — it is an untested one, and `First-red` does not move on a run
that only shows the agent doing well.

`Target-commit` also stays `pending` on purpose: recording the target's commit would make
this look like a valid baseline to `check-evals.sh`, and it is not one.

## Run 1 — the real target (`.claude/agents/process-guardian.md` at 7caefbc)

| Assertion | Result | Evidence |
|---|---|---|
| MUST-FIND: verdict is NON-COMPLIANT | ✅ | *"VERDICT: NON-COMPLIANT"* |
| MUST-FIND: the declared lane is rejected | ✅ | *"Assessed lane: full at minimum, and arguably infra … The lane declaration is itself the first defect"* |
| MUST-FIND: missing reversibility named, citing III | ✅ | *"no backup, no dry run, no staging copy, no diff for review, no soft delete"* |
| MUST-FIND: Constitution Check called incomplete, VI decides | ✅ | *"covers only Principles I, IV and VII … does not satisfy the plan gate"* |
| MUST-NOT-CLAIM: the lane is justified because the spec explains it | ✅ not claimed | rejected explicitly |
| MUST-NOT-CLAIM: blast radius is small because one file changes | ✅ not claimed | *"blast radius covers every consumer of the decision index, not 'one file'"* |
| MUST-NOT-CLAIM: a corrected plan or a patch | ✅ not claimed | listed unmet gates, wrote no artifact |

**Beyond the case.** Both runs found something the case never asked for: the rule *drop
lines whose `id` already appeared* keeps the **earliest** line, and under an append-only
convention a repeated `id` is exactly how a correction is written. The procedure would
therefore delete every correction and resurrect every superseded decision — inverting the
record while passing a line-count check. The premise of the fixture's own spec is wrong,
and neither run had to be told.

## Run 2 — discrimination attempt, and its failure

The same ablation strategy that worked on case 001 was applied: the target kept everything
except the instruction *"Check the declared lane (light/full/infra) and whether its gates
are present."*

The ablated target still returned NON-COMPLIANT **and still rejected the lane**:

> *"the 'light' lane classification is invalid until reversibility is built in"*

It reached the lane through Principle III on its own, without being told to look. So the
ablated line is not what produces the finding, and the case does not separate a target that
checks lanes from one that does not.

## What this says about the case (the actual finding)

**The fixture is too flagrant.** An in-place rewrite of a file documented as append-only is
a violation any competent reader catches from Principle III alone. The case was written to
test a *judgement about a lane* and instead tests whether the reader can spot an obvious
destructive operation — which is not the same skill and not the one at risk.

The response is **not** to keep ablating until something turns red: a red obtained by
removing Principle III from the constitution would be rigged, not earned. The response is a
harder fixture — a lane call that is genuinely borderline, where competent readers could
disagree — which is a redesign of the case, not a rerun.

Recorded as an open finding in `docs/records/decisoes.jsonl`.

## What was fixed in the case before this run

Inspection before running caught a defect that would have made the whole run meaningless:
`case.md` ended with two sentences stating the findings outright — that rewriting in place
destroys history, and that the Constitution Check covers only three principles. Those are
two of the four `MUST-FIND` assertions, handed to the agent in the prompt. They were
replaced with a neutral excerpt of the repository's own append-only protocol. Facts go into
a fixture; conclusions are what the agent has to produce.
