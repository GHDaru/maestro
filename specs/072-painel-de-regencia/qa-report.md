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

- **Entregue** (`[[DONE id=072-T08 outcome=delivered]]`, 24/10): `docs/jornada/072-painel-de-regencia.md`
  (a jornada do regente, cobrindo **as duas telas** — Kanban e Fila —, a partir do §3 do
  `specs/066-painel-de-regencia/ux-design.md`), o script versionado
  `docs/jornada/scripts/captura-072.sh` e duas capturas **do build real**. Base desta seção: `2d4a8c5`.
  *(Caminhos em `docs/jornada/` — singular — desde a correção R2/T13; antes, `docs/journeys/`.)*
- **O ambiente renderizou** — o plano B da D-072-7 **não** foi necessário. Script sobe o painel de
  verdade (`painel/server.py painel/projetos/exemplo.json`, porta 8791, derrubado no fim por `trap`)
  e fotografa o DOM com Playwright + Edge do sistema (`PW_CHANNEL=msedge`, headless), 1440×900.
  Saída da execução que gerou as imagens:
  ```
  == subindo o painel real em http://127.0.0.1:8791 (fixture exemplo) ==
  == esperando a derivação aquecer (até 90s) ==
    derivação estabilizada com 1 chamado(s) em 2.1s
  == capturando as duas telas com o navegador (msedge) ==
  ok: ...\docs\jornada\img\072-01-kanban.png  (Painel de regência)
  ok: ...\docs\jornada\img\072-02-fila.png  (Fila de decisões)
  == pronto: capturas em ...\docs\jornada\img ==
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
- **Artefato vivo do mesmo PR**: `painel/projetos/exemplo.json` — o glob `documentos.jornadas`.
  Depois da correção R2/T13 ele aponta só para **`docs/jornada/*.md`** (a pasta declarada em
  `boundary.json`), como estava antes do T08.
- **Limites respeitados**: só a worktree; sem push/merge/rm -rf; sem `.env`/`settings.local.json`;
  fixture sem dado real; servidor em porta alta, derrubado ao fim.
- **Nota de ambiente conhecida (corrigida no T13)**: `scripts/check-links.sh` é **bash puro** — não
  chama `python3` (a nota antiga era imprecisa). O que trava aqui é o emulador de **fork do msys**
  com um `sed`/`grep` por arquivo sobre as ROOTS (agravado por `.claude/worktrees`). Rodei o bloco
  **equivalente** num processo só e declarei a poda; nenhum link relativo desta entrega ficou sem
  resolver. Detalhe e saída: seção **"### 072-T13 — R2 corrigida"**.

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

### 072-T14 — contagem corrigida (Worker02)

- **Entregue** (`[[DONE id=072-T14 outcome=delivered]]`, 24/10): commit **`f0c2b39`** na `w/worker02`
  ("ciclo 072: contagem de FR corrigida (27, nao 25; T14)"), sobre a base **`ee9b3a9`** (a rodada de
  correção registrada pelo regente; `git merge --ff-only ee9b3a9`, de `2d4a8c5` para cá, sem push).
  O `tasks.md` **não foi tocado** (a correção do regente em `ee9b3a9` é dele) e a seção "### FR por
  FR"/"## Requirement coverage" do W06 **não foi reescrita** — corrijo só as linhas de **contagem**.
- **Onde o número vivia, e o que ficou:** `spec.md` enumera **27 FR (FR1–FR27)**; a moldura dizia
  "25 FR" em **quatro linhas vivas** — `plan.md` **duas** (l. 4, o cabeçalho da spec; e l. 32, a tabela
  do *Constitution Check*) e `qa-report.md` **duas** (l. 418 e l. 420, ambas na bala do `TAIL:review`:
  a contagem e a referência à tabela de cobertura). As quatro passam a **27 FR (FR1–FR27)**.
  **Desvio do "uma linha cada" do `tasks.md` §T14, declarado (regra V0b):** o `plan.md` tinha **duas**
  menções, não uma — deixar a segunda seria conservar o erro de contagem no documento vivo; e o
  `qa-report.md` pedia as duas linhas da mesma bala (corrigir a primeira e deixar "25-FR coverage
  table" na segunda produziria um par incoerente). Portanto: **4 linhas, não 2**.
- **Evidência — greps (saída real, medida imediatamente antes deste append):**

  ```
  $ grep -rn '25 FR' specs/072-painel-de-regencia/
  specs/072-painel-de-regencia/qa-report.md:447:> **Nota de contagem**: a moldura do ciclo (tasks.md/T06) fala em "25 FR"; `spec.md` enumera **27**
  specs/072-painel-de-regencia/qa-report.md:615:- **Contagem de FR divergente (menor).** A moldura do ciclo (tasks.md/T06) diz "25 FR"; `spec.md`
  specs/072-painel-de-regencia/tasks.md:9:> `spec.md` — **revisão T01b**, 25 FR. Os **13 testes já existem** (`c1eb802`,
  specs/072-painel-de-regencia/tasks.md:225:      plano, os 25 FR e a tabela **"Nomes fixados"**: veredito no `qa-report.md`. Procurar os
  specs/072-painel-de-regencia/tasks.md:296:  (Theorem 2). Evidence: the verdict, in `qa-report.md`. Aqui: revisar os 25 FR contra o diff

  $ grep -c '27 FR' specs/072-painel-de-regencia/plan.md specs/072-painel-de-regencia/qa-report.md
  specs/072-painel-de-regencia/plan.md:2
  specs/072-painel-de-regencia/qa-report.md:2

  $ grep -n '27 FR' specs/072-painel-de-regencia/plan.md specs/072-painel-de-regencia/qa-report.md
  specs/072-painel-de-regencia/plan.md:4:  incorporadas; **27 FR** (FR1–FR27) em EARS; 13 testes nomeados; …
  specs/072-painel-de-regencia/plan.md:32:| I. Spec-driven | ✅ A spec revisada (**27 FR** — FR1–FR27) precede o código; …
  specs/072-painel-de-regencia/qa-report.md:418:  integrated diff against `plan.md`, the **27 FR** (FR1–FR27) of `spec.md`, …
  specs/072-painel-de-regencia/qa-report.md:453:> restante das 27 FR está implementado e provado.
  ```

  **As 5 ocorrências de "25 FR" que restam — nenhuma é contagem viva, todas declaradas:**
  `tasks.md` **3** (l. 9, 225, 296 — o regente mandou "não a toque"); `qa-report.md` **2** (l. 447 e
  l. 615 — **citações históricas** da divergência *medida* pelo W06 na revisão em contexto fresco:
  "a moldura do ciclo … fala em '25 FR'"; reescrevê-las falsificaria o registro do que foi achado).
  Zero linhas de **contagem** com o número antigo.
- **Nota de honestidade sobre o próprio grep (auto-referência):** esta seção **cita** o token ao colar
  a saída, então um `grep '25 FR'` rodado **depois** dela soma as ocorrências que estão **aqui dentro**
  (o mesmo vale para o `grep -c '27 FR'`, que sobe acima de 2 em `qa-report.md`). Por isso as saídas
  acima são as medidas **antes do append** — é o número que vale para o critério do T14, e os 2 em
  cada arquivo (em vez de 1) são exatamente as linhas extras que declarei no desvio.
- **Sem regressão e sem teste tocado:** correção de texto em `specs/`; o diff `ee9b3a9..f0c2b39` traz
  **só** `plan.md` e `qa-report.md` (4 inserções / 4 remoções) — nenhum arquivo de `painel/` foi
  alterado (nenhuma linha de código ou de teste).

## Fitness functions (DoD) — filled by Worker06 with real output

> Ambiente: Windows, `PYTHONUTF8=1`, `python` 3.12.10 (o `python3` desta máquina é o alias da MS Store
> e **não** executa — por isso os dois gates de `bash` que chamam `python3` foram rodados como
> **equivalentes Python**, e o desvio fica declarado, não escondido: §"Caveats de ambiente").

| Check | Expected | Result |
|---|---|---|
| `python -m unittest discover -s painel/tests -p test_regencia.py` | `Ran 24 tests`, `OK`, exit 0 (supersessão de `Ran 13` e `Ran 15` declarada em `plan.md § Verification`) | **`Ran 24 tests in 3.874s` · `OK`** (exit 0) |
| 48 tests of the old suite (`--ignore=test_regencia.py`) | green, untouched | **`48 passed in 13.49s`** |
| `python painel/chamados.py painel/projetos/exemplo.json` | exit 0 (FR5 only adds a field) | **`exit=0`** |
| `python -m unittest discover -s painel/tests -p 'test_*.py'` | green (regression 068/069/070) | **`Ran 54 tests in 13.180s` · `OK`** (24 regência + 30 antigos; a suíte antiga isolada por pytest dá 48 — a diferença é **como cada runner coleta**, não cobertura nova; declarado para não haver divergência silenciosa) |
| `ls specs/070-conferidor-ordem-veredito/` | 10 files (immutable folder) | **`10`** |
| `ls painel/projetos/*hindiana*` | empty (fixture rule) | **`0`** |
| `grep -rn '\.env\|settings.local.json' painel/` | no **read** path | **nenhum caminho de leitura** — os matches são docs (`arquitetura.html`, `docs/*.md`), o **guard** `PROIBIDOS` de `ingest.py:25` (regex que *recusa*), os `os.environ.get` dos hooks (variável de ambiente, não arquivo) e testes, incluindo o **negativo** `test_ler_recusa_caminho_proibido` (espera `PermissionError`) e `test_painel.py:67` (`assertFalse` de que nada abriu) |
| `ls docs/journeys/072-*.md` / `grep -c 'F11'` | exists / ≥ 1 | **`1`** arquivo / **`1`** ocorrência |
| `scripts/check-language.sh` | green | **green** (exit 0) |
| `scripts/check-boundary.sh` | green | **✗ FAIL** — 4 arquivos órfãos: `docs/journeys/072-painel-de-regencia.md`, `docs/journeys/img/072-01-kanban.png`, `docs/journeys/img/072-02-fila.png`, `docs/journeys/scripts/captura-072.sh`. `boundary.json` declara `docs/jornada/` (**singular**); a T08 criou `docs/journeys/` (**plural**, o caminho da skill). Achado da revisão — anti-padrão 23 |
| `scripts/check-links.sh` | green | **ok: 341 links relativos, todos resolvem** |
| `scripts/check-conformance.sh 072` | green after plan, tasks and this file carry the evidence | **green (exit 0)** após esta evidência — as **quatro** evidências da cauda são reconhecidas (`✓ TAIL:review/security/gate/mutation evidence`). O modo `--ticked-only` (que bloqueia) roda a bateria inteira e é **lento** nesta máquina; não concluiu em 3 min |

### Caveats de ambiente (declarados, não escondidos)

- **`check-boundary.sh` e `check-links.sh` chamam `python3`**, que nesta máquina é o alias da
  Microsoft Store (`Python was not found`, exit 49); `bash`+msys também é lento. Rodei os **dois como
  equivalente Python** (mesma lógica: `git ls-files` + `owner()` do `boundary.json` para a fronteira;
  varredura dos `.md` das `ROOTS` com os *inline code spans* removidos para os links). **O resultado da
  fronteira é FAIL (real)** e o de links é OK — nenhum dos dois foi "passado por cima".
- **`python -m unittest discover -p 'test_*.py'` dá 54 e o pytest da suíte antiga dá 48**: não é
  regressão nem cobertura nova — é o `unittest` coletando as classes das duas suítes no mesmo
  processo. Os 48 do pytest (com `--ignore=test_regencia.py`) e os 24 de regência fecham a conta.

### Dívidas declaradas ao fechamento (não pagas, não silenciadas)

- **D-072-1** — a fila é **local** (`painel/dados/`, gitignored): não versionada, não viaja no clone
  (mitigada pelo backup datado). · **D-072-2** — a dívida 2 do 070 **piora**: os `CREATE TRIGGER` entram
  nas cópias de `_ensure_schema`. · **D-072-3** — endurecimento de CSRF/autoria nas rotas POST novas
  (herdada). · **D-072-4** — `data()` de `painel/chamados.py` sem `try/except` (herdada). · **D-072-5** —
  filtro do `custo.py` (substring → igualdade) (herdada). · **D-072-6** — `TAIL:gate` como item da fila
  por leitura simples do `tasks.md`. · **D-072-7** — captura da jornada (aqui **não** foi preciso: o
  ambiente renderizou, ver T08). · **D-072-8** — a renderização por JavaScript **não** é verificada nesta
  rodada (F1/F9 provam o HTML servido). **Nenhuma delas é vendida como paga.**

## Closing tail — the evidence

- **TAIL:review** — independent review in fresh context (Worker06, who did not execute), of the
  integrated diff against `plan.md`, the **27 FR** (FR1–FR27) of `spec.md`, the "Nomes fixados" table and the
  anti-rules 1–8 of `specs/066-painel-de-regencia/ux-design.md` §4. **Verdict: approved with two
  blocking reservations** — the 27-FR coverage table below. Two defects found, both **anti-pattern 23**
  ("a new door, and the old guard never told"): (1) `_pasta_do_chamado` is defined **twice** in
  `painel/server.py` (W04 line 400, W05 line 582) and the later **shadows** the earlier, so the
  transition route (`v_transicao`) **always crashes and never implements FR9**; (2) `docs/journeys/`
  (plural) is undeclared in `boundary.json`, leaving `check-boundary.sh` red. Coverage of every FR and
  anti-rule is in "## Requirement coverage".
- **TAIL:security** — security pass, **medium class** (two new POST routes, a DB trigger that now
  refuses writes on the inherited base, local file read/write including the new `painel/dados/backup/`).
  Verdict below in "## Security pass". Summary: no POST accepts outside `127.0.0.1`/`::1` (guard at
  `painel/server.py:819`, covering **all** POSTs including the two new ones); the ruling records `autor`
  **from the form** (`acrescenta_na_fila`) and refuses outside `cfg["regencia"]["pessoas"]`
  (`"config sem regencia.pessoas"` when the key is absent); `grep -rn '\.env\|settings.local.json' painel/`
  finds **no read path**; inherited debts **D-072-3 / D-072-4 / D-072-5 declared, not silenced**.
- **TAIL:mutation** — the five gates of this cycle were **broken on purpose (the CONDITION, not the
  name)** and seen refusing, with the failing test names pasted: FR10, FR12, FR9, FR16, FR17. Full
  transcript below in "## Mutation (TAIL:mutation)". **One mutation (FR9) did *not* produce a failure —
  and that silence is the finding**: the route's fitness function F3 is vacuous (it passes on a crash).
- **TAIL:gate** — **DoD executable is filled above** with real output; **what awaits the regent**: the
  guardian verdict and the human/regent merge gate (delegated this round — `decisao-072-gates-delegados`,
  ADR 0026). This round **does not arrive green**: two gates are red by fact, not by omission — the
  boundary gate (`docs/journeys/` orphan) and the FR9 route defect. The box in `tasks.md` stays
  **unticked** (the gate is the regent's); a green tick here would be a claim without a witness.

## Requirement coverage

> Revisão **em contexto fresco** (Worker06, que não executou — Teorema 2), do diff integrado contra o
> plano, os FR de `spec.md`, a tabela "Nomes fixados" e as anti-regras §4 do `ux-design.md` do 066.
> **Nota de contagem**: a moldura do ciclo (tasks.md/T06) fala em "25 FR"; `spec.md` enumera **27**
> (FR1–FR27). Nenhuma ficou sem revisão por causa do número — a divergência fica declarada.
>
> **Veredito: APROVADO COM DUAS RESSALVAS QUE BLOQUEIAM O GATE** — (R1) a rota de FR9 **não implementa
> a regra** (o 422 vem de um crash, não do domínio; o 200 legítimo nunca acontece) e sua *fitness
> function* F3 é **vacua**; (R2) `check-boundary.sh` está **vermelho** (`docs/journeys/` órfão). O
> restante das 27 FR está implementado e provado.

### FR por FR

| FR | Veredito | Onde / prova |
|---|---|---|
| FR1 (dez colunas G0–G9) | ✅ | `v_kanban` monta de `chamados.GATES`; `abertura`/`GD` **não** viram coluna (§5). `TestF1DezColunas` verde |
| FR2 (cartão no último gate aprovado) | ✅ | `coluna_do_cartao` = último `estado=="ok"` entre G0–G9; `cartao`. `TestF2CartaoEmGn` verde |
| FR3 (anatomia do cartão + fonte de cada campo) | ✅ | `_cartao_kanban` (id/frente/dono papel+sessão/veredito+original/idade/selo). FR21 coberto por F1 |
| FR4 (independência provada) | ✅ | `independencia(autor_da_peca, por)`. `TestF4Independencia` verde (mesmo autor → vermelho) |
| FR5 (parser expõe `autor_da_peca`) | ✅ | `painel/chamados.py:145` (`confere` devolve `autor_da_peca` no item, ao lado de `por`); `conferir_chamado.py` intacto. `TestF5ParserAutorDaPeca` verde |
| FR6 ("integrado = criticado" → "não conferido") | ✅ | fixo em `_cartao_kanban` (`"não conferido"`), nunca verde. Anti-regra 8 |
| FR7 (filtro por frente) | ✅ | `cfg["frentes"]` em `/api/meta` (`v_meta`). `TestF7FiltroPorFrente` verde |
| FR8 (arrasto é proposta, não promoção) | ✅ | `proposta_transicao` (pura, `{permitido, falta?}`); a rota **não** move/grava. `TestF2CartaoEmGn` verde |
| **FR9 (transição sem evidência → 422, não grava)** | ❌ **NÃO CUMPRIDO na rota** | Ver **achado R1**. O caminho de domínio (`proposta_transicao`) está certo e é provado por F2, mas `v_transicao` **nunca o alcança**: `_arquivos_do_gate` estoura (`_pasta_do_chamado` colidido) e o `except ValueError` do `do_POST` devolve um **422 de crash**. O 200 legítimo nunca ocorre, e F3 passa por acidente |
| FR10 (normalização tabela-dirigida) | ✅ | `normaliza` → `dict {canonico, original, motivo?}`; tabela fixa; fora da tabela → `inválido` com original. `TestF6Normalizacao` verde; **mutação FR10 confirmada** |
| FR11 (anatomia do pedido) | ✅ | `valida_pedido` (7 campos de texto + `opcoes` + `destrava`). `TestF11AnatomiaDoPedido` verde |
| FR12 (pedido sem ruling fica na fila) | ✅ | `sai_da_fila` só com ruling que fecha. `TestF4Fila` verde; **mutação FR12 confirmada** |
| FR13 (anatomia do ruling / "encaminhado a" / "devolver a quem pediu") | ⚠️ PARCIAL | `valida_ruling` cobre autor+destino+delegação (`registrado_por`); as ações de tela ("encaminhado a …", "devolver") **não têm prova de tela** — é renderização por JS, **D-072-8**. Declarado, não vendido como coberto |
| FR14 (ruling sem autor/destino recusado; delegação) | ✅ | `valida_ruling`. `TestF5Ruling` verde (`registrado_por`/`delegacao` registram quem lançou sem trocar a autoria) |
| FR15 (ordem da fila: prazo × bloqueio) | ✅ | `ordena_fila` (prazo asc, `-n_destravados`). `TestF15OrdemDaFila` verde |
| FR16 (append-only **mecânico**) | ✅ | `fila_registro.acrescenta` sempre `"a"`, sob `_LOCK`; prefixo de bytes intacto. `TestF14AppendOnly`/`AbreEmAppend`/`Concorrente` verdes; **mutação FR16 confirmada (3 falhas)** |
| FR17 (append-only por **gatilho**) | ✅ | 8 `TRIGGER` no `schema_workflow.sql`; `passos`/`fila` com `WHEN`. `TestDivida5Gatilho` verde; **mutação FR17 confirmada** (o `WHEN` é *load-bearing*) |
| FR18 (o painel não escolhe; `autor` do formulário) | ✅ | `acrescenta_na_fila` lê `autor` do corpo, **não** infere do agente. Ver § Security |
| FR19 (resposta nunca pré-marcada) | ⚠️ PARCIAL | tela `vFila` sem pré-seleção — **não há prova automatizada** (JS; **D-072-8**). Declarado |
| FR20 (portão do regente vira item da fila) | ✅ | `portoes_do_regente` + `_item_tail` (G7/G8 + `TAIL:gate`), id derivado `chamado+gate`. `TestPortaoRegente` + os **2 negativos** (`TestF20Negativos`) verdes |
| FR21 (todo número tem `data-fonte`) | ✅ | **sobre o HTML renderizado** (não `grep`): `TestF1MetricaComFonte` verde |
| FR22 ("—" sempre com motivo) | ✅ | `sem_fonte` (nunca "0", nunca "n/a"). `TestF8Traco` verde |
| FR23 (idade do relógio + carimbo + contador) | ✅ | `idade_do_carimbo` (`{texto, carimbo, selo}`) + `cabecalho_fila` (`{n, idade_mais_velha}`). `TestF7Idade`/`TestF23CabecalhoDaFila` verdes |
| FR24 (botão só-ícone com `aria-label`) | ✅ | **sobre o HTML renderizado**: `TestF9BotaoSoIcone` verde (inclui os três botões antigos rotulados pelo W04) |
| FR25 (ingestão defasada anunciada) | ✅ | `aviso_ingestao` (> 1 h → "defasado"). `TestF10IngestaoDefasada` verde |
| FR26 (jornada viva) | ✅ | `docs/journeys/072-painel-de-regencia.md` + script versionado + capturas do build real (T08); `grep -c F11` = 1 |
| FR27 (nunca abre `.env`/`settings.local.json`, não guarda host/token) | ✅ | `grep` sem caminho de leitura; guard `PROIBIDOS` do `ingest.py`; negativo `test_ler_recusa_caminho_proibido` verde. Ver § Security |

### Tabela "Nomes fixados" — arbitragem cumprida

Todos os nomes fixados existem com a assinatura fixada e são reexportados por
`painel/regencia/__init__.py` (os testes resolvem **pelo pacote** — `_fn`). As duas obrigações
mecânicas: (1) `__init__.py` reexporta o público ✅; (2) os testes foram **apensados por fatia**, e
**só** os métodos marcados "adapta" na fatia de cada Worker foram tocados — `normaliza`→dict (F6),
`proposta_transicao`→dict (F2) no W03; `idade`→`idade_do_carimbo` (F7) no W03; **F3 adapta** (corpo e
caminho) no W04; **F14 adapta** (`import fila_registro`) no W05 ✅. `cabecalho_fila` entrou na tabela
após o T03b (`42e24f4`) ✅. Divergência **fechada** pelo T11: `valida_ruling` e `contracts/rotas.md`
dizem o **mesmo** texto `"ruling sem destino"` ✅.

### Anti-regras §4 do `ux-design.md` (o que a UI **nunca** faz)

1. **Não promove** — ✅ (a regra; `proposta_transicao` pura, sem escrita). *Mas* a **rota** que a serve está quebrada (R1).
2. **Não decide pelo humano** — ✅ (`autor` do formulário, FR18; opções sem pré-seleção, FR19 — FR19 sem prova de tela).
3. **Não inventa número** — ✅ (`sem_fonte`, FR22).
4. **Não esconde pergunta** — ✅ (`sai_da_fila` só com ruling, FR12).
5. **Não digita hora** — ✅ (`idade_do_carimbo` do relógio/registro, FR23).
6. **Não unifica apagando** — ✅ (veredito **original** ao lado do **normalizado**, FR3/FR10).
7. **Não escreve em arquivo do projeto / não lê `.env` / sem host-token** — ✅ (fila em `painel/dados/`; grep sem leitura; FR27).
8. **Não marca "conferido"** — ✅ (`integrado_criticado: "não conferido"`, FR6).

### Achados da revisão (anti-padrões)

- **R1 — anti-padrão 23 (e 13): `_pasta_do_chamado` colide e mata FR9; F3 é vacua.** `painel/server.py`
  define `_pasta_do_chamado` **duas vezes**: linha **400** (commit `0a9a44a`, W04 — devolve `(pasta,
  rel)`) e linha **582** (commit `2826278`, W05 — devolve só `pasta`). A definição **posterior vence**.
  `_arquivos_do_gate` (`:430`) faz `pasta, rel = _pasta_do_chamado(...)` → desempacota a **string** →
  `ValueError: too many values to unpack (expected 2)`; `do_POST` captura com `except ValueError` e
  responde **422** com essa mensagem. Medido: `POST …/transicao` com arquivo **válido** → **422
  `{"erro": "too many values to unpack (expected 2)"}`** (deveria ser 200). Logo: a rota **nunca**
  entrega o 422 de domínio nem o 200 legítimo; F3 passa porque só checa `code==422` e "contém
  'erro'" — o crash satisfaz os dois (**anti-padrão 13**). A colisão nasceu na **integração** (W04 e
  W05 correram em worktrees separadas; cada prova de ponta a ponta era verdadeira *antes* do merge).
- **R2 — anti-padrão 23: `boundary.json` não declara `docs/journeys/`.** A skill `living-journey`
  fixa o plural (`skills/living-journey/SKILL.md:30`); `boundary.json` declara `docs/jornada/`
  (singular, o trilho do livro). A T08 criou `docs/journeys/` e o gate de fronteira ficou **vermelho**
  (4 órfãos). Correção de uma linha em `boundary.json` — **mas não é minha** (só posso tocar
  `qa-report.md`/`tasks.md` nesta entrega).

## Security pass (TAIL:security — classe média)

Passo proporcional à classe (duas rotas POST novas, gatilho que passa a recusar escrita na base
herdada, leitura/escrita de arquivo local, **agora também o backup**). Veredito: **sem bloqueio de
segurança novo**; as dívidas herdadas ficam **declaradas**.

| Item | Veredito | Evidência |
|---|---|---|
| Nenhuma rota POST aceita fora de `127.0.0.1`/`::1` | ✅ | guard **único** no topo do `do_POST` (`painel/server.py:819`): `if self.client_address[0] not in ("127.0.0.1", "::1"): return … 403` — cobre **todas** as rotas, incl. `/api/regencia/transicao` e `/api/regencia/fila` |
| O *ruling* grava `autor` **do formulário** (não inferido do agente) | ✅ | `acrescenta_na_fila` monta `linha = {**corpo, …}` — o `autor` vem do corpo da requisição (FR18) |
| Recusa fora de `regencia.pessoas` | ✅ | `acrescenta_na_fila` passa `cfg["regencia"]["pessoas"]` a `valida_ruling`; sem a chave → `"config sem regencia.pessoas"`; `TestF20Negativos::test_f20_autor_fora_das_pessoas_recusado` verde |
| `grep -rn '\.env\|settings.local.json' painel/` sem caminho de **leitura** | ✅ | matches só em docs, no guard que *recusa* (`ingest.py:25`), em `os.environ.get` dos hooks e em testes (negativo) |
| Dívidas herdadas **declaradas** | ✅ | **D-072-3** (CSRF/autoria), **D-072-4** (`data()` sem `try/except`), **D-072-5** (`custo.py`) — no plano e em "Dívidas declaradas" acima. **Não** silenciadas, **não** vendidas como pagas |

*Nota de escopo*: o gatilho de FR17 **fortalece** a base (recusa `UPDATE`/`DELETE` arbitrários em
`rodadas`/`transicoes`/`fila`/`passos`) e preserva o fechamento legítimo do `Stop` via `WHEN` — sem
vetor novo.

## Mutation (TAIL:mutation)

Quebrada a **CONDIÇÃO** (não o nome) de cada gate deste ciclo; nomes dos testes que falharam colados
da saída; **cada mutação revertida** (`git checkout -- <arquivo>`), worktree limpa ao fim.

| Gate | Mutação aplicada | Teste(s) que falharam |
|---|---|---|
| **FR10** — normalização | `normalizacao.normaliza` passa a `return canonico` (str) em vez de `dict` | `TestF6Normalizacao::test_f6_normalizacao_tabela_dirigida` — **1 failed** (`TypeError: string indices must be integers`) |
| **FR12** — permanência na fila | `fila.sai_da_fila` → `return True` (todo pedido sai) | `TestF4Fila::test_f4_pedido_sem_ruling_fica_na_fila` — **1 failed** (`[] != ['D-001','D-003']`) |
| **FR9** — transição sem arquivo | rota: `if not proposta.get("permitido") and False:` (o 422 pretendido some) | **NENHUM** — `TestF3TransicaoSemArquivo` **PASSOU** com a mutação ⇒ **F3 é vacua** (o 422 real vem do crash, não da regra). Confirmado com 2ª mutação na **função pura**: `proposta_transicao` sempre `permitido` → `TestF2CartaoEmGn::test_f2_cartao_em_gn_exige_arquivo_do_gate` **failed**, `TestF3` **passou**. ⇒ a regra é provada por F2, **a rota de FR9 não** |
| **FR16** — append-only | `fila_registro.acrescenta` abre em `"w"` (trunca) | `TestF14AppendOnly::test_f14_registro_append_only_so_cresce` · `TestF14AbreEmAppend::test_f14_registro_abre_sempre_em_append` · `TestF14Concorrente::test_f14_registro_concorrente_sem_perda` — **3 failed** |
| **FR17** — gatilho com `WHEN` | `passos_no_update` perde o `WHEN` (`WHEN 1`, recusa incondicional) | `TestDivida5Gatilho::test_divida5_gatilho_recusa_update_e_delete` — **1 failed** (`sqlite3.IntegrityError: append-only: passo so aceita o fechamento`) **na linha do fechamento legítimo** ⇒ o `WHEN` é *load-bearing* |

**Prova do fechamento com o gatilho intacto** (revertida a mutação): `TestDivida5Gatilho` →
**`1 passed in 0.25s`** — `UPDATE passos SET saida_em=… WHERE saida_em IS NULL` **continua passando**
(FR3 do 070 preservado); o passo **já fechado** segue recusado.

**Saída integral das mutações (colada da execução):**

```
FR10  F  TestF6Normalizacao::test_f6_normalizacao_tabela_dirigida  1 failed
FR12  F  TestF4Fila::test_f4_pedido_sem_ruling_fica_na_fila        1 failed
FR9   .  TestF3TransicaoSemArquivo                                  1 passed   <-- VACUA
FR9'  F  TestF2CartaoEmGn::test_f2_cartao_em_gn_exige_arquivo_do_gate  1 failed (função pura)
FR16  F F F  TestF14AppendOnly / TestF14AbreEmAppend / TestF14Concorrente   3 failed
FR17  F  TestDivida5Gatilho  1 failed  (IntegrityError no fechamento)
FR17' .  TestDivida5Gatilho  1 passed  (gatilho intacto)
```

<details><summary>Saída literal (recortes)</summary>

```
# FR10
>       self.assertEqual(r["canonico"], canon, f"normaliza({valor!r})['canonico']")
E       TypeError: string indices must be integers, not 'str'

# FR16 (abre-em-append)
E       AssertionError: Lists differ: [(85, 'w')] != []
E        : FR16: o registro never é aberto em modo de reescrita/truncagem — só append.

# FR17 (gatilho sem WHEN)
>               con.execute("UPDATE passos SET saida_em='2026-10-22T16:05:00+00:00', "
                            "resumo='ok', resultado='ok' WHERE passo='T1'")
E       sqlite3.IntegrityError: append-only: passo so aceita o fechamento (saida_em, resumo, resultado)
```
</details>

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
- **R1 (novo) — o nome `_pasta_do_chamado` colide e mata FR9; F3 é vacua (anti-padrões 23 e 13).**
  A rotina é definida **duas vezes** em `painel/server.py` (W04 `:400` devolve `(pasta, rel)`; W05
  `:582` devolve `pasta`), a última vence, e `_arquivos_do_gate` desempacota a string →
  `ValueError` → o `except ValueError` do `do_POST` responde **422 de crash** para *toda* transição.
  Medido por sonda: POST com arquivo **válido** devolve 422, não 200. A *fitness function* F3 passa
  porque só confere `code==422` + "contém 'erro'". **Não corrigido por mim** (a entrega só toca
  `qa-report.md`/`tasks.md`): o remédio é renomear uma das duas funções (ou dar-lhes nomes distintos)
  e, na volta, F3 deve passar a exigir o **motivo de domínio** e um **200** no caminho legítimo.
- **R2 (novo) — `boundary.json` não declara `docs/journeys/` (anti-padrão 23).** `check-boundary.sh`
  fica **vermelho** com 4 órfãos sob `docs/journeys/` (a skill usa o plural; `boundary.json` declara
  só `docs/jornada/`). Correção de uma linha em `boundary.json` — fora do alcance desta entrega.
- **Contagem de FR divergente (menor).** A moldura do ciclo (tasks.md/T06) diz "25 FR"; `spec.md`
  enumera **27** (FR1–FR27). Revisadas todas as 27; a divergência fica declarada.
- **Dívida do método (registrada por decisão do regente, 24/10): a skill `living-journey` cita
  `docs/journeys/` (`skills/living-journey/SKILL.md:30`) enquanto a convenção deste repositório é
  `docs/jornada/` (pasta existente, declarada em `boundary.json`). Decisão do regente na rodada de
  correção: a jornada do 072 **muda para `docs/jornada/`** (T13/W01) e a **skill será corrigida num
  ciclo próprio, raia leve** — a divergência é do método, não desta rodada.**

### 072-T13 — R2 corrigida (Worker01)

- **Entregue** (`[[DONE id=072-T13 outcome=delivered]]`, 24/10) na `w/worker01`. Base: `git merge
  --ff-only ee9b3a9` entrou limpo a partir de `3cbd9f1` (sem push).
- **A jornada mudou para `docs/jornada/` (singular — o repositório vence).** `git mv` dos 4 arquivos,
  registrados como **renames** (não apagar+criar):
  ```
  R  docs/journeys/072-painel-de-regencia.md  ->  docs/jornada/072-painel-de-regencia.md
  R  docs/journeys/img/072-01-kanban.png      ->  docs/jornada/img/072-01-kanban.png
  R  docs/journeys/img/072-02-fila.png        ->  docs/jornada/img/072-02-fila.png
  R  docs/journeys/scripts/captura-072.sh     ->  docs/jornada/scripts/captura-072.sh
  ```
  `docs/jornada/` já existia (o trilho do livro, `README.md`); `scripts/` e `img/` foram criados
  dentro dela — **nada sobrescrito**.
- **Links e caminhos corrigidos**: o cabeçalho do documento da jornada, as três ocorrências no
  `captura-072.sh` (uso, saída e `OUT=`) e o glob `documentos.jornadas` de
  `painel/projetos/exemplo.json`, que **volta a `docs/jornada/*.md`**. O `ROOT` do script (`../../..`
  a partir de `docs/jornada/scripts/`) continua resolvendo a raiz — mesma profundidade. Os links de
  imagem do documento (`img/072-*.png`) são relativos e seguem válidos.
- **O script regenera do caminho novo** (regeneração é o teste do próprio script — skill
  `living-journey`). Saída real:
  ```
  == subindo o painel real em http://127.0.0.1:8791 (fixture exemplo) ==
  == esperando a derivação aquecer (até 90s) ==
    derivação estabilizada com 1 chamado(s) em 2.2s
  == capturando as duas telas com o navegador (msedge) ==
  ok: ...\docs\jornada\img\072-01-kanban.png  (Painel de regência)
  ok: ...\docs\jornada\img\072-02-fila.png  (Fila de decisões)
  == pronto: capturas em ...\docs\jornada\img ==
  ```
- **`check-boundary` verde, sem órfãos.** O script versionado chama `python3` (alias da MS Store,
  não executa); rodei o **mesmo corpo Python** embutido nele — extraído do arquivo e executado com o
  interpretador real, sem alterar uma linha do script:
  ```
  ── 1. Every tracked file has exactly one domain ──
    toolkit   586 files  (read by machines)   guide      85 files  (read by humans)
    ✓ no orphan, no double claim
  ── 2. Every shared path is owned by the toolkit ──
    ✓ 6 shared path(s), all owned by the toolkit
  ── 3. Every published page has a declared source ──
    ✓ 39 pages: 29 owned by the guide, 10 declared shared
  ✓ boundary decidable: every file has a domain, every published page has a source.
  exit=0
  ```
  Os 4 órfãos de `docs/journeys/` deixaram de existir: os arquivos agora pertencem ao domínio `guide`
  (`docs/jornada/`). `boundary.json` **não** foi tocado — a correção foi no conteúdo, como o regente
  decidiu.
- **`check-links` verde (bloco equivalente; ressalva declarada).** O script é **bash puro** e o
  emulador de **fork do msys** (um `sed`/`grep` por arquivo sobre as ROOTS, agravado por
  `.claude/worktrees`) não o deixa terminar nesta máquina — o mesmo já registrado no T08. Bloco
  equivalente (mesma regra, mesmas ROOTS, podando `.claude/worktrees`), num processo só:
  ```
  -- Relative links across the repository (equivalente; worktrees podados) --
    checked: 341
  v every relative link resolves.
  ```
- **Não reescrevi o histórico.** As menções a `docs/journeys/` nas seções de revisão acima (achados
  R1/R2 do T06 e a dívida do método) **ficam como estão** — registram o estado de então. Pelo mesmo
  motivo **não** toquei `spec.md`, `plan.md` nem `tasks.md`: são registro do ciclo, e a rota é
  **apensar**, não reescrever (CLAUDE.md).
- **Ressalva para o Gerente decidir (1 linha cada; arquivos também abertos no T14/W02).** A evidência
  de FR26 em `spec.md:314`, `plan.md:384` e no bloco do T08 em `tasks.md:191,193,199,201` ainda cita
  `ls docs/journeys/072-*.md`. Depois da mudança, esse comando aponta para o caminho antigo — quem
  rodar a evidência do DoD colhe "no such file". Recomendo corrigir **plural → singular** nesses
  pontos (ou manter a divergência visível, se a decisão for essa). Não editei para não colidir com o
  T14 nos mesmos arquivos.
- **Limites respeitados**: só a worktree; sem push/merge/rm -rf; sem `.env`/`settings.local.json`.
- **Resíduo (não rastreado, inofensivo)**: os diretórios **vazios** `docs/journeys/` (e
  `docs/journeys/scripts`, `docs/journeys/img`) continuam no disco; não são rastreados pelo git e não
  aparecem em nenhum gate. Removê-los exige `Remove-Item`, negado pela política da sessão.
