# Spec 072 — Painel de regência, rodada 1: kanban por gate e fila de decisões (o painel lê; o regente decide)

> **Rodada 1, recorte por fronteira.** O `ux-design.md` do ciclo 066 desenhou quatro telas novas
> (§2.1 kanban por frente, §2.2 jornada do chamado, §2.3 fila de decisões, §2.4 mapa de sessões).
> Esta spec cobre **só §2.1 e §2.3** — o que o regente precisa às 07:00 para ver onde cada chamado
> parou e o que espera por ele. §2.2 e §2.4 ficam nomeadas em "Fora de escopo". As regras do
> conferidor **já existem** em `painel/chamados.py` (ciclos 068/069): esta spec as **consome**, não
> as reimplementa (anti-padrão 22, a cópia com perdas).

- **Status**: Draft (proposta) · **Raia**: plena · **Data**: 2026-10-24
- **Appetite**: um ciclo — o recorte de duas telas (§2.1 kanban por gate, §2.3 fila de decisões);
  escopo variável dentro do tempo fixo, sem prazo estimado (operating-model §5; DoR §7).
- **Origem**: ciclo 072 (painel de regência), rodada 1 — demanda do Darú no mapa de integração
  (`specs/066-painel-de-regencia/plano-integracao-linha-paralela.md` §3, linha 072) e no `ux-design.md`
  do 066 §2.1 e §2.3. Fonte dos objetos: `specs/NNN-*/G*-*.md` via `painel/chamados.py` (o estado do
  chamado já é calculado — 068/069); a fila de decisões é fonte **nova** (registro append-only).
- **Revisão**: T01b — condições do gate DoR (ADR 0026, crítico `process-guardian`), incorporadas
  abaixo; as duas ambiguidades abertas na T01 foram **decididas** pelo Darú (ver última seção).

**Siglas usadas neste documento** (Princípio VIII — nenhuma sigla nasce nua): **EARS** (*Easy
Approach to Requirements Syntax*, a forma "QUANDO … O SISTEMA DEVERÁ …") · **FR** (*functional
requirement*, requisito funcional) · **JSONL** (*JSON Lines*, um objeto JSON por linha) · **A2A**
(*Agent-to-Agent*, protocolo de ligação entre agentes) · **PID** (*Process IDentifier*, identificador
de processo) · **DOM** (*domain model*, o bloco `DOM:*` que o plano carrega) · **TAIL** (*closing
tail*, cauda de fechamento do ciclo: `TAIL:review/security/mutation/gate`) · **HTTP** (*Hypertext
Transfer Protocol*, protocolo da web) · **HTML** (*HyperText Markup Language*, a linguagem da tela) ·
**ADR** (*Architecture Decision Record*, registro de decisão de arquitetura) · **DoR** (*Definition of
Ready*, definição de pronto para executar) · **DoD** (*Definition of Done*, definição de pronto) ·
**F1–F12** (as *fitness functions* do gate de UX, `ux-design.md` §7).

> **Raia**: plena, não leve. Não cabe numa frase: acrescenta **duas telas**, **um registro de
> decisão** e uma **tabela de normalização** que decide o que a tela mostra em todo chamado de todo
> projeto instalado; e (por decisão do gate) impõe append-only mecânico no workflow herdado.
> **Ambiguidade** média (as regras de veredito e conferidor são precisas em 068/069; a novidade — a
> fila e a normalização — é o que a spec fixa em EARS); **raio** amplo (o kanban passa a ser a leitura
> padrão do estado por gate; a fila, a fonte do ruling); **irreversibilidade** baixa (texto versionado
> em `painel/`; desfeito por `git revert`; nenhum ambiente tocado). **A rodada 2 é declarada INFRA**
> (operating-model §3): toca schema, hooks de terceiro e configuração do alvo — ver "Fora de escopo".

## Glossário deste ciclo

