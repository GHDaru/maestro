# Spec NNN — Painel de coordenação v0 (projeção dos arquivos, só localhost)

> **Spec retroativa.** O código já existe: branch `painel-controle`, ponta `a1172a2`, 12 commits
> entre 01 e 03/10/2026, pela equipe do projeto Hindiana, instalado e em uso diário lá. Esta spec
> registra o QUÊ e o PORQUÊ que o código obedece, para que o plano, a revisão em contexto fresco
> e o portão humano tenham contra o que medir. Nada aqui foi inventado além do que a branch faz.

- **Status**: Implementado retroativamente na branch `painel-controle` (`a1172a2`); número do ciclo pendente da decisão do Darú · **Raia**: plena · **Data**: 2026-10-19
- **Origem**: escala do projeto Hindiana (29/09 a 01/10/2026): 16 sessões simultâneas, cerca de
  160 worktrees, 52 desvios de método registrados em três dias, 28 decisões numa única noite. Essa
  escala tornou obsoleta a linha "Metrics dashboard — Later / YAGNI" do
  `docs/governance/operating-model.md` §6 (linha 145). Este ciclo a **supera em parte**, por um
  ADR (*Architecture Decision Record*, registro de decisão de arquitetura) de número pendente — o
  próximo livre é o 0022. Rascunho de origem: `proposta.md` e `adr-rascunho-painel.md` da
  Hindiana Assistente (01/10/2026).

> **Raia**: plena. **Ambiguidade** média (o painel entra onde o método dizia "não"; três decisões
> só o Darú toma, ver seção final); **raio** amplo (um diretório novo no toolkit, um hook de
> pre-commit, uma tabela que só cresce e uma superfície HTTP/MCP lida por outros agentes);
> **irreversibilidade** baixa por desenho (apagar `painel/` e reverter três linhas de documentação
> desfaz tudo; o único dado que não se reconstrói é a tabela `eventos`, e ela nunca é apagada).

## Glossário deste ciclo

| Termo | O que é aqui |
|---|---|
| **SQLite** (*SQL* — *Structured Query Language* — *lite*, banco de dados em um arquivo) | O arquivo `.db` local que o painel lê. Aqui ele é **projeção**, nunca fonte. |
| **CQRS** (*Command Query Responsibility Segregation*, separação entre escrita e leitura) | O padrão que o painel segue: os arquivos recebem a escrita; o SQLite é o modelo de leitura reconstruível. |
| **MCP** (*Model Context Protocol*, protocolo de contexto de modelo) | Protocolo pelo qual um agente consulta ferramentas. `mcp_painel.py` é um servidor MCP por entrada e saída padrão (stdio). |
| **DORA** (*DevOps Research and Assessment*, as quatro métricas de entrega) | Frequência de deploy, tempo de entrega, taxa de falha e tempo de recuperação. O painel mostra cada número com a fonte ao lado. |
| **HTTP** (*Hypertext Transfer Protocol*) · **JS** (*JavaScript*) · **CLI** (*command-line interface*, interface de linha de comando) | O servidor local, o único `index.html`, e o `registrar.py`. |
| **stdlib** (biblioteca padrão do Python) | `sqlite3`, `http.server`, `subprocess`. Sem dependência externa. |
| **Peça** | Unidade de entrega do Hindiana que atravessa o fluxo spec → red → entregue → suítes aceitas → aprovada às cegas → integrada → em produção. |
| **Veredito** | Arquivo de veredito de auditoria do Hindiana (`.maestro/controle/`), que o hook de pre-commit obriga a carregar carimbo de tempo verificável. |

## O quê e por quê

### 1. O controle estava espalhado e desatualizava

O estado de um projeto conduzido por dezesseis sessões vivia em dez arquivos e nas mensagens
entre sessões: decisões, retro, barra, quadro, relatório da manhã, roteiro de ciclos. O "Estado
atual" de cada sessão era **digitado pelo próprio agente** e envelhecia em horas. O desvio mais
caro (teste verde que não passa pelo caminho real) e o mais perigoso (dez branches com upstream
em `origin/main`, achadas em 01/10) eram invisíveis até alguém procurar à mão.

