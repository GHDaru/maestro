# Spec 074 — Protótipo navegável do painel de regência

- **Status**: Draft · **Lane**: plena (com o ramo de interface) · **Data**: 2026-10-26
- **Origem**: briefing da regente (`specs/074-prototipo-navegavel/briefing-regente.md`,
  26/10/2026). Pedido do Darú (26/10, 20:25): *"Vamos agora começar a construir os
  protótipos funcionais com telas e simulação da navegabilidade."*
- **Raia**: plena — **ambiguidade** baixa/média (as decisões da regente no briefing §3 são
  fixas; o que resta é de detalhe), **raio de explosão** alto (é a fundação da superfície
  navegável do produto, sobre a qual o backend de cada tela será construído) e
  **irreversibilidade** baixa (artefato novo e isolado; nada do painel v0 é tocado). Como
  tem tela, carrega o **ramo de interface**: papel semântico antes do componente
  (`ux-design.md`, agente ux-semantics) → gate de UX → jornada viva.
- **Siglas** (Princípio VIII, expandidas na 1ª ocorrência): DoD (*Definition of Done*), ADR
  (*Architecture Decision Record*), DDD (*Domain-Driven Design*), FR (*functional
  requirement*, requisito funcional), NFR (*non-functional requirement*, requisito não
  funcional), JSON (*JavaScript Object Notation*), HTML (*HyperText Markup Language*), CSS
  (*Cascading Style Sheets*), CDN (*Content Delivery Network*), HTTP (*HyperText Transfer
  Protocol*), UX (*user experience*), CI (*Continuous Integration*), DoR (*Definition of
  Ready*).

## Contexto e intenção

O 073 entregou os wireframes estáticos das 11 telas da área administrativa, o mapa de
contextos delimitados (DDD) e o design system v1 — mas eles não se andam: cada tela abre
sozinha, como documento. O Darú quer **andar pelo produto** antes de construir o backend de
cada tela. Este ciclo transforma aquela base num **protótipo clicável de alta fidelidade do
painel de regência inteiro**.

- **É**: casca única, navegação por contexto delimitado, todas as telas dos cinco
  contextos, dados de exemplo e **ações simuladas** — clicar "reiniciar sessão" abre a
  confirmação desenhada no 073, confirma, muda o estado em memória e mostra o efeito.
- **Não é** o produto: sem servidor novo, sem banco, sem chamada real ao harness. Toda
  ação de escrita é marcada `data-simulado="sim"` e produz efeito **só em memória**
  (recarregar a página volta às fixtures). O painel v0 (`painel/`) continua intacto; o
  protótipo **lê** dele o que já existe de verdade (`painel/projetos/exemplo.json`,
  `schema_workflow.sql`) para as fixtures.

Fundações que não se reinventam (briefing §2): os 11 wireframes e o contrato de marcação do
073, o design system v1 (tokens + 16 objetos), o mapa de contextos e a linguagem ubíqua, as
telas da regência do 072 (`painel/index.html`, `vKanban`, `vFila`) e o padrão de jornada
viva do 072 (capturas por script versionado + heurística datada).

## Requisitos funcionais

> As decisões da regente (briefing §3) são transcritas como requisitos, no espírito
> verbatim; nada aqui as reabre.

- **FR1 — Casca única e roteador** (decisão 1): WHEN o protótipo é aberto THEN
  `prototipo/index.html` é a casca única e `prototipo/app.js` roteia por
  `#/contexto/tela`, carregando o fragmento `prototipo/telas/<contexto>/<tela>.html`;
  WHEN a rota não existe THEN a casca cai na tela inicial sem erro.
- **FR2 — Navegação por contexto** (decisão 2): WHEN a casca renderiza THEN a navegação é
  lateral em desktop e inferior em largura estreita, com os seis itens — **Regência ·
  Chamados · Fila · Sessões · Administração · Mensageria** —; a tela inicial é a
  **frase-chave do regente** (ex.: "você tem N decisões esperando, a mais velha há X h",
  design system §4); toda tela é alcançável em **no máximo 3 cliques** a partir da inicial;
  toda tela diz em que contexto está (atributo `data-contexto`).
- **FR3 — Todas as telas dos cinco contextos** (decisões 1 e 2): o protótipo entrega **14
  fragmentos** — 3 da Regência (kanban por gate, fila de decisões, ruling) + 4 da
  Mensageria + 3 da Administração + 4 do Workflow de sessões —, todos preservando o
  contrato de marcação do 073 (`data-fonte`, `data-rotulo`, `data-exemplo`,
  `data-referencia`) e a **regra 5** de identidade de sessão `nome · ref · projeto` em
  todo texto visível e atributo. As telas da Regência são reproduzidas a partir do
  `painel/index.html` e do `ux-design.md` do 072, sobre os tokens novos, com os mesmos
  dados de exemplo.
