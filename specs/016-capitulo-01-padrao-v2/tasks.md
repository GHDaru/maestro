# Tasks 016 — Capítulo 01 no padrão v2

## Verificação primeiro
- [x] **T0** — Checks: 9 seções, frameworks/fontes preservados, pytest, build.

## Implementação
- [x] **T1** — FR1/FR3: reescrita do capítulo 01 no esqueleto de 9 seções, preservando os
  5 frameworks, as 6 fontes e os conceitos (*accountability* × capacidade, *ex-ante* ×
  *ex-post*, reversibilidade como alavanca).
- [x] **T2** — FR2: §6 com o `promover-main.sh` — saída real do abort com árvore suja e do
  registro automático do gate.
- [x] **T3** — Novo no v2: objetivos, ideia central, anti-padrões, verificação, o que roubar.
- [x] **T4** — FR4: índice do handbook (marca ✨, anatomia v1 agora 02–12) e sumário do site.
- [x] **T5** — FR5: corpus regenerado (262 trechos).

## Automação nascida do ciclo
- [x] **T6** — Fitness function: teste compara páginas do sumário com o corpus; falha
  provada injetando página nova (mensagem com a instrução de regenerar).

## Gate
- [x] **T7** — DoD verde → `promover-main.sh`.
