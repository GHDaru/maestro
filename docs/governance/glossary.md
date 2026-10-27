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
| **Task ledger** | `docs/records/tarefas.jsonl` | Append-only record, one event per line, of the tokens, cost and attempts of each tagged task. Protocol in [task-ledger.md](task-ledger.md). | Cycle 065 |
| **Task tag** (`[[TASK]]` / `[[DONE]]`) | One-line message tag | `[[TASK id=… kind=…]]` marks a task handed out; `[[DONE id=… outcome=…]]` marks it delivered. Each tag stands alone on its line; the first `[[TASK]]` and the last `[[DONE]]` of a message count. The contract between manager and worker sessions, read by the `maestro-ledger` mod. | [task-ledger.md](task-ledger.md) |
| **Mod** | Claude Code plugin that runs inside the Claude Code process | Subscribes to engine events (`session.receive`, `turn.step`…). `maestro-ledger` is the one Maestro ships; installed with `claude plugin install`, never by the method installer. | [task-ledger.md](task-ledger.md) |
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
| **Veredito vigente** | — | Among several verdicts on the same gate, the one in force: the latest `data:` in its header on the right hash; ties by the file's commit date, then by name — never by alphabetical order. | Cycle 069 |
| **Data legível** | — | A `data:` header the conferidor can parse (`YYYY-MM-DD HH:MM ±HHMM`); a verdict whose date is unreadable is rejected by `valida()` and never competes to be in force. | Cycle 069 |
| **Rodada** | — | One execution of the Maestro workflow, recorded step by step in SQLite (`rodadas`): who opened it, when, for which desire, when it closed; append-only. | Cycle 070 |
| **Passo** | — | A step of a rodada, recorded three times by the session hooks: entry (who, when, branch, starting hash), summary (one to three lines) and exit (result and the next step released); a step without exit blocks the next entry. | Cycle 070 |
| **Outbox** | — | The SQLite queue (`fila`, WAL mode) that sessions on one machine use to message each other without a broker; the hooks read and drain it. | Cycle 070 |
| **Chamado** | — | A ticket: one folder `specs/<id>/` with `00-chamado.md` and one file per gate verdict; the aggregate root of the panel (`DOM:aggregate=Chamado`, cycle 068). | Cycle 068 |
| **Gate (G0–G9)** | — | One checkpoint of a chamado with one deliverable file; its state (ok, bad, run, falta, na) is derived from the files, never typed. | Cycle 068 |
| **Veredito** | — | The verdict file of a gate (`Gn-<papel>-<crítico>-<hash>.md`) with a mandatory header; the latest-dated one on the right hash is the one in force (see **Veredito vigente**, cycle 069). | Cycle 068 |
| **Conferidor** | — | The rule set that derives a chamado's gate state (header format, author ≠ critic, date not after the file's commit, runner2 clean); pure functions in `painel/chamados.py`. | Cycle 068 |
| **runner2** | — | The clean-clone test run of a hash on the Linux runner; counts only with 0 failed and 0 errors. | Cycle 068 |
| **pendente:** | — | An open item declared inside a verdict; it lets the gate pass but blocks G8 (production order) until accepted. | Cycle 068 |
| **Classe C** | — | The risk class of a chamado that needs an ADR and the owner's decision before G8. | Cycle 068 |
| **Trilha** | — | The audit trail of a chamado for people and agents: each gate's text in order, with the session cost of each step beside it. | Cycle 068 |
| **Custo por sessão** | — | Token counts per Claude Code session, read incrementally (by byte offset) from the session transcripts into a local index; counts only, never content. | Cycle 068 |
| **Aggregate root** | — | The entity that owns an invariant and is the only entry point to change it; the plan names which one(s) a cycle touches (`DOM:aggregate=`). | Cycle 067 |
| **Declared domain model** | — | The four decisions a plan makes explicit — aggregate root, where the invariants live, ubiquitous-language changes, ports and adapters — read by `check-conformance.sh` from cycle 067 on; silence is not a decision. | Cycle 067 |
| **Invariant** | — | A business rule that must always hold; it lives in the domain (aggregate, value object, domain service) or, with a stated reason, at the edge (route, adapter, screen) — `DOM:invariants=`. | Cycle 067 |
| **Port / adapter** | — | A port is the interface the domain exposes or needs; an adapter implements it for one technology (HTTP, SQLite, a CLI). The plan declares the ones a cycle changes (`DOM:ports=`). | Cycle 067 |
| **Ubiquitous language** | — | The shared vocabulary of a bounded context, written down (this glossary) and used verbatim in code, specs and conversation; the plan declares the terms it adds or changes (`DOM:glossary=`). | Cycle 067 |
| **Painel de regência** (*regency panel*) | Regency panel | The local read-model where the human sees the queue, the chamados per gate and the journey; it never promotes and never decides. | Cycle 072 |
| **Pedido de decisão** (*decision request*) | Decision request | A question escalated to the human: id, who asked, options, recommendation, deadline, what it unblocks and the destination. | Cycle 072 |
| **Ruling** | — | The recorded answer to a decision request — human author, date, addressee and a link to the merge/ADR; a ruling without an author or an addressee is refused. | Cycle 072 |
| **Veredito normalizado** (*normalized verdict*) | Normalized verdict | The canonical mapping — approved / returned / red-proved / running / invalid — written **beside** the original verdict, never in its place. | Cycle 072 |
| **Portão do regente** (*regent's gate*) | Regent's gate | G7, G8 and `TAIL:gate` — the gates only the human records; a derived item of the queue, read-only for an agent. | Cycle 072 |
| **Agente (perfil)** (*agent profile*) | Agent profile | The **profile ↔ executable** pair a session runs on — the file under `.claude/agents/` (listed by `ls .claude/agents`), with its role, tools and default model. It is what the **Administração registers and lists** (`docs/agents/*.md` is the profile doc; the versioned file is the registration). It is **not** a **Sessão de agente** and carries **no ref**: the *sessão* is one execution, identified by `nome · ref · projeto` (**Ref de sessão**); the *agente* is the profile that occupies it — hence name collision at §7, line 295. | Cycle 073 (correction 2) |
| **Sessão de agente** (*agent session*) | Agent session | One execution of an agent that the human starts, watches and takes down — **the unit of administration**. It is not **agente** — see **Agente (perfil)**: the *agente* is the profile ↔ executable pair which occupies it (the Administração registers the *agente*, the Workflow follows the *sessão*), so name collision at §7, line 295. | Cycle 073 |
| **Estado do agente vivo** (*live agent state*) | Live agent state | The session's current state — working / waiting / no task / blocked — detected from the **process**, not from a heartbeat alone. | Cycle 073 |
| **Tarefa aberta** (*open task*) | Open task | The task an agent is on **right now**, per agent, with a `start` and no `stop`. | Cycle 073 |
| **Consumo por agente** (*per-agent usage*) | Per-agent usage | Tokens per **agent**, not only per session or per model — the finer grain of **Custo por sessão** (cycle 068). | Cycle 073 |
| **Limite de orçamento** (*budget limit*) | Budget limit | The consumption ceiling of a session or of a project — **executable**, not merely declared. From cycle 073 correction 3 it is read as **declare the ceiling + warn**, with the **Emissor do aviso** drawn; the **cut** (refuse, suspend) stays later. | Cycle 073 |
| **Catálogo de skills/ferramentas/modelos** (*skill/tool/model catalog*) | Skill/tool/model catalog | The **queryable** registry of skills, tools and **models** per project (today: skills as folders, models chosen per session). | Cycle 073 |
| **Mensagem entre agentes** (*agent-to-agent message*) | Agent-to-agent message | An **addressed** exchange between sessions, through an artifact or the *outbox* — **never chat**. It rides the **Outbox** queue (cycle 070); that store is the *fila (outbox)*, never the *fila de decisões* of Regência — two deposits, two owners (see **Colisão de nomes**, line 292). | Cycle 073 |
| **Protocolo de intercomunicação** (*intercommunication protocol*) | Intercommunication protocol | The protocol by which agents expose and consume tools (**MCP**, *Model Context Protocol*) and talk to their peers (**A2A**, *agent-to-agent*). | Cycle 073 |
| **Caixa de entrada** (*inbox*) | Inbox | The **named view** of what arrived for a session and has not been read or drained. It belongs to Mensageria; the panel's **Fila** screen is Regência's entrance of *decisões* — same word, another context (see **Colisão de nomes**, line 293). | Cycle 073 |
| **Livro de mensagens** (*message ledger*) | Message ledger | The **append-only**, unified record of the messages between sessions. It is not the **Task ledger** (`docs/records/tarefas.jsonl`, cycle 065) — that one is the *livro de ponto*: tokens, cost and attempts per task (see **Colisão de nomes**, line 294). | Cycle 073 |
| **Roteamento por nome/ref** (*name/ref routing*) | Name/ref routing | Addressing a message or a task to a session by **name or reference**, through a resolution table. | Cycle 073 |
| **Colisão de nomes** (*name collision*) | Name collision | Two sessions, agents or skills under one name, and the rule that prevents it — today only **ids** have such a rule. The **five live collisions** are listed, with evidence, in `specs/073-area-administrativa/confronto/mapa-de-contextos.md` §7: "fila" (*fila de decisões* × *fila (outbox)*, line 292); "caixa de entrada" (Regência's **Fila** screen × Mensageria's inbox, line 293); "livro de ponto" (**Task ledger** × **Livro de mensagens**, line 294); "sessão" × "agente" (**Sessão de agente**, line 295); "portão" (the **chamado**'s gate × the **Portão do regente**, line 296 — Regência reuses the first through an **anticorruption layer**, §4 relationship 4). Operative rule: **"fila" and "portão" are never written bare.** | Cycle 073 |
| **Colisão de endereço** (*address collision*) | Address collision | The same **identifier** pointing at two sessions, or at none any more — one name under several refs, one name under two projects, a **Ref de sessão** gone stale after a restart. It is **not** a **Colisão de nomes**: that one is a *word* with two meanings (§7 of the map); here the *address itself* is ambiguous. Invariant: **an ambiguous address is refused, never resolved** — a delivery to the wrong peer cannot be undone. Classes and evidence: `specs/073-area-administrativa/confronto/mapa-de-contextos.md` (decision 3, cycle 073 correction 1). | Cycle 073 (correction 1) |
| **Ferramenta MCP como escopo de política** (*MCP tool as policy scope*) | MCP tool as policy scope | Who may call which **MCP** tool is a **scope of the `allow`/`deny`/`ask` policy per agent** — not a screen of its own: the policy rule names the tool as its scope, and every tool of the intercommunication screen points back to that rule (decision D2, cycle 073 correction 3). | Cycle 073 (correction 3) |
| **Emissor do aviso** (*warning emitter*) | Warning emitter | The panel's **usage ingestion** (`painel/custo.py`) that compares measured usage with the **ceiling** and the **threshold** declared in the Administração and, on crossing the threshold, **enqueues a message** in the **fila (outbox)** addressed to the owning session and to the regent (`nome · ref · projeto`) — *a late warning, never a lost one*. The **cut** (refuse, suspend) stays later and is not the emitter's job. Drawn in `administracao-03-orcamento.html`, § "Quem emite o aviso" (decision D3, cycle 073 correction 3). | Cycle 073 (correction 3) |
| **Ref de sessão** (*session ref*) | Session ref | The short reference of a session — the `[xxxxxx]` the harness shows beside the name (`ListAgents`). It is the field that tells two same-named sessions apart, and the only one that **expires**: **the ref changes when the session restarts**. Hence session identity is written **`name · ref · project`** (decision 2, cycle 073 correction 1), and every action that names a session carries that warning. | Cycle 073 (correction 1) |
