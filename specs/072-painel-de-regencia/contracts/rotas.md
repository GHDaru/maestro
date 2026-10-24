# Contratos — rotas HTTP da rodada 1 (072)

> Artefato condicional declarado no plano (`ART:contracts=yes`). Contrato das **portas novas** que
> outras sessões e a IA consomem. O *como* foi delegado ao plano pela spec revisada (FR9: "rota e
> tratamento de erro é decisão do plano"). Todas as rotas são **locais** (o servidor recusa fora de
> `127.0.0.1` — `painel/server.py:507`) e o painel **nunca promove nem decide** (anti-regras 1–8 do
> `ux-design.md` §4).
>
> Siglas: FR (*functional requirement*) · HTTP (*Hypertext Transfer Protocol*) · JSON (*JavaScript
> Object Notation*) · POST/GET (métodos HTTP).

## Convenções comuns

- **Base**: `http://127.0.0.1:<porta>` (só loopback). Requisição de outro host → **403**.
- **Corpo**: JSON (`Content-Type: application/json`). Corpo inválido → **400**.
- **Recusa de domínio**: **422** com `{"erro": "<motivo>"}` — o mesmo tratamento de `ValueError`
  que já existe em `painel/server.py:523`.
- **Resposta OK**: **200** com `{"ok": true, …}`.

## `POST /api/regencia/transicao` — o arrasto propõe, não promove (FR8, FR9)

Pedido:

```json
{ "chamado": "072", "de": "G2", "para": "G3" }
```

- **200** — existe, na pasta do chamado, um arquivo `G3-*.md` com **cabeçalho válido** (o mesmo
  `valida`/`confere` do conferidor). Devolve a **proposta**, sem mover nem gravar nada:
  `{"ok": true, "proposta": {"chamado": "072", "de": "G2", "para": "G3", "exige": "G3-*.md",
  "dono": "<papel do GATES>", "promocao": "arquivo assinado pelo dono (068)"}}`.
- **422** — falta o arquivo do gate de destino (ou o cabeçalho não é válido):
  `{"erro": "falta G3-*.md com cabeçalho válido"}`. **Nenhum arquivo muda** (anti-regra 1).

## `GET /api/regencia/fila` — leitura da fila (FR11–FR15, FR20)

- **200** com `{"ok": true, "itens": [ … ], "mais_velho": "<ISO-8601>", "destravados": <n>, "vazia": <bool>, "data_fonte": "…"}`.
- Cada item é um **pedido** ou um **portão derivado** (ver `esquemas.md`). Ordenados por **prazo ×
  bloqueio** (o que estoura antes e trava mais vem primeiro — FR15), com o **nº de destravados**.
- Fila vazia é **informação**: `{"vazia": true, "mensagem": "fila vazia — última decisão às HH:MM"}`.
- Toda idade vem do relógio/registro: `"idade": "há 7 h 12 min"` **e** o carimbo absoluto em
  `"carimbo"` (FR23); `mais_velho` alimenta o **contador do cabeçalho**.
- A um agente, o item de **portão do regente** vem `"somente_leitura": true`.

## `POST /api/regencia/fila` — acréscimo (append-only) (FR11, FR14, FR16, FR18, FR19)

- Corpo = um **pedido** (`{"tipo": "pedido", …}`) ou um **ruling** (`{"tipo": "ruling", …}`), conforme
  `esquemas.md`.
- **200** — acrescenta **exatamente uma linha** ao JSONL (`painel/dados/fila-<projeto>.jsonl`) e devolve
  `{"ok": true, "registrado": {"tipo": "ruling", "pedido": "D-014"}}`. **Nunca** reescreve, reordena ou
  remove linha (FR16); o `POST` do *ruling* grava `autor` **do formulário** (FR18) — o servidor **não**
  infere autoria do agente que pediu.
- **422** — `ruling` sem `autor` humano ou sem `destinatario`: `{"erro": "ruling sem autor humano"}` /
  `{"erro": "ruling sem destinatario"}` (FR14); `pedido` sem campo obrigatório: `{"erro": "falta
  '<campo>' no pedido"}` (FR11). **Nada é gravado.**
- A resposta do `ruling` aceita o **id derivado** de um portão do regente (ex.: `"pedido": "072+T7"`).

## `GET /api/regencia/kanban` — projeção do 068 (FR1–FR7, FR10)

- **200** com `{"ok": true, "colunas": [ {"gate": "G0", "nome": "…", "cartoes": [ … ]}, … ],
  "faixa": {"abertura": …,"GD": …}, "frentes": [ … ], "meta": {"ingerido_em": "…"}, "data_fonte": "…"}`.
- **Dez** colunas fixas **G0–G9**, na ordem da tabela `GATES` (`painel/chamados.py:18-30`); o cartão fica
  no **último gate com veredito vigente aprovado** (FR2, reusando `confere`/`ordem_veredito` — sem
  segundo conferidor).
- `faixa` carrega `abertura` e `GD` (que **não** viram coluna — limites da spec), com estado e motivo.
- Cada cartão traz `veredito` **original** e `veredito_normalizado` **ao lado** (FR3/FR10), o
  `independencia` (FR4, com `autor_da_peca` exposto pelo parser — FR5) e `integrado_criticado` sempre
  `"não conferido"` (FR6). Todo número/selo traz `data_fonte` (FR21); fonte ausente → `"—"` com
  `motivo:` (FR22).
- `meta.ingerido_em` com mais de 1 h → `"defasado": true` no cabeçalho (FR25).

## `GET /api/meta` — acrescenta `frentes` (FR7)

- **200** com o que já existe (equipes, contatos, `ingerido_age_min`) **mais** `"frentes": { "<frente>":
  ["specs/<pasta>", …] }` lido de `projetos/<nome>.json`. Sem a chave, todas as frentes (FR7).
