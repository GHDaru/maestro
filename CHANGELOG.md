# Changelog

Todas as mudanças notáveis do **Maestro** são registradas aqui. Formato baseado em
[Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/); versionamento semântico.

> **Forcing function**: toda PR adiciona uma entrada em **[Unreleased]** — a CI
> (`.github/workflows/ci.yml`, job `changelog`) falha se o `CHANGELOG.md` não for
> alterado. Bypass: label `skip-changelog`.

## [Unreleased]

### Added
- **Companion — o tutor do livro (spec 015)**: serviço FastAPI que responde sobre o método
  **a partir do livro**, citando a página. Busca lexical em 259 trechos gerados do sumário
  (sem embeddings — YAGNI); prompt que aplica as regras do próprio livro (citar fonte,
  sigla por extenso, não inventar); porta do modelo compatível com OpenAI (NVIDIA NIM) com
  modo `echo` sem chave e BYOK por requisição (nunca persistida); persistência em
  Postgres/Neon com queda para memória; 6 endpoints com CORS restrito e limites por sessão.
  Widget flutuante em HTML/JavaScript puro, com fontes clicáveis, injetado no site **apenas**
  quando `MAESTRO_COMPANION_URL` está definida — sem ela, o site é idêntico ao anterior.
  10 testes (feliz + falha) e evidência visual nos dois temas.
- **Livro em cinco trilhas (spec 014)**: navegação por tipo de texto (Diátaxis) — A Jornada
  (tutorial), Os Capítulos (explicação), Receitas (como-fazer), Referência e Bastidores —
  cada trilha com tipo e descrição na barra lateral e no sumário; **cadência educacional**
  no topo do sumário (Entender ~20 min · Aprender ~2 h · Aplicar ~1 dia · Aprofundar);
  quatro receitas novas (instalar o Maestro, abrir um ciclo, escrever critério verificável,
  rodar a retrospectiva) e o mapa da Jornada (12 paradas: tensão → pergunta → regra).
  A capa passa a apontar para as trilhas; nenhum link de conteúdo sai para o GitHub.
- **Livro Maestro: padrão editorial + capítulo-piloto + instalador (spec 013, ADR 0011)**:
  guia editorial (`docs/livro/guia-editorial.md`) com projeto pedagógico (Backward Design,
  Diátaxis, carga cognitiva, 4C/ID), esqueleto de capítulo em 9 seções — com exemplo de
  ciclo real e verificação obrigatórios — cinco trilhas de navegação e cadência
  educacional; capítulo 13 (decisões de engenharia) como piloto, com 14 decisões no
  formato quando/por quê/o que faz/o que provoca; `scripts/instalar-maestro.sh` para
  instalar o método (agentes, skills, scripts, comandos, templates, governança) em outro
  repositório, idempotente e com `--dry-run`. Companion decidido (backend próprio,
  NVIDIA NIM + Neon) — construção em ciclo próprio.
- **Princípio VIII — comunicação inteligível (ADR 0010, constituição v1.1.0)**: em cada
  resposta/documento, a primeira ocorrência de uma sigla vem por extenso (contagem
  reinicia a cada resposta); brechas fechadas; alimenta o glossário.
- **Apêndice C — panorama exploratório de templates (spec 012)**: varredura do resto do
  ecossistema (PRP, CCPM, claude-code-spec-workflow, memory banks, claude-flow, ADK,
  marketplaces) com triagem 🔬/👁/⛔ e gatilhos explícitos; formaliza o funil
  exploratório → gatilho → hands-on → absorção por gate. Achados novos com gatilho:
  PRP (código de produto) e CCPM (multi-dev com Issues).
- **Absorções do Superpowers (spec 011)**: Iron Laws em todas as 5 skills (enforcement
  linguístico com brechas fechadas), protocolo TDD-para-skills no `skill-author`
  (baseline RED sem a skill antes de publicar), skill nova `diagnostico-antes-do-fix`
  (causa raiz antes de correção), checkpoint leve por task (raia plena >3 tasks),
  regra de zero-contexto por task no template e enforcement "Skills primeiro" no
  CLAUDE.md. Vereditos do Apêndice B aprovados integralmente (`gate-010-vereditos`).
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

### Fixed
- **Widget no tema claro**: o CSS usava `var(--fg,…)`, variável inexistente no tema do
  livro (é `--text`) — todo o texto caía no fallback escuro e ficava ilegível no tema
  claro. Descoberto em verificação visual com navegador real.
- **Assets órfãos do companion**: `companion.{css,js}` permaneciam em `site/` após remover
  `MAESTRO_COMPANION_URL` (o build limpava apenas `.html`); agora são removidos.
- **Colisão de slug no motor do site**: os cinco `README.md` do livro (handbook, receitas,
  jornada, adr, registro) resolviam todos para `readme.html`, sobrescrevendo-se em
  silêncio — o portão de links não pegava porque o alvo existia. Slug de `README.md`/
  `index.md` passa a usar o diretório pai; o resolvedor de links resolve o caminho
  relativo antes de derivar o slug; adicionada fitness function que falha o build em
  qualquer colisão (testada com colisão deliberada).
- **Links da capa do site**: `site/index.html` (escrita à mão na V0, antes das páginas
  existirem) apontava para arquivos `.md` no GitHub em 6 links; agora aponta para as
  páginas internas do livro. Permanece um único link externo, deliberado ("ver no GitHub").

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
