# Protótipo da área administrativa — telas × `ENTRA` × contexto dono × juízes (ciclo 073, rodada 3)

> **O que é isto.** Wireframes **estáticos** das funcionalidades que a rodada 2 decidiu que **`ENTRA`**
> — as que **entram** na área administrativa — (`confronto/confronto-decisao.md`), desenhados sobre o
> **mapa de contextos delimitados**
> (`../confronto/mapa-de-contextos.md`). **Não é o produto**: nenhum arquivo desta pasta tem servidor,
> rota ou banco — é HTML parado, para o regente julgar a **feição** antes de alguém construir.
> **O contrato** — que o verificador desta pasta cobra (ver "Como estas telas são julgadas"): cada
> elemento interativo declara `data-fonte` (de onde a ideia veio, plataforma + URL da ficha ou
> requisito do método), todo rótulo de domínio é termo do glossário, e todo número vem marcado
> `exemplo` — **nenhum valor é inventado**. Onde as telas de hoje ainda devem esse contrato, a
> medição de 25/10 está declarada abaixo.

- **Ciclo**: 073 (área administrativa) · **Rodada**: 3 (wireframes) · **Fonte de verdade**:
  `confronto/confronto-decisao.md` (§ "ENTRA — 13")
- **Juízes (rodada 4)**: **controle** · **administração e gerenciamento de agentes** ·
  **intercomunicabilidade** — o bar dá nota **0 a 10 por peça** e só passa com os **três** em 9 ou mais.
- **Siglas** (Princípio VIII, expandidas na 1ª ocorrência): **ADR** (*Architecture Decision Record*),
  **A2A** (*Agent-to-Agent*), **MCP** (*Model Context Protocol*).

## As telas, uma a uma (telas × `ENTRA` × contexto dono × juízes)

| Tela (`prototipo/`) | `ENTRA` que serve (nº · nome na linguagem ubíqua) | Contexto dono | Grupo da matriz | Juízes | Estado |
|---|---|---|---|---|---|
| `mensageria-01-caixa-de-entrada.html` | 23 · **caixa de entrada** | Mensageria | INTERCOMUNICAÇÃO | Intercomunicabilidade | **neste ramo** |
| `mensageria-02-livro-de-mensagens.html` | 25 · **livro de mensagens** | Mensageria | INTERCOMUNICAÇÃO | Intercomunicabilidade | **neste ramo** |
| `mensageria-03-roteamento.html` | 24 · **roteamento por nome/ref** · 26 · **colisão de nomes** (visível) | Mensageria | INTERCOMUNICAÇÃO | Intercomunicabilidade | **neste ramo** |
| `mensageria-04-protocolo.html` | 22 · **protocolo de intercomunicação** · 21 · **mensagem entre agentes** | Mensageria | INTERCOMUNICAÇÃO | Intercomunicabilidade | **neste ramo** |
| `administracao-catalogo.html` | 9 · **catálogo de skills/ferramentas/modelos** | Administração | ADMINISTRAÇÃO | Administração/Gerenciamento | **neste ramo** (`5ce4a5f`, Worker04) |
| `administracao-politicas.html` | 5 · **política declarativa (allow/deny/ask)** | Administração | CONTROLE | Controle · Administração/Gerenciamento | **neste ramo** (`5ce4a5f`, Worker04) |
| `administracao-orcamento.html` | 4 · **limite de orçamento** | Administração | CONTROLE | Controle | **neste ramo** (`5ce4a5f`, Worker04) |
| *(arquivo a declarar pelo Worker05)* | 1 · **sessão de agente** (subir/derrubar) | Workflow de sessões | CONTROLE | Controle · Administração/Gerenciamento | **não entregue** |
| *(idem)* | 13 · **estado do agente vivo** | Workflow de sessões | GERENCIAMENTO | Administração/Gerenciamento · Controle | **não entregue** |
| *(idem)* | 14 · **tarefa aberta** | Workflow de sessões | GERENCIAMENTO | Administração/Gerenciamento | **não entregue** |
| *(idem)* | 16 · **consumo por agente** | Workflow de sessões | GERENCIAMENTO | Administração/Gerenciamento | **não entregue** |

**Os 13 `ENTRA` cabem em 11 telas** — dois deles não têm tela própria de propósito:

- **21 · mensagem entre agentes** é o **objeto** que as quatro telas da Mensageria exibem (o remetente e
  o destinatário da caixa de entrada, a linha do livro, o consumo pelo protocolo). Coberto, não órfão.
- **26 · colisão de nomes** é **visível dentro** de `mensageria-03-roteamento.html`, como o motivo que
  aparece na linha do roteador — é uma condição que se mostra, não uma tela.

**Uma divergência declarada, entre o despacho e a matriz.** O despacho da rodada 3 deu **4 · limite de
orçamento** e **5 · políticas allow/deny/ask** ao contexto **Administração**; na matriz do confronto as
duas são do grupo **CONTROLE**. As telas seguem o despacho (autor e contexto dono); a coluna "grupo da
matriz" preserva a outra leitura. Não é erro de um dos dois — é a diferença entre **contexto dono** e
**grupo de funcionalidade**.

## Onde cada tela entra na navegação do painel existente

