# Plan 074 — Protótipo navegável do painel de regência

- **Spec**: `spec.md` (aprovada com ajustes no gate de spec, `gate-spec.md`, 26/10) · **UX**:
  `ux-design.md` (aprovado com ajustes no gate de UX, `gate-ux.md`, 27/10) · **Lane**: plena,
  com o ramo de interface · **Data**: 2026-10-27
- **Siglas** (Princípio VIII, expandidas na 1ª ocorrência): DoD (*Definition of Done*), ADR
  (*Architecture Decision Record*), FR (*functional requirement*, requisito funcional), NFR
  (*non-functional requirement*, requisito não funcional), ENTRA (as funcionalidades que
  **entram** — veredicto do confronto do 073), JSON (*JavaScript Object Notation*), UX
  (*user experience*), CI (*Continuous Integration*, integração contínua), YAGNI (*You Aren't
  Gonna Need It*), CDN (*Content Delivery Network*), DOM (*Document Object Model*), API
  (*Application Programming Interface*), PR (*pull request*), PNG (*Portable Network
  Graphics*).

> A linguagem ubíqua do projeto **existe** — `docs/governance/glossary.md` e o §6 do mapa de
> contextos (`specs/073-area-administrativa/confronto/mapa-de-contextos.md`) — e é a fonte
> obrigatória dos nomes deste plano: todo rótulo de menu, título e botão é termo do glossário.
> Os termos que este ciclo introduz (**frase-chave**, **trilha de contexto**, **aviso de
> simulação** e os quatro verbos **Propor regra**, **Endereçar por ref**, **Registrar ruling**,
> **Drenar outbox**) entram no glossário pela tarefa T12 — em inglês, por ser superfície
> instalável (ADR 0014).

## Constitution Check (governance/principles.md)

