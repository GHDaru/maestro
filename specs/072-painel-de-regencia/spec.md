# Spec 072 — Painel de regência, rodada 1: kanban por gate e fila de decisões (o painel lê; o regente decide)

> **Rodada 1, recorte por fronteira.** O `ux-design.md` do ciclo 066 desenhou quatro telas novas
> (§2.1 kanban por frente, §2.2 jornada do chamado, §2.3 fila de decisões, §2.4 mapa de sessões).
> Esta spec cobre **só §2.1 e §2.3** — o que o regente precisa às 07:00 para ver onde cada chamado
> parou e o que espera por ele. §2.2 e §2.4 ficam nomeadas em "Fora de escopo". As regras do
> conferidor **já existem** em `painel/chamados.py` (ciclos 068/069): esta spec as **consome**, não
> as reimplementa (anti-padrão 22, a cópia com perdas).

- **Status**: Draft (proposta) · **Raia**: plena · **Data**: 2026-10-24
- **Origem**: ciclo 072 (painel de regência), rodada 1 — demanda do Darú no mapa de integração
  (`specs/066-painel-de-regencia/plano-integracao-linha-paralela.md` §3, linha 072) e no `ux-design.md`
  do 066 §2.1 e §2.3. Fonte dos objetos: `specs/NNN-*/G*-*.md` via `painel/chamados.py` (o estado do
  chamado já é calculado — 068/069); a fila de decisões é fonte **nova** (registro append-only).

> **Raia**: plena, não leve. Não cabe numa frase: acrescenta **duas telas** e **um registro de
> decisão** ao painel, com rotas novas e uma tabela de normalização que decide o que a tela mostra
> em todo chamado de todo projeto instalado. **Ambiguidade** média (as regras de veredito e conferidor
> são precisas em 068/069; a novidade — a fila de decisões e a normalização — é o que a spec fixa em
> EARS); **raio** amplo (o kanban passa a ser a leitura padrão do estado por gate, e a fila passa a
> ser a fonte do ruling); **irreversibilidade** baixa (tudo é texto versionado em `painel/`: um módulo
> de regras, a tela e duas rotas; desfeito por `git revert`; nenhum ambiente tocado). Não é infra:
> nenhum dado real, nenhuma migração — dados da Hindiana entram como **fixture**.

## Glossário deste ciclo

| Termo | O que é aqui |
|---|---|
| **Painel de regência** | Read-model local onde o humano vê a fila de decisões, os chamados por gate e (em rodadas futuras) as sessões: projeção de arquivos de gate e de um registro de decisão. **Nunca promove, nunca decide, nunca inventa** (ux-design §0, princípio 1 do v0). |
| **Pedido de decisão** | Pergunta escalada ao humano com **id**, quem pediu (papel + sessão), pergunta, opções com descrição, recomendação, **prazo**, idade, o que destrava e destino da resposta. O painel só exibe e registra. |
| **Ruling** | Resposta registrada ao pedido de decisão: texto/opção escolhida, **autor humano**, data e **destinatário**. Sem autor humano ou sem destino, é recusado (F5). |
| **Veredito normalizado** | Mapeamento canônico **aprovado / devolvido / vermelho provado / em curso / inválido**, exibido **ao lado do valor original** do arquivo de gate; o arquivo nunca é reescrito (F6, anti-regra 6). |
| **Portão do regente** | G7 (aceite), G8 (ordem) e `TAIL:gate`: gates que **só o humano registra**. Quando pendentes, aparecem com chamado, gate, "desde quando" e evidência, e como **somente leitura** para um agente (ux-design §3, §4). |

## O quê e por quê

### 1. O regente às 07:00 precisa saber onde cada chamado parou

O 068 já calcula o estado de cada gate a partir dos arquivos (`confere`, `ordem_veredito`). O que
falta é a **tela** que responde "onde está cada chamado" sem o regente abrir pasta por pasta: um
**kanban por gate**, com o cartão no último gate aprovado, o dono do gate atual e a idade no gate
(ux-design §2.1). A tela **lê** os dados do 068; não inventa um segundo conferidor.

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
exibido **normalizado ao lado do original** — normalizar é traduzir, não sobrescrever: a palavra do
arquivo continua visível.

## Requisitos funcionais (FR, de *functional requirement*)

