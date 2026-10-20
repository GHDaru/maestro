# Plan 068 — Chamados gate a gate (o estado vem dos arquivos; o custo vem das sessões)

- **Spec**: `spec.md` (retroativa; ciclo 068 pela decisão `decisao-066-daru-20-10`) · **Raia**: plena
  · **Data**: 2026-10-20 · **ADR** (*Architecture Decision Record*, registro de decisão de
  arquitetura): nenhum — ver § How, decisão 7.

> **Plano retroativo.** O código já está integrado nesta branch: o merge `120a32c` trouxe a
> branch `067-painel-chamados` (trecho `db6b89c..2796cbf`, 10 commits de 03 a 09/10/2026) em
> `painel/chamados.py` (420 linhas), `painel/custo.py` (143), `painel/index.html` (+287),
> `painel/server.py` (três rotas, linhas 429, 437 e 439), `painel/workflow-chamado.bpmn` (643),
> `painel/tests/test_chamados.py` (6 testes) e `.maestro/controle/git-hooks/pre-commit`. Na
> resolução do conflito: `painel/projetos/hindiana.json` continua apagado, o
> `chamados-manuais-hindiana.json` real (1133 linhas) saiu e entrou a fixture
> `chamados-manuais-exemplo.json`; `exemplo.json` ganhou `chamados`, `chamados_manuais` e
> `custo_pastas`. Este plano não decide a arquitetura — ela está no diff — mas registra o COMO
> contra o qual a revisão em contexto fresco e o portão humano medem.

## Constitution Check (governance/principles.md)

