# Protótipo da área administrativa — telas × `ENTRA` × contexto dono × juízes (ciclo 073, rodadas 3 e 4)

> **O que é isto.** Wireframes **estáticos** das funcionalidades que a rodada 2 decidiu que **`ENTRA`**
> — as que **entram** na área administrativa — (`confronto/confronto-decisao.md`), desenhados sobre o
> **mapa de contextos delimitados**
> (`../confronto/mapa-de-contextos.md`). **Não é o produto**: nenhum arquivo desta pasta tem servidor,
> rota ou banco — é HTML parado, para o regente julgar a **feição** antes de alguém construir.
> **O contrato** — que o verificador desta pasta cobra (ver "Como estas telas são julgadas"): cada
> elemento interativo declara `data-fonte` (de onde a ideia veio, plataforma + URL da ficha ou
> requisito do método), todo rótulo de domínio é termo do glossário, e todo número vem marcado
> `exemplo` — **nenhum valor é inventado**. As medições datadas (25/10 e 26/10) estão declaradas
> abaixo: **hoje o verificador fecha verde**.

- **Ciclo**: 073 (área administrativa) · **Rodada**: 3 (wireframes) · **correções 1, 2 e 3 da rodada 4**
  (26–27/10) · **Fonte de verdade**: `confronto/confronto-decisao.md` (§ "ENTRA — 13", que esta página
  passa a ler como **16** depois das decisões 4 e 5)
- **Juízes (rodada 4)**: **controle** · **administração e gerenciamento de agentes** ·
  **intercomunicabilidade** — o bar dá nota **0 a 10 por peça** e só passa com os **três** em 9 ou mais.
- **Rodada 4 — correção 1 (26/10)**: as decisões da regente (`specs/073-area-administrativa/rodada-4/correcao-1.md`) mudam o que
  esta página afirmava em quatro pontos: **12 · auditoria administrativa** e **17 · custo estimado em
  dólar por agente** entram como `ENTRA` (decisão 4); a identidade de sessão passa a
  **`nome · ref · projeto`** (decisão 2); colisão de **termo** e colisão de **endereço** ficam
  separadas (decisão 3); e o **limite de orçamento é da Administração** (decisão 1) — a divergência
  que esta página declarava, resolvida. Os três pareceres frescos (`specs/073-area-administrativa/rodada-4/juiz-1..3-*.md`) deram
  **barra não atingida** (máximo 8 de 10).
- **Rodada 4 — correção 2 (26/10)**: a consolidação da regente
  (`specs/073-area-administrativa/rodada-4/correcao-2.md`) fecha o que restava e mexe em quatro pontos
  desta página: o **cadastro de agentes** vira `ENTRA` (**o 16º**, decisão 5) como **leitura do
  catálogo de perfis**; o verificador ganha a **regra 6** — o *roster* de exemplo e o **ref único por
  nome** dentro de cada tela (decisão 1); a ambiguidade de **endereço** continua **não verificada por
  script** (declarado abaixo); e a **citação de ficha passa a ser revalidada no mesmo commit que muda
  a ficha** (decisão 8, ver "Convenções").
