# 030 — Portão duro universal (mesmo rigor para toda mudança)

- **Id**: `hard-gate-universal`
- **Fonte**: `obra/superpowers`
- **Observado em**: 2026-07-31
- **Veredito no momento**: descartar
- **Destino**: —
- **Gatilho de reavaliação**: —

## A ideia

Um único fluxo mandatório para qualquer mudança: mesmo TDD, mesmo review, mesmos estágios,
sem exceção por tamanho.

## Por que atravessa (ou não)

A tensão foi registrada no Apêndice B e resolvida a favor das **raias**: rigor proporcional
a ambiguidade × raio × irreversibilidade (ADR 0005). Rigor uniforme tem custo uniforme, e
custo uniforme em mudança trivial é o que faz gente pular o processo inteiro — o portão que
todos contornam protege menos que o portão proporcional que todos seguem.

Note-se a assimetria deliberada: o **rigor linguístico** da mesma fonte foi absorvido
([002](002-iron-law.md)); a **universalidade** dele, não. Absorver uma ideia não obriga a
absorver o que vem colado nela.

## Dimensões

| # | Dimensão | Leitura |
|---|---|---|
| 1 | Conflito com princípio | **sim**: raias (ADR 0005) e Princípio VII |
| 2 | Licença e redistribuição | MIT — não é a licença que reprova |
| 3 | Função já servida | sim, de outra forma: as raias |
| 4 | Custo de contexto | alto por mudança trivial |
| 5 | Reversibilidade | total |
| 6 | Maturidade e evidência | maduro na origem; 12 ciclos nossos na raia leve dizem o contrário |
| 7 | Dor real hoje | não |
