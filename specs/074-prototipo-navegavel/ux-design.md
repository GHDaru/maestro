# User experience (UX) design 074 — protótipo navegável do painel de regência

- **Status**: aprovado com ajustes no gate de UX (`gate-ux.md`, 27/10/2026) — B-UX1, B-UX2
  e os secundários aplicados neste documento · **Data**: 2026-10-27 · **Agente**:
  `ux-semantics`
- **Insumos**: `specs/074-prototipo-navegavel/spec.md` (aprovada com ajustes B1, B2, S1–S6) ·
  `specs/074-prototipo-navegavel/briefing-regente.md` (§3 fixo) ·
  `specs/074-prototipo-navegavel/gate-spec.md` (S5 manda a tabela do §4) ·
  `specs/074-prototipo-navegavel/gate-ux.md` (B-UX1, B-UX2, S-a–S-f) ·
  `specs/073-area-administrativa/design-system.md` (tokens + 16 objetos, §4) ·
  `specs/073-area-administrativa/confronto/mapa-de-contextos.md` (os cinco contextos) ·
  `specs/073-area-administrativa/prototipo/README.md` (contrato de marcação, regras 5 e 6,
  *roster*) · `specs/066-painel-de-regencia/ux-design.md` (as telas da regência, via o
  apontador do `specs/072-painel-de-regencia/ux-design.md`) · `painel/projetos/exemplo.json`
  (origem das fixtures; projeto `maestro`).
- **Consumido por**: `dev-implementer` (implementa o papel) · `qa` (jornadas do §3 como
  roteiro do crítico que anda) · jornada viva (`docs/jornada/074-prototipo-navegavel.md`).
- **Siglas** (Princípio VIII, expandidas na 1ª ocorrência): ENTRA (as funcionalidades que
  **entram** — veredicto do confronto do 073), FR (*functional requirement*, requisito
  funcional), NFR (*non-functional requirement*, requisito não funcional), HTML
  (*HyperText Markup Language*), CSS (*Cascading Style Sheets*), CTA (*call to action*,
  ação principal), MCP (*Model Context Protocol*), A2A (*Agent-to-Agent*).

## 0. Lei de ferro deste documento

```
NENHUMA TELA NASCE SEM PAPEL SEMÂNTICO — E NENHUM CLIQUE PROMETE O QUE O MÉTODO NÃO CUMPRE
```

O painel **nunca promove e nunca decide** (066, §0); o protótipo acrescenta a regra própria
dele: **simular não é autorizar**. Todo efeito de clique é **declarativamente simulado**
(`data-simulado="sim"` + aviso visível "simulado"), e o botão documenta **quem autorizaria
no produto** (`data-autoriza`), não quem autoriza no protótipo. O único caso em que a tela
deixa de oferecer a ação é fixo da decisão 3 do briefing: **o Gerente nunca é derrubável**.

## 1. A casca: seis vistas sobre cinco contextos (B1)

Os cinco contextos são os do mapa; os seis itens do menu são **vistas** — cada item resolve
para um fragmento existente (requisito funcional 2 — FR2 — da spec), e toda tela declara
`data-contexto` com um dos cinco valores que o verificador (d) aceita.

| Item do menu | Vista sobre | Resolve para (fragmento, proposta) | `data-contexto` |
|---|---|---|---|
| **Regência** | síntese da Regência (contadores dos outros contextos, como projeção) | `telas/regencia/inicial.html` — tela inicial, a frase-chave | `regencia` |
| **Chamados** | **Chamados e Gates** (core domain — não esvaziar, B1) | `telas/chamados-e-gates/kanban-por-gate.html` | `chamados-e-gates` |
| **Fila** | Regência (o que espera o humano) | `telas/regencia/fila-de-decisoes.html` | `regencia` |
| **Sessões** | Workflow de sessões | `telas/workflow-de-sessoes/sessao-de-agente.html` | `workflow-de-sessoes` |
| **Administração** | Administração | `telas/administracao/catalogo.html` | `administracao` |
| **Mensageria** | Mensageria | `telas/mensageria/caixa-de-entrada.html` | `mensageria` |