| Principle | Compliance |
|---|---|
| I. Spec-driven | ✅ Nove requisitos funcionais (FR, de *functional requirement*) lidos do diff numa spec retroativa; o que o trecho traz e a spec não pediu (cache em thread `em_cache`, classificação `ATIV`) está em spec § Limites, entregue como está. Um desvio de forma: a spec aponta o `ux-design.md` do 066 em `specs/066-painel-de-regencia/`, pasta que não existe — o arquivo real é `specs/066-painel-de-coordenacao-v0/ux-design.md`; corrigir a spec é a tarefa T9, não este plano. |
| II. Human-governed orchestration | ✅ O painel **só lê**: ninguém promove gate, grava veredito nem aceita pendência pela tela — quem assina é o dono do gate, no arquivo, e o pre-commit do Hindiana continua sendo o portão. O `com_quem` de cada chamado nomeia o humano ou a sessão responsável pelo gate onde ele parou. Merge deste ciclo é gate do Darú. |
| III. Reversibility / risk gates | ✅ Desfazer é `git revert 120a32c`: tudo é texto versionado em `painel/`; o único arquivo gravado (`painel/dados/custo.db`) é cache reconstruível a partir dos transcripts. Raio amplo (todo projeto instalado que adote o padrão de chamado), irreversibilidade baixa — raia plena, não infra. A classe de risco da passagem de segurança é **média** porque `custo.py` lê o diretório pessoal do usuário (§ How, decisão 8). |
| IV. Test-first / verifiable DoD | ❌ **Violado**: os testes vieram **depois** do código na linha paralela (03 a 09/10), como no 066 e no 067; e três regras ficaram **sem teste nomeado** — regra (c) "data do veredito depois do commit do arquivo" (`chamados.py:130-133`), regra (d) "vale o hash do veredito mais recente" (`:189-190`) e FR4 classe C (`:151-155`). Os 6 testes existentes são verdes (`Ran 6 tests OK`) e a DoD (*Definition of Done*, definição de pronto) abaixo é executável. Vai para **Complexity Tracking**. |
| V. Context economy / boundary | ✅ Três fatias com fronteira clara: (1) `chamados.py` + testes — regras puras, sem HTTP (*Hypertext Transfer Protocol*) nem SQLite (*Structured Query Language lite*, banco em um arquivo); (2) `custo.py` — adaptador de transcripts, que lê cada `.jsonl` **a partir do offset gravado** e em blocos de 32 MB, nunca o arquivo inteiro de novo (economia de contexto na própria ferramenta); (3) `server.py` + `index.html` + BPMN — borda e tela. `check-boundary.sh` verde após o merge. |
| VI. Living artifacts | ✅ O BPMN (*Business Process Model and Notation*, notação de modelagem de processos) **não duplica** nada: é o fluxo documentado que o painel implementa, servido pela própria tela (`/workflow-chamado.bpmn`) e lido pelo visualizador — artefato consumido, não desenho solto. As tabelas de estado (`GATES`, `PASSA`, `BARRA`) são a mesma lista de gates que o BPMN desenha; divergência entre os dois é achado de retro. Este plano, as tasks, `data-model.md`, `contracts/`, o apontador de UX e o `qa-report.md` fecham a cadeia spec ↔ pull request ↔ testes. |
| VII. Light governance / YAGNI | ✅ **Este ciclo não acrescenta regra ao método**: ele é código de aplicação (um módulo de regras, um indexador, uma tela, três rotas) e não muda template, portão, skill nem constituição. `principles.md § Governance` exige ADR para "decisão material de metodologia" — não há nenhuma aqui; por isso **nenhum ADR** é devido, ao contrário do 067, que criou um bloco de portão e teve de escrever o ADR 0023. O que YAGNI (*You Aren't Gonna Need It*, não vai precisar) podou: sincronização automática das regras com o conferidor, custo em dinheiro, promoção de gate pela tela. |
| VIII. Intelligible communication | ✅ A spec traz glossário próprio; este plano expande cada sigla na primeira ocorrência; os termos novos do domínio entram em `docs/governance/glossary.md` (tarefa T8), não ficam órfãos no código. |

**Complexity Tracking:**

- **Princípio IV — testes depois do código, e três regras sem teste nomeado.** Inevitável aqui
  porque o ciclo é retroativo: o trecho `db6b89c..2796cbf` pré-existe. O que torna a violação
  **limitada**: (a) declarada na spec (§ Limites, item 1) e aqui; (b) as três regras moram em
  trechos curtos e puros de `confere` (`chamados.py:130-133`, `:189-190`, `:151-155`),
  testáveis com a mesma fixture de `test_chamados.py`; (c) o `qa-report.md` registra a lacuna
  como **dívida**, não como verde. **Decisão do plano**: os três testes **não entram neste
  ciclo** (raia retroativa, diff mínimo — anti-padrão 10) e vão para a lista de dívidas do
  painel de regência (072), onde já vale "teste vermelho antes de cada mudança no painel"
  (plano 066). Nomes propostos para o 072: `test_data_depois_do_commit_do_arquivo_nao_conta`,
  `test_vale_o_hash_do_veredito_mais_recente`, `test_classe_c_sem_adr_fica_em_curso`. O
  portão humano decide se aceita.

## Artifacts of this cycle (declare all five — silence is not a decision)

<!-- Read by scripts/check-conformance.sh. Declaring =yes means the file MUST exist here.
     What each one is for: docs/governance/artifacts.md -->

| Artifact | Declaration | Why |
|---|---|---|
| `research.md` | `ART:research=no` | Nenhuma incógnita: as regras vêm do conferidor do Hindiana; o formato dos transcripts foi lido do que existe em `~/.claude/projects/`. |
| `data-model.md` | `ART:data-model=yes` | Chamado, Gate e Veredito são entidades novas com relações; o índice de custo (`arquivos`, `sessoes`, `uso`) é esquema novo. Arquivo: `data-model.md`. |
| `contracts/` | `ART:contracts=yes` | Três rotas novas lidas por outras sessões e pela IA (*inteligência artificial*), a CLI (*command-line interface*) de `custo.py`, o JSON (*JavaScript Object Notation*) de chamados manuais e o BPMN como contrato do fluxo. Arquivo: `contracts/interfaces.md`. |
| `checklist.md` | `ART:checklist=no` | A DoD abaixo cobre o que há para checar. |
| `ux-design.md` | `ART:ux-design=yes` | Duas vistas novas (tabela chamado × gate; trilha). Os papéis semânticos são os do `specs/066-painel-de-coordenacao-v0/ux-design.md` (kanban por gate, jornada por peça); o `ux-design.md` deste ciclo é um **apontador** para lá, como o do 066 — tarefa T10. |

## Domain model (declare all four — silence is not a decision)

<!-- Read by scripts/check-conformance.sh (block 3b). Source of truth for the terms:
     docs/governance/glossary.md. Keep the itemized form out of this table (ADR 0023). -->

| Decision | Declaration | Why |
|---|---|---|
| Aggregate root | `DOM:aggregate=Chamado` | `Chamado` é a raiz: `Gate` e `Veredito` são entidades dentro dele (um gate não existe sem chamado, um veredito não existe sem gate) e toda consulta entra pela raiz — `confere` recebe a pasta inteira do chamado e devolve o chamado com seus gates e itens; `trilha` é lida por `id` de chamado. `Trilha` é uma vista derivada da raiz, não um agregado. |
| Where the invariants live | `DOM:invariants=domain` | Todas as regras do conferidor moram em funções puras de `painel/chamados.py`, sem HTTP nem SQLite: `cabecalho` (parse do cabeçalho), `valida` (regras a, b, c-primeira-metade e e, linhas 81-109), `numeros_limpos` (regra e, 67-71) e `confere` (regras c-segunda-metade, d, f, g, semântica de `pendente:` e classe C, 112-230). Nenhuma regra ficou na borda: `server.py:437-440` só despacha para `em_cache` e `trilha`; `le_chamados` e `_git` são adaptadores que entregam texto ao domínio. |
| Ubiquitous language | `DOM:glossary=changed` | Entram em `docs/governance/glossary.md` (tarefa T8, em inglês): chamado, gate, veredito, conferidor, runner2, pendente, classe C, trilha e custo por sessão — definições em `spec.md § Glossário deste ciclo`. O termo "peça" do 066 é sucedido por "chamado" onde o padrão de pasta se aplica. |
| Ports and adapters | `DOM:ports=changed` | Três portas HTTP novas (`GET /api/chamados`, `GET /api/chamados/{id}/trilha`, `GET /workflow-chamado.bpmn`); dois adaptadores de entrada novos — o leitor de git (`chamados._git` e `le_chamados`) e o leitor de transcripts (`custo.indexa`, com `custo.janela` como porta de consulta) —; e uma porta de configuração nova no `projeto.json` (`chamados`, `chamados_manuais`, `custo_pastas`) mais o arquivo de chamados manuais. Contratos em `contracts/interfaces.md`. |

**Nota sobre a linguagem ubíqua.** O documento do projeto é `docs/governance/glossary.md`; os
nomes deste plano vêm da spec § Glossário e vão para lá — este plano não inventa nome de
passagem. O domínio do Hindiana (nomes de pessoas e de pastas) **não** entra no glossário do
Maestro: é acoplamento declarado (§ Dívidas, item 1).

## How

**1. Estado derivado, nunca digitado (FR1).** `le_chamados` pede ao git o último commit, em
qualquer branch e nos últimos `dias`, que tocou `specs/<id>/00-chamado.md`, `G*.md` ou
`spec.md`, e lê cada arquivo com `git show` (`chamados.py:247-266`). `confere` recebe
`{nome: texto}` e um `data_hash` e devolve o chamado completo; é a mesma função que os testes
chamam com fixtures — a borda não participa. Exceção única e rotulada: chamados manuais
(`registro: manual`), que entram sem passar pelas regras (`:281-292`).

**2. Vale o hash do veredito mais recente (regra d).** Em G3, os vereditos válidos são
agrupados por hash e o grupo escolhido é o de **data máxima** (`:186-190`); só dentro dele se
exige `codigo` APPROVE, `criterio` APPROVE e `runner2` OK (regra f). Uma rodada antiga aprovada
não salva uma rodada nova reprovada. Nos gates simples vale `validos[-1]` (ordem de nome).

**3. runner2 só conta com failed 0 e errors 0 (regra e).** `numeros_limpos` exige ao menos uma
trinca `passados/falhos/erros` e todas com `0/0` no fim; `valida` transforma a falha em erro do
item (`:107-108`), que o deixa listado sem contar. Teste: `test_runner2_com_errors_nao_conta`.

**4. `pendente:` passa o gate mas trava o G8 (FR3).** Cada gate válido com `pendente:` entra em
`pendencias`; G8 com `ORDEM` e pendências sem `pendencias_aceitas` fica `run` com a falta
nomeada (`:213-215`). G7 `ADIADO` sem `pendente:` fica `run` (`:216-217`). Teste:
`test_pendente_passa_o_gate_mas_trava_o_g8_ate_ser_aceita`.

**5. Custo por offset (FR7).** `custo.indexa` guarda em `arquivos (caminho, offset, sessao,
ultimo_id)` até onde leu; na próxima corrida faz `seek(offset)` e só processa o que veio depois,
em blocos de 32 MB cortados na última quebra de linha (`custo.py:57-79`); mensagens repetidas
pelo streaming são ignoradas por `id` (`:94-97`). `trilha` consulta `custo.janela` por sessão e
janela de tempo e rotula o resultado como estimativa (`metricas.nota`).

**6. BPMN como fluxo documentado (FR8).** `workflow-chamado.bpmn` tem 12 raias e os gates
`G0`, `GD`, `G1`…`G9` como `exclusiveGateway`; é servido como `application/xml` e desenhado pela
aba da tela. Não é cópia das tabelas de `chamados.py`: as tabelas dizem **o que faz um gate
passar**, o BPMN diz **quem faz o quê entre os gates**. As duas listas de gates têm de
coincidir — critério da DoD.

**7. Nenhum ADR.** `principles.md § Governance`: "toda decisão material de metodologia vira
ADR". Este ciclo não decide metodologia — não toca template, portão, skill, agente nem
constituição; é uma feature do painel. O 067 precisou do ADR 0023 porque criou uma regra
cobrada por portão; o 068 não cria regra. A decisão de desenho "estado derivado, nunca
digitado" já está gravada na spec e no `data-model.md` do 066 (CQRS, *Command Query
Responsibility Segregation*, separação entre comando e consulta) e aqui só se estende.