### A. Kanban por gate (§2.1)

- **FR1 — Colunas é o gate.** QUANDO o painel desenha o kanban, O SISTEMA DEVERÁ mostrar as dez
  colunas **G0 a G9**, na ordem da tabela `GATES` de `painel/chamados.py`, cada coluna com nome e
  sigla; onde não houver fonte para o "limite de idade", exibir "—" com motivo (FR18).
- **FR2 — O cartão está no último gate aprovado.** QUANDO um chamado tem vereditos em vários gates,
  O SISTEMA DEVERÁ colocar o cartão no **último gate cujo veredito vigente é `aprovado`**, usando
  `confere`/`ordem_veredito` de `painel/chamados.py` (veredito vigente = maior `data:` válida, 069);
  a spec **não** cria uma segunda regra de estado.
- **FR3 — Anatomia do cartão.** QUANDO um cartão é desenhado, O SISTEMA DEVERÁ exibir **id do
  chamado, frente, dono do gate atual (papel + sessão), veredito normalizado do gate atual E o valor
  original do arquivo, idade no gate e selo de evidência** (ux-design §2.1).
- **FR4 — Independência provada.** QUANDO o autor da peça (`autor_da_peca`) e o autor do veredito
  (`por`) são a **mesma** pessoa, O SISTEMA DEVERÁ mostrar o marcador **vermelho**; diferentes,
  marcador "builder ≠ crítico" sem vermelho (Princípio II; ux-design §2.1).
- **FR5 — Filtro por frente.** QUANDO o regente escolhe uma frente, O SISTEMA DEVERÁ restringir os
  cartões à frente escolhida, lendo as frentes de `projetos/<nome>.json`; sem escolha, todas.
- **FR6 — Arrasto é proposta, não promoção.** QUANDO um cartão é arrastado para um gate de destino,
  O SISTEMA DEVERÁ habilitar a proposta **só** se existir, na pasta do chamado, o arquivo do gate de
  destino com cabeçalho válido; faltando, O SISTEMA DEVERÁ recusar na origem e mostrar "falta
  `G<n>-*.md` com cabeçalho válido" (F2; anti-regra 1).
- **FR7 — `POST /transicao` recusa sem evidência.** QUANDO chega um `POST /transicao` sem arquivo de
  gate de destino válido, O SISTEMA DEVERÁ responder **422 com o motivo** (mesmo tratamento de
  `ValueError` já existente em `painel/server.py`), sem gravar nem mover arquivo algum (F3).

### A/B. Veredito normalizado (regra comum às duas telas)

- **FR8 — Normalização é tabela-dirigida.** QUANDO o painel exibe um veredito, O SISTEMA DEVERÁ
  mapeá-lo pela tabela fixa — `aprovado` ⇐ `APPROVE`/`OK`/`PASSA`/`PASSOU`; `devolvido` ⇐
  `RETURN`/`REPROVE`/`FALHA`; `vermelho provado` ⇐ `FALHA_ESPERADA`; `em curso` ⇐
  `PENDENTE`/`REPRODUZIDO`; `inválido` ⇐ cabeçalho reprovado pelo conferidor. **Qualquer outro valor**
  DEVERÁ cair em `inválido`, **mantendo o original visível**; o arquivo de gate **nunca** é reescrito
  (F6; anti-regra 6).

### B. Fila de decisões (§2.3)

- **FR9 — Anatomia do pedido de decisão.** QUANDO um pedido é registrado, O SISTEMA DEVERÁ exigir
  **id, quem pediu (papel + sessão), pergunta, opções com descrição, recomendação, prazo, o que
  destrava (chamados/sessões presas em "aguardo o GO"), destino da resposta (para quem volta) e
  status** (ux-design §2.3).
- **FR10 — Pedido sem ruling nunca sai da fila.** QUANDO um pedido não tem ruling registrado,
  O SISTEMA DEVERÁ mantê-lo na fila (F4); **não existe "dispensar"** — só "responder" ou "devolver a
  quem pediu", e os dois geram registro (anti-regra 4).
- **FR11 — Anatomia do ruling.** QUANDO o humano responde, O SISTEMA DEVERÁ registrar o ruling com
  **texto/opção escolhida, autor humano, data e destinatário** (ux-design §2.3).
