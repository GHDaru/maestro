# Evaluations

The deterministic gates in `scripts/` measure what can be compared by equality: sections
present, links resolving, lists matching disk. They cannot measure a **judgement** — the
verdict of a review agent, the lane call of the process guardian, the trade-off in a plan.

This directory is where those judgements get a baseline. It exists because of **Theorem 7**
([axioms](../docs/governance/axioms.md)): where output is not comparable by equality, the
criterion needs a recorded baseline, not attentive reading.

## Anatomy of a case

A case lives in `evals/<NNN-slug>/` and is three text files, one question each.

| File | Question it answers | Required fields |
|---|---|---|
| `case.md` | what is handed to the agent | `Target:` (a path that exists), `Question:`, `Axis:` |
| `expect.md` | what separates a right answer from a plausible one | ≥1 `MUST-FIND:`, ≥1 `MUST-NOT-CLAIM:` |
| `baseline.md` | what was actually observed, and when | `Date:`, `Target-commit:`, `First-red:`, `Verdict:`, `Ablation:`, `Premise-checked:` |

Two of those fields carry the whole design.

**`MUST-NOT-CLAIM` is not decoration.** A case with only `MUST-FIND` passes on any verbose
answer that happens to mention the right words. The negative assertion states what a wrong
answer would say — an approval that should not have been given, a completeness that is not
there. Without it the case does not discriminate, and `check-evals.sh` refuses it.

**`First-red` is the second law, as a field.** Until somebody has watched this case reject
an answer, it is a hope, not a check. A case whose `First-red` is `pending` fails the gate
on purpose, and says so out loud.

**`Axis` and `Ablation` exist because a pass is not evidence.** The axis names the
capability the case claims to separate; the ablation is the same target with exactly that
capability removed. If the ablated target passes too, the case is measuring something the
target cannot lose, and no amount of rewriting the fixture will fix it — the honest move is
to retire the case with its reason (`Status: retired` + `Retired-because:`), which the gate
prints and counts rather than hides. Case 002 was retired that way after two fixtures and
two ablations.

**`Premise-checked` exists because fixtures lie.** Two of the first fixtures written here
were defective — one stated its own findings in prose, the other claimed a symptom its
inputs do not produce — and both defects were found by the agents under evaluation, not by
their author.

## Running one

The gate is deterministic and free:

```bash
scripts/check-evals.sh      # structure · target exists · assertions discriminate · baseline fresh
```

The judgement needs a model in the loop and runs on demand, in **fresh context** — whoever
runs it must not be the agent under evaluation (Theorem 2):

```
/eval 001-review-drops-a-requirement
```

That is deliberately outside continuous integration (CI). A gate everyone must be able to
run cannot depend on an interface key or a per-run cost.

## Freshness is the forcing function

A baseline records the commit of its target. Edit `.claude/agents/review.md` and the case
that evaluates it goes **stale** — the gate names the drift and points at `/eval`. That is
what keeps this directory from becoming the documentation that nothing consumes (Theorem 5).

## What is *not* an eval here

- **A test.** If the output can be compared by equality, write a test or a `check-*.sh`.
  Bringing a model in to judge what `grep` settles is cost with no gain.
- **A benchmark.** These cases do not score models against each other; they hold one
  target — an agent, a skill, a command — to a behaviour we depend on.
- **A demo.** A run that only shows the agent doing well proves nothing. A case earns its
  place by rejecting something.
