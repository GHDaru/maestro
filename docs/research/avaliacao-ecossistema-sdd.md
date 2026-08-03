# Avaliação do ecossistema SDD — Superpowers, BMAD, Kiro, Taskmaster, Agent OS e afins

> Ficha de pesquisa (papel `research-curator`) · Ciclo: spec 007 · Data: 2026-07-30
> Pergunta: **que ferramentas/metodologias de Spec-Driven Development e toolkits de agentes
> existem além do Spec Kit (adotado) e OpenSpec (descartado, ADR 0005), e o que o Maestro
> deve adotar, absorver, observar ou descartar?**
> Decisão consolidada: **ADR 0008**. Critério de veredito: conflito com princípio → descarta;
> ideia boa sem a ferramenta → absorve (com artefato-destino); complementar e maduro → adota
> (spec própria); imaturo/incerto → observa (com gatilho).

## Contexto do mercado (2026)

O ecossistema explodiu: análises comparativas listam **15 a 30+ frameworks SDD** ativos.
Os que dominam a conversa séria: **Spec Kit (GitHub, ~90k stars)**, **OpenSpec (~52k)**,
**BMAD-METHOD (~47k)**, **Superpowers (~93k)**, além de Kiro (AWS), GSD, Tessl, Agent OS.
A diferença estrutural entre eles: spec como **documento que o agente lê** vs. spec como
**infraestrutura operacional que coordena agentes** ao longo do SDLC.

---

### 1. Superpowers (obra/superpowers — Jesse Vincent)

- **O que é**: biblioteca de skills + metodologia para agentes de código; a mais popular do
  ecossistema Claude Code (~93k stars; entrou no marketplace oficial da Anthropic em 2026). MIT.
- **Mecânica central**: skills compostas em Markdown que **disparam automaticamente por
  contexto** (sem invocação manual): brainstorming socrático → git worktree isolado → plano
  em tasks de 2–5 min → execução por **subagentes com review em 2 estágios** → **TDD
  RED-GREEN-REFACTOR obrigatório** → code review → merge/PR.
- **O que faz bem**: workflows **mandatórios** (não sugestões); disciplina TDD real;
  "subagent-driven development" com contexto fresco por task.
- **Onde conflita com o Maestro**: é uma **metodologia completa** — adotá-la inteira criaria
  duas fontes de verdade de processo (conflito com ADR 0005: uma ferramenta só). Muito do
  que oferece já temos com outro nome: brainstorming ≈ `/speckit.clarify`; subagente com
  review fresco ≈ nosso `review`; skills por contexto ≈ nosso padrão agentskills.io.
- **Veredito**: **absorver ideias + observar como referência**. Ideias absorvidas:
  (a) **git worktree isolado por task** → candidato a script/skill na F3 (destino:
  `scripts/`/`skills/`, quando houver dor real de paralelismo); (b) **rigor "mandatório vs.
  sugestão"** nas nossas skills → reforço na skill `verifiable-dod` e nos system prompts.
  Não adotar por atacado.
- **Fontes**: https://github.com/obra/superpowers ·
  https://augmentclaude.com/s/superpowers-obra ·
  https://rywalker.com/research/superpowers-skills-framework

### 2. BMAD-METHOD (bmad-code-org)

- **O que é**: "Breakthrough Method for Agile AI-Driven Development" (~47k stars, v6, open
  source). Organiza **12+ agentes como um time ágil** (PM, Arquiteto, Dev, QA, SM…) com
  artefatos ágeis (PRD, épicos, stories) e handoffs por arquivo.
- **Mecânica central**: planejamento agêntico up-front (PRD + arquitetura) → "shard" em
  **story files** com contexto focado → agentes especializados executam → QA gates.
- **O que faz bem**: torna a colaboração humano-IA reconhecível para times ágeis; contexto
  focado por story (mesmo insight do nosso "cada agente estreito").