- **FR12 — Ruling sem autor humano ou destino é recusado.** QUANDO um ruling chega sem autor humano
  **ou** sem destinatário, O SISTEMA DEVERÁ recusá-lo e não registrar (F5).
- **FR13 — Ordem da fila.** QUANDO a fila é exibida, O SISTEMA DEVERÁ ordená-la por **prazo e por
  bloqueio** (o que estoura antes e trava mais vem primeiro), com o nº de itens destravados
  (ux-design §2.3, "Ordem da fila").
- **FR14 — Registro só de acréscimo.** QUANDO o painel acrescenta um pedido ou um ruling, O SISTEMA
  DEVERÁ **apenas acrescentar uma linha** ao arquivo JSONL do projeto — nunca reescrever, reordenar
  ou remover linha. **O caminho do arquivo é decisão do plano** (`DOM:*`); a spec exige o registro,
  não o endereço.
- **FR15 — O painel nunca decide.** QUANDO a fila oferece a resposta, O SISTEMA DEVERÁ gravar
  `autor = humano`, **nunca pré-marcar** opção, e nunca escolher: a recomendação é texto de quem
  pediu (anti-regra 2).
- **FR16 — Portão do regente.** QUANDO G7, G8 ou `TAIL:gate` está pendente, O SISTEMA DEVERÁ
  listá-lo como **portão do regente** com **chamado, gate, "desde quando" e evidência (link)** e
  apresentá-lo a um agente como **somente leitura** (ux-design §2.3, §3 "sem permissão").

### Regras universais (valem para A e B; ux-design §7)

- **FR17 — Todo número tem data-fonte.** QUANDO um número ou selo é exibido, O SISTEMA DEVERÁ
  acompanhá-lo de `data-fonte` com o comando ou caminho que o produziu (F1).
- **FR18 — "—" sempre com motivo.** QUANDO a fonte de um valor falta, O SISTEMA DEVERÁ exibir "—"
  **com o motivo e o caminho**; nunca "0", nunca "n/a" (F8; anti-regra 3).
- **FR19 — Idade nunca vem de campo digitado.** QUANDO o painel calcula idade ou carimbo, O SISTEMA
  DEVERÁ lê-los do **relógio do sistema** ou do **timestamp do registro**, nunca de campo digitado;
  data escrita à mão em arquivo aparece com o selo **"declarada"** (F7; anti-regra 5).
- **FR20 — Botão só-ícone tem rótulo.** QUANDO um controle é só-ícone (arrastar, responder, abrir
  evidência), O SISTEMA DEVERÁ trazer `aria-label` com o verbo e o objeto ("responder pedido D-014")
  (F9; ux-design §6).
- **FR21 — Ingestão defasada é anunciada.** QUANDO `meta.ingerido_em` tem mais de 1 h, O SISTEMA
  DEVERÁ anunciar **"defasado"** no cabeçalho (F10).

## Fora de escopo

Nomeado, não desenhado nesta rodada (ux-design §8):

- **Mapa de sessões (§2.4)** — sessões vivas, "sem sinal", "caída", nome duplicado.
- **Jornada do chamado (§2.2)** — trilha G0→G9, hash julgado, histórico de devoluções, marcador
  "integrado = criticado" (patch-id).
- **Abrir agente / ligar via A2A** — ação de regência; só o objeto é nomeado (ciclo futuro).
- **Controle de PID** — subir/derrubar sessão (risco alto; spec própria).
- **Livro de mensagens como fonte** — quando ausente, a tela declara "—, livro não configurado".
- Promover gate, gravar veredito no arquivo ou aceitar pendência pelo painel — o painel lê e
  registra; quem assina o gate é o dono, no arquivo (068, Fora de escopo).
- Substituir o conferidor do Hindiana (`conferir_chamado.py`) — aqui só a projeção.

## Artefatos condicionais que o plano DEVERÁ declarar (`docs/governance/artifacts.md`)