| Termo | O que é aqui |
|---|---|
| **Painel de regência** | Read-model local onde o humano vê a fila de decisões, os chamados por gate e (em rodadas futuras) as sessões: projeção de arquivos de gate e de um registro de decisão. **Nunca promove, nunca decide, nunca inventa** (ux-design §0, princípio 1 do v0). |
| **Pedido de decisão** | Pergunta escalada ao humano com **id**, quem pediu (papel + sessão), pergunta, opções com descrição, recomendação, **prazo**, idade, o que destrava e destino da resposta. O painel só exibe e registra. |
| **Ruling** | Resposta registrada ao pedido: texto/opção escolhida, **autor humano**, data, **destinatário**, link para o merge/ADR que a cita. Sem autor humano ou sem destino, é recusado (F5). |
| **Veredito normalizado** | Mapeamento canônico **aprovado / devolvido / vermelho provado / em curso / inválido**, exibido **ao lado do valor original** do arquivo de gate; o arquivo nunca é reescrito (F6, anti-regra 6). |
| **Portão do regente** | G7 (aceite), G8 (ordem) e `TAIL:gate`: gates que **só o humano registra**. Quando pendentes, viram **item da fila** com id derivado (chamado+gate) e **marcador** no cartão (FR20). |

## O quê e por quê

### 1. O regente às 07:00 precisa saber onde cada chamado parou

O 068 já calcula o estado de cada gate a partir dos arquivos (`confere`, `ordem_veredito`). O que
falta é a **tela** que responde "onde está cada chamado" sem abrir pasta por pasta: um **kanban por
gate**, com o cartão no último gate aprovado, o dono do gate atual e a idade no gate (ux-design §2.1).
A tela **lê** os dados do 068; não inventa um segundo conferidor.

### 2. O que está esperando por mim não é o mesmo que onde está cada chamado

A dor de 16/10 (um pedido das 07:04 respondido só à tarde, esperas de 7 h e 24 h) não aparece num
kanban de chamados: aparece numa **fila de decisões** — pedidos escalados ao humano, ordenados por
prazo e por bloqueio, com o que destrava e para quem volta a resposta (ux-design §2.3). O pedido sem
resposta **fica na fila** (não há "dispensar"); a resposta vira um **ruling** com autor humano e
destino.

### 3. O painel não decide — e a normalização não apaga a palavra do arquivo

Duas anti-regras governam as duas telas (ux-design §4): o painel **não promove** (arrastar é só
proposta de transição, recusada na origem sem arquivo de gate válido) e **não decide pelo humano** (a
recomendação é texto de quem pediu, o botão de resposta nunca vem pré-marcado). E o veredito é
exibido **normalizado ao lado do original** — normalizar é traduzir, não sobrescrever.

### 4. O que herdamos do 070 e onde cada pendência cai

O gate DoR recusou deixar o workflow do 070 em silêncio nesta rodada. A **dívida 5** (append-only não
imposto) **vira FR** desta rodada, porque exige-se do registro append-only um mecanismo, não uma
convenção; as demais dívidas e FR1/FR2/FR3 vão para a **rodada 2 — raia infra**. A disposição completa
está na seção "Herdado do 070".

## Requisitos funcionais (FR, de *functional requirement*)

### A. Kanban por gate (§2.1)

- **FR1 — Colunas é o gate.** QUANDO o painel desenha o kanban, O SISTEMA DEVERÁ mostrar as dez
  colunas **G0 a G9**, na ordem da tabela `GATES` de `painel/chamados.py`, cada coluna com nome e
  sigla; onde não houver fonte para o "limite de idade", exibir "—" com motivo (FR22).
- **FR2 — O cartão está no último gate aprovado.** QUANDO um chamado tem vereditos em vários gates,
  O SISTEMA DEVERÁ colocar o cartão no **último gate cujo veredito vigente é `aprovado`**, usando
  `confere`/`ordem_veredito` de `painel/chamados.py` (veredito vigente = maior `data:` válida, 069);
  a spec **não** cria uma segunda regra de estado.
- **FR3 — Anatomia do cartão, com a fonte de cada campo.** QUANDO um cartão é desenhado, O SISTEMA
  DEVERÁ exibir **id do chamado, frente, dono do gate atual (papel + sessão), veredito normalizado do
  gate atual E o valor original do arquivo, idade no gate e selo de evidência** (ux-design §2.1). As
  **fontes**: id e frente da pasta/`projetos/<nome>.json`; **dono (papel) da tabela `GATES` de
  `painel/chamados.py`** e sessão do cabeçalho do gate (sem sessão, "—" com motivo); veredito e selo
  do cabeçalho do gate; idade por FR23.
