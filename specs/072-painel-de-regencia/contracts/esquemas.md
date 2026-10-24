# Contratos — esquemas do pedido, do ruling e da linha do registro (072)

> Complemento de `rotas.md`. Os esquemas casam com `data-model.md`. Nomes de campo em **português**
> (dado do painel, ADR 0014). Os esquemas são **frouxos de propósito**: o painel **exibe e registra** —
> quem valida o conteúdo é o humano (FR14), não o servidor.

## Pedido de decisão (FR11)

```json
{
  "tipo": "pedido",
  "id": "D-014",
  "pedido_por": "Worker03/sess-12",
  "pergunta": "Aceitar a rodada 1 sem o mapa de sessões?",
  "opcoes": [
    {"id": "a", "descricao": "Aceitar agora e fazer o mapa na rodada 2"},
    {"id": "b", "descricao": "Esperar o mapa entrar nesta rodada"}
  ],
  "recomendacao": "a — o recorte de duas telas já destrava o regente",
  "prazo": "2026-10-24T12:00:00-03:00",
  "destrava": ["072", "066"],
  "destino": "Regente",
  "status": "aguardando",
  "criado_em": "2026-10-24T07:04:00-03:00"
}
```

- **Obrigatórios** (senão **422**): `id`, `pedido_por`, `pergunta`, `opcoes` (≥ 1, cada uma com `id` e
  `descricao`), `recomendacao`, `prazo`, `destrava`, `destino`, `status`.
- `recomendacao` é **texto de quem pediu**; o painel nunca a completa nem a marca (anti-regra 2).
- `criado_em` é o **timestamp do registro** — a idade sai dele (FR23).

## Ruling (FR13, FR14, FR18, FR19)

```json
{
  "tipo": "ruling",
  "pedido": "D-014",
  "escolha": "a",
  "autor": "Darú",
  "destinatario": "Worker03",
  "data": "2026-10-24T09:30:00-03:00",
  "link": "docs/adr/0027-registro-da-fila-e-append-only-mecanico.md",
  "tipo_ruling": "resposta",
  "registrado_por": null,
  "delegacao": null,
  "registrado_em": "2026-10-24T09:30:05-03:00"
}
```

- **Obrigatórios** (senão **422**, FR14): `pedido`, `escolha`, **`autor`** (só pessoa — decisão 1a) e
  **`destinatario`**. `registrado_em` sempre preenchido pelo servidor.
- `autor` é **gravado do formulário** (FR18): o servidor **não** infere autoria do agente que pediu,
  nem aceita o campo ausente para "preencher depois".
- `pedido` aceita o **id derivado** de portão do regente (`"072+T7"` — FR20).
- `tipo_ruling`: `resposta` | `devolucao`. "Devolver a quem pediu" é *ruling* **registrado** — não há
  "dispensar" (FR12).
- Delegação (Office): `registrado_por` = quem lançou e `delegacao` = referência ao registro que
  autoriza; **`autor` continua sendo a pessoa** (FR14/FR18 — a Office não substitui a autoria).

## Linha do registro JSONL (FR16)

Uma linha = um objeto JSON com `tipo` (`pedido` | `ruling`), campos em português. Append-only:
`painel/fila_registro.py` **só acrescenta** (`open(..., "a")`), nunca reescreve/reordena/remove.

```jsonl
{"tipo":"pedido","id":"D-014", ... ,"criado_em":"2026-10-24T07:04:00-03:00"}
{"tipo":"ruling","pedido":"D-014","escolha":"a","autor":"Darú","destinatario":"Worker03","data":"2026-10-24T09:30:00-03:00","registrado_em":"2026-10-24T09:30:05-03:00"}
```

Prova: `test_f14_registro_append_only_so_cresce` guarda o **prefixo de bytes** e confirma que ficou
inalterado (o arquivo só cresceu). Leitura tolerante: linha inválida é ignorada com aviso, sem derrubar
a fila.

## Item da fila devolvido por `GET /api/regencia/fila` (FR20)

```json
{
  "id": "072+T7",
  "origem": "portao",
  "chamado": "072",
  "gate": "TAIL:gate",
  "status": "pendente",
  "desde": "2026-10-24T06:12:00-03:00",
  "evidencia": "specs/072-painel-de-regencia/tasks.md",
  "somente_leitura": true,
  "idade": "há 1 h 02 min",
  "carimbo": "2026-10-24T06:12:00-03:00"
}
```

`origem: "portao"` distingue o item **derivado** do pedido registrado (`origem: "pedido"`). Um agente
recebe `somente_leitura: true` ("portão do regente"); o *ruling* aceita `"pedido": "072+T7"`.

## Cartão do kanban devolvido por `GET /api/regencia/kanban` (FR3–FR6)

```json
{
  "id": "072",
  "frente": "painel",
  "coluna": "G2",
  "dono": {"papel": "Runner", "sessao": "sess-07"},
  "veredito": "APROVE",
  "veredito_normalizado": "aprovado",
  "autor_da_peca": "Worker03",
  "por": "Worker07",
  "independencia": "builder != critico",
  "idade": "há 3 h 40 min",
  "carimbo": "2026-10-24T05:20:00-03:00",
  "selo_evidencia": "G2-vermelho-W13-6741315.md",
  "integrado_criticado": "não conferido",
  "data_fonte": "painel/chamados.py confere()"
}
```

- `veredito` **original** sempre ao lado de `veredito_normalizado` (anti-regra 6).
- `autor_da_peca` (FR5) ausente → `"—"` com motivo; iguais a `por` → marcador **vermelho** (FR4).
- `integrado_criticado` é **"não conferido"** até existir o script versionado de `git patch-id
  --stable` (FR6) — nunca verde.
- Todo número/selo carrega `data_fonte` (FR21); sem fonte → `"—"` e `motivo:` (FR22).
