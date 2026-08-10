# 001 — Critério de aceite com sintaxe fixa (EARS)

- **Id**: `ears`
- **Fonte**: `Kiro (AWS)`
- **Observado em**: 2026-07-30
- **Veredito no momento**: absorver
- **Destino**: `skills/verifiable-dod/SKILL.md`
- **Gatilho de reavaliação**: —

## A ideia

*Easy Approach to Requirements Syntax*: `QUANDO <condição> O SISTEMA DEVERÁ <comportamento
observável>`. Uma forma sintática fixa para requisito, que vira teste quase 1:1.

## Por que atravessa (ou não)

O Maestro já exigia "critério testável"; o que faltava era **forma**. A lição recorrente
deste repositório é que instrução falha onde forma funciona — e EARS é forma pura, com custo
zero de ferramenta. A ferramenta de origem (IDE proprietária) foi descartada no mesmo
movimento: a ideia atravessa, a IDE não. Ver [009](009-ide-proprietaria-spec-first.md).

## Dimensões

| # | Dimensão | Leitura |
|---|---|---|
| 1 | Conflito com princípio | nenhum — reforça o Princípio IV (DoD verificável) |
| 2 | Licença e redistribuição | a **sintaxe** é técnica documentada publicamente; nada foi copiado, só reimplementado nas nossas palavras |
| 3 | Função já servida | não: servia-se o *objetivo* (critério testável), nunca a forma |
| 4 | Custo de contexto | uma linha no template e um parágrafo na skill |
| 5 | Reversibilidade | total: é convenção de escrita, sai sem deixar dependência |
| 6 | Maturidade e evidência | usada em todas as specs de 009 em diante; os FRs deste próprio ciclo estão em EARS |
| 7 | Dor real hoje | sim, e era antiga: critérios que não viravam teste |
