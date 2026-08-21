# Orientações do projeto — Maestro

> Este arquivo é a instrução que a IA lê antes de trabalhar. `AGENTS.md` é um link
> simbólico para ele — **uma fonte só**, para as duas instruções não divergirem (era o que
> vinha acontecendo até o ciclo 021). Verificação: `scripts/check-install.sh`.
>
> **Idioma (ADR 0014)**: tudo que é **instalável** — agentes, skills, scripts, comandos,
> templates e `docs/governance/` — é escrito em **inglês**. O **livro** (`docs/handbook/`,
> receitas, diagramas) e este arquivo de projeto seguem em **português**. Verificação:
> `scripts/check-language.sh`.

<!-- BLOCO INSTALADO — gerado por `scripts/install-maestro.sh --block`, não editado à mão.
     Está aqui porque o Maestro instalado no próprio Maestro é o único teste honesto do
     instalador: se o bloco que enviamos a terceiros não serve para nós, ele não serve.
     O `@`-import abaixo INLINA a constituição em toda sessão deste repositório — custo
     medido: 6.072 B, ~1.518 tokens (ciclo 056). -->

## Method: Maestro
@docs/governance/principles.md

- The constitution above is loaded automatically. Read
  `docs/governance/operating-model.md` before any work — it is not.
- **Skills first**: before acting, check whether one of the skills below applies; if
  there is a reasonable chance, follow it (each carries its Iron Law):
  - `anti-patterns` — Catalogue of what NOT to do when one human runs many agents — the recurring mistakes observed in our own retrospectives and in the ecosystem.
  - `constitution-check` — Produces the Constitution Check table (Maestro Principles I–VIII) inside a plan.md, decides when a principle counts as violated and what to do with the violation.
  - `diagnose-before-fix` — Root-cause discipline — investigate before fixing.
  - `fight-the-pile-up` — Editorial checklist that turns a dense document (a "pile-up" — many acronyms with no dictionary, everything on one page, no narrative) into clear text without changing the technical content.
  - `living-journey` — Living journey documentation — one document per journey, screenshots generated from the real build by a versioned script, and a dated heuristic evaluation, all in the same pull request.
  - `verifiable-dod` — Turns vague acceptance criteria into executable fitness functions (grep, ls, tests) that a machine can verify without human judgement.
- Flow: `spec → plan (Constitution Check) → tasks → implement → DoD → review in
  fresh context → human gate → merge`.
- Lanes: light (the pull request is the artifact) · full (complete spec) · infra (full +
  reversibility).
- Every cycle declares its conditional artifacts and carries the closing tail
  (`TAIL:review`, `TAIL:security`, `TAIL:mutation`, `TAIL:gate`) in `tasks.md`, with
  the evidence in
  `qa-report.md`. Catalogue: `docs/governance/artifacts.md`.
- **Asked "are you following the method?" — do NOT answer from memory.** Run
  `scripts/check-conformance.sh <NNN>` and read it: memory reports intention, not fact.
- Three artifacts are **immutable**, and a `PreToolUse` guard refuses to rewrite them:
  the body of an existing ADR, `docs/records/decisoes.jsonl`, and the dated idea cards
  under `docs/ecosystem/ideias/`. The route is always to APPEND — a new ADR that
  supersedes, `scripts/record-decision.sh`, a new state line.

## Regra central

- **Antes de qualquer trabalho, leia `docs/governance/principles.md`** (a
  constituição, princípios I–VIII) e o `docs/governance/operating-model.md` (a regra
  vigente). Prevalecem sobre qualquer outra prática.
- **Skills primeiro (enforcement — ciclo 011):** antes de agir, verifique se uma skill de
  `skills/` se aplica. **Se houver chance razoável de aplicar-se, siga-a** — as skills
  comandam, não sugerem (cada uma tem sua Iron Law):

  | Skill | Quando |
  |---|---|
  | `constitution-check` | todo plano, antes de implementar |
  | `verifiable-dod` | ao escrever critério de aceite ou portão |
  | `fight-the-pile-up` | ao ver arquivo/agente/prompt inchando |
  | `anti-patterns` | ao desenhar e ao revisar (checklist negativo, 23 itens) |
  | `diagnose-before-fix` | **encontrou bug? antes de propor correção** |
  | `living-journey` | mexeu em tela: captura do build real + heurística datada |

