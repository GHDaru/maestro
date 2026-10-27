# Data model 074 — as fixtures do protótipo navegável (um JSON por agregado do mapa)

> Artefato condicional declarado no plano (`ART:data-model=yes`). Descreve **o dado novo**
> deste ciclo: as fixtures de `prototipo/fixtures/*.json` — **um JSON (JavaScript Object
> Notation) por agregado do mapa** de contextos (sessão, tarefa, chamado, pedido de decisão,
> mensagem, política, orçamento, catálogo). Este arquivo é o **contrato**: os valores abaixo
> são **fixados na autoria** e as fatias de telas (074-T03–T06) e a fatia de fixtures (074-T07)
> não divergem — quem renderiza usa exatamente o que está aqui. Nomes de campo em
> **português** (dado do produto, como o `docs/records/decisoes.jsonl`); o glossário é em
> inglês (ADR — *Architecture Decision Record* — 0014).
>
> Siglas (Princípio VIII, expandidas na 1ª ocorrência): JSON (*JavaScript Object Notation*),
> FR (*functional requirement*, requisito funcional), ENTRA (as funcionalidades que **entram** —
> veredicto do confronto do 073), ISO 8601 (formato de data da *International Organization for
> Standardization*).

## 0. Regras de identidade e marcação (valem para os oito arquivos)

1. **Projeto**: `maestro` — o valor de `repos[0].nome` de `painel/projetos/exemplo.json`
   (`:27`), **em toda tela** (FR5, S6). Declarado **diferente** do `410_MAESTRO` do roster
   datado do 073 (que é o nome da pasta do projeto em `~/.claude/projects/`, o retrato de
   26/10); as fixtures do 074 seguem o valor do campo `repos` (S-b do gate de UX).
2. **Roster de exemplo** (refs do retrato datado do 073,
   `specs/073-area-administrativa/prototipo/README.md` — **dados de fixture, nunca os refs
   vivos das sessões de hoje**): `Gerente [31ee4d]` · `Worker01 [9a1b27]` · `Worker02 [31f7bf]`
   · `Worker03 [ad66d6]` · `Worker04 [4d000a]` · `Worker05 [78d88f]` · `Worker06 [c85948]` ·
   `MAESTRO [7c8d05]` — todos `· maestro`. A identidade em todo texto visível e atributo é
   **`nome · ref · projeto`** (regra 5 do verificador do 073).
3. **Office e Assistente** (nomes de catálogo sem sessão viva neste projeto) só aparecem
   **dentro da tabela de colisão** do roteamento — a cerca
   `data-rotulo="colisão de nomes"` isenta a tabela das regras 5 e 6, e é lá que a colisão é
   o **conteúdo** (mapa §7.1: "Office" em refs de outro projeto). Nas listas de sessão do
   Workflow, **só o roster do projeto `maestro`** — Office/Assistente ficam de fora (outro
   projeto / sem sessão viva), e o motivo é declarado, nunca um ref inventado fora da cerca.
4. **Autor humano**: `Ana Exemplo` (`painel/projetos/exemplo.json`, `regencia.pessoas` —
   `:40`). **Nenhum dado pessoal real** em qualquer fixture.
5. **Números**: todo número é fixture marcada **`(exemplo)`** ou vem de
   `painel/projetos/exemplo.json` com `data-fonte` (FR5). Ids de chamado (`072`, `073`, `074`)
   e refs (`[xxxxxx]`) são **referência**, não métrica — na tela vêm em contexto de citação
   (`data-fonte`/`data-referencia`) ou com a marca, como as telas do 073 já fazem.
6. **`—` sempre com motivo** (regra F8 do 066): célula vazia é informação declarada, nunca
   valor padrão.
7. **Derivação na autoria** (S3 do gate de spec): o que **existe** em
   `painel/projetos/exemplo.json` vem com `data-fonte` apontando a origem; o que não existe é
   **fixture `(exemplo)`** com `data-fonte` apontando à origem **estrutural** — o
   `painel/schema_workflow.sql`, o `painel/regencia/`, o data-model do 072 e o mapa §7.1. As
   fixtures são **estáticas**: derivadas uma única vez, na autoria — o protótipo não lê
   `../painel` em runtime (FR6, offline).
8. **Meta de arquivo**: cada JSON começa com o objeto de declaração —
   `"_fonte": "<origem>"`, `"_exemplo": true`, `"projeto": "maestro"` — o equivalente em dado
   do `data-fonte` das telas.
