# Tasks 047 — Catálogo do ecossistema

## Verification first
- [x] T0 — `scripts/check-ecosystem.sh` com os seis invariantes, escrito **antes** da
  migração e visto acusar por mutação em cada requisito.

## Implementation
- [x] T1 — `data-model.md`: entidades fonte · ideia · estado, cardinalidade, vocabulário
  fechado de veredito e o formato de linha do `estado.jsonl` (é contrato).
- [x] T2 — `docs/ecosystem/README.md`: como funciona, vocabulário, as sete dimensões.
- [x] T3 — `docs/ecosystem/fontes.md`: **toda** fonte já avaliada, com licença e data de
  observação — as **sete** origens, sem perda (a revisão achou 5 fontes e 10 ideias perdidas
  na primeira passada; recuperadas).
- [x] T4 — `docs/ecosystem/ideias/*.md`: um card por ideia, datado, com as sete dimensões.
- [x] T5 — `docs/ecosystem/estado.jsonl`: estado corrente de cada ideia.
- [x] T6 — corrigir o **conteúdo** (não o portão): as **cinco** ideias com destino condicional
  que nunca chegaram a um arquivo voltam a `observar` com gatilho, em **linha nova** datada de
  hoje — nunca editando a linha histórica.
- [x] T7 — `.specify/templates/evaluation-template.md` (em inglês, é instalável) + o
  instalador copiando-o.
- [x] T8 — nota "migrado para" nas sete origens antigas, sem apagar nenhuma.
- [x] T9 — `boundary.json` (toolkit + shared), `publicar/sumario.json` (Bastidores),
  `check-ecosystem` na CI como bloqueante.
- [x] T10 — registrar: CHANGELOG, roadmap, índice de decisões.

## Closing tail — MANDATORY, one line each, never delete
<!-- TICK ONLY WHILE WRITING THE EVIDENCE, never in advance: the box records what happened.
     Do not delete a line to say it does not apply: write `n/a: <reason>` on it.
     check-conformance.sh requires the evidence of every non-n/a step in qa-report.md. -->
- [x] TAIL:review — independent review in fresh context, by whoever did not execute
- [x] TAIL:security — security pass proportional to the risk class
- [x] TAIL:gate — DoD green -> guardian verdict -> human merge gate (not delegable)