- **Onde conflita**: é um **concorrente integral** do nosso modelo (papéis + cerimônia +
  artefatos próprios); adotá-lo substituiria o Maestro, não o complementaria. Cerimônia
  scrum-like que já descartamos (§10 do modelo operacional). Análises apontam custo de token
  alto (o mais caro dos comparados). Nossos 12 agentes já cobrem os papéis.
- **Veredito**: **descartar adoção**. Nenhuma ideia essencial não coberta: "story file com
  contexto focado" ≈ nosso `tasks.md` por fronteira + Princípio V.
- **Fontes**: https://github.com/bmad-code-org/BMAD-METHOD · https://docs.bmad-method.org/ ·
  https://www.augmentcode.com/guides/bmad-method-ai-development

### 3. Kiro (AWS)

- **O que é**: IDE agêntica proprietária da AWS, aposta "spec-first": prompt → três
  arquivos: `requirements.md` (user stories com critérios em **EARS**), `design.md`
  (arquitetura, diagramas), `tasks.md` (tasks sequenciadas com dependências). + steering
  (padrões do projeto) e hooks.
- **O que faz bem**: **EARS (Easy Approach to Requirements Syntax)** — critérios de aceite
  no padrão `WHEN <condição> THE SYSTEM SHALL <comportamento>`: testável por construção,
  vira teste quase 1:1. Estrutura requirements/design/tasks espelha nosso spec/plan/tasks.
- **Onde conflita**: ferramenta **proprietária, presa a uma IDE** e ao ecossistema AWS —
  contra nossa reversibilidade (lock-in) e contra o motor único (Spec Kit).
- **Veredito**: **absorver ideia (EARS), descartar a ferramenta**. Destino concreto: sintaxe
  EARS entra como **forma recomendada de critério de aceite** na skill `verifiable-dod` e
  no `spec-template` (F4 da vendorização).
- **Fontes**: https://kiro.dev/docs/specs/ · https://kiro.dev/docs/specs/feature-specs/ ·
  https://aws.plainenglish.io/what-is-spec-driven-development-and-how-to-implement-it-with-kiro-b5846bd55869

### 4. Taskmaster AI (eyaltoledano/claude-task-master)

- **O que é**: sistema de gestão de tasks para desenvolvimento com IA (MCP + CLI), plugável
  em Cursor/Claude Code/etc. Faz parse de PRD → `tasks.json` com **dependências mapeadas,
  scores de complexidade e validação de dependência circular**.
- **O que faz bem**: grafo de dependências explícito e validável; bom para projetos com
  muitas tasks paralelas.
- **Onde conflita**: nosso `tasks.md` (leve, por fronteira, WIP=1) cobre a necessidade
  atual; adotar um gerenciador com 36 tools MCP (~21k tokens de overhead) viola YAGNI e
  economia de contexto para o nosso porte.
- **Veredito**: **observar**. Gatilho de reavaliação: quando um ciclo tiver >20 tasks
  paralelas ou múltiplos projetos simultâneos e a ordenação manual doer (registrar em retro).
- **Fontes**: https://github.com/eyaltoledano/claude-task-master ·
  https://github.com/eyaltoledano/claude-task-master/blob/main/docs/task-structure.md

### 5. Agent OS (buildermethods/agent-os — Brian Casel)

- **O que é**: sistema open source para **injetar padrões do codebase** (standards) +
  contexto de produto + instruções de execução em qualquer agente (Claude, OpenAI…);
  v3 focada em descobrir e documentar standards de codebases existentes/legadas.
- **O que faz bem**: separação clara **standards / product / specs** como camadas de
  contexto; foco em reduzir "drift" do agente em código legado.
- **Onde conflita**: nossa pilha CLAUDE.md/AGENTS.md + Constituição + linguagem ubíqua já
  cumpre o papel de standards-injection para o nosso porte; adotar seria camada redundante.