| Principle | Compliance |
|---|---|
| I. Spec-driven | Sim — o plano deriva da spec aprovada (B1, B2, S1–S6 aplicados) e do `ux-design.md` aprovado (B-UX1, B-UX2 aplicados); nenhuma tela nasce antes da base da FR7, e nenhuma decisão do briefing §3 é reaberta. Uma mudança de escopo volta à spec antes de virar fragmento. |
| II. Human-governed orchestration | Sim, com a delegação declarada — os gates de spec e de UX foram decididos **por delegação** (ADR 0026), com crítico em contexto fresco; o **gate deste plano é humano** (a regente o aprova antes de qualquer fatia de implementação começar); a barra do ciclo é um crítico em contexto fresco que **anda** pelo protótipo (quem executa não verifica); o gate de merge é humano e não delegável. A emenda ao design system do 073 (T11) só executa quando o julgamento do 073 fechar — decisão que é da regente. |
| III. Reversibility / risk gates | Sim — nada irreversível: o protótipo é artefato novo e isolado (sem servidor novo, sem banco, sem chamada ao harness); o painel v0 (`painel/`) é apenas lido; os wireframes do 073 não são movidos nem editados (FR8). O único toque em artefato de outro ciclo (T11, emenda ao `design-system.md` do 073) é condicionado ao fechamento do julgamento do 073 — nunca durante ele. As ações irreversíveis **da tela** são simuladas e exibem `data-perde`/`data-reverte`: a engenharia de reversibilidade vira conteúdo visível da tela (o Princípio III como requisito de UX). |
| IV. Test-first / verifiable DoD | Sim, com **desvio declarado e justificado**: o verificador `prototipo/verifica-navegacao.py` nasce com as telas, com as nove verificações (a)–(i) e o corpus de mutação (f) que o prova discriminante; o verificador do 073 continua verde sobre a pasta dele (FR8). Dois critérios de aceite — "abre offline" e "recarregar restaura as fixtures" — **não têm verificação por máquina** (S4/S7 do gate de spec): um protótipo estático servido por `python -m http.server` não é verificável offline por leitura de fonte; são **critérios declarados do crítico que anda**, no roteiro da barra (`tasks.md`). A nota ≥ 9 por jornada é julgamento (o portão determinístico mede a saúde; a avaliação é da barra) — a parte determinística é executável e verde antes de qualquer crítico abrir o browser. |
| V. Context economy / boundary | Sim — o corte é por contexto delimitado: um dono por contexto de fragmentos (T03–T06), um arquivo de ações por contexto (`prototipo/acoes/<contexto>.js`, sem edição concorrente do `app.js`), um JSON por agregado com o contrato (`data-model.md`) fixado **antes** das telas — é isso que permite as fatias paralelas sem divergirem. O `app.js` (roteador + motor de ações) é a fronteira do Worker02. A ordem da FR7 (tokens + amostra antes das telas) preserva o contexto: quem desenha fragmento consome tokens medidos, não decide design. |
| VI. Living artifacts | Sim — jornada viva com capturas do build real por script versionado e heurística datada, no mesmo PR (NFR3); CHANGELOG (gate de CI); glossário (T12) alimentando a allowlist do verificador (a regra 2 do 073 lê o glossary.md — o T12 pousa antes do primeiro verde do T09); emenda ao design system (T11) quando o 073 fechar. Nenhuma função duplicada: `contracts/` e `checklist.md` recusados com motivo (abaixo). A cadeia spec 074 ↔ PR ↔ verificadores ↔ jornada fica registrada no qa-report. |
| VII. Light governance / YAGNI | Sim — zero dependência: sem framework, sem build, sem CDN; `python -m http.server` na pasta do protótipo. A constante de quebra 768 px é **comentada e provisória** (a captura a 360 px na jornada viva confirma ou move — não se constrói tooling para isso). Os seis itens de menu são **vistas** sobre os cinco contextos do mapa (B1) — nenhum sexto contexto inventado. A regra das duas rodadas limita o retrabalho da barra ao essencial. |
| VIII. Intelligible communication | Sim — siglas expandidas na primeira ocorrência em cada um dos três documentos deste plano; os termos novos entram no glossário (T12) antes de o verificador cobrá-los; os rótulos curtos ("Políticas", "Orçamento") declaram os termos por extenso nos títulos e no `data-rotulo` (S-f). |

## Artifacts of this cycle (declare all five — silence is not a decision)

| Artifact | Declaration | Why |
|---|---|---|
| `research.md` | `ART:research=no` | nenhum desconhecido técnico: o design system foi **medido** no 073, o padrão de captura foi provado no 072 (`captura-072.sh`) e a FR6 elimina escolha de biblioteca (zero dependência) |
| `data-model.md` | `ART:data-model=yes` | este ciclo cria dados — as fixtures dos oito agregados do mapa; o modelo é o **contrato** que permite as fatias paralelas (este arquivo existe, ao lado deste plano) |
| `contracts/` | `ART:contracts=no` | as duas interfaces do ciclo já têm casa: o contrato de marcação dos botões (`ux-design.md` §5, B-UX1) e o contrato das fixtures (`data-model.md`); um `contracts/` duplicaria função já servida (Princípio VI) |
| `checklist.md` | `ART:checklist=no` | as nove verificações (NFR1) e a tabela ENTRA → tela → elemento (`ux-design.md` §4, 18 linhas) **são** as listas de conferência — a do verificador para a máquina, a do §4 para o crítico que anda; duplicá-las violaria o Princípio VI |
| `ux-design.md` | `ART:ux-design=yes` | existe, aprovado com ajustes (`gate-ux.md`, 27/10) — papel semântico de cada tela antes do componente, jornadas J1–J5, contrato dos botões, quebra 768 px |

## Domain model (declared — o detalhe vive no `data-model.md`)

- `DOM:aggregate=` um JSON por agregado do mapa — **sessão**, **tarefa**, **chamado**,
  **pedido de decisão** (com o Ruling **dentro** do agregado, como no 072), **mensagem**,
  **política**, **orçamento**, **catálogo**.
