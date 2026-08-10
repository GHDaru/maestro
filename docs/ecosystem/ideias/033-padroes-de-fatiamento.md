# 33 — Padrões de fatiamento com regras de desempate (Lawrence, SPIDR)

- **Id**: `padroes-de-fatiamento`
- **Fonte**: `Padrões de fatiamento (Lawrence) + SPIDR`
- **Observado em**: 2026-08-06
- **Veredito no momento**: absorver
- **Destino**: —
- **Gatilho de reavaliação**: primeira intenção grande **real** que não caiba em um ciclo

## A ideia

Um repertório nomeado de formas de cortar escopo (por caminho, por regra de negócio, por tipo de dado, por interface, por esforço) mais regras de desempate quando dois cortes competem.

## Por que atravessa (ou não)

A pesquisa do upstream registrou **absorver** — "é o miolo da skill que falta". A skill nunca foi escrita: verificado em 2026-08-10, não há skill de fatiamento em `skills/`. O destino nunca existiu, o que faz disto `observar` com gatilho, e não absorção. Terceiro caso da mesma família que motivou este ciclo, e o portão o pegou pelo mesmo invariante.

## Dimensões

| # | Dimensão | Leitura |
|---|---|---|
| 1 | Conflito com princípio | nenhum |
| 2 | Licença e redistribuição | literatura: a técnica é livre de reimplementar, o texto não é de copiar |
| 3 | Função já servida | não: não há skill de fatiamento |
| 4 | Custo de contexto | baixo |
| 5 | Reversibilidade | total |
| 6 | Maturidade e evidência | conhecimento estável e maduro; **zero** experiência nossa — nenhum ciclo precisou fatiar |
| 7 | Dor real hoje | **não**: 47 ciclos, nenhum que não coubesse |
