# Spec 068 — Chamados gate a gate (o estado vem dos arquivos; o custo vem das sessões)

> **Spec retroativa.** O código já existe: branch `067-painel-chamados`, trecho `db6b89c..2796cbf`,
> 10 commits de 03 a 09/10/2026 pela equipe do projeto Hindiana. Esta spec registra o QUÊ e o
> PORQUÊ que o código obedece, para que o plano, a revisão em contexto fresco e o portão humano
> tenham contra o que medir. Nada aqui foi inventado além do que o trecho faz; o que o código traz
> e a spec não pediu está em "Limites declarados".

- **Status**: Implementado retroativamente na branch `067-painel-chamados` (trecho `db6b89c..2796cbf`); ciclo 068 pela decisão do Darú (decisao-066-daru-20-10) · **Raia**: plena · **Data**: 2026-10-20
- **Origem**: o padrão Hindiana **"um chamado, uma pasta; cada gate, um entregável"**
  (`hindiana/DOCS/processo/padrao-chamado.md`, adotado em 05/10/2026) precisava de uma tela que
  **derivasse o estado dos arquivos** em vez de alguém digitá-lo — o "Estado atual" digitado
  envelhecia em horas (achado do ciclo 066) — e de um **custo por sessão** para o humano ver o
  que cada worker gasta em cada passo.

> **Raia**: plena, não infra. Tudo é texto versionado dentro de `painel/` (um módulo de regras,
> um indexador, uma tela, três rotas), desfeito por `git revert`; nenhum ambiente é tocado e o
> único arquivo gravado (`painel/dados/custo.db`) é cache reconstruível. **Ambiguidade** média
> (as regras do conferidor são precisas; a leitura dos transcripts é a dúvida, ver última seção);
> **raio** amplo (todo projeto instalado que adote o padrão de chamado passa a ter o estado
> calculado por este código); **irreversibilidade** baixa.

## Glossário deste ciclo

| Termo | O que é aqui |
|---|---|
| **Chamado** | Unidade de trabalho do Hindiana: uma pasta `specs/<id>/` com `00-chamado.md` (abertura) e um arquivo por gate. Sucede a "peça" do ciclo 066. |
| **Gate** | Cada um dos passos `abertura, G0, GD, G1 … G9` do padrão. Cada gate tem um dono (quem entrega) e um ou mais arquivos `G<n>-*.md` com cabeçalho. |
| **Veredito** | O arquivo de gate com cabeçalho `gate / objeto / veredito / por / data`. Um veredito **conta** quando passa nas regras do conferidor; senão fica listado com os erros e não muda o estado. |
| **Conferidor** | `scripts/maestro/conferir_chamado.py` do Hindiana, cujas regras `painel/chamados.py` reproduz. |
| **runner2** | Segunda execução da suíte por quem não é autor, registrada no G3 com `numeros: "<suite> passados/falhos/erros"`. |
| **`pendente:`** | Campo do cabeçalho que registra o que ficou para depois num gate que passou. |
| **Classe C** | Classe de risco (gate GD) que exige um ADR (*Architecture Decision Record*, registro de decisão de arquitetura) e a decisão do dono do produto. |
| **BPMN** (*Business Process Model and Notation*, notação de modelagem de processos) | O fluxo do chamado desenhado em `painel/workflow-chamado.bpmn`, servido pelo painel. |
| **Trilha** | A linha do tempo de um chamado: commits e vereditos em ordem, com quem, quando, hash e tokens por passo. Para a IA (*inteligência artificial*) e para auditoria. |
| **Custo por sessão** | Tokens (entrada, saída, cache) por sessão e por minuto, lidos dos transcripts do Claude Code (`~/.claude/projects/<pasta>/*.jsonl`). |
| **Offset** | Posição em bytes até onde cada transcript já foi lido; o índice só lê o que veio depois (incremental). |

## O quê e por quê

### 1. O estado digitado mente; o estado calculado não

O ciclo 066 mostrou que o "Estado atual" digitado pelo agente envelhece. O padrão de chamado
resolve isso na fonte: cada gate deixa um arquivo com cabeçalho, e o estado **é** a leitura dos
arquivos sob regras fixas. O painel passa a calcular, gate a gate, PASSOU / BARRADO / EM CURSO /
FALTA (no código: `ok / bad / run / falta`, mais `na` para gate que não se aplica) e a dizer onde
o chamado está e com quem. Ninguém digita estado; ninguém promove nada (Princípio II).

