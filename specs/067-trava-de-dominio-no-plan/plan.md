# Plan 067 — Trava de domínio no plan (o modelo de domínio é declarado, nunca omitido)

- **Spec**: `spec.md` (retroativa; ciclo 067 pela decisão `decisao-066-daru-20-10`) · **Raia**: plena
  · **Data**: 2026-10-20 · **ADR** (*Architecture Decision Record*, registro de decisão de
  arquitetura): nenhum escrito neste plano — ver § How, decisão 5.

> **Plano retroativo.** O código já está integrado nesta branch: o merge `b5775ac` trouxe a
> branch `trava-dominio-plan` (ponta `db6b89c`; commits `14f77a5`, `a94574a`, `db6b89c`), em
> 4 arquivos: `.specify/templates/plan-template.md` (+22, seção "Domain model"),
> `scripts/check-conformance.sh` (+62, bloco 3b), `painel/server.py` (+12/−5, filtro de
> ambiente no `v_dora`) e `painel/index.html` (contador "N sem plan ou tasks"). Este plano não
> decide a arquitetura — ela está no diff — mas registra o COMO contra o qual a revisão em
> contexto fresco e o portão humano medem. **Este é o primeiro ciclo acima do piso 67**: o
> próprio plano carrega os quatro tokens `DOM` que o portão passou a cobrar, e é sobre ele
> que a mutação do portão roda.

## Constitution Check (governance/principles.md)

