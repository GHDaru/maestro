# Tasks 066 — Painel de regência: ciclo guarda-chuva da integração da linha paralela

> Ciclo de **coordenação**: as tarefas abaixo são o que esta pasta produziu; o código e as caudas
> de cada entrega estão nos ciclos filhos (066 v0, 067, 068, 069, 070; 072 em curso), cada um com
> `tasks.md` e `qa-report.md` próprios. Siglas: ADR (*Architecture Decision Record*) · DoD
> (*Definition of Done*) · UX (*user experience*).

## Verification first

- [x] **T0** — DoD definida em `plan.md § Verification`: presença dos artefatos de coordenação,
      dry-run do lançador, conformance da pasta. Medida em 24/10/2026 (ver `qa-report.md`).

## Coordenação (feito — evidência: arquivo ou hash)

- [x] **T1** — `plano-integracao-linha-paralela.md`: inventário das 42 branches, mapa de
      renumeração 066–072, estratégia e decisões 1–9 (Opus, 19/10).
- [x] **T2** — `handoff-longrun.md` e `andamento.md`: cinco decisões do longrun fechadas com o
      Darú; decisões A, B, C; ponto de retomada do 070; roteiro das sete sessões.
- [x] **T3** — `ux-design.md` (agente `ux-semantics`): papéis semânticos do painel de regência,
      anti-regras, fitness functions F1–F12; insumo da spec do 072.
- [x] **T4** — `scripts/multi-session.py`: lançador adaptado da Hindiana (um modelo por sessão,
      uma worktree por Worker, sem segredo); correção do 401 por herança de
      `ANTHROPIC_BASE_URL` (**`18d7223`**); sete sessões abertas e respondendo em 24/10.
- [x] **T5** — Insumos e pareceres datados: `pareceres-sessoes-via-gateway.md`,
      `insumo-hindiana.md`, `insumo-prompt-setup-harness.md` (Jev, prompt de harness).
- [x] **T6** — Decisões de método: ADR 0024 (cabeçalho conferível, decisão A), ADR 0026 (gate por
      delegação); linhas em `docs/records/decisoes.jsonl`.
- [x] **T7** — Rodada 1 do 072 despachada ao Gerente (24/10); gate DoR aberto por delegação
      (`gate-072-dor-delegado`).

## Dívidas declaradas

1. `scripts/multi-session.py` sem teste (`gateway_url`, `ps_for`); provado só por dry-run e
   abertura real.
2. Colisão de nomes entre projetos ("Gerente" do Maestro × da Hindiana): o lançador deveria
   prefixar os nomes com o projeto; até lá, endereçar com o ref do ListAgents.

## Closing tail — MANDATORY, one line each, never delete

<!-- TICK ONLY WHILE WRITING THE EVIDENCE, never in advance: the box records what happened.
     Do not delete a line to say it does not apply: write `n/a: <reason>` on it.
     check-conformance.sh requires the evidence of every non-n/a step in qa-report.md. -->

- [ ] **TAIL:review** — n/a: ciclo de coordenação sem código de produto; cada ciclo filho (066 v0,
  067, 068, 069, 070) teve revisão independente em contexto fresco registrada no próprio
  `qa-report.md`; o lançador (dívida 1) terá revisão quando ganhar teste.
- [ ] **TAIL:security** — n/a: a superfície deste ciclo é a do lançador, coberta pelos três
  pareceres de `pareceres-sessoes-via-gateway.md` (sem segredo no repositório, uma worktree por
  Worker, token só no escopo de usuário) e pela correção do 401; os ciclos filhos carregam as
  próprias passagens.
- [x] **TAIL:mutation** — o portão lê o número do ciclo, e commits "ciclo 066" tocaram
  `scripts/check-conformance.sh` (a isenção por forma para evidência importada, decisão B1 de
  21/10, `3f590ab`) e `boundary.json` (ciclo 066 v0). As duas mutações foram feitas e vistas
  recusando: a da isenção (um `tasks.md` vazio na pasta importada volta a ser cobrado) está no
  `qa-report.md` do 069 § Findings e é espelhada no `qa-report.md` desta pasta; a do
  `boundary.json` está no `qa-report.md` do 066 v0. Evidence: the mutation and its output, in
  `qa-report.md`.
- [ ] **TAIL:gate** — n/a: a pasta não promove nada por si; os gates estão nos ciclos filhos
  (`gate-dev-integra-066-069`, `gate-main-3f590ab`, `gate-070-delegado`) e a promoção seguinte
  acontece com o fechamento da rodada 1 do 072.