- **Tela inicial** (FR1): rota desconhecida cai nela sem erro. O `data-contexto` da tela
  inicial é **`regencia`** — decisão deste documento, **aceita no gate de UX** (decisão 1):
  ela é a vista Regência do menu (B1: "Regência → tela inicial"), e os contadores que agrega
  (sessões caídas, mensagens desviadas) são **projeção** dos outros contextos, lidos, não
  decididos — mesma categoria do painel no mapa (§2 do mapa: projeção não é contexto).
- **Trilha de contexto** (papel introduzido por este ciclo): navegação secundária entre
  fragmentos **irmãos do mesmo contexto** (as três da Administração, as quatro do
  Workflow, as quatro da Mensageria), no padrão que o 073 já mediu
  (`administracao-01-catalogo.html` carrega `<nav class="telas>` com os irmãos). É ela que
  garante o **≤ 3 cliques** (FR2): item do menu (1 clique) → fragmento de entrada →
  trilha para qualquer irmão (2 cliques). A Fila alcança o ruling pelo CTA "Responder".
- **Ruling** é alcançado **pela Fila** (CTA "Responder" do pedido), nunca solto: a resposta
  nasce de um pedido — o papel manda a ordem.

## 2. Papel semântico de tela a tela (15 fragmentos: a tela inicial + 3 da Regência + 4 da Mensageria + 3 da Administração + 4 do Workflow)

> Os nomes de arquivo abaixo são **proposta** (o padrão
> `prototipo/telas/<contexto>/<tela>.html` é da FR1; o slug exato é deste documento). Os
> objetos do design system citados são os da §4 do `design-system.md`. As telas da
> Mensageria, Administração e Workflow **reproduzem** os wireframes do 073
> (`mensageria-01-caixa-de-entrada.html` … `workflow-04-consumo-por-agente.html`) sem
> movê-los nem editá-los (FR8); as da Regência reproduzem o 072 (`painel/index.html`,
> `vKanban`, `vFila`) sobre os tokens novos. A coluna "decisão que serve" cita a decisão
> fixa do **briefing §3** que a tela cumpre; telas de leitura dizem **só leitura**.

### 2.1 Regência (e a tela inicial) — "o que me espera"

| Tela | Papel semântico | Decisão que serve (briefing §3) | `data-contexto` | Design system consumido | Fragmento (proposta) |
|---|---|---|---|---|---|
| Tela inicial | **Frase-chave do regente**: em uma linha, o que espera o humano — "você tem N decisões esperando, a mais velha há X h (exemplo)" — com os contadores vivos (fila, sessões caídas, mensagens desviadas) sem rolar | 2 (a tela inicial é a frase-chave) · **só leitura** | `regencia` | frase-chave do regente · navegação · contadores | `telas/regencia/inicial.html` |
| Kanban por gate | **"Onde está cada chamado"**: projeção do core domain; o estado do portão é derivado, nunca digitado — a tela nunca promove (anti-regra 1 do 066) | 2 (item Chamados) · **só leitura** | `chamados-e-gates` (B1) | coluna G0–G9 · cartão de chamado em gate · veredito normalizado · filtro por frente · portão do regente (marcador) · `data-fonte` · "—" com motivo | `telas/chamados-e-gates/kanban-por-gate.html` |
| Fila de decisões | **"O que está esperando por mim"**: pedidos ordenados por prazo e bloqueio; pergunta sem ruling nunca sai da fila | 2 (item Fila) · **só leitura** — o CTA "Responder" navega ao ruling | `regencia` | pedido de decisão (cartão com CTA "Responder") · portão do regente · "—" com motivo | `telas/regencia/fila-de-decisoes.html` |
| Ruling | **"A resposta registrada com volta"**: opção escolhida, autor humano, destino — sem autor ou sem destino, recusada | 3 (ação simulada "Registrar ruling") · 4 (autor humano e identidade) | `regencia` | ruling (formulário em cartão + botão primário) · chips selecionáveis | `telas/regencia/ruling.html` |

### 2.2 Mensageria — "como as sessões se falam"

