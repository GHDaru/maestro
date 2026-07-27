# ADR 0005 — Raias de trabalho (leve/plena/infra) e specs de infra com gates de reversibilidade

- **Status**: Aceito
- **Data**: 2026-07-22
- **Relacionado**: `docs/governance/modelo-operacional.md` (v1.1.0); ADR 0004;
  Constituição v1.3.0 (Princípios I, IV, V)

## Contexto

O modelo operacional v1.0.0 tratava todo trabalho como fluxo Spec Kit completo
(`specify → clarify → plan → tasks → implement`). Na prática isso é caro demais para
mudanças pequenas (bug, typo, rename, ajuste de log) — o fluxo completo vira cerimônia
de papel (YAGNI). Ao mesmo tempo, infra e migrações são o oposto: alto raio de impacto
e **irreversibilidade**, exigindo mais rigor, não menos.

Durante a avaliação surgiu o **OpenSpec** (Fission-AI) como alternativa leve ao Spec
Kit, com modelo *delta* (`Propose → Apply → Archive`, mudanças como delta contra o
comportamento atual). Decisão do mantenedor: **não manter duas ferramentas de
spec-driven** — o custo operacional de duas SDDs não se justifica.

Princípio-guia derivado da jornada de aprendizado: **o valor de uma spec escala com
ambiguidade × raio de impacto × irreversibilidade**; e o que torna uma ação irreversível
segura de delegar não é a aprovação em si, mas a **reversibilidade engenheirada**
(backup, dry-run, staging, soft-delete).

## Decisão

1. **Três raias de trabalho** no modelo operacional (§3):
   - **Leve (delta)**: bug/typo/rename/log — sem `spec/plan/tasks`; o **PR é o
     artefato**; bug exige um teste que o reproduz. DoD reduzida (mantém testes,
     fitness functions e revisão independente).
   - **Plena (spec)**: feature ambígua/contrato/cross-feature — Spec Kit completo.
   - **Infra**: infra/migração/deploy — **sempre plena**, nunca leve, com gates de
     reversibilidade adicionais.
   Regra de desempate: na dúvida, é plena; infra/migração nunca são leves.

2. **Spec de infra** entra no catálogo de entregáveis como tipo próprio, e a DoD
   ganha um **bloco obrigatório para ações irreversíveis** (§7): backup/snapshot,
   dry-run + staging, estratégia de rollback no runbook, aprovação humana explícita.

3. **Uma única ferramenta SDD (Spec Kit)**. OpenSpec avaliado e **descartado**; a
   ideia útil (modelo delta) foi absorvida como a raia leve dentro do próprio fluxo.

Não adotado (YAGNI): papel "Plataforma/DevOps" nomeado separadamente — se é a mesma
pessoa, nomear a *responsabilidade* basta.

## Consequências

- Mudanças pequenas deixam de pagar o pedágio da spec completa, sem afrouxar
  verificação (revisão independente e testes continuam obrigatórios).
- Infra passa a ter rigor proporcional ao risco: a reversibilidade vira requisito de
  DoD, não boa intenção.
- Uma ferramenta só reduz carga cognitiva e de manutenção; a decisão sobre OpenSpec
  fica registrada para não ser reaberta sem novo contexto.
- `modelo-operacional.md` sobe para **v1.1.0** (MINOR); disciplina de branch/remote do
  FlowBuilder foi avaliada e **não** trazida (específica daquele repositório).

## Fontes

- OpenSpec (Fission-AI): https://github.com/Fission-AI/OpenSpec
- Spec Kit vs OpenSpec: https://intent-driven.dev/knowledge/spec-kit-vs-openspec/
- Demais fontes da jornada em
  `docs/research/resultado-pesquisa-praticas-desenvolvimento-avaliacao.md`.
