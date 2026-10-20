# Plan 069 — Conferidor pela data (o veredito vigente é o mais novo, não o último no alfabeto)

- **Spec**: `spec.md` (retroativa; ciclo 069 pela decisão `decisao-066-daru-20-10`) · **Raia**: plena
  · **Data**: 2026-10-20 · **ADR** (*Architecture Decision Record*, registro de decisão de
  arquitetura): nenhum — ver § How, decisão 6.

> **Plano retroativo.** O código já está integrado nesta branch: o merge `23f8325` trouxe
> `aa0efd1` da branch `067-painel-chamados` (trecho `2796cbf..aa0efd1`, 21 commits de
> 09/10/2026; 12 arquivos, +485 linhas, 0 conflitos). O que mudou de código: a função pura
> `ordem_veredito(item, commit_de)` em `painel/chamados.py:115-118`, aplicada em `:151`; quatro
> testes na classe `TestOrdemDoVeredito` (`painel/tests/test_chamados.py:88`); e a pasta
> `specs/070-conferidor-ordem-veredito/` com os dez arquivos de gate do chamado 070 do Hindiana.
> Este plano não decide a arquitetura — ela está no diff — mas registra o COMO contra o qual a
> revisão em contexto fresco e o portão humano medem.

## Constitution Check (governance/principles.md)

