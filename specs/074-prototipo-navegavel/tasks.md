# Tasks 074 — Protótipo navegável do painel de regência

> Fatias por dono, diff pequeno, **um commit por fatia** com a mensagem `ciclo 074: <fatia>`.
> O Gerente integra e roda os gates a cada fatia. **Ordem obrigatória** (gate do plano, B3/B4):
> **T01 (Worker02) e T07 (Worker01) começam juntas, já liberadas pelo gate**; T02 após a T01;
> **T12 (glossário) executa ANTES da T03** (mesmo dono, uma tarefa ativa por sessão); **T03–T06
> só após T02 e T07 integrados**. A FR8 vale para toda fatia: o verificador do 073 permanece
> **11 telas · 0 achados** sobre a pasta dele, os wireframes do 073 não são movidos nem
> editados, e os fragmentos são **arquivos novos**.
>
> Siglas (Princípio VIII, expandidas na 1ª ocorrência): FR (*functional requirement*, requisito
> funcional), NFR (*non-functional requirement*, requisito não funcional), ENTRA (as
> funcionalidades que **entram** — veredicto do confronto do 073), DoD (*Definition of Done*),
> ADR (*Architecture Decision Record*), UX (*user experience*), HTML (*HyperText Markup
> Language*), JSON (*JavaScript Object Notation*), DOM (*Document Object Model*), CTA (*call
> to action*, ação principal), PNG (*Portable Network Graphics*), SHA-256 (*Secure Hash
> Algorithm*, variante de 256 bits).

## Base — liberada pelo gate do plano (FR7, FR1, FR2, FR6)

`[[TASK id=074-T01 kind=implement attempt=1 cycle=074]]`

- [ ] T01 — Worker02: `prototipo/tokens.css` (tokens medidos do design system v1, nomes em
  português) e `prototipo/amostra.html` (cada componente da §4 do design system com os objetos
  do Maestro) — **a primeira entrega, antes de qualquer tela** (FR7). A constante de quebra
  **768 px** entra como constante **comentada** em `tokens.css` (a forma exata está no
  `ux-design.md` §6), marcada provisória até a captura a 360 px da jornada viva.
  - DoD: abrir `prototipo/amostra.html` pelo servidor local (`python -m http.server` na pasta
    do protótipo) renderiza **todos** os componentes da §4;
    `grep -ciE "https?://" prototipo/tokens.css prototipo/amostra.html` → **0** (zero
    dependência externa, FR6).

`[[TASK id=074-T02 kind=implement attempt=1 cycle=074]]`

- [ ] T02 — Worker02: `prototipo/index.html` (casca) + `prototipo/app.js` — roteador
  `#/contexto/tela` com queda **sem erro** na tela inicial (FR1); navegação lateral em desktop
  e inferior abaixo de 768 px, com os **seis itens como vistas** sobre os cinco contextos
  (FR2, B1: Regência → inicial; Chamados → kanban `chamados-e-gates`; Fila → `regencia`;
  Sessões → `workflow-de-sessoes`; Administração; Mensageria); estado **em memória**
  inicializado das fixtures (recarregar restaura); **motor de ações** (FR4): confirmação
  irreversível com `data-perde`/`data-reverte` acionada por `data-irreversivel="sim"` +
  `data-confirma="<id>"` (B-UX1), toast e aviso de simulação (`data-aviso="simulado"`,
  `role="status"`). A entrada `prototipo-074` do `.claude/launch.json` **já existe rastreada**
  (o arquivo passa a ser versionado neste PR — decisão da regente; a fatia **não o edita**).
  `app.js` é fronteira do Worker02: os efeitos por contexto vivem em `prototipo/acoes/<contexto>.js`,
  um arquivo por dono (acréscimo declarado aceito, S4 do gate). **Logo depois da T02, antes de
  qualquer tela**: o **esqueleto** do `prototipo/verifica-navegacao.py` com o corpus de mutação
  (f) — o portão nasce antes das telas (S1 do gate); o "primeiro verde" fica para a integração.
  - DoD (conferido na integração, com a T07 já integrada — B4): pela entrada `prototipo-074`,
    a casca abre; rota desconhecida (`#/x/y`) cai na tela inicial **sem erro no console**; o
    `app.js` **carrega as oito fixtures sem erro** (console limpo;
    `python -m json.tool prototipo/fixtures/<arquivo>` → OK em cada uma das oito).

