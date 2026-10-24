# Plan 072 — Painel de regência, rodada 1: kanban por gate e fila de decisões

- **Spec**: `specs/072-painel-de-regencia/spec.md` — **revisão T01b** (condições C1–C8 do gate DoR
  incorporadas; **25 FR** em EARS; 13 testes nomeados; duas ambiguidades decididas pelo Darú) ·
  **Raia**: plena · **Data**: 2026-10-24 · **Status**: proposta (aguarda o gate do plano)
- **Appetite** (espelha a spec, operating-model §5): um ciclo — o recorte de duas telas (§2.1
  kanban por gate, §2.3 fila de decisões); escopo variável dentro do tempo fixo, sem prazo estimado.
- **Insumos lidos**: `spec.md` (revisada — copiada da worktree `w/worker01`, que **não** tinha
  commit além de `f48a383`), `docs/governance/principles.md`, `operating-model.md`, `artifacts.md`,
  `specs/066-painel-de-regencia/ux-design.md` (§2.1, §2.3, §3, §4 anti-regras, §5 glossário, §6,
  §7 F1–F12), `specs/070-workflow-sqlite/plan.md` (as dez dívidas), `painel/chamados.py`,
  `painel/server.py`, `painel/index.html`, `painel/schema_workflow.sql`,
  `painel/hooks/workflow_stop.py`, `painel/projetos/exemplo.json`, `docs/records/decisoes.jsonl`.
- **Decisão de método já tomada (não se reabre)**: `decisao-072-gates-delegados` + gate DoR
  delegado ao crítico independente (**ADR 0026**). Ambiguidade 1 → **(1a) só pessoa é autor humano**
  (FR14/FR18); ambiguidade 2 → **(2a) os dois**: item de fila com id derivado **e** marcador no
  cartão (FR20).
- **Siglas**: A2A (*Agent-to-Agent*, ligação entre agentes) · ADR (*Architecture Decision Record*) ·
  CI (*Continuous Integration*) · DOM (*domain model*) · DoD (*Definition of Done*) · DoR
  (*Definition of Ready*) · EARS (*Easy Approach to Requirements Syntax*) · FR (*functional
  requirement*) · HTML (*HyperText Markup Language*) · HTTP (*Hypertext Transfer Protocol*) ·
  JSONL (*JSON Lines*) · PID (*Process IDentifier*) · TAIL (*closing tail*) · UX (*User Experience*).

## Constitution Check (governance/principles.md)

| Principle | Compliance |
|---|---|
| I. Spec-driven | ✅ A spec revisada (25 FR) precede o código; este plano existe antes de qualquer linha de `painel/regencia/`. A tela consome o `ux-design.md` do 066 (§2.1/§2.3), que é input, não descrição. |
| II. Human-governed orchestration | ✅ O painel **lê e registra**, nunca promove nem decide (anti-regras 1 e 2). O *ruling* exige autor humano (FR14); a delegação guarda `registrado_por` sem confundir autoria. FR17 impõe append-only **mecânico** no workflow herdado — quem recusa é a base, não a convenção. |
| III. Reversibility / risk-proportional gates | ✅ Texto versionado em `painel/` + `git revert`; nada de ambiente, migração ou arquivo de gate movido. **Exceção declarada**: FR17 mexe no schema do 070 e ajusta o hook `Stop` — risco **médio** (a base passa a recusar escrita), com *rollback* = `git revert`; sem bloco de irreversibilidade (nada fora do repositório, nenhum dado real). A rodada 2 fica declarada **infra**. |
| IV. Test-first / verifiable DoD | ✅ **13 testes nomeados** (um por regra) em `painel/tests/test_regencia.py`; as regras puras nascem antes do adaptador HTTP; **F1 e F9 viram teste sobre o HTML renderizado**, não `grep` no fonte (condição do gate). A cauda `TAIL:mutation` quebra a **condição** de FR9, FR12, FR10 e do gatilho de FR17 e cola os nomes dos testes que falham. |
| V. Context economy / boundary | ✅ Corte hexagonal: regras puras numa fronteira só (`painel/regencia/`, sem HTTP nem arquivo) e adaptadores em `painel/server.py` + `painel/fila_registro.py` (JSONL) e `painel/index.html` (tela). O kanban **reusa** `confere`/`ordem_veredito` do 068 — não há segundo conferidor (anti-padrão 22). `painel/regencia/` fica dentro de `painel/`, que já está no `boundary.json`. |
| VI. Living artifacts / traceability | ✅ No mesmo PR: `spec.md`, `plan.md`, `tasks.md`, `data-model.md`, `contracts/`, `ux-design.md` (apontador), `docs/journeys/072-*.md`, `qa-report.md`, glossário (5 termos), ADR 0026 + 0027, `CHANGELOG.md` e `docs/roadmap.md`. Cadeia spec ↔ PR ↔ testes ↔ jornada. |
| VII. Light governance / YAGNI | ✅ Sem broker/big-bang: a fila é JSONL append-only; o gatilho de FR17 são três `TRIGGER` curtos no schema que já existe. `abertura`/`GD` não viram coluna (faixa acima do kanban). Dívida 2 do 070 **não** é paga (declarada). |
| VIII. Intelligible communication | ✅ Primeira ocorrência de cada sigla expandida; os cinco termos novos entram em `docs/governance/glossary.md` (inglês, ADR 0014). |

