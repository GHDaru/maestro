# Tasks 053 — Peças de apresentação: o fluxo v5 e o caderno de desenvolvimento

## Verification first
- [x] T0 — contar no disco o que as peças vão afirmar (agentes, comandos, skills, portões,
      bloqueantes na CI) antes de escrever qualquer número.

## Implementation
- [x] T1 — `docs/diagramas/06-fluxo-v5-proposta.md`, rotulada proposta em três lugares.
- [x] T2 — `docs/handbook/apresentacao-desenvolvimento-maestro.html`, reusando o esqueleto
      visual das apresentações existentes.
- [x] T3 — linha nova em `docs/diagramas/README.md` e em `docs/handbook/README.md`.
- [x] T4 — entrada em `CHANGELOG.md` sob `[Unreleased]`.
- [x] T5 — aplicar o parecer da revisão independente: oito grupos de defeito, todos de
      **afirmação sem lastro** (o defeito que corresponde, num ciclo de documentação, ao
      anti-padrão 13). Detalhe no `qa-report.md`.

## Closing tail — MANDATORY, one line each, never delete
<!-- TICK ONLY WHILE WRITING THE EVIDENCE, never in advance: the box records what happened.
     Do not delete a line to say it does not apply: write `n/a: <reason>` on it.
     check-conformance.sh requires the evidence of every non-n/a step in qa-report.md. -->
- [x] TAIL:review — independent review in fresh context, by whoever did not execute
- [x] TAIL:security — security pass proportional to the risk class
- [x] TAIL:gate — DoD green -> guardian verdict -> human merge gate (not delegable)
