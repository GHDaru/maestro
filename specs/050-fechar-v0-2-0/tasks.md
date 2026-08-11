# Tasks 050 — Fechar a v0.2.0

## Verification first
- [x] T0 — `scripts/check-version.sh` escrito **antes** do corte, visto verde em 0.1.0 e
  vermelho no estado intermediário real do próprio ciclo.

## Implementation
- [x] T1 — nota de release da `0.2.0` com as três partes, incluindo a tag não publicada.
- [x] T2 — corte nas quatro declarações; plugin reempacotado.
- [x] T3 — `check-version` na CI como bloqueante e documentado em `scripts/README.md`.
- [x] T4 — tag local `v0.2.0` no commit da versão, com o comando de publicação escrito.
- [x] T5 — registrar: roadmap e índice de decisões.

## Closing tail — MANDATORY, one line each, never delete
<!-- TICK ONLY WHILE WRITING THE EVIDENCE, never in advance: the box records what happened.
     Do not delete a line to say it does not apply: write `n/a: <reason>` on it.
     check-conformance.sh requires the evidence of every non-n/a step in qa-report.md. -->
- [x] TAIL:review — independent review in fresh context, by whoever did not execute
- [x] TAIL:security — security pass proportional to the risk class
- [x] TAIL:gate — DoD green -> guardian verdict -> human merge gate (not delegable)