- `DOM:invariants=` identidade `nome · ref · projeto` em todo texto visível e atributo (regra
  5 do 073) · projeto **`maestro`** em toda tela (S6: `repos[0].nome` de
  `painel/projetos/exemplo.json`) · todo número marcado `(exemplo)` ou com `data-fonte` · `—`
  sempre com motivo · **o Gerente nunca é derrubável** (B2-h; a linha não carrega o botão) ·
  endereço ambíguo **recusado, nunca resolvido** · efeito de ação **só em memória**
  (recarregar restaura as fixtures).
- `DOM:glossary=` `docs/governance/glossary.md` + mapa §6 — existe e é a fonte dos nomes; os
  termos novos entram pela T12 (inglês, ADR 0014).
- `DOM:ports=nenhuma` — o protótipo não serve nem consome API (FR6, offline); as únicas
  "interfaces" são o contrato de marcação (ux-design §5) e o contrato das fixtures
  (data-model.md) — nenhuma rota, porta ou evento novo.

## How (ordem de implementação — a FR7 manda a base antes das telas)

1. **T01 — base da FR7** (Worker02): `prototipo/tokens.css` (tokens medidos do design system
   v1, nomes em português) e `prototipo/amostra.html` (cada componente da §4 do design system
   com os objetos do Maestro), **antes de qualquer fragmento**. A constante de quebra 768 px
   entra como **constante comentada** (não é variável consumível em `@media`), marcada
   provisória até a captura a 360 px.
2. **T02 — casca e motor** (Worker02): `prototipo/index.html` + `prototipo/app.js` — roteador
   `#/contexto/tela` com queda sem erro na tela inicial (FR1), navegação lateral/inferior com
   os seis itens como vistas sobre os cinco contextos (FR2, B1), estado em memória inicializado
   das fixtures (recarregar restaura), **motor de ações**: confirmação irreversível com
   `data-perde`/`data-reverte` (B-UX1), toast e aviso de simulação (`data-aviso="simulado"`,
   `role="status"`). Entrada `prototipo-074` em `.claude/launch.json` (`python -m http.server`
   em `prototipo/`, offline — FR6).
3. **T07 — fixtures** (Worker06, em paralelo às telas): os oito JSON de
   `prototipo/fixtures/`, **um por agregado**, com os valores **já fixados** pelo
   `data-model.md` (o contrato existe antes das telas — as fatias não divergem).
4. **T03–T06 — fragmentos por contexto** (FR3; cada dono com seu `prototipo/acoes/<contexto>.js`):
   - T03 Worker01 — Regência e Chamados: `telas/regencia/inicial.html` (frase-chave),
     `telas/regencia/fila-de-decisoes.html`, `telas/regencia/ruling.html`,
     `telas/chamados-e-gates/kanban-por-gate.html` (reproduzidos do 072 sobre os tokens novos);
   - T04 Worker03 — Mensageria: as 4 telas do 073 viram fragmentos novos (caixa de entrada,
     livro de mensagens, roteamento, protocolo);
   - T05 Worker04 — Administração: as 3 telas (catálogo, políticas, orçamento);
   - T06 Worker05 — Workflow de sessões: as 4 telas (sessão de agente, estado do agente vivo,
     tarefa aberta, consumo por agente).
   Todo fragmento preserva o contrato de marcação do 073 (`data-fonte`, `data-rotulo`,
   `data-exemplo`, `data-referencia`) e a regra 5; os nomes de arquivo são os propostos no
   `ux-design.md` §2. **T12 (glossário, Worker01) corre em paralelo desde já** e pousa antes
   do primeiro verde do T09 — a regra 2 do verificador lê o glossário.