- **FR4 — Independência provada.** QUANDO o autor da peça (`autor_da_peca`) e o autor do veredito
  (`por`) são a **mesma** pessoa, O SISTEMA DEVERÁ mostrar o marcador **vermelho**; diferentes,
  marcador "builder ≠ crítico" sem vermelho (Princípio II; ux-design §2.1).
- **FR5 — O parser expõe `autor_da_peca` (nomeadamente, sem tocar o 068 em silêncio).** QUANDO o
  cabeçalho de um gate traz `autor_da_peca`, O SISTEMA DEVERÁ expô-lo no item do gate, ao lado de
  `por`. **Hoje `painel/chamados.py` só lê `por`;** o campo `autor_da_peca` só aparece no ux-design.
  Esta rodada **estende o parser de `painel/chamados.py`** (arquivo do 068) de forma explícita: o
  campo é lido do cabeçalho e, sem ele, o marcador de FR4 exibe "—" com motivo — nunca um verde
  presumido. A extensão é **declarada** aqui, não silenciosa.
- **FR6 — Identidade de patch: "não conferido".** QUANDO o cartão exibe o marcador "integrado =
  criticado", O SISTEMA DEVERÁ mostrá-lo como **"não conferido"** (nunca verde) enquanto não existir o
  script de `git patch-id --stable` versionado; só o script transforma o marcador em conferido
  (ux-design §2.1, anti-regra 8).
- **FR7 — Filtro por frente.** QUANDO o regente escolhe uma frente, O SISTEMA DEVERÁ restringir os
  cartões à frente escolhida, lendo as frentes de `projetos/<nome>.json`; sem escolha, todas.
- **FR8 — Arrasto é proposta, não promoção.** QUANDO um cartão é arrastado para um gate de destino,
  O SISTEMA DEVERÁ habilitar a proposta **só** se existir, na pasta do chamado, o arquivo do gate de
  destino com cabeçalho válido; faltando, recusar na origem e mostrar "falta `G<n>-*.md` com cabeçalho
  válido" (F2; anti-regra 1).
- **FR9 — Transição sem evidência é recusada (comportamento).** QUANDO uma transição é pedida sem
  arquivo de gate de destino com cabeçalho válido, O SISTEMA DEVERÁ responder **422 com o motivo** e
  **não** gravar nem mover arquivo algum (F3). (O *como* — rota e tratamento de erro — é decisão do
  plano, não desta spec.)

### A/B. Veredito normalizado (regra comum às duas telas)

- **FR10 — Normalização é tabela-dirigida.** QUANDO o painel exibe um veredito, O SISTEMA DEVERÁ
  mapeá-lo pela tabela fixa — `aprovado` ⇐ `APPROVE`/`OK`/`PASSA`/`PASSOU`; `devolvido` ⇐
  `RETURN`/`REPROVE`/`FALHA`; `vermelho provado` ⇐ `FALHA_ESPERADA`; `em curso` ⇐
  `PENDENTE`/`REPRODUZIDO`; `inválido` ⇐ cabeçalho reprovado pelo conferidor. **Qualquer outro valor**
  DEVERÁ cair em `inválido`, **mantendo o original visível**; o arquivo de gate **nunca** é reescrito
  (F6; anti-regra 6).

### B. Fila de decisões (§2.3)

- **FR11 — Anatomia do pedido de decisão.** QUANDO um pedido é registrado, O SISTEMA DEVERÁ exigir
  **id, quem pediu (papel + sessão), pergunta, opções com descrição, recomendação, prazo, o que
  destrava, destino da resposta (para quem volta) e status** (ux-design §2.3).
- **FR12 — Pedido sem ruling nunca sai da fila.** QUANDO um pedido não tem ruling registrado,
  O SISTEMA DEVERÁ mantê-lo na fila (F4); **não existe "dispensar"** — só "responder" ou "devolver a
  quem pediu", e os dois geram registro (anti-regra 4).
