# Artifact catalogue — what exists, when it applies, what consumes it

> The canonical list of every artifact a Maestro cycle can produce. **Every conditional
> artifact is declared in `plan.md`, never merely absent** — an omission violates nothing
> visibly, which is how a plan quietly becomes a lossy copy of the method.
>
> **Version**: 1.0.0 · **Date**: 2026-08-07 · **Cycle**: 042 · ADR 0019
> · Constitution: [principles.md](principles.md) · Assumed truths: [axioms.md](axioms.md)
> · Verification: `scripts/check-conformance.sh`

## Why this document exists

It was written because its absence had a measurable cost. Two facts, from the repository
that produced this method:

- **Zero of forty cycles** produced `research.md`, `data-model.md`, `contracts/`,
  `checklist.md` or `ux-design.md`. For most that was correct — they were documentation
  cycles. Nothing recorded which.
- The rule for when each one applies lived in a planning document that the installer
  **does not copy**, while the vendored `/speckit.plan` command — which *is* copied —
  instructs the agent to generate four of them. Whoever installed the method received a
  command demanding artifacts, a template for one of them, and no rule.

Principle VI says an artifact only exists if something consumes it. The corollary this
document adds: **an artifact nobody declared does not exist either — not even as a decision
not to write it.**

## The four that always exist

Every cycle has these, in this order. A cycle missing one of them is not a Maestro cycle.

| Artifact | Answers | Produced by | Consumed by |
|---|---|---|---|
| `spec.md` | what and why; the lane and its rationale | `/speckit.specify`, `spec-agent` | the plan, the review, the gate |
| `plan.md` | how; the **Constitution Check**, complete | `/speckit.plan`, `plan-architect` | the tasks, the guardian |
| `tasks.md` | the executable checklist, **including the closing tail** | `/speckit.tasks` | whoever implements — this is the file an agent actually follows |
| `qa-report.md` | what was observed, with evidence | `qa` | the human gate |

> **`tasks.md` carries more weight than its size suggests.** It is the list an executing
> agent reads, and it survives context compaction only to the extent it is written down.
> A step that lives in the spec but not here will be skipped by an agent that is obeying
> perfectly (corollary C12).

## The five that are conditional — and always declared

Declared in `plan.md` with a machine-readable token, so the check survives translation and
rewording. `=yes` means the file must exist in the cycle directory.

| Artifact | Token | Applies when | Does not apply when |
|---|---|---|---|
| `research.md` | `ART:research=` | there is a technical unknown to resolve **before** deciding — a library choice, a protocol, an unmeasured cost | the decision needs no new information |
| `data-model.md` | `ART:data-model=` | the cycle introduces or changes **entities and their relations** | documentation, method, tooling |
| `contracts/` | `ART:contracts=` | there is an **interface between parts**: a route, a port, an event, a schema. This is what makes parallel work safe | nothing crosses a boundary |
| `checklist.md` | `ART:checklist=` | this cycle deserves a **quality checklist of its own** beyond the DoD | the DoD covers it |
| `ux-design.md` | `ART:ux-design=` | **it touches a screen — then it is not optional.** Semantic role before component (Principle VII of the platform this came from); the `ux-semantics` agent produces it | no interface |

The honest note about the last one: it is the one most often skipped, because a screen feels
like implementation rather than design. It is also the one where skipping is most expensive,
since a component built without its semantic role has to be rebuilt rather than adjusted.

## The closing tail — four steps that are not artifacts, and are still mandatory

They live in `tasks.md` as tokens, and their **evidence** lives in `qa-report.md`. A ticked
box is not a witness.

| Token | What it is | Never delegable |
|---|---|---|
| `TAIL:review` | independent review in **fresh context**, by whoever did not execute (Theorem 2) | the review may be an agent; it must not be the executor |
| `TAIL:security` | a security pass proportional to the risk class. Write `n/a:` with a real reason when there is no risk surface | — |
| `TAIL:mutation` | every gate this cycle created or changed, **broken on purpose and seen refusing**. Write `n/a:` with a reason when the cycle touched no gate — the check reads the diff, not the sentence, and refuses the dispensation from a cycle that did (cycle 055) | — |
| `TAIL:gate` | the **human merge gate** (Axiom A2) | yes — this one is the human's, always |

To declare a tail step inapplicable, write `n/a:` and the reason **on the line**. Do not
delete the line: an absent step is invisible, a declared exception is auditable. A
placeholder reason is rejected.

## Memory and governance (not per-cycle)

| Artifact | Nature | Rule |
|---|---|---|
| ADR (`docs/adr/`) | immutable | a reversal is a **new** ADR that supersedes; the body of the old one is never rewritten |
| decision index (`docs/records/decisoes.jsonl`) | append-only | a correction is a new line; see the protocol in that directory |
| `CHANGELOG.md` | living | forcing function in continuous integration |
| roadmap | living | updated in the same pull request as the cycle that changes it |

## How to answer "am I following Maestro?"

Not from memory. Memory reports intention, and intention is not evidence — an agent asked in
conversation will describe the method it believes it followed. Run this instead:

```bash
scripts/check-conformance.sh        # every cycle from the floor onward
scripts/check-conformance.sh 042    # one cycle
```

What it can tell you: whether the method survived into the artifacts. What it cannot tell
you: whether the work is any good, and whether a human read the evidence. Those stay where
Axiom A2 puts them.
