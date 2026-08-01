# Tasks 014 — Navegação em cinco trilhas

## Verificação primeiro
- [x] **T0** — Checks: build ≥34 páginas, colisão falha o build, 5 tipos, 5 READMEs, capa sem `blob/main`.

## Implementação
- [x] **T1** — FR2: quatro receitas + índice (`docs/receitas/`), cada uma com "Pronto quando".
- [x] **T2** — FR3: `docs/jornada/README.md` — 12 paradas (tensão · pergunta · regra nascida).
- [x] **T3** — FR1/FR4: `sumario.json` em cinco trilhas com `tipo`/`descricao` + bloco `cadencia`.
- [x] **T4** — FR1/FR4: `build.mjs` renderiza tipo e descrição (lateral + sumário) e os
  cartões de cadência; CSS correspondente.
- [x] **T5** — FR5: capa aponta para as cinco trilhas; nenhum link de conteúdo para o GitHub.

## Correção de defeito (encontrado no ciclo)
- [x] **T6** — Colisão de slug: cinco `README.md` viravam `readme.html`. Corrigido nas duas
  funções (item e resolvedor) + **fitness function** que falha o build; testada com
  colisão deliberada (exit 1).

## Documentação viva (mesmo PR)
- [x] **T7** — CHANGELOG; site reconstruído (34 páginas, links OK).

## Gate
- [x] **T8** — DoD verde → `promover-main.sh` (registro automático do gate).
