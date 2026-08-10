# 025 — Review por task, não só por ciclo

- **Id**: `review-por-task`
- **Fonte**: `obra/superpowers`
- **Observado em**: 2026-07-31
- **Veredito no momento**: absorver
- **Destino**: `docs/agents/comunicacao.md`
- **Gatilho de reavaliação**: —

## A ideia

Cada task passa por revisão em contexto fresco, não só a entrega do ciclo. Erro encontrado
cedo custa menos, e o revisor que não executou vê o que o executor não vê.

## Por que atravessa (ou não)

Absorvida **parcialmente**, de propósito: revisão por task em toda mudança seria cerimônia
desproporcional na raia leve (Princípio VII). Virou *checkpoint* leve na raia plena com mais
de três tasks. A parte integral da ideia — revisão independente em contexto fresco no
fechamento — já era `TAIL:review`, e reprovou quatro ciclos seguidos (042 a 045) e o 046.

## Dimensões

| # | Dimensão | Leitura |
|---|---|---|
| 1 | Conflito com princípio | integral conflitaria com VII; parcial, não |
| 2 | Licença e redistribuição | MIT na origem; prática reimplementada |
| 3 | Função já servida | parcialmente: havia revisão de ciclo, não de task |
| 4 | Custo de contexto | um contexto fresco por checkpoint |
| 5 | Reversibilidade | total |
| 6 | Maturidade e evidência | forte: as revisões independentes reprovaram cinco dos seis últimos ciclos |
| 7 | Dor real hoje | sim, comprovada |