### 2. O YAGNI do painel valia sem escala

O operating-model §6 recusava um painel de métricas: "sem a quem comparar, instrumentar é débito
prematuro". A premissa era um humano regendo poucos agentes. Com dezesseis, o custo de coordenação
já é medido, e o "a quem comparar" existe: a barra de cada peça e o histórico do próprio projeto.

### 3. O que muda — e o que NÃO muda

O painel **não instrumenta código nem produção**. Ele lê o que o método já obriga a escrever
(specs, ADRs, retro, barra, git) e reconstrói tudo do zero a cada ingestão. O descarte custa o
mesmo que a adoção: um diretório. Isso é o que o separa do débito que o YAGNI temia.

## Princípios de desenho (não se discutem — `proposta.md` §2)

1. **Os arquivos são a fonte de verdade; o SQLite é projeção** reconstruível (ADR 0008, CQRS).
2. **Só entra direto no SQLite o que não existe em arquivo nenhum**: status de sessão, sinal de
   vida, transição de peça com evidência, deploy, incidente, recuperação. Esses fatos vão para a
   tabela `eventos`, **só-acréscimo**: triggers recusam `UPDATE` e `DELETE`.
3. **Sem prova parseável, a peça não muda de estado.** Cada estado exige sua evidência (entregue:
   hash; suítes aceitas: hash + runner2; aprovada às cegas: hash + par montado por + descrição
   factual; integrada: hash + merge; em produção: hash + deploy). Faltou, o registro é recusado.
4. **O painel nunca promove nada** (Princípio II). Quem promove assina em `autor`.
5. **Merge não é deploy.** DORA conta só deploy registrado; merge aparece como proxy rotulado.
6. **Ingestão segura**: nunca abre `.env` nem backups; nunca escreve nos arquivos do projeto; não
   guarda host, IP (*Internet Protocol*, endereço de rede), usuário ou token.
7. **Leveza**: stdlib, um `index.html` com JS puro, sem build, **só localhost**.

## Requisitos funcionais (FR, de *functional requirement*)

- **FR1 — Ingestão reconstrutível.** `painel/ingest.py <projeto.json>` DEVERÁ apagar e
  reconstruir toda tabela derivada a partir dos arquivos do projeto, preservando apenas `eventos`.
  Duas ingestões seguidas sem mudança nos arquivos DEVERÃO produzir projeção idêntica.
- **FR2 — Tabela `eventos` só-acréscimo.** Triggers no SQLite DEVERÃO recusar `UPDATE` e
  `DELETE` em `eventos`. Todo evento DEVERÁ carregar `autor` e carimbo de tempo.
- **FR3 — Registro com evidência.** `painel/registrar.py <projeto.json> peca|status|deploy ...`
  (CLI) DEVERÁ recusar, com saída diferente de zero, qualquer transição de peça cuja `--evidencia`
  não contenha os campos exigidos pelo estado-alvo (lista do princípio 3).
- **FR4 — Servidor local.** `painel/server.py <projeto.json>` DEVERÁ servir só em `127.0.0.1`
  (porta padrão 8765) o `index.html` e as rotas de leitura (`/api/...`), incluindo
  `GET /api/estado-ia?sessao=<id>`, o estado derivado de uma sessão para a IA.
- **FR5 — Servidor MCP.** `painel/mcp_painel.py` DEVERÁ expor por stdio a mesma leitura do
  estado derivado, para que uma sessão consulte em vez de digitar o próprio "Estado atual".
- **FR6 — Telas.** O `index.html` DEVERÁ mostrar: board de agentes (estado, o que faz, idade do
  último sinal, alerta de sem sinal); fluxo de peças com selos de evidência; specs e roadmap;
  decisões e ADRs; DORA com a fonte ao lado de cada número e "—" quando falta registro; barra,
  defeitos e desvios; tempo por fase; higiene do git (lista de remoção **para aprovação**, nunca
  executada); relatório de lote; documentos do projeto com idade; linguagem ubíqua.
