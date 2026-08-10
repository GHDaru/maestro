# 012 — Contexto do codebase empacotado dentro da spec (PRP)

- **Id**: `contexto-na-spec`
- **Fonte**: `Wirasm/PRPs-agentic-eng`
- **Observado em**: 2026-08-01
- **Veredito no momento**: observar
- **Destino**: —
- **Gatilho de reavaliação**: primeiro ciclo em que o Maestro reger código de produto, e não o próprio repositório

## A ideia

*Product Requirement Prompt*: a spec carrega junto o contexto do codebase que o agente vai
precisar — arquivos relevantes, convenções, exemplos —, para que ele não tenha de descobrir
sozinho.

## Por que atravessa (ou não)

É uma das duas ideias genuinamente novas do panorama (a outra é
[014](014-rastreabilidade-via-issues.md)). Hoje o Maestro rege um repositório que o agente
já conhece inteiro; num codebase grande e alheio, "descobrir o contexto" é a maior parte do
custo e a maior fonte de erro. Observar com gatilho é a decisão honesta: a dor é previsível
e ainda não chegou.

## Dimensões

| # | Dimensão | Leitura |
|---|---|---|
| 1 | Conflito com princípio | nenhum; reforçaria o Princípio V |
| 2 | Licença e redistribuição | MIT |
| 3 | Função já servida | não |
| 4 | Custo de contexto | ambíguo: gasta na spec para economizar na execução |
| 5 | Reversibilidade | total |
| 6 | Maturidade e evidência | leitura do repositório; sem uso nosso |
| 7 | Dor real hoje | **não**, e a razão é conhecida: ainda regemos o próprio repositório |
