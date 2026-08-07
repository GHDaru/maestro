# Axioms, Theorems and Corollaries

> The **assumed truths** of Maestro. An axiom is not argued for — it is *assumed*, and
> everything else is derived from it. A theorem is derived and must be **provable in this
> repository**. A corollary is what follows immediately, and is where most of the day-to-day
> rules come from.
>
> **Version**: 1.2.0 · **Date**: 2026-08-07 · **Cycles**: 035, 037, 042 · ADR 0015, 0016, 0019
> · Constitution: [principles.md](principles.md) · Acronyms: [glossary](glossary.md)

## How to read this document

The constitution says **what must be done**. This document says **why it cannot be
otherwise**. When a new rule is proposed, the first question is which axiom it derives from;
a rule that derives from none is either a new axiom (rare, and it is argued for) or ceremony
(and it is pruned).

Every theorem below carries its **evidence in this repository** — the derivation is not a
rhetorical exercise. A theorem that cannot be shown failing when violated is a belief, not a
theorem (that is Theorem 4 applied to this very document).

| Element | Status | Test |
|---|---|---|
| **Axiom** | assumed, not proved | is it independent? does removing it break the rest? |
| **Theorem** | derived from axioms | can it be shown with evidence from the repository? |
| **Corollary** | immediate consequence | does it change a decision in practice? |

---

## The five axioms

### A1 — Intent is human

Software exists to serve a purpose that belongs to a person. An agent can propose, write and
verify; it cannot *want*. The intent — what to build and why it is worth it — has no source
other than a human.

> **Independence**: remove A1 and there is no reason for a specification to exist; the system
> becomes an optimiser with no objective function.

### A2 — Consequence needs an owner

Responsibility exists where there is something to lose. An agent produces the best analysis
on the table and still bears nothing if it is wrong. Accountability is therefore not
transferable to it — not for lack of capability, but for lack of exposure.

> **Independence**: remove A2 and every gate becomes optional; the question "who answers for
> this?" has no answer.

### A3 — Context is finite and degrades as it fills

The window that an agent reads is bounded, and its performance falls as the window fills with
noise. This is a physical property of the tool, not a habit of the operator.

> **Independence**: remove A3 and there is no reason to slice work, to reset context, or to
> keep an agent narrow.

### A4 — What is written down is what survives

An agent starts each session from zero. Whatever is not in an artifact does not exist for the
next execution — including the reason a decision was made.

> **Independence**: remove A4 and documentation becomes optional; memory would live somewhere
> other than the repository.

### A5 — Cost is asymmetric between doing and undoing

Producing is cheap and getting cheaper; undoing is not. Deleting data, deploying, migrating
and publishing have costs that no speed compensates for.

> **Independence**: remove A5 and every action deserves the same treatment — which is exactly
> the uniform gate the method rejects.

---

## The theorems

### T1 — Specification precedes code (from A1 and A4)

If intent is human (A1) and only what is written survives (A4), then intent must live in an
artifact **before** it becomes code. Otherwise the agent fills the silence by guessing, and
the result compiles while missing the point.

> **Evidence**: 34 cycles, each opening with `spec.md`. Cycle 021 shows the inverse case: the
> requirement (FR3) written before the code became a loop in `check-install.sh` and caught a
> three-cycle drift on its first run.

### T2 — Whoever executes does not verify (from A2 and A3)

Independent verification is not distrust of the author; it is a consequence of context. The
agent that wrote carries the dead ends it explored (A3), and someone must answer for the
result (A2). Fresh context is the only way to look at the diff without that load.

> **Evidence**: three of the thirteen agents — `review`, `security`, `process-guardian` —
> have no `Write` or `Edit` in their tool list, and `check-agents.sh` fails if they gain it.
> Independence is configuration, not promise.

### T3 — The gate scales with irreversibility, never uniformly (from A2 and A5)

If cost is asymmetric (A5) and consequence needs an owner (A2), then a uniform gate is always
wrong: heavy everywhere it turns the human into a rubber stamp; light everywhere it lets the
irreversible through. The gate must be a function of the risk class.

> **Evidence**: 21 merge gates recorded in the decision index, while dozens of reversible
> operations ran with no human approval. Chapter 10 also declares the honest limit: four of
> the seven risk classes have never occurred here.

### T4 — A criterion without a command is not a criterion (from A2 and A4)

If someone answers for the result (A2) and only the written survives (A4), "done" must
produce evidence that a machine can confirm. Otherwise "done" means whatever the reader
assumed, and accountability has nothing to attach to.

