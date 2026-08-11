# Operating Model — Roles, Ceremonies, Deliverables and Artifacts

> How work is conducted in a context of **one human orchestrating many AI agents**. This
> document defines WHO does WHAT (roles and responsibilities), WHEN (ceremonies and
> cadence) and WHAT is produced (deliverables and artifacts, each with its gate).
>
> **Status**: Active · **Version**: 1.4.0 · **Date**: 2026-08-02 ·
> **Decisions**: ADR 0004 (operating model), ADR 0005 (lanes and infra specs),
> ADR 0006 (DoD and changelog enforcement) and ADR 0014 (English in the installable
> surface) — all in the Maestro repository, under its own `docs/adr/`. This file is
> installed elsewhere, where those records do not travel: the book is Portuguese by
> decision, and only the English surface is shipped.
> · Acronyms: [glossary](glossary.md).

## 1. Purpose and scope

The constitution (`principles.md`) defines the **principles** (what is non-negotiable) and
the spec-driven toolkit defines the **technical flow of a feature**
(`specify → clarify → plan → tasks → implement`). What was missing is the layer above: the
**operating model** — how roles are shared between human and agents, the work cadence and
the catalogue of deliverables with their quality gates.

This document does **not** replace the constitution; it **integrates** with it. Where they
conflict, the constitution prevails.

## 2. Central operating principle

> **AI to explore, propose and write; the human to specify, decide and approve; tests,
> gates and independent review to validate.**

Three operating rules follow from it:

1. **The spec is the source of truth, not the code and not the prompt.** All work is born
   from a specification (Principle I). The human *directs and refines*; the agent writes.
2. **Whoever executes is not whoever verifies.** Final verification goes through a
   **reviewing agent in fresh context** (and/or the human), never the same agent that
   produced the code. It is the counterweight that replaces a team's second pair of eyes.
3. **Prove it, don't claim it.** "Done" requires evidence an agent can produce and a gate
   can check: green tests, clean build, lint, screenshot, updated journey.

## 3. Work lanes (how much process each change receives)

Not every change deserves a full spec. The **value of a spec scales with ambiguity ×
blast radius × irreversibility** — when all three are low, the spec is ceremony theatre
(YAGNI); when any is high, it pays for itself. Hence three lanes:

| Lane | When | Flow | Record | DoD |
|---|---|---|---|---|
| **Light (delta)** | bug, typo, rename, log, copy — "the diff fits in one sentence" | direct: explore → code → commit (no `spec.md`/`plan.md`/`tasks.md`) | **the pull request is the artifact**; a bug **requires a test that reproduces it** (failing first) | reduced: tests + fitness functions + independent review; living docs only if a journey is touched |
| **Full (spec)** | ambiguous feature, contract, cross-feature change | the complete flow: specify → clarify → plan → tasks → implement | `specs/NNN-*/` | complete (§7) |
| **Infra** | infrastructure, migration, deployment | complete flow — **always full**, never light (even when it looks small) | `specs/NNN-*/` | complete **plus reversibility gates** (§7) |

Rules of the light lane: (1) when in doubt between light and full, it is **full**;
(2) infrastructure and migration are **never** light — blast radius and irreversibility put
them straight into the infra lane; (3) the light lane does **not** loosen independent review
or tests — it only waives the planning artifacts.

> **One spec-driven toolkit only.** The light lane (the *delta* model) lives **inside** it,
> not in a second tool. See §10 (OpenSpec evaluated and discarded).

## 4. Roles and responsibilities

In a tiny team the classic roles **stack up**, but the **counterweights** are preserved by
moving *verify* to an independent agent and keeping *decide* always with the human. Each
"role" is a **mode of work** performed by a human, an agent, or both with a gate.