**No violations.**

## Artifacts of this cycle (declare all five — silence is not a decision)

| Artifact | Declaration | Why |
|---|---|---|
| `research.md` | `ART:research=no` | Nenhuma incógnita: as regras de veredito e conferidor vêm de 068/069; o desenho das telas, do `ux-design.md` do 066; a disposição das dívidas, do gate DoR. A única decisão nova (o caminho do registro) é do plano e vira ADR 0027, não pesquisa. |
| `data-model.md` | `ART:data-model=yes` | Entidades novas: **Pedido de decisão** (raiz) e **Ruling** (dentro dele), mais o **registro append-only** da fila; o item **Portão do regente** é derivado. O kanban projeta Chamado/Gate/Veredito do 068 sem entidade nova. |
| `contracts/` | `ART:contracts=yes` | Interface nova entre partes: a transição (escrita, 422 em recusa), a rota da fila (leitura e acréscimo) e a leitura do kanban, consumidas por outras sessões e pela IA. Separa o trabalho paralelo com segurança. |
| `checklist.md` | `ART:checklist=no` | A DoD abaixo cobre o que há para checar; os critérios de aceite da spec já são executáveis (comando → resultado). |
| `ux-design.md` | `ART:ux-design=yes` | As duas telas (§2.1 kanban, §2.3 fila) **já** estão desenhadas em `specs/066-painel-de-regencia/ux-design.md`; o artefato deste ciclo é um **apontador** de uma linha (padrão do 068), não uma reescrita. |

## Domain model (declare all four — silence is not a decision)

### Agregado

| Question | Declaration | Why |
|---|---|---|
| Aggregate root | `DOM:aggregate=PedidoDeDecisao` | Raiz nova: o **Pedido de decisão** é a raiz e o **Ruling não existe sem o pedido que ele fecha** (spec §"Para o plano", item 1) — escolho entidade **dentro** do agregado, e não agregado próprio, porque a resposta chega por delegação mas a referência ao pedido é invariante. O kanban **não** cria agregado: projeta Chamado/Gate/Veredito, cuja raiz segue sendo `Chamado` (`painel/chamados.py:121` `confere`; o estado vigente sai de `painel/chamados.py:151` e `:220`). O item **Portão do regente** (FR20) é derivado do arquivo de gate e do `tasks.md` — não é raiz, não é gravado. |

### Invariantes

`DOM:invariants=normaliza=domain | sai_da_fila=domain | ordena_fila=domain | valida_pedido=domain | valida_ruling=domain | coluna_do_cartao=domain | independencia=domain | idade_do_carimbo=domain | portao_derivado=domain | acrescimo_do_registro=edge(so-cresce-o-arquivo: vive no adaptador painel/fila_registro.py) | gatilho_append_only=edge(imposto-pela-base: vive em painel/schema_workflow.sql)`

