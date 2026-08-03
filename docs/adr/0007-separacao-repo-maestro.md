# ADR 0007 — Separação do Maestro em repositório próprio

- **Status**: Aceito
- **Data**: 2026-07-22
- **Relacionado**: `docs/governance/principles.md`; ADR 0004/0005/0006

## Contexto

A metodologia (papéis, cerimônias, artefatos, raias, gates, DoD, governança) nasceu e
amadureceu dentro de `ghdaru` (e antes, práticas de `flowbuilder`). Ela é **transversal a
produto** — serve qualquer projeto humano+IA — e passou a ter massa própria: um modelo
operacional versionado, um handbook de 12 capítulos, ADRs, templates e enforcement. Mantê-la
acoplada ao repositório de uma plataforma específica limita sua evolução e reuso.

## Decisão

Extrair a metodologia para o repositório próprio **`GHDaru/maestro`**, que passa a ser seu
**lar único**, evoluindo de forma independente de `ghdaru` e `flowbuilder` (que ficam como
consulta de origem, somente leitura).

Migrados (preservando o layout `docs/` para manter referências internas):
- `docs/governance/operating-model.md` + novo `docs/governance/principles.md`
  (constituição própria da metodologia);
- `docs/handbook/` (12 capítulos + apresentações + prompts);
- ADRs 0004–0006 (números preservados);
- `docs/research/` (pesquisa + diário de aprendizado);
- templates: `.github/pull_request_template.md`, `.claude/commands/dod.md`, gate de
  CHANGELOG no CI.

**Não migrados**: a constituição da plataforma `ghdaru` e ADRs 0001–0003 (específicos de
produto). No Maestro, "a Constituição" corresponde a `principles.md`.

## Consequências

- Maestro evolui com versão própria; `ghdaru`/`flowbuilder` consomem a metodologia como
  referência.
- As cópias em `ghdaru` tornam-se redundantes; podem ser removidas de lá quando esta
  migração for confirmada (fora do escopo deste ADR).
- **Follow-up**: rebaixar as referências "Constituição / Princípio IV/V/VII" nos documentos
  migrados para apontar a `principles.md` (o mapa de linhagem está no fim daquele
  documento).

## Fontes

- `docs/governance/principles.md` (nota de linhagem); `README.md`.
