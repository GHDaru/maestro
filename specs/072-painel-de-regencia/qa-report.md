# QA report 072 — Painel de regência, rodada 1: kanban por gate e fila de decisões

- **Date**: 2026-10-24 · **Lane**: full · **Status**: **open — rodada 1 in progress** (this file
  is the skeleton created before the mutations, as the regent session asked; every section below
  is filled by whoever delivers, with command output, never intention)
- **Verdict**: to be written by the independent review (Worker06, fresh context) after the
  slices integrate

> Ruler of the cycle: the DoD of `plan.md § Verification` (**`Ran 15 tests`** — the 13 named
> tests of `c1eb802` plus the two FR16 proofs the plan gate added; the supersession
> `Ran 13 → Ran 15` is declared there, not silent). Each Worker leaves **green its own slice**
> and pastes here the hash where the red was captured and the hash of the green.
> Measured on this Windows machine, `PYTHONUTF8=1`, branch `066-painel-de-regencia`.

## Evidence per task

> One subsection per task. The worker who delivers appends the real command output under its
> subsection (hash of red, hash of green, test names). Nothing is written here before it
> happened.

### 072-T03b — tests reconciled and widened (Worker03)

- **Delivered** (`[[DONE id=072-T03b outcome=delivered]]`, 24/10): commit `42e24f4` on `w/worker03`
  ("ciclo 072: testes reconciliados e ampliados (gate do plano)"), integrated into the working
  branch in `2b0b768`. One file: `painel/tests/test_regencia.py` (+355/−97). No implementation.
- **Red captured at `42e24f4`**: `PYTHONUTF8=1 python -m pytest painel/tests/test_regencia.py -q`
  → **24 failed in 7.51s**, every one for the right reason (the `regencia/` package, the
  `fila_registro.py` adapter and the regency routes do not exist yet): F1 (served HTML has no
  `.metrica`), F9 (no labeled regency control), F2 (`painel/regencia/` missing), F3 (404 ≠ 422,
  route missing), F4-fila, F5-ruling, F4-independencia, F5-parser (`confere` does not expose
  `autor_da_peca`), F6, F7, F8, F10, F14-so-cresce (`fila_registro.py` missing), dívida5
  (schema has no TRIGGER; UPDATE passed), portão-do-regente, F20-autor-fora, F20-pedido-inexistente,
  F14-AST, F14-concorrente (404), F15-ordena, F23-cabecalho, F1-dez-colunas (404),
  F7-frentes (`frentes` absent from `/api/meta`), F11-valida-pedido.
- **Regressions**: old suite `python -m pytest painel/tests -q --ignore=painel/tests/test_regencia.py`
  → **48 passed in 15.68s**; `python painel/chamados.py painel/projetos/exemplo.json` → **exit 0**.
- **Temp files** `rg_new.txt`/`rg_old.txt` removed from the worktree (`bash rm`, exit 0).
- **Divergences reported by the worker (rule V0b iii) and decided by the regent session (MAESTRO,
  no new gate):** (a) `cabecalho_fila(itens, agora) -> {n, idade_mais_velha}` entered the
  "Nomes fixados" table of `plan.md`; (b) the plan DoD now says **`Ran 24 tests`** — declared
  supersession of `Ran 13` (spec) and `Ran 15` (plan gate); (c) the three old `index.html`
  buttons with `${…}` and no `aria-label` (`#ch-atualiza`, `.ch-cartao`, `.botoes[data-el]`)
  are labeled by Worker04 in slice A — D-072-8 keeps declaring only the JS-rendering limit;
  (d) the dispatch text `task-072-t03b.md` was untracked — committed by the MAESTRO in `dd98ad6`.

### 072-T09 — ADR 0027 + index line + glossary (Worker01 + MAESTRO)

- **Delivered in two parts, closed 24/10** — the split is by design, not accident: worker
  sessions cannot write under `docs/adr/` (permission rule `Edit/Write(docs/adr/**)`), and the
  worker **refused to route around it via shell**, reporting the block instead
  (`[[DONE id=072-T09 outcome=blocked]]` → reopened by the regent session).
