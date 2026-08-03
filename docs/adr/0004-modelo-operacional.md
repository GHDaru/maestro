# ADR 0004 — Modelo operacional (papéis, cerimônias, entregáveis e artefatos)

- **Status**: Aceito
- **Data**: 2026-07-22
- **Relacionado**: Constituição v1.3.0 (Princípios I, IV, V, VII e Governance);
  `docs/governance/operating-model.md`;
  `docs/research/resultado-pesquisa-praticas-desenvolvimento-avaliacao.md`

## Contexto

A Constituição define os **princípios** e o Spec Kit define o **fluxo técnico de uma
feature**. Faltava a camada intermediária de governança: **quem** faz **o quê**
(papéis/responsabilidades), **quando** (cerimônias/cadência) e **o que** se produz
(entregáveis/artefatos com portões de qualidade) — num contexto singular: **um
desenvolvedor humano orquestrando múltiplos agentes de IA**, não um time
multi-pessoa.

Pesquisa profunda (2026-07-22, avaliada em `docs/research/resultado-pesquisa-praticas-
desenvolvimento-avaliacao.md`) triangulou fontes primárias — GitHub Spec-Driven
Development, Claude Code best practices, Anthropic "building effective agents", DORA,
Shape Up, Swarmia — e concluiu:

- **Spec-Driven é o consenso de ponta**: quando o agente escreve o código, a
  especificação (não o prompt nem o código) é a fonte de verdade; o humano dirige e
  refina.
- **Time pequeno não precisa de Scrum**: Kanban/Shape Up (apetite fixo, escopo
  variável, sem backlog nem daily) preservam o valor sem a cerimônia.
- **Velocidade e estabilidade não são trade-off** (DORA); as 4 métricas são resultado
  de capacidades (CI, trunk-based, testes, revisão) que já são princípio nosso.
- **O gate humano + revisão independente é o contrapeso inegociável** de qualquer
  fluxo agentic sério.

## Decisão

Adotar o **Modelo Operacional** documentado em `docs/governance/operating-model.md`,
que:

1. Define os **papéis como modos de trabalho** exercidos por humano, agente ou os dois
   com gate — preservando os contrapesos (quem *decide* ≠ *executa* ≠ *verifica*) ao
   mover o *verifica* para um **agente revisor em contexto fresco** e manter o *decide*
   sempre no **humano (Accountable fixo em toda linha de risco)**. RACI por etapa.
2. Estabelece a **cadência Shape Up + Kanban**: shaping/spec (planning real), execução
   por apetite fixo com WIP=1, checkpoint de ciclo, cooldown e **retro individual** —
   sem daily nem sprint planning. A retro alimenta emendas de processo (erro
   recorrente → regra versionada).
3. Cataloga os **entregáveis/artefatos** com dono, gate e localização, e formaliza
   **Definition of Ready** e **Definition of Done** como checklists verificáveis por
   agente (fecháveis por Stop-hook/`/goal`).
4. Publica o **mapa de gates humanos inegociáveis** reaproveitando a taxonomia de
   classes de risco do Princípio IV (aprovar spec, plan, merge, deploy/migração são
   indelegáveis).
5. Torna explícita a **rastreabilidade** spec NNN ↔ PR ↔ testes ↔ journey como parte
   da DoD.

Fica **descartado por ora (YAGNI)**: Scrum completo, backlog formal, RFC pesado, C4
formal e instrumentação de métricas DORA — observados, reavaliáveis na Fase 2.

## Consequências

- Existe uma referência única de "como o trabalho anda" acima da Constituição e do
  Spec Kit, sem duplicá-los (a Constituição prevalece em conflito).
- Definition of Ready/Done passam a ser checklists objetivos — habilitam automação de
  gate (Stop-hook, `/code-review` como gate de merge).
- O modelo é **versionado** e evolui via ADR + retro de ciclo; a próxima emenda
  provável é integrar a DoD a um hook de CI e materializar `CHANGELOG.md`.
- Candidatos de Fase 2 (C4, métricas DORA, DoD como hook) ficam registrados para não
  serem reinventados.

## Fontes

Ver `docs/research/resultado-pesquisa-praticas-desenvolvimento-avaliacao.md` e
`docs/research/fontes-consultadas.md` (seção 2026-07-22).
