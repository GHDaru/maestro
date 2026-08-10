# 003 — Worktree git isolado por task

- **Id**: `worktree-por-task`
- **Fonte**: `obra/superpowers`
- **Observado em**: 2026-07-30
- **Veredito no momento**: absorver
- **Destino**: `scripts/` ou `skills/`, *"quando houver dor real de paralelismo"*
- **Gatilho de reavaliação**: dois ou mais agentes escrevendo no mesmo repositório ao mesmo tempo, com conflito observado

## A ideia

Cada task de agente roda em seu próprio *worktree* do git, isolada; o merge acontece no fim.
Agentes paralelos deixam de pisar uns nos outros.

## Por que atravessa (ou não)

O card está **congelado como foi julgado em 2026-07-30**, e é justamente o exemplo que
motivou este catálogo: o ADR 0008 registrou a ideia na coluna "absorvidas" com um destino
**condicional** ("quando houver dor real"), o que é `observar` com outro nome. O Apêndice B
reclassificou para `observar` no ciclo 011, e o ADR nunca soube. Verificado em 2026-08-10:
**nenhuma ocorrência de `worktree` em `scripts/`, `skills/` ou `.claude/`**. O estado
corrente, em [`estado.jsonl`](../estado.jsonl), é `observar` — e isto aqui continua sendo o
que se julgou naquele dia, não uma reescrita dele.

## Dimensões

| # | Dimensão | Leitura |
|---|---|---|
| 1 | Conflito com princípio | nenhum |
| 2 | Licença e redistribuição | MIT na origem; a técnica é do git, não do projeto |
| 3 | Função já servida | não, mas também não há a dor: WIP=1 por atenção humana (Princípio II) |
| 4 | Custo de contexto | baixo |
| 5 | Reversibilidade | total |
| 6 | Maturidade e evidência | maduro na origem; **zero** experiência nossa — nunca rodamos dois agentes escrevendo em paralelo |
| 7 | Dor real hoje | **não** — e é esta dimensão que decide. Construir isolamento para um paralelismo que não existe é YAGNI |
