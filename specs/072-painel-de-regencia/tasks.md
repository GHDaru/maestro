# Tasks 072 — Painel de regência, rodada 1: kanban por gate e fila de decisões

> Uma seção por Worker, com a etiqueta `[[TASK ...]]` sozinha na linha (task-ledger). Quem executa
> termina com `[[DONE id=… outcome=delivered|blocked|failed]]`. **Nenhuma caixa é marcada antes de a
> evidência existir** — a caixa registra o que aconteceu, não o que se pretende.
>
> Plano: `plan.md` (aprovado no gate do plano). Spec: `spec.md` — **revisão T01b**, 25 FR.
>
> Siglas: ADR (*Architecture Decision Record*) · CI (*Continuous Integration*) · DoD (*Definition of
> Done*) · FR (*functional requirement*) · HTML (*HyperText Markup Language*) · JSONL (*JSON Lines*).

## Verification first

- [ ] **V0** — A DoD executável de `plan.md § Verification` (13 testes nomeados + os pares comando →
  resultado) é a régua deste ciclo. Os testes das **regras puras** nascem **antes** do adaptador HTTP
  (Princípio IV): primeiro o vermelho, depois o verde — cada um com o hash do par vermelho/verde no
  `qa-report.md`.

## Escopo A — kanban por gate

### Worker03 — domínio puro + parser (FR5)

`[[TASK id=072-T03 kind=implement cycle=072 attempt=1]]`

- [ ] Criar `painel/regencia/` (**puro**): `__init__.py`, `normalizacao.py`
      (`normaliza(valor, erros=None)` — FR10), `kanban.py` (`coluna_do_cartao`, `independencia`,
      `idade_do_carimbo`, `faixa_abertura_gd` — FR2/FR4/FR23/FR1), `fila.py` (`valida_pedido`,
      `valida_ruling`, `sai_da_fila`, `ordena_fila`, `portao_derivado` — FR11/FR14/FR12/FR15/FR20).
      **Nada** em `painel/regencia/` importa `http.server`, `sqlite3` nem abre arquivo.
- [ ] **FR5**: estender `painel/chamados.py` (`valida`/`confere`, ~`painel/chamados.py:81-148`) para
      ler `autor_da_peca` do cabeçalho do gate e devolvê-lo **no item**, ao lado de `por`. **Sem o
      campo → "—" com motivo** (nunca verde presumido). Não tocar `conferir_chamado.py`.
- [ ] Criar `painel/tests/test_regencia.py` com o **núcleo** dos testes puros:
      `test_f6_normalizacao_tabela_dirigida`, `test_f4_pedido_sem_ruling_fica_na_fila`,
      `test_f5_ruling_sem_autor_humano_ou_destino_e_recusado`, `test_f7_idade_do_relogio_e_carimbo`,
      `test_f8_traco_com_motivo`, `test_f2_cartao_em_gn_exige_arquivo_do_gate`.
      Deixar no fim do arquivo o comentário `# --- APPEND AQUI (W04/W05/W07) ---`.
- [ ] Regressão: `painel/tests/test_chamados.py` verde e `python painel/chamados.py
      painel/projetos/exemplo.json` → exit 0.
- Evidência: hash do commit; saída dos testes (com o par vermelho/verde) no `qa-report.md`.
- **Depende de**: plano aprovado. **Entrega para**: W04, W05, W07 (apensam testes aqui).

### Worker04 — rotas e tela do kanban

`[[TASK id=072-T04 kind=implement cycle=072 attempt=1]]`

- [ ] `GET /api/regencia/kanban` em `painel/server.py`: dez colunas G0–G9 (FR1) **reusando**
      `chamados.confere` (não criar segundo conferidor), o cartão com id/frente/dono(papel+sessão)/
      veredito normalizado **ao lado do original**/idade/selo (FR3), o marcador de independência
      (FR4) e a **faixa `abertura`·`GD`** acima do kanban (limites da spec).
- [ ] `POST /api/regencia/transicao`: valida o arquivo do gate de destino + cabeçalho; devolve a
      proposta; **não move nem grava**; sem arquivo válido → **422 com motivo** (FR9). Manter a
      recusa fora de localhost (`painel/server.py:507`) e o `ValueError`→422 (`:523`).
- [ ] `cfg["frentes"]` exposto em `/api/meta` (`v_meta`, `painel/server.py:283`) e filtro por frente
      na tela (FR7); sem escolha, todas.
- [ ] Tela do kanban em `painel/index.html` (`vKanban` + botão de nav): lista (não `div` solta),
      estado nunca só cor, todo número/selo com `data-fonte` (FR21), "—" com `motivo:` (FR22),
      botões só-ícone com `aria-label` (FR24).
- [ ] Apensar no fim de `painel/tests/test_regencia.py`:
      `test_f1_metrica_sem_data_fonte_zero_no_html_renderizado` (FR21),
      `test_f9_botao_so_icone_com_aria_label_no_html_renderizado` (FR24),
      `test_f3_transicao_sem_arquivo_devolve_422` (FR9),
      `test_f10_ingestao_defasada_anunciada` (FR25). **F1/F9 sobre o HTML renderizado** (não `grep`).