- **Veredito**: **absorver ideia parcial + observar**. Ideia absorvida: quando o Maestro
  reger um projeto com código de produto, manter **standards por camada em arquivo próprio**
  (destino: template de `docs/standards/` na F4, se a dor aparecer). Gatilho de reavaliação:
  onboarding do método em codebase legado grande.
- **Fontes**: https://github.com/buildermethods/agent-os · https://buildermethods.com/agent-os/v2

### 6. GSD — "Get Shit Done" (achado da varredura)

- **O que é**: framework SDD low-ceremony nativo de Claude Code (~61k stars nas análises de
  2026), foco em onboarding rápido e custo baixo.
- **Veredito**: **observar**. A proposta (pouca cerimônia para mudanças simples) é o que a
  nossa **raia leve** já faz dentro do Spec Kit; sem lacuna a preencher hoje.
- **Fontes**: https://www.marktechpost.com/2026/05/08/9-best-ai-tools-for-spec-driven-development-in-2026-kiro-bmad-gsd-and-more-compare/ ·
  https://medium.com/@wasowski.jarek/comparing-15-spec-driven-development-frameworks-artifacts-and-decision-paths-sdd-c052df529274

### 7. Tessl (achado da varredura)

- **O que é**: framework "spec-as-source" — instala "tiles" em `.tessl/` e ensina qualquer
  agente MCP a tratar a spec como **artefato executável** (o código deriva da spec
  continuamente), não documento lido uma vez.
- **Veredito**: **observar**. A tese (spec viva > spec documento) é alinhada ao nosso
  Princípio VI, mas a ferramenta é comercial/imatura para apostar. Gatilho: maturidade +
  case público de produção.
- **Fontes**: https://www.softwareseni.com/the-30-plus-framework-landscape-navigating-spec-driven-development-options-in-2026/ ·
  https://www.augmentcode.com/tools/best-spec-driven-development-tools

---

## Síntese (o quadro de vereditos)

| Ferramenta | Veredito | O que fica no Maestro | Registro |
|---|---|---|---|
| Spec Kit (GitHub) | ✅ **adotada** (já) | motor do fluxo; vendorizar na F4 | ADR 0005 |
| OpenSpec | ❌ descartada (já) | ideia absorvida: raia leve (delta) | ADR 0005 |
| **Superpowers** | 🔄 absorver ideias + observar | worktree/task (F3 futura); rigor mandatório nas skills | ADR 0008 |
| **BMAD-METHOD** | ❌ descartar adoção | nada essencial não coberto | ADR 0008 |
| **Kiro (AWS)** | 🔄 absorver **EARS**; descartar ferramenta | EARS na skill `verifiable-dod` + spec-template (F4) | ADR 0008 |
| **Taskmaster** | 👁 observar | gatilho: >20 tasks paralelas / multi-projeto | ADR 0008 |
| **Agent OS** | 🔄 absorver parcial + observar | standards por camada (se codebase de produto) | ADR 0008 |
| **GSD** | 👁 observar | raia leve já cobre | ADR 0008 |
| **Tessl** | 👁 observar | gatilho: maturidade/case de produção | ADR 0008 |

**Avaliação crítica (não só colagem):** o padrão do mercado confirma as apostas do Maestro —
(1) spec como fonte de verdade, (2) contexto estreito por agente/task, (3) gates de
qualidade. Onde o mercado nos desafia: **EARS** dá forma sintática ao nosso "critério
testável" (adotamos a ideia), e **Superpowers** mostra que skill mandatória > skill
sugestiva (reforçamos as nossas). Onde não nos movemos: frameworks integrais (BMAD) e
ferramentas proprietárias (Kiro) conflitam com princípios — descartados com racional, como
o OpenSpec.

**Incerteza declarada:** números de stars/custo vêm de análises de terceiros (2026) — ordem
de grandeza confiável, valor exato não auditado.