- **FR13 — Anatomia do ruling.** QUANDO o humano responde, O SISTEMA DEVERÁ registrar o ruling com
  **texto/opção escolhida, autor humano, data e destinatário**, **link para o merge/ADR que o cita**,
  o retorno **"encaminhado a …"** na tela e a ação **"devolver a quem pediu"** como operação
  **registrada** (ux-design §2.3).
- **FR14 — Ruling sem autor humano ou destino é recusado.** QUANDO um ruling chega sem autor humano
  **ou** sem destinatário, O SISTEMA DEVERÁ recusá-lo e não registrar (F5). Pela decisão do Darú (1a),
  **só pessoa é autor humano**: quando a resposta vier por delegação, o registro guarda
  `registrado_por` (quem lançou) mais a **referência ao registro de delegação**, sem confundir autoria.
- **FR15 — Ordem da fila.** QUANDO a fila é exibida, O SISTEMA DEVERÁ ordená-la por **prazo e por
  bloqueio** (o que estoura antes e trava mais vem primeiro), com o nº de itens destravados
  (ux-design §2.3, "Ordem da fila").
- **FR16 — Registro append-only é MECÂNICO, não convenção.** QUANDO o painel acrescenta um pedido ou
  um ruling, O SISTEMA DEVERÁ **somente crescer** o arquivo JSONL da fila. O acréscimo é **garantido**
  por: (a) o painel abre o registro em modo append e **nunca** reescreve, reordena ou remove linha; e
  (b) um teste que guarda o **prefixo de bytes** do arquivo antes do acréscimo e prova que ele ficou
  **inalterado** depois (o arquivo só cresce). O registro é **arquivo do painel, fora do projeto
  lido** (ux-design §4, anti-regra 7 — o painel **lê** o projeto e **registra** só no próprio dado);
  o caminho exato é decisão do plano (`DOM:*`).
- **FR17 — Append-only imposto por gatilho (dívida 5 do 070).** QUANDO um `UPDATE` ou um `DELETE`
  incide sobre `rodadas`, `passos` ou `transicoes` do SQLite do workflow, O SISTEMA DEVERÁ recusá-lo
  por **`TRIGGER`** — append-only imposto pela base, não pela convenção. Consequência declarada: o
  `UPDATE passos` do hook `Stop` deixa de ser possível e o hook é ajustado nesta rodada para **não**
  escrever `UPDATE`; a cobrança de verdade do `Stop` (dívida 7) fica para a rodada 2.
- **FR18 — O painel não escolhe.** QUANDO a fila oferece a resposta, O SISTEMA DEVERÁ gravar
  **`autor = humano`** (decisão do Darú 1a), nunca inferir autoria do agente que pediu.
- **FR19 — A resposta nunca vem pré-marcada.** QUANDO a fila exibe as opções, O SISTEMA DEVERÁ
  apresentá-las **sem pré-seleção**: a recomendação é texto de quem pediu, e o botão de resposta não
  marca nada em nome do humano (anti-regra 2).
- **FR20 — Portão do regente pendente é item da fila.** QUANDO G7, G8 ou `TAIL:gate` está pendente,
  O SISTEMA DEVERÁ (decisão do Darú 2a) criar um **item da fila com id derivado (chamado + gate)**,
  ler o **status do arquivo de gate**, tirar o **"desde quando" do commit do arquivo** e, no cartão do
  kanban, pôr um **marcador com link para o item**; o **ruling aceita o id derivado**. A um agente, o
  item aparece como **somente leitura** (ux-design §2.3, §3 "sem permissão").

### Regras universais (valem para A e B; ux-design §7)

- **FR21 — Todo número tem data-fonte.** QUANDO um número ou selo é exibido, O SISTEMA DEVERÁ
  acompanhá-lo de `data-fonte` com o comando ou caminho que o produziu (F1).
- **FR22 — "—" sempre com motivo.** QUANDO a fonte de um valor falta, O SISTEMA DEVERÁ exibir "—"
  **com o motivo e o caminho**; nunca "0", nunca "n/a" (F8; anti-regra 3).