### 2. As regras são as do conferidor — uma só fonte de verdade

Um veredito só conta se obedece às mesmas regras que o conferidor do Hindiana aplica no
pre-commit. Duas implementações com regras diferentes seriam a cópia com perdas (anti-padrão 22);
por isso cada regra é um requisito abaixo, e cada uma tem um teste nomeado.

### 3. O custo aparece ao lado do passo

Com dezesseis sessões, "quanto custou este chamado" é pergunta diária sem resposta. Os transcripts
já guardam o uso de tokens por mensagem; indexá-los de forma incremental e cruzar com a trilha
dá o custo por passo **como estimativa rotulada** — a sessão pode ter feito outra coisa na janela.

## Requisitos funcionais (FR, de *functional requirement*)

- **FR1 — Estado derivado só dos arquivos.** `painel/chamados.py` DEVERÁ ler cada pasta
  `specs/<id>/` com `00-chamado.md` direto do git (último commit que a tocou, em qualquer branch,
  nos últimos `dias`) e calcular o estado de cada gate. Nenhum campo de estado DEVERÁ vir de
  entrada manual nem de SQLite; o módulo só lê e não grava no projeto.
- **FR2 — Regras do conferidor, uma a uma.** Um veredito só conta se: (a) o cabeçalho traz os
  campos obrigatórios e `objeto` está na forma `<caminho> @ <hash>` sem negrito nem crase, com
  hash existente no repositório; (b) em G1 e G3 o crítico (`por`) **não é autor** da peça;
  (c) a `data` do veredito **não é anterior ao objeto** nem **posterior ao commit do arquivo**
  (hora digitada); (d) quando há vereditos em mais de um hash, **vale o hash do veredito mais
  recente**; (e) `runner2` só conta com **failed 0 e errors 0** em toda trinca de `numeros`;
  (f) G3 passa só com `codigo` APPROVE, `criterio` APPROVE e `runner2` OK **no mesmo hash**, e
  REPROVE/RETURN/FALHA barram; (g) G1 exige 2 APPROVE no mesmo hash (1 se `escopo: correcao`).
- **FR3 — Semântica de `pendente:`.** Um gate com `pendente:` **passa**, e a pendência entra
  na lista do chamado; o G8 (ordem de produção) DEVERÁ ficar EM CURSO até o veredito trazer
  `pendencias_aceitas`. G7 `ADIADO` só conta **com** `pendente:`.
- **FR4 — Gate de classe C.** No GD, `classe: C` sem `adr` **e** decisão do dono DEVERÁ ficar
  EM CURSO com a falta nomeada.
- **FR5 — Vista de tabela (board) chamado × gate.** Ao lado da lista por gate, o `index.html`
  DEVERÁ oferecer a vista "Tabela (board)": uma linha por chamado, uma coluna por gate, o estado
  de cada célula e o dono do gate onde o chamado está.
- **FR6 — Trilha com custo por passo.** `GET /api/chamados/<id>/trilha` DEVERÁ devolver os
  eventos (commits e vereditos) em ordem, cada um com quem, quando, hash, veredito, os erros que
  o fizeram não contar e os tokens da janela; mais métricas (vereditos, reprovações, rodadas de
  G3, horas) e a nota de que o custo é estimativa. A tela mostra a trilha numa aba do chamado.
- **FR7 — Índice de custo incremental.** `painel/custo.py` DEVERÁ ler os transcripts das pastas
  listadas em `custo_pastas` a partir do **offset** gravado por arquivo, somar tokens por sessão e
  minuto em `painel/dados/custo.db`, e ignorar mensagens repetidas pelo mesmo `id` (streaming).
- **FR8 — BPMN como fluxo documentado.** `painel/workflow-chamado.bpmn` DEVERÁ descrever o fluxo
  do chamado e ser servido por `GET /workflow-chamado.bpmn`.
- **FR9 — Testes junto com o código.** `painel/tests/test_chamados.py` DEVERÁ cobrir as regras
  de FR2 e FR3 (6 testes).

