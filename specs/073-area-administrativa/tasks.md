# Tasks 073 — Área administrativa do Maestro (rodada 1: pesquisa de plataformas)

## Verification first
- [x] T0 — define the DoD checks — critérios de aceite FR1–FR4 na `spec.md` (ficha por plataforma
  com fonte, matriz consolidada, nenhuma célula sem fonte vira "sim", `andamento.md` a cada DONE);
  comandos verificáveis na `plan.md` §Verification.

## Implementation
- [x] T1-W03 — gateways e consoles de LLM: LiteLLM, Portkey, OpenAI Platform, Helicone (4 fichas;
  LiteLLM rodou local com chave descartável, capturas em `pesquisa/img/`).
- [x] T1-W05 — observabilidade e orquestração de agentes: 9 fichas (7 do despacho + Arize Phoenix
  e Comet Opik no mesmo nicho).
- [x] T1-W06 — controle de processos e governança: 12 fichas (10 do despacho + AWS Bedrock
  AgentCore e Windmill na mesma raia); pausou para a reverificação R1/R2 do ciclo 072 e retomou.
- [x] T1-consolidacao — `pesquisa/plataformas.md`: matriz 25 plataformas × 26 funcionalidades,
  fechada por acréscimo pelo Worker06 (as 13 colunas que faltavam depois das 12 dele).
- [ ] T1-revisao — verificação em contexto fresco pelo Worker03 (não consolidou): amostragem
  dirigida de 7 células + recontagem independente + passagem de segurança sobre `pesquisa/`.
- [ ] T1-fechamento — Gerente: preenche plan/qa-report, marca o rabo com a evidência, roda
  check-conformance 073 e emite o DONE da rodada 1 ao regente (a rodada 2 espera o "segue").

## Closing tail — MANDATORY, one line each, never delete
<!-- TICK ONLY WHILE WRITING THE EVIDENCE, never in advance: the box records what happened.
     Do not delete a line to say it does not apply: write `n/a: <reason>` on it.
     check-conformance.sh requires the evidence of every non-n/a step in qa-report.md. -->
- [ ] TAIL:review — independent review in fresh context, by whoever did not execute
- [ ] TAIL:security — security pass proportional to the risk class
- [ ] TAIL:mutation — every gate created or changed here, broken on purpose and seen refusing
- [ ] TAIL:gate — DoD green -> guardian verdict -> human merge gate (not delegable)