| Artefato | Declaração | Motivo em uma linha |
|---|---|---|
| `data-model.md` | `ART:data-model=yes` | Entidades novas: **Pedido de decisão** e **Ruling**, mais o registro append-only da fila; o kanban projeta Chamado/Gate/Veredito do 068 sem entidade nova. |
| `contracts/` | `ART:contracts=yes` | Rota nova de escrita (`POST /transicao`, 422 em recusa) e rota(s) de leitura da fila, consumidas por outras sessões e pela IA. |
| `ux-design.md` | `ART:ux-design=yes` | Duas telas (§2.1 kanban, §2.3 fila) — **já desenhadas** em `specs/066-painel-de-regencia/ux-design.md`; o artefato é **consumido/apontado**, não reescrito. |
| `research.md` | `ART:research=no` | Nenhuma incógnita: as regras de veredito e conferidor vêm de 068/069; o desenho das telas vem do ux-design do 066. |
| `checklist.md` | `ART:checklist=no` | A DoD abaixo cobre o que há para checar. |

## Para o plano — modelo de domínio (obrigatório desde o 067)

Esta spec **não** carrega os tokens `DOM:*`; o plano os declara. O que o plano DEVERÁ decidir:

1. **Agregado**: `Chamado`/`Gate`/`Veredito` (068) permanecem — o kanban é **projeção**, não agregado
   novo. A fila é agregado novo: `PedidoDeDecisao` é a raiz e o `Ruling` **não existe sem o pedido que
   ele fecha**. O plano decide se `Ruling` é entidade dentro de `PedidoDeDecisao` ou agregado próprio
   (a resposta pode chegar por delegação — ver ambiguidade 1).
2. **Invariantes no domínio** (funções puras, sem HTTP nem arquivo): `normaliza(valor) -> canônico`
   (FR8, tabela-dirigida), `sai_da_fila(pedido, rulings)` (FR10) e `ordena_fila(itens)` (FR13). O plano
   diz se alguma ficou na borda e por quê.
3. **Glossário**: `changed` — entram **painel de regência**, **pedido de decisão**, **ruling**,
   **veredito normalizado** e **portão do regente** (os cinco desta spec), em
   `docs/governance/glossary.md` (em inglês — ADR 0014).
4. **Portas**: `new` — `POST /transicao` (FR7) e a(s) rota(s) de leitura da fila; o **registro JSONL**
   e a leitura dos arquivos de gate como adaptadores. **O plano fixa o caminho do arquivo JSONL** e o
   nome do módulo de regras.

## Critérios de aceite

> O código ainda não existe; os nomes de módulo/rota abaixo são a **meta** que o plano fixa. Cada
> critério é executável: comportamento em EARS ou par (comando, resultado esperado).

- `python -m unittest discover -s painel/tests -p test_regencia.py` → `Ran 8 tests`, `OK`, exit 0.
- Os oito testes nomeados, um por regra (arquivo `painel/tests/test_regencia.py`):
  `test_f2_cartao_em_gn_exige_arquivo_do_gate` (FR2/FR6, F2),
  `test_f3_transicao_sem_arquivo_devolve_422` (FR7, F3),
  `test_f4_pedido_sem_ruling_fica_na_fila` (FR10, F4),
  `test_f5_ruling_sem_autor_humano_ou_destino_e_recusado` (FR12, F5),
  `test_f6_normalizacao_tabela_dirigida` (FR8, F6),
  `test_f7_idade_vem_do_relogio_ou_registro` (FR19, F7),
  `test_f8_traco_com_motivo` (FR18, F8),
  `test_f10_ingestao_defasada_anunciada` (FR21, F10).
- WHEN `G3-*.md` está ausente e o chamado tem G2 aprovado THE SYSTEM SHALL manter o cartão em G2 e
  exibir "falta `G3-*.md` com cabeçalho válido" (F2).
- WHEN chega `POST /transicao` sem arquivo de gate de destino válido THE SYSTEM SHALL responder
  `422` com motivo, e nenhum arquivo muda (F3).
- WHEN a fixture tem 3 pedidos e 1 ruling THE SYSTEM SHALL listar 2 na fila (F4).
- WHEN um ruling chega sem `destino` (ou sem autor humano) THE SYSTEM SHALL recusá-lo (F5).
- WHEN o veredito é `APPROVE`/`OK`/`PASSA`/`PASSOU` THE SYSTEM SHALL normalizar como `aprovado`; com
  `RETURN`/`REPROVE`/`FALHA` → `devolvido`; `FALHA_ESPERADA` → `vermelho provado`;
  `PENDENTE`/`REPRODUZIDO` → `em curso`; `NÃO PASSA` (ou qualquer outro valor) → `inválido` **com o
  original visível** (F6, tabela-dirigida).