| Tela | Papel semântico | Decisão que serve (briefing §3) | `data-contexto` | Design system consumido | Fragmento (proposta) |
|---|---|---|---|---|---|
| Caixa de entrada | **"O que chegou para cada sessão e ainda não foi lido/drenado"** — não é a Fila de decisões (colisão de termo: a entrada de **mensagens** é Mensageria) | 2 (item Mensageria) · 3 ("Drenar outbox") | `mensageria` | caixa de entrada / livro de mensagens (lista com ponto de não lida) · sessão de agente (linha) | `telas/mensageria/caixa-de-entrada.html` |
| Livro de mensagens | **"O registro append-only unificado"** do que foi dito entre sessões — a memória, não a pendência | **só leitura** (append-only) | `mensageria` | livro de mensagens (lista compacta) · `data-fonte` | `telas/mensageria/livro-de-mensagens.html` |
| Roteamento por nome/ref | **"A tabela de resolução nome → ref"** — e onde a colisão aparece: endereço ambíguo é **recusado, nunca resolvido** (mapa §7.1) | 3 ("Enviar ao endereço ambíguo", com confirmação) | `mensageria` | sessão de agente (linha) · chip `--erro` a 10 % "endereçar por ref" | `telas/mensageria/roteamento.html` |
| Protocolo de intercomunicação | **"Como as sessões se expõem e conversam"**: MCP servido, A2A nomeado | **só leitura** | `mensageria` | cartão de lista · status | `telas/mensageria/protocolo.html` |

### 2.3 Administração — "quem existe, com que papel e configuração"

| Tela | Papel semântico | Decisão que serve (briefing §3) | `data-contexto` | Design system consumido | Fragmento (proposta) |
|---|---|---|---|---|---|
| Catálogo | **"O registro consultável"** de skills, ferramentas e modelos por projeto — e dos **perfis de agentes** (acréscimo da correção 2 do 073: o cadastro é o arquivo versionado, a tela **lê**) | 2 (item Administração) · **só leitura** (o cadastro é o arquivo; a tela lê) | `administracao` | cartão de lista · categoria em caixa alta · CTA | `telas/administracao/catalogo.html` |
| Políticas | **"A política declarativa"** allow/deny/ask por projeto: a Administração **declara**; a execução é do harness (mapa §2) — propor regra **não executa**, propõe | 3 ("Propor regra") | `administracao` | cartão · chips de regra · CTA "Propor regra" | `telas/administracao/politicas.html` |
| Orçamento | **"O teto declarado pelo administrador"** e o consumo medido contra ele — a Administração é upstream, o Workflow obedece e mede (mapa §2) | 3 ("Ajustar teto") | `administracao` | consumo/limite de orçamento (número grande + barra) · etiqueta "declarado"/"medido" | `telas/administracao/orcamento.html` |

> **Rótulos curtos (S-f)**: "Políticas" e "Orçamento" são rótulos curtos de **política
> declarativa (allow/deny/ask)** e **limite de orçamento** — os termos da linguagem ubíqua
> seguem nos títulos e no `data-rotulo` das telas; o botão "Ajustar teto" remete a
> **limite de orçamento**.

### 2.4 Workflow de sessões — "quem está fazendo o quê, agora"

| Tela | Papel semântico | Decisão que serve (briefing §3) | `data-contexto` | Design system consumido | Fragmento (proposta) |
|---|---|---|---|---|---|
| Sessão de agente | **"A unidade de administração"**: subir, acompanhar, reiniciar, derrubar — derrubar é irreversível e **vira gate humano** (mapa, relação 5) | 2 (item Sessões) · 3 (Subir/Reiniciar/Derrubar) | `workflow-de-sessoes` | sessão de agente (linha de lista compacta) · estado do agente vivo · botão primário "Subir" | `telas/workflow-de-sessoes/sessao-de-agente.html` |
| Estado do agente vivo | **"Quem está vivo e em que estado"**, por detecção de processo, não só heartbeat | **só leitura** | `workflow-de-sessoes` | estado do agente vivo (ponto de status + texto) | `telas/workflow-de-sessoes/estado-do-agente-vivo.html` |
| Tarefa aberta | **"O que cada agente está fazendo agora"**: a tarefa ativa por agente (`start` sem `stop`) | **só leitura** | `workflow-de-sessoes` | linha de lista compacta · "—" com motivo quando não há | `telas/workflow-de-sessoes/tarefa-aberta.html` |
| Consumo por agente | **"Quanto custa quem"**: tokens por agente contra o teto, e o dólar **estimado** ao lado | **só leitura** — o segmento de período é botão de escrita (3) | `workflow-de-sessoes` | consumo por agente (número + barra) · período (segmento) · coluna "estimado" | `telas/workflow-de-sessoes/consumo-por-agente.html` |

