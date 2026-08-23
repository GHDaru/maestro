# Tasks 061 — Retro: a caixa marcada sem testemunha

## Verification first
- [x] T0 — medir a dívida antes de opinar sobre ela: `retro.sh`, `check-retro.sh`, e os
      quatro `qa-report.md` de 057–060, que dizem no próprio texto o que se repetiu.

## Implementation
- [x] T1 — `check-conformance.sh --ticked-only`: caixa marcada exige evidência; caixa não
      marcada não deve nada. (FR1)
- [x] T2 — o modo entra na CI como **bloqueante**, ao lado dos outros; o
      `check-conformance.sh` completo continua consultivo. (FR2)
- [x] T3 — `--ticked-only` reduzido a **uma** regra. A contraprova exigida pelo plano mostrou
      que um ciclo recém-gerado reprovava por ART sem motivo — o modo teria reconstruído
      justamente o portão sempre-vermelho que ele existe para evitar. Nasceu o `soft()`.
- [x] T4 — `TAIL:gate` marcado passa a cobrar `package-plugin.sh --verify` no ato da
      afirmação (a CI já cobrava no push; o que faltava era cobrar na hora de afirmar). (FR1)
- [x] T5 — `check-chapters.sh` pergunta ao `git status` antes do `git log`. (FR3)
- [x] T6 — a promessa da linguagem ubíqua sai do `plan-architect` e do `perfis.md`. A primeira
      tentativa **nomeava** `docs/governance/ubiquitous-language.md` e o `check-installed.sh`
      reprovou: nomear o caminho **é** a promessa. (FR4)
- [x] T7 — `check-installed.sh` compara as contagens que as páginas afirmam com a instalação
      de referência. (FR5)
- [x] T8 — as quatro seções `### Adicionado` viram uma; `check-version.sh` passa a ler a
      estrutura de `[Unreleased]`. (FR6)
- [x] T9 — os cinco achados fechados no índice, cada um por linha nova com `fecha`.

## Closing tail — MANDATORY, one line each, never delete
<!-- TICK ONLY WHILE WRITING THE EVIDENCE, never in advance: the box records what happened.
     Do not delete a line to say it does not apply: write `n/a: <reason>` on it.
     check-conformance.sh requires the evidence of every non-n/a step in qa-report.md. -->
- [x] TAIL:review — independent review in fresh context, by whoever did not execute
- [x] TAIL:security — security pass proportional to the risk class
- [x] TAIL:mutation — every gate created or changed here, broken on purpose and seen refusing
- [x] TAIL:gate — DoD green -> guardian verdict -> human merge gate (not delegable)
