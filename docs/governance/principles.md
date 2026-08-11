# Maestro Principles (the constitution of the method)

> Source of truth for Maestro's conventions. It prevails over any other practice in this
> repository. **Every agent and every human MUST read this document before any work.**
> Amendments go through an ADR (Architecture Decision Record) plus a version bump.
>
> **Version**: 1.3.0 · **Ratified**: 2026-07-22 · **Amended**: 2026-08-03 (ADR 0015 —
> axioms, theorems and corollaries as the derivation layer)
>
> New to Maestro? Start with "Comece por aqui", in the Maestro repository (Portuguese —
> the book does not travel with the installation; only this English surface does).
> Acronyms: [glossary](glossary.md). Assumed truths: [axioms](axioms.md) (ADR 0015).

Maestro is the method of **one human conducting many AI agents**: the specification is the
source of truth, the agents execute, the human decides, approves and verifies. These are the
non-negotiable principles; the **operating model** (`operating-model.md`) turns them into
practice and the **book** (`../handbook/`, in Portuguese) explains their foundations.

## Principles

### I. Spec-driven (the spec is the source of truth)
No code is born without a specification. The spec is the **input that generates** the code,
not a description of it — that is why it does not rot. Flow:
`specify → clarify → plan → tasks → implement`. A scope change goes back to the spec before
it becomes code.

### II. Human-governed orchestration (one conducts many)
Roles are **modes of work** in a human × agents matrix (RACI). **Responsible, Consulted and
Informed** are delegated to agents; the **Accountable is always human**, and is accountable
**for the policy, the gates and the criteria — not for each item**. Verification is done by
an **independent agent in fresh context** (whoever executes does not verify).

### III. Reversibility and risk-proportional gates (NON-NEGOTIABLE)
The human gate scales with **irreversibility × blast radius** (taxonomy: read → … →
irreversible → blocked). What makes an irreversible action safe to delegate is **engineered
reversibility** (backup, dry run, staging, soft delete), which **lowers the risk class**.
Declarative policy `allow / deny / ask`; authorization lives outside the model.

### IV. Test-first and verifiable DoD ("prove it, don't claim it")
Tests are born with the code, or before it. "Done" is **autonomously verifiable** (a
pass/fail the agent produces and a hook confirms); the work is **turning judgement into a
check**. Green locally ≠ right globally — global coherence and "is this the right thing" stay
with the human. Continuous integration and architecture tests (fitness functions) are gates
from the start.

### V. Context economy and cutting by boundary
The context window is finite and degrades as it fills: preserve the **integrating context
(the spec)**, discard the noise. Parallelise **by bounded context** — good cuts are what make
orchestration safe. Use the least autonomy that solves the problem (fixed flow before
autonomous agent).

### VI. Living artifacts and traceability
An artifact only exists if it is an **input consumed with a forcing function** (or immutable,
like an ADR). Never duplicate a function already served. The traceability chain
**spec ↔ pull request ↔ tests ↔ journey** is the project's durable memory — it emerges from
the workflow, with no heavy tooling.

### VII. Light governance that learns (YAGNI)
Governance **learns without bloating**: a firm core (this constitution) plus an evolving
periphery (operating model and book, with their own version) plus append-only memory (ADRs)
plus **retrospective → versioned rule**. **YAGNI** prunes what does not pay for itself.
Complexity beyond what is needed is justified in writing or removed.

### VIII. Intelligible communication (an acronym is never born naked)

**Iron Law:** in **every answer, document or artifact**, the **first occurrence** of an
acronym is written **in full**, with the abbreviation in parentheses; from there on,
abbreviate freely. The count restarts with each answer or document — the reader has no
obligation to have read the previous one.

> Example: "the Definition of Done (DoD) requires evidence; with no green DoD there is no
> gate."

Violating the letter violates the spirit. This is **not** an excuse: "everyone knows this
acronym" (tomorrow's reader, or the new agent, does not) · "I explained it before" (before
was another answer) · "it is domain jargon" (orphan jargon is what produces the pile-up).
A new term also enters the [glossary](glossary.md). Operationalised by the
`fight-the-pile-up` skill.

## Where the principles come from

The eight principles above are the **operative norm**. What they are derived *from* lives in
[axioms.md](axioms.md): five assumed truths, six theorems proved with evidence from this
repository, and ten corollaries. A new rule is argued against that layer — a rule that
derives from no axiom is either a new axiom (argued for, through an ADR) or ceremony (pruned
by YAGNI).

## Governance

This constitution prevails; amendments bump the semantic version (MAJOR: removal or
redefinition; MINOR: a new principle or an expansion; PATCH: clarification) and are recorded
in an ADR. Every material methodology decision becomes an ADR.

## Language (ADR 0014)

The **installable method is written in English** — agents, skills, scripts, commands,
templates and these governance documents. The **book** (`../handbook/`), the recipes and the
published site are written in Portuguese. The rule exists because the installable surface is
read by AI agents in any repository, while the book is written for a specific audience.

## Lineage note (migration)

Documents migrated from earlier repositories cite "the Constitution" and "Principle IV/V/VII"
referring to the constitution of the **platform** they came from. In Maestro those roles map
onto the principles above (approximate map: IV→III+IV, V→IV, VII→II+VI). Rewriting those
references in detail is a follow-up recorded in ADR 0007.