## Fixtures e glossário — em paralelo desde o gate (FR5, S-e)

`[[TASK id=074-T07 kind=implement attempt=1 cycle=074]]`

- [ ] T07 — Worker01 (o Worker06 está na correção 3 do 073 — decisão da regente; começa
  **junto com a T01**, B4): fixtures — os oito JSON de `prototipo/fixtures/` (**um por
  agregado do mapa**: `sessao.json`, `tarefa.json`, `chamado.json`, `pedido-de-decisao.json`,
  `mensagem.json`, `politica.json`, `orcamento.json`, `catalogo.json`), com os valores
  **exatos** do contrato `data-model.md` — ele é a fonte; nada é inventado fora dele. Regra de
  identidade: refs do roster de exemplo do 073 (Gerente `[31ee4d]`, Worker01 `[9a1b27]`,
  Worker02 `[31f7bf]`, Worker03 `[ad66d6]`, Worker04 `[4d000a]`, Worker05 `[78d88f]`,
  Worker06 `[c85948]`, MAESTRO `[7c8d05]`) — **dados de fixture, não os refs vivos**; projeto
  **`maestro`** (`repos[0].nome` de `painel/projetos/exemplo.json`) em toda tela, declarado
  **diferente** do `410_MAESTRO` do roster datado do 073 (S-b); autor humano `Ana Exemplo`
  (`regencia.pessoas`); **nenhum dado pessoal real**; todo número `(exemplo)` ou com
  `data-fonte`; `—` sempre com motivo. O `tarefa.json` inclui **também Worker06 e MAESTRO** —
  `—` com motivo (S5 do gate do plano).
  - DoD: `python -m json.tool prototipo/fixtures/<arquivo>` → OK nas **oito**; conferência
    célula a célula contra o `data-model.md` (a fixture é o contrato em dado).

`[[TASK id=074-T12 kind=docs attempt=1 cycle=074]]`

- [ ] T12 — Worker01: glossário — `docs/governance/glossary.md` (inglês, ADR 0014, coluna
  "Cycle 074"): **frase-chave** (*key phrase*), **trilha de contexto** (*context trail*),
  **aviso de simulação** (*simulation notice*) e as quatro ações como **verbos sobre termos**:
  **Propor regra** (*propose rule*), **Endereçar por ref** (*address by ref*), **Registrar
  ruling** (*register ruling*), **Drenar outbox** (*drain outbox*) — mandato S-e do gate de UX.
  **Executa ANTES da T03** (mesmo dono, uma tarefa ativa por sessão — B3 do gate) e **deve
  pousar antes do primeiro verde do T09** (a regra 2 do verificador do 073 lê o glossário —
  sem os termos novos, os rótulos novos acusariam).
  - DoD: os sete termos novos presentes na coluna "Cycle 074" do `glossary.md`
    (`grep -ciE "key phrase|context trail|simulation notice|propose rule|address by ref|register
    ruling|drain outbox" docs/governance/glossary.md` → **≥ 7**); `scripts/check-language.sh`
    → verde.

## Fragmentos — só após T02 e T07 integrados (FR3, B4)

`[[TASK id=074-T03 kind=implement attempt=1 cycle=074]]`

- [ ] T03 — Worker01: fragmentos da Regência e de Chamados e Gates — `telas/regencia/inicial.html`
  (frase-chave do regente), `telas/regencia/fila-de-decisoes.html`, `telas/regencia/ruling.html`
  (reproduzidos do `painel/index.html` e do ux-design do 072, sobre os tokens novos, com os
  mesmos dados de exemplo) e `telas/chamados-e-gates/kanban-por-gate.html` (colunas G0–G9,
  `data-contexto="chamados-e-gates"` — core domain, B1). Com `acoes/regencia.js` e
  `acoes/chamados-e-gates.js` (filtro por frente com efeito visível; "Detalhar" como expansão
  na própria tela, B-UX2; marcador portão do regente levando à Fila). O ruling é alcançado
  **pela Fila** (CTA "Responder"), nunca solto.
  - DoD: os quatro fragmentos abrem na casca pelas rotas `#/regencia/inicial`,
    `#/regencia/fila-de-decisoes`, `#/regencia/ruling`, `#/chamados-e-gates/kanban-por-gate`;
    `python specs/073-area-administrativa/prototipo/verifica-prototipo.py` → **11 telas, 0
    achados** (FR8); regras 5/6 verdes nos fragmentos (o esqueleto do
    `verifica-navegacao.py` roda sobre eles sem achado novo).