| Principle | Compliance |
|---|---|
| I. Spec-driven | ✅ Cinco requisitos funcionais (FR, de *functional requirement*) lidos do diff numa spec retroativa, em EARS (*Easy Approach to Requirements Syntax*); o que o trecho faz e a spec não pediu está em spec § Limites (R2 sem teste próprio; `G3-criterio` com hash do cabeçalho diferente do nome), entregue como está. A spec aguarda a aprovação do Darú (DoR); este plano só vira tasks depois dela. |
| II. Human-governed orchestration | ✅ O painel continua **só lendo**: a correção muda qual arquivo decide o estado, não quem assina. Cada veredito da pasta 070 foi assinado por não autor (W11, W13, W01, W10); o merge deste ciclo é gate do Darú. |
| III. Reversibility / risk gates | ✅ Desfazer é `git revert 23f8325` (dois arquivos de código, uma pasta de evidência); GD do chamado classe A. Raio amplo — a regra decide seis gates (GD, G4 a G9) de todo chamado de todo projeto instalado —, irreversibilidade baixa: raia plena, não infra. Classe de risco da passagem de segurança: **baixa** (função pura; arquivos de evidência). |
| IV. Test-first / verifiable DoD | ✅ **Primeiro ciclo integrado em que o Princípio IV vale para a mudança principal**: o teste de FR1 (`test_mais_novo_vence_mesmo_vindo_antes_no_alfabeto`) existe no commit `6741315`, anterior à correção `d2822ef`, e falhou na base por não autor (`G2-vermelho-W13-6741315.md`, `FALHA_ESPERADA`); `git merge-base --is-ancestor 6741315 d2822ef` prova a ordem. **Dito com honestidade**: os testes de FR2 (`6ea2347`) e FR3 (`98a62a1`) são **testes de regressão** sobre comportamento que a base `2796cbf` já tinha — não são par vermelho/verde, e o de FR3 é mutante verificado (sem o `sort`, falha). A DoD (*Definition of Done*, definição de pronto) abaixo é executável. Sem violação: o que não é vermelho/verde está declarado como tal, não vendido como tal. |
| V. Context economy / boundary | ✅ Uma fatia só, numa fronteira já cortada no 068: a regra de seleção mora em `ordem_veredito`, função pura sem HTTP (*Hypertext Transfer Protocol*) nem SQLite (*Structured Query Language lite*); `confere` só troca a chave do `sorted`. A trilha (`eventos.sort`, `:393`) não foi tocada. A pasta 070 entra como dado, não como contexto a ler: o `qa-report.md` cita os arquivos, não os copia. |
| VI. Living artifacts | ✅ A pasta `specs/070-conferidor-ordem-veredito/` é evidência imutável (como um ADR): cada arquivo de gate é consumido por `painel/chamados.py` com forcing function (o estado do chamado é derivado deles). Este plano, as tasks e o `qa-report.md` fecham a cadeia spec ↔ pull request ↔ testes; a entrada do CHANGELOG e a linha F33 do roadmap já estão em `23f8325`. Nada duplicado: o `qa-report.md` aponta para os arquivos de gate em vez de reescrevê-los. |
| VII. Light governance / YAGNI | ✅ Correção de uma regra de feature do painel: não toca template, portão, skill, agente nem constituição. `principles.md § Governance` exige ADR para "decisão material de metodologia" — não há nenhuma aqui; **nenhum ADR** é devido (§ How, decisão 6). YAGNI (*You Aren't Gonna Need It*, não vai precisar) podou: sincronizar as duas cópias da regra (dívida mantida do 068) e adotar o padrão de arquivos de gate como padrão do Maestro (ambiguidade da spec, decisão do Darú — não deste plano). |
| VIII. Intelligible communication | ✅ A spec traz glossário próprio; este plano expande cada sigla na primeira ocorrência; os dois termos novos (veredito vigente, data legível) entram em `docs/governance/glossary.md` (tarefa T6), não ficam órfãos no código. |

**No violations.**

## Artifacts of this cycle (declare all five — silence is not a decision)

<!-- Read by scripts/check-conformance.sh. Declaring =yes means the file MUST exist here.
     What each one is for: docs/governance/artifacts.md -->

| Artifact | Declaration | Why |
|---|---|---|
| `research.md` | `ART:research=no` | Nenhuma incógnita: o defeito foi reproduzido por não autor (`G0-reproducao.md`) e a regra está em EARS (R1–R4). |
| `data-model.md` | `ART:data-model=no` | Nenhuma entidade nova: Chamado, Gate e Veredito são os do 068 (`specs/068-chamados-gate-a-gate/data-model.md`); muda uma regra de seleção. |
| `contracts/` | `ART:contracts=no` | Nenhuma rota nova nem campo novo na resposta; `/api/chamados` e `/trilha` devolvem o mesmo esquema do 068, com outro conteúdo. |
| `checklist.md` | `ART:checklist=no` | A DoD abaixo cobre o que há para checar. |
| `ux-design.md` | `ART:ux-design=no` | A ordem da trilha é comportamento de um objeto que já existe (desenho do 068), não objeto novo nem tela nova; nenhum papel semântico muda. |

## Domain model (declare all four — silence is not a decision)

<!-- Read by scripts/check-conformance.sh (block 3b). Source of truth for the terms:
     docs/governance/glossary.md. Keep the itemized form out of this table (ADR 0023). -->

| Decision | Declaration | Why |
|---|---|---|
| Aggregate root | `DOM:aggregate=Chamado` | Raiz inalterada desde o 068: `Gate` e `Veredito` continuam entidades dentro de `Chamado`, e toda consulta entra pela raiz (`confere` recebe a pasta inteira do chamado). Este ciclo não cria agregado nem entidade; muda qual veredito, dentro do gate, é o vigente. |
| Where the invariants live | `DOM:invariants=domain` | A regra "vence o veredito de maior data do cabeçalho sobre o hash certo; empate pelo commit do arquivo, depois pelo nome" mora na função pura `ordem_veredito` (`painel/chamados.py:115-118`), que devolve a tupla data-ou-MINIMO, commit-ou-MINIMO, nome; `confere` a aplica em `validos = sorted(...)` (`:151`). Nada na borda: `server.py` não mudou e `commit_de` já era parâmetro de `confere`. A exclusão da data ilegível fica em `valida` (`:86`), também domínio. |
| Ubiquitous language | `DOM:glossary=changed` | Entram em `docs/governance/glossary.md` (tarefa T6, em inglês): **veredito vigente** (the one verdict that decides a single-verdict gate: latest header date on the right hash, tie by file commit date then name) e **data legível** (a header `data:` that matches `RE_DATA`); a linha de **Veredito** do 068 já dizia "latest-dated" e passa a apontar para o termo novo. Definições: `spec.md § Glossário deste ciclo`. |
| Ports and adapters | `DOM:ports=none` | Nenhuma porta nova nem adaptador novo: as três rotas HTTP do 068 ficam iguais em forma; o leitor de git (`le_chamados`, `_git`) não mudou; `commit_de` já chegava a `confere` desde o 068. Só muda o critério de ordenação dentro do domínio. |

**Nota sobre a linguagem ubíqua.** O documento do projeto é `docs/governance/glossary.md`; os
nomes deste plano vêm da spec § Glossário e vão para lá — este plano não inventa nome de
passagem. Papéis do Hindiana (W01, W10, W11, W13, Office) **não** entram no glossário do
Maestro: aparecem só como assinatura nos arquivos de evidência.

## How

**1. Data em vez de nome (FR1).** O nome `G6-tela-<hash>.md` ordena pelo hash, que é aleatório;
a `data:` do cabeçalho ordena pelo tempo. `ordem_veredito` devolve `(data(item["data"]) or
MINIMO, commit do arquivo or MINIMO, item["arquivo"])` e `confere` usa essa tupla como chave do
`sorted` em `:151`; os gates de veredito único seguem lendo `validos[-1]` (`:219`), agora o mais
novo. O estado sai desse veredito e do hash que ele cita — um veredito antigo sobre outro hash
nunca decide.

**2. Cadeia de desempate.** Data do cabeçalho; em empate, data do commit do arquivo
(`commit_de`, `%aI` do git); persistindo, o nome. O terceiro elemento garante ordem total e
determinística; não tem teste próprio (spec § Limites) — dívida 3.

**3. Data ilegível é excluída por `valida`, não pelo `sort` (FR2).** `valida` (`:86`) acrescenta
"data fora do formato" a qualquer `data:` que não case `RE_DATA`, e `confere` só ordena itens
sem erro. Logo o ramo `or MINIMO` da data em `ordem_veredito` **só é alcançável quando `data:`
está ausente** — e um cabeçalho sem `data:` também cai em `valida` ("falta 'data'"). A regra
R3 está declarada e testada (`test_r3_veredito_sem_data_legivel_nao_vence`), mas o teste passa
pela exclusão de `valida`, não pelo `MINIMO`: a mutação (b) da DoD é **mutante equivalente** no
cenário testado. Lacuna declarada — dívida 2.

**4. A pasta do chamado viaja como evidência imutável, com o id 070 (FR5).** Os dez arquivos
de `specs/070-conferidor-ordem-veredito/` se referenciam pelo id (`objeto:
specs/070-conferidor-ordem-veredito/spec.md @ 6741315`); renomear a pasta para 069 quebraria a
referência e reescreveria história. A pasta do ciclo Maestro é esta, `069-conferidor-pela-data/`,
e aponta para aquela. O `qa-report.md` cita os arquivos de gate (`grep` de `FALHA_ESPERADA` e
`APPROVE`), não os reescreve.

**5. Por que `699bddb` ficou de fora.** A branch lateral `w10/070-g3-codigo` (`699bddb`) é
anterior ao fechamento do chamado: `git diff --stat aa0efd1 699bddb -- specs/070-*` mostra que
ela só **carece** de 8 dos arquivos de gate e não acrescenta nada. Integrá-la seria merge sem
conteúdo; fica preservada na tag local `arquivo/paralela/w10-070-g3-codigo`.

**6. Nenhum ADR.** `principles.md § Governance`: "toda decisão material de metodologia vira
ADR". Este ciclo corrige uma regra de feature do painel e não toca template, portão, skill,
agente nem constituição. A ambiguidade "o Maestro adota o padrão de arquivos de gate?" (spec,
última seção) **é** decisão de metodologia — mas é do Darú, e quando decidida terá o seu ADR
num ciclo próprio, não neste.

**7. Fato de método que fica.** A GD do chamado 070 veio depois do G3 (a Office pediu a
correção antes de abrir a GD e assume a falha, registrado em `GD-risco.md`). É achado de retro;
não se apaga nem se corrige aqui.

### Como foi medido no Windows

Windows 11, Git Bash (não PowerShell) para `scripts/check-*.sh`; `python3` é shim para o
`python` do Windows; `PYTHONUTF8=1` no ambiente; `core.autocrlf=false` no worktree. Os testes
rodam com `python -m unittest discover -s painel/tests -p test_chamados.py` a partir da raiz.
Códigos de saída lidos com `echo $?` no Git Bash. As duas mutações foram feitas e revertidas
byte a byte (`git diff --exit-code painel/chamados.py` vazio ao fim).

### Dívidas (entregues ao 072, painel de regência)

1. **`data()` deixa `strptime` levantar** (`security-pass.md`, achado 1, média, pré-existente):
   `RE_DATA` aceita `2026-13-01 00:00` ou fuso `+2500`; a `ValueError` sobe por `valida` →
   `confere` → `le_chamados` e cai no `except` de `_atualiza` (`:323`) — **o painel inteiro
   fica em erro**, não só o chamado. Fix de uma linha: `try/except ValueError: return None` em
   `data()`, com teste vermelho antes.
2. **Teste para `data:` ausente** chegando a `ordem_veredito`: hoje nenhum teste cobre o ramo
   `or MINIMO` da data (decisão 3; mutação (b) equivalente). Nome proposto:
   `test_veredito_sem_campo_data_e_o_mais_antigo`.
3. **Desempate por nome (R2, terceiro elemento)** sem teste próprio. Nome proposto:
   `test_empate_de_data_e_de_commit_desempata_pelo_nome`.
4. **Confiança na author date** (`security-pass.md`, achado 2, baixa): `commit_de` vem de `%aI`,
   forjável por `GIT_AUTHOR_DATE`; a trava "hora digitada" (`:139-142`) confia nela. Dentro do
   modelo de confiança (quem commita já é crítico); fix opcional: `%cI`, ou os dois.
5. Mantidas do 068: duas cópias da regra (`conferir_chamado.py` lá, `chamados.py` aqui);
   acoplamento ao Hindiana; `unittest.main()` antes de `TestPendencia`.

## Verification (DoD)

Medido em 20/10/2026 neste worktree (`integra/linha-paralela-066`), Git Bash; o `qa-report.md`
cola a saída de cada linha.

| Comando | Esperado |
|---|---|
| `python -m unittest discover -s painel/tests -p test_chamados.py; echo $?` | `Ran 10 tests`, `OK`, `0` (6 do 068 + 4 deste ciclo) |
| `python -m unittest discover -s painel/tests -p test_painel.py` | `Ran 12 tests`, `OK` (nada regrediu) |
| `grep -c 'def test_' painel/tests/test_chamados.py` · `grep -c 'class TestOrdemDoVeredito' painel/tests/test_chamados.py` | `10` · `1` |
| `grep -c 'ordem_veredito' painel/chamados.py` | `2` (`:115` definição, `:151` uso) |
| Mutação (a): `ordem_veredito` devolve `(item["arquivo"],)` (comportamento alfabético antigo) → `unittest` | **`FAILED (failures=2)`** — `test_mais_novo_vence...` e `test_empate_de_data...` vermelhos; observado em 20/10 |
| Mutação (b): `or MINIMO` da data trocado por uma data do ano 2999 → `unittest` | **`Ran 10 tests OK`** — mutante **equivalente** em todo cenário via `confere` (o campo `data` é obrigatório no cabeçalho, `chamados.py:36-37`, então nenhum item sem data chega ao sort) (decisão 3); registrar como lacuna, não como verde |
| `git diff --exit-code painel/chamados.py; echo $?` (após as mutações) | vazio, `0` — restaurado byte a byte |
| `ls specs/070-conferidor-ordem-veredito/ \| wc -l` | `10`: `00-chamado.md`, `spec.md`, `G0-reproducao.md`, `GD-risco.md`, `G1-W11.md`, `G2-vermelho-W13-6741315.md`, `G3-codigo-W10.md`, `G3-criterio-W01-d2822ef.md`, `G3-runner2-W13-d2822ef-8adb545a.md`, `G3-runner2-W13-98a62a1.md` |
| `grep -c 'veredito: FALHA_ESPERADA' specs/070-conferidor-ordem-veredito/G2-*.md` | `1` |
| `grep -c 'veredito: APPROVE' specs/070-conferidor-ordem-veredito/G3-*.md` | `≥ 2` (código W10 e critério W01; os runner2 trazem `veredito: OK`) |
| `grep -c 'escopo: correcao' specs/070-conferidor-ordem-veredito/00-chamado.md` · `grep -c 'classe: A' specs/070-conferidor-ordem-veredito/GD-risco.md` | `1` · `1` |
| `git merge-base --is-ancestor 6741315 d2822ef; echo $?` | `0` (teste antes da correção — FR4) |
| `git diff --stat aa0efd1 699bddb -- specs/070-*` | só linhas com `-` (8 arquivos a menos, nada a mais) — decisão 5 |
| `grep -c 'Cycle 069' docs/governance/glossary.md` (após T6) | `≥ 2` |
| `grep -c 'ciclo 069' CHANGELOG.md` · `grep -c 'F33' docs/roadmap.md` | `≥ 1` · `≥ 1` (já em `23f8325`) |
| `scripts/check-language.sh` · `check-links.sh` · `check-boundary.sh` · `check-adr.sh` | verdes |
| `scripts/check-conformance.sh 069` (após plano, tasks, `qa-report.md`) | imprime `domain model declared (aggregate, invariants, glossary, ports) with a reason`; verde |

<!--
  GATE (not delegable): o plano é aprovado pelo Darú antes de virar tasks.
  Handoff: plan-architect → (aprovação) → tasks → dev-implementer / qa.
-->
