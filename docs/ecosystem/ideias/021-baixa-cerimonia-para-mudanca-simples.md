# 021 — Cerimônia mínima para mudança simples

- **Id**: `baixa-cerimonia`
- **Fonte**: `GSD (Get Shit Done)`
- **Observado em**: 2026-07-30
- **Veredito no momento**: observar
- **Destino**: —
- **Gatilho de reavaliação**: —

> **Estado corrente ≠ este card.** Este card é o **momento**: registra o veredito de
> 2026-07-30 — o `ADR 0008` item 3 o listou entre os "observar com gatilho explícito" ("nenhuma lacuna hoje — raia leve cobre"). O veredito de hoje é **descartar**, reclassificado no ciclo 047 e
> registrado em [`estado.jsonl`](../estado.jsonl) numa linha nova, datada de 2026-08-10.
> O card não é reescrito: mudar de ideia é legítimo, apagar o registro de que se pensava
> diferente não é.

## A ideia

Framework SDD de baixa cerimônia, nativo de Claude Code: entrar rápido, custo baixo, pouco
artefato para mudança pequena.

## Por que atravessa (ou não)

A tese é boa e **já é nossa**: é a raia leve, que veio do OpenSpec ([005](005-raia-leve-delta.md))
e cobriu 12 dos 46 ciclos. Não há lacuna. Descartado em vez de observado pela regra do
vocabulário: `observar` exige gatilho, e não existe condição que faria adotar um segundo
motor para uma função já servida. Sem licença declarada na varredura, copiar estaria fora de
questão de qualquer forma.

## Dimensões

| # | Dimensão | Leitura |
|---|---|---|
| 1 | Conflito com princípio | sim: segundo motor de fluxo (ADR 0005) |
| 2 | Licença e redistribuição | sem licença declarada na varredura — **citar, nunca copiar** |
| 3 | Função já servida | **sim**: a raia leve, com 12 ciclos de uso |
| 4 | Custo de contexto | irrelevante |
| 5 | Reversibilidade | alta |
| 6 | Maturidade e evidência | análises de terceiros de 2026; sem leitura direta do código |
| 7 | Dor real hoje | não |