- **FR23 — Idade do relógio e do carimbo, com o mais velho no cabeçalho.** QUANDO o painel calcula
  idade ou carimbo, O SISTEMA DEVERÁ lê-los do **relógio do sistema** ou do **timestamp do registro**
  (nunca de campo digitado), exibir a idade como **"há 7 h 12 min" E o carimbo absoluto** no atributo
  do elemento, e manter no **cabeçalho um contador com a idade do item mais velho da fila**
  (jornada §3, passo 1). Data escrita à mão em arquivo aparece com o selo **"declarada"** (F7;
  anti-regra 5).
- **FR24 — Botão só-ícone tem rótulo.** QUANDO um controle é só-ícone (arrastar, responder, abrir
  evidência), O SISTEMA DEVERÁ trazer `aria-label` com o verbo e o objeto ("responder pedido D-014")
  (F9; ux-design §6).
- **FR25 — Ingestão defasada é anunciada.** QUANDO `meta.ingerido_em` tem mais de 1 h, O SISTEMA
  DEVERÁ anunciar **"defasado"** no cabeçalho (F10).
- **FR26 — Jornada viva.** QUANDO a rodada mexe na tela, O SISTEMA DEVERÁ manter
  `docs/journeys/072-*.md` com capturas geradas por **script versionado** e heurística **datada ≥** a
  data da captura (F11; skill `living-journey`).
- **FR27 — Nunca abre `.env` nem guarda host/token.** QUANDO o painel ingere ou registra,
  O SISTEMA DEVERÁ **não** abrir `.env`, **não** ler `settings.local.json` e **não** gravar host nem
  token; o registro da fila é arquivo do painel, **fora do projeto lido** (F12; v0 §2.6).

## Herdado do 070 — disposição das dez dívidas e de FR1/FR2/FR3

O gate DoR exigiu disposição explícita. A tabela dá o destino de cada pendência do plano do 070
(`specs/070-workflow-sqlite/plan.md` § "Dívidas declaradas") e de FR1/FR2/FR3 da spec do workflow.

| Pendência do 070 | Disposição |
|---|---|
| **dívida 5** — "append-only" sem gatilho (`UPDATE`/`DELETE` livres em `rodadas`/`passos`/`transicoes`; o hook `Stop` faz `UPDATE passos`) | **Vira FR desta rodada (FR17)**: um `TRIGGER` recusa `UPDATE`/`DELETE` nas três tabelas — append-only mecânico, não convenção. Consequência: o `UPDATE passos` do `Stop` deixa de ser possível e o hook é ajustado nesta rodada. |
| dívida 6 — hook `SessionStart` imprime `payload`/`sessao_origem`/`passos.sessao` no stdout (vetor de injeção) | **rodada 2 — raia infra**: sanitizar o stdout (só campos conhecidos, truncados, sem caracteres de controle) e auditar injeção; exige dry run. |
| dívida 7 — `Stop` fecha o passo (`UPDATE`, `resultado='skip'`) em vez de cobrar | **rodada 2 — raia infra** (comportamento do hook + teste; é o par da dívida 5). |
| dívida 10 — `os.replace` com WAL deixa `-wal`/`-shm` velhos; `PermissionError` no Windows; broadcast consumido pelo primeiro leitor | **rodada 2 — raia infra**: exige `wal_checkpoint(TRUNCATE)`, **lock de ingest**, **backup** antes da troca e teste de interrupção. |
| FR1 (spec do 070) — entrada do passo sem branch nem hash de partida | **rodada 2 — raia infra** (muda o schema). |
| FR2 (spec do 070) — recusar entrada sem saída com evidência (hoje só no adaptador, sem teste) | **rodada 2 — raia infra** (função pura + teste; toca o schema). |
| FR3 (spec do 070) — encerrar com passo aberto deve cobrar resumo e saída | **rodada 2 — raia infra** (é a dívida 7, o mesmo hook). |
| dívida 1 — FR2/FR3 sem teste nomeado, regra na borda | **rodada 2**, junto de FR1/FR2/FR3. |
| dívida 2 — `_ensure_schema` em três cópias (dois hooks + `fila_outbox`) | **rodada 2**, ao mexer nos hooks. |
| dívida 3 — `install_hooks.py` escreve em `settings.json` do alvo sem backup | **rodada 2 — raia infra** (toca configuração de terceiro: **backup** e dry run). |
| dívida 4 — nomes reais do Hindiana na fixture `equipes` | **rodada 2**, junto do board que exibe a equipe. |
| dívida 8 — FR1 parcial: schema sem colunas de branch/hash | **rodada 2**, junto de FR1. |
| dívida 9 — FR10 provado por teste que injeta os dados | **rodada 2**, ao reescrever o teste sobre a fixture. |