**8. Ambiguidade para o Darú — leitura de `~/.claude/projects/` (não decidida aqui).**
`pastas_do_projeto` filtra as pastas por **substring** (`custo.py:46-49`: `any(f in
os.path.basename(p) for f in filtros)`), com padrão `["180-HINDIANA"]` quando `custo_pastas`
falta. Numa ferramenta instalada, uma substring frouxa (`"maestro"`) lê transcripts de **outros
projetos** da mesma máquina e grava o uso deles em `custo.db`. Este plano **não decide**: registra
a ambiguidade e o padrão seguro recomendado para um ciclo posterior — `custo_pastas` obrigatório
(falha fechada, sem padrão do Hindiana) e casamento pelo **nome inteiro** da pasta, não por
substring. A fixture `exemplo.json` já usa o nome inteiro
(`C--Users-ghdaru-Documents-010-PROJETOS-410-MAESTRO`) — por isso o comando da DoD lê só este
repositório. Decisão: [decisão do Darú]; dívida 3 abaixo.

**9. Apontador de UX.** A spec cita `specs/066-painel-de-regencia/ux-design.md §2`; a pasta
real é `specs/066-painel-de-coordenacao-v0/`. O `ux-design.md` deste ciclo aponta para o
arquivo real e nomeia os dois papéis semânticos novos (tabela chamado × gate = kanban por gate
transposto; aba de trilha = jornada por peça com custo), sem portão de UX novo — a
heurística datada fica para o 072, quando a tela for capturada do build real (`living-journey`).