## Fora de escopo

- Promover gate, gravar veredito ou aceitar pendência pelo painel — o painel lê; quem assina é
  o dono do gate, no arquivo.
- Substituir o conferidor do Hindiana (o pre-commit continua lá); aqui só a projeção.
- Custo em dinheiro: o índice guarda tokens; preço por modelo é ciclo futuro.
- Sincronizar as regras automaticamente entre `conferir_chamado.py` e `chamados.py` — dívida
  declarada (duas cópias, uma fonte humana).
- Pagar o acoplamento ao Hindiana (nomes de pessoas e pastas) — medido e declarado, pago no 072.

## Artefatos condicionais que o plano DEVERÁ declarar (`docs/governance/artifacts.md`)

| Artefato | Declaração | Motivo em uma linha |
|---|---|---|
| `data-model.md` | `ART:data-model=yes` | Chamado, Gate e Veredito são entidades novas com relações; o índice de custo (`arquivos`, `sessoes`, `uso`) é esquema novo. |
| `contracts/` | `ART:contracts=yes` | Três rotas novas (`/api/chamados`, `/api/chamados/<id>/trilha`, `/workflow-chamado.bpmn`) lidas por outras sessões e pela IA. |
| `ux-design.md` | `ART:ux-design=yes` | Duas vistas novas (board chamado × gate; trilha). Os objetos são os do desenho semântico do painel de regência (branch `066-painel-de-regencia`, a ser renumerada 072) §2 — kanban por gate, jornada por chamado; apontador do v0 em `specs/066-painel-de-coordenacao-v0/ux-design.md`; o `ux-design.md` retroativo deste ciclo é um apontador, como o do 066. |
| `research.md` | `ART:research=no` | Nenhuma incógnita: as regras vêm do conferidor; o formato dos transcripts foi lido do que existe. |
| `checklist.md` | `ART:checklist=no` | A DoD (*Definition of Done*, definição de pronto) abaixo cobre o que há para checar. |

## Para o plano — modelo de domínio (obrigatório desde o 067)

Esta spec não carrega os tokens `DOM:*`; o plano os declara. O que o plano DEVERÁ decidir:

1. **Agregado**: `Chamado` é a raiz; `Gate` e `Veredito` são entidades dentro dele (um gate não
   existe sem chamado; um veredito não existe sem gate).
2. **Invariantes no domínio** (funções puras de `chamados.py`, sem HTTP nem SQLite): `cabecalho`,
   `valida` (regras a–c, e), `numeros_limpos` (regra e), `confere` (regras d, f, g; `pendente:`;
   classe C). O plano diz se alguma regra ficou na borda e por quê.
3. **Glossário**: `changed` — entram chamado, gate, veredito, runner2, pendente, trilha, custo
   por sessão.
4. **Portas**: `changed` — três rotas HTTP; leitor de transcripts (`custo.indexa`) e leitor de
   git (`_git`) como adaptadores.

## Critérios de aceite

- `python -m unittest discover -s painel/tests -p test_chamados.py` → `Ran 6 tests`, `OK`, exit 0.
- Os seis testes são a prova de FR2 e FR3, um por regra:
  `test_passa_com_codigo_criterio_e_runner2_limpo_no_mesmo_hash` (f),
  `test_runner2_com_errors_nao_conta` (e),
  `test_critico_autor_veredito_antes_do_objeto_e_negrito_nao_contam` (a, b, c),
  `test_reprove_barra` (f), `test_correcao_passa_com_um_approve` (g),
  `test_pendente_passa_o_gate_mas_trava_o_g8_ate_ser_aceita` (FR3). Lacunas declaradas, sem
  teste nomeado: regra (c) "data depois do commit do arquivo", regra (d) e FR4 classe C.
- WHEN um veredito de G3 traz `numeros: "pytest 2751/0/14"` THE SYSTEM SHALL listá-lo com o
  erro `runner2 sem 0 failed e 0 errors` e não mudar o estado do G3.
- WHEN o G4 passa com `pendente:` e o G8 traz `ORDEM` sem `pendencias_aceitas` THE SYSTEM SHALL
  marcar G4 `ok` e G8 `run`; com `pendencias_aceitas`, G8 `ok`.