- **FR4 — Ações simuladas com contrato** (decisão 3): WHEN um botão de escrita existe THEN
  ele declara `data-acao` (verbo da linguagem ubíqua), `data-autoriza` (humano · regente
  por delegação · sessão dona), `data-simulado="sim"` e `data-efeito` (o que muda na
  tela); WHEN a ação é confirmada THEN o efeito ocorre **só em memória** (recarregar volta
  às fixtures) e é visível na tela; WHEN a ação é irreversível (derrubar, entregar a
  destino não resolvido, estourar teto) THEN a confirmação mostra **o que se perde e como
  reverter**, como desenhado no 073; o **Gerente nunca é derrubável** pela tela.
- **FR5 — Fixtures coerentes** (decisões 1 e 4): os dados de exemplo vivem em
  `prototipo/fixtures/*.json`, **um JSON por agregado do mapa** (sessão, tarefa, chamado,
  pedido de decisão, mensagem, política, orçamento, catálogo), lidos do que já existe
  (`painel/projetos/exemplo.json`); as fixtures são **coerentes entre contextos** — a
  mesma sessão `Worker03 [ad66d6] · maestro` aparece em todas as telas que a citam; todo
  número é fixture marcada `(exemplo)` ou vem de `painel/projetos/exemplo.json` com
  `data-fonte`; `—` sempre com motivo; **nenhum dado pessoal real** (fixtures saem dos
  exemplos do repositório).
- **FR6 — Zero dependência externa** (decisão 1): o protótipo abre **offline** — sem
  framework, sem build, sem CDN — e é servido por `python -m http.server`, com a entrada
  declarada em `.claude/launch.json`.
- **FR7 — Design system como primeira entrega** (decisão 1, briefing §2):
  `prototipo/tokens.css` (tokens medidos do design system v1, nomes em português) e
  `prototipo/amostra.html` (cada componente da seção 4 do design system com os objetos do
  Maestro) existem **antes** das telas — são a base sobre a qual os fragmentos constroem.
- **FR8 — O verificador do 073 nunca fica vermelho** (briefing §5):
  `specs/073-area-administrativa/prototipo/verifica-prototipo.py` mantém **11 telas · 0
  achados** sobre a sua pasta; os wireframes do 073 não são movidos nem editados para
  virarem fragmentos — os fragmentos são arquivos novos. WHEN os juízes do 073 pedirem
  mudança numa tela THEN a mudança entra na tela do 073 **e** no fragmento do 074, pelo
  mesmo dono.

## Requisitos não funcionais

- **NFR1 — DoD executável** (decisão 5): `prototipo/verifica-navegacao.py` falha alto em
  seis verificações, além do verificador do 073 sobre as telas:
  - (a) todo `href="#/…"` e todo `data-vai-para` resolve para um fragmento existente;
  - (b) toda tela é alcançável em ≤ 3 cliques (grafo a partir da inicial);
  - (c) todo botão de escrita tem os quatro atributos da decisão 3 (FR4);
  - (d) toda tela tem `data-contexto` em um dos cinco contextos;
  - (e) nenhum `<link>`/`<script>` externo;
  - (f) corpus de mutação com fixtures boa/ruim (o verificador tem de **falhar** com a
    fixture ruim, provando que discrimina).
- **NFR2 — Fitness functions do repositório**: `scripts/check-conformance.sh 074` verde
  nos dois modos; `scripts/check-language.sh` verde; `scripts/check-links.sh` verde.
- **NFR3 — Jornada viva** (skill `living-journey`): `docs/jornada/074-prototipo-navegavel.md`
  com capturas geradas do protótipo rodando de verdade por script versionado
  (`docs/jornada/scripts/captura-074.sh`) e heurística de UX datada, no mesmo PR.

## Critérios de aceite

<!-- Sem checkboxes: aqui se declara o que tem de valer; se valeu é o qa-report quem diz. -->

- **Barra do ciclo (decisão 6, gate final por delegação, ADR 0026)**: um crítico em
  contexto fresco **anda** pelo protótipo no browser (não lê HTML), cumprindo as jornadas
  do `ux-design.md` clicando; cada um dos **15 ENTRA** do 073 **mais** as **3 telas da
  regência** é alcançado e sua ação simulada produz o efeito declarado. Passa com
  **nota ≥ 9 por jornada**; vale a **regra das duas rodadas**.
- `prototipo/verifica-navegacao.py` termina verde com as seis verificações (a)–(f) de
  NFR1, e **vermelho** sobre o corpus de mutação (fixture ruim).
