# 004 — Standards do codebase por camada, em arquivo próprio

- **Id**: `standards-por-camada`
- **Fonte**: `buildermethods/agent-os`
- **Observado em**: 2026-07-30
- **Veredito no momento**: absorver
- **Destino**: `docs/standards/`, *"se a dor aparecer"*
- **Gatilho de reavaliação**: primeiro onboarding do método em codebase legado grande, com deriva de padrão observada

## A ideia

Separar em camadas o contexto que o agente carrega: **standards** (padrões do código),
**product** (o que se está construindo) e **specs** (a mudança em curso), cada um em seu
arquivo, para reduzir deriva do agente em código legado.

## Por que atravessa (ou não)

Segundo exemplo que motivou este catálogo, com a mesma anatomia do
[003](003-worktree-por-task.md): registrado como absorção parcial, com destino condicional
e uma pasta que **nunca existiu**. Verificado em 2026-08-10: `docs/standards/` não existe.
Para o porte atual, `CLAUDE.md` + constituição + linguagem ubíqua já fazem a injeção de
padrões; uma camada a mais seria redundância, que o Princípio VI proíbe.

## Dimensões

| # | Dimensão | Leitura |
|---|---|---|
| 1 | Conflito com princípio | nenhum de fundo; a implementação prematura conflitaria com VI (função duplicada) |
| 2 | Licença e redistribuição | MIT na origem; a ideia é organizacional |
| 3 | Função já servida | **sim, hoje**: `CLAUDE.md`/`AGENTS.md` como fonte única já injeta padrão |
| 4 | Custo de contexto | mais arquivos para carregar em todo ciclo |
| 5 | Reversibilidade | total |
| 6 | Maturidade e evidência | maduro na origem; **zero** experiência nossa em codebase legado |
| 7 | Dor real hoje | **não**: o Maestro ainda rege o próprio repositório, não código de produto legado |
