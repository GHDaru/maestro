# Revisão em contexto fresco — rodada 3 do ciclo 073 (as 11 telas) e a mutação do gate

> **Data**: 2026-10-26 · **Ciclo**: 073 · **Rodada**: 3 · **Raia**: plena
> **Autor**: Worker02 — **revisor**, não autor de tela (nenhuma das 11 foi escrita por mim:
> é o que qualifica a revisão como independente, Teorema 2)
> **Base**: `af81499` (worktree `w/worker02`) · **Mandato**: `[[TASK 073-T3-revisao]]`, fechamento
> da rodada 3, em duas partes
>
> **Natureza**: **relato, não correção**. Nenhuma tela foi tocada. O script do gate foi alterado
> de propósito na Parte 2 e **restaurado byte a byte** (prova no §2.5).
>
> **Insumos**: `confronto/mapa-de-contextos.md` (§6, contexto dono de cada tela; §7, as cinco
> colisões de nome) · o contrato de marcação na *docstring* de `prototipo/verifica-prototipo.py`
> · as 11 telas de `prototipo/` · os dois fixtures, `fixtures/tela-ruim.html` e
> `fixtures/tela-bom.html`.
>
> **Limites respeitados**: sem `push`, sem `merge`, sem código de produto, sem segredo.
>
> **Siglas (Princípio VIII)**: ADR (*Architecture Decision Record* — registro de decisão de
> arquitetura) · CSS (*Cascading Style Sheets*) · DDD (*Domain-Driven Design* — desenho orientado
> a domínio) · HTML (*HyperText Markup Language*) · SHA-256 (*Secure Hash Algorithm*, 256 bits)
> · UX (*User Experience* — experiência de uso) · JSONL (*JSON Lines*).

---

## 0. O que li, e o que o gate já dizia

| Verificação | Resultado |
|---|---|
| `git status` antes de começar | limpo, `HEAD` em `af81499` |
| `python prototipo/verifica-prototipo.py` (base sã) | `-- verifica-prototipo: 11 screen(s), 0 finding(s)` · `EXIT=0` |
| Tamanho do corpus revisado | 11 telas (4 `mensageria-*`, 3 `administracao-*`, 4 `workflow-*`) |

O gate está **verde**. Toda a Parte 1, portanto, é sobre o que ele **não** alcança — cada achado
abaixo diz, na última coluna, se o gate o veria.

**Como a tela é julgada aqui.** Três réguas, nesta ordem:
1. **Contexto dono** (mapa §6): a tela fala a linguagem do contexto a que pertence, e não invade
   o vocabulário de outro (§6.1 é do método; §6.2 Chamados e Gates; §6.3 Workflow de sessões;
   §6.4 Regência; §6.5 Administração; §6.6 Mensageria).
2. **As cinco colisões de nome** (§7, linhas 292–296 do mapa): a prescrição do mapa é literal —
   *fila* é sempre **"fila de decisões"** ou **"fila (outbox)"**; o segundo *portão* é sempre
   **qualificado** ("portão do regente", e "portão do chamado" para o gate G0–G9); *caixa de
   entrada* é Mensageria e a tela *Fila* do painel é Regência; *livro de ponto* (o *task ledger*)
   é coisa distinta do *livro de mensagens*; **sessão** (execução) é distinta de **agente**
   (perfil registrado pela Administração).
3. **Contrato de marcação** (docstring do gate): `data-fonte` por bloco · `data-rotulo` com termo
   do glossário · `data-exemplo="true"` (e o "(exemplo)" visível) · `—` sempre com "motivo:" ·
   citação sob `data-fonte`/`data-referencia`.

---

## 1. Parte 1 — as 11 telas

### 1.1 Contexto dono — conferência de pertencimento (§6)