### Como foi medido no Windows

Windows 11, Git Bash (não PowerShell) para `scripts/check-*.sh`; `python3` é shim para o
`python` do Windows; `PYTHONUTF8=1` no ambiente; `core.autocrlf=false` no worktree. Os testes
rodam com `python -m unittest discover -s painel/tests -p test_chamados.py` a partir da raiz
(o `sys.path.insert` do teste resolve `import chamados`). Códigos de saída lidos com `echo $?`
no Git Bash. `custo.py` expande `~` para `%USERPROFILE%`; a pasta de transcripts deste
repositório existe nesta máquina (5 arquivos lidos, 311 mensagens novas em 20/10).

### Dívidas (entregues ao 072, painel de regência)

1. **Acoplamento ao Hindiana, medido**: `chamados.py:28` (`"Gilsiley"` em `GATES`) e `:154-155`
   (`decisao_gilsiley`); `custo.py:33-34` (`"Hindiana Office"`) e `:48` (padrão
   `["180-HINDIANA"]`). Critério do 072: `grep -n 'Gilsiley' painel/chamados.py` e
   `grep -n 'Hindiana Office\|180-HINDIANA' painel/custo.py` com saída vazia — dono do gate e
   nome canônico vêm do `projeto.json`.
2. **Três regras sem teste nomeado** (Complexity Tracking): regra (c) segunda metade, regra (d),
   FR4 classe C.