9. **Efeitos são só em memória** (FR4): nenhuma ação de escrita altera estes arquivos; o
   `app.js` carrega as fixtures para o estado em memória e recarregar restaura.

## 1. `sessao.json` — agregado Sessão de agente (Workflow de sessões)

`DOM:aggregate=sessao` — a unidade de administração: uma execução de agente que o humano
sobe, acompanha, reinicia e derruba. **Fonte estrutural**: o roster datado do 073 (identidade
e refs) e `painel/projetos/exemplo.json` (equipes, `repos[0].nome`).

| Campo | Tipo | O que é |
|---|---|---|
| `nome` | texto | nome do catálogo (`Gerente`, `WorkerNN`, `MAESTRO`) |
| `ref` | texto | `[xxxxxx]` do roster de exemplo — o campo que resolve e o único que expira |
| `projeto` | texto | `maestro` em toda linha |
| `estado` | texto | `trabalhando` · `esperando` · `bloqueado` · `sem tarefa` · `sem sinal` |
| `desde` | texto (ISO 8601) | carimbo do estado — a idade sai daqui, nunca digitada |
| `aviso_ref` | texto | "o ref muda ao reiniciar" — obrigatório onde houver ação sobre a sessão |

**Fixture (exemplo)**: `Gerente [31ee4d] · maestro` esperando · `Worker01 [9a1b27] · maestro`
trabalhando · `Worker02 [31f7bf] · maestro` trabalhando · `Worker03 [ad66d6] · maestro`
bloqueado (motivo: aguarda ruling do pedido `D-014`) · `Worker04 [4d000a] · maestro` sem
tarefa (motivo: nenhuma tarefa com `start` sem `stop`) · `Worker05 [78d88f] · maestro`
trabalhando · `Worker06 [c85948] · maestro` esperando · `MAESTRO [7c8d05] · maestro` esperando.

**Invariantes**: identidade `nome · ref · projeto` em todo texto visível e atributo; um ref
só aparece colado a um único nome dentro de cada tela (regra 6 do 073); **o Gerente nunca é
derrubável** — a linha dele não carrega o botão e mostra o aviso "portão do regente" (B2-h;
é regra de tela declarada aqui para o fixture saber); reiniciar e derrubar são irreversíveis
com confirmação `data-perde`/`data-reverte`.

## 2. `tarefa.json` — agregado Tarefa aberta (Workflow de sessões)

`DOM:aggregate=tarefa` — a tarefa ativa por agente: `start` sem `stop`. **Fonte estrutural**:
`painel/schema_workflow.sql` (tabela `passos`) e `docs/governance/task-ledger.md`
(`[[TASK]]`/`[[DONE]]`).

| Campo | Tipo | O que é |
|---|---|---|
| `sessao` | texto | `nome · ref · projeto` de quem executa |
| `tarefa_id` | texto | id no padrão do ledger (`074-T03`) |
| `kind` | texto | do vocabulário fechado (`implement`, `docs`, `test`…) |
| `cycle` | texto | `074` |
| `inicio_em` | texto (ISO 8601) | quando entrou no passo (a idade deriva daqui) |
| `resumo` | texto | o que está fazendo — ou `—` com o motivo |

**Fixture (exemplo)**: `Worker01 [9a1b27] · maestro` em `074-T03` (implement); `Worker02
[31f7bf] · maestro` em `074-T02`; `Worker05 [78d88f] · maestro` em `074-T06`; `Worker03
[ad66d6] · maestro` — `—` (motivo: bloqueado, aguarda ruling do pedido `D-014`); `Worker04
[4d000a] · maestro` — `—` (motivo: nenhuma tarefa aberta); `Worker06 [c85948] · maestro` —
`—` (motivo: sem fatia de implementação neste retrato); `MAESTRO [7c8d05] · maestro` — `—`
(motivo: o regente decide e julga, não executa fatia); `Gerente [31ee4d] · maestro` — `—`
(motivo: integra e despacha, não executa fatia).

**Invariantes**: um `start` sem `stop` por agente; um passo sem saída bloqueia a entrada do
próximo (`schema_workflow.sql`); `—` sempre com motivo.

## 3. `chamado.json` — agregado Chamado (Chamados e Gates — core domain)