| Role (mode) | Performed by | Responsibility | Gate |
|---|---|---|---|
| **Product Steward** | **Human** | Decides what and why; prioritises; sets the cycle appetite; approves specs and releases | Accountable for everything |
| **Architect / Tech Lead** | Human + `plan-architect` | Architectural decisions (boundaries, contracts, ADRs); Constitution Check | Human approves the plan |
| **Spec-agent** | Agent (human decides) | Writes `spec.md` from intent; raises ambiguities | Human approves the spec |
| **Plan-agent** | Agent | Writes `plan.md` and the Constitution Check | Human approves the plan |
| **UX-agent** | Agent + skills | Consults the design system and semantic layer; defines `ux-design.md` | Semantic role before component (§6) |
| **Dev-agent** | Agent | Implements tasks; writes tests; small diffs | Green tests + fitness functions |
| **QA/SDET-agent** | Agent | Happy path plus failure coverage per use case; contract and architecture tests | DoD (§7) |
| **Review-agent** (independent reviewer) | Agent in **fresh context** | Reviews the diff against the plan; reports correctness and requirement gaps | Code review, merge gate |
| **Security-agent** | Agent | Injection, secrets and authorization review; secret scanning | Light security gate (§7) |
| **Tech Writer-agent** | Agent | Updates journeys, ADRs and changelog in the same pull request | Living artifacts (P. VI) |
| **Orchestrator** | **Human** | Sequences agents; clears context between tasks; decides parallel versus pipeline; stops when something is expensive to undo | — |

**RACI per lifecycle stage** (R = executes, A = approves and is accountable, C = consulted,
I = informed):

| Stage | Executes (R) | Verifies (C) | Approves (A) |
|---|---|---|---|
| Define intent and appetite | Human | — | **Human** |
| Spec (`spec.md`) | Spec-agent | Human | **Human** |
| Plan + Constitution Check | Plan-agent | Review-agent | **Human** |
| UX design | UX-agent | Human | **Human** |
| Implementation | Dev-agent | QA-agent | Review-agent → **Human** |
| Code review | Review-agent (fresh) | Security-agent | **Human** |
| Documentation and journeys | Tech Writer-agent | Human | **Human** |
| Release and deployment | Human + continuous integration | Review-agent | **Human** |

> **The human is the fixed Accountable on every risk-bearing row.** No agent decides alone
> anything that falls into the change / deletion / external / irreversible risk classes
> (Principle III) — see §8.

## 5. Ceremonies and cadence

We adopt a **Shape Up plus Kanban skeleton**, not Scrum. Daily stand-up and sprint planning
are cut (ceremony theatre for a single operator). Work flows continuously with **work in
progress limited to one feature or spec at a time**, organised in **cycles with a fixed
appetite**.

| Ceremony | Cadence | Who | Purpose | Output |
|---|---|---|---|---|
| **Shaping / Spec** | Per feature | Human + spec and plan agents | Define appetite, scope and testable acceptance criteria; this is the real planning | Approved `spec.md` |
| **Cycle execution** | Continuous (fixed appetite) | Orchestrator + agents | Implement with variable scope inside the appetite; stop when the appetite runs out, not when everything is finished | Merged pull requests |
| **Cycle checkpoint** | End of each cycle | Human | Inspect what landed; decide cooldown or next bet | Decision on the next spec |
| **Cooldown** | After the cycle | Human + agents | Technical debt, maintenance, small bugs (light lane, §3), skill curation | — |
| **Retrospective** | End of each cycle | Human | What the agents got wrong repeatedly → becomes a rule | A rule in `CLAUDE.md`, a skill or the constitution |

> **The retrospective has the highest return in this model.** Every recurring correction you
> make to an agent must become a **versioned instruction**. The process learns; you stop
> repeating the same correction.

**Appetite (Shape Up)**: the cycle has fixed time and variable scope — the opposite of
estimating a deadline. It pairs directly with YAGNI and small diffs: when the appetite runs
out, scope is cut, the deadline is not extended.

## 6. Deliverables and artifacts

Catalogue of lifecycle artifacts, with **owner**, **gate** and **where it lives**.
"Essential" = mandatory now; "Later / YAGNI" = observed, not adopted (§10).