- **FR7 — Projeto por configuração.** Um projeto novo entra com um `painel/projetos/<nome>.json`
  que lista os caminhos a ingerir. Nada do Hindiana fica fixo no código.
- **FR8 — Hook de veredito.** `.maestro/controle/git-hooks/veredito_hook.py` (pre-commit)
  DEVERÁ recusar o commit de um arquivo de veredito sem carimbo de tempo verificável, e deixar
  passar os que o trazem.
- **FR9 — Testes junto com o código.** `painel/tests/test_painel.py` (12 testes) e a suíte do
  hook (34 testes) DEVERÃO cobrir, no mínimo, um teste por regra do princípio 6 e os triggers de
  `eventos`.

## Fora de escopo

- Promover peça, remover worktree, fazer merge ou deploy a partir do painel — o painel lê e
  registra; a ação é do humano.
- Autenticação, rede, exposição fora de localhost, múltiplos usuários.
- Medir DORA por merge, por commit ou por qualquer proxy não rotulado.
- Instalar o painel por `install-maestro.sh` ou empacotá-lo no plugin (decisão de ciclo futuro).
- As skills candidatas da proposta (`evidence-gate`, `critica-as-cegas`, `dora-from-git`,
  `higiene-git`, `estado-atual-derivado`) — cada uma é ciclo próprio.
- Arquivar ou reviver os 28 documentos parados do Hindiana — decisão do projeto, não do método.
- Reescrever o livro (`docs/handbook/02-dora-space.md`, capítulo 08): o ADR aponta; o texto
  do livro é ciclo editorial à parte.

## Artefatos condicionais que o plano DEVERÁ declarar (`docs/governance/artifacts.md`)

| Artefato | Declaração | Motivo em uma linha |
|---|---|---|
| `data-model.md` | `ART:data-model=yes` | A tabela `eventos` (campos, tipos de evento, evidência por estado) e as tabelas de projeção são entidades novas com relações. |
| `contracts/` | `ART:contracts=yes` | As rotas HTTP (`/api/...`) e as ferramentas MCP são interface entre o painel e outras sessões — é o que torna o trabalho paralelo seguro. |
| `ux-design.md` | `ART:ux-design=yes` | Tem tela: o `index.html` com onze visões. Papel semântico antes do componente; agente `ux-semantics`. |
| `research.md` | `ART:research=no` | Nenhuma incógnita técnica: stdlib, SQLite e HTTP local já estavam decididos pelo princípio 7. |
| `checklist.md` | `ART:checklist=no` | A DoD (*Definition of Done*, definição de pronto) abaixo cobre o que há para checar. |

## Critérios de aceite

- `python -m unittest discover -s painel/tests` → `Ran 12 tests`, `OK`, exit 0.
- Suíte do hook de veredito (`python -m unittest discover -s .maestro/controle/git-hooks` ou o
  comando que o plano fixar) → `Ran 34 tests`, `OK`, exit 0.
- WHEN `registrar.py <fixture.json> peca --peca P1 --estado entregue` é chamado **sem**
  `--evidencia` THE SYSTEM SHALL sair com código diferente de zero e não inserir linha em `eventos`.
- WHEN `registrar.py <fixture.json> peca --peca P1 --estado "suites aceitas" --evidencia '{"hash":"abc"}'`
  (sem `runner2`) THE SYSTEM SHALL sair com código diferente de zero.
- WHEN `registrar.py <fixture.json> peca --peca P1 --estado "suites aceitas" --evidencia '{"hash":"abc","runner2":"r2"}' --autor X`
  THE SYSTEM SHALL sair com 0 e `SELECT COUNT(*) FROM eventos` crescer em 1.
- `sqlite3 <db> "UPDATE eventos SET autor='x'"` → erro de trigger, exit diferente de zero;
  `sqlite3 <db> "DELETE FROM eventos"` → erro de trigger, exit diferente de zero. Um teste em
  `test_painel.py` prova cada um.