`DOM:aggregate=chamado` — a pasta `specs/<id>/` com seus portões; o kanban **projeta** (o
estado do portão é **derivado**, nunca digitado). **Fonte estrutural**: `painel/chamados.py`
(o conferidor, `GATES`) e o data-model do 072 §4 (a projeção do kanban); frentes de
`painel/projetos/exemplo.json` (`frentes`: `painel`, `administrativa`).

| Campo | Tipo | O que é |
|---|---|---|
| `id` | texto | a pasta do chamado (`072`) — referência, não métrica |
| `frente` | texto | `painel` · `administrativa` (de `exemplo.json`) |
| `gate` | texto | `G0`…`G9` — derivado dos arquivos |
| `veredito_original` | texto | o cabeçalho como está no arquivo |
| `veredito_normalizado` | texto | o canônico — **ao lado** do original, nunca no lugar |
| `idade` | texto | do carimbo (`há 7 h (exemplo)`) — nunca digitada |
| `dono` | texto | `nome · ref · projeto`, ou `—` com motivo |
| `autor_da_peca` / `por` | texto | iguais → marcador vermelho (builder ≠ crítico); sem → `—` |
| `selo_evidencia` | texto | o selo do cabeçalho do gate |
| `portao_do_regente` | booleano | o marcador laranja (G7/G8) — leva à Fila, é somente leitura |

**Fixture (exemplo)** — três cartões para o kanban: `072` (frente `painel`) parado em **G3**,
veredito original `DEVOLVIDO` / normalizado `devolvido`, idade `há 7 h (exemplo)`, dono
`Worker01 [9a1b27] · maestro`, `autor_da_peca ≠ por` (marcador) — é o cartão do passo 3 de J2
("Detalhar" como expansão na própria tela, B-UX2); `073` (frente `administrativa`) em **G7**
com `portao_do_regente: true` (o marcador leva à Fila — passo 4 de J2), idade `há 2 h
(exemplo)`; `074` (frente `painel`) em **G0**, idade `há 1 h (exemplo)`.

**Invariantes**: a tela **nunca promove** (o estado do gate é derivado); o veredito
normalizado aparece **ao lado** do original; o portão do regente é item somente leitura da
fila, nunca botão de aceite no cartão.

## 4. `pedido-de-decisao.json` — agregado Pedido de decisão (Regência; Ruling dentro)

`DOM:aggregate=pedido-de-decisao` — a raiz da fila; o **Ruling** é entidade **dentro** do
pedido (um ruling não existe sem o pedido que ele fecha — data-model do 072 §1). **Fonte
estrutural**: `specs/072-painel-de-regencia/data-model.md` §1 e
`painel/projetos/exemplo.json` (`regencia.pessoas`, `fila_decisoes`).

| Campo | Tipo | O que é |
|---|---|---|
| `id` | texto | `D-012`, `D-013`, `D-014` |
| `pedido_por` | texto | quem pediu — sessão em `nome · ref · projeto` |
| `pergunta` | texto | a pergunta escalada ao humano |
| `opcoes` | lista `{id, descricao}` | as alternativas (chips selecionáveis no ruling) |
| `recomendacao` | texto | de **quem pediu** — nunca do painel (anti-regra 2 do 066) |
| `prazo` | texto (ISO 8601) | quando estoura; entra na ordenação |
| `destrava` | lista de textos | chamados/sessões presos que isto solta |
| `destino` | texto | para quem volta a resposta |
| `status` | texto | `aguardando` enquanto não houver ruling |
| `criado_em` | texto (ISO 8601) | a idade sai daqui (`há 7 h (exemplo)`) |
| `rulings` | lista | vazio na fixture; o ruling nasce do "Registrar ruling" |

