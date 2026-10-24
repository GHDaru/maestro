# Tasks 070 — Workflow do ciclo em SQLite: rodadas, passos, outbox e hooks

> **Ciclo retroativo.** O código veio pronto da branch `w07-064-integrate` (`b33bb81`, 14
> commits de 02/10/2026, linhagem A do Hindiana) e entrou pelo merge `f37bf89`; hooks movidos e
> spec renumerada em `8ef082f`. As tarefas `[x]` já aconteceram e têm o hash como evidência; as
> `[ ]` são o que falta para o ciclo fechar pelo método. Nenhuma caixa da cauda é marcada antes
> de a evidência existir.
>
> Siglas: ADR (*Architecture Decision Record*, registro de decisão de arquitetura) · DoD
> (*Definition of Done*, definição de pronto) · FR (*functional requirement*, requisito
> funcional) · WAL (*write-ahead log*, modo de escrita do SQLite).

## Verification first

- [x] **T0** — DoD executável definida em `plan.md § Verification` a partir dos critérios de
      aceite da spec. Medida em 22/10/2026 nesta worktree: `python -m pytest painel/tests -q`
      → `46 passed` (24 da linhagem A mais 22 da B). Princípio IV declarado com honestidade:
      os testes vieram com o código no mesmo merge; não há par vermelho/verde conferível por
      hash neste ciclo, e FR2/FR3 não têm teste nomeado (dívida 1 do plano).

## Implementation (já feito — evidência: hash do commit)

- [x] **T1** — Schema SQLite `painel/schema_workflow.sql`: `rodadas`, `passos`, `transicoes`,
      `fila`, modo WAL; append-only por convenção, sem gatilho (dívida 5 do plano). (FR8, FR9)
      Origem `b33bb81`; evidência **`f37bf89`**.
- [x] **T2** — Hook `SessionStart` `painel/hooks/workflow_session_start.py`: registra a entrada
      (rodada, passo, sessão, hora) e mostra os passos abertos. **Parcial**: não grava branch nem
      hash (FR1, dívida 8) e não recusa a entrada sem saída anterior (FR2 ausente, dívida 1) —
      corrigido pela revisão em contexto fresco. (FR1 parcial, FR7) **`f37bf89`**, caminho final
      em **`8ef082f`**.
- [x] **T3** — Hook `Stop` `painel/hooks/workflow_stop.py`: **invertido** em relação a FR3 — fecha
      o passo sozinho (`resultado='skip'`) e só avisa no stderr, em vez de cobrar (dívida 7,
      achado 3 da revisão); `_ensure_schema` quando o banco não tem as tabelas
      (`test_stop_com_db_sem_tabelas_workflow`, que prova só esse caminho). JSON da fila montado
      com `json.dumps` desde **`3d3da3b`** (achado 2 da segurança). **`f37bf89`**, **`8ef082f`**.
- [x] **T4** — Ingest transacional em `painel/ingest.py`: reconstrói em arquivo temporário e
      troca no fim; versão anterior continua servindo se interrompido
      (`test_ingere_interrompido_mantem_anterior`, `test_ingere_completo_faz_swap`). (FR5, FR12,
      FR14) **`f37bf89`**.
- [x] **T5** — Fila outbox `painel/fila_outbox.py` (`FilaOutbox`, `FilaMensagem`):
      `test_enfileirar_drenar`, `test_drenar_destino_especifico`, `test_fila_outbox`. (FR9)
      **`f37bf89`**.
- [x] **T6** — Roadmap com rodada, passo atual, tempo e quem
      (`test_rodada_com_passo_atual_tempo_e_quem`). (FR4) **`f37bf89`**.
- [x] **T7** — Equipe configurada aparece em `/api/meta`; `test_meta_equipes_tem_19_sessoes`
      **injeta** os 19 nomes no `cfg` (não lê a fixture, que tem 8 — achado 6 da revisão, dívida
      9); `hindiana.json` removido no merge. (FR10 como requisito do Hindiana) **`f37bf89`**.
- [x] **T8** — Aviso de leitura velha: `ingerido_age_min` em `/api/meta` e o aviso em
      `index.html` `meta()` (`test_meta_inclui_idade_do_ingest`). (FR11) **`f37bf89`**.
- [x] **T9** — Erros de leitura: `/api/erros` com caminho e motivo
      (`test_erros_leitura_retorna_caminho_e_motivo`, `test_ingere_registra_erro_de_leitura`,
      `test_ingere_erro_real_vai_para_erros_leitura`). (FR6) **`f37bf89`**.
