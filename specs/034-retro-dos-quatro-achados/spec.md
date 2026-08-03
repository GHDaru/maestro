# Spec 034 — Retrospectiva: os quatro achados abertos viram regra

- **Status**: Concluída · **Raia**: plena · **Data**: 2026-08-03
- **Origem**: pedido do Steward — "retro destes quatro". Achados herdados dos ciclos 023,
  027, 029, 031 e 033.

> **Raia**: plena. **Ambiguidade** alta (um achado é "a cerimônia não tem gatilho" — não há
> forma óbvia de codificar isso); **raio** amplo (mexe em skill, scripts, receita, livro e no
> índice de decisões); **irreversibilidade** baixa (tudo é `git revert`). Dois fatores altos
> → plena, conforme a regra de desempate.

## O quê e por quê

Cinco achados estavam registrados em relatórios de qualidade (QA) e nenhum tinha virado
regra. Isso é literalmente o anti-padrão 14 ("achado que morre em candidato") — e o mais
velho deles tinha **onze ciclos**. A retrospectiva existe para fechar exatamente esse laço;
enquanto ela não roda, o método aprende no papel e não no executável.

| Achado | Ciclo | Sintoma |
|---|---|---|
| Régua de raias não aplicada | 023 | 19 specs "plena" contra 2 "leve" |
| Retrospectiva sem gatilho | 027 | acontecia quando alguém percebia |
| Regra de skill não chega ao capítulo | 029 | a segunda lei ficou 10 ciclos fora do livro |
| Elo de commit sem portão | 031 | 28 commits citando a spec por hábito |
| Renome em massa quebra link fora do site | 033 | duas trocas excessivas passaram pelo build |

## Requisitos funcionais

- **FR1**: QUANDO houver achado aberto demais (≥4) ou achado aberto velho demais (≥6 ciclos),
  `check-retro.sh` DEVE falhar cobrando a retrospectiva.
- **FR2**: QUANDO uma spec de ciclo ≥034 declarar a raia, ela DEVE justificar com os três
  fatores; `check-cycle.sh` DEVE falhar sem a justificativa e DEVE imprimir a distribuição.
- **FR3**: QUANDO um commit à frente de `main` não citar `spec NNN` ou `ADR NNNN`,
  `check-cycle.sh` DEVE falhar.
- **FR4**: QUANDO uma skill mudar depois da última revisão de um capítulo que a cita,
  `check-chapters.sh` DEVE falhar apontando o capítulo atrasado.
- **FR5**: QUANDO qualquer link relativo do repositório apontar para arquivo inexistente,
  `check-links.sh` DEVE falhar — inclusive fora das páginas publicadas.
- **FR6**: Os cinco achados DEVEM ser fechados no índice de decisões por linha nova
  (append-only), citando a regra que os fecha.

## Fora de escopo

- Reclassificar as raias das specs antigas (registro histórico).
- Automatizar a retrospectiva em si — o gatilho é mecânico, a cerimônia continua humana.

## Critérios de aceite (DoD)

- [x] Os cinco achados registrados como `achado-*` com status `aberta` — e o
      `check-retro.sh` **provado falhando** com eles (5 abertos, o mais velho com 11 ciclos)
- [x] `check-cycle.sh` **provado falhando** (spec sem raia declarada)
- [x] `check-links.sh` **provado falhando** (link apontado para arquivo inexistente)
- [x] `check-chapters.sh` **provado falhando** (skill mais nova que o capítulo)
- [x] Todos verdes ao fim do ciclo; achados fechados por linha nova no índice
- [x] Anti-padrões 17 e 18 no catálogo, com o ciclo de origem

## Clarify

1. O gatilho da retro é calendário ou dívida? → **dívida de achados**. Calendário produz
   cerimônia vazia; achado aberto é a condição que realmente importa.
2. O check pode julgar se a raia está certa? → **não** — ele cobra a justificativa e mostra
   a distribuição. Julgamento continua humano, e o texto do capítulo diz isso.
