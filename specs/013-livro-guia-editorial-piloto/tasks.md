# Tasks 013 — Livro: guia editorial, piloto e instalador

## Verificação primeiro
- [x] **T0** — Checks: build 25 páginas, 9 seções, ≥14 "O que provoca", idempotência.

## Implementação
- [x] **T1** — FR1: `docs/livro/guia-editorial.md` (projeto pedagógico, esqueleto v2,
  regras, livro vivo, 5 trilhas, cadência, Iron Law editorial).
- [x] **T2** — FR2: capítulo 13 — 14 decisões com quando/por quê/o que faz/o que provoca,
  exemplo do ciclo real (retro 008 → ADR 0009) e verificação.
- [x] **T3** — FR3: `scripts/instalar-maestro.sh` — testado em destino limpo (47 arquivos)
  e re-execução (15 "mantido"); `--dry-run` verificado.
- [x] **T4** — FR4: sumário do site + índice do handbook com nota de transição v1→v2.

## Documentação viva (mesmo PR)
- [x] **T5** — FR5: ADR 0011, índice de ADRs, registro consultável, CHANGELOG.

## Gate
- [x] **T6** — Decisões do Steward registradas (esqueleto ✔, chat opção c, piloto ✔) →
  `promover-main.sh`.
