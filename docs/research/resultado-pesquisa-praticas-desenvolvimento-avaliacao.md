# Avaliação do estudo "Melhores práticas de desenvolvimento de software — modelo humano + agentes de IA"

- **Data**: 2026-07-22 · **Método**: pesquisa profunda inline (fan-out de buscas +
  leitura de fontes primárias), sem PDF externo. Prompt em
  `prompt-pesquisa-praticas-desenvolvimento.md`.
- **Objetivo**: fundamentar o modelo operacional (papéis, cerimônias, entregáveis,
  artefatos) para "1 humano orquestrando N agentes de IA".

## Síntese

A prática de ponta (2024–2026) convergiu em algo que valida a fundação desta
plataforma: **quando o agente escreve o código, o artefato central deixa de ser o
código e passa a ser a especificação** — "a especificação, não o prompt nem o código,
é onde a intenção humana de fato vive" (GitHub, Spec Kit). O papel do humano muda de
"escrever" para **dirigir e verificar**: "seu papel primário é dirigir; o agente faz
o grosso da escrita" e "a cada fase você reflete e refina" (GitHub).

Três eixos sustentam o modelo:

1. **Processo enxuto orientado a ciclos, não a papéis inflados.** Kanban e Shape Up
   provam que time pequeno não precisa da cerimônia do Scrum completo; Shape Up
   elimina backlog e stand-up diário e trabalha por apetite fixo + escopo variável.
2. **Evidência acima de folclore.** DORA/SPACE mostram que velocidade e estabilidade
   **não são trade-off** — "o trade-off real, no longo prazo, é entre software melhor
   mais rápido e software pior mais devagar" — e que as 4 métricas são *resultados*
   de capacidades subjacentes (CI, trunk-based, testes, revisão).
3. **O gate humano é o contrapeso inegociável.** Todo fluxo agentic sério — Anthropic,
   Claude Code, GitHub SDD — mantém o humano no ponto de decisão para o que é caro de
   reverter, e usa **verificação independente** (revisor em contexto fresco) porque
   "quem faz o trabalho não deve ser quem o corrige".

**Máxima do estudo**: *IA para explorar, propor e escrever; humano para especificar,
decidir e aprovar; testes, gates e revisão independente para validar.*

## Por tópico (achado + veredito para solo+IA)

### 1. Frameworks de processo (Scrum, Kanban, Scrumban, Shape Up, XP, Lean)
- **Scrum** define 3 papéis (PO, Scrum Master, Dev Team) e 4 eventos (planning, daily,
  review, retro) + artefatos (product/sprint backlog, increment) — desenhado para
  time cross-funcional de ~5–9 pessoas. **Kanban** não prescreve papéis nem
  cerimônias: foca em visualizar o fluxo e limitar WIP. **Shape Up** (Basecamp) troca
  sprints por **ciclos de 6 semanas + 2 de cooldown**, papéis **shapers/builders**,
  **apetite** (tempo fixo, escopo variável) e **betting table sem backlog**.
- **Veredito solo+IA**: adotar o **esqueleto Shape Up + Kanban**, não Scrum. Apetite
  fixo por ciclo mapeia direto no nosso "diffs pequenos + YAGNI"; WIP limitado mapeia
  no fluxo spec-kit uma-feature-por-vez. Scrum Master e daily de time são **cerimônia
  de papel** aqui (não há time para sincronizar). Manter só o *shaping* (nossa spec) e
  o *cooldown* (janela de dívida/manutenção).

### 2. Engenharia de alto desempenho (DORA, SPACE, trunk-based, CI/CD)
- As métricas DORA (deployment frequency, lead time, change fail rate, failed-deploy
  recovery — hoje com *rework rate* como 5ª) são **outcomes**, dirigidos por
  capacidades: CI, trunk-based development, testes automatizados, revisão de código,
  deploys pequenos. "Velocidade e estabilidade não são trade-off." SPACE amplia para
  Satisfação/Performance/Atividade/Comunicação/Eficiência; DX Core 4 é o mais
  prescritivo. **Alerta**: métricas como "PRs por dev" incentivam comportamento
  nocivo se usadas para avaliar indivíduo.
- **Veredito solo+IA**: usar DORA como **bússola de saúde do fluxo**, não como painel
  de RH (não há a quem comparar). Lead time e change fail rate são os dois que
  importam para um solo: "consigo levar uma spec a produção rápido e sem quebrar?".
  Trunk-based + CI verde como gate já são princípio da constituição (V) — a evidência
  confirma. Instrumentação pesada de métricas é **YAGNI** na fase atual.