**Regra do gate**: **só a dívida 5** é paga nesta rodada (porque FR16 exige append-only mecânico). Todo
o resto vai para a **rodada 2 — raia infra**, declarada abaixo.

## Fora de escopo

Nomeado, não desenhado nesta rodada (ux-design §8):

- **Mapa de sessões (§2.4)** — sessões vivas, "sem sinal", "caída", nome duplicado.
- **Jornada do chamado (§2.2)** — trilha G0→G9, hash julgado, histórico de devoluções.
- **Abrir agente / ligar via A2A** — ação de regência; só o objeto é nomeado (ciclo futuro).
- **Controle de PID** — subir/derrubar sessão (risco alto; spec própria).
- **Livro de mensagens como fonte** — quando ausente, a tela declara "—, livro não configurado".
- Promover gate, gravar veredito no arquivo ou aceitar pendência pelo painel — o painel lê e
  registra; quem assina o gate é o dono, no arquivo (068, Fora de escopo).
- Substituir o conferidor do Hindiana (`conferir_chamado.py`) — aqui só a projeção.

### Rodada 2 — raia infra (nomeada, não desenhada)

A rodada 2 é **infra** (operating-model §3): toca schema SQLite, hooks de terceiro e configuração do
alvo, e por isso carrega gates de reversibilidade — **backup**, dry run, **lock de ingest**,
`wal_checkpoint` e rollback documentado. Ela absorve as pendências do 070 marcadas acima como
"rodada 2" (dívidas 6, 7, 10 e as demais, e FR1/FR2/FR3 do workflow) e o mapa de sessões (§2.4).

## Artefatos condicionais que o plano DEVERÁ declarar (`docs/governance/artifacts.md`)

| Artefato | Declaração | Motivo em uma linha |
|---|---|---|
| `data-model.md` | `ART:data-model=yes` | Entidades novas: **Pedido de decisão** e **Ruling**, mais o registro append-only da fila; o kanban projeta Chamado/Gate/Veredito do 068 sem entidade nova. |
| `contracts/` | `ART:contracts=yes` | Rota de escrita (transição, 422 em recusa) e rota(s) de leitura da fila, consumidas por outras sessões e pela IA. |
| `ux-design.md` | `ART:ux-design=yes` | Duas telas (§2.1 kanban, §2.3 fila) — **já desenhadas** em `specs/066-painel-de-regencia/ux-design.md`; o artefato é **consumido/apontado**, não reescrito. |
| `research.md` | `ART:research=no` | Nenhuma incógnita: as regras de veredito e conferidor vêm de 068/069; o desenho das telas, do ux-design do 066; a disposição das dívidas, do gate. |
| `checklist.md` | `ART:checklist=no` | A DoD (*Definition of Done*, definição de pronto) abaixo cobre o que há para checar. |

## Para o plano — modelo de domínio (obrigatório desde o 067)

Esta spec **não** carrega os tokens `DOM:*`; o plano os declara. O que o plano DEVERÁ decidir:

1. **Agregado**: `Chamado`/`Gate`/`Veredito` (068) permanecem — o kanban é **projeção**, não agregado
   novo. A fila é agregado novo: `PedidoDeDecisao` é a raiz; `Ruling` **não existe sem o pedido que
   ele fecha**. O plano decide se `Ruling` é entidade dentro de `PedidoDeDecisao` ou agregado próprio
   (a resposta pode chegar por delegação — FR14).
2. **Invariantes no domínio** (funções puras, sem HTTP nem arquivo): a normalização tabela-dirigida
   (FR10), a permanência do pedido sem ruling (FR12) e a ordem da fila (FR15). O plano diz se alguma
   ficou na borda e por quê.
