# Orientações do projeto — Maestro

## Regra central

- **Antes de qualquer trabalho, leia `docs/governance/principios-maestro.md`** (a
  constituição da metodologia) e o `docs/governance/modelo-operacional.md` (a regra
  vigente). Prevalecem sobre qualquer outra prática.
- **Skills primeiro (enforcement — ciclo 011):** antes de agir, verifique se uma skill de
  `skills/` se aplica à tarefa (constitution-check, dod-verificavel, combater-amontoado,
  anti-padroes, diagnostico-antes-do-fix). **Se houver chance razoável de aplicar-se,
  siga-a** — as skills comandam, não sugerem (cada uma tem sua Iron Law). Encontrou bug?
  `diagnostico-antes-do-fix` ANTES de propor correção.
- **TODO o desenvolvimento da metodologia acontece neste repositório (`GHDaru/maestro`).**
  Os repositórios `ghdaru` e `flowbuilder` são **somente leitura**, para consulta de
  origem — não commitar neles.

## Fluxo de desenvolvimento

- Trabalha-se na branch **`dev`**; promove-se para **`main`** a cada elemento/entrega
  concluída (checkpoint) ou quando solicitado.
- Fluxo de feature (spec-driven): `spec → plan (Constitution Check) → tasks → implement →
  DoD (CI) → revisão em contexto fresco → gate humano → merge`.
- **Raias** (modelo §3): leve (bug/typo — o PR é o artefato), plena (feature — spec),
  infra (sempre plena + gates de reversibilidade).

## Aplicação (enforcement)

- **Hard gates (CI)**: `.github/workflows/ci.yml` — inclui o gate de **CHANGELOG** (toda
  PR adiciona entrada em `[Unreleased]`; bypass: label `skip-changelog`).
- **Checklist humano/agente**: `.github/pull_request_template.md` (espelha a DoD).
- **Self-check do agente**: comando `/dod` (`.claude/commands/dod.md`).
- Decisões de metodologia viram **ADR** em `docs/adr/`.

## Onde está o quê

- Princípios → `docs/governance/principios-maestro.md`
- Modelo operacional → `docs/governance/modelo-operacional.md`
- Fundamentos (handbook, 12 capítulos + decks) → `docs/handbook/`
- ADRs → `docs/adr/` (ver `docs/adr/README.md`)
- Pesquisa + diário → `docs/research/`
