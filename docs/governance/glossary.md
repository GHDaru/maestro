# Glossary — Maestro acronyms and terms

> Dictionary of every acronym used in the governance documents and in the book. In each
> document an acronym is expanded on its **first occurrence**; this is the full reference.
> The book (`docs/handbook/`) is written in Portuguese; the installable method is in
> English (ADR 0014), so both spellings appear where they are used.

| Acronym / term | Expansion | In Maestro | Where |
|---|---|---|---|
| **ADR** | *Architecture Decision Record* | **Immutable** record of a decision (context → decision → consequences). | Ch. 12 · `docs/adr/` |
| **API** | *Application Programming Interface* | Integration contract between systems. | — |
| **ABAC** | *Attribute-Based Access Control* | Attribute-based authorization — decided **outside** the model. | Ch. 1 · 10 |
| **RBAC** | *Role-Based Access Control* | Role-based authorization. | Ch. 10 |
| **BMAD** | *BMAD-METHOD* (`bmad-code-org`) | Agentic spec-driven framework, ~22 agents in per-phase teams. Evaluated and **rejected** (cycle 007): a whole competing methodology would create a second source of truth. | ADR 0008 |
| **BDD** | *Behavior-Driven Development* | Tests written in behaviour/business language. | Ch. 9 |
| **Bounded context** | Bounded context (DDD) | The **seam** along which work is cut for safe parallelism. | Ch. 4 · 5 |
| **C4** | Modelo C4 (*Context, Container, Component, Code*) | Architecture diagrams at four levels. | Ch. 8 (not adopted for now) |
| **CI** | *Continuous Integration* | Continuous integration — runs tests and gates on every change. | Ch. 8 · 9 |
| **CD** | *Continuous Delivery/Deployment* | Continuous delivery/deployment. | — |
| **DDD** | *Domain-Driven Design* | Domain-driven design; it provides the bounded contexts. | Ch. 3 · 5 |
| **DoD** | *Definition of Done* | **Verifiable** criteria for "done". | Ch. 9 |
| **DoR** | *Definition of Ready* | Criteria for "ready to start" (a spec executable without guessing). | Ch. 9 |
| **DORA** | *DevOps Research and Assessment* | Programme and four delivery-performance metrics. | Ch. 2 |
| **DX** | *Developer Experience* | Developer experience. | Ch. 2 |
| **EARS** | *Easy Approach to Requirements Syntax* | `WHEN ‹condition› THE SYSTEM SHALL ‹observable behaviour›` — a requirement that becomes a test almost 1:1. Absorbed from Kiro (cycle 007); lives in `verifiable-dod` and the spec template. | ADR 0008 |
| **Eval** (*evaluation*) | Judgement baseline | Fixed input + assertions that discriminate + a dated observation, for output that cannot be compared by equality. **Not** a test (equality) and **not** a benchmark (models against each other). | `evals/` · ADR 0016 |
| **Fitness function** | Architecture test | Checks dependency rules in continuous integration. | Ch. 9 |
| **Forcing function** | Mechanism that forces | What **fails loudly** when an artifact is not kept up to date. | Ch. 8 |
| **AI / IA** | Artificial Intelligence | The agent that executes under orchestration. | — |
| **LLM** | *Large Language Model* | Language model; the agent's engine. | Ch. 1 · 5 |
| **MCP** | *Model Context Protocol* | Protocol for exposing and consuming tools for agents. | — |
| **NNN** | Spec numbering | The `specs/NNN-name/` convention (001, 002…). | Ch. 3 · 11 |
| **OPA** | *Open Policy Agent* | Declarative policy engine (`allow/deny/ask`). | Ch. 10 |
| **OWASP** | *Open Worldwide Application Security Project* | Security reference (for example LLM01 — prompt injection). | Ch. 10 |
| **PII** | *Personally Identifiable Information* | Sensitive personal data (the "sensitive read" risk class). | Ch. 10 |
| **PO** | *Product Owner* | Product decision role (in Maestro, the human Steward). | Ch. 6 |
| **PR** | *Pull Request* | Reviewable change proposal; in the **light lane** it is the artifact itself. | Ch. 8 · 11 |
| **PRD** | *Product Requirements Document* | Product requirements; the function is absorbed by the **spec**. | Ch. 8 |
| **QA** | *Quality Assurance* | Quality assurance (tests and coverage). | Ch. 6 |
| **RACI** | *Responsible, Accountable, Consulted, Informed* | Responsibility matrix: **R/C/I** delegable to agents, **A** always human. | Ch. 6 |
| **Lane** (*raia*) | Work lane | Light / full / infra — how much process each change receives. | Ch. 3 |
| **ReBAC** | *Relationship-Based Access Control* | Relationship-based authorization. | Ch. 1 |
| **RFC** | *Request for Comments* | Design proposal for discussion (not adopted standalone — the ADR covers it). | Ch. 8 |
| **ROI** | *Return on Investment* | Return on investment — Maestro's executive thesis. | — |
| **SBOM** | *Software Bill of Materials* | Inventory of what composes a shipped artifact — dependencies, versions, licences. Named in cycle 046 as **theatre here**: in an agentic system the payload is the prose, so a fully-markdown MIT file can still instruct harm. | Cycle 046 |
| **SDD** | *Spec-Driven Development* | Spec-driven development. | Ch. 3 |
| **SDET** | *Software Development Engineer in Test* | Test engineer. | Ch. 6 |
| **SM** | *Scrum Master* | Scrum role — cut in Maestro (ceremony theatre). | Ch. 6 · 7 |
| **SPACE** | *Satisfaction, Performance, Activity, Communication, Efficiency* | Multidimensional productivity framework. | Ch. 2 |
| **SSE** | *Server-Sent Events* | Server-to-client streaming. | — |
| **SAST / DAST** | *Static / Dynamic Application Security Testing* | Static and dynamic security analysis. | Ch. 9 |
| **Spec** | Specification | The **source of truth**: the input that generates the code. | Ch. 3 |
| **TDD** | *Test-Driven Development* | Test before code (red → green → refactor). | Ch. 9 |
| **UI / UX** | *User Interface / User Experience* | User interface / user experience. | Ch. 6 |
| **WIP** | *Work In Progress* | Work in progress — limited by **human attention**. | Ch. 7 |
| **YAGNI** | *You Aren't Gonna Need It* | Do not build the speculative; prune what does not pay for itself. | Ch. 12 |