- WHEN `ingest.py` roda sobre uma fixture que contém um arquivo `.env` com a string
  `CANARIO_SEGREDO` e um diretório `backups_producao/` com a mesma string THE SYSTEM SHALL
  terminar com `grep -c CANARIO_SEGREDO <db>` = 0. Um teste em `test_painel.py` prova isso.
- WHEN `ingest.py` roda duas vezes seguidas sobre a mesma fixture THE SYSTEM SHALL produzir
  `.dump` idênticos nas tabelas derivadas (`diff` vazio), com `eventos` intacta.
- `git -C <fixture> status --porcelain` antes e depois de `ingest.py` → saída idêntica (a
  ingestão não escreve no projeto).
- `grep -rE "^(import|from) " painel/*.py painel/tests/*.py | grep -vE "sqlite3|http|json|subprocess|os|sys|re|pathlib|datetime|argparse|unittest|hashlib|urllib|collections|typing|time|shutil|tempfile|textwrap|functools|io|socketserver|html|uuid|dataclasses|glob|logging|contextlib|statistics|fnmatch"`
  → vazio (só stdlib; o plano pode fechar a lista).
- `grep -nE "0\.0\.0\.0|\"\"|''\s*,\s*8765" painel/server.py` → vazio e
  `grep -c "127.0.0.1" painel/server.py` ≥ 1 (só localhost).
- WHEN `GET /api/estado-ia?sessao=W04` é chamado com o servidor de pé sobre a fixture THE SYSTEM
  SHALL responder 200 com JSON contendo `estado`, `peca` e `proximo_passo`.
- WHEN um commit inclui um arquivo de veredito sem carimbo de tempo THE SYSTEM SHALL (pre-commit)
  sair com código diferente de zero; com carimbo válido → 0. Dois testes da suíte do hook provam.
- `grep -rn "hindiana" painel/*.py` → vazio (nada do projeto fixo no código; só em `projetos/*.json`).
- `grep -nE "merge" painel/*.py` em linhas que alimentam DORA → cada ocorrência acompanhada do
  rótulo `proxy` na saída (o plano fixa o grep exato; a tela mostra "proxy" ao lado).
- `scripts/check-language.sh` e `scripts/check-boundary.sh` → verdes (o segundo depende da
  decisão 2 do Darú).
- `scripts/check-conformance.sh <NNN>` → verde após o plano, as tasks e o `qa-report.md`.

## Limites declarados

- **Testes da v0 escritos depois do código** (desvio 2 da proposta, Princípio IV). Registrado
  aqui e no ADR; a partir da v2 do Hindiana, teste vermelho antes. A spec retroativa não apaga
  o fato — o `qa-report.md` o cita.
- **Sem registro, o painel mostra o vazio**: board "sem registro", DORA "—". É desenho, não
  defeito: o painel nunca inventa número.
- **Status de sessão depende de disciplina** (quem grava: a sessão ao mudar, o loop cobra quem
  ficou sem sinal). O painel só mostra o que foi gravado.
- **Windows**: `http.server` e `sqlite3` funcionam; o hook de pre-commit depende de `python` no
  caminho do Git Bash. O plano registra como foi medido.

## Ambiguidades para o Darú

Só ele decide; a spec não inventa.

1. **Número do ciclo.** Esta spec usa o placeholder `NNN` no diretório e no título. Qual é o
   número? (O 066 está em `066-painel-de-regencia`; o ADR vai para o 0022.) → pendente.
2. **Fronteira.** `painel/` e `.maestro/` entram em `boundary.json` no domínio **toolkit**
   (lidos por máquina), como a proposta sugere? Hoje nenhum dos dois consta, e
   `check-boundary.sh` reprova caminho não classificado. → pendente.
3. **Dado real num repositório público.** `painel/projetos/hindiana.json` traz caminhos e nomes
   do projeto Hindiana. Substituir por uma fixture (`painel/projetos/exemplo.json`) e manter o
   real fora do repositório, ou manter como primeiro exemplo? → pendente.

<!--
  GATE (DoR — não delegável): esta spec só vira plano depois da aprovação do Darú.
  Handoff: spec-agent → (aprovação) → plan-architect.
-->