| Invariante (pura) | Onde vive | Motivo (arquivo:linha) |
|---|---|---|
| `normaliza(valor, erros)` | `painel/regencia/normalizacao.py` (novo) | FR10, tabela-dirigida. Lê o veredito como já lido hoje (`painel/chamados.py:144-148`, campo `veredito`) e o sinal de inválido do conferidor (`painel/chamados.py:136` `erros = valida(...)` → `inválido`); qualquer outro valor cai em `inválido` com o original. |
| `sai_da_fila(pedido, rulings)` | `painel/regencia/fila.py` (novo) | FR12: pedido sem ruling fica na fila. |
| `ordena_fila(itens)` | `painel/regencia/fila.py` (novo) | FR15: prazo × bloqueio, com nº de destravados; o relógio entra por parâmetro. |
| `valida_pedido(pedido)` | `painel/regencia/fila.py` (novo) | FR11: exige os campos do pedido. |
| `valida_ruling(ruling)` | `painel/regencia/fila.py` (novo) | FR14: recusa sem autor humano ou sem destinatário — é o portão que o adaptador converte em 422. |
| `coluna_do_cartao(gates)` | `painel/regencia/kanban.py` (novo) | FR2: último gate com veredito vigente aprovado; reusa `ordem_veredito` (`painel/chamados.py:115-118`) e `validos[-1]` (`:220`) — **não** recalcula estado. |
| `independencia(autor_da_peca, por)` | `painel/regencia/kanban.py` (novo) | FR4/Princípio II: iguais → marcador vermelho. Alimentada por `autor_da_peca` (novo, FR5) e `por` (`painel/chamados.py:145`). |
| `idade_do_carimbo(quando, agora)` | `painel/regencia/kanban.py` (novo) | FR23: "há Xh Ymin" + carimbo absoluto, do relógio/registro; selo "declarada" para data digitada. |
| `portao_derivado(chamado, gate, status, commit)` | `painel/regencia/fila.py` (novo) | FR20: id derivado (chamado+gate), status do arquivo, "desde quando" do commit. |
| acréscimo sem reescrita | **borda** — `painel/fila_registro.py` (novo) | Append é regra de escrita: só existe junto do `open(..., "a")`. |
| gatilho append-only | **borda** — `painel/schema_workflow.sql` (FR17) | Imposto pela base (`TRIGGER`), não pela convenção: é a correção da dívida 5 do 070. |

> Duas invariantes ficaram na **borda** de propósito: elas não descrevem o domínio da fila, descrevem
> **como o arquivo é escrito** (append) e **quem garante** (a base). Movê-las para o domínio daria a
> uma função pura o poder de abrir arquivo — exatamente o que o corte hexagonal proíbe.

### Glossário

| Question | Declaration | Why |
|---|---|---|
| Ubiquitous language | `DOM:glossary=changed` | Entram cinco termos em `docs/governance/glossary.md`, em inglês (ADR 0014): **painel de regência**, **pedido de decisão**, **ruling**, **veredito normalizado** e **portão do regente**. Texto-fonte: `specs/066-painel-de-regencia/ux-design.md:128-133` (§5). |

### Portas e adaptadores

| Question | Declaration | Why |
|---|---|---|
| Ports and adapters | `DOM:ports=new` | Portas novas: **transição** `POST /api/regencia/transicao` (FR9; tratada no `do_POST` de `painel/server.py:507-525`, `ValueError`→422 em `:523`), a **rota da fila** `GET`/`POST /api/regencia/fila` e a **leitura do kanban** `GET /api/regencia/kanban`; a chave `frentes` do projeto exposta em
`/api/meta` (`painel/server.py:283` `v_meta`, que já abre a config para `contatos`/`equipes`, `:315-321`). Adaptadores: `painel/server.py` (HTTP), `painel/fila_registro.py` (JSONL), `painel/schema_workflow.sql` (o gatilho de FR17) e `painel/index.html` (telas). A leitura dos gates reusa `chamados.confere` (`painel/chamados.py:121`). |

## Decisões de arquitetura

### 1. Corte hexagonal — regras puras × adaptadores