- Evidência: hash; a saída dos testes de HTML renderizado no `qa-report.md`.
- **Depende de**: W03 (parser + `regencia/`). **Fatia**: `painel/server.py` (funções do kanban e da
  transição), `painel/index.html` (`vKanban`).

## Escopo B — fila de decisões

### Worker05 — registro, rotas e tela da fila

`[[TASK id=072-T05 kind=implement cycle=072 attempt=1]]`

- [ ] `painel/fila_registro.py` (adaptador): `caminho(cfg)` (padrão
      `painel/dados/fila-<projeto>.jsonl`, chave `cfg["fila_decisoes"]`), `acrescenta(caminho, obj)`
      — **sempre** `open(..., "a", encoding="utf-8")`, `json.dumps(..., ensure_ascii=False)` + `\n`,
      **nunca** `"w"`/`truncate`/`seek` — e `le(caminho)` tolerante a linha inválida (FR16).
- [ ] `GET /api/regencia/fila` (pedidos + portões derivados, ordenados por prazo × bloqueio com nº de
      destravados — FR15) e `POST /api/regencia/fila` (acrescenta `pedido` ou `ruling`; **422 com
      motivo** — FR11/FR14). Manter a recusa fora de localhost.
- [ ] **FR20**: para cada G7/G8/`TAIL:gate` pendente, criar o **item de fila** com id derivado
      (chamado+gate), status do arquivo de gate e "desde quando" do commit; **marcador no cartão** com
      link para o item; a um agente, **somente leitura** ("portão do regente").
- [ ] Tela da fila em `painel/index.html` (`vFila` + botão de nav): item, idade **"há Xh Ymin" + o
      carimbo absoluto** no atributo do elemento, **contador da idade do item mais velho no
      cabeçalho** (FR23); "responder" grava `autor = humano` do formulário (FR18), **nunca
      pré-marcado** (FR19); "devolver a quem pediu" registrado (FR13); "encaminhado a …" (FR13);
      fila vazia = "fila vazia — última decisão às HH:MM".
- [ ] Apensar no fim de `painel/tests/test_regencia.py`: `test_f14_registro_append_only_so_cresce`
      (FR16 — guarda o **prefixo de bytes** e prova que ficou inalterado) e
      `test_portao_do_regente_item_com_id_derivado` (FR20).
- Evidência: hash; a saída do teste do prefixo de bytes no `qa-report.md`.
- **Depende de**: W03. **Fatia**: `painel/server.py` (`v_fila` + ramo do JSONL), `painel/index.html`
  (`vFila`).

## Escopo C — herança do 070 (a dívida 5 vira FR)

### Worker07 — append-only mecânico na base (FR17)

`[[TASK id=072-T07 kind=implement cycle=072 attempt=1]]`

- [ ] `painel/schema_workflow.sql`: três `TRIGGER` (`BEFORE UPDATE` e `BEFORE DELETE` em `rodadas`,
      `passos`, `transicoes` → `RAISE(ABORT, …)`). Hoje **não há gatilho nenhum** no arquivo.
- [ ] `CREATE TRIGGER IF NOT EXISTS` nas cópias de `_ensure_schema` (hooks + `fila_outbox.py`) para
      que um banco vivo ganhe os gatilhos.
- [ ] Ajustar `painel/hooks/workflow_stop.py` para **não** escrever `UPDATE passos` (o gatilho torna o
      `UPDATE` impossível): só avisar no `stderr`. **Não** implementar a cobrança de verdade (dívida 7
      → rodada 2) — declarar no docstring que fica para a rodada 2.
- [ ] Apensar `test_divida5_gatilho_recusa_update_e_delete` em `test_regencia.py` (aplica o schema num
      banco temporário, tenta `UPDATE`/`DELETE`, espera `sqlite3.IntegrityError`).
- Evidência: hash; a saída do teste do gatilho no `qa-report.md`; a declaração de que a dívida 2
  **piora** (D-072-2) e de que a dívida 7 **não** é paga.
- **Depende de**: nada (paralelo a W03/W04/W05).

## Escopo D — jornada viva e documentação

### Worker08 — jornada viva (FR26)

`[[TASK id=072-T08 kind=docs cycle=072 attempt=1]]`

- [ ] `docs/journeys/072-painel-de-regencia.md` (skill `living-journey`): o caminho passo a passo do
      regente (ux-design §3), as **imagens geradas por um script versionado** do build real
      (`docs/journeys/scripts/captura-072.sh`) e a **heurística datada ≥** a data da captura, com
      severidade e status por achado; o documento cita a spec e traz o marcador **F11**.
- [ ] Se o ambiente **não** renderizar a tela real: entregar o script e a heurística e declarar a
      captura como **pendente** (D-072-7) — **nunca** inventar imagem nem reaproveitar captura velha.
- [ ] Somar `docs/journeys/*.md` ao glob `documentos.jornadas` de `painel/projetos/exemplo.json`
      (hoje só `docs/jornada/*.md`; a skill usa o plural em inglês — `skills/living-journey/SKILL.md:30`).
