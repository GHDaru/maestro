# Tasks 048 — A instalação que funciona onde ela cai

## Verification first
- [x] T0 — `scripts/check-installed.sh`: instala num diretório vazio, roda todo portão
  enviado e confere toda citação de caminho. Escrito **antes** de qualquer correção e visto
  acusar as nove citações e os dois portões vermelhos.

## Implementation
- [x] T1 — constituição única: os 3 comandos `/speckit.*` apontam para
  `docs/governance/principles.md`; `.specify/memory/constitution.md` é apagado; divergência
  declarada em `.specify/UPSTREAM.md`.
- [x] T2 — `check-roles.sh` diz explicitamente quando não há índice de perfis, e sai verde.
- [x] T3 — `check-conformance.sh` diz explicitamente quando o projeto não tem ciclo nenhum;
  mantém vermelho quando há specs fora do alcance do piso.
- [x] T4 — instalador envia `.specify/scripts/bash/`, `.specify/init-options.json` e
  `scripts/check-retro.sh`.
- [x] T5 — `agent-designer` cita o que é instalado; `/dod` deixa de citar `check-chapters`;
  `THIRD-PARTY-NOTICES.md` deixa de citar o caminho do instalador.
- [x] T6 — `check-installed` na CI como bloqueante; `boundary.json` se preciso.
- [x] T7 — registrar: CHANGELOG, roadmap, índice de decisões.

## Closing tail — MANDATORY, one line each, never delete
<!-- TICK ONLY WHILE WRITING THE EVIDENCE, never in advance: the box records what happened.
     Do not delete a line to say it does not apply: write `n/a: <reason>` on it.
     check-conformance.sh requires the evidence of every non-n/a step in qa-report.md. -->
- [x] TAIL:review — independent review in fresh context, by whoever did not execute
- [x] TAIL:security — security pass proportional to the risk class
- [x] TAIL:gate — DoD green -> guardian verdict -> human merge gate (not delegable)