```text
painel/regencia/                 (puro: sem HTTP, sem arquivo, sem sqlite3)
  __init__.py                    reexporta o que é público
  normalizacao.py                normaliza(valor, erros=None) -> {canonico, original, motivo?}
  kanban.py                      coluna_do_cartao, independencia, idade_do_carimbo, cartao, faixa_abertura_gd
  fila.py                        valida_pedido, valida_ruling, sai_da_fila, ordena_fila, portao_derivado
painel/fila_registro.py          (adaptador) caminho(cfg), acrescenta(caminho, obj), le(caminho)
painel/server.py                 (adaptador) rotas + enriquecimento do kanban
painel/index.html                (adaptador) as duas telas
painel/chamados.py               (estendido, FR5) expõe autor_da_peca no item do gate
painel/schema_workflow.sql       (estendido, FR17) três TRIGGER
painel/hooks/workflow_stop.py    (ajustado, FR17) para de escrever UPDATE em passos
painel/tests/test_regencia.py    os 13 testes nomeados
docs/journeys/072-*.md           (FR26) jornada viva + script versionado de captura
```

O plano **fixa os nomes de módulo e de rota** (a spec revisada delegou: "os nomes de módulo/rota
são decisão do plano, não critério"). A função pura de normalização **mantém o nome `normaliza`**
(a spec do T01 pedia esse nome; o T01b só retirou o `grep` do critério).

### 2. Endereço do registro JSONL da fila (FR16) — `painel/dados/fila-<projeto>.jsonl`

Chave nova `cfg["fila_decisoes"]`; **padrão** `painel/dados/fila-<projeto>.jsonl`, ao lado do
`<projeto>.db` que o servidor já cria ali (`painel/server.py:540`, `db_path = os.path.join(AQUI,
"dados", f"{cfg.get('projeto','painel')}.db")`).

**Por quê não `docs/records/`** (a inclinação do T01, corrigida pela spec revisada): a **anti-regra 7**
(`ux-design.md:120`) é literal — *"Não escreve em arquivo do projeto"* — e a FR16 exige o registro
como **arquivo do painel, fora do projeto lido**. `docs/records/` é pasta **do projeto** (o painel a
*ingere*) e `decisoes.jsonl` é do método, não do painel; gravar a fila ali misturaria o dado lido com
o dado do painel e faria o painel **escrever dentro do que ele lê**. `painel/dados/` é, por
construção, "o próprio dado" do painel (o `.db` já mora lá) — o único lugar que satisfaz a
anti-regra 7 **e** o FR16 ao mesmo tempo.

**Troca declarada (e aceita)**: `painel/dados/` é **ignorado pelo git** (`painel/.gitignore` —
`dados/`). Logo a fila é **local**: não é versionada, não viaja no clone e não aparece em revisão de
PR. É o preço de a anti-regra 7 ser literal; fica declarado como **D-072-1** e, em troca, o painel
não escreve uma linha sequer em arquivo do projeto. (O índice **versionado** de decisões continua
sendo `docs/records/decisoes.jsonl`, gerido por `scripts/record-decision.sh` — outro artefato, outro
dono.)

### 3. Append-only **mecânico** (FR16 + FR17) — duas provas, dois registros

(a) **Fila (FR16)**: `painel/fila_registro.py` abre **sempre** `open(caminho, "a", encoding="utf-8")`
e nunca `"w"`/`truncate`/`seek`; `acrescenta` serializa uma linha com `json.dumps(..., ensure_ascii=False)`
e um `\n`. O teste `test_f14_registro_append_only_so_cresce` guarda o **prefixo de bytes** antes e
prova que ficou **byte a byte inalterado** depois (o arquivo só cresceu) — é a exigência do FR16(b).

(b) **Workflow herdado (FR17 — a dívida 5 do 070 vira FR)**: três `TRIGGER`s em
`painel/schema_workflow.sql`, uma por tabela, recusando `UPDATE` **e** `DELETE` em `rodadas`,
`passos` e `transicoes` (`BEFORE UPDATE`/`BEFORE DELETE` → `RAISE(ABORT, 'append-only: …')`). Hoje o
schema **não tem gatilho nenhum** (confirmado: só `CREATE TABLE`, `painel/schema_workflow.sql:11-45`)
e o hook `Stop` faz `UPDATE passos` — que passa a ser **impossível**. Consequência declarada e
executada nesta rodada: `painel/hooks/workflow_stop.py` é ajustado para **não** escrever `UPDATE`
(só avisa no `stderr`), e a **cobrança de verdade** do `Stop` (dívida 7) fica para a rodada 2. Os
`_ensure_schema` (duplicados em hooks + `fila_outbox.py`) recebem os mesmos `CREATE TRIGGER IF NOT
EXISTS` para que um banco vivo ganhe os gatilhos — isso **não** paga a dívida 2 (as três cópias
continuam) e a **agrava** um pouco; declarado em **D-072-2**.

### 4. Rotas (portas) — decisão do plano

| Método e caminho | Papel | Recusa |
|---|---|---|
| `POST /api/regencia/transicao` | proposta de transição (arrasto): valida o arquivo do gate de destino + cabeçalho e devolve a proposta; **não move nem grava arquivo** (anti-regra 1) | **422 com motivo** (FR9) quando falta o arquivo do gate de destino válido |
| `GET /api/regencia/fila` | lê a fila ordenada (pedidos + portões derivados), com idade e nº de destravados | — |
| `POST /api/regencia/fila` | **acrescenta** uma linha ao JSONL — um `pedido` ou um `ruling` | **422 com motivo** (FR14: ruling sem autor humano/destino; FR11: pedido sem campo) |
| `GET /api/regencia/kanban` | dez colunas G0–G9 (FR1) com cartões, veredito normalizado **ao lado do original**, independência e a faixa `abertura`·`GD` | — |

A spec revisada deixou o *como* para o plano (FR9: "rota e tratamento de erro é decisão do plano").
Fecho em **três caminhos** (um de escrita da transição, um da fila — dois métodos — e um do kanban);
o kanban tem porta própria em vez de reusar `/api/chamados` porque precisa do veredito
**normalizado** e do filtro por frente, que não existem no cru. O `POST` mantém o tratamento de
`ValueError`→422 já existente (`painel/server.py:523`) e **recusa fora de localhost** como os outros
(`:507`).

### 5. `abertura` e `GD` — a faixa acima do kanban (spec, Limites)

`abertura` e `GD` existem na tabela `GATES` (`painel/chamados.py:18-19`) e **não** viram coluna. Entram
numa **faixa acima do kanban** ("Abertura · Risco") que mostra, por chamado da frente escolhida, o
estado e o motivo das duas pré-colunas — que `confere` **já** calcula (`painel/chamados.py:155-168`,
inclusive "classe C sem ADR ou decisão"). O kanban continua com **exatamente as dez colunas G0–G9**
(FR1). Sem fonte, "—" com motivo e caminho (FR22).

### 6. FR5 — o parser passa a expor `autor_da_peca` (extensão explícita do 068)

Verificado: `autor_da_peca` **não existe** em `painel/` hoje (nenhuma ocorrência em `painel/*.py` nem
`painel/*.html`); o cabeçalho só é lido por `por` (`painel/chamados.py:144-148`) e a regra de
independência vigente usa `autores` do `00-chamado.md` (`:105-106`, `:127`). Esta rodada **estende**
`valida`/`confere` de `painel/chamados.py` para ler `autor_da_peca` do cabeçalho do gate e devolvê-lo
**no item** ao lado de `por`; sem o campo, o marcador de FR4 exibe "—" com motivo (nunca verde
presumido). O `conferir_chamado.py` do Hindiana **não** é tocado, e a extensão é **declarada** (não
silenciosa), como a spec exige. Regressão: `painel/tests/test_chamados.py` e `python painel/chamados.py
painel/projetos/exemplo.json` (exit 0) continuam verdes.

### 7. ADRs desta rodada

- **ADR 0026 — Gates humanos delegados à sessão regente, com crítico independente**: registra a
  `decisao-072-gates-delegados` (o gate DoR delegado; o Accountable segue humano, Princípio II). É o
  ADR que a própria spec referencia na sua cauda.
- **ADR 0027 — O registro da fila é arquivo do painel (fora do projeto) e o append-only é mecânico**:
  registra (i) o endereço `painel/dados/fila-<projeto>.jsonl` e a troca "local × versionado", (ii) os
  dois mecanismos de append-only (escritor único + prefixo de bytes; `TRIGGER` na base), (iii) a
  rodada 2 declarada **infra**. Linha em `docs/records/decisoes.jsonl` (**só acréscimo**).

## How

1. **Domínio puro primeiro (Worker03).** `painel/regencia/` (normalizacao, kanban, fila) + extensão do
   parser (`painel/chamados.py`, FR5) + `painel/tests/test_regencia.py` com o **núcleo** dos testes
   puros (FR10, FR12, FR14, FR23, FR22, FR2). Nada em `painel/regencia/` importa `http.server`,
   `sqlite3` ou abre arquivo.
2. **Rotas e tela do kanban (Worker04).** `GET /api/regencia/kanban`, `POST /api/regencia/transicao`
   (422), `cfg["frentes"]` em `/api/meta`, a tela do kanban (dez colunas + a faixa `abertura`·`GD` +
   filtro por frente) e os testes **F1/F9 sobre o HTML renderizado** + F3/F2 HTTP.
3. **Fila: registro e tela (Worker05).** `painel/fila_registro.py`, `GET`/`POST /api/regencia/fila`, a
   ordenação, os portões derivados (FR20, com marcador no cartão) e a tela da fila (item, idade,
   destrava, "responder" grava `autor = humano`, nunca pré-marcado; "devolver a quem pediu"
   registrado). Testes F14 (prefixo de bytes) e FR20.
4. **Append-only mecânico (Worker07).** Os três `TRIGGER` + `CREATE TRIGGER IF NOT EXISTS` nas cópias de
   `_ensure_schema` + ajuste de `painel/hooks/workflow_stop.py` + `test_divida5_gatilho_recusa_update_e_delete`.
5. **Jornada viva (Worker08).** `docs/journeys/072-*.md` + script versionado de captura + heurística
   **datada ≥** a data da captura (skill `living-journey`, F11). Se o ambiente não renderizar, entregar
   o script e a heurística com a captura **declarada como pendente** — nunca inventar imagem.
6. **Revisão e segurança em contexto fresco + `qa-report.md` (Worker06)**, com a **mutação** de FR9,
   FR12, FR10 e do gatilho (nomeando os testes que falham).
7. **Fecha o ciclo**: `data-model.md`, `contracts/`, o apontador `ux-design.md`, os cinco termos no
   glossário, ADR 0026/0027 + linha em `decisoes.jsonl`, `CHANGELOG.md`, `docs/roadmap.md` e a
   correção do glob `documentos.jornadas` da fixture (`docs/jornada/*.md` → somar `docs/journeys/*.md`,
   porque a skill/spec usam o plural em inglês: `skills/living-journey/SKILL.md:30`).

**Ordem de merge e fatias disjuntas (evita conflito).** W03 (domínio + `painel/chamados.py` +
cria `test_regencia.py`) → **W04 e W05 em paralelo** sobre `server.py` (W04: `v_meta`/`ROTAS`/`do_POST`
do kanban e da transição; W05: `v_fila` + o ramo do JSONL — **funções separadas**) e sobre
`index.html` (W04 cria `vKanban` + botão de nav; W05 cria `vFila` + botão de nav) → **W07 e W08 em
paralelo** (`schema_workflow.sql`/`workflow_stop.py`/hooks vs. `docs/journeys/`) → **W04, W05 e W07
apensam seus testes no fim de `test_regencia.py`** (arquivo único exigido pela DoD; regra: **só
acrescentar ao final**, cada bloco com o seu comentário-cabeçalho) → W06 revisa o conjunto já
integrado.

## Verification (DoD)

> Comando → resultado esperado. Onde a spec do T01 fixava nomes e o T01b delegou ao plano, o comando
> usa o caminho decidido aqui (ex.: `painel/regencia/normalizacao.py`).

- `python -m unittest discover -s painel/tests -p test_regencia.py` → `Ran 13 tests`, `OK`, exit 0.
- Os **13 testes nomeados** (`painel/tests/test_regencia.py`):
  `test_f1_metrica_sem_data_fonte_zero_no_html_renderizado` (FR21) ·
  `test_f2_cartao_em_gn_exige_arquivo_do_gate` (FR2/FR8) ·
  `test_f3_transicao_sem_arquivo_devolve_422` (FR9) ·
  `test_f4_pedido_sem_ruling_fica_na_fila` (FR12) ·
  `test_f5_ruling_sem_autor_humano_ou_destino_e_recusado` (FR14) ·
  `test_f6_normalizacao_tabela_dirigida` (FR10) ·
  `test_f7_idade_do_relogio_e_carimbo` (FR23) ·
  `test_f8_traco_com_motivo` (FR22) ·
  `test_f9_botao_so_icone_com_aria_label_no_html_renderizado` (FR24) ·
  `test_f10_ingestao_defasada_anunciada` (FR25) ·
  `test_f14_registro_append_only_so_cresce` (FR16) ·
  `test_divida5_gatilho_recusa_update_e_delete` (FR17) ·
  `test_portao_do_regente_item_com_id_derivado` (FR20).
- **FR21 sobre o HTML renderizado**: a página renderizada tem **zero** `.metrica` sem `data-fonte` (não `grep` no fonte).
- **FR24 sobre o HTML renderizado**: **zero** `<button>` só-ícone sem `aria-label` e sem texto (não `grep` no fonte).
- QUANDO `G3-*.md` está ausente e o chamado tem G2 aprovado → cartão fica em G2 e exibe "falta `G3-*.md` com cabeçalho válido" (FR2).
- QUANDO uma transição é pedida sem arquivo de gate de destino válido → `422` com motivo e **nenhum arquivo muda** (FR9).
- QUANDO a fixture tem 3 pedidos e 1 ruling → a fila lista **2** (FR12).
- QUANDO um ruling chega sem `destino` (ou sem autor humano) → recusado (FR14).
- QUANDO o veredito é `APPROVE`/`OK`/`PASSA`/`PASSOU` → `aprovado`; `RETURN`/`REPROVE`/`FALHA` → `devolvido`; `FALHA_ESPERADA` → `vermelho provado`; `PENDENTE`/`REPRODUZIDO` → `em curso`; `NÃO PASSA` ou qualquer outro → `inválido` **com o original visível** (FR10).
- QUANDO um cabeçalho é reprovado pelo conferidor → `inválido`, **sem reescrever** o arquivo (FR10).
- QUANDO a fonte de um valor falta → "—" e o texto contém `motivo:` (FR22).
- QUANDO um `UPDATE`/`DELETE` é tentado em `rodadas`/`passos`/`transicoes` → recusado pelo `TRIGGER` (FR17).
- QUANDO o painel acrescenta uma linha ao registro da fila → o **prefixo de bytes** anterior fica inalterado (FR16).
- QUANDO `meta.ingerido_em` é antigo (> 1 h) → "defasado" no cabeçalho (FR25).
- QUANDO um chamado tem G7/G8/`TAIL:gate` pendente → item de fila com id derivado (chamado+gate), status do arquivo e marcador no cartão (FR20).
- `ls docs/journeys/072-*.md` → existe; `grep -c 'F11' docs/journeys/072-*.md` → `≥ 1` (FR26).
- `grep -rn '\.env\|settings.local.json' painel/` → nenhum caminho de **leitura** de `.env`/`settings.local.json` (FR27).
- `python painel/chamados.py painel/projetos/exemplo.json` → exit 0 (o conferidor 068/069 não mudou de comportamento; só o parser **acrescentou** um campo, FR5).
- `python -m unittest discover -s painel/tests -p 'test_*.py'` → verde (regressão de 068/069/070).
- `ls specs/070-conferidor-ordem-veredito/` → **10** arquivos (regressão do 069; a pasta segue imutável).
- `ls painel/projetos/*hindiana*` → vazio (fixture; `decisao-066-daru-20-10`).
- `scripts/check-language.sh` → verde; `scripts/check-boundary.sh` → verde; `scripts/check-links.sh` → verde.
- `scripts/check-conformance.sh 072` → verde **após** plano, tasks e `qa-report.md`.

## Herdado do 070 — disposição das dez dívidas (só a 5 é paga aqui)

> Espelha a spec revisada §"Herdado do 070". As demais vão para a **rodada 2 — raia infra** (declarada).
> Esta rodada **não** as vende como pagas.

| # | Dívida (070) | Disposição | O que 072 faz |
|---|---|---|---|
| 5 | "append-only" sem gatilho; o `Stop` faz `UPDATE passos` | **PAGA (FR17)** | Três `TRIGGER` no schema + ajuste do hook `Stop` (sem `UPDATE`) + `test_divida5_...`. |
| 1 | FR2/FR3 sem teste nomeado; regra na borda | rodada 2 | 072 **não** reincide: as regras novas são puras (`painel/regencia/`) com teste nomeado. |
| 2 | `_ensure_schema` em três cópias | rodada 2 | 072 **agrava** um pouco (os `CREATE TRIGGER` entram nas cópias) — declarado em D-072-2, não pago. |
| 3 | `install_hooks.py` sem backup/dry run | rodada 2 — infra | Fora do escopo; em aberto. |
| 4 | Nomes reais do Hindiana na fixture `equipes` | rodada 2 | 072 não acrescenta nomes reais: a fixture segue "Regente/Gerente/WorkerNN" e `ls painel/projetos/*hindiana*` fica vazio. |
| 6 | `SessionStart` imprime payload no stdout (injeção) | rodada 2 — infra | Fora do escopo; a fila nova lê só campos conhecidos. |
| 7 | FR3 invertido (`workflow_stop.py`) | rodada 2 — infra | 072 só **retira o `UPDATE`**; a **cobrança de verdade** do `Stop` fica na rodada 2 (declarado para não parecer pago). |
| 8 | FR1 parcial (sem branch/hash) | rodada 2 | Fora do escopo; em aberto. |
| 9 | FR10 provado por teste que injeta dados | rodada 2 | 072 testa sobre a **fixture** (`exemplo.json` + um JSONL de exemplo criado em diretório temporário), não sobre dados injetados no teste. |
| 10 | Troca atômica com WAL (`-wal`/`-shm` velhos; broadcast) | rodada 2 — infra | Fora do escopo; em aberto. |

**Dívidas de segurança que gates anteriores atribuíram ao 072** (em `docs/records/decisoes.jsonl` —
`gate-dev-integra-066-069`: *"CSRF no POST, autor forjável via MCP, `data()` sem try/except"*, dono
072; e `decisao-066-d4-custo-privacidade`: filtro de substring do `custo.py`, dono 072). **Esta
rodada as encosta sem as resolver por inteiro** — e por isso as **declara** em vez de as esconder:

- **CSRF/autor no POST**: as rotas POST novas (`/api/regencia/transicao`, `/api/regencia/fila`)
  herdam a classe de risco. Mitigação mantida: só `127.0.0.1` (`painel/server.py:507`), e o *ruling*
  grava `autor = humano` **do formulário**, sem inferir. O endurecimento (token de origem/CSRF,
  autoria não-forjável) **não** é feito aqui → **D-072-3**.
- **`data()` sem `try/except`** (`painel/chamados.py:74-78`): fora do caminho novo → **D-072-4**.
- **Filtro do `custo.py`**: fora do escopo desta rodada → **D-072-5**.

## Dívidas declaradas (novas desta rodada)

- **D-072-1** — a fila é **local** (`painel/dados/`, gitignored): não versionada, não viaja no clone.
  Preço aceito da anti-regra 7 ("não escreve em arquivo do projeto"); o índice **versionado** de
  decisões continua sendo `docs/records/decisoes.jsonl`.
- **D-072-2** — a dívida 2 do 070 (`_ensure_schema` em cópias) **piora**: os `CREATE TRIGGER IF NOT
  EXISTS` de FR17 entram nas cópias e precisam ficar em sincronia. Não paga aqui.
- **D-072-3** — endurecimento de **CSRF/autoria** nas rotas POST novas (herdada; dono original o
  próprio 072). Declarada, não silenciada.
- **D-072-4** — `data()` de `painel/chamados.py` sem `try/except` (herdada). Rodada 2, com teste.
- **D-072-5** — filtro do `custo.py` (substring → igualdade) (herdada). Fora do escopo desta rodada.
- **D-072-6** — **`TAIL:gate` como item da fila**: o item derivado é lido de `specs/<id>/tasks.md` por
  leitura simples; se a fonte divergir do estado do gate, a leitura plena do `TAIL:gate` fica para a
  rodada 2.
- **D-072-7** — **captura da jornada**: o script versionado entra nesta rodada; se o ambiente não
  renderizar a tela real, as imagens ficam **declaradas como pendentes** na jornada (nunca
  inventadas) — o critério executável de FR26 é o documento com o marcador F11.

<!--
  GATE (não delegável na origem; delegado nesta rodada ao crítico independente, ADR 0026): o plano
  é aprovado antes de virar tasks.
  Handoff: plan-architect → (gate) → tasks → dev-implementer.
-->