3. **Glossário**: `changed` — entram **painel de regência**, **pedido de decisão**, **ruling**,
   **veredito normalizado** e **portão do regente** (os cinco desta spec), em
   `docs/governance/glossary.md` (em inglês — ADR 0014).
4. **Portas**: `new` — a rota de escrita da transição (FR9) e a(s) rota(s) de leitura da fila; o
   **registro JSONL**, o **gatilho de append-only** (FR17) e a leitura dos arquivos de gate como
   adaptadores. **O plano fixa o caminho do arquivo JSONL** (arquivo do painel, fora do projeto) e os
   nomes de módulo/rota — nada disso é fixado por esta spec.

## Critérios de aceite

> O código ainda não existe. As **regras puras** carregam nomes de teste (o plano fixa o arquivo); os
> **nomes de módulo e de rota são decisão do plano**, não critério.

- `python -m unittest discover -s painel/tests -p test_regencia.py` → `Ran 13 tests`, `OK`, exit 0.
- Os testes nomeados, um por regra:
  `test_f1_metrica_sem_data_fonte_zero_no_html_renderizado` (FR21, F1),
  `test_f2_cartao_em_gn_exige_arquivo_do_gate` (FR2/FR8, F2),
  `test_f3_transicao_sem_arquivo_devolve_422` (FR9, F3),
  `test_f4_pedido_sem_ruling_fica_na_fila` (FR12, F4),
  `test_f5_ruling_sem_autor_humano_ou_destino_e_recusado` (FR14, F5),
  `test_f6_normalizacao_tabela_dirigida` (FR10, F6),
  `test_f7_idade_do_relogio_e_carimbo` (FR23, F7),
  `test_f8_traco_com_motivo` (FR22, F8),
  `test_f9_botao_so_icone_com_aria_label_no_html_renderizado` (FR24, F9),
  `test_f10_ingestao_defasada_anunciada` (FR25, F10),
  `test_f14_registro_append_only_so_cresce` (FR16),
  `test_divida5_gatilho_recusa_update_e_delete` (FR17),
  `test_portao_do_regente_item_com_id_derivado` (FR20).
- **F1 vira TESTE sobre o HTML renderizado** (não grep no `index.html`): WHEN a página é renderizada
  THEN THE SYSTEM SHALL ter **zero** elementos `.metrica` sem `data-fonte` (F1; FR21).
- **F9 vira TESTE sobre o HTML renderizado** (não grep no `index.html`): WHEN a página é renderizada
  THEN THE SYSTEM SHALL ter **zero** `<button>` só-ícone sem `aria-label` e sem texto (F9; FR24).
- WHEN `G3-*.md` está ausente e o chamado tem G2 aprovado THE SYSTEM SHALL manter o cartão em G2 e
  exibir "falta `G3-*.md` com cabeçalho válido" (F2).
- WHEN uma transição é pedida sem arquivo de gate de destino válido THE SYSTEM SHALL responder `422`
  com motivo, e nenhum arquivo muda (F3).
- WHEN a fixture tem 3 pedidos e 1 ruling THE SYSTEM SHALL listar 2 na fila (F4).
- WHEN um ruling chega sem `destino` (ou sem autor humano) THE SYSTEM SHALL recusá-lo (F5).
- WHEN o veredito é `APPROVE`/`OK`/`PASSA`/`PASSOU` THE SYSTEM SHALL normalizar como `aprovado`; com
  `RETURN`/`REPROVE`/`FALHA` → `devolvido`; `FALHA_ESPERADA` → `vermelho provado`;
  `PENDENTE`/`REPRODUZIDO` → `em curso`; `NÃO PASSA` (ou qualquer outro valor) → `inválido` **com o
  original visível** (F6, tabela-dirigida).
- WHEN um cabeçalho é reprovado pelo conferidor (`painel/chamados.py`) THE SYSTEM SHALL normalizar o
  veredito como `inválido`, sem reescrever o arquivo (FR10).
- WHEN a fonte de um valor falta THE SYSTEM SHALL renderizar "—" e o texto conter `motivo:` (F8).
- WHEN um `UPDATE`/`DELETE` é tentado em `rodadas`/`passos`/`transicoes` THE SYSTEM SHALL ser recusado
  pelo `TRIGGER` (FR17).