### 2.5 Papéis introduzidos — anatomia mínima (a entrada no design system é tarefa do plano)

**Trilha de contexto** — anatomia mínima: lista horizontal de links `href="#/contexto/tela"`
para os fragmentos irmãos do mesmo contexto, logo abaixo do título da tela (padrão medido no
073, `administracao-01-catalogo.html`); rótulo = nome da tela na linguagem ubíqua; item
ativo com `aria-current="page"` em `--sucesso`. Estados: **presente** (contexto com dois ou
mais fragmentos) · **ausente** (contexto com um fragmento só — `chamados-e-gates` não tem
trilha). Atributos: é navegação (`href="#/…"`), **não** botão de escrita — não carrega o
contrato do §5.

**Aviso de simulação** — anatomia mínima: mensagem curta "simulado — recarregar restaura as
fixtures (exemplo)" junto ao botão acionado, com `data-aviso="simulado"` e `role="status"`
(anunciada por leitor de tela). Estados: **aparece** ao confirmar a ação · **some** sozinha
após alguns segundos · o efeito em si permanece na tela (o contador atualizado da fila é o
efeito; o aviso só declara que é simulação).

## 3. Jornadas por contexto — o que o crítico anda (gate final, decisão 6)

Cinco jornadas, uma por contexto. Cada passo é um **clique real na casca** com efeito
visível; o crítico cumpre no browser, sem ler HTML. Fixtures: projeto **`maestro`** em toda
tela (S6) — o valor vem de `repos[0].nome` de `painel/projetos/exemplo.json` (o campo
`projeto` do arquivo é `exemplo`, o nome do arquivo de configuração; o **retrato datado do
073** usa `410_MAESTRO`, o nome da pasta do projeto em `~/.claude/projects/` — as fixtures
do 074 seguem o valor `maestro` do campo `repos`, S-b do gate); a mesma sessão
`Worker03 [ad66d6] · maestro` onde for citada (FR5); *roster* de refs da regra 6 do 073;
autor humano `Ana Exemplo` (`painel/projetos/exemplo.json`, `regencia.pessoas`). Nenhum
dado pessoal real.

### J1 · Regência — "decidir o que está esperando"

| Passo | Clique | Efeito visível esperado |
|---|---|---|
| 1 | abrir `prototipo/index.html` | frase-chave "você tem 3 decisões esperando, a mais velha há 7 h (exemplo)" com número e ação em laranja; contadores de sessões caídas e mensagens desviadas |
| 2 | item **Fila** | fila de decisões ordenada por prazo; o pedido mais velho com idade "há 7 h (exemplo)" e, se estourado, borda esquerda `--erro` |
| 3 | CTA **Responder** do pedido mais velho | fragmento do ruling: pergunta, opções em chips, recomendação, autor, destino |
| 4 | chip de opção | chip selecionado em `--primaria` |
| 5 | **Registrar ruling** | toast "simulado"; o pedido **sai da fila**; o contador da frase-chave passa a 2 |
| 6 | item **Regência** | a frase-chave mostra **2 decisões esperando** — o efeito do ruling propagado à síntese |

### J2 · Chamados e Gates — "ver onde cada chamado parou" (core domain, leitura)

| Passo | Clique | Efeito visível esperado |
|---|---|---|
| 1 | item **Chamados** | kanban por gate: colunas G0–G9 com contadores; cartões com idade no gate e selo de evidência |
| 2 | chip de **filtro por frente** | só os cartões da frente escolhida ficam visíveis (efeito do `data-efeito`) |
| 3 | botão **Detalhar** no cartão parado em G3 | painel de detalhe **na própria tela** (expansão; botão `data-acao="detalhar"`, `data-autoriza="humano"`, `data-simulado="sim"`, `data-efeito="mostra o veredito normalizado e o original ao lado"`): veredito normalizado **e** o original ao lado; marcador builder ≠ crítico; idade |
| 4 | marcador laranja **portão do regente** (G7/G8) | leva à Fila — o portão é item somente leitura da fila, nunca botão de aceite no cartão |

