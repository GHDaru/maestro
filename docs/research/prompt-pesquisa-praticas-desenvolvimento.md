# Prompt para pesquisa profunda — Melhores práticas de desenvolvimento de software (modelo humano + agentes de IA)

> Gerado em 2026-07-22 para embasar a definição do **modelo operacional** da
> plataforma (papéis, responsabilidades, cerimônias, entregáveis e artefatos).
> Resultado será consolidado em `docs/governance/modelo-operacional.md` e em ADR.

---

## PROMPT

Sou **desenvolvedor solo auxiliado por agentes de IA** (Claude Code e compatíveis)
construindo uma plataforma SaaS white-label multi-tenant de conhecimento e trabalho
assistido por IA. Preciso de um **estudo das melhores práticas de desenvolvimento de
software (2024–2026)** que fundamente a definição de um **modelo operacional** —
QUEM faz O QUÊ (papéis e responsabilidades), QUANDO (cerimônias/cadência) e O QUE
produz (entregáveis e artefatos) — para um contexto em que **um humano orquestra
múltiplos agentes de IA** que assumem parte dos papéis tradicionais de um time.

### Contexto (não re-pesquisar; apenas integrar)

- Fluxo já adotado: **Spec-Driven Development** via Spec Kit
  (`/speckit.specify → clarify → plan → tasks → implement`), specs numeradas em
  `specs/NNN-*`, constituição versionada como fonte de verdade.
- Princípios já ratificados: DDD + arquitetura hexagonal; **test-first** com
  fitness functions no CI; modularidade plugável; contratos API+MCP; design system
  + camada semântica de interface; documentação viva de jornadas; ADRs para decisões.
- Restrição cultural: **YAGNI**, diffs pequenos, "prove, não declare" (evidência:
  teste verde/build/screenshot), sem mudança silenciosa de escopo.

### O que pesquisar (com comparação, evidência e veredito por tópico)

1. **Frameworks de processo e sua anatomia de papéis/cerimônias/artefatos**:
   Scrum, Kanban, Scrumban, **Shape Up (Basecamp)**, XP, Lean/Lean Software
   Development, SAFe (só o que escala para baixo). Para cada um: papéis, eventos/
   cerimônias, artefatos e **em que tamanho de time faz sentido** — destacando o que
   sobrevive num contexto solo/duo.

2. **Práticas de engenharia de alto desempenho (evidência empírica)**: **DORA**
   (4 key metrics + capabilities), **SPACE framework** de produtividade, Accelerate
   (State of DevOps), trunk-based development, CI/CD, feature flags, code review,
   pair/mob programming. O que a evidência diz que causa performance vs. o que é
   folclore.

3. **Desenvolvimento assistido/aumentado por IA (o núcleo do estudo)**:
   - **Spec-Driven Development** com agentes (GitHub Spec Kit, Kiro, Tessl,
     "specs as source of truth"); por que specs viram o artefato central.
   - **Agentic coding workflows**: human-in-the-loop, plan-then-execute,
     verificação/gates automáticos, revisão de PR por agente, orquestração de
     múltiplos agentes (paralelo/pipeline), sub-agentes especializados.
   - Fluxos de referência (ex.: Addy Osmani DEFINE→PLAN→BUILD→VERIFY→REVIEW→SHIP;
     Anthropic "harness design"/context engineering; padrões de "explore–plan–code–
     commit"). Como os papéis clássicos (PO, dev, QA, revisor, tech writer) se
     redistribuem entre humano e agentes.
   - Riscos e contramedidas: alucinação, drift de escopo, dívida técnica silenciosa,
     over-engineering por IA, perda de contexto; **quais gates humanos são
     inegociáveis**.

4. **Papéis e responsabilidades**: definição moderna de Product Owner/Manager,
   Tech Lead, Engenheiro, QA/SDET, UX/UI, DevOps/Platform, Arquiteto, Tech Writer;
   **RACI** e como colapsar/acumular papéis num time minúsculo sem perder os
   contrapesos (quem decide, quem executa, quem verifica).

5. **Cerimônias/cadência**: propósito real de cada evento (planning, daily,
   review, retro, refinement/grooming, backlog), timeboxing, e **como um solo+IA
   preserva o valor de cada cerimônia** (ex.: retro individual, "daily" como
   checkpoint de agente). O que cortar sem perda.

6. **Entregáveis e artefatos**: taxonomia de artefatos de um ciclo de vida moderno
   — Vision/Product brief, PRD/spec, backlog, ADR, design docs/RFC, **Definition of
   Ready/Done**, runbook, changelog, release notes, test plan, **docs-as-code /
   living documentation**, C4/diagramas, journey maps. Quais são essenciais vs.
   cerimônia de papel.

7. **Qualidade e Definition of Done**: quality gates, test pyramid vs. testing
   trophy, TDD/BDD, cobertura pragmática, revisão de código, segurança no ciclo
   (DevSecOps, SAST/DAST leve), como um agente satisfaz um DoD verificável.

8. **Governança leve e gestão do conhecimento**: constituições/working agreements,
   ADRs, RFCs, documentation-first, gestão de decisões e rastreabilidade
   spec↔código↔teste — como manter coerência em desenvolvimento assistido por IA.

### Formato de saída desejado

- Por tópico: síntese + tabela (prática/framework × papéis × cerimônias × artefatos ×
  tamanho de time onde faz sentido × veredito para solo+IA).
- **Modelo operacional recomendado, consolidado** para "1 humano orquestrando N
  agentes": lista fechada de papéis (com quem os exerce — humano/agente), cerimônias
  mínimas com cadência, e catálogo de entregáveis/artefatos com Definition of Done.
- **Mapa de gates humanos inegociáveis** (onde o humano DEVE decidir/aprovar).
- Sinalizar explicitamente toda prática que é **cerimônia de papel / YAGNI** para
  este contexto (evitar processo especulativo).
- Fontes citadas com data; priorizar evidência (DORA/SPACE/Accelerate, docs oficiais,
  engenheiros reconhecidos) sobre marketing; distinguir consenso de opinião.
