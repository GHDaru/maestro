# Tasks 055 — Retro: o portão que mede a frase vira prova por mutação

## Verification first
- [x] T0 — rodar `scripts/retro.sh` e apurar o que os artefatos dizem, não o que eu lembro:
      um achado aberto (047, 7 ciclos) e seis ciclos com o mesmo defeito na revisão.

## Implementation
- [x] T1 — fechar `achado-047` com `fecha`, gatilho citado e motivo; `check-retro.sh` verde.
- [x] T2 — `docs/records/README.md`: a forma "achado cujo remédio virou gatilho".
- [x] T3 — `TAIL:mutation` no template instalável, com a evidência dos seis ciclos no texto.
- [x] T4 — `check-conformance.sh` cobra `TAIL:mutation` a partir do ciclo 055, e decide
      "tocou portão" pelo **diff**, nunca pela prosa do plano.
- [x] T5 — anti-padrão 23 (porta nova, guarda antigo) com o ciclo de origem.

## Closing tail — MANDATORY, one line each, never delete
<!-- TICK ONLY WHILE WRITING THE EVIDENCE, never in advance: the box records what happened.
     Do not delete a line to say it does not apply: write `n/a: <reason>` on it.
     check-conformance.sh requires the evidence of every non-n/a step in qa-report.md. -->
- [x] TAIL:review — independent review in fresh context, by whoever did not execute
- [x] TAIL:security — security pass proportional to the risk class
- [x] TAIL:mutation — every gate created or changed here, broken on purpose and seen refusing
- [x] TAIL:gate — DoD green -> guardian verdict -> human merge gate (not delegable)