### J3 · Workflow de sessões — "quem morreu e quem reinicio"

| Passo | Clique | Efeito visível esperado |
|---|---|---|
| 1 | item **Sessões** | sessões por linha `nome · ref · projeto` com ponto de estado |
| 2 | **Reiniciar** em `Worker03 [ad66d6] · maestro` | confirmação irreversível (`data-perde`/`data-reverte`): o que se perde — o ref atual; como reverter — o contexto vivo só volta por `claude --resume` |
| 3 | confirmar | o **ref muda** na linha e o aviso "o ref muda ao reiniciar" aparece; toast "simulado" |
| 4 | **Derrubar** em `Worker02 [31f7bf] · maestro` → confirmar | a linha passa a **caída** (sem sinal, `--borda-2` tachado) |
| 5 | conferir a linha `Gerente [31ee4d] · maestro` | **sem botão Derrubar** — aviso "portão do regente" (o Gerente nunca é derrubável) |
| 6 | trilha de contexto → tarefa aberta, consumo | telas irmãs abrem em 1 clique a partir desta |

### J4 · Administração — "declarar regra e teto, e ver quem mudou"

| Passo | Clique | Efeito visível esperado |
|---|---|---|
| 1 | item **Administração** | catálogo: skills/ferramentas/modelos por projeto; seção **"Agentes (perfis)"** listando os perfis reais; uma linha de fixture do histórico de mudanças visível |
| 2 | trilha → **políticas** | blocos allow/deny/ask por projeto; uma linha de fixture do histórico visível |
| 3 | **Propor regra** (ask) | toast "simulado" + link "ver na fila": a proposta **vira pedido de decisão** (mapa, relação 5 — propor não executa) |
| 4 | trilha → **orçamento** | teto por projeto/agente/modelo; barra de consumo com etiqueta "declarado"/"medido" |
| 5 | **Ajustar teto** | a barra recalcula contra o teto novo e muda de cor (`--grafico-2` → `--primaria` → `--erro`); **nova linha no histórico de mudanças** (auditoria, `changed_by`) |

### J5 · Mensageria — "o que chegou, para quem, e o que ficou registrado"

| Passo | Clique | Efeito visível esperado |
|---|---|---|
| 1 | item **Mensageria** | caixa de entrada: mensagens não lidas com ponto laranja e destinatário `nome · ref · projeto` |
| 2 | **Drenar outbox** | os pontos somem, o contador de não lidas zera; toast "simulado" |
| 3 | trilha → **roteamento** | tabela de resolução nome → ref; a linha colidida mostra o chip `--erro` "endereçar por ref" |
| 4 | **Enviar ao endereço ambíguo** na linha colidida | abre a **confirmação irreversível** (`data-perde`/`data-reverte`) — a confirmação **antecede** a recusa |
| 5 | confirmar | o endereço ambíguo é **recusado** com pedido de desambiguação — a resolução é só pelo ref (`nome · ref · projeto`), nunca "o mais provável" |
| 6 | trilha → **livro de mensagens** | a linha da mensagem drenada está registrada (append-only; recusar `DELETE` é do depósito) |

## 4. Tabela ENTRA → tela → elemento alcançado (S5 do gate de spec)

As **18 linhas** do S5: os **15 ENTRA** do 073 (números do confronto,
`specs/073-area-administrativa/confronto/confronto-decisao.md` § "ENTRA — 15") **mais** as
**3 telas da regência** (prefixadas "Tela da regência" para se distinguirem das linhas
ENTRA). O 16º ENTRA (cadastro de agentes, correção 2 do 073) entra como **linha acrescentada
após as 18**, para a contagem fixa do S5 ficar legível.