- **Glossary** (Worker01, commit `d8c63b6` on `w/worker01`, integrated in `d8aa60f`):
  `docs/governance/glossary.md` with the five "Cycle 072" terms — regency panel, decision
  request, ruling, normalized verdict, regent's gate. Evidence: `grep -c 'Cycle 072'
  docs/governance/glossary.md` → **5**; `scripts/check-language.sh` → **green**.
- **ADR 0027 + ADR index + decision index** (MAESTRO, bypass, commit `fe74587`, from the
  committed draft `adr-0027-rascunho.md`): `docs/adr/0027-registro-da-fila-e-append-only-mecanico.md`
  written, line added to `docs/adr/README.md`, and the `adr-0027` line appended to
  `docs/records/decisoes.jsonl` (**171 decisions** now). Evidence: `scripts/check-adr.sh` →
  **green (24 ADRs)**. The order held: the ADR and its index line entered **before** any code of
  the queue register (W05), as the plan gate requires.
- Environment notes for the record: `python3` on this machine is the Microsoft Store alias (the
  script needs a real one in the PATH), and `scripts/check-adr.sh` here is slow (msys
  subprocesses; a worker-side run was interrupted past 120 s — environment, not a block).

### 072-T03 — pure domain + parser FR5 (Worker03)

- **Delivered** (`[[DONE id=072-T03 outcome=delivered]]`, 24/10): commit `da3f724` on `w/worker03`
  ("ciclo 072: dominio puro da regencia e parser expoe autor_da_peca (FR5; T03)"). Files:
  `painel/regencia/` (`__init__.py` reexporting all public names, `normalizacao.py`, `kanban.py`,
  `fila.py` — pure: no `http.server`, no `sqlite3`, no `chamados`, no file) and one field added to
  `painel/chamados.py` (`confere` exposes `autor_da_peca` in the item, next to `por` — FR5).
  `conferir_chamado.py` untouched.
- **Green captured at `da3f724`** (slice W03 only): `PYTHONUTF8=1 python -m pytest
  painel/tests/test_regencia.py -q` → **15 passed, 9 failed in 5.11s**. The 15 green are exactly
  the W03 slice: F2 (`cartao`/`proposta_transicao` dict `{permitido, falta?}`), F4-fila
  (`sai_da_fila`), F5-ruling (`valida_ruling`), F4-independencia (`independencia`), F5-parser
  (`confere` exposes `autor_da_peca`), F6 (`normaliza` dict), F7 (`idade_do_carimbo`), F8
  (`sem_fonte`), F10 (`aviso_ingestao`), portão-do-regente (`portoes_do_regente`), F20-autor-fora,
  F20-pedido-inexistente, F15 (`ordena_fila`), F23 (`cabecalho_fila`), F11 (`valida_pedido`). The 9
  red stay red on purpose (not this slice): F1, F9, F3, three F14 and dívida5 (W04/W05/W02), plus
  F1-dez-colunas and F7-frentes (routes of W04).
- **Regressions**: `python -m pytest painel/tests/test_chamados.py -q` → **10 passed in 0.17s**;
  old suite `python -m pytest painel/tests -q --ignore=painel/tests/test_regencia.py` →
  **48 passed in 18.52s**; `python painel/chamados.py painel/projetos/exemplo.json` → **exit 0**;
  `scripts/check-boundary.sh` → **exit 0** (`painel/` already owned by the toolkit domain, so
  `painel/regencia/` needs no `boundary.json` change).
- **Divergence reported by the worker (rule V0b iii), for the plan to arbitrate:** the F5 test
  asserts the *pure* refusal reason contains the substring `"destino"`, while `contracts/rotas.md`
  fixes the HTTP 422 body as exactly `"ruling sem destinatario"` (which does not contain
  `"destino"`). The pure `valida_ruling` now returns `"ruling sem destino (destinatario)"` so the
  test passes; Worker05 must emit the wire text of `contracts/rotas.md` at the route (or the plan
  aligns the two wordings). The other FR20/F14 messages already match the contract text exactly
  (`"ruling sem autor humano"`, `"autor não é pessoa do projeto: '…'"`, `"pedido desconhecido: '…'"`).


### 072-T07 — append-only triggers in the base, FR17 (Worker02)

- **Entregue** (`[[DONE id=072-T07 outcome=delivered]]`, 24/10): código no commit **`61e78b5`**,
  worktree `w/worker02` ("ciclo 072: append-only mecânico na base (FR17 …; W02)"). Três arquivos:
  `painel/schema_workflow.sql` (+72), `painel/hooks/workflow_session_start.py` (+62/−1),
  `painel/fila_outbox.py` (+71). **`painel/hooks/workflow_stop.py` não aparece no diff — não foi
  tocado.**
- **Verde — o teste do gatilho** (vermelho capturado em `42e24f4`, pelo T03b):
  `PYTHONUTF8=1 python -m pytest "painel/tests/test_regencia.py::TestDivida5Gatilho" -q` →
  **`1 passed in 0.27s`**. O arquivo de testes **não foi editado** (nada de `# --- FATIA W07 ---`):
  a prova fixada pelo T03b já cobria o desenho, então nenhum teste novo entrou e a contagem
  continua **`Ran 24`**, como a DoD exige. `test_regencia.py` inteiro: **`23 failed, 1 passed`** —
  o único verde é o deste worker; os 23 seguem vermelhos **pela razão certa** (o pacote
  `regencia/`, o adaptador e as rotas ainda não existem — W03/W04/W05 pendentes).