5. **T08 — ações simuladas ponta a ponta** (Worker02, FR4/B-UX1): os 18 elementos da tabela
   §4 do ux-design com o efeito declarado funcionando; as quatro ações irreversíveis
   (reiniciar, derrubar, entregar a destino não resolvido, estourar teto) abrindo a confirmação
   com `data-perde`/`data-reverte`; a linha `Gerente [31ee4d] · maestro` **sem** botão Derrubar
   e com o aviso "portão do regente".
6. **T09 — verificador e corpus** (Worker02, NFR1): `prototipo/verifica-navegacao.py` com as
   nove verificações (a)–(i) e o corpus de mutação (f) — fixture boa passa, fixture ruim
   **faz falhar**. A verificação (g) **importa ou invoca as regras do
   `specs/073-area-administrativa/prototipo/verifica-prototipo.py`** sobre `prototipo/telas/`,
   com 0 achados — **planejado para as seis regras** (as cinco da correção 1 mais a regra 6 do
   roster, que pousa com o fechamento do 073; ver Clarify 1).
7. **T10 — jornada viva** (Worker06, NFR3): `docs/jornada/scripts/captura-074.sh` (o padrão do
   `captura-072.sh`: sobe o servidor de verdade em `prototipo/`, fotografa o DOM renderizado
   com Playwright + Edge do sistema, derruba o servidor ao fim) e
   `docs/jornada/074-prototipo-navegavel.md` com heurística **datada ≥ data da captura**. A
   captura a **360 px** confere se "Administração" cabe a 12 px — é ela que valida (ou move) a
   constante provisória 768 px, no mesmo commit.
8. **T11 — emenda ao design system do 073** (Worker02, condicional): quebra 768 px, trilha
   de contexto, aviso de simulação, "3 a **6** itens" em
   `specs/073-area-administrativa/design-system.md` — **só quando o julgamento do 073 fechar**
   (mandato do gate de UX, decisão 2); nunca durante o julgamento.
9. **T13 — segurança documental e fitness** (Worker06, NFR2): varredura de segredos e dados
   pessoais sobre `prototipo/` e `specs/074-*/`; `scripts/check-conformance.sh 074` nos dois
   modos, `check-language.sh`, `check-links.sh` (com o aviso de lentidão abaixo); evidência por
   acréscimo no `qa-report.md`.