| Tela | Contexto dono declarado | Dono no mapa | Veredito |
|---|---|---|---|
| `mensageria-01-caixa-de-entrada.html` | Mensageria | §6.6 | conforme |
| `mensageria-02-livro-de-mensagens.html` | Mensageria | §6.6 | conforme |
| `mensageria-03-roteamento.html` | Mensageria | §6.6 | conforme |
| `mensageria-04-protocolo.html` | Mensageria | §6.6 | conforme |
| `administracao-catalogo.html` | Administração | §6.5 | conforme |
| `administracao-orcamento.html` | Administração | §6.5 | conforme |
| `administracao-politicas.html` | Administração | §6.5 | conforme |
| `workflow-01-sessao-de-agente.html` | Workflow de sessões | §6.3 | conforme |
| `workflow-02-estado-do-agente-vivo.html` | Workflow de sessões | §6.3 | conforme |
| `workflow-03-tarefa-aberta.html` | Workflow de sessões | §6.3 | conforme |
| `workflow-04-consumo-por-agente.html` | Workflow de sessões | §6.3 | conforme |

**Nenhuma tela invade o contexto alheio**, e nenhuma reivindica para si o *core domain*
(Chamados e Gates, mapa §5): as telas de Workflow descrevem o estado da sessão, não o gate do
chamado; as de Mensageria descrevem transporte, não decisão. A projeção do painel aparece
declarada como projeção, não como contexto (§2 do mapa) — coerente.

### 1.2 Achados — violação literal da letra do mapa ou do contrato