- WHEN o painel acrescenta uma linha ao registro da fila THE SYSTEM SHALL manter inalterado o prefixo
  de bytes anterior (o arquivo só cresce) (FR16).
- WHEN `meta.ingerido_em` é antigo (> 1 h) THE SYSTEM SHALL anunciar "defasado" no cabeçalho (F10).
- WHEN um chamado tem G7/G8/`TAIL:gate` pendente THE SYSTEM SHALL criar o item da fila com id derivado
  (chamado+gate), ler o status do arquivo e pôr o marcador no cartão (FR20).
- `ls docs/journeys/072-*.md` → existe; `grep -c 'F11' docs/journeys/072-*.md` → `≥ 1` (FR26).
- `grep -rn '\.env\|settings.local.json' painel/` → nenhum caminho de **leitura** de `.env`/`settings.local.json`
  pela ingestão/registro (FR27).
- Regressão do 069: `ls specs/070-conferidor-ordem-veredito/` → **10** arquivos (nove de gate —
  `00-chamado`, `G0-reproducao`, `GD-risco`, `G1-W11`, `G2-vermelho`, `G3-codigo`, `G3-criterio`,
  dois `G3-runner2` — mais `spec.md`; conferido por `ls`); a pasta segue imutável.
- Dados reais da Hindiana **não** entram: `ls painel/projetos/*hindiana*` → vazio (fixture).
- `ls specs/072-painel-de-regencia/spec.md` → existe.
- `scripts/check-language.sh` → verde; `scripts/check-conformance.sh 072` → verde após plano, tasks e
  `qa-report.md`.

## Limites declarados

- **Dez colunas (G0 a G9)**, por recorte do ux-design §2.1. `abertura` e `GD`, que existem na tabela
  `GATES`, **não** viram coluna nesta rodada — o plano declara onde entram.
- **FR5 estende `painel/chamados.py`** (arquivo do 068) para expor `autor_da_peca`; a extensão é
  declarada aqui, e o conferidor do Hindiana (`conferir_chamado.py`) **não** é tocado por ela.
- **FR17 impõe o gatilho no schema do 070** e obriga a ajustar o hook `Stop` nesta rodada; a
  **cobrança de verdade** do `Stop` (dívida 7) fica na rodada 2 — declarado para não parecer pago.
- **O caminho do registro JSONL da fila é decisão do plano** (`DOM:*`); a spec exige que seja arquivo
  do painel (fora do projeto) e **append-only** (FR16).
- **O marcador "integrado = criticado" fica "não conferido"** até existir o script versionado de
  `git patch-id --stable` (FR6); não se apresenta como verde sem prova.
- **O arrasto só propõe**; nada é promovido, movido ou apagado por ele. A promoção do gate continua
  sendo o arquivo assinado pelo dono (068).
- **Fila vazia é informação**: "fila vazia — última decisão às HH:MM" (ux-design §3).
- **Dados reais da Hindiana não entram** neste repositório público (fixture, decisão
  `decisao-066-daru-20-10`).
- **Dívida 2 (três cópias de `_ensure_schema`) não é paga aqui** — vai com os hooks para a rodada 2.

## Ambiguidades — resolvidas no gate DoR (24/10)

1. **A Office conta como "autor humano" de um ruling?** → **Decidido (1a): só pessoa é autor
   humano.** O registro guarda `registrado_por` (quem lançou) e a **referência ao registro de
   delegação**; a Office não substitui a autoria (FR14, FR18).
2. **O portão do regente é item da fila ou marcador do cartão?** → **Decidido (2a): os dois.** Item da
   fila com **id derivado (chamado + gate)**, status do arquivo, "desde quando" do commit, **e**
   marcador no cartão com link; o ruling aceita o id derivado (FR20).

<!--
  GATE (DoR — não delegável na origem; delegado nesta rodada ao crítico independente, ADR 0026):
  esta spec só vira plano depois do veredito. Revisão T01b: APROVADO COM CONDIÇÕES — condições
  C1–C8 + itens "MAIS" incorporados; ambiguidades 1 e 2 decididas pelo Darú.
  Handoff: spec-agent → (gate) → plan-architect.
-->