### 3. NÚCLEO — Desenvolvimento aumentado por IA
- **Spec-Driven Development**: fases specify → plan → tasks → implement; a spec é
  "verdade executável"; prompt vago "força o modelo a adivinhar milhares de
  requisitos não ditos". É exatamente o nosso Spec Kit.
- **Fluxo agentic (Claude Code)**: **explore → plan → code → commit**; "separe
  pesquisa/planejamento da implementação para não resolver o problema errado".
  Verificação é central: "dê ao agente um teste que ele mesmo possa rodar — é a
  diferença entre uma sessão que você vigia e uma da qual você se afasta". Padrões:
  **Writer/Reviewer** (um agente escreve, outro revisa em contexto fresco),
  **subagentes** para investigação/verificação, **revisão adversarial do diff** antes
  de dar por pronto, `CLAUDE.md`/`AGENTS.md` como contexto persistente, gerenciamento
  agressivo de contexto (`/clear` entre tarefas).
- **Orquestração (Anthropic "building effective agents")**: distinção
  **workflow** (caminhos de código predefinidos) × **agent** (o LLM dirige o próprio
  processo); 6 padrões: prompt chaining, routing, parallelization, orchestrator-
  workers, evaluator-optimizer, autonomous. "Comece simples; adicione complexidade só
  quando o simples comprovadamente falha" e "revisão humana permanece crucial em
  agentes de código".
- **Riscos/contramedidas**: alucinação de comandos → `CLAUDE.md` com build/test reais;
  "trust-then-verify gap" (código plausível que não trata edge cases) → sempre prover
  verificação, "se não dá para verificar, não faça deploy"; over-engineering do
  revisor → instruir a sinalizar só o que afeta correção/requisito; escopo largo →
  "se um loop precisa de +30 turnos, o escopo está largo ou o critério de pronto não
  está claro".
- **Veredito solo+IA**: este é o coração do nosso modelo operacional. Os "papéis"
  clássicos viram **modos de agente com gate humano**: specify/plan = humano + agente
  (decisão humana), implement = agente, verify/review = **agente independente +
  humano**. A revisão adversarial em contexto fresco é o substituto direto do
  "segundo par de olhos" de um time.

### 4. Papéis, responsabilidades e RACI
- Time minúsculo pode **acumular papéis**, desde que preserve os **contrapesos**:
  quem *decide* (accountable) ≠ quem *executa* ≠ quem *verifica*. É o risco de
  colapsar tudo numa pessoa: perde-se o revisor.
- **Veredito solo+IA**: mantemos a separação **movendo o "verifica" para o agente
  independente** e o "decide" sempre no humano. RACI vira uma matriz **humano × classe
  de agente** (spec-agent, plan-agent, dev-agent, review-agent, qa-agent), com o
  humano como *Accountable* fixo em todas as linhas de risco (casa com as classes de
  risco do Princípio IV).

### 5. Cerimônias — o que preservar, o que cortar
- Propósito real: planning (comprometer escopo), daily (sincronizar/desbloquear),
  review (inspecionar incremento com stakeholder), retro (melhorar o processo),
  refinement (preparar backlog). Kanban/Shape Up mostram que **daily e planning de
  sprint são descartáveis** em fluxo contínuo.
- **Veredito solo+IA**: cortar daily e sprint planning. **Preservar**: (a) *shaping/
  spec* (= planning real), (b) *checkpoint de ciclo* (review do que entrou +
  cooldown), (c) **retro individual leve** por ciclo (o que os agentes erraram →
  vira regra em `CLAUDE.md`/constituição). Retro é a cerimônia de maior ROI num
  modelo com IA: cada correção recorrente deve virar instrução versionada.