- **Prova de ponta a ponta (o `WHEN` preserva o 070):** schema novo → **8 gatilhos**;
  `CREATE TRIGGER … BEFORE UPDATE OR DELETE` → `OperationalError near "OR"` (o SQLite aceita **um**
  evento por gatilho — medido, `sqlite_version 3.49.1`); o **hook Stop real** fecha o passo
  (`exit=0`, `saida_em` gravado) **apesar** dos gatilhos; o **drain da fila** marca `lida_em`; e
  `passo já fechado`, `UPDATE rodadas`, `UPDATE fila SET payload`, `DELETE FROM fila`,
  `DELETE FROM transicoes` são **recusados** com `RAISE(ABORT, 'append-only: …')`.
- **Regressões**: suíte antiga `python -m pytest painel/tests -q --ignore=painel/tests/test_regencia.py`
  → **`48 passed in 22.08s`**; hooks/workflow (`test_fr13_fr14.py` + `test_workflow_schema.py` +
  `test_workflow_painel.py`) → **`26 passed in 8.25s`**.
- **Declaração 1 — D-072-2 piora (a dívida 2 segue não paga).** Os `CREATE TRIGGER IF NOT EXISTS`
  entram **nas cópias** de `_ensure_schema`: as duas dos hooks e uma **nova** em `fila_outbox.py`
  (o 070 falava em "três cópias"; no código havia duas — a terceira nasce aqui). As cópias agora
  precisam ficar em sincronia; duplicar as sentenças é exatamente o custo declarado em D-072-2.
- **Declaração 2 — a dívida 7 NÃO é paga e o hook não foi retocado.** `painel/hooks/workflow_stop.py`
  fica **byte a byte** como estava. O `WHEN` de `passos` libera só o fechamento (`saida_em IS NULL`
  e só as colunas `saida_em`/`resumo`/`resultado`), que é o que o `Stop` faz — **FR3 do 070
  preservado pelo desenho do gatilho**, não mutilando o hook. A cobrança de verdade do `Stop` fica
  para a rodada 2.
- **Divergência que volta ao plano (V0b) — o `WHEN` que faltava em `fila`.** O ADR 0027 §2/§3 e o
  `plan.md` §3(b) escrevem que `fila` recusa `UPDATE` **e** `DELETE` **sem** `WHEN`. Isso é
  impossível de cumprir junto com o resto: o 070 tem um fechamento legítimo em `fila` — o drain
  marca `lida_em` (`painel/fila_outbox.py:88`, `painel/hooks/workflow_session_start.py:102`) — e a
  própria DoD do plano exige a suíte antiga verde. Sem um `WHEN` em `fila`, três testes hoje verdes
  (`test_enfileirar_drenar`, `test_drenar_destino_especifico`, `test_payload_invalido_nao_envenena_a_fila`)
  quebrariam. Implementei `fila` **espelhando `passos`**: o `WHEN` libera só o fechamento da leitura
  (`lida_em`, NULL → valor) e recusa qualquer outra coluna ou linha já lida — que é **exatamente** o
  que o teste do T03b pede (`UPDATE fila SET payload` e `DELETE` recusados) **e** o que a suíte antiga
  pede. Declarada aqui, não silenciada: o texto do ADR 0027 §2/§3 pede emenda (a decisão de fundo —
  append-only mecânico — não muda).
- **Divergência menor (mesma origem): "quatro TRIGGER" são oito.** O ADR/plano dizem "quatro
  `TRIGGER`"; o SQLite não aceita dois eventos no mesmo gatilho, então o arquivo traz **oito**
  (dois por tabela). O comportamento fixado é idêntico; só a contagem do texto diverge.

