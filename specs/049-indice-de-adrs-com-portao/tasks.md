# Tasks 049 — O índice de decisões com portão

## Verification first
- [x] T0 — `scripts/check-adr.sh` com os três invariantes, e a mutação que **reconstrói o
  defeito real do ciclo 046** para provar que o portão o teria pego.

## Implementation
- [x] T1 — entrada ausente é falha declarada, nunca silêncio.
- [x] T2 — status lido por `grep`, não por número de linha (os ADRs 0005 e 0008 têm nota
  acima do cabeçalho desde o ciclo 047).
- [x] T3 — `check-adr` na CI como bloqueante, documentado em `scripts/README.md` e **enviado
  pelo instalador** (revisão de escopo: o método tem de funcionar onde cai).
- [x] T3b — `.specify/templates/adr-index-template.md`, para que o primeiro ADR de um projeto
  instalado tenha receita em vez de portão vermelho sem saída.
- [x] T4 — fechar `achado-046-indice-adr-congelado` no índice de decisões.
- [x] T5 — registrar: CHANGELOG, roadmap.

## Closing tail — MANDATORY, one line each, never delete
<!-- TICK ONLY WHILE WRITING THE EVIDENCE, never in advance: the box records what happened.
     Do not delete a line to say it does not apply: write `n/a: <reason>` on it.
     check-conformance.sh requires the evidence of every non-n/a step in qa-report.md. -->
- [x] TAIL:review — independent review in fresh context, by whoever did not execute
- [x] TAIL:security — security pass proportional to the risk class
- [x] TAIL:gate — DoD green -> guardian verdict -> human merge gate (not delegable)