O painel navega por grupos temáticos (`painel/index.html:216-240`): **Agora** (Board de agentes · Fluxo
de peças · Chamados e gates · Fila de decisões · Painel de regência) · **Planejamento** · **Medição** ·
**Controle** · **Conhecimento**.

**Regência e Chamados ficam exatamente como estão.** Nenhuma vista existente muda de lugar, de nome ou
de `data-v`: `chamados`, `fila`, `kanban`, `board`, `pecas`, `processo` e as demais seguem intactas
(`painel/index.html:955`). O protótipo **não** substitui nenhuma delas.

**Proposta para a rodada 4 (não decidida, e não implementada aqui):** um grupo novo —
**"Área administrativa"** — logo abaixo de *Agora*, com **uma entrada por contexto**, cada uma abrindo
as suas telas em abas: `Administração` (3), `Workflow de sessões` (4), `Mensageria` (4). O painel já tem
esse padrão de abas: o `chip` de vista de Chamados (`index.html:627`) e o carregamento preguiçoso da
vista BPMN (`:757`).

**A colisão que a navegação precisa respeitar.** A **caixa de entrada** (Mensageria — o que chegou para
uma **sessão** e ainda não foi lido ou drenado) **não é** a **Fila de decisões** (Regência — o que
espera **decisão do humano**). São dois depósitos, dois donos, dois `append-only`, e o mapa §7 (linha
293) fixa a distinção. Duas entradas de menu com "entrada" no nome **exigem o qualificador no rótulo**
sob pena de a fitness function acusar `fila` sem qualificador.

## Estado real das telas (declarado, com a data — 25/10)

| Contexto | Telas | Autor | Onde estão (medido no topo `20f352c`) |
|---|---|---|---|
| Mensageria | 4 | Worker03 | **neste ramo** — `5f6dcf8` |
| Administração | 3 | Worker04 | **neste ramo** — `5ce4a5f` |
| Workflow de sessões | 4 esperadas | Worker05 | **em entrega** — nomes de arquivo ainda não declarados |

**São 7 telas na árvore hoje** (4 + 3); a tabela é o retrato datado de 25/10 — quem listar a pasta vê o
mesmo. As quatro do Workflow entram na próxima integração e passam a ocupar as linhas "não entregue" da
tabela acima.

A convenção de nome **não é uniforme** hoje — `mensageria-NN-slug.html` (com ordem) contra
`administracao-slug.html` (sem ordem). Fica **declarado** aqui em vez de silenciado; renomear arquivo de
outro worker não é decisão minha, e o Worker05 ainda vai escolher a sua.

## Como estas telas são julgadas

```bash
python specs/073-area-administrativa/prototipo/verifica-prototipo.py
```

A fitness function (`verifica-prototipo.py`, v3 — `da85def`) percorre os `*.html` e falha em quatro
regras:

1. elemento interativo **sem `data-fonte`** — onde a ideia foi achada;
2. **rótulo fora da allowlist** — o `docs/governance/glossary.md` **mais** os 12 termos ratificados
   (comparação com fronteira de palavra, para `RACI` não casar dentro de "ope**raci**onal"); o
   vocabulário de **moldura** da interface (v3: `tipo`, `regra`, `efeito`, `onde`, `vive`…) é stopword
   declarado — palavra de **domínio** nova não entra ali, ela ganha `data-rotulo` ou acusa;
3. **número sem a marca `exemplo`**, salvo em contexto de citação (`data-fonte`/`data-referencia`) ou
   dentro de sigla com dígito (`A2A`, `F1`, `T16`);
4. **termo de colisão sem qualificador** — `fila` sem *decisões*/*outbox*, `portão` sem
   *chamado*/*regente*.

**Medido em 25/10, no topo `20f352c`** (script v3): **7 telas · 45 achados**, e **só duas classes**:

| Regra | Achados | Onde |
|---|---|---|
| **3** · número sem a marca `exemplo` | **40** | 22 nas 4 telas da Mensageria · 18 nas 3 da Administração |
| **2** · texto de `th`/`label` sem `data-rotulo` | **5** | todas nas telas da Administração (`Teto`, `Consumo`, `Restante`, `Efeito ao estourar`, `Administração — política declarativa (allow/deny/ask)`) |
| **1** · elemento interativo sem `data-fonte` | **0** | — |
| **4** · termo de colisão sem qualificador | **0** | — |

E **zero** `data-rotulo` fora do glossário: **onde o rótulo foi declarado, ele resolve**. Os 40 de
regra 3 são **texto de citação solto no rodapé** (ex.: `specs/066-painel-de-regencia/ux-design.md`,
`mcp_painel.py:26-27`): nasceram com as telas e são **alheios ao glossário** — a contagem é a mesma com
o glossário anterior e com o de agora (**22 = 22** nas telas da Mensageria). As **duas classes já estão
despachadas** às telas (attempt=2: contrato de citação via `data-fonte`/`data-referencia`, e
`data-rotulo` nos `th` de domínio) — o verde é esperado antes do fechamento. A saída colada fica no
`../qa-report.md`.

## Rastreabilidade

`spec 073` ↔ `../tasks.md` (rodada 3) ↔ `confronto/confronto-decisao.md` (os 13 `ENTRA`) ↔
`../confronto/mapa-de-contextos.md` (contexto dono e as cinco colisões) ↔ as telas desta pasta ↔
`verifica-prototipo.py` (quem julga).