- **Rodada 4 — correção 3 (27/10)**: a terceira leitura dos juízes deu **barra atingida no juiz 3**
  (16 peças em 9) e **não atingida nos juízes 1 e 2** (13 e 12 peças em 9) — o laço parou
  (`specs/073-area-administrativa/rodada-4/parada-do-laco.md`) e o **Darú reabriu**, com os três juízes
  de novo. Três decisões fixas mexem nesta página: **D1** — a matriz marca **por célula** (*corta*/*avisa*),
  não por coluna; **D2** — "ferramenta MCP" é **escopo da política**; **D3** — o **emissor do aviso** de
  teto está **desenhado**. O `ENTRA` **4 · limite de orçamento** passa a ser lido como **"declarar teto
  + avisar, com emissor desenhado"**. Detalhe na seção "Correção 3", abaixo.
- **Siglas** (Princípio VIII, expandidas na 1ª ocorrência): **ADR** (*Architecture Decision Record*),
  **A2A** (*Agent-to-Agent*), **MCP** (*Model Context Protocol*).

## As telas, uma a uma (telas × `ENTRA` × contexto dono × juízes)

| Tela (`prototipo/`) | `ENTRA` que serve (nº · nome na linguagem ubíqua) | Contexto dono | Grupo da matriz | Juízes | Estado |
|---|---|---|---|---|---|
| `mensageria-01-caixa-de-entrada.html` | 23 · **caixa de entrada** | Mensageria | INTERCOMUNICAÇÃO | Intercomunicabilidade | **neste ramo** |
| `mensageria-02-livro-de-mensagens.html` | 25 · **livro de mensagens** | Mensageria | INTERCOMUNICAÇÃO | Intercomunicabilidade | **neste ramo** |
| `mensageria-03-roteamento.html` | 24 · **roteamento por nome/ref** · 26 · **colisão de nomes** (visível) | Mensageria | INTERCOMUNICAÇÃO | Intercomunicabilidade | **neste ramo** |
| `mensageria-04-protocolo.html` | 22 · **protocolo de intercomunicação** · 21 · **mensagem entre agentes** | Mensageria | INTERCOMUNICAÇÃO | Intercomunicabilidade | **neste ramo** |
| `administracao-01-catalogo.html` | 9 · **catálogo de skills/ferramentas/modelos** · **cadastro de agentes** | Administração | ADMINISTRAÇÃO | Administração/Gerenciamento | **neste ramo** (`5ce4a5f`, Worker04) |
| `administracao-02-politicas.html` | 5 · **política declarativa (allow/deny/ask)** | Administração | CONTROLE | Controle · Administração/Gerenciamento | **neste ramo** (`5ce4a5f`, Worker04) |
| `administracao-03-orcamento.html` | 4 · **limite de orçamento** — *declarar teto + avisar, com emissor desenhado* (correção 3) | Administração | CONTROLE | Controle | **neste ramo** (`5ce4a5f`, Worker04) |
| `workflow-01-sessao-de-agente.html` | 1 · **sessão de agente** (subir/derrubar) | Workflow de sessões | CONTROLE | Controle · Administração/Gerenciamento | **neste ramo** (`365f59d`, Worker05) |
| `workflow-02-estado-do-agente-vivo.html` | 13 · **estado do agente vivo** | Workflow de sessões | GERENCIAMENTO | Administração/Gerenciamento · Controle | **neste ramo** (`365f59d`, Worker05) |
| `workflow-03-tarefa-aberta.html` | 14 · **tarefa aberta** | Workflow de sessões | GERENCIAMENTO | Administração/Gerenciamento | **neste ramo** (`365f59d`, Worker05) |
| `workflow-04-consumo-por-agente.html` | 16 · **consumo por agente** | Workflow de sessões | GERENCIAMENTO | Administração/Gerenciamento | **neste ramo** (`365f59d`, Worker05) |

**Os 16 `ENTRA` cabem em 11 telas** — cinco deles não têm tela própria de propósito:

- **21 · mensagem entre agentes** é o **objeto** que as quatro telas da Mensageria exibem (o remetente e
  o destinatário da caixa de entrada, a linha do livro, o consumo pelo protocolo). Coberto, não órfão.
- **26 · colisão de nomes** é **visível dentro** de `mensageria-03-roteamento.html`, como o motivo que
  aparece na linha do roteador — é uma condição que se mostra, não uma tela.
- **12 · auditoria administrativa** *(entra na correção 1)* — uma **seção "histórico de mudanças"** nas
  **três** telas da Administração: **quem mudou o quê**, com `changed_by`. O confronto dizia `NÃO
  PRECISA` (`specs/073-area-administrativa/confronto/confronto-decisao.md:53`); a decisão 4 a promove a `ENTRA` — o índice de decisões
  é append-only, mas a **mudança de chave, de papel ou de modelo** não tinha onde aparecer.
- **17 · custo estimado em dólar por agente** *(entra na correção 1)* — uma **coluna** em
  `workflow-04-consumo-por-agente.html`, com a fonte declarada (o **preço do modelo** no catálogo) e a
  marca **estimado**. O confronto dizia `NÃO PRECISA` (`specs/073-area-administrativa/confronto/confronto-decisao.md:63`).
- **cadastro de agentes** *(entra na correção 2, decisão 5; **o 16º `ENTRA`**)* — o cadastro **é o
  arquivo versionado** (o perfil: `.claude/agents/*.md`, `data-fonte: ls .claude/agents`); a tela
  **lista os perfis reais** — papel, ferramentas e modelo padrão — na seção **"Agentes (perfis)"** de
  `administracao-01-catalogo.html`, e liga ao roteamento. Não é tela nova: é **leitura** do catálogo
  de perfis. O confronto dizia `NÃO PRECISA`; a decisão 5 o promove a `ENTRA` (o administrador não
  tinha onde ver os perfis).

Os `ENTRA` novos das duas correções da rodada 4 — **12 · auditoria administrativa** e **17 · custo
estimado em dólar por agente** (correção 1, `specs/073-area-administrativa/rodada-4/correcao-1.md`) e
**cadastro de agentes** (correção 2, `specs/073-area-administrativa/rodada-4/correcao-2.md`) — entram
nas telas **já existentes** (a auditoria nas três da Administração, o dólar por agente em
`workflow-04`, os perfis no catálogo). A coluna "Estado" da tabela acima continua sendo o retrato do
topo `faca232`, medido em 26/10.

**A divergência do orçamento está resolvida (decisão 1).** O despacho da rodada 3 deu **4 · limite de
orçamento** e **5 · políticas allow/deny/ask** ao contexto **Administração**; a matriz do confronto as
punha no grupo **CONTROLE**, e esta página declarava as duas leituras sem escolher. A regente decidiu em
26/10: **o limite de orçamento é da Administração** — ela **define e guarda o teto**; o Workflow de
sessões apenas **mede e exibe o consumo contra o teto**. O mapa (§ 2, § 6.3 e § 6.5) é corrigido por
Worker02 nesta rodada; aqui, a coluna "Grupo da matriz" passa a ser lida como **grupo de
funcionalidade** (CONTROLE), nunca como contexto dono.

## Correção 3 (27/10) — as três decisões do Darú

A terceira leitura fechou o juiz 3 em **16/16 peças em 9** e manteve os juízes 1 e 2 abaixo da barra
(13 e 12 de 16) — `specs/073-area-administrativa/rodada-4/parada-do-laco.md`. Pela regra combinada, o
laço parava aí; o Darú decidiu **reabrir** uma correção 3, e as três decisões abaixo são fixas
(`specs/073-area-administrativa/rodada-4/correcao-3.md`). **Nada da Mensageria regride**: a cerca
`data-rotulo="colisão de nomes"` (decisão 7 da correção 2) e a regra 6 do verificador continuam como estão.

**D1 — a matriz marca por célula, não por coluna.** A linha **limites de orçamento e de taxa** da
matriz de plataformas **fica uma só** (a tabela fixa de 26 é mantida) e a **nota de coluna** "corta ×
avisa" (`specs/073-area-administrativa/pesquisa/plataformas.md:93-98`) vira **marca por célula**: cada
célula `sim`/`parcial` dessa linha ganha **`corta`** ou **`avisa`**, com a **fonte da ficha** ao lado.
Célula sem fonte para a distinção fica **`avisa?` com o motivo** — nunca um palpite. Quem escreve as
marcas é a Worker06; o confronto passa a **citar a marca**. Nesta página, "matriz" é outra coisa: a
coluna "Grupo da matriz" da tabela de telas é lida como **grupo de funcionalidade** (CONTROLE), nunca
como contexto dono.

**D2 — "ferramenta MCP" é escopo da política, não tela nova.** Quem pode chamar qual ferramenta **MCP**
é **escopo da política `allow`/`deny`/`ask` por agente** (`ENTRA` 5): a tela de políticas ganha a regra
de exemplo com escopo `ferramenta MCP` (`registrar_peca`: `ask` para Worker, `allow` para o regente por
delegação, `deny` para sessão de outro projeto) e a frase do `deny` **não sobrescritível** (o *guard* de
imutáveis) — Worker04; cada ferramenta de `mensageria-04-protocolo.html` **aponta para essa regra** —
Worker03; e o mapa § 6.5 lista a **política declarativa** como `ENTRA` da Administração — Worker02.
Termo novo no glossário: **ferramenta MCP como escopo de política**.

**D3 — o emissor do aviso de teto está desenhado.** O `ENTRA` **4** passa a ser lido como **"declarar
teto + avisar, com emissor desenhado"**. O emissor é a **ingestão de consumo do painel**
(`painel/custo.py`): compara o consumo medido com o **teto** e o **limiar** declarados na Administração
e, ao cruzar o limiar, **enfileira uma mensagem** na **fila (outbox)** endereçada à **sessão dona** e ao
**regente**, em **`nome · ref · projeto`**, com `data-fonte` apontando o módulo. A tela de orçamento
ganha a seção **"Quem emite o aviso"** (processo, gatilho, idade do relógio e o que acontece se a
ingestão estiver parada — *aviso atrasado, nunca perdido*) — Worker04; `workflow-04-consumo-por-agente.html`
e `mensageria-02-livro-de-mensagens.html` mostram uma **linha de exemplo** do aviso — Worker05 e Worker03.
O **corte** (recusar, suspender) continua **`DEPOIS`**. Termo novo no glossário: **emissor do aviso**
(*warning emitter*).

## Identidade de sessão: `nome · ref · projeto`

**Decisão 2 (correção 1).** Toda tela que cite uma sessão escreve as **três** partes — `nome · ref ·
projeto` — e, **onde houver ação**, o aviso de que **o `ref` muda ao reiniciar**. O motivo é este: o
**`nome`** sozinho não identifica, e o par **`nome · ref`** também não, porque **o `ListAgents` não
mostra o projeto** — duas sessões com o mesmo nome, em projetos diferentes, parecem o mesmo
interlocutor. O **`ref`** (referência curta da sessão: o `[xxxxxx]` que o `ListAgents` mostra ao lado do
nome) é o campo que resolve **e o único que expira**.

**Retrato datado — exemplo da forma, medido em 26/10/2026.** Os valores abaixo **não são cadastro**:
valem para este retrato e mudam no próximo reinício; o que fica é a **forma**.

| `nome` (do catálogo) | `ref` | `projeto` |
|---|---|---|
| `Gerente` (a sessão que despacha — "a regente", no vocabulário dos despachos) | `[31ee4d]` | `410_MAESTRO` |
| `Worker01` (esta) | `[9a1b27]` | `410_MAESTRO` |
| `Worker02` | `[31f7bf]` | `410_MAESTRO` |
| `Worker03` | `[ad66d6]` | `410_MAESTRO` |
| `Worker04` | `[4d000a]` | `410_MAESTRO` |
| `Worker05` | `[78d88f]` | `410_MAESTRO` |
| `Worker06` | `[c85948]` | `410_MAESTRO` |
| `MAESTRO` | `[7c8d05]` | `410_MAESTRO` |
| `Office` | — | **outro projeto** — **Hindiana** (`painel/custo.py:33-36`) |
| `Assistente` | — | **—** (nenhuma sessão viva com esse nome em 26/10) |

`projeto` é a pasta do projeto em `~/.claude/projects/` (a que o painel filtra: `painel/projetos/
exemplo.json:103`); a daqui é `C--Users-ghdaru-Documents-010-PROJETOS-410-MAESTRO`. `Office` e
`Assistente` são **nomes do catálogo** (a decisão 2 os lista; `painel/custo.py:33-36` é quem os mapeia)
e **não têm sessão viva neste projeto em 26/10** — por isso `—` **com o motivo**, e nunca um `ref`
inventado.

**Decisão 1 (correção 2): esta tabela é o *roster* único de exemplo de todas as telas.** Todo nome do
*roster* vem com o `ref` do *roster*, e **nenhum `ref` pertence a dois nomes na mesma tela** — as
sessões de outro projeto (a Hindiana Office) usam `ref` próprio e nunca um `ref` do *roster*. É o
*fixture* da **regra 6** (abaixo): os `ref`s acima são o **retrato de 26/10**, que segue os `ref`s de
então — não os novos das sessões de hoje.

**Regra 5 (entregue pela Worker02 na correção 1; já no script, v4).** O verificador exige
o `ref` no formato `[xxxxxx]` depois de toda menção a um nome do catálogo, **salvo** em tabela marcada
`data-rotulo="colisão de nomes"`.

**Regra 6 (correção 2, decisão 1; entregue pela Worker02).** O *roster* desta página vira lista no
script: dentro de uma tela, **um `ref` `[xxxxxx]` só aparece colado a um único nome**, e **todo nome do
*roster* vem com o `ref` do *roster*. É a regra que fecha a colisão *de exemplo* — `Worker01 [9a1b27]`
e `Worker03 [9a1b27]` na mesma tela deixam de passar. O *fixture* e a mutação acompanham.

## As colisões: de **termo** e de **endereço** (são duas coisas diferentes)

**Decisão 3 (correção 1).** As cinco colisões do mapa § 7 são de **termo**: a mesma **palavra** quer
dizer duas coisas em dois contextos. A dor que o protótipo desenha é outra — a **colisão de endereço**:
o mesmo **identificador** aponta para duas sessões, ou deixa de apontar para nenhuma. Termo se
**escreve qualificado**; endereço se **recusa**.

### Colisão de termo — cinco casos; o script trava dois

| Termo | O que é no contexto A | O que é no contexto B | Como desambiguar |
|---|---|---|---|
| `fila` | a **fila de decisões** (o `JSONL` — *JSON Lines* — da Regência) | a **fila (outbox)** (`SQLite` da Mensageria) | escrever sempre **`fila de decisões`** ou **`fila (outbox)`** |
| `caixa de entrada` | a tela **Fila** do painel (entrada de **decisões**, Regência) | a entrada de **mensagens** (Mensageria) | a do painel é Regência; "caixa de entrada" é Mensageria |
| `livro de ponto` | o **`Task ledger`** (`docs/records/tarefas.jsonl`) | o **livro de mensagens** proposto | `Task ledger` para o primeiro; `livro de mensagens` para o segundo |
| `sessão` × `agente` | hoje, sinônimos ("a sessão W04") | conceitos distintos: **sessão de agente** é a execução, **agente** é o perfil registrado | a Administração registra o **agente**; o Workflow acompanha a **sessão** |
| `portão` | o **gate do chamado** (`G0`–`G9`, derivado dos arquivos) | o **portão do regente** (`TAIL:gate`, item da fila) | o segundo é sempre **`portão do regente`** |

Fonte: `specs/073-area-administrativa/confronto/mapa-de-contextos.md` § 7 (`:292–296`). **O verificador
trava dois dos cinco** — `fila` e `portão`, pela regra 4 (abaixo); os outros três (`caixa de entrada`,
`livro de ponto`, `sessão × agente`) ficam com a revisão em contexto fresco: não são executáveis por
script hoje.

### Colisão de endereço — três classes; nenhuma é executável hoje

**Invariante (decisão 3): endereço ambíguo é recusado, nunca resolvido.** Quem resolve a ambiguidade
"por conta própria" entrega ao interlocutor errado — e entregar não se desfaz.

| Classe | O caso | Por que o endereço não se resolve sozinho |
|---|---|---|
| **nome em N `ref`s** | `Hindiana Office`: um nome, mais de uma sessão (juiz 3, P5) | o nome é de catálogo, não é identidade; só o `ref` separa |
| **nome em dois projetos** | `Gerente` em dois projetos (juiz 3, P5) | o `ListAgents` **não mostra o projeto** — dois "Gerente" parecem o mesmo |
| **`ref` obsoleto após reinício** | a sessão reinicia, o `ref` é outro; o antigo deixa de resolver | mensagem ou tarefa no `ref` antigo não chega — e o recibo de entrega (**ack**, *acknowledgement*) é `DEPOIS` (decisão 4), não existe hoje |

A **tabela de colisões de endereço** entra no mapa por Worker02, **separada** das cinco de termo
(decisão 3). **A ambiguidade de endereço continua não verificada por script** (decisão 1 da correção
2): o verificador ganha as **regras 5 e 6** — a identidade `nome · ref · projeto` e o **ref único por
nome** dentro de cada tela, com o *roster* no script — e isso cobre o sintoma mais comum (*o mesmo
`ref` em dois nomes na mesma tela*); as três classes acima (*nome em N refs*, *nome em dois projetos*,
*`ref` obsoleto após reinício*) seguem **fora do alcance da fitness function**. Fica **declarado** —
aqui e no mapa (§ 8).

Na `mensageria-03-roteamento.html` essa isenção é **concreta e declarada na própria tela**: a
**tabela de resolução nome → ref** traz o **nome nu como foi digitado** na coluna "nome pretendido"
(decisão 7) e está marcada `data-rotulo="colisão de nomes"` — é o ponto que o script **não** verifica,
e a tela o diz por escrito. Detalhe em "Convenções", abaixo.

## Onde cada tela entra na navegação do painel existente

O painel navega por grupos temáticos (`painel/index.html:216-240`): **Agora** (Board de agentes · Fluxo
de peças · Chamados e gates · Fila de decisões · Painel de regência) · **Planejamento** · **Medição** ·
**Controle** · **Conhecimento**.

**Regência e Chamados ficam exatamente como estão.** Nenhuma vista existente muda de lugar, de nome ou
de `data-v`: `chamados`, `fila`, `kanban`, `board`, `pecas`, `processo` e as demais seguem intactas
(`painel/index.html:955`). O protótipo **não** substitui nenhuma delas.

**A navegação entre as telas do protótipo (medido na pasta, 26/10).** Só as **três telas da
Administração** carregam a faixa de navegação entre si: um `<nav class="telas">` logo abaixo do título,
com os três **nomes de arquivo irmãos** (`administracao-01-catalogo.html:62-65`; igual nas outras duas),
e os `href` já atualizados na renomeação do R8. As **outras oito** telas não têm `href` nenhum — abrem
sozinhas, como documento. Fica **declarado** para o revisor não procurar o que não existe.

**Proposta para a rodada 4 (não decidida, e não implementada aqui):** um grupo novo —
**"Área administrativa"** — logo abaixo de *Agora*, com **uma entrada por contexto**, cada uma abrindo
as suas telas em abas: `Administração` (3), `Workflow de sessões` (4), `Mensageria` (4). O painel já tem
esse padrão de abas: o `chip` de vista de Chamados (`index.html:627`) e o carregamento preguiçoso da
vista BPMN (`:757`).

**A colisão que a navegação precisa respeitar.** A **caixa de entrada** (Mensageria — o que chegou para
uma **sessão** e ainda não foi lido ou drenado) **não é** a **Fila de decisões** (Regência — o que
espera **decisão do humano**). São dois depósitos, dois donos, dois `append-only`, e o mapa §7 (linha
293) fixa a distinção — está também na tabela de colisão de **termo**, acima. Duas entradas de menu com
"entrada" no nome **exigem o qualificador no rótulo** sob pena de a fitness function acusar `fila` sem
qualificador.

## Estado real das telas (declarado, com a data — 26/10)

| Contexto | Telas | Autor | Onde estão (medido no topo `af81499`) |
|---|---|---|---|
| Mensageria | 4 | Worker03 | **neste ramo** — `5f6dcf8` |
| Administração | 3 | Worker04 | **neste ramo** — `5ce4a5f` |
| Workflow de sessões | 4 | Worker05 | **neste ramo** — `365f59d` |

**São 11 telas na árvore hoje** (4 + 3 + 4); a tabela é o retrato datado de 26/10 — quem listar a pasta
vê o mesmo.

**A convenção de nome é uniforme hoje: as 11 telas usam `contexto-NN-slug.html`.** As três da
Administração foram renomeadas de `administracao-slug.html` para `administracao-01/02/03-…` na
integração da rodada 4 (achado R8, `6a32e24`), depois das quatro do Workflow, que a regente já
uniformizara no formato `NN-` (`af81499`). A frase anterior desta página — "a convenção **não é
uniforme**" — está **substituída** por esta: o que a mantinha verdadeira era só a pasta da
Administração, e ela mudou.

## Como estas telas são julgadas

```bash
python specs/073-area-administrativa/prototipo/verifica-prototipo.py
```

A fitness function (`verifica-prototipo.py`, v5 — regra 5 da Worker02 na correção 1 e **regra 6** na
correção 2) percorre os `*.html` e falha em **seis** regras:

1. elemento interativo **sem `data-fonte`** — onde a ideia foi achada;
2. **rótulo fora da allowlist** — o `docs/governance/glossary.md` **mais** os 12 termos ratificados
   (comparação com fronteira de palavra, para `RACI` não casar dentro de "ope**raci**onal"); o
   vocabulário de **moldura** da interface (v3: `tipo`, `regra`, `efeito`, `onde`, `vive`…) é stopword
   declarado — palavra de **domínio** nova não entra ali, ela ganha `data-rotulo` ou acusa;
3. **número sem a marca `exemplo`**, salvo em contexto de citação (`data-fonte`/`data-referencia`) ou
   dentro de sigla com dígito (`A2A`, `F1`, `T16`);
4. **termo de colisão sem qualificador** — `fila` sem *decisões*/*outbox*, `portão` sem
   *chamado*/*regente*. **Trava dois dos cinco** pares de termo do mapa § 7; os outros três
   (`caixa de entrada`, `livro de ponto`, `sessão × agente`) não são executáveis por script hoje;
5. **identidade de sessão** — toda menção a um nome do catálogo (`Gerente`, `WorkerNN`, `MAESTRO`,
   `Office`, `Assistente`) seguida do `ref` no formato `[xxxxxx]`, em todo texto visível e atributo,
   **salvo** em tabela marcada `data-rotulo="colisão de nomes"` — a cerca que a **regra 6** herda. A
   **tabela de resolução nome → ref** da `mensageria-03-roteamento.html` **está** marcada assim
   (decisão 7: o **nome nu digitado** na coluna "nome pretendido", as refs na coluna ao lado), com a
   isenção **declarada na própria tela**;
6. **roster e ref único por nome** — dentro de uma tela, um `ref` `[xxxxxx]` só aparece colado a um
   **único** nome, e todo nome do *roster* (a lista vive no script) vem com o `ref` do *roster*; o
   *fixture* e a mutação acompanham, com a **mesma cerca** da regra 5 (a tabela de resolução/colisão
   da `mensageria-03` fica isenta). É a **regra 6** (correção 2, decisão 1) — a fitness function
   cobre **este** sintoma de endereço; as três classes de colisão de **endereço** acima continuam
   **não verificadas por script**.

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

**Medido em 26/10, no topo `af81499`** (mesmo script v3): **11 telas · 0 achados — verde.** As duas
classes acima foram fechadas **só acrescentando atributos** — `data-referencia` nas citações e
`data-rotulo` nos `th` de domínio —, sem reescrever o conteúdo de nenhuma tela: as telas não estavam
erradas, o **contrato** é que não estava declarado.

**Remedido em 26/10, no topo `6a32e24`,** antes da correção 1 (mesmo script v3): **11 telas · 0
achados** — o verde atravessou a renomeação da Administração e a troca da base de citação. Depois da
correção 1 a regente fechou **11 telas · 0 achados com as cinco regras** (`specs/073-area-administrativa/done-073-correcao-1.md`).
A **correção 2** fechou em **11 telas · 0 achados com as seis regras** (`4e421a4`; a regra 6 pousou em
`2cd7d44`), e a **terceira leitura** dos juízes foi medida sobre esse topo (27/10). A próxima medição é a
do fechamento da **correção 3** — **seis** regras, sem regra nova.

## Convenções

**Base única de citação: todo caminho é relativo à raiz do repositório.** Vale para as 11 telas desta
pasta — é a mesma base que as telas do Workflow já seguiam. Nada de caminho relativo ao ciclo
(`confronto/…`, `pesquisa/…`) nem de nome solto de arquivo (`mapa-de-contextos.md`, `tasks.md`):

| A citação | Base antiga (errada) | Base única (certa) |
|---|---|---|
| o confronto do ciclo | `confronto/confronto-decisao.md` | `specs/073-area-administrativa/confronto/confronto-decisao.md` |
| a pesquisa do ciclo | `pesquisa/litellm.md` | `specs/073-area-administrativa/pesquisa/litellm.md` |
| o mapa de contextos | `mapa-de-contextos.md` | `specs/073-area-administrativa/confronto/mapa-de-contextos.md` |
| a decisão do confronto | `confronto-decisao.md` | `specs/073-area-administrativa/confronto/confronto-decisao.md` |
| as tarefas do ciclo | `tasks.md` | `specs/073-area-administrativa/tasks.md` |
| a spec do ciclo | `spec.md` | `specs/073-area-administrativa/spec.md` |

**Aplicada em 26/10** (achado R9 da revisão da rodada 3,
`specs/073-area-administrativa/revisao-073-rodada-3.md`): substituição **mecânica**, com **zero mudança
de conteúdo** — só a base do caminho mudou; cada caminho resultante foi conferido contra o disco.

**Citação de ficha é revalidada no mesmo commit que muda a ficha** (decisão 8 da correção 2). Toda
citação `arquivo:linha` a uma ficha de plataforma (`specs/073-area-administrativa/pesquisa/*.md`)
**anda com ela**: quem edita a ficha confere e corrige as linhas citadas — no `inventario-maestro.md`,
no `confronto-decisao.md` e nas telas — **no mesmo commit**. A `claude-code.md` deste ciclo é o caso
vivo: as linhas citadas andaram (`:47→:61`, `:49→:63`, `:65→:79`, `:68→:82`, `:71→:84`) e a citação
velha passou a apontar para outra coisa.

**A isenção da regra 5 — e da regra 6 — é declarada, não inferida.** A cerca que isenta a identidade
é um `<table>` cujo `th`/`dt` traz `data-rotulo="colisão de nomes"`. Ela cobre a **tabela de resolução
nome → ref** da `mensageria-03-roteamento.html`, onde a coluna "nome pretendido" mostra o **nome nu
como foi digitado** e as refs que casam ficam na coluna ao lado (decisão 7). Ali o nome sem `ref` é
**exigência do desenho**, não descuido — e a tela **declara a própria isenção** no texto. Fora dessa
cerca, a identidade `nome · ref · projeto` vale; as três classes de colisão de **endereço** seguem
fora do alcance da fitness function (ver a seção de colisões, acima).

> O corpo desta página ainda guarda as citações da redação original (as da coluna "base antiga" acima):
> na passagem do R9 elas não foram reescritas, para não colidir com a renomeação das telas da
> Administração, que se concluiu em `6a32e24`. **O que a correção 1 acrescentou — identidade, colisões,
> os dois `ENTRA` novos e a navegação — já nasce na base única.** Fechar a base do corpo inteiro é
> passagem própria, declarada aqui e **não** feita nesta rodada.

## Rastreabilidade

`spec 073` ↔ `specs/073-area-administrativa/tasks.md` (rodada 3) ↔
`specs/073-area-administrativa/confronto/confronto-decisao.md` (os `ENTRA`) ↔
`specs/073-area-administrativa/confronto/mapa-de-contextos.md` (contexto dono e as cinco colisões) ↔ as
telas desta pasta ↔ `specs/073-area-administrativa/prototipo/verifica-prototipo.py` (quem julga) ↔
`specs/073-area-administrativa/rodada-4/juiz-1..3-*.md` (os três pareceres frescos da 1ª rodada, barra não atingida) ↔
`specs/073-area-administrativa/rodada-4/correcao-1.md` (as seis decisões da regente e as fatias) ↔
`specs/073-area-administrativa/rodada-4/juiz-1..3-*-rodada-2.md` e
`specs/073-area-administrativa/rodada-4/correcao-2.md` (a segunda rodada de juízes e a correção 2) ↔
`specs/073-area-administrativa/rodada-4/juiz-1..3-*-rodada-3.md` e
`specs/073-area-administrativa/rodada-4/parada-do-laco.md` (a terceira leitura e a parada do laço) ↔
`specs/073-area-administrativa/rodada-4/correcao-3.md` (a correção 3 decidida pelo Darú) ↔ esta página.
