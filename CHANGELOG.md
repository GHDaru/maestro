# Changelog

Todas as mudanças notáveis do **Maestro** são registradas aqui. Formato baseado em
[Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/); versionamento semântico.

> **Forcing function**: toda PR adiciona uma entrada em **[Unreleased]** — a CI
> (`.github/workflows/ci.yml`, job `changelog`) falha se o `CHANGELOG.md` não for
> alterado. Bypass: label `skip-changelog`.

## [Unreleased]

### Added
- **Apêndice B — estudo hands-on do Superpowers (spec 010)**: avaliação do fork
  `GHDaru/superpowers` (obra/superpowers v6.2.0) com 10 vereditos propostos — Iron Laws,
  TDD para skills, root cause antes de fix, review por task, zero-contexto, bootstrap de
  enforcement — e a tensão HARD-GATE × raias registrada. Vereditos aguardam gate.
- **Spec Kit vendorizado (spec 009, F4)**: templates `spec/plan/tasks` reescritos como
  fonte nossa (PT, raias, critérios EARS, Constitution Check I–VII, gates explícitos —
  formato provado nos ciclos 003–008), comando `/speckit.converge` trazido do fork
  (sem extension hooks) e proveniência registrada em `.specify/UPSTREAM.md` (sync
  deliberada; templates mandam sobre o esqueleto do `novo-ciclo.sh`).
- **Registro automático do gate de merge (ADR 0009, modelo v1.3.0)**: `promover-main.sh`
  anexa `gate-main-<sha>` ao índice `docs/registro/decisoes.jsonl` a cada promoção;
  gates dos ciclos 003–007 registrados retroativamente; `retro.sh` cruza pendências dos
  qa-reports com o registro. Regra nascida do primeiro run da retro executável.
- **Absorções do estudo maestro-02 (spec 008)**: registro de decisões consultável por
  máquina (`docs/registro/decisoes.jsonl` + protocolo + `scripts/registrar-decisao.sh`),
  retro executável (`scripts/retro.sh`), skill `anti-padroes`, gates em nível de task
  (handbook cap. 10 §6b), economia de contexto medida (cap. 04 §6b) e sintaxe **EARS**
  na skill `dod-verificavel` (fecha absorção do ciclo 007). ADR 0008 aceito.
- **Toolkit dos ciclos 003–007**: 12 subagentes executáveis (`.claude/agents/`), 3 skills
  agentskills.io (`skills/`), 3 scripts do ritual (`scripts/`), diagramas do método
  (`docs/diagramas/`, md+PDF), avaliação do ecossistema SDD (`docs/research/` + ADR 0008)
  e Apêndice A do handbook (estudo do maestro-02).
- **Site V0 (storytelling + pipeline)**: capa narrativa `site/index.html` + motor
  `publicar/` (Markdown→site multipágina, sidebar, tema, callouts, gate de link quebrado)
  + roadmap de agentes (`docs/agents/perfis.md`, `comunicacao.md`) + deploy no GitHub Pages
  (`.github/workflows/pages.yml`).
- **Camada didática (spec 001)**: guia narrativo [`docs/comece-por-aqui.md`](docs/comece-por-aqui.md)
  (dor → jornada → sistema) + [`docs/governance/glossario.md`](docs/governance/glossario.md)
  (dicionário de todas as siglas); links no `README.md` e banners nos docs de governança.
  Compêndio PDF regenerado com Introdução + Apêndice Glossário (57 páginas).

### Changed
- **Rebasing (FR4)**: referências a "Constituição / Princípio IV/V/VII" nos docs migrados
  passam a apontar para `docs/governance/principios-maestro.md` (via mapa de linhagem).

### Anterior
- **Fundação do repositório Maestro** (ADR 0007): metodologia extraída de `ghdaru`/
  `flowbuilder` para repositório próprio.
- `docs/governance/principios-maestro.md` — constituição própria da metodologia (v1.0.0).
- `docs/governance/modelo-operacional.md` (v1.2.0) — papéis, cerimônias, artefatos,
  raias, gates, DoR/DoD e enforcement.
- `docs/handbook/` — 12 capítulos de fundamentos + apresentações executiva e técnica
  (decks HTML) + prompts de imagem.
- `docs/adr/` — ADRs 0004–0006 (preservados) + 0007 (separação) + índice.
- `docs/research/` — pesquisa citada + diário de aprendizado.
- Templates/boas práticas: PR template com a DoD, comando `/dod`, gate de CHANGELOG na CI.
- **PDF do handbook** (livro A4, capa + 12 capítulos) — `docs/handbook/maestro-handbook.pdf`.
- **PDF compêndio de governança** (visão geral: Princípios + Modelo operacional + Handbook +
  ADRs, 51 páginas) — `docs/handbook/maestro-compendio-governanca.pdf`.

### Follow-up
- Rebaixar referências "Constituição / Princípio IV/V/VII" nos docs migrados para
  `principios-maestro.md` (mapa de linhagem no fim daquele doc).
- Remover as cópias redundantes da metodologia em `ghdaru` após validação desta migração.