| Artifact | Owner | Where it lives | Gate | Status |
|---|---|---|---|---|
| **Brief / intent** | Human | issue or spec header | — | Essential |
| **Spec** (`spec.md`) | Spec-agent | `specs/NNN-*/` | Human approves (DoR) | Essential (full lane) |
| **Plan** (`plan.md`) + Constitution Check | Plan-agent | `specs/NNN-*/` | Human approves | Essential (full lane) |
| **UX design** (`ux-design.md`) | UX-agent | `specs/NNN-*/` | Semantic role before component (§4) | Essential (if there is a user interface) |
| **Tasks** (`tasks.md`) | Plan-agent | `specs/NNN-*/` | — | Essential (full lane) |
| **Infra spec** | Human + agent | `specs/NNN-*/` | Always full lane plus reversibility gates (§7) | Essential (infra and migration) |
| **Code + tests** | Dev-agent | the application code | Green tests and fitness functions | Essential |
| **ADR** | Tech Writer-agent | `docs/adr/NNNN-*.md` | Architectural decision recorded | Essential (per decision) |
| **Journey doc** | Tech Writer-agent | `docs/journeys/NNN-*.md` | Living artifacts (P. VI) | Essential (if there is a journey) |
| **Runbook** | Human + agent | `docs/infra/` | Rollback strategy documented | Essential (infra) |
| **Changelog / release notes** | Tech Writer-agent | `CHANGELOG.md` | Gated in continuous integration | Essential |
| **Decision index** | automatic | `docs/records/decisoes.jsonl` | Append-only, validated by script | Essential |
| **Definition of Ready/Done** | Human | this document (§7) | Verifiable checklist | Essential |
| **Pull request** | Dev-agent | the forge | Merge gate (§7); **in the light lane the pull request is the artifact** | Essential |
| Architecture diagrams | — | — | — | Later / YAGNI |
| Heavy RFC process | — | — | — | YAGNI (the ADR covers it) |
| Metrics dashboard | — | — | — | Later / YAGNI |

## 7. Definition of Ready and Definition of Done

Written as **verifiable checklists** — an agent can satisfy them and a hook can check them.
The Definition of Ready (DoR) applies to the **full lane** (§3); the light lane goes straight
into execution with the **reduced DoD** below.

### Definition of Ready (may a spec enter execution? — full lane)
- [ ] `spec.md` describes **what and why** with **testable** acceptance criteria.
- [ ] Ambiguities resolved (clarify) or recorded.
- [ ] `plan.md` passed the **Constitution Check** (a violation is justified or removed).
- [ ] `ux-design.md` declares the semantic roles consumed and introduced (if there is a
      user interface).
- [ ] **Appetite** defined (the fixed time of the cycle).

### Definition of Done (is a feature finished?)
- [ ] Green tests: domain unit tests, contract per port, integration per route.
- [ ] **Fitness functions** (dependency rules) green in continuous integration (P. V).
- [ ] Lint and type checks clean.
- [ ] **Independent review** in fresh context, with no open correctness or requirement gaps.
- [ ] **Light security gate**: secret scanning clean; injection and authorization review
      where applicable (P. IV).
- [ ] **Living documentation updated in the same pull request**: journey (screenshots plus
      heuristic), ADR if a decision was made, changelog.
- [ ] **Traceability** recorded: spec NNN ↔ pull request ↔ tests ↔ journey (§9).
- [ ] Evidence attached (test, build or screenshot output) — "prove it, don't claim it".

**Reduced DoD (light lane, §3)**: tests, fitness functions, lint/type checks and
**independent review** still apply; planning artifacts and living docs are waived **unless**
the change touches a journey. A bug **requires a test that reproduces it** before the fix.

### Mandatory block for irreversible actions (infra lane, §3)
Beyond the DoD above, every irreversible action (destructive migration, deployment, data
deletion) requires — materialising "engineered reversibility":
- [ ] **backup or snapshot** before any destructive action;
- [ ] **dry run plus staging validation** before production;
- [ ] **rollback strategy** documented in the runbook (soft delete where applicable);
- [ ] **explicit human approval** (risk class "financial / irreversible", §8).

## 8. Map of non-negotiable human gates

This reuses the **risk-class taxonomy** of `principles.md` (Principle III). The agent acts
alone at low risk; the human **MUST** approve from "change" upwards.

| Risk class | Example | Agent alone? | Human gate |
|---|---|---|---|
| Read | Read code, search, explore | ✅ Yes | No |
| Sensitive read | Data with personal information or secrets | ⚠️ With policy and masking | Review |
| Reversible creation | New feature on a branch, a draft | ✅ Yes | At merge |
| **Change** | Broad refactor, contract change | ❌ No | **Approval with a summary** |
| **Deletion / external action** | Delete data, call an external service, push | ❌ No | **Strong confirmation** |
| **Financial / irreversible** | Production deployment, destructive migration | ❌ No | **Double approval / re-authentication** |
| **Batch / cross-tenant / admin** | Mass migration, administrative action | ❌ **Blocked** | **Formal human workflow** |