`[[TASK id=074-T04 kind=implement attempt=1 cycle=074]]`

- [ ] T04 — Worker03: fragmentos da Mensageria — `telas/mensageria/caixa-de-entrada.html`,
  `livro-de-mensagens.html`, `roteamento.html`, `protocolo.html` (reproduzem os wireframes do
  073 **sem movê-los nem editá-los** — arquivos novos). Com `acoes/mensageria.js`:
  "Drenar outbox" (pontos somem, contador zera), "Enviar ao endereço ambíguo" com a
  confirmação irreversível (`data-perde`/`data-reverte`) **antecedendo** a recusa com pedido de
  desambiguação (J5). A tabela de resolução nome → ref mantém a cerca
  `data-rotulo="colisão de nomes"` e a isenção declarada na própria tela.
  - DoD: os quatro fragmentos abrem na casca pelas rotas `#/mensageria/<tela>`;
    `python specs/073-area-administrativa/prototipo/verifica-prototipo.py` → **11 telas, 0
    achados** (FR8); regras 5/6 verdes nos fragmentos (esqueleto do verificador sem achado
    novo).

`[[TASK id=074-T05 kind=implement attempt=1 cycle=074]]`

- [ ] T05 — Worker04: fragmentos da Administração — `telas/administracao/catalogo.html`,
  `politicas.html`, `orcamento.html` (reproduzem os wireframes do 073, arquivos novos). Com
  `acoes/administracao.js`: "Propor regra" (ask) — toast "simulado" + link "ver na fila"; a
  proposta **vira pedido de decisão** (propor não executa); "Ajustar teto" — a barra recalcula
  contra o teto novo e muda de cor, com **nova linha no histórico de mudanças** (`changed_by`).
  Seção "Agentes (perfis)" no catálogo (o cadastro é o arquivo versionado; a tela **lê**,
  `data-fonte: ls .claude/agents`). Uma linha de fixture do histórico visível ao crítico nas
  **três** telas (ENTRA 12, auditoria administrativa).
  - DoD: os três fragmentos abrem na casca pelas rotas `#/administracao/<tela>`;
    `python specs/073-area-administrativa/prototipo/verifica-prototipo.py` → **11 telas, 0
    achados** (FR8); regras 5/6 verdes nos fragmentos (esqueleto do verificador sem achado
    novo).

`[[TASK id=074-T06 kind=implement attempt=1 cycle=074]]`

