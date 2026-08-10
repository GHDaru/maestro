# 37 — Quebrar a feature em issues do tamanho de um agente

- **Id**: `decompose-feature-em-issues`
- **Fonte**: `skill decompose (comunitária)`
- **Observado em**: 2026-08-06
- **Veredito no momento**: descartar
- **Destino**: —
- **Gatilho de reavaliação**: —

## A ideia

Uma skill que corta a feature em *issues* ordenadas, do tamanho de um agente, consumidas em sequência por um laço de execução.

## Por que atravessa (ou não)

Faz o corte **abaixo** da spec, que é onde o `tasks.md` já opera — e amarra o resultado a *issues* de uma plataforma, acoplamento que a mesma pesquisa recusou. O corte que falta é o de **cima**, entre ciclos ([022](022-decomposicao-em-tres-passadas.md)).

## Dimensões

| # | Dimensão | Leitura |
|---|---|---|
| 1 | Conflito com princípio | acoplaria a rastreabilidade a uma plataforma (Princípio III) |
| 2 | Licença e redistribuição | sem licença declarada — citável, nunca copiável |
| 3 | Função já servida | **sim**: `tasks.md` por fronteira |
| 4 | Custo de contexto | médio |
| 5 | Reversibilidade | baixa: as issues ficariam na plataforma |
| 6 | Maturidade e evidência | leitura da skill publicada |
| 7 | Dor real hoje | não |