- WHEN um cabeçalho é reprovado pelo conferidor (`painel/chamados.py`) THE SYSTEM SHALL normalizar o
  veredito como `inválido`, sem reescrever o arquivo.
- WHEN a fonte de um valor falta THE SYSTEM SHALL renderizar "—" e o texto conter `motivo:` (F8).
- WHEN `meta.ingerido_em` é antigo (> 1 h) THE SYSTEM SHALL anunciar "defasado" no cabeçalho (F10).
- `grep -c 'aria-label' painel/index.html` → `≥ 1` e nenhum `<button` só-ícone sem texto e sem
  `aria-label` (F9).
- `grep -c '/transicao' painel/server.py` → `≥ 1` (rota nova registrada, recusa em 422).
- `grep -c 'def normaliza' painel/regencia.py` → `≥ 1` (tabela-dirigida; o plano pode mover a função,
  mantendo o nome).
- `python painel/chamados.py painel/projetos/exemplo.json` continua saindo com exit 0 — as regras do
  conferidor (068/069) não foram alteradas por esta rodada.
- `ls specs/072-painel-de-regencia/spec.md` → existe; e a pasta `specs/070-conferidor-ordem-veredito/`
  segue com seus 10 arquivos (regressão do 069).
- Dados reais da Hindiana **não** entram: `ls painel/projetos/*hindiana*` → vazio (fixture).
- `scripts/check-language.sh` → verde; `scripts/check-conformance.sh 072` → verde após plano, tasks e
  `qa-report.md`.

## Limites declarados

- **Dez colunas (G0 a G9)**, por recorte do ux-design §2.1. `abertura` e `GD`, que existem na tabela
  `GATES` de `painel/chamados.py`, **não** viram coluna nesta rodada — o plano declara onde entram.
- **"Integrado = criticado" (patch-id)** está nomeado no ux-design §2.1 mas **não** entra nesta
  rodada (depende de `git patch-id --stable` hoje feito à mão); fica em "Fora de escopo".
- **O caminho do arquivo JSONL da fila é decisão do plano** (`DOM:*`), não desta spec; a spec exige
  que o registro seja **append-only** (FR14).
- **Append-only é a regra de escrita do painel** (só acrescenta linha); um guard mecânico (triggers,
  hook) **não** é exigido aqui e fica declarado como possível dívida — a lição do 070 (dívida 5:
  "append-only" sem gatilho é convenção).
- **O arrasto só propõe**; nada é promovido, movido ou apagado por ele (anti-regra 1). A promoção do
  gate continua sendo o arquivo assinado pelo dono (068).
- **Fila vazia é informação**, não erro: "fila vazia — última decisão às HH:MM" (ux-design §3).
- **A idade é sempre derivada** (relógio/timestamp); data digitada em arquivo ganha o selo
  "declarada" (F7).
- **Dados reais da Hindiana não entram** neste repositório público (fixture, decisão
  `decisao-066-daru-20-10`).

## Ambiguidades para o Darú

1. **A Office conta como "autor humano" de um ruling?** O glossário do ux-design §5 diz "resposta do
   humano (ou da Office, por delegação)", mas F5 exige **autor humano** — e as duas coisas colidem
   quando a resposta vem por delegação. O que a spec não escolhe: a) só `autor = humano` (pessoa)
   satisfaz F5, e a Office delega registrando **em nome de** quem delegou; b) a Office é autora
   humana válida e o campo guarda também "quem delegou". → [decisão do Darú]
2. **O portão do regente é item da fila com id próprio, ou marcador do cartão?** O ux-design §2.3
   lista "Portão humano pendente" como objeto da fila, mas ele **nasce do arquivo de gate** (não de
   um pedido registrado). O que a spec não escolhe: a) cada G7/G8/`TAIL:gate` pendente entra na fila
   como item, com id derivado do chamado+gate; b) o portão aparece só como **marcador** no cartão do
   kanban, com link para responder pela fila (ux §3, passo 7). → [decisão do Darú]

<!--
  GATE (DoR — não delegável): esta spec só vira plano depois da aprovação do Darú.
  Handoff: spec-agent → (aprovação) → plan-architect.
-->