- `specs/073-area-administrativa/prototipo/verifica-prototipo.py` termina verde: 11 telas,
  0 achados (FR8).
- `scripts/check-conformance.sh 074` verde nos dois modos; `check-language` e `check-links`
  verdes (NFR2).
- A jornada viva existe com capturas do build real (script versionado) e heurística datada
  (NFR3); se uma correção não estiver integrada no momento da captura, a captura é
  declarada pendente, nunca regerada por cima da evidência anterior.
- O protótipo abre offline (sem rede) pela entrada de `.claude/launch.json` e recarregar a
  página restaura as fixtures (FR4, FR6).

## Fora de escopo

- Servidor novo, banco de dados, chamada real ao harness — o protótipo é estático servido
  por `python -m http.server`.
- Alterar o painel v0 (`painel/`) — o protótipo apenas **lê** dele (`exemplo.json`,
  `schema_workflow.sql`); nenhuma vista existente muda de lugar, nome ou `data-v`.
- Dado pessoal real em qualquer fixture ou tela.
- Push ou merge — o ciclo termina no gate humano; a promoção a `main` é decisão do regente.
- Migrar o painel v0 para os tokens novos (a migração variável a variável é decisão
  futura, declarada no design system §5).

## Clarify

Ambiguidades encontradas e a interpretação tomada (nenhuma decisão da regente foi inventada;
o que é dela continua no briefing):

1. **"3 telas da regência" × quatro elementos** — a fatia 3 do briefing lista
   "frase-chave, kanban por gate, fila, ruling" para "3 telas". Interpretação: a
   frase-chave é a **tela inicial** da casca (decisão 2), não uma tela por contexto; as 3
   telas da Regência são **kanban por gate, fila de decisões e ruling**. Se a regente
   quiser a frase-chave contada como tela do contexto, é um acréscimo declarado no gate de
   spec.
2. **Seis itens de navegação × cinco contextos** — a decisão 2 diz "cada item é um contexto
   delimitado", mas há seis itens e cinco contextos, e "Chamados" e "Fila" são vistas que o
   mapa coloca na Regência (o painel de regência exibe "a fila, os chamados por portão e a
   jornada"). Interpretação: os itens seguem o design system (cinco) **mais** Mensageria;
   o atributo `data-contexto` de cada tela declara um dos **cinco** contextos (verificação
   d da decisão 5), com o kanban e a fila declarando `regencia`. Se a regente quiser
   "Chamados" apontando a um contexto próprio, é decisão dela no gate de UX.
3. **"Os 15 ENTRA alcançados e sua ação simulada"** — quatro ENTRA não têm tela própria de
   propósito (mensagem entre agentes é objeto; colisão de nomes é condição visível;
   auditoria administrativa é seção; custo estimado é coluna). Interpretação: cada ENTRA é
   alcançado **por sua tela** e o elemento que o serve é visível; a "ação simulada"
   aplica-se onde o ENTRA tem ação de escrita — para objeto/seção/coluna, alcançar e ver o
   elemento com o efeito declarado (quando houver) é o critério.
4. **Verificador do 073 sobre os fragmentos** — a decisão 5 diz "além do verificador do
   073 sobre as telas", sem dizer se o `verifica-prototipo.py` passa a percorrer
   `prototipo/telas/` também. Interpretação tomada: o verificador do 073 **continua sobre
   a pasta dele** (FR8, nunca vermelho) e os fragmentos seguem o mesmo contrato, cobrado
   pelo `verifica-navegacao.py`; estender o caminho do verificador do 073 é decisão do
   plano (Gerente), não da spec.
5. **Ponto de quebra da navegação inferior** — "lateral em desktop, inferior em largura
   estreita" sem valor de quebra. Interpretação: o valor exato fica para o `ux-design.md`
   e o design system; a spec só exige as duas formas.
6. **`data-autoriza` no protótipo** — o atributo declara quem autoriza (humano · regente
   por delegação · sessão dona), mas o protótipo não tem autorização de verdade. 
   Interpretação: o atributo é **declarativo** (documenta quem autorizaria no produto); o
   protótipo não bloqueia clique por papel — exceto o caso fixo da decisão 3: o Gerente
   nunca é derrubável pela tela.
7. **Projeto na identidade das fixtures** — o critério de coerência usa
   `Worker03 [ad66d6] · maestro`; o retrato do 073 usa `410_MAESTRO` como projeto.
   Interpretação: o valor do projeto nas fixtures vem de `painel/projetos/exemplo.json` e é
   o **mesmo** em todas as telas; a forma `nome · ref · projeto` é o que a regra 5 verifica.