| Principle | Compliance |
|---|---|
| I. Spec-driven | ✅ Seis requisitos funcionais (FR, de *functional requirement*) lidos do diff numa spec retroativa; nada aqui vai além do que a branch faz. O que o código traz e a spec não pediu (contador "N sem qa-report", `14f77a5`) está declarado na spec § Limites e entregue como está. |
| II. Human-governed orchestration | ✅ O portão lê a **forma** da declaração (valor + motivo), nunca julga o **conteúdo**: se o agregado existe e se o motivo da borda é bom continua sendo juízo da revisão em contexto fresco e do Darú. O piso é um botão que o humano só aperta, nunca afrouxa. O merge deste ciclo é gate do Darú. |
| III. Reversibility / risk gates | ✅ Desfazer é `git revert b5775ac` (3 arquivos de texto versionado, nenhum dado migrado, nenhum ambiente tocado) — por isso raia plena, não infra (spec § Raia). Raio amplo (todo ciclo ≥ 067 em todo projeto instalado), irreversibilidade baixa; falha **soft**, para que o gate não vire um vermelho perene (decisão 1). Gate humano de merge é proporcional. |
| IV. Test-first / verifiable DoD | ❌ **Violado**: `db6b89c` muda `v_dora` (`painel/server.py:150-158`) **sem teste** do filtro de ambiente — `test_dora_nao_conta_merge_como_deploy` prova "merge não é deploy", não "staging não é deploy"; os 12 testes do painel continuam 12. O bloco 3b do portão não tem teste unitário (convenção do repositório para `scripts/*.sh`: a prova é a mutação, corolário C2) — essa parte é verificável pela `TAIL:mutation`. A DoD (*Definition of Done*, definição de pronto) abaixo é executável. Vai para **Complexity Tracking**. |
| V. Context economy / boundary | ✅ Três fatias com fronteira clara e sem dependência entre si: (1) template + portão (método, domínio `toolkit`), (2) `index.html` (tela), (3) `v_dora` em `server.py` (leitura). Cada commit de origem toca uma fatia; o painel não conhece o portão e o portão não conhece o painel. `check-boundary.sh` verde após o merge. |
| VI. Living artifacts | ✅ O token `DOM` só existe porque `check-conformance.sh` o **consome** (teorema T5): não é documentação solta. Este plano, as tasks, o `qa-report.md` e os termos novos no glossário fecham a cadeia spec ↔ pull request ↔ mutação. CHANGELOG e roadmap: tarefa T9 confere se o merge já os tocou. |
| VII. Light governance / YAGNI | ✅ **Este ciclo acrescenta uma regra ao método**, e `principles.md` exige argumentá-la contra a camada de axiomas: ela deriva de **T6** (correção que não vira regra se repete — o Hindiana corrigiu em conversa uma rodada inteira com regras em rotas; só a regra versionada sobrevive à próxima sessão) e de **T4/C7** (norma sem executável é norma sem efeito — o template sozinho seria ceremônia; por isso o portão lê o token), com o mecanismo de **C12** (o que sobrevive à compactação é o que está num artefato consumido — mesma lógica dos `ART` do ciclo 042). O que YAGNI (*You Aren't Gonna Need It*, não vai precisar) podou: nenhum capítulo nem skill de DDD (*Domain-Driven Design*, projeto dirigido pelo domínio), nenhuma validação de conteúdo, nenhuma coluna nova no painel, nenhum reescrever dos planos 042–066. Custo: 22 linhas de template + 62 de script. |
| VIII. Intelligible communication | ✅ A spec traz glossário próprio; este plano expande cada sigla na primeira ocorrência; os cinco termos de DDD que o template passa a exigir entram no glossário do projeto (`DOM:glossary`, tarefa T8), não ficam órfãos no template. |

**Complexity Tracking:**

- **Princípio IV — testes depois do código, e o filtro de ambiente do DORA (*DevOps Research
  and Assessment*, as quatro métricas de entrega) sem teste.** Inevitável aqui porque o ciclo
  é retroativo: `db6b89c` pré-existe (03/10/2026, Hindiana). O que torna a violação
  **limitada**: (a) declarada na spec (§ Limites, item 4) e aqui; (b) o filtro é uma linha
  (`server.py:158`) atrás de `_ambiente` (`server.py:141`), reversível por revert; (c) o
  `qa-report.md` registra a lacuna como **dívida**, não como verde. **Decisão do plano**: o
  teste **não entra neste ciclo** (raia retroativa, diff mínimo — anti-padrão 10) e vai para a
  lista de dívidas do painel de regência (072), onde já vale "teste vermelho antes de cada
  mudança no painel" (plano 066). O portão humano decide se aceita.

## Artifacts of this cycle (declare all five — silence is not a decision)

<!-- Read by scripts/check-conformance.sh. Declaring =yes means the file MUST exist here.
     What each one is for: docs/governance/artifacts.md -->

| Artifact | Declaration | Why |
|---|---|---|
| `research.md` | `ART:research=no` | Nenhuma incógnita técnica: a forma dos tokens e dos pisos copia o que o portão já faz desde 042/055/061. |
| `data-model.md` | `ART:data-model=no` | Nenhuma entidade nova: os tokens são texto num template; o painel não ganha coluna nem tabela. |
| `contracts/` | `ART:contracts=no` | Nenhuma rota, porta ou evento novo; os tokens são lidos do disco pelo mesmo script que já lê `ART:*`. |
| `checklist.md` | `ART:checklist=no` | A DoD abaixo cobre o que há para checar. |
| `ux-design.md` | `ART:ux-design=no` | O painel muda um contador e um filtro em telas que o ciclo 066 já desenhou (`ux-design.md` de lá); nenhum papel semântico novo, nenhuma visão nova. |

## Domain model (declare all four — silence is not a decision)

<!-- Read by scripts/check-conformance.sh (block 3b) from cycle 067 on — this cycle is the
     first one charged. Source of truth for the terms: docs/governance/glossary.md. -->

| Decision | Declaration | Why |
|---|---|---|
| Aggregate root | `DOM:aggregate=none` | O ciclo muda um template e um script de portão; não há agregado de negócio. O "domínio" aqui é o próprio método, e o método não tem raiz de agregado — tem artefatos consumidos por portões. |
| Where the invariants live | `DOM:invariants=edge(a regra "todo plan ≥ 067 declara os quatro tokens com motivo" mora em scripts/check-conformance.sh:353-399, bloco 3b, um script de portão, porque as invariantes do método são aplicadas por portões e não por uma camada de domínio — não existe camada de domínio onde ela pudesse morar)` | Borda **decidida**, não por descuido: o Maestro aplica invariantes de método em `scripts/check-*.sh` desde o ciclo 042 (C7), e é isso que a mutação prova. |
| Ubiquitous language | `DOM:glossary=changed` | Cinco termos entram em `docs/governance/glossary.md` (tarefa T8): modelo de domínio declarado, raiz de agregado, invariante, porta/adaptador, linguagem ubíqua — o template os exige de todo projeto instalado, logo precisam de definição onde o projeto guarda a sua língua. |
| Ports and adapters | `DOM:ports=none` | Nenhuma porta aberta nem adaptador mudado: o portão lê `plan.md` do disco pelo mesmo caminho dos `ART`; o painel lê o mesmo SQLite (*Structured Query Language lite*, banco em um arquivo) e serve as mesmas rotas; `registrar.py` não ganha campo. |

**Nota sobre a linguagem ubíqua.** O documento do projeto é `docs/governance/glossary.md`;
os nomes deste plano (raiz de agregado, invariante, borda, porta/adaptador, piso) vêm da spec
§ Glossário e vão para lá — este plano não inventa nome de passagem.

## How

**1. Falha soft, não hard (FR2).** O bloco 3b usa `soft` (reprova na corrida padrão, só nota em
`--ticked-only`), como os `ART`. Motivo: o `qa-report.md` de todo ciclo é esqueleto até o
fim, e um portão vermelho durante a vida inteira de cada branch é um portão que as pessoas
aprendem a rolar para baixo — lição do ciclo 043, gravada em `scripts/promote-main.sh:32-36`:
a conformidade é cobrada **na promoção**, onde a alegação precisa valer. Um `hard` aqui
reproduziria o anti-padrão que o 043 removeu.

**2. Piso 67, e só aperta (FR3).** `DOM_FLOOR="${MAESTRO_MIN_CYCLE_DOMAIN:-67}"`
(`check-conformance.sh:57-67`). 67 é o primeiro ciclo **depois** do achado de 03/10: cobrar
retroativamente os planos 042–066 transformaria o portão em ruído (precedente de
`check-cycle.sh` e dos pisos 42/45/55/61). A variável só aceita número ≤ 67 e aborta com
código 2 fora disso: um piso que falha **aberto** não é um botão, é um furo — mesmo
precedente de `ABSENCE_FLOOR`. Um `MAESTRO_MIN_CYCLE_DOMAIN=60` apertando o 066 é o teste de
que o botão funciona (DoD).

**3. Forma itemizada das invariantes (FR4, `a94574a`).** `domain` e `edge` globais não bastam
quando um ciclo tem três regras e uma delas precisa ficar na rota (validação de entrada, só
leitura): `regra_a=domain | regra_b=edge(porquê)` obriga a decisão **por regra**, e o item
`=edge` sem parênteses reprova nomeando o item (`check-conformance.sh:369-389`). Sem a forma
itemizada, o ciclo ou declararia `edge` para tudo (perde informação) ou `domain` (mente).
**Limite medido**: o separador dos itens é `|`, o mesmo da tabela Markdown — a forma
itemizada só funciona numa linha de tabela se a célula "Why" ficar **vazia** (o `|` da célula
vira item e reprova). Registrar como dívida (§ Dívidas, item 3).

**4. Painel aponta quem pulou; DORA só produção (FR5, FR6).** `index.html:293,299` conta
specs sem `tem_plan` ou sem `tasks_total` — é a spec que pulou o passo onde o domínio se
decide. `v_dora` (`server.py:150`) filtra `_ambiente(e) in ("", "production", "producao",
"produção")` (`server.py:158`); ausente conta como produção para não apagar os deploys
anteriores à regra — compatibilidade que também é furo (§ Dívidas, item 2).

**5. Decisão de método → ADR.** Este ciclo muda o método (nova declaração obrigatória no
plano e novo bloco no portão). `CLAUDE.md` manda decisão de metodologia virar ADR + linha em
`docs/records/decisoes.jsonl`. O merge `b5775ac` **não** trouxe ADR. Este plano não o escreve
(fora do seu escopo de arquivo); fica como tarefa T10 para decisão do gerente/Darú: escrever
"ADR 0023 — modelo de domínio declarado no plan, cobrado pelo portão a partir do 067" ou
registrar a ausência como dívida no `qa-report.md`.

### Como foi medido no Windows

Windows 11, Git Bash (não PowerShell) para `scripts/check-*.sh`; `python3` é shim para o
`python` do Windows; `PYTHONUTF8=1` no ambiente; `core.autocrlf=false` no worktree (o `grep`
do bloco 3b lê `plan.md` com `sed -E` — um `\r` no fim da linha entraria no motivo, inócuo,
mas num item `=edge(...)\r` quebraria a regex `\)$`). Códigos de saída lidos com `echo $?`
no Git Bash, não `$LASTEXITCODE`.

### Dívidas (entregues ao próximo ciclo que tocar o painel ou o portão)

1. **Teste do filtro de ambiente do DORA**: `test_dora_nao_conta_staging_como_deploy` —
   evento `deploy` com `ambiente: staging` fora da frequência; `production` e ausente dentro.
   Dono: ciclo 072 (painel de regência).
2. **`ambiente` ausente conta como produção** (`_ambiente` → `""`): decisão do Darú em ciclo
   posterior — exigir o campo em `registrar.py` ou manter a compatibilidade. Fora desta spec.
3. **Forma itemizada × célula "Why"** na mesma linha de tabela (decisão 3): ou o template
   documenta "célula vazia na forma itemizada", ou o portão para de ler a célula como item.
4. **Códigos de saída desiguais** entre pisos (domínio: 2; ausência/mutação: 1) — manutenção
   do portão, não deste ciclo.

## Verification (DoD)

Medido em 20/10/2026 neste worktree (`integra/linha-paralela-066`), Git Bash; o
`qa-report.md` cola a saída de cada linha.

| Comando | Esperado |
|---|---|
| `grep -c 'DOM:' .specify/templates/plan-template.md` | `4` (`plan-template.md:66-69`) |
| `grep -c '^## Domain model' .specify/templates/plan-template.md` | `1` |
| `MAESTRO_MIN_CYCLE_DOMAIN=abc scripts/check-conformance.sh 067; echo $?` | saída contém `is not a number`; `2` |
| `MAESTRO_MIN_CYCLE_DOMAIN=99 scripts/check-conformance.sh 067; echo $?` | saída contém `above the built-in floor 67`; `2` |
| `MAESTRO_MIN_CYCLE_DOMAIN=60 scripts/check-conformance.sh 066` | bloco 3b roda sobre o 066 e imprime `domain model never declared in plan.md` |
| `scripts/check-conformance.sh 066` | verde; imprime `domain-model declarations: not checked below cycle 67` |
| `scripts/check-conformance.sh 067` (plano íntegro) | imprime `domain model declared (aggregate, invariants, glossary, ports) with a reason`; verde após tasks e `qa-report.md` |
| **mutação (a)**: apagar a linha `DOM:aggregate` deste plano → `scripts/check-conformance.sh 067; echo $?` | `✗ domain model never declared in plan.md: aggregate`; `1`; com `--ticked-only` a mesma linha com `·` e `0`; restaurar → verde |
| **mutação (b)**: trocar a declaração das invariantes por `` `DOM:invariants=edge` `` e **esvaziar** a célula Why | `domain invariants: declared DOM:invariants=edge with no reason`; restaurar → verde |
| **mutação (b')**: trocar por `` `DOM:invariants=regra_portao=domain \| regra_dora=edge` `` com célula Why vazia | `'regra_dora=edge' is edge with no reason`; com `regra_dora=edge(só leitura)` → nenhuma linha `✗` do bloco 3b; restaurar → verde |
| **mutação (c)**: `MAESTRO_MIN_CYCLE_DOMAIN=abc scripts/check-conformance.sh 067; echo $?` | `2`; sem a variável → verde |
| `python -m unittest discover -s painel/tests -p test_painel.py` | `Ran 12 tests`, `OK` (nenhum teste novo em `db6b89c` — dívida 1) |
| `grep -c 'DORA counts production only' painel/server.py` | `1` (`server.py:158`) |
| `grep -c 'sem plan ou tasks' painel/index.html` · `grep -c 'tem_plan' painel/ingest.py` | `1` · `1` |
| `scripts/check-language.sh` · `check-boundary.sh` · `check-links.sh` | verdes (medido em 20/10 após o merge) |
| `grep -c 'raiz de agregado\|aggregate root' docs/governance/glossary.md` (após T8) | ≥ `1` |

<!--
  GATE (not delegable): o plano é aprovado pelo Darú antes de virar tasks.
  Handoff: plan-architect → (aprovação) → tasks → dev-implementer / qa.
-->
