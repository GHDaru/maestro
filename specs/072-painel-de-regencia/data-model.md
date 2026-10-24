# Data model 072 — o agregado da fila, o registro append-only e a projeção do kanban

> Artefato condicional declarado no plano (`ART:data-model=yes`). Descreve **o que é dado novo** nesta
> rodada: o agregado da fila (Pedido de decisão + Ruling), o formato da linha do registro, o item
> derivado "portão do regente" e o que o kanban **projeta** sem criar entidade (Chamado/Gate/Veredito
> do 068). Nomes de campo seguem **português** (dado do painel, como o `docs/records/decisoes.jsonl`,
> ADR 0014); nomes de código (funções, rotas) são o que o plano fixou.
>
> Siglas: FR (*functional requirement*) · JSONL (*JSON Lines*, um objeto JSON por linha) · SQLite
> (*Structured Query Language, light*) — apenas para contraste, o registro da fila **não** é SQLite.

## 1. Agregado novo: a fila (raiz `PedidoDeDecisao`)

`DOM:aggregate=PedidoDeDecisao`. A fila é um agregado novo; o **Pedido de decisão** é a raiz e o
**Ruling** é entidade **dentro** dele — um *ruling* não existe sem o pedido que ele fecha (spec §"Para
o plano", item 1). A escolha de "dentro" e não "agregado próprio" é deliberada: a resposta pode chegar
por delegação (FR14), mas a **referência ao pedido** é invariante em todo *ruling*.

### Pedido de decisão (raiz)

| Campo | Tipo | Obrigatório (FR11) | O que é |
|---|---|---|---|
| `id` | texto | ✅ | Identificador do pedido (ex.: `D-014`). |
| `pedido_por` | texto | ✅ | Quem pediu — **papel + sessão** (ex.: `Worker03/sess-12`). |
| `pergunta` | texto | ✅ | A pergunta escalada ao humano. |
| `opcoes` | lista de `{id, descricao}` | ✅ | As alternativas, com descrição (a/b, i/ii). |
| `recomendacao` | texto | ✅ | Texto de **quem pediu** (nunca do painel — anti-regra 2). |
| `prazo` | texto (ISO-8601) | ✅ | Quando estoura; entra na ordenação (FR15). |
| `destrava` | lista de textos | ✅ | Chamados/sessões presos em "aguardo o GO" que isto solta. |
| `destino` | texto | ✅ | Para quem volta a resposta. |
| `status` | texto | ✅ | Derivado: `aguardando` enquanto não houver *ruling*. |
| `criado_em` | texto (ISO-8601) | ✅ | **Timestamp do registro** — a idade sai daqui, nunca digitada (FR23). |
| `pedido_de` | texto | — | Pedido-pai, se este pedido nasceu de outro (encadeamento). |

### Ruling (entidade dentro do pedido)

| Campo | Tipo | Obrigatório (FR13/FR14) | O que é |
|---|---|---|---|
| `pedido` | texto | ✅ | **A referência ao pedido** (a razão de o Ruling viver dentro do agregado). |
| `escolha` | texto | ✅ | Opção escolhida (id da opção) e/ou o texto livre do humano. |
| `autor` | texto | ✅ | **Autor humano** — só pessoa (decisão 1a). Sem ele, o *ruling* é **recusado**. |
| `destinatario` | texto | ✅ | Destino — a quem a resposta é **encaminhada** ("encaminhado a …"). Sem ele, **recusado**. |
| `data` | texto (ISO-8601) | ✅ | Quando; do relógio/timestamp, nunca digitado. |
| `link` | texto | — | Link para o **merge/ADR** que cita o *ruling* (FR13). |
| `registrado_por` | texto | — | Quem **lançou** o registro, quando ≠ `autor` (ex.: a Office por delegação). |
| `delegacao` | texto | — | **Referência ao registro de delegação** que autoriza o lançamento (decisão 1a). |
| `tipo` | texto | — | `resposta` \| `devolucao` — "devolver a quem pediu" é *ruling* **registrado** (FR12/FR13). |
| `registrado_em` | texto (ISO-8601) | ✅ | Timestamp do acréscimo ao registro. |

**Invariante (pura):** `valida_ruling(ruling)` → recusa sem `autor` **ou** sem `destinatario` (FR14);
`sai_da_fila(pedido, rulings)` → um pedido **sem** *ruling* com `pedido == pedido.id` permanece na
fila (FR12). Ambas vivem em `painel/regencia/fila.py`, sem HTTP nem arquivo.

## 2. Item derivado: Portão do regente (não é entidade — é projeção)

`portao_derivado(chamado, gate, status, commit)` (FR20). **Não** é gravado: nasce do arquivo de gate
e do `tasks.md` do ciclo. Existe na fila como item **somente leitura** para um agente.

| Campo | De onde vem |
|---|---|
| `id` | **derivado**: `chamado + gate` (ex.: `072+T7`); o *ruling* aceita esse id. |
| `chamado` | a pasta `specs/<id>/`. |
| `gate` | `G7`, `G8` ou `TAIL:gate`. |
| `status` | o status no arquivo de gate (pendente). |
| `desde` | **o commit do arquivo** de gate (não data digitada). |
| `evidencia` | link para o arquivo/evidência que o sustenta. |

## 3. Registro da fila — arquivo do painel, append-only

**Caminho**: `cfg["fila_decisoes"]`, padrão `painel/dados/fila-<projeto>.jsonl` (decisão do plano,
ADR 0027). Fica em `painel/dados/` — **o próprio dado do painel**, ao lado do `<projeto>.db` — porque a
anti-regra 7 proíbe o painel de **escrever em arquivo do projeto** e a anti-regra do FR16 exige o
registro fora do projeto lido. `painel/dados/` é ignorado pelo git (`painel/.gitignore`): a fila é
**local** (dívida D-072-1).

**Formato**: **uma linha = um objeto JSON**, sempre com `tipo` (`pedido` \| `ruling`) para o leitor
distinguir o que a linha é; campos em português.

```jsonl
{"tipo":"pedido","id":"D-014","pedido_por":"Worker03/sess-12","pergunta":"…","opcoes":[{"id":"a","descricao":"…"}],"recomendacao":"…","prazo":"2026-10-24T12:00:00-03:00","destrava":["072"],"destino":"Regente","status":"aguardando","criado_em":"2026-10-24T07:04:00-03:00"}
{"tipo":"ruling","pedido":"D-014","escolha":"a","autor":"Darú","destinatario":"Worker03","data":"2026-10-24T09:30:00-03:00","link":"docs/adr/0027-…","registrado_em":"2026-10-24T09:30:05-03:00"}
{"tipo":"ruling","pedido":"072+T7","escolha":"aceito","autor":"Darú","destinatario":"Regente","tipo_ruling":"resposta","registrado_em":"2026-10-24T10:00:00-03:00"}
```

**Regra de escrita (FR16, mecânica)**: o painel **só cresce** o arquivo. `painel/fila_registro.py`
abre **sempre** `open(caminho, "a", encoding="utf-8")` e **nunca** `"w"`/`truncate`/`seek`; cada
chamada acrescenta exatamente uma linha (`json.dumps(..., ensure_ascii=False)` + `\n`). O teste
`test_f14_registro_append_only_so_cresce` guarda o **prefixo de bytes** de antes e prova que ficou
**inalterado** depois — a prova de que nada foi reescrito, reordenado ou removido.

**Leitura**: `le(caminho)` é tolerante — uma linha inválida (JSON quebrado) é **ignorada com aviso**,
nunca derruba a fila; o leitor não escreve.

## 4. Projeção do kanban (entidade **nenhuma** é criada)

O kanban **projeta** o que o 068 já calcula — não há entidade nova (spec §"Para o plano", item 1).

```text
Chamado (raiz, do 068 — painel/chamados.py:121 confere)
  └─ Gate (G0..G9, de GATES — painel/chamados.py:18-30)
       └─ Veredito (do cabeçalho do arquivo G*-*.md; painel/chamados.py:144-148)
```

| Campo do cartão | Fonte (FR3) |
|---|---|
| `id`, `frente` | pasta `specs/<id>/` e `cfg["frentes"]` (FR7). |
| `dono` (papel + sessão) | papel da tabela `GATES`; sessão do cabeçalho do gate (sem sessão → "—" com motivo). |
| `veredito_normalizado` | `normaliza(valor, erros)` (FR10), **ao lado** do `veredito` original — nunca no lugar dele (anti-regra 6). |
| `autor_da_peca`, `por` | **`autor_da_peca` é campo novo exposto pelo parser** (FR5, `painel/chamados.py`); `por` já existe (`:145`). Iguais → marcador vermelho (FR4); sem `autor_da_peca` → "—". |
| `idade` | `idade_do_carimbo(quando, agora)` (FR23) — do relógio/timestamp; data digitada → selo "declarada". |
| `selo_evidencia` | cabeçalho do gate. |
| `integrado = criticado` | **"não conferido"** (FR6) até existir o script versionado de `git patch-id --stable`. |

## 5. Relações

```text
PedidoDeDecisao 1 ──< Ruling            (o Ruling não existe sem o pedido)
PedidoDeDecisao 1 ──< destrava >── N Chamado/Sessão   (texto; o nº de destravados ordena a fila, FR15)
Chamado        1 ──< PortaoDoRegente    (derivado, não gravado; id = chamado+gate, FR20)
Chamado        1 ──< Gate 1 ──< Veredito (do 068; o kanban só projeta)
registro JSONL 1 linha ── 1 PedidoDeDecisao | 1 Ruling   (append-only, FR16)
```

## 6. Vocabulário (vai para `docs/governance/glossary.md`, em inglês, ADR 0014)

| Termo | Definição | Evitar |
|---|---|---|
| Painel de regência | read-model local onde o humano vê a fila, os chamados por gate e a jornada; nunca promove nem decide. | "dashboard de métricas" |
| Pedido de decisão | pergunta escalada ao humano com id, quem pediu, opções, recomendação, prazo, o que destrava e destino. | "pendência", "aguardo o GO" |
| Ruling | resposta registrada ao pedido, com autor humano, data, destinatário e link ao merge/ADR. | decisão só em mensagem/memória |
| Veredito normalizado | mapeamento canônico aprovado/devolvido/vermelho provado/em curso/inválido, **ao lado** do original. | reescrever o arquivo de gate |
| Portão do regente | G7, G8 e `TAIL:gate` — gates que só o humano registra; item derivado da fila. | "aprovação automática" |