- **TODO o desenvolvimento da metodologia acontece neste repositório (`GHDaru/maestro`).**
  Os repositórios `ghdaru` e `flowbuilder` são **somente leitura**, para consulta de
  origem — não commitar neles.

## Fluxo de desenvolvimento

- Trabalha-se na branch **`dev`**; promove-se para **`main`** a cada entrega concluída
  (`scripts/promote-main.sh`, que registra o gate no índice de decisões).
- Fluxo de feature (spec-driven): `spec → plan (Constitution Check) → tasks → implement →
  DoD (CI) → revisão em contexto fresco → gate humano → merge`.
- **Raias** (modelo §3): leve (bug/typo — o PR é o artefato), plena (feature — spec),
  infra (sempre plena + gates de reversibilidade).
- **Tem tela?** O ramo de interface não é opcional: papel semântico antes do componente
  (agente `ux-semantics`) → `ux-design.md` → gate de UX → jornada viva.
- Todo ciclo atualiza os **artefatos vivos no mesmo PR**: `CHANGELOG.md`, `docs/roadmap.md`
  e, quando decide algo, um ADR + linha em `docs/records/decisoes.jsonl`.

## Aplicação (enforcement)

- **Hard gates (CI)**: `.github/workflows/ci.yml` — inclui o gate de **CHANGELOG** (toda
  PR adiciona entrada em `[Unreleased]`; bypass: label `skip-changelog`).
- **Fitness functions locais** (rodar antes de fechar ciclo):

  ```bash
  scripts/check-agents.sh              # invariantes dos subagentes
  scripts/check-roles.sh               # papel do modelo × agente que o entrega
  scripts/check-install.sh           # método instalado e coerente neste repo
  scripts/check-language.sh          # inglês no que é instalável (ADR 0014)
  scripts/check-cycle.sh             # raia justificada + commit citando o ciclo
  scripts/check-links.sh             # todo link relativo do repositório resolve
  scripts/check-retro.sh             # dívida de achados abertos (gatilho da retro)
  scripts/check-evals.sh             # corpus de evals: alvo real, discrimina, não defasou
  scripts/check-boundary.sh          # fronteira interna entre os dois domínios (ADR 0018)
  scripts/check-conformance.sh       # "estou seguindo o Maestro?" — resposta executável
  scripts/check-chapters.sh            # Iron Law editorial: 9 seções, datação, exemplo real
  scripts/package-plugin.sh --verify   # plugin sincronizado com as fontes
  node publicar/build.mjs                   # livro: links, imagens e slugs
  ```

- **Checklist humano/agente**: `.github/pull_request_template.md` (espelha a DoD).
- **Self-check do agente**: comando `/dod` (`.claude/commands/dod.md`).
- **Julgamento (saída não-determinística)**: o portão determinístico mede a saúde do corpus;
  a avaliação em si é o comando `/eval` (`.claude/commands/eval.md`), em contexto fresco e
  sob demanda. Anatomia e limites: `evals/README.md`, ADR 0016, teorema T7.
- Decisões de metodologia viram **ADR** em `docs/adr/`.

## Onde está o quê

- **Pergunta "estou seguindo o Maestro?"** → **não responda de memória**: rode
  `scripts/check-conformance.sh <NNN>`. Memória de agente relata intenção, não fato (C13).
- Catálogo de artefatos (quando cada um se aplica) → `docs/governance/artifacts.md`
- Princípios → `docs/governance/principles.md`
- Modelo operacional → `docs/governance/operating-model.md`
- O livro (13 capítulos + apêndices, receitas, diagramas) → `docs/handbook/`,
  `docs/receitas/`, `docs/diagramas/` — publicado por `publicar/build.mjs`
- O processo desenhado → `docs/diagramas/05-bpmn-processo.md` (navegável)
- ADRs → `docs/adr/` (ver `docs/adr/README.md`) · decisões → `docs/records/decisoes.jsonl`
- Pesquisa + diário → `docs/research/`
- Levar o método para outro projeto → `docs/receitas/instalar-o-maestro.md`
