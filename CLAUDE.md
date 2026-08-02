# Orientações do projeto — Maestro

> Este arquivo é a instrução que a IA lê antes de trabalhar. `AGENTS.md` é um link
> simbólico para ele — **uma fonte só**, para as duas instruções não divergirem (era o que
> vinha acontecendo até o ciclo 021). Verificação: `scripts/verificar-instalacao.sh`.

## Regra central

- **Antes de qualquer trabalho, leia `docs/governance/principios-maestro.md`** (a
  constituição, princípios I–VIII) e o `docs/governance/modelo-operacional.md` (a regra
  vigente). Prevalecem sobre qualquer outra prática.
- **Skills primeiro (enforcement — ciclo 011):** antes de agir, verifique se uma skill de
  `skills/` se aplica. **Se houver chance razoável de aplicar-se, siga-a** — as skills
  comandam, não sugerem (cada uma tem sua Iron Law):

  | Skill | Quando |
  |---|---|
  | `constitution-check` | todo plano, antes de implementar |
  | `dod-verificavel` | ao escrever critério de aceite ou portão |
  | `combater-amontoado` | ao ver arquivo/agente/prompt inchando |
  | `anti-padroes` | ao desenhar e ao revisar (checklist negativo, 16 itens) |
  | `diagnostico-antes-do-fix` | **encontrou bug? antes de propor correção** |
  | `jornada-viva` | mexeu em tela: captura do build real + heurística datada |

- **TODO o desenvolvimento da metodologia acontece neste repositório (`GHDaru/maestro`).**
  Os repositórios `ghdaru` e `flowbuilder` são **somente leitura**, para consulta de
  origem — não commitar neles.

## Fluxo de desenvolvimento

- Trabalha-se na branch **`dev`**; promove-se para **`main`** a cada entrega concluída
  (`scripts/promover-main.sh`, que registra o gate no índice de decisões).
- Fluxo de feature (spec-driven): `spec → plan (Constitution Check) → tasks → implement →
  DoD (CI) → revisão em contexto fresco → gate humano → merge`.
- **Raias** (modelo §3): leve (bug/typo — o PR é o artefato), plena (feature — spec),
  infra (sempre plena + gates de reversibilidade).
- **Tem tela?** O ramo de interface não é opcional: papel semântico antes do componente
  (agente `ux-semantica`) → `ux-design.md` → gate de UX → jornada viva.
- Todo ciclo atualiza os **artefatos vivos no mesmo PR**: `CHANGELOG.md`, `docs/roadmap.md`
  e, quando decide algo, um ADR + linha em `docs/registro/decisoes.jsonl`.

## Aplicação (enforcement)

- **Hard gates (CI)**: `.github/workflows/ci.yml` — inclui o gate de **CHANGELOG** (toda
  PR adiciona entrada em `[Unreleased]`; bypass: label `skip-changelog`).
- **Fitness functions locais** (rodar antes de fechar ciclo):

  ```bash
  scripts/verificar-agentes.sh              # invariantes dos subagentes
  scripts/verificar-papeis.sh               # papel do modelo × agente que o entrega
  scripts/verificar-instalacao.sh           # método instalado e coerente neste repo
  scripts/verificar-capitulos.sh            # Iron Law editorial: 9 seções, datação, exemplo real
  scripts/empacotar-plugin.sh --verificar   # plugin sincronizado com as fontes
  node publicar/build.mjs                   # livro: links, imagens e slugs
  ```

- **Checklist humano/agente**: `.github/pull_request_template.md` (espelha a DoD).
- **Self-check do agente**: comando `/dod` (`.claude/commands/dod.md`).
- Decisões de metodologia viram **ADR** em `docs/adr/`.

## Onde está o quê

- Princípios → `docs/governance/principios-maestro.md`
- Modelo operacional → `docs/governance/modelo-operacional.md`
- O livro (13 capítulos + apêndices, receitas, diagramas) → `docs/handbook/`,
  `docs/receitas/`, `docs/diagramas/` — publicado por `publicar/build.mjs`
- O processo desenhado → `docs/diagramas/05-bpmn-processo.md` (navegável)
- ADRs → `docs/adr/` (ver `docs/adr/README.md`) · decisões → `docs/registro/decisoes.jsonl`
- Pesquisa + diário → `docs/research/`
- Levar o método para outro projeto → `docs/receitas/instalar-o-maestro.md`