Numeração minha (R#), para o Gerente poder citar. **A coluna "gate vê?"** é o resultado do §2:
o gate é verde, então *nada* aqui é acusado — a coluna diz **por que**.

| # | Onde | O que diz | Regra ferida | Gate vê? |
|---|---|---|---|---|
| **R1** | `mensageria-01-caixa-de-entrada.html:78` | "A **fila** é *append-only*: a leitura é registrada…" | mapa §7 (*fila* nua) | não — é `<p>`, e a regra 4 só olha rótulos |
| **R1b** | `mensageria-01-caixa-de-entrada.html:75` | `data-fonte="… ADR 0027 — a **fila** recusa DELETE …"` | mapa §7 (*fila* nua) | não — a regra 4 nunca lê atributo |
| **R2** | `mensageria-04-protocolo.html:61` | "(o **portão** vira contrato)" | mapa §7 (*portão* nu) | não — é `<td>` |
| **R2b** | `administracao-politicas.html:105` | "ux-design 066 §3 (**portão do humano** aparece somente leitura ao agente)" | mapa §7: o par prescrito é *portão do chamado* / *portão do regente* | não |
| **R3** | `mensageria-03-roteamento.html:73`, `:74`, `:100` | "**fila outbox**" | mapa §7: a grafia é **"fila (outbox)"** | não |
| **R4** | `workflow-03-tarefa-aberta.html:52`, `:66`, `:71`, `:72`, `:73` | cita **`tasks.jsonl`** | o livro de ponto é `docs/records/tarefas.jsonl` (mapa §7, l.294); o arquivo `tasks.jsonl` **não existe** | não — sem verificação de existência |
| **R5** | `administracao-politicas.html:62`, `:92`, `:98`, `:110`, `:122`, `:123` | `hooks/guard-immutables.py` | o caminho real é `scripts/hooks/guard-immutables.py` | não |

**R1/R2 são exatamente o que a rodada 3 existia para pegar.** O mapa §7 prescreve a qualificação
literal, e as telas qualificam em todo lugar *menos* na prosa corrente e nos atributos — onde a
regra 4 do gate não chega (§2.3). Não é descuido de uma tela: é um ponto cego do instrumento.

**R3 é uma terceira grafia.** O mapa fixou "fila (outbox)"; a tela escreve "fila outbox" (sem
parênteses) três vezes. Pequeno, mas a razão de existir da §7 é *uma* grafia por conceito.

**R4 é o achado mais sério**, porque afirma um arquivo que não existe (`tasks.jsonl`) em cinco
lugares, incluindo a fonte da coluna `tentativas`. Pior: `workflow-03-tarefa-aberta.html:73`
cita **os dois nomes, um errado e um certo, no mesmo atributo** —
`data-fonte="método: tasks.jsonl (attempt=) e o histórico de despachos do tarefas.jsonl"`.
O mesmo arquivo acerta em `:102` (`tarefas.jsonl`) e `mensageria-02-livro-de-mensagens.html:32`,
`:38`, `:92` também acertam — logo é inconsistência, não desconhecimento.

**R5** repete o padrão: o símbolo existe, o caminho está truncado (`hooks/` em vez de
`scripts/hooks/`), seis vezes na mesma tela.

### 1.3 Achados — robustez e consistência (não violam a letra; o gate, por desenho, aceita)

| # | Onde | O que diz | Por que incomoda | Gate vê? |
|---|---|---|---|---|
| **R6** | as 3 telas `administracao-*` | marcam o valor ilustrativo com `class="exemplo"` e a palavra "(exemplo)" no texto — e usam **`data-exemplo` zero vezes** (contagem: 0 nas três, contra 10/16/4/17/10/10/13/13 nas outras oito) | é um **segundo dialeto de marcação**, tolerado pela regra 3 porque ela aceita a palavra "exemplo" no texto como fallback | sim, e passa |
| **R7** | `workflow-01-sessao-de-agente.html:89`, `:99`, `:109` · `workflow-02-estado-do-agente-vivo.html:79`, `:85`, `:91` | as células de **estado** ("trabalhando", "esperando", "sem tarefa") ficam sem marca de exemplo, enquanto **todas as células vizinhas da mesma linha** trazem `data-exemplo="true"` + "(exemplo)" | a regra 3 só fala de **número**; um estado ilustrativo nu deixa o leitor sem saber se é dado vivo ou exemplo — ambíguo, não ilegal | não — estado não é número |
| **R8** | `administracao-catalogo.html`, `administracao-orcamento.html`, `administracao-politicas.html` | são as **únicas 3 de 11** sem prefixo numérico, depois que `af81499` uniformizou `workflow-NN-` | a uniformidade foi decidida no ciclo e só chegou ao grupo do Workflow | irrelevante |
| **R9** | `workflow-01:80` e `:47` · `workflow-02:58`, `:71` e `:47` · `mensageria-01:65` · `mensageria-02:71` · `mensageria-03:62`, `:73`, `:74`, `:84`, `:95`, `:96`, `:100`–`:104` | no **mesmo rodapé**, umas citações são relativas ao ciclo (`confronto/…`, `pesquisa/…`) e outras à raiz do repositório (`docs/…`, `painel/…`, `scripts/…`, `specs/066-…`); e o mapa aparece como **`mapa-de-contextos.md` sem diretório** | duas bases de citação convivendo tornam a resolução ambígua para quem lê fora de `specs/073-…/` | não |

Não trato nenhum destes como violação: **R6 e R7 são escolhas que o contrato permite**; R8 e R9
são de forma. Ficam registrados porque o Gerente decide — não eu.

### 1.4 Examinados e **aceitos** (o que parecia achado e não é)

- **A tabela das cinco colisões dentro de uma tela de Mensageria**
  (`mensageria-03-roteamento.html:88`–`:107`): uma tela do contexto Mensageria exibindo a §7
  inteira poderia parecer invasão de contexto. Aceito: a tela **cita** o mapa como fonte
  (`data-fonte="método: mapa-de-contextos.md §7"`) e a coluna de significado remete cada nome ao
  dono; é leitura da §7, não reivindicação de vocabulário.
- **"Livro de ponto" e "Fila" escritos nus em `mensageria-02:102` e `mensageria-03:100`, `:102`**:
  aqui os termos são **o objeto da colisão** (nomear os dois sentidos é o propósito da tabela) e o
  mapa é citado como fonte. Aceito — qualificar seria contradizer a própria §7.
- **`administracao-politicas.html:105`, expressão "portão do humano"** aparece também em
  `ux-design 066 §3`, de onde a tela a copiou: registrado como R2b (terceiro qualificador) mas
  **não** como invenção da tela — a fonte é outra, e cabe ao Gerente decidir qual grafia prevalece.
- **`mensageria-01-caixa-de-entrada.html:85` citando `pesquisa/maestro-canvas.md`**: verificado
  byte a byte; o arquivo diz `pesquisa/maestri-canvas.md`, que existe. **Nenhum achado** — registrado
  porque foi a hipótese que eu levantei e descartei.

### 1.5 Veredito da Parte 1

Nenhuma tela viola o **contrato estrutural** (todos os interativos têm `data-fonte`; todo `—` tem
"motivo:"; todo rótulo de domínio declara `data-rotulo` com termo do glossário) nem o
**pertencimento de contexto**. Os achados são de **disciplina de nome e de citação**: 7 violações
literais (R1–R5) e 4 pontos de consistência (R6–R9). **Nenhuma delas o gate vê** — o que motiva a
Parte 2.

---

## 2. Parte 2 — mutação do gate (quebrar de propósito e mostrar o achado sumindo)

### 2.1 Mecânica

O gate varre `PROTO.glob("*.html")` e **pula** o que começa com `_` — logo o fixture em
`fixtures/` não é lido por ele. Para pôr o corpus ruim no alcance do gate, copiei
`prototipo/fixtures/tela-ruim.html` para `prototipo/zz-tela-ruim.html` (sem `_`, fora de
subdiretório), rodei, e ao final **tirei a cópia do repositório** (§2.5).

Backup do script antes de tudo: `%TEMP%\verifica-prototipo.worker02.bak.py`.
Hash de `verifica-prototipo.py` na base `af81499`:
`05445E13635D0278D7F06E0A2BF386057B55850F251E6A5B9DFF86BC9BB14653` (SHA-256).

### 2.2 ANTES — o corpus ruim acusado (5 achados)

```
FINDING: zz-tela-ruim.html: label outside the glossary: "Fila"
FINDING: zz-tela-ruim.html: "fila" unqualified (decisões or outbox?): "Fila"
FINDING: zz-tela-ruim.html: interactive <button> without data-fonte
FINDING: zz-tela-ruim.html: label outside the glossary: "Fluxo de caixa operacional"
FINDING: zz-tela-ruim.html: number without the "exemplo" mark: "42"
-- verifica-prototipo: 12 screen(s), 5 finding(s)
EXIT=1
```

### 2.3 Mutação A — cegar a regra 3 (número sem marca de exemplo)

Mudança de uma única expressão, na linha 168:

```python
# antes (af81499)
if NUMBER.search(stripped) and "exemplo" not in data.lower() \
# mutado
if NUMBER.search(stripped) and False \
```

Saída do gate mutado, mesmo corpus:

```
FINDING: zz-tela-ruim.html: label outside the glossary: "Fila"
FINDING: zz-tela-ruim.html: "fila" unqualified (decisões or outbox?): "Fila"
FINDING: zz-tela-ruim.html: interactive <button> without data-fonte
FINDING: zz-tela-ruim.html: label outside the glossary: "Fluxo de caixa operacional"
-- verifica-prototipo: 12 screen(s), 4 finding(s)
EXIT=1
```

**O achado que sumiu** (nome copiado da saída): `number without the "exemplo" mark: "42"`.
5 → 4. A regra 3 ficou cega de propósito e o número inventado passou.

### 2.4 Mutação B — cegar a regra 4 (termo de colisão nu)

Segunda mutação, na linha 201:

```python
# antes (af81499)
if re.search(r"\bfila\b", low) and "decis" not in low and "outbox" not in low:
# mutado
if False:  # MUTACAO rule 4 (fila)
```

Saída com o corpus ruim presente:

```
FINDING: zz-tela-ruim.html: label outside the glossary: "Fila"
FINDING: zz-tela-ruim.html: interactive <button> without data-fonte
FINDING: zz-tela-ruim.html: label outside the glossary: "Fluxo de caixa operacional"
FINDING: zz-tela-ruim.html: number without the "exemplo" mark: "42"
-- verifica-prototipo: 12 screen(s), 4 finding(s)
EXIT=1
```

**O achado que sumiu**: `"fila" unqualified (decisões or outbox?): "Fila"`.

E — o dado que importa — **com a regra 4 ainda cega e a cópia do fixture já fora do repositório**,
o corpus real de 11 telas deu:

```
-- verifica-prototipo: 11 screen(s), 0 finding(s)
EXIT=0
```

Idêntico ao resultado da base sã. **Nenhuma das 11 telas reais exercita a regra 4**; o fixture é
o único oráculo dela. É a explicação mecânica de por que R1/R2/R3 convivem com um gate verde: a
regra 4 é chamada só a partir de `check_label`, isto é, só sobre `<th>/<label>/<legend>/<h1>/<dt>`
ou elementos com `data-rotulo` — e nas telas reais a palavra nua vive em `<p>`, `<td>` e
atributos.

### 2.5 Restauração byte a byte (o gate não ficou alterado)

```
HASH_backup             05445E13635D0278D7F06E0A2BF386057B55850F251E6A5B9DFF86BC9BB14653
HASH_apos_restaurar     05445E13635D0278D7F06E0A2BF386057B55850F251E6A5B9DFF86BC9BB14653
HASH_af81499 esperado   05445E13635D0278D7F06E0A2BF386057B55850F251E6A5B9DFF86BC9BB14653
python verifica-prototipo.py  ->  11 screen(s), 0 finding(s)   EXIT=0
git diff (script)            ->  vazio
git status --porcelain       ->  vazio
```

- **Desvio declarado**: o mandate sugeria *remover* a cópia ao final. `Remove-Item` foi **negado
  por política de permissão** nesta sessão; usei `Move-Item` para tirar a cópia do repositório
  (ela está em `%TEMP%\zz-tela-ruim.worker02.html`). O efeito no repositório é o pedido —
  **nada rastreado, nada não rastreado**; `git status --porcelain` vazio o prova. Nada foi
  apagado do repositório.
- O script quebrado **não foi commitado** — só a evidência textual neste arquivo.

### 2.6 O que a mutação ensina (para além do exercício)

1. **O gate é verde porque as telas reais não o exercitam.** O único corpus que acusa algo é
   `fixtures/tela-ruim.html`. Se o fixture não roda em algum gate automático, o valor de
   regressão do script é zero: qualquer regra pode ser cegada sem que a suíte note (foi o que
   acabamos de demonstrar).
2. **A regra 4 é a mais frágil** — e é justamente a condição de ratificação que a rodada 3
   existia para cobrir. Cegá-la **não muda nada** no corpus real, enquanto as violações R1/R2/R3
   vivem fora do alcance dela.
3. **Cegar uma regra é invisível no sinal de saúde**: as duas mutações mantiveram `EXIT=1` no
   corpus com o fixture — porque *outras* regras seguiam acusando o mesmo arquivo. O sinal
   "verde/vermelho" não distingue "regra funcionando" de "regra cega com outra acusando por ela".

---

## 3. Recomendações ao Gerente (relato — a decisão é humana)

1. **Corrigir R1, R2, R3, R4, R5** nas telas, como achados de rodada 3: são violação direta da
   §7 do mapa (a razão de existir da rodada) e do contrato de citação. R4 é o mais sério
   (arquivo inexistente, citado 5×).
2. **Decidir a grafia única** antes de corrigir: o mapa prescreve "fila (outbox)" — adotar isso
   em `mensageria-03` (R3); e decidir se "portão do humano" sobrevive ou entra no par
   permitido do §7 (R2b), que hoje presume duas grafias.
3. **Estender a regra 4** (e o teste do contrato) a `<p>`/`<td>`/atributos, ou declarar no mapa
   que a disciplina de nome vale só em rótulos — hoje o instrumento promete mais do que mede.
4. **Pôr `tela-ruim.html` no alcance do gate** (renomear sem `_`, ou passar diretório por
   parâmetro) — senão a fitness function não tem oráculo (§2.6).
5. **R6/R7/R8/R9**: padronizar `data-exemplo="true"` no grupo Administração, marcar os estados
   ilustrativos, prefixar as 3 telas de Administração, e escolher **uma** base de citação.

**Não corrigi nada disso** — relato, conforme o mandato. As 11 telas não foram tocadas por esta
revisão.