- [x] **T9b** — Decisões aparecendo no painel (`test_decisoes_nao_vazias`). **`f37bf89`**.
- [x] **T10** — `data-model.md` com entidades e relações (veio da linha paralela). **`f37bf89`**.
- [x] **T11** — `ux-design.md` com o desenho da tela (veio da linha paralela). **`f37bf89`**.
- [x] **T12** — Escrita concorrente em `eventos` sem "database is locked"
      (`test_eventos_escrita_concorrente_nao_trava`). (FR13) **`f37bf89`**.

## Fechamento (a fazer)

- [x] **T13** — Escrever este plano com o Constitution Check (oito linhas), os cinco `ART` e os
      quatro tokens `DOM` com motivo. Critério: `scripts/check-conformance.sh 070` imprime
      `domain model declared`. Marcar ao commitar.
- [x] **T14** (`docs/governance/glossary.md`, linhas "Cycle 070", em inglês, ADR 0014) —
      **rodada**, **passo**, **outbox**. Critério: `grep -c 'Cycle 070' docs/governance/glossary.md`
      → 3; `check-language.sh` e `check-links.sh` verdes.
- [x] **T15** (`docs/adr/0025-hooks-de-terceiro-gravando-sqlite.md` + linha no `README.md` dos ADRs
      + linha em `docs/records/decisoes.jsonl`, só acréscimo) — Critério: `check-adr.sh` verde.
- [x] **T16** (`qa-report.md`, saídas reais) — Colar a saída de cada linha da DoD; as mutações
      com o resultado observado e os nomes dos testes capturados da saída; as dívidas 1 a 4 como
      dívida, não como verde. Critério: `scripts/check-conformance.sh 070` verde.

- [x] **T18** — Correções nascidas das caudas, cada uma com teste vermelho antes e verde depois:
      `test_payload_invalido_nao_envenena_a_fila` (**`3d3da3b`**, segurança achado 2) e
      `test_ingere_preserva_tabelas_do_workflow` (**`04e559c`**, revisão achado 1: cada ingest
      apagava rodadas, passos, transicoes e fila). Suíte: 48 verdes.

## Living documentation (same pull request)

- [x] **T17** (CHANGELOG `[Unreleased]` e roadmap F34) — entrada "ciclo 070" em `### Adicionado`
      (uma seção por tipo, gate `check-version.sh`); linha **F34** no roadmap. Critério:
      `grep -c 'ciclo 070' CHANGELOG.md` ≥ 1; `grep -c 'F34' docs/roadmap.md` ≥ 1.

## Closing tail — MANDATORY, one line each, never delete

<!-- TICK ONLY WHILE WRITING THE EVIDENCE, never in advance: the box records what happened.
     Do not delete a line to say it does not apply: write `n/a: <reason>` on it.
     check-conformance.sh requires the evidence of every non-n/a step in qa-report.md. -->

- [x] **TAIL:review** — independent review in **fresh context**, by whoever did not execute
  (Theorem 2). Evidence: the verdict, in `qa-report.md`. Aqui: revisar a integração (`f37bf89`,
  `8ef082f`, spec, este plano) contra os 14 FR; conferir a resolução de `index.html` (roteamento
  de B, meta de A) e que nenhuma referência a `scripts/hooks/workflow_` sobrou.
- [x] **TAIL:security** — security pass proportional to the risk class. Classe **média**: hooks
  de terceiro escrevem num SQLite local; `install_hooks.py` edita o `settings.json` de outro
  projeto; a fila transporta texto entre sessões. Evidence: the verdict, in `qa-report.md`.
- [x] **TAIL:mutation** — every gate this cycle created or changed was **broken on purpose and
  seen refusing**. Nenhum `scripts/check-*.sh` é tocado; os portões deste ciclo são o filtro por
  destino da fila outbox, o swap atômico do ingest e o schema das tabelas, provados pelos testes
  (cada mutação em cópia restaurada byte a byte). Evidence: the mutation and its output, in
  `qa-report.md`.
- [x] **TAIL:gate** (aberto por delegação em 24/10/2026 — `decisao-072-gates-delegados`, ADR 0026;
  crítico `process-guardian` em contexto fresco: APPROVE_WITH_CONDITIONS, cinco condições
  fechadas no `qa-report.md`; spec declarada parcial, não concluída) — DoD green → guardian
  verdict → human merge gate by written delegation; promotion via `scripts/promote-main.sh`
  (records `gate-main-<sha>` automatically, ADR 0009).