- [ ] T06 — Worker05: fragmentos do Workflow de sessões —
  `telas/workflow-de-sessoes/sessao-de-agente.html`, `estado-do-agente-vivo.html`,
  `tarefa-aberta.html`, `consumo-por-agente.html` (reproduzem os wireframes do 073, arquivos
  novos). Com `acoes/workflow-de-sessoes.js`: "Reiniciar" (irreversível: o ref muda; aviso "o
  ref muda ao reiniciar"), "Derrubar" (irreversível com confirmação; linha passa a caída) — e a
  linha `Gerente [31ee4d] · maestro` **sem botão Derrubar**, com o aviso "portão do regente"
  (B2-h). Segmento de período como botão de escrita (`data-autoriza="humano"`,
  `data-simulado="sim"`); coluna "estimado" no consumo (fonte: preço do modelo no catálogo).
  - DoD: os quatro fragmentos abrem na casca pelas rotas `#/workflow-de-sessoes/<tela>`;
    `python specs/073-area-administrativa/prototipo/verifica-prototipo.py` → **11 telas, 0
    achados** (FR8); regras 5/6 verdes nos fragmentos (esqueleto do verificador sem achado
    novo).

## Integração e verificação (FR4, NFR1, NFR3)

`[[TASK id=074-T08 kind=implement attempt=1 cycle=074]]`

- [ ] T08 — Worker02: ações simuladas **ponta a ponta** — cada um dos 18 elementos da tabela
  §4 do `ux-design.md` (15 ENTRA + 3 telas da regência) com o efeito declarado funcionando no
  browser; as quatro ações irreversíveis (reiniciar, derrubar, entregar a destino não
  resolvido, estourar teto) abrindo a confirmação com `data-perde`/`data-reverte` (B-UX1);
  nenhum `data-acao="derrubar"` com `data-alvo` começando por `Gerente` (B2-h) **e todo
  `data-acao="derrubar"` declarando `data-alvo`** (S9 do gate); todo botão de escrita (S1) com
  os quatro atributos da decisão 3. Efeitos **só em memória** — recarregar restaura as
  fixtures.
  - DoD: as verificações (c), (h) e (i) do `python prototipo/verifica-navegacao.py` → verdes
    sobre os 18 elementos; efeito visível no browser para cada um (declarado no qa-report).

`[[TASK id=074-T09 kind=test attempt=1 cycle=074]]`

- [ ] T09 — Worker02: `prototipo/verifica-navegacao.py` — falha alto nas **nove verificações**
  (a)–(i) do NFR1: (a) todo `href="#/…"` e `data-vai-para` resolve; (b) toda tela alcançável em
  ≤ 3 cliques (grafo com a inicial como **raiz**, incluindo as arestas dos seis itens — S2);
  (c) todo botão de escrita com os quatro atributos; (d) `data-contexto` em exatamente os cinco
  valores do mapa; (e) nenhum `<link>`/`<script>` **externo** — `<script src>` **local** é
  aceito (S4); (f) **corpus de mutação** com fixture boa/ruim — o verificador tem de **falhar**
  com a ruim; (g) os fragmentos passam nas regras do `verifica-prototipo.py` do 073 —
  **IMPORTADAS com `importlib`** (nome de arquivo com hífen), reutilizando o parser e os
  termos do glossário dele, percorrendo `prototipo/telas/**/*.html`, 0 achados, **o arquivo do
  073 não é editado** (S8; a regra 1 dele vale nos links da trilha); (h) nenhum
  `data-acao="derrubar"` com o Gerente como alvo (via `data-alvo`) **e todo
  `data-acao="derrubar"` declarando `data-alvo`** (S9); (i) todo botão irreversível aponta
  para uma confirmação existente com `data-perde` e `data-reverte`. **Mensagens e docstring em
  inglês** (S12, ADR 0014). Python invocado como **`python`** (o `python3` do bash é stub da
  Microsoft Store nesta máquina).
  - DoD: `python prototipo/verifica-navegacao.py` → verde nas nove (a)–(i);
    `python prototipo/verifica-navegacao.py --mutacao` → **vermelho** sobre a fixture ruim
    (corpus (f) prova que discrimina).

`[[TASK id=074-T10 kind=docs attempt=1 cycle=074]]`

- [ ] T10 — Worker06: jornada viva (skill `living-journey`) —
  `docs/jornada/scripts/captura-074.sh` (padrão do `captura-072.sh`: sobe o servidor de verdade
  em `prototipo/`, fotografa o DOM renderizado com Playwright + Edge do sistema —
  `PW_CHANNEL=msedge` —, derruba o servidor ao fim) e
  `docs/jornada/074-prototipo-navegavel.md` com **heurística datada ≥ data da captura**. A
  captura a **360 px** confere se "Administração" cabe a 12 px — valida (ou move, no mesmo
  commit) a constante provisória 768 px. **Nunca regerar PNG por cima de evidência anterior**:
  se uma correção não está integrada no momento da captura, declarar a captura **pendente**.
  - DoD: os PNGs das capturas existem em `docs/jornada/`, gerados pelo script versionado
    (datas conferíveis); a data da heurística é **≥** a data da captura; a captura a 360 px
    declara o veredito da constante 768 px.

## Condicional — mandato dos gates (só após o julgamento do 073 fechar)

`[[TASK id=074-T11 kind=docs attempt=1 cycle=074]]`

- [ ] T11 — Worker02: emenda ao `specs/073-area-administrativa/design-system.md` — quebra
  **768 px** (constante comentada, não token de `@media`), **trilha de contexto**,
  **aviso de simulação** (anatomias mínimas do `ux-design.md` §2.5) e a §4 passando a ler
  "3 a **6** itens". Mandato do gate de UX (decisão 2) e do gate de spec. **Só executa quando
  o julgamento do 073 fechar** — nunca durante; se os juízes do 073 pedirem mudança de tela,
  ela entra na tela do 073 **e** no fragmento do 074, pelo mesmo dono (FR8). **T11 pendente
  não bloqueia o DONE** — o estado fica declarado no qa-report (S10 do gate).
  - DoD: o `design-system.md` do 073 com a emenda;
    `python specs/073-area-administrativa/prototipo/verifica-prototipo.py` → **11 telas, 0
    achados** (a emenda não regrediu nada).

## Fechamento (NFR2, barra, DONE)

`[[TASK id=074-T13 kind=audit attempt=1 cycle=074]]`

- [ ] T13 — Worker06: segurança documental e fitness — varredura de segredos e dados pessoais
  sobre `prototipo/` e `specs/074-prototipo-navegavel/` (falsos positivos declarados, como no
  073); NFR2: `scripts/check-conformance.sh 074` verde nos **dois modos** (normal e
  `--ticked-only` — o modo é a flag; a variável de ambiente é ignorada), `scripts/check-language.sh`
  verde, `scripts/check-links.sh` verde (com timeout longo — o script é lento no checkout
  principal). Evidência **por acréscimo** no `qa-report.md`.
  - DoD: `scripts/check-conformance.sh 074` → verde; `scripts/check-conformance.sh 074
    --ticked-only` → verde; `scripts/check-language.sh` → verde; `scripts/check-links.sh` →
    verde (timeout longo); varredura de segredos → 0 achados reais (falsos positivos
    declarados).

`[[TASK id=074-T14 kind=review attempt=1 cycle=074]]`

- [ ] T14 — Gerente: integração, `qa-report.md`, **barra** e DONE. A barra (gate final por
  delegação, ADR 0026): crítico em **contexto fresco** que **anda** pelo protótipo no browser
  (não lê HTML), cumprindo as jornadas J1–J5 do `ux-design.md` clicando; cada um dos
  **15 ENTRA + 3 telas da regência** alcançado com o efeito simulado declarado (lista de
  conferência: tabela §4); **nota ≥ 9 por jornada**; **regra das duas rodadas**. `[[DONE 074]]`
  com cópia à sessão regente **viva, conferida no `ListAgents` na hora** — nenhum ref de
  sessão é fixado em documento versionado (S3 do gate; o `[7c8d05]` é ref de fixture do roster,
  nunca destino de DONE) — e fallback commitado em `specs/074-prototipo-navegavel/done-*.md`.
  - DoD: o qa-report com a evidência de cada cauda (`TAIL:*`) e de cada verificação; a barra
    com nota ≥ 9 por jornada; o DONE entregue (com fallback commitado se o envio falhar).

### Critérios declarados ao crítico que anda (S4/S7 do gate de spec — não verificáveis por máquina)

1. **Abre offline**: com a rede desconectada, o protótipo abre pela entrada `prototipo-074` do
   `.claude/launch.json` e toda navegação e ação simulada funciona (FR6).
2. **Recarregar restaura**: executar uma ação simulada (por exemplo, "Registrar ruling"),
   recarregar a página e conferir que o estado volta ao das fixtures — o efeito era só em
   memória (FR4).
3. A **frase-chave** propaga o efeito entre telas (J1 passos 5–6: o contador passa a 2 na
   volta à tela inicial) — coerência entre contextos, lida no browser.

## Closing tail — MANDATORY, one line each, never delete
<!-- TICK ONLY WHILE WRITING THE EVIDENCE, never in advance: the box records what happened.
     Do not delete a line to say it does not apply: write `n/a: <reason>` on it.
     check-conformance.sh requires the evidence of every non-n/a step in qa-report.md. -->
- [ ] TAIL:review — independent review in fresh context, by whoever did not execute: a barra
      (crítico que **anda** J1–J5, tabela §4 como lista de conferência) **mais** revisão fresca
      do diff contra o plano
- [ ] TAIL:security — security pass proportional to the risk class: segurança documental
      (segredos, dados pessoais) sobre `prototipo/` e `specs/074-*/`; sem superfície de rede
      além do `http.server` local — a passagem é documental, como no 073
- [ ] TAIL:mutation — o gate novo é mutado e visto recusando: (1) o corpus (f) — fixture ruim
      faz o `verifica-navegacao.py` falhar; (2) **cegar regras** do verificador novo (pelo
      menos (h) e (d)) por quem **não** o escreveu, em contexto fresco, copiar os achados que
      sumiram, restaurar byte a byte (SHA-256 conferido) — evidência no qa-report
- [ ] TAIL:gate — DoD green -> guardian verdict -> human merge gate (not delegable)