10. **T14 — fechamento** (Gerente): integração, qa-report, **barra** — crítico em contexto
    fresco que **anda** pelas jornadas J1–J5 no browser (os 15 ENTRA + as 3 telas da regência
    alcançados com o efeito simulado; nota ≥ 9 por jornada; regra das duas rodadas; "abre
    offline" e "recarregar restaura" julgados por ele — S4/S7), `[[DONE 074]]` com cópia à
    sessão regente **viva** (MAESTRO — ref corrente conferido no `ListAgents` da hora; hoje
    `[5f2fba]`; o `[7c8d05]` é ref de fixture do roster, nunca destino de DONE) e fallback
    `done-*.md`.

## FR8 — restrição dura: o verificador do 073 nunca fica vermelho

- `specs/073-area-administrativa/prototipo/verifica-prototipo.py` mantém **11 telas · 0
  achados** sobre a pasta dele — conferido **a cada integração** do 074.
- Os wireframes do 073 **não são movidos nem editados** para virarem fragmentos: os fragmentos
  são **arquivos novos** em `prototipo/telas/`.
- WHEN os juízes do 073 pedirem mudança numa tela THEN a mudança entra na tela do 073 **e** no
  fragmento do 074, **pelo mesmo dono**, no mesmo ciclo de correção.
- O `painel/` v0 é apenas **lido** (`exemplo.json`, `schema_workflow.sql`); nenhuma vista
  existente muda de lugar, nome ou `data-v`.

## Environment constraints (medidos nesta máquina — para o implementador não tropeçar)

- **Sem Docker**; **`python3` no bash é o stub da Microsoft Store** — invocar Python sempre
  como **`python`** (o `verifica-navegacao.py` e o `captura-074.sh` já nascem assim).
- **`scripts/check-links.sh` é muito lento no checkout principal** (fork por arquivo; passa de
  5 min) — timeout longo ou o corpo equivalente em Python, como o ciclo 073 já fez.
- As capturas usam **Playwright com o Edge do sistema** (`PW_CHANNEL=msedge`), sem download de
  binário — o padrão do `captura-072.sh`.
- **Captura grava PNG em nome fixo**: nunca regerar por cima de evidência anterior; se a
  correção não está integrada no momento da captura, **declarar a captura pendente** (critério
  de aceite da spec).
- **Write/Edit em `docs/adr/**` é negado a sessões worker** — se este ciclo criar decisão que
  peça ADR, ela sobe ao humano/MAESTRO; nada no plano atual depende disso (as decisões de
  produto são da regente, briefing §3; as de UX estão no ux-design).
- O **ref da sessão muda ao reiniciar**: DONE enviado a ref antigo se perde — na retomada, o
  Gerente manda o ref novo; fallback = commitar `done-*.md` (briefing §6).
- Windows: um escritor por vez no ledger (`docs/governance/task-ledger.md`, limite declarado).

## Verification (DoD)

```bash
python prototipo/verifica-navegacao.py             # verde: nove verificações (a)–(i)
python prototipo/verifica-navegacao.py --mutacao   # vermelho sobre a fixture ruim (corpus (f))
python specs/073-area-administrativa/prototipo/verifica-prototipo.py   # 11 telas, 0 achados (FR8)
scripts/check-conformance.sh 074                   # verde nos dois modos (normal e TICKED_ONLY=1)
scripts/check-language.sh                          # verde
scripts/check-links.sh                             # verde (timeout longo — ver constraints)
```

- **Barra** (gate final por delegação, ADR 0026): crítico em contexto fresco **anda** J1–J5 no
  browser; os 15 ENTRA + as 3 telas da regência alcançados com o efeito simulado declarado;
  nota ≥ 9 por jornada; regra das duas rodadas; critérios declarados S4/S7 ("abre offline",
  "recarregar restaura") julgados por ele — o roteiro está no `tasks.md`.
- Jornada viva com capturas do build real (script versionado) e heurística datada ≥ data da
  captura; a captura a 360 px valida a constante 768 px.
- `qa-report.md` com a evidência de cada cauda (`TAIL:*`) e de cada verificação acima.

## Clarify (para o gate do plano — nada aqui reabre decisão fixa)

1. **Regra 6 do verificador do 073 — divergência registrada e RESOLVIDA em 27/10.** Na
   primeira redação deste plano o script em disco tinha **cinco** regras (o plan-architect o
   leu antes do merge); a regra 6 (roster e ref único por nome) **pousou** com o `2cd7d44`
   (correção 2 do 073, integrada em `4e421a4`) — conferido em disco em 27/10: as seis regras
   estão no `verifica-prototipo.py`, com a cerca de isenção compartilhada das regras 5/6.
   Disco e README agora concordam e o plano **planeja para as seis**, como a spec manda
   (NFR1-(g)). Procedimento que segue valendo: (g) invoca/importa as regras **como estiverem
   no momento da execução**; se o fechamento do julgamento do 073 mudar as regras depois
   disto, o Gerente **declara o estado** no qa-report e sincroniza antes do gate final. Não é
   decisão a tomar — é fato a declarar.
2. **"Derivadas na autoria" (S3) interpretado**: o que **existe** em
   `painel/projetos/exemplo.json` (projeto `maestro`, nomes das equipes, `regencia.pessoas`,
   frentes) vem com `data-fonte`; o que não existe é **fixture `(exemplo)`** com `data-fonte`
   apontando à origem **estrutural** (`schema_workflow.sql`, `painel/regencia/`, data-model do
   072, mapa §7.1). É a leitura que a própria FR5 faz ("todo número é fixture marcada `(exemplo)`
   **ou** vem de exemplo.json com `data-fonte") — registrada no `data-model.md`, não decidida
   aqui.
