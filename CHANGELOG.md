# Changelog

Todas as mudanças notáveis do **Maestro** são registradas aqui. Formato baseado em
[Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/); versionamento semântico.

> **Forcing function**: toda PR adiciona uma entrada em **[Unreleased]** — a CI
> (`.github/workflows/ci.yml`, job `changelog`) falha se o `CHANGELOG.md` não for
> alterado. Bypass: label `skip-changelog`.

## [Unreleased]

### Added
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