**Fixture (exemplo)** — **três** pedidos (a frase-chave de J1: "você tem 3 decisões
esperando, a mais velha há 7 h (exemplo)"): `D-012` criado há 2 h (exemplo), prazo ok;
`D-013` criado há 4 h (exemplo), prazo ok; **`D-014`** criado há **7 h (exemplo)**,
**prazo estourado** (borda esquerda `--erro`), pedido por `Worker03 [ad66d6] · maestro`,
destrava `["073"]` — é o pedido mais velho, o do CTA "Responder" (J1) e o do
`aria-label` "responder pedido D-014 (exemplo)".

**Invariantes**: ruling **sem autor humano ou sem destino é recusado**; o autor tem de estar
em `regencia.pessoas` (`Ana Exemplo`); pergunta sem ruling **nunca sai da fila**; "Registrar
ruling" tira o pedido da fila e o contador da frase-chave passa a **2** (J1 passos 5–6);
"Propor regra" da Administração **nasce** aqui como pedido novo (mapa, relação 5 — propor
não executa).

## 5. `mensagem.json` — agregado Mensagem (Mensageria)

`DOM:aggregate=mensagem` — a linha da fila (outbox): troca **endereçada** entre sessões, por
artefato/outbox, não por chat. **Fonte estrutural**: `painel/schema_workflow.sql` (tabela
`fila`) e `painel/fila_outbox.py`.

| Campo | Tipo | O que é |
|---|---|---|
| `id` | número | da tabela `fila` |
| `sessao_origem` | texto | `nome · ref · projeto` |
| `sessao_destino` | texto | `nome · ref · projeto` — endereço ambíguo é recusado |
| `payload` | texto | o texto da mensagem |
| `criada_em` | texto (ISO 8601) | quando entrou na fila |
| `lida_em` | texto (ISO 8601) ou `null` | `null` = não lida (o ponto laranja da caixa de entrada) |

**Fixture (exemplo)** — **três não lidas** (J5 passo 1): duas para `Worker03 [ad66d6] ·
maestro` (de `Worker01 [9a1b27] · maestro` e de `Gerente [31ee4d] · maestro`) e uma para
`Worker05 [78d88f] · maestro` (de `Worker02 [31f7bf] · maestro`); mais duas **lidas** (o
registro do livro de mensagens). "Drenar outbox" preenche o `lida_em` das não lidas da sessão
e zera o contador (J5 passo 2); a linha drenada **permanece** no livro (append-only).

**Invariantes**: a fila recusa `DELETE` e só aceita o fechamento da leitura (`lida_em`,
`schema_workflow.sql`); **endereço ambíguo é recusado, nunca resolvido** — a confirmação
irreversível (`data-perde`/`data-reverte`) **antecede** a recusa com pedido de desambiguação
(J5 passos 4–5); a resolução é só pelo ref (`nome · ref · projeto`), nunca "o mais provável".

## 6. `politica.json` — agregado Política declarativa (Administração)

`DOM:aggregate=politica` — a política declarativa allow/deny/ask por projeto: a Administração
**declara**; a execução é do harness (mapa §2 — o ponto de execução do controle está fora dos
cinco contextos). **Fonte estrutural**: `.claude/settings.json` (blocos
`permissions.allow`/`ask`/`deny`).

| Campo | Tipo | O que é |
|---|---|---|
| `projeto` | texto | `maestro` |
| `bloco` | texto | `allow` · `deny` · `ask` |
| `regra` | texto | a regra declarada (ex.: `Bash(git push*)` no bloco `ask`) |
| `histórico` | lista `{mudanca, changed_by, data}` | a auditoria administrativa (ENTRA 12) |

**Fixture (exemplo)**: `allow` — leitura de docs do repositório; `ask` — `Bash(git push*)`;
`deny` — `Bash(rm -rf*)`. Uma linha de fixture do histórico visível ao crítico: "deny
`Bash(rm -rf*)` ajustado por `Ana Exemplo` em 2026-10-20 (exemplo)" (`changed_by`).

**Invariantes**: propor regra **não executa** — a proposta vira pedido de decisão (J4 passo
3); autorização vive **fora** do modelo; a tela mostra o histórico (quem mudou o quê).

## 7. `orcamento.json` — agregado Limite de orçamento (Administração)

`DOM:aggregate=orcamento` — o teto **declarado** pelo administrador, por projeto/agente/modelo;
o Workflow **obedece** e **mede** (mapa §2, correção 1 decisão 1). **Fonte estrutural**:
`painel/projetos/exemplo.json` (`custo_pastas`) e `painel/custo.py` (a medição); a barra e as
etiquetas são do design system §4.

| Campo | Tipo | O que é |
|---|---|---|
| `projeto` | texto | `maestro` |
| `escopo` | texto | `projeto` · `agente` · `modelo` (o teto é por escopo) |
| `teto` | número | o limite **declarado** — etiqueta "declarado" |
| `consumo` | número | o consumo **medido** contra o teto — etiqueta "medido" |
| `periodo` | texto | `hoje` · `semana` · `mês` (o segmento da tela de consumo) |
| `histórico` | lista `{mudanca, changed_by, data}` | a auditoria (ENTRA 12) |

**Fixture (exemplo)**: teto **80.000.000 tokens/mês (exemplo)**, consumo medido **61.400.000
(exemplo)** — 77 %, barra em `--grafico-2` (até 80 % do teto). "Ajustar teto" para
**60.000.000 (exemplo)** recalcula para 102 % — a barra passa a `--erro` — e acrescenta
**nova linha no histórico** (`changed_by: Ana Exemplo`). O bloco "Efeito ao estourar" carrega
`data-perde`/`data-reverte` (é uma das quatro ações irreversíveis).

**Invariantes**: a barra é `--grafico-2` até 80 % do teto, `--primaria` até 100 %, `--erro`
acima (design system §4); o número é **medido** com etiqueta — nunca apresentado como
declarado; estourar teto é irreversível com confirmação.

## 8. `catalogo.json` — agregado Catálogo (Administração)

`DOM:aggregate=catalogo` — o registro **consultável** de skills, ferramentas e modelos por
projeto, **mais** os perfis de agentes (o ENTRA da correção 2 do 073: o cadastro **é o
arquivo versionado** — `.claude/agents/*.md` — e a tela **lê**). **Fonte estrutural**:
`skills/` (pastas), `.claude/agents/` (perfis), `docs/agents/README.md` (perfil ↔ executável).

| Campo | Tipo | O que é |
|---|---|---|
| `projeto` | texto | `maestro` |
| `skills` | lista `{nome, arquivo}` | as skills do repositório |
| `ferramentas` | lista `{nome, origem}` | as ferramentas que um agente pode usar |
| `modelos` | lista `{nome, preco_por_milhao, estimado}` | o modelo por sessão e o **preço** — a fonte do custo estimado (ENTRA 17) |
| `agentes_perfis` | lista `{perfil, papel, ferramentas, modelo_padrao}` | a leitura de `ls .claude/agents` |
| `histórico` | lista `{mudanca, changed_by, data}` | a auditoria (ENTRA 12) |

**Fixture (exemplo)**: skills do repositório (`anti-patterns`, `constitution-check`,
`diagnose-before-fix`, `fight-the-pile-up`, `living-journey`, `verifiable-dod`) com
`data-fonte: skills/`; perfis reais com `data-fonte: ls .claude/agents`; preço do modelo
marcado **estimado** (é a fonte declarada da coluna "estimado" do consumo por agente); uma
linha de fixture do histórico visível ao crítico.

**Invariantes**: o cadastro é o arquivo versionado; a tela **lê** (não cadastra); toda
afirmação do registro tem invariante que a verifica; o dólar por agente é **estimado** com a
fonte (preço do modelo) declarada.

## 9. Relações (entre agregados de fixture)

```text
Sessão 1 ──< Tarefa aberta            (start sem stop; um passo sem saída bloqueia o próximo)
Sessão 1 ──< Mensagem                 (origem e destino endereçadas por nome · ref · projeto)
Sessão 1 ──< Consumo medido >── Orçamento declarado   (o Workflow mede; a Administração declara)
Chamado 1 ──< Gate (G0–G9)            (o kanban projeta; estado derivado, nunca digitado)
Pedido de decisão 1 ──< Ruling        (dentro do agregado; sem autor ou sem destino, recusado)
Pedido de decisão ← nasce de: "Propor regra" (política) e do ask/derrubar do Workflow (mapa, relação 5)
Catálogo ── alimenta: roteamento (nomes de catálogo) e custo estimado (preço do modelo)
```

## 10. Vocabulário

Os termos dos agregados **já estão** no glossário (`docs/governance/glossary.md`, colunas
"Cycle 072/073"): pedido de decisão, ruling, sessão de agente, tarefa aberta, caixa de
entrada, livro de mensagens, roteamento por nome/ref, colisão de nomes, política declarativa,
limite de orçamento, catálogo de skills/ferramentas/modelos. Os termos **novos** deste ciclo —
**frase-chave**, **trilha de contexto**, **aviso de simulação** e os verbos **Propor regra**,
**Endereçar por ref**, **Registrar ruling**, **Drenar outbox** — entram pela tarefa **T12**
(inglês, ADR 0014), antes do primeiro verde do verificador: a regra 2 do `verifica-prototipo.py`
lê o glossário, e rótulo novo sem entrada acusaria.