| # | ENTRA / tela | Tela (fragmento) | Elemento alcançado (e efeito simulado, quando houver) |
|---|---|---|---|
| 1 | ENTRA 1 · sessão de agente | `telas/workflow-de-sessoes/sessao-de-agente.html` | linha da sessão com Subir/Reiniciar/Derrubar; reiniciar troca o ref, derrubar marca caída (J3) |
| 2 | ENTRA 4 · limite de orçamento | `telas/administracao/orcamento.html` | teto por projeto/agente/modelo + "Ajustar teto"; a barra recalcula (J4) |
| 3 | ENTRA 5 · política declarativa (allow/deny/ask) | `telas/administracao/politicas.html` | blocos allow/deny/ask + "Propor regra"; a proposta vira pedido na fila (J4) |
| 4 | ENTRA 9 · catálogo de skills/ferramentas/modelos | `telas/administracao/catalogo.html` | registro consultável por projeto |
| 5 | ENTRA 12 · auditoria administrativa | seção "histórico de mudanças" nas **três** telas da Administração — Catálogo, Políticas e Orçamento, **cada uma com uma linha de fixture visível ao crítico** | linha "quem mudou o quê" (`changed_by`); o ajuste de teto acrescenta linha (J4) |
| 6 | ENTRA 13 · estado do agente vivo | `telas/workflow-de-sessoes/estado-do-agente-vivo.html` | ponto de status por sessão (trabalhando/esperando/bloqueado/sem tarefa/sem sinal) |
| 7 | ENTRA 14 · tarefa aberta | `telas/workflow-de-sessoes/tarefa-aberta.html` | tarefa ativa por agente (`start` sem `stop`); "—" com motivo quando não há |
| 8 | ENTRA 16 · consumo por agente | `telas/workflow-de-sessoes/consumo-por-agente.html` | tokens por agente + barra contra o teto; segmento de período |
| 9 | ENTRA 17 · custo estimado por agente | coluna em `telas/workflow-de-sessoes/consumo-por-agente.html` | dólar por agente marcado **estimado**; fonte = preço do modelo no catálogo |
| 10 | ENTRA 21 · mensagem entre agentes | objeto nas **quatro** telas da Mensageria | remetente/destinatário `nome · ref · projeto` em toda mensagem exibida |
| 11 | ENTRA 22 · protocolo de intercomunicação | `telas/mensageria/protocolo.html` | MCP servido, A2A nomeado |
| 12 | ENTRA 23 · caixa de entrada | `telas/mensageria/caixa-de-entrada.html` | não lidas com ponto; "Drenar outbox" zera o contador (J5) |
| 13 | ENTRA 24 · roteamento por nome/ref | `telas/mensageria/roteamento.html` | tabela de resolução nome → ref |
| 14 | ENTRA 25 · livro de mensagens | `telas/mensageria/livro-de-mensagens.html` | registro append-only unificado |
| 15 | ENTRA 26 · colisão de nomes | visível dentro de `telas/mensageria/roteamento.html` | chip "endereçar por ref" na linha colidida; endereço ambíguo recusado (J5) |
| 16 | Tela da regência · kanban por gate | `telas/chamados-e-gates/kanban-por-gate.html` | colunas G0–G9 + cartões; filtro por frente com efeito visível (J2) |
| 17 | Tela da regência · fila de decisões | `telas/regencia/fila-de-decisoes.html` | pedidos por prazo com CTA "Responder" (J1) |
| 18 | Tela da regência · ruling | `telas/regencia/ruling.html` | formulário com chips de opção; "Registrar ruling" tira o pedido da fila (J1) |
| — | ENTRA (correção 2 do 073) · **cadastro de agentes** — **acréscimo da correção 2 do 073, fora das 18 linhas do S5** | seção "Agentes (perfis)" em `telas/administracao/catalogo.html` | perfis reais listados (papel, ferramentas, modelo padrão), `data-fonte: ls .claude/agents` |

## 5. Ações simuladas: o contrato dos botões de escrita

**Botão de escrita (S1, definição fixa)**: todo `<button>`, `<form>` ou `[role=button]`
**sem** `href="#/…"` e **sem** `data-vai-para`. Consequência declarada aqui: **chips de
filtro, segmentos de período e seleção de opção são botões de escrita** pela definição
mecânica — e está certo que carreguem o contrato: o `data-efeito` descreve a mudança visível
(filtrar é mudar a tela, não navegar). Por decisão 3 do gate de UX: o **filtro por frente**
e o **segmento de período** levam `data-autoriza="humano"` e `data-simulado="sim"`.