3. **Padrão de privacidade de `custo_pastas`** (decisão 8): obrigatório e por nome inteiro.
4. **`unittest.main()` antes de `TestPendencia`** em `test_chamados.py:69-70`: `discover` acha
   as três classes, mas `python painel/tests/test_chamados.py` direto roda só duas. Mover o
   bloco para o fim.
5. **Duas cópias das regras** (`conferir_chamado.py` lá, `chamados.py` aqui): o teste é o
   contrato; divergência é achado de retro, não deste ciclo.

## Verification (DoD)

Medido em 20/10/2026 neste worktree (`integra/linha-paralela-066`), Git Bash; o `qa-report.md`
cola a saída de cada linha.

| Comando | Esperado |
|---|---|
| `python -m unittest discover -s painel/tests -p test_chamados.py; echo $?` | `Ran 6 tests`, `OK`, `0` |
| `grep -c 'def test_' painel/tests/test_chamados.py` | `6` (os seis nomes da spec § Critérios) |
| `python -m unittest discover -s painel/tests -p test_painel.py` | `Ran 12 tests`, `OK` (nada regrediu) |
| `grep -c '"G8"' painel/chamados.py` | `≥ 1` (`GATES`, `PASSA`, `BARRA`, `confere`) |
| `grep -c 'offset' painel/custo.py` | `≥ 1` (tabela `arquivos`, `seek`, `UPDATE`) |
| `grep -c 'bpmn:process' painel/workflow-chamado.bpmn` | `≥ 1` |
| `grep -o 'exclusiveGateway id="G[0-9D]"' painel/workflow-chamado.bpmn \| sort -u \| wc -l` | `10` — `G0`–`G7`, `G9`, `GD`; o **G8 não é gateway** no BPMN, é `bpmn:userTask id="T_ordem"` (linha 329): a ordem de produção é tarefa humana. `GATES` tem 11; a decisão 6 ("as duas listas coincidem") vale para os 10 gateways, e o G8 fica declarado como exceção |
| `grep -c '/api/chamados' painel/server.py` · `grep -c 'workflow-chamado.bpmn' painel/server.py` | `2` · `≥ 1` (`server.py:429,437,439`) |
| `grep -c 'Tabela (board)' painel/index.html` · `grep -c 'Trilha (IA e auditoria)' painel/index.html` | `1` (`:598`) · `1` (`:695`) |
| `python painel/custo.py painel/projetos/exemplo.json; echo $?` | JSON com `arquivos_lidos` e `mensagens_novas`; `0` (segunda corrida: `arquivos_lidos` menor ou `0` — prova do offset) |
| `grep -c 'custo_pastas' painel/projetos/exemplo.json` | `1` (nome inteiro da pasta, decisão 8) |
| `ls painel/projetos/chamados-manuais-exemplo.json; ls painel/projetos/chamados-manuais-hindiana.json painel/projetos/hindiana.json 2>&1 \| grep -c 'No such'` | existe · `2` |
| `grep -c 'veredito_hook.py --pre-commit' .maestro/controle/git-hooks/pre-commit` | `1` |
| `grep -n 'Gilsiley' painel/chamados.py` · `grep -n 'Hindiana Office\|180-HINDIANA' painel/custo.py` | `:28`, `:154-155` · `:33-34`, `:48` — **dívida 1, não verde** |
| `scripts/check-language.sh` · `check-links.sh` · `check-boundary.sh` · `check-adr.sh` | verdes (medido em 20/10 após o merge) |
| `grep -c 'Cycle 068' docs/governance/glossary.md` (após T8) | `≥ 8` |
| `scripts/check-conformance.sh 068` (após plano, tasks, `qa-report.md`) | imprime `domain model declared (aggregate, invariants, glossary, ports) with a reason`; verde |

<!--
  GATE (not delegable): o plano é aprovado pelo Darú antes de virar tasks.
  Handoff: plan-architect → (aprovação) → tasks → dev-implementer / qa.
-->