### 072-T11 — ajustes de texto pós-T03/T07 (Worker02)

- **Entregue** (`[[DONE id=072-T11 outcome=delivered]]`, 24/10): commit **`573a6f5`** na `w/worker02`
  ("ciclo 072: plano e contratos ajustados após T03/T07"), sobre a base **`6be6525`** (a task T11
  registrada pelo regente). O HEAD estava em `d1cb955`; a worktree fez `git merge --ff-only 6be6525`
  antes de começar (sem push). Dois arquivos, **+2/−2**: `specs/072-painel-de-regencia/contracts/rotas.md`
  e `painel/regencia/fila.py`.
- **O que mudou (a decisão do regente ao aceitar T03/T07):** o corpo **422** do ruling sem
  destinatário passa a `{"erro": "ruling sem destino"}` — o **campo** do esquema continua
  `destinatario` (é nome de campo, não mensagem). `valida_ruling` devolve `"ruling sem destino"`,
  **sem** o híbrido `"(destinatario)"` que o Worker03 usou no T03 para manter a fatia verde
  (divergência registrada em "### 072-T03"). Teste puro e contrato passam a dizer o **mesmo texto** —
  a divergência fecha aqui.
- **Evidência — o grep (2 ocorrências, uma por arquivo):**

  ```
  specs/072-painel-de-regencia/contracts/rotas.md:57:  `{"erro": "ruling sem destino"}` (FR14); `pedido` sem campo obrigatório: `{"erro": "falta
  painel/regencia/fila.py:63:        return "ruling sem destino"
  ```

  (a única ocorrência remanescente do texto antigo é `qa-report.md:90`, na seção **histórica** do
  T03 — não reescrita.)
- **Evidência — verde:** `PYTHONUTF8=1 python -m pytest "painel/tests/test_regencia.py::TestF5Ruling" -q`
  → **`1 passed in 0.26s`** (exit 0). O arquivo de testes **não foi tocado**: o teste já cobrava a
  substring `"destino"`; o híbrido era a única mensagem que não casava com o contrato.
- **Regressão:** suite antiga `python -m pytest painel/tests -q --ignore=painel/tests/test_regencia.py`
  → **`48 passed in 20.67s`** (exit 0).
- **Item 3 — verificado, nada a completar:** a tabela "Nomes fixados" do `plan.md` já traz
  `cabecalho_fila` (linha 61) e a DoD já diz **`Ran 24 tests`** (linha 345), ambos do commit
  **`2d9ef37`**. O diff `6be6525..573a6f5` toca **só** os dois arquivos acima — nenhuma pendência
  de plano restou.

### 072-T04 — kanban routes and screen (Worker04)

- **Entregue** (`[[DONE id=072-T04 outcome=delivered]]`, 24/10): código no commit **`0a9a44a`**,
  worktree `w/worker04` ("ciclo 072: rotas e tela do kanban (T04)"). Três arquivos:
  `painel/server.py` (+174/−6), `painel/index.html` (+98/−1), `painel/tests/test_regencia.py`
  (+4/−3). **Separado da fila de decisões (W05)**: as funções do kanban/transição
  (`v_kanban`, `_cartao_kanban`, `v_transicao`, `_arquivos_do_gate`) e o `vKanban` são novas,
  ao lado das da fila — nada da W05 foi tocado. Sem push/merge/`rm -rf`.
- **O que entrou.** (a) `GET /api/regencia/kanban` — dez colunas G0–G9 (FR1) montadas de
  `chamados.GATES` **reusando** `chamados.em_cache`/`confere` (não há segundo conferidor); o
  cartão traz `veredito` original **ao lado** de `veredito_normalizado` (FR3/FR10 via
  `regencia.normaliza`), `idade`+`selo` (FR23), marcador de independência (FR4), e
  `integrado_criticado` sempre `"não conferido"`; a **faixa `abertura`·`GD`** vem de
  `regencia.faixa_abertura_gd` e **não vira coluna**. (b) `POST /api/regencia/transicao`
  (corpo `{chamado, de, para}`) consome `regencia.proposta_transicao` (pura) — o adaptador
  resolve o arquivo do gate de destino e passa o mapa `arquivos`; **não move nem grava**;
  recusa → **422 com o campo `falta`** (FR9); a recusa fora do localhost (`painel/server.py:675`)
  e o `ValueError`→422 seguem de pé. (c) `/api/meta` passa a expor `cfg["frentes"]` (FR7).
  (d) `painel/index.html`: `vKanban` + botão de navegação; cartões em lista, estado nunca só
  por cor, todo número/selo com `data-fonte` (FR21), `"—"` com `motivo:` (FR22 via
  `regencia.sem_fonte`), botões só-ícone com `aria-label` (FR24) — **inclusive os três antigos**
  (`#ch-atualiza`, `.ch-cartao`, `.botoes[data-el]`), como decidiu a sessão regente (D-072-8).
- **Verde — as seis da fatia** (provas sobre o HTML **servido** pela rota `/`, não grep na fonte;
  vermelho capturado em `42e24f4`, pelo T03b):

  ```
  $ PYTHONUTF8=1 python -m pytest "painel/tests/test_regencia.py::TestF1MetricaComFonte" \
      "painel/tests/test_regencia.py::TestF9BotaoSoIcone" \
      "painel/tests/test_regencia.py::TestF3TransicaoSemArquivo" \
      "painel/tests/test_regencia.py::TestF1DezColunas" \
      "painel/tests/test_regencia.py::TestF7FiltroPorFrente" \
      "painel/tests/test_regencia.py::TestF10IngestaoDefasada" -v
  ... PASSED [16%] TestF1MetricaComFonte
  ... PASSED [33%] TestF9BotaoSoIcone
  ... PASSED [50%] TestF3TransicaoSemArquivo
  ... PASSED [66%] TestF1DezColunas
  ... PASSED [83%] TestF7FiltroPorFrente
  ... PASSED [100%] TestF10IngestaoDefasada
  ============================== 6 passed in 2.98s ==============================
  ```

- **Arquivo inteiro** (`0a9a44a`): `PYTHONUTF8=1 python -m pytest painel/tests/test_regencia.py -q`
  → **`21 passed, 3 failed in 4.68s`**. As 3 vermelhas são **exatamente as três F14**, todas por
  `painel/fila_registro.py` e pela rota `/api/regencia/fila` **não existirem** (`ModuleNotFoundError`,
  `os.path.exists` falso, `404` nos dois POST paralelos) — **é a fatia da W05, fora desta**; a
  fatia W04 não encosta nelas.
- **Prova de ponta a ponta** (script descartável fora da worktree, git real na fixture — não é
  teste do repositório, é a evidência do desenho): kanban com um chamado aprovado em G0→G2 devolve
  as dez colunas `['G0'…'G9']`, o cartão na coluna do **último gate aprovado** (`G2`), com
  `veredito: "APPROVE"` / `veredito_normalizado: "aprovado"`, `frente: "painel"` resolvida de
  `cfg.frentes`, `idade.carimbo`/`selo`, `independencia.texto` e `integrado_criticado`; a faixa
  traz `abertura.estado=ok` e `GD.estado=falta` (motivo "sem entregável"). Na transição:
  `{de:"G1", para:"G2"}` (arquivo do destino presente e válido) → **`200`**
  `{"ok":true,"proposta":{"chamado","de","para","exige":"G2-*.md","dono","promocao"}}`;
  `{de:"G1", para:"G5"}` (sem `G5-*.md`) → **`422`** `{"erro":"falta G5-*.md com cabeçalho válido"}`;
  e a **foto da árvore não mudou** depois dos dois POST (`foto mudou? False`) — FR9 provado.
- **Regressões**: suíte antiga `python -m pytest painel/tests -q --ignore=painel/tests/test_regencia.py`
  → **`48 passed in 15.60s`**; `python -m pytest painel/tests/test_chamados.py -q` →
  **`10 passed in 0.13s`**; `python painel/chamados.py painel/projetos/exemplo.json` → **exit 0**.
- **Divergência declarada (regra V0b iii) — F3 era insatisfazível como escrita.** O `plan.md` marca
  `F3 adapta (W04)`. Além do corpo/caminho já adaptados, faltava isto: o teste fotografa a árvore
  **antes** de `self._sobe()`, mas `_sobe()` cria `<raiz>/painel.db` — então a comparação final
  diferia **sempre**, por artefato da fixture e não da transição (medido: `iguais? False`, a única
  diferença era `painel.db`). Adaptei minimamente: a foto passa a ser tirada **depois** de `_sobe()`,
  preservando o intento (FR9: nenhum arquivo muda na recusa). Nenhum outro teste foi tocado; nenhum
  `# --- FATIA W04 ---` foi necessário (as provas fixadas pelo T03b já cobriam o desenho).
- **Achado da D-072-8, confirmado na prática.** A regra literal do `${…}` no F9 acusou também o
  **chip de frente novo** (`<button class="chip" data-kf="${esc(f)}">`) — resolvido com
  `aria-label` no próprio chip (não é exceção nova, é o mesmo remédio dos três antigos).

### 072-T05 — decision queue: register, routes and screen (Worker05)

- **Entregue** (`[[DONE id=072-T05 outcome=delivered]]`, 24/10): código no commit **`2826278`**,
  worktree `w/worker05` ("ciclo 072: registro, rotas e tela da fila de decisoes (FR11-FR23; T05/W05)").
  Três arquivos: `painel/fila_registro.py` (novo, adaptador JSONL), `painel/server.py` (+154:
  as duas rotas) e `painel/index.html` (+103: `vFila` + botão de navegação).
- **Vermelho herdado do T03b (`42e24f4`)**: as três provas de FR16 falhavam pela razão certa —
  `fila_registro.py` inexistente e POST `/api/regencia/fila` → 404. O pacote puro `regencia/`
  já existia (T03), então os negativos de FR20 e o `valida_ruling` já estavam verdes.
- **Verde — as três provas de FR16, no commit `2826278`**:
  `PYTHONUTF8=1 python -m pytest painel/tests/test_regencia.py -q -k F14 -v` → **`3 passed, 21 deselected`**:
  - `test_f14_registro_append_only_so_cresce` — prefixo de bytes intacto, exatamente 1 linha acrescentada;
  - `test_f14_registro_abre_sempre_em_append` — AST: as aberturas de `fila_registro.py` são `"a"`
    e `"r"` (leitura); **nenhuma** em `w`/`x`/`r+`;
  - `test_f14_registro_concorrente_sem_perda` — dois POST paralelos → `[200, 200]`, duas linhas.
- **Backup datado (ADR 0027 §4)** — demonstração (a suíte não cobre o caminho do backup): duas
  escritas seguidas; a 1ª não acha o registro (nada a copiar) → backup `None`; a 2ª cria o backup
  do dia e **só então** grava:
  ```
  backup 1a escrita: None
  backup 2a escrita: ...\backup\fila-exemplo-2026-10-24.jsonl
  linhas no registro: 2
  linhas no backup: 1
  caminho padrao: painel\dados\fila-x.jsonl
  ```
- **Fatia W05 medida** (arquivo inteiro, `2826278`): `python -m pytest painel/tests/test_regencia.py -q`
  → **`20 passed, 4 failed`**. Os 4 vermelhos **não são desta fatia** (W04): F9 (três botões antigos
  `#ch-atualiza`, `.ch-cartao`, `.botoes[data-el]` com `${…}` e sem `aria-label` — D-072-8 / fatia A),
  F3 (`/api/regencia/transicao`), F1-dez-colunas (`/api/regencia/kanban`) e F7-frentes (`frentes`
  em `/api/meta`). **F1 (`.metrica` com `data-fonte`) ficou verde** com o `vFila`.
- **Regressões**: suíte antiga `python -m pytest painel/tests -q --ignore=painel/tests/test_regencia.py`
  → **`48 passed in 13.71s`**; `python -m pytest painel/tests/test_chamados.py -q` → **`10 passed`**;
  `python painel/chamados.py painel/projetos/exemplo.json` → **exit 0**.
- **Divergência (V0b iii) que volta ao plano.** O `POST` **passa adiante** o texto que a função pura
  devolveu — não hardcodei o wire de `contracts/rotas.md` na rota. Hoje `valida_ruling` devolve
  `"ruling sem destino (destinatario)"`, então o 422 da rota diz isso, não `"ruling sem destinatario"`.
  A T11 (W02) alinha a função pura e o contrato a `"ruling sem destino"`; quando entrar, a rota passa
  a dizer isso **sem tocar em `server.py`** — que é o desenho (a rota não duplica a string).
- **Limites respeitados**: a fila de teste vive no diretório temporário da fixture (`fila_decisoes`),
  nada em `painel/dados/`; sem dado real da Hindiana; sem push/merge.

### 072-T08 — living journey (Worker01)

- **Entregue** (`[[DONE id=072-T08 outcome=delivered]]`, 24/10): `docs/journeys/072-painel-de-regencia.md`
  (a jornada do regente, cobrindo **as duas telas** — Kanban e Fila —, a partir do §3 do
  `specs/066-painel-de-regencia/ux-design.md`), o script versionado
  `docs/journeys/scripts/captura-072.sh` e duas capturas **do build real**. Base desta seção: `2d4a8c5`.
- **O ambiente renderizou** — o plano B da D-072-7 **não** foi necessário. Script sobe o painel de
  verdade (`painel/server.py painel/projetos/exemplo.json`, porta 8791, derrubado no fim por `trap`)
  e fotografa o DOM com Playwright + Edge do sistema (`PW_CHANNEL=msedge`, headless), 1440×900.
  Saída da execução que gerou as imagens:
  ```
  == subindo o painel real em http://127.0.0.1:8791 (fixture exemplo) ==
  == esperando a derivação aquecer (até 90s) ==
    derivação estabilizada com 1 chamado(s) em 2.1s
  == capturando as duas telas com o navegador (msedge) ==
  ok: ...\docs\journeys\img\072-01-kanban.png  (Painel de regência)
  ok: ...\docs\journeys\img\072-02-fila.png  (Fila de decisões)
  == pronto: capturas em ...\docs\journeys\img ==
  ```
- **A captura é real, não uma foto de "vazio" (verificação por medição, não por leitura de olho).**
  A derivação é preguiçosa/assíncrona: sem aquecer, a 1ª consulta devolve lista vazia. Prova do DOM
  aquecido (subiu o servidor, aqueceu e leu `#main` no navegador):
  ```
  API kanban total: 1
  G0 · Reprodução 1
  000-exemplo
  dono: —   sessão: —   INVÁLIDO   original: —   —
  SELO: REGISTRO
  — (MOTIVO: CABEÇALHO DO GATE SEM AUTOR_DA_PECA (FR5))
  integrado = criticado: não conferido
  contem 000-exemplo: True
  ```
  E a Fila declara o vazio: `fila vazia — nenhuma decisão registrada`, contador `0`.
- **Achado R1 (novo) — derivação preguiçosa sem estado "carregando".** O §3 manda cara própria para
  o estado **carregando**; hoje o servidor frio mostra um "vazio" falso. Severidade **Média**,
  registrado para a **rodada 2** na heurística da jornada. O script contorna aquecendo antes de
  fotografar (regeneração é o teste do próprio script — skill `living-journey`); a tela ainda não.
- **Jornada viva ligada (F11)**: documento + capturas por script versionado + heurística datada em
  **2026-10-24** (≥ data das capturas), com severidade e destino por achado. R2–R5 conformes
  (vazio declarado, "—" com motivo, não marca "conferido", veredito original ao lado do normalizado);
  R6 (ruling no build real) registrado — o caminho é provado por contrato (T03b/T05), não pela tela.
- **Artefato vivo atualizado no mesmo PR**: `painel/projetos/exemplo.json` — o glob
  `documentos.jornadas` passa a incluir `docs/journeys/*.md`.
- **Limites respeitados**: só a worktree; sem push/merge/rm -rf; sem `.env`/`settings.local.json`;
  fixture sem dado real; servidor em porta alta, derrubado ao fim.
- **Nota de ambiente conhecida**: `scripts/check-links.sh` chama `python3`, que nesta máquina é o
  alias da MS Store (não executa). Rodei o equivalente com o interpretador real (`python` 3.12.10) e
  declarei; nenhum link relativo desta entrega ficou sem resolver.

### 072-T10 — living artifacts of the closing (Worker01)

- **Entregue** (`[[DONE id=072-T10 outcome=delivered]]`, 24/10): artefatos vivos no commit
  **`f9f0f0d`** na `w/worker01` ("ciclo 072: artefatos vivos do fechamento (CHANGELOG e roadmap;
  T10)"); a evidência deste arquivo entra no commit seguinte. Base: o `git merge --ff-only 460dd8c`
  entrou limpo a partir de `6be6525` (sem push).
- **CHANGELOG.md** — entrada do ciclo 072 em `[Unreleased]`, **uma seção por tipo**: `### Adicionado`
  (o painel de regência rodada 1 — kanban por gate, fila de decisões com registro JSONL append-only
  e backup datado, parser expondo `autor_da_peca`, testes de contrato da regência) e `### Modificado`
  (os oito gatilhos append-only do schema do workflow — dívida 5 do 070 paga). Evidência:
  `grep -c 'ciclo 072' CHANGELOG.md` → **2** (≥ 1).
- **docs/roadmap.md** — linha **F35 — painel de regência, rodada 1** na tabela de fases, com a
  **rodada 2 declarada infra** (dívidas 3, 6, 7 e 10 do 070 + D-072-1..8); o cabeçalho "Atualizado"
  passou de ciclo 065 a **ciclo 072**. Evidência: `grep -c '072' docs/roadmap.md` → **4** (≥ 1).
- **Artefatos condicionais do plano, no mesmo PR** — todos presentes em
  `specs/072-painel-de-regencia/`: `plan.md`, `tasks.md`, `data-model.md`, `contracts/`
  (`esquemas.md`, `rotas.md`), `ux-design.md` (**apontador** para `specs/066-…/ux-design.md` §2.1/§2.3,
  não reescrita), `adr-0027-rascunho.md`, `qa-report.md`. Ausentes: **nenhum** dos listados (a pasta
  traz ainda `spec.md` e os despachos `task-072-t03b.md`/`task-072-t09.md`).
- **Evidência — `ls -1 specs/072-painel-de-regencia/`:**

  ```
  adr-0027-rascunho.md
  contracts
  data-model.md
  plan.md
  qa-report.md
  spec.md
  task-072-t03b.md
  task-072-t09.md
  tasks.md
  ux-design.md
  ```

  (`contracts/` → `esquemas.md`, `rotas.md`.)

## Fitness functions (DoD) — filled by Worker06 with real output

| Check | Expected | Result |
|---|---|---|
| `python -m unittest discover -s painel/tests -p test_regencia.py` | `Ran 15 tests`, `OK`, exit 0 (supersession of `Ran 13` declared in `plan.md`) | — |
| 48 tests of the old suite (`--ignore=test_regencia.py`) | green, untouched | — |
| `python painel/chamados.py painel/projetos/exemplo.json` | exit 0 (FR5 only adds a field) | — |
| `python -m unittest discover -s painel/tests -p 'test_*.py'` | green (regression 068/069/070) | — |
| `ls specs/070-conferidor-ordem-veredito/` | 10 files (immutable folder) | — |
| `ls painel/projetos/*hindiana*` | empty (fixture rule) | — |
| `grep -rn '\.env\|settings.local.json' painel/` | no **read** path | — |
| `ls docs/journeys/072-*.md` / `grep -c 'F11'` | exists / ≥ 1 | — |
| `scripts/check-language.sh` / `check-boundary.sh` / `check-links.sh` | green | — |
| `scripts/check-conformance.sh 072` | green after plan, tasks and this file carry the evidence | — |

## Closing tail — the evidence

> The four steps below all **apply** to this cycle (none is n/a). Their evidence bullets are
> appended by Worker06 as each step actually runs; the boxes in `tasks.md` are ticked only
> while the evidence is being written. Until then this section intentionally carries no
> evidence bullets — an open cycle is red by design, and a placeholder that passes the gate
> would be the exact defect the gate exists to catch.

## Requirement coverage

- To be written by the independent review: the 25 FR of `spec.md` (revisão T01b) against the
  integrated diff, plus the "Nomes fixados" table of `plan.md` and the anti-rules 1–8 of
  `specs/066-painel-de-regencia/ux-design.md` §4.

## Findings inside the cycle

- **SendMessage to workers keeps falling (classifier unavailable).** The T03b dispatch went
  through on the second try; the T09 dispatch fell twice and was committed as
  `task-072-t09.md` (`e276f83`), which the MAESTRO relayed — the same fallback that saved T03b
  in the previous session. Rule confirmed: after two failures, the dispatch text is committed
  to `specs/072-painel-de-regencia/task-<id>.md`.
- **F9 measured consequence of the literal `${…}` rule (D-072-8).** The reconciled F9 does not
  count a template literal as button text, so three **old** `index.html` buttons
  (`#ch-atualiza`, `.ch-cartao`, `.botoes[data-el]`) fail it even though they render text at
  runtime. Decided by the regent session: Worker04 labels them with `aria-label` in slice A;
  the limitation itself stays declared in D-072-8, unchanged.