- Evidência: `ls docs/journeys/072-*.md`; `grep -c 'F11' docs/journeys/072-*.md` ≥ 1; `check-links.sh`
  verde (as imagens/links relativos resolvem).
- **Depende de**: W04 e W05 (a tela precisa existir para a captura).

## Fechamento — revisão, segurança, mutação e artefatos vivos

### Worker06 — revisão e segurança em contexto fresco + `qa-report.md`

`[[TASK id=072-T06 kind=review cycle=072 attempt=1]]`

- [ ] Revisão **em contexto fresco**, por quem não executou (Teorema 2), do diff integrado contra o
      plano e os 25 FR: veredito no `qa-report.md`. Procurar os anti-padrões (`anti-patterns`, 23
      itens), com atenção a "cópia com perdas" do conferidor e a `abertura`/`GD` virando coluna.
- [ ] **Passo de segurança** proporcional à classe (média: rotas POST novas, gatilho na base, leitura
      de arquivo): confirmar que nenhuma rota POST aceita fora de `127.0.0.1`, que o *ruling* grava
      `autor` do formulário (não inferido do agente que pediu), que `grep -rn '\.env\|settings.local.json'
      painel/` não acha caminho de **leitura**, e que as dívidas herdadas de segurança (**D-072-3**,
      CSRF/autoria; **D-072-4**, `data()`; **D-072-5**, `custo.py`) ficam **declaradas** — não
      silenciadas nem vendidas como pagas. Veredito no `qa-report.md`.
- [ ] Colar no `qa-report.md` a saída real de **cada** linha da DoD do plano (os 13 testes nomeados, os
      pares comando → resultado, as regressões) e as dívidas D-072-1..7 como dívida.
- [ ] `[[DONE id=072-T06 outcome=delivered|blocked|failed]]` ao terminar.
- **Depende de**: W03, W04, W05, W07, W08 integrados.

### Worker09 — artefatos vivos (mesmo PR)

`[[TASK id=072-T09 kind=docs cycle=072 attempt=1]]`

- [ ] `docs/governance/glossary.md` (em inglês, ADR 0014): **painel de regência**, **pedido de
      decisão**, **ruling**, **veredito normalizado**, **portão do regente** (coluna "Cycle 072").
      Critério: `grep -c 'Cycle 072' docs/governance/glossary.md` → 5 e `check-language.sh` verde.
- [ ] `docs/adr/0026-gates-humanos-delegados-sessao-regente.md` (a decisão do DoR) e
      `docs/adr/0027-registro-da-fila-e-append-only-mecanico.md` (endereço do registro + os dois
      mecanismos de append-only + rodada 2 = infra) + linha no `README.md` dos ADRs.
      Critério: `scripts/check-adr.sh` verde.
- [ ] `docs/records/decisoes.jsonl`: **só acrescentar** uma linha (ADR 0026 e 0027) via
      `scripts/record-decision.sh` — **nunca** reescrever (guard `guard-immutables.py`).
- [ ] `CHANGELOG.md` `[Unreleased]` (entrada "ciclo 072") e `docs/roadmap.md` (linha do ciclo 072).
      Critério: `grep -c 'ciclo 072' CHANGELOG.md` ≥ 1; `grep -c '072' docs/roadmap.md` ≥ 1.
- **Depende de**: nada (pode correr em paralelo; fecha antes do gate).

## Closing tail — MANDATORY, one line each, never delete

<!-- TICK ONLY WHILE WRITING THE EVIDENCE, never in advance: the box records what happened.
     Do not delete a line to say it does not apply: write `n/a: <reason>` on it.
     check-conformance.sh requires the evidence of every non-n/a step in qa-report.md. -->

- [ ] **TAIL:review** — independent review in **fresh context**, by whoever did not execute
  (Theorem 2). Evidence: the verdict, in `qa-report.md`. Aqui: revisar os 25 FR contra o diff
  integrado (kanban, fila, parser FR5, gatilho FR17) e contra as anti-regras 1–8.
- [ ] **TAIL:security** — security pass proportional to the risk class. Classe **média**: duas rotas
  POST novas, gatilho que passa a recusar escrita na base herdada, leitura/escrita de arquivo local.
  Evidence: the verdict, in `qa-report.md`, com as dívidas herdadas (D-072-3/4/5) declaradas.
- [ ] **TAIL:mutation** — every gate this cycle created or changed was **broken on purpose and seen
  refusing**, quebrando a **CONDIÇÃO** (não o nome) de FR10 (normalização), FR12 (permanência na
  fila), FR9 (transição sem arquivo) e FR17 (o gatilho), e **colando os nomes dos testes que falham**.
  Evidence: the mutation and its output, in `qa-report.md`.
- [ ] **TAIL:gate** — DoD green → guardian verdict → **human merge gate (not delegable on the
  origin; delegated this round to the regent session with an independent critic, ADR 0026)**;
  promotion via `scripts/promote-main.sh` (records `gate-main-<sha>` automatically, ADR 0009).
