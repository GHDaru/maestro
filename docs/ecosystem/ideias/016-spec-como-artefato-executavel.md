# 016 — A spec como artefato executável, não documento lido uma vez

- **Id**: `spec-executavel`
- **Fonte**: `Tessl`
- **Observado em**: 2026-07-30
- **Veredito no momento**: observar
- **Destino**: —
- **Gatilho de reavaliação**: a ferramenta amadurecer **e** existir caso público de produção que possamos ler

## A ideia

*Spec-as-source*: o código deriva da spec continuamente, e a spec é reexecutada, não
consultada. A implementação é saída, não fonte.

## Por que atravessa (ou não)

A tese é a nossa levada ao extremo — o Princípio VI diz que artefato que não vive é artefato
que mente. O que reprova hoje não é a ideia, é a **aposta**: ferramenta comercial, imatura,
com o método inteiro dependendo dela. Reversibilidade é princípio, e essa dependência não é
reversível barato. Observar com gatilho duplo, e o gatilho é sobre a evidência, não sobre o
marketing.

## Dimensões

| # | Dimensão | Leitura |
|---|---|---|
| 1 | Conflito com princípio | a ideia reforça o VI; a **dependência** conflita com o III |
| 2 | Licença e redistribuição | comercial — **citável, não copiável** |
| 3 | Função já servida | parcialmente: a spec já é fonte de verdade, sem ser reexecutável |
| 4 | Custo de contexto | desconhecido |
| 5 | Reversibilidade | **baixa**: o método passaria a depender de um produto |
| 6 | Maturidade e evidência | **imatura**; nossa evidência é material de terceiros de 2026 |
| 7 | Dor real hoje | não |