### 6. Entregáveis e artefatos
- Taxonomia moderna: Vision/PRD → spec → tasks → ADR (Nygard: "decisão + contexto +
  consequências", arquivo markdown numerado) → RFC/design doc → **Definition of
  Ready/Done** → runbook → changelog/release notes → **docs-as-code / living
  documentation** (o problema é "tratar doc como atividade separada; quando a doc mora
  num wiki desconectado do código, não há força que a mantenha atualizada") → **C4**
  (Context/Container/Component/Code) + journey maps.
- **Veredito solo+IA**: quase tudo isso já existe no repo em alguma forma (spec.md,
  plan.md, tasks.md, docs/adr/, docs/journeys/, linguagem-ubiqua). O que **falta
  formalizar** é: **Definition of Ready/Done explícitas**, **runbook** (já há
  `docs/infra/runbook-fase1.md`), **changelog/release notes**, e o **catálogo de
  artefatos com dono (humano/agente) e gate**. C4 é **candidato fase 2** (hoje
  mermaid + linguagem-ubiqua bastam — YAGNI).

### 7. Qualidade e Definition of Done
- Quality gates no CI; **test pyramid × testing trophy** (mais testes de integração
  no trophy); TDD/BDD; cobertura *pragmática*; DevSecOps leve (SAST/DAST, secret
  scanning). Um agente satisfaz um DoD **verificável**: teste verde, build, lint,
  screenshot.
- **Veredito solo+IA**: já temos test-first + fitness functions (Princípio V). Falta
  **redigir a DoD como checklist verificável por agente** (o que fecha um Stop-hook/
  `/goal`) e incluir gate de segurança leve (secret scanning + revisão de injeção,
  que o Princípio IV já exige no runtime — trazer para o CI).

### 8. Governança leve e rastreabilidade
- Constituições/working agreements, ADRs e RFCs como memória de decisão;
  documentation-first; rastreabilidade **spec ↔ código ↔ teste**. ADRs ligados a
  componentes C4 dão rastreabilidade decisão→sistema.
- **Veredito solo+IA**: temos constituição + ADRs. Falta tornar a **rastreabilidade
  explícita** (spec NNN → PR → teste → journey) como parte da DoD, e um **índice de
  decisões** navegável.

## O que valida nas nossas definições

- **Spec-Driven é o consenso de ponta** — nosso Spec Kit + constituição não é
  idiossincrasia, é a prática recomendada quando agentes escrevem código.
- **Test-first + CI + fitness functions** (Princípio V) são exatamente as capacidades
  que a pesquisa DORA associa a alto desempenho.
- **Gate humano + revisão independente** (nossa "revisão humana ou agente revisor")
  é o contrapeso que todos os fluxos agentic sérios mantêm.
- **YAGNI / diffs pequenos / "prove não declare"** casam com "comece simples",
  "apetite fixo, escopo variável" e "mostre evidência, não afirme sucesso".

## O que complementa (ações — entram na Fase 2)

1. **Modelo operacional explícito** (`docs/governance/operating-model.md`): papéis
   como matriz humano × agentes, cerimônias mínimas (shaping, checkpoint de ciclo,
   retro), catálogo de artefatos com dono e gate — **este é o entregável da Fase 2**.
2. **Definition of Ready e Definition of Done** verificáveis (checklist que um agente
   consegue satisfazer e um Stop-hook consegue conferir).
3. **Mapa de gates humanos inegociáveis** (onde o humano DEVE aprovar), reaproveitando
   a taxonomia de classes de risco do Princípio IV.
4. **Cadência por ciclo estilo Shape Up** (apetite + cooldown) sobreposta ao spec-kit,
   sem adotar backlog nem daily.
5. **Candidatos fase 2 (não agora — YAGNI)**: C4 formal, instrumentação de métricas
   DORA, RFC process pesado. Registrar como observados, não adotar.

## Ressalvas

- Boa parte da literatura pressupõe **time multi-pessoa**; a transposição para
  solo+IA (colapsar papéis preservando contrapesos via agente independente) é **nossa
  síntese**, não um padrão pronto citável — é o valor agregado desta pesquisa.
- DORA/SPACE foram medidos em organizações; para um solo servem como **bússola
  qualitativa**, não como benchmark comparativo.
- Fluxos agentic evoluem rápido (2025–2026); as fontes primárias (Anthropic, GitHub)
  são as mais estáveis; posts de terceiros foram usados só para triangular consenso.

## Fontes da pesquisa

- GitHub Blog — *Spec-driven development with AI* (2025-09-02):
  https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/
- GitHub Spec Kit (repo): https://github.com/github/spec-kit
- Anthropic / Claude Code — *Best practices*:
  https://code.claude.com/docs/en/best-practices
- Anthropic — *Building effective agents*:
  https://www.anthropic.com/engineering/building-effective-agents
- DORA — *DORA metrics (four keys)*: https://dora.dev/guides/dora-metrics-four-keys/
- Basecamp — *Shape Up* (cap. 2, shaping): https://basecamp.com/shapeup/1.1-chapter-02
- Swarmia — *Comparing DORA, SPACE and DX Core 4*:
  https://www.swarmia.com/blog/comparing-developer-productivity-frameworks/
- Michael Nygard — *Documenting Architecture Decisions* (ADR original):
  https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- Simon Brown — *C4 model*: https://c4model.com/
- (Triangulação de consenso) TrueFoundry, thebcms, MindStudio, Reintech, Graph AI,
  Luca Mezzalira (ver `fontes-consultadas.md`).