Todo botão de escrita declara os **quatro atributos** (FR4): `data-acao` (verbo da
linguagem ubíqua) · `data-autoriza` (humano · regente por delegação · sessão dona —
**declarativo**, documenta quem autorizaria no produto; o protótipo não bloqueia clique por
papel, Clarify 6 da spec) · `data-simulado="sim"` · `data-efeito` (o que muda na tela).
Exemplo concreto por contexto:

| Contexto | Botão | `data-acao` | `data-autoriza` | `data-efeito` |
|---|---|---|---|---|
| chamados-e-gates | chip de filtro por frente | `filtrar-frente` | humano | só os cartões da frente escolhida ficam visíveis |
| regencia | Registrar ruling | `registrar-ruling` | humano | o pedido sai da fila e o contador da frase-chave atualiza |
| workflow-de-sessoes | Reiniciar sessão | `reiniciar` | regente por delegação | o ref da sessão muda e o aviso "o ref muda ao reiniciar" aparece |
| administracao | Ajustar teto | `ajustar-teto` | humano | a barra de consumo recalcula contra o teto novo e muda de cor |
| mensageria | Drenar outbox | `drenar-outbox` | sessão dona | as mensagens não lidas da sessão ficam lidas e o contador zera |

### Confirmações irreversíveis — nomes finais (B2-i) e contrato exato (B-UX1)

Confirmados como **nomes finais**: **`data-perde`** e **`data-reverte`**, na confirmação que
o botão irreversível abre (desenhada no 073):

