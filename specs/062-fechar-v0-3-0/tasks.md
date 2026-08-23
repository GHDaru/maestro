# Tasks 062 — Fechar a v0.3.0

## Verification first
- [x] T0 — medir antes de cortar: 18 itens de 11 ciclos em `[Unreleased]`, versão corrente
      0.2.0 em quatro lugares, e `git tag -l` **vazio**.

## Implementation
- [x] T1 — `[Unreleased]` vira `[0.3.0] — 2026-08-22`, com a nota de release (o que ela é ·
      o que ela **não** tem) e um `[Unreleased]` novo e vazio acima. (FR1)
- [x] T2 — README, roadmap e plugin declaram `0.3.0`; plugin reempacotado. (FR2)
- [x] T3 — `check-installed.sh` compara o `install-options.json` que a receita publica com o
      que o `init` grava. Nasceu acusando `maestro_version: 0.2.0`, parado havia 11 ciclos. (FR3)
- [x] T4 — a tag `v0.3.0` criada localmente; publicação **tentada quatro vezes e falhada**, e
      o estado do remoto **lido** com `git ls-remote --tags`. (FR4)
- [x] T5 — roadmap ganha `F27 — A porta da frente` e `F28 — v0.3.0`. (FR5)
- [x] T6 — a contagem de portões da nota corrigida antes de publicar: "quinze bloqueando"
      virou "quatorze inteiros mais a metade bloqueante da conformidade", que é o fato.

## Closing tail — MANDATORY, one line each, never delete
<!-- TICK ONLY WHILE WRITING THE EVIDENCE, never in advance: the box records what happened.
     Do not delete a line to say it does not apply: write `n/a: <reason>` on it.
     check-conformance.sh requires the evidence of every non-n/a step in qa-report.md. -->
- [ ] TAIL:review — independent review in fresh context, by whoever did not execute
- [x] TAIL:security — security pass proportional to the risk class
- [x] TAIL:mutation — every gate created or changed here, broken on purpose and seen refusing
- [x] TAIL:gate — DoD green -> guardian verdict -> human merge gate (not delegable)