- `grep -c '"G8"' painel/chamados.py` → `≥ 1` (o G8 existe na tabela de gates e na regra de
  pendências; medido: `GATES`, `PASSA`, `BARRA`, `confere`).
- `grep -c 'offset' painel/custo.py` → `≥ 1` (medido: tabela `arquivos`, `seek`, `UPDATE`).
- `grep -c 'bpmn:process' painel/workflow-chamado.bpmn` → `≥ 1`.
- `grep -c '/api/chamados' painel/server.py` → `2` e `grep -c 'workflow-chamado.bpmn' painel/server.py` → `≥ 1`
  (`server.py:429,437,439`).
- `grep -c 'Tabela (board)' painel/index.html` → `1` (`index.html:598`) e
  `grep -c 'Trilha (IA e auditoria)' painel/index.html` → `1` (`index.html:695`).
- `python painel/custo.py painel/projetos/exemplo.json` → exit 0 e um JSON com
  `arquivos_lidos` e `mensagens_novas`. **Pré-condição que o plano fixa**: `exemplo.json` passa a
  carregar `custo_pastas: ["C--Users-ghdaru-Documents-010-PROJETOS-410-MAESTRO"]`, a pasta de
  transcripts deste próprio repositório; sem a chave o padrão do código é `["180-HINDIANA"]` e o
  comando roda com zero arquivos.
- `ls painel/projetos/chamados-manuais-exemplo.json` → existe, e
  `ls painel/projetos/chamados-manuais-hindiana.json` → **não existe** na ponta integrada
  (decidido em decisao-066-daru-20-10: fixture aqui, dado real fica no repositório do Hindiana).
- `grep -c 'veredito_hook.py --pre-commit' .maestro/controle/git-hooks/pre-commit` → `1`.
- Acoplamento ao Hindiana, **medido e declarado como dívida, não critério verde**:
  `grep -n 'Gilsiley' painel/chamados.py` → `chamados.py:28` (`("G8", "Ordem de produção",
  "Gilsiley")`) e `:154-155` (`decisao_gilsiley`); `grep -n 'Hindiana Office\|180-HINDIANA' painel/custo.py`
  → `custo.py:33-34` e `:48`. O critério que vale para o 072 é saída vazia.
- `scripts/check-language.sh` → verde; `scripts/check-conformance.sh 068` → verde após plano,
  tasks e `qa-report.md`.

## Limites declarados

- **Testes depois do código** (Princípio IV), como no 066 e no 067; e três regras sem teste
  nomeado (ver critérios). O plano decide se os testes entram neste ciclo ou no 072.
- **Duas cópias das regras** (`conferir_chamado.py` lá, `chamados.py` aqui). O teste é o contrato
  entre elas; divergência é achado de retro.
- **O custo é estimativa** por janela (da ação anterior da mesma sessão até esta, ou 90 min); a
  resposta diz isso em `metricas.nota`. Nunca se apresenta como medida exata.
- **Leitura do git é lenta** (cerca de 20 s por varredura); há cache em memória de 120 s e a
  tela mostra "atualizando". É desenho, não defeito.
- **Chamados manuais** (`registro: manual`): o JSON de chamados anteriores ao padrão entra na
  lista **sem** passar pelas regras — é o único estado digitado, e fica rotulado como tal.
- **Escopo que o trecho traz e esta spec não pediu**: o cache em thread (`em_cache`) e a
  classificação de atividade por prefixo do commit (`ATIV`). Declarados como entregues.

## Ambiguidades para o Darú

1. **`custo.py` lê `~/.claude/projects/` do usuário.** O filtro é por substring do nome da pasta
   (`custo_pastas`); sem filtro, ou com substring frouxa, ele lê transcripts de **outros
   projetos** da mesma máquina e grava o uso deles em `custo.db`. Isso é aceitável numa
   ferramenta instalada? Opções que a spec não escolhe: exigir `custo_pastas` explícito (falha
   fechada), ou casar o nome inteiro da pasta. → [decisão do Darú]

<!--
  GATE (DoR — não delegável): esta spec só vira plano depois da aprovação do Darú.
  Handoff: spec-agent → (aprovação) → plan-architect.
-->