- **`data-perde`** — **o que se perde**: o estado que não volta (em "Derrubar
  `Worker02 [31f7bf] · maestro`": "o contexto vivo da sessão e o ref atual; mensagens
  endereçadas ao ref antigo não chegam").
- **`data-reverte`** — **como reverter**: o caminho de engenharia de reversibilidade
  (Princípio III): "subir a sessão de novo pelo lançador; a fila de decisões e o livro de
  mensagens são append-only e permanecem".

São ações irreversíveis (FR4, com o **reiniciar** incluído pelo gate de UX): **reiniciar
sessão** (o ref muda; o contexto vivo só volta por `claude --resume`), **derrubar** sessão,
**entregar a destino não resolvido** (mensageria — a confirmação antecede a recusa do
endereço ambíguo, J5) e **estourar teto** (orçamento — "Efeito ao estourar" com os dois
atributos).

**Contrato exato (B-UX1)**: botão irreversível declara `data-irreversivel="sim"` e
`data-confirma="<id da confirmação>"`. Botão com `data-acao="derrubar"` declara
`data-alvo="nome · ref · projeto"`. A verificação (h) falha se `data-alvo` começar por
`Gerente`. A verificação (i) falha se o id de `data-confirma` não existir ou se a confirmação
não tiver `data-perde` e `data-reverte`.

**O Gerente nunca é derrubável (B2-h, fixo)**: nenhum botão com `data-acao="derrubar"` tem
o Gerente como alvo — a linha `Gerente [31ee4d] · maestro` **não carrega o botão** e mostra
o aviso "portão do regente"; o verificador (h) falha alto se algum `data-acao="derrubar"`
apontar para ele (via `data-alvo`, B-UX1).

## 6. Ponto de quebra da navegação inferior (Clarify 5 da spec; decisão 2 do gate de UX, aceita com ajuste)

O design system v1 **não tem token de quebra** (a §1 dele mede cor, raio, sombra e
tipografia; a §4 diz "barra inferior (3 a 5 itens) ou lateral em desktop"). Decisão do gate:

- **O valor não é token consumido em `@media`** — variável CSS não vale em media query. É
  **constante comentada** em `prototipo/tokens.css` e em `prototipo/app.js`, na forma
  (proposta):

  ```css
  /* PROVISÓRIO (gate de UX 074): quebra da navegação — 768px. NÃO é variável
     consumível em @media. Confirmação: captura do build real a 360px na jornada
     viva ("Administração" cabe a 12px?); se não couber, a constante anda no
     mesmo commit da captura. */
  ```

- **768 px**: abaixo disso a navegação é a **barra inferior** (ícone sobre o rótulo `12px`,
  ativo em `--sucesso` com fundo a 10 %, como medido na referência); acima, **lateral**.
  Seis itens cabem na barra inferior com ícone sobre rótulo a partir de ~360 px de largura
  (6 × ~60 px); a §4 do design system passa a ler "3 a **6** itens". Motivo do valor: é a
  largura em que a coluna de conteúdo (cartão `--raio-lg`, padding 24 px) deixa de caber ao
  lado de um menu lateral de seis itens com rótulo legível.
- **O `design-system.md` do 073 não é editado durante o julgamento do 073**: a emenda
  (quebra, trilha de contexto, aviso de simulação, "3 a 6 itens") vira **tarefa do plano do
  074**, aplicada quando o julgamento do 073 fechar.

## 7. Estados (todos declarados, todos com cara própria)

- **vazio**: informação, não erro — "fila vazia — última decisão às HH:MM (exemplo)" na
  Fila; "nenhuma mensagem não lida" na caixa de entrada; "nenhum chamado nesta frente" no
  kanban; "—, nenhuma tarefa aberta" na tarefa aberta.
- **carregando**: o estado é da **casca** (fragmento sendo carregado), curto e local; as
  fixtures são estáticas, nenhuma tela inventa "carregando dados" que não existe.
- **erro**: rota inexistente **cai na tela inicial sem erro** (FR1); fixture ausente →
  "—" com o motivo e o caminho (regra F8 do 066), nunca um valor padrão.
- **sem permissão**: o papel "portão do regente" — a ação que é do humano (ruling, G7/G8,
  derrubar) aparece a um agente como somente leitura com o aviso; o protótipo não bloqueia
  por papel (Clarify 6), **exceto** o caso fixo: o Gerente não tem botão Derrubar (§5).

## 8. Acessibilidade (declarada aqui, não no fim)

- Todo controle só-ícone tem `aria-label` com verbo e objeto ("responder pedido D-014
  (exemplo)", "derrubar sessão Worker02 [31f7bf] · maestro").
- Estado nunca é só cor: aprovado/devolvido/vermelho provado/sem sinal têm texto ou glifo
  além da cor; contraste mínimo 4,5:1 (tokens `--tinta`/`--texto-2` sobre `--fundo`).
- Foco visível; ordem de tabulação pela urgência (o pedido mais velho primeiro na Fila).
- Idade como "há 7 h (exemplo)" **e** carimbo absoluto no atributo do elemento (066, §6).
- A barra inferior é navegável por teclado e o item ativo é anunciado (`aria-current`).

## 9. Decisões julgadas pelo gate de UX (gate-ux.md, 27/10/2026)

As três decisões declaradas na versão proposta foram julgadas:

1. **Tela inicial com `data-contexto="regencia"` — ACEITA** (§1).
2. **Quebra em 768 px e barra inferior "3 a 6 itens" — ACEITA COM AJUSTE** (§6): constante
   comentada em `tokens.css` e `app.js`, não token de `@media`; provisória até a captura do
   build real a 360 px na jornada viva; a emenda ao design system do 073 é **tarefa do
   plano do 074** (o 073 está em julgamento e não é editado).
3. **Chips de filtro e segmentos são botões de escrita — ACEITA** (§5): filtro por frente e
   segmento de período levam `data-autoriza="humano"` e `data-simulado="sim"`.

Os bloqueantes **B-UX1** (contrato exato de `data-irreversivel`/`data-confirma`/
`data-alvo`, §5) e **B-UX2** (J2 passo 3 como expansão na própria tela, botão `detalhar`)
e os secundários **S-a** (15 fragmentos, aqui e na FR3 da spec), **S-b** (origem de
`maestro`, §3), **S-c** (prefixo ENTRA na tabela, J1 passo 6, J5 renomeada e com
confirmação, reiniciar irreversível), **S-d** (siglas), **S-f** (rótulos curtos) e a
coluna "decisão que serve" estão aplicados. **S-e** (glossário: frase-chave, trilha de
contexto, aviso de simulação e os quatro verbos) é **tarefa do plano** (Worker01), não
deste documento.

**Handoff**: → `dev-implementer` (papéis §2, contrato dos botões §5, quebra §6) · → `qa`
(jornadas J1–J5 como roteiro do crítico que anda; tabela §4 como lista de conferência) · →
jornada viva (`docs/jornada/074-prototipo-navegavel.md`, capturas do build real).
