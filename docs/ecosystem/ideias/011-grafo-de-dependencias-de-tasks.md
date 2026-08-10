# 011 — Grafo explícito de dependências entre tasks

- **Id**: `grafo-de-dependencias`
- **Fonte**: `eyaltoledano/claude-task-master`
- **Observado em**: 2026-07-30
- **Veredito no momento**: observar
- **Destino**: —
- **Gatilho de reavaliação**: um ciclo com mais de 20 tasks paralelas, ou vários projetos simultâneos, e a ordenação manual doer (registrado em retro)

## A ideia

PRD vira `tasks.json` com dependências mapeadas, *score* de complexidade e validação de
dependência circular. A ordem de execução deixa de ser implícita.

## Por que atravessa (ou não)

Resolve um problema que ainda não temos: o `tasks.md` é curto, por fronteira, com WIP=1
limitado pela atenção humana. Carregar 36 ferramentas MCP (~21k tokens de *overhead*) para
ordenar dez tasks é o oposto da economia de contexto. **A dimensão 7 decide** — e o gatilho
está escrito para que a decisão possa mudar sem depender de alguém lembrar.

## Dimensões

| # | Dimensão | Leitura |
|---|---|---|
| 1 | Conflito com princípio | não de fundo; o **custo** conflita com o Princípio V no porte atual |
| 2 | Licença e redistribuição | MIT |
| 3 | Função já servida | parcialmente: `tasks.md` ordena, sem validar ciclo de dependência |
| 4 | Custo de contexto | **alto**: ~21k tokens de overhead de ferramentas |
| 5 | Reversibilidade | média: os `tasks.json` ficariam |
| 6 | Maturidade e evidência | maduro; nossa evidência é leitura de documentação |
| 7 | Dor real hoje | **não**: nenhum ciclo passou de ~10 tasks |