> **Evidence**: eight fitness functions in `scripts/`, plus two gates inside the site build
> and eleven tests in the companion. And the counter-evidence, which matters more: **nine
> defects escaped to the main line** with the gate green — every one of them caught later by
> *a check somebody wrote*, never by attentive reading.

### T5 — An artifact survives by consumption or by immutability (from A3 and A4)

Keeping an artifact updated costs attention, which is the scarce resource (A3). So only two
kinds survive: the one something downstream **consumes** (and which fails loudly when stale),
and the one that describes a moment and therefore never goes stale (A4).

> **Evidence**: the changelog survives because continuous integration fails without it; the
> decision records survive because they are immutable — nine of the ten ADRs have exactly one
> commit since they were born.

### T6 — Correction that does not become a rule will repeat (from A3 and A4)

An agent does not remember the previous session (A4) and its window does not hold the whole
history (A3). A correction made in conversation therefore has a lifetime of one session; only
a versioned rule survives into the next.

> **Evidence**: anti-pattern 13 ("a check that measures the proxy") recurred **four times**
> before the antidote became law in a skill. And the retrospective itself was a rule with no
> trigger for thirty-three cycles — until cycle 034 gave it one.

### T7 — Where output is not comparable, the criterion is a baseline (from A2 and A4)

T4 says a criterion needs a command. But a command can only settle what is comparable by
equality: a section is present or absent, a link resolves or does not. A **judgement** — a
review verdict, a lane call, a trade-off in a plan — has no such comparison, and reading it
attentively is not a criterion: it produces no artifact (A4) and nothing to hold anyone to
(A2).

What replaces the comparison is a **recorded baseline**: a fixed input, assertions that
separate a right answer from a merely plausible one, and an observation with a date. The
positive assertion is not enough — a case that only asks "did it find something?" passes on
any verbose answer. What discriminates is the negative side: what a wrong answer *would*
claim.

> **Evidence**: for thirty-six cycles, thirteen agents operated with no baseline at all —
> nothing would have noticed a regression in `review.md`. And the limit was known and
> written down: the only occurrence of *judge* in `scripts/` is the comment at
> `check-cycle.sh:8` conceding that the gate "cannot judge the answer". Knowing the gap and
> stopping there is what T7 names.

---

## The corollaries (where the everyday rules come from)

| # | Corollary | From | Where it shows up |
|---|---|---|---|
| C1 | Every ceremony has a trigger, and the trigger is measurable | T6 | `check-retro.sh`; anti-pattern 17 |
| C2 | Prove the check by watching it fail | T4 | second law of `verifiable-dod` |
| C3 | The role that judges does not get write permission | T2 | agent tool lists; `check-agents.sh` |
| C4 | Reversibility lowers the risk class, and is cheaper than one more approval | T3 | infra block of the operating model |
| C5 | A gate covers a whole family or it covers nothing | T4 | anti-pattern 16; `check-links.sh` |
| C6 | How much process a change gets is a function of ambiguity × blast radius × irreversibility | T1, T3 | the three lanes; `check-cycle.sh` |
| C7 | A norm without an executable is a norm without effect | T4, T6 | `check-roles.sh`; `check-install.sh` |
| C8 | A narrow agent is cheaper than a capable one | T2, T5 | 13 agents in 267 lines |
| C9 | Documentation that nothing consumes will rot, however good it is | T5 | artifact catalogue; the "we do not adopt" list |
| C10 | What is installed is read by machines; what is published is read by people | A4 | ADR 0014: English toolkit, Portuguese book |
| C11 | An evaluation names its target and goes stale when the target moves | T7, T5 | `check-evals.sh`; `evals/*/baseline.md` |
| C12 | What survives compaction is what is in a consumed artifact — the rest is deleted, not degraded | A3, A4 | `check-conformance.sh`; the closing tail in `tasks.md` |
| C13 | A question answerable from memory will be answered from memory, and memory reports intention | A4, T4 | `check-conformance.sh` replaces "are you following the method?" |

## What this document does NOT do

It does not replace the constitution: the principles remain the operative norm, and it is
them a plan is checked against. This document exists so that a **new** rule can be argued
against something stable — and so that a rule that derives from nothing can be recognised as
what it is.

It also does not claim completeness. Five axioms is a bet on the smallest set that supports
the method as it stands. If a principle turns out to derive from none of them, either an
axiom is missing (and it enters through an ADR) or the principle is ceremony (and it is
pruned by YAGNI).