Non-negotiable human gates, always: **approve the spec**, **approve the plan (Constitution
Check)**, **approve the merge**, **authorize deployment or migration**. None of these is
delegable to an agent.

## 9. Traceability and end-to-end flow

```
intent → spec.md (NNN) → plan.md (+Constitution Check) → ux-design.md → tasks.md
   → implementation (Dev-agent) → tests + fitness functions (continuous integration)
   → independent review (Review-agent) + security
   → living docs (journey/ADR/changelog) → pull request → human merge gate → release
```

In the **light lane** (§3) the path shortens to `intent → code → test → independent review →
pull request (the artifact) → merge`, with no spec, plan or tasks.

Every feature keeps the link **spec NNN ↔ pull request ↔ tests ↔ journey** explicit (part of
the DoD). That gives the decision → code → verification traceability that light governance
requires, with no heavy tooling.

## 10. What we do NOT adopt (anti-process / YAGNI)

Stated explicitly to avoid speculative process (constitution, governance and YAGNI):

- **Full Scrum** (Scrum Master, sprint planning, team stand-up) — ceremony theatre for one
  human plus agents. We keep shaping, cooldown and the retrospective.
- **A formal backlog** — Shape Up shows that important ideas come back through re-shaping;
  we do not accumulate a backlog.
- **A second spec-driven toolkit (for example OpenSpec)** — evaluated and discarded: we do
  not maintain two of them. What was worth keeping was the *delta* model for small changes,
  absorbed as the **light lane** (§3).
- **A heavy RFC process** — the ADR already covers decision, context and consequences.
- **Formal architecture diagrams and metrics instrumentation** — today diagrams in text plus
  a green pipeline are enough; revisit when scale justifies it.
- **Deadline estimates** — we use appetite (fixed time, variable scope).

## 11. Evolution of this document

This document is **versioned** and evolves like the constitution: material changes bump the
version (MINOR: a new role, ceremony, artifact or lane; PATCH: clarification) and are
recorded in an ADR. The **cycle retrospective** is the primary source of amendments — every
new rule is born from an observed recurring mistake. A review is mandatory at the end of
each project phase.

**History**: 1.0.0 (2026-07-22, ADR 0004) foundation · 1.1.0 (2026-07-22, ADR 0005) work
lanes (light/full/infra), infra spec with reversibility gates, OpenSpec evaluated and
discarded · 1.2.0 (2026-07-22, ADR 0006) enforcement (§12): pull request template with the
DoD, changelog gate in continuous integration, the `/dod` command · 1.3.0 (2026-07-31,
ADR 0009) automatic recording of the merge gate in the queryable index
(`docs/records/decisoes.jsonl` via `promote-main.sh`); the index is the source of truth for
gate state · 1.4.0 (2026-08-02, ADR 0014) English as the language of the installable method;
role and artifact names aligned with the executable toolkit.

## 12. Enforcement (how the model is actually applied)

The guarantee does not come from discipline or memory — it comes from **making every
criterion executable and blocking**. Each item has a mechanism, split between **mechanical**
(a hard gate that blocks on its own) and **judgement** (a checklist plus human approval):

| Item | Mechanism | Where |
|---|---|---|
| Tests + fitness functions + build and type checks | **Hard gate (continuous integration)** — blocks the merge | `.github/workflows/ci.yml` |
| Changelog entry | **Hard gate** — the `changelog` job (bypass: label `skip-changelog`) | `ci.yml` + `CHANGELOG.md` |
| Secret scanning | **Native forge setting** (secret scanning plus push protection) | repository configuration |
| DoD/DoR, lane, traceability, risk gate | **Mandatory checklist** | `.github/pull_request_template.md` |
| Agent self-check before "done" | **Command** `/dod` | `.claude/commands/dod.md` |
| DoR (spec ready) + Constitution Check | **Templates** plus the constitution | `.specify/templates/` |
| Reading the constitution and this model before acting | **Directive** | `CLAUDE.md` / `AGENTS.md` |
| Merge gate record | **Automatic** — `promote-main.sh` appends `gate-main-<sha>` to the index (ADR 0009) | `scripts/` + `docs/records/decisoes.jsonl` |
| Method installed and coherent | **Fitness function** — `check-install.sh` | `scripts/` |

**The split is the same as the RACI one**: what is mechanical becomes a hard gate on the
machine; what requires judgement — "is this the right thing?", the risk class — stays in the
pull request checklist plus human approval (the Accountable).
