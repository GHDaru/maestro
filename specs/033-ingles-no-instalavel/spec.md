# Spec 033 — Inglês no método instalável

- **Status**: Concluída · **Raia**: plena · **Data**: 2026-08-02
- **Origem**: decisão do Steward — "tudo que será instalado deve ser em inglês"; escopo
  confirmado como **toolkit + governança** (o livro segue em português).

## O quê e por quê

A superfície instalável do Maestro é lida por **Inteligência Artificial (IA) em repositórios
de terceiros** — e estava em português, dentro de um ecossistema em inglês. O bloco de
instrução gerado pelo instalador já viajava para projetos alheios; nomes como
`verificar-instalacao.sh` e `dod-verificavel/` obrigavam o projeto de destino a conviver com
convenções que ele não escolheu.

O livro é o caso oposto: tem público definido, treze capítulos recém-migrados e nenhum
motivo para mudar de idioma. Daí a fronteira: **instalável em inglês, livro em português**.

## Requisitos funcionais

- **FR1**: QUANDO um arquivo pertence à superfície instalável (`.claude/agents/`, `skills/`,
  `scripts/`, `.claude/commands/`, `.specify/templates/`, `docs/governance/`,
  `docs/records/README.md`), O SISTEMA DEVE tê-lo em inglês — nome, conteúdo e mensagens.
- **FR2**: QUANDO houver resíduo de português na superfície instalável, `check-language.sh`
  DEVE falhar apontando arquivo e linha.
- **FR3**: QUANDO uma linha legitimamente carregar português (padrão casado contra o livro),
  ela DEVE declarar o marcador `PT-DATA` na própria linha — exceção visível onde se aplica.
- **FR4**: O índice de decisões DEVE manter os nomes de campo originais: o arquivo é
  append-only e traduzir chaves exigiria reescrever linhas imutáveis.
- **FR5**: QUANDO os arquivos são renomeados, O SISTEMA DEVE manter o livro publicando sem
  link quebrado (`node publicar/build.mjs` sai com código 0).
- **FR6**: O instalador DEVE continuar funcionando ponta a ponta com os nomes novos.

## Fora de escopo

- Traduzir o livro, as receitas, os diagramas e o site (decisão do Steward).
- Traduzir os registros históricos em `specs/` — são evidência do que aconteceu.
- Renomear os arquivos de ADR (o conteúdo é registro imutável; só os caminhos citados
  foram corrigidos).

## Critérios de aceite (DoD)

- [x] `scripts/check-language.sh` **provado falhando** com resíduo injetado num agente
- [x] `check-language.sh` verde nos 13 caminhos instaláveis
- [x] `check-agents.sh`, `check-roles.sh`, `check-install.sh` verdes com os nomes novos
- [x] `package-plugin.sh --verify` sincronizado
- [x] `node publicar/build.mjs` exit 0, 35 páginas, sem link quebrado
- [x] `install-maestro.sh --block` gera o bloco em inglês, com as 6 skills do disco

## Clarify

1. Até onde vai "instalável"? → **toolkit + governança** (resposta do Steward). O livro e o
   `CLAUDE.md` deste repositório seguem em português.
2. Traduzir as chaves do índice de decisões? → **não** (FR4): append-only vence.
