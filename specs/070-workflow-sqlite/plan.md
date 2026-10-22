# Plan 070 — Workflow do ciclo em SQLite: rodadas, passos, outbox e hooks

- **Spec**: `spec.md` (retroativa; escrita como "Spec 064" na linha paralela em 02/10/2026, renumerada 070 pelo mapa de `specs/066-painel-de-regencia/plano-integracao-linha-paralela.md` § 3) · **Raia**: plena · **Data**: 2026-10-22
- **Origem**: branch `w07-064-integrate`, ponta `b33bb81` (14 commits de 02/10/2026, linhagem A do Hindiana); entrou pelo merge `--no-ff` **`f37bf89`** sobre `39a86ba` (branch `066-painel-de-regencia`, que contém a `dev` `ffecd70`). Hooks movidos e spec renumerada em **`8ef082f`**.
- **Ciclo retroativo**: o código veio pronto; este plano declara o que já existe, o que foi decidido na integração e o que falta para o ciclo fechar pelo método. Siglas: ADR (*Architecture Decision Record*, registro de decisão de arquitetura) · DoD (*Definition of Done*, definição de pronto) · FR (*functional requirement*, requisito funcional) · WAL (*write-ahead log*, modo de escrita do SQLite que permite leitura concorrente) · CI (*Continuous Integration*, integração contínua).

## Constitution Check (governance/principles.md)

| Principle | Compliance |
|---|---|
| I. Spec-driven | ✅ A spec (14 FR em EARS, critérios de aceite executáveis) precedeu o código na linha paralela (02/10); a renumeração não muda o conteúdo. |
| II. Human-governed orchestration | ✅ Os hooks registram e cobram; nenhum hook decide nem promove. O gate deste ciclo é do Darú (`TAIL:gate`). |
| III. Reversibility / risk gates | ✅ Ingest reconstrói em arquivo temporário e troca por rename (FR12/FR14, `test_ingere_interrompido_mantem_anterior`); o SQLite fica fora do git (`painel/.gitignore`). Reverter o ciclo = `git revert -m 1 f37bf89`. Declarado: o "append-only" das tabelas do workflow é convenção, não gatilho — o schema não tem `TRIGGER` e os testes com esse nome só conferem colunas (dívida 5). |
| IV. Test-first / verifiable DoD | ✅ 24 testes da linhagem A (`test_workflow_schema`, `test_workflow_painel`, `test_fr13_fr14`) mais os 22 da linhagem B, 46 verdes após o merge. Declarado: FR2 e FR3 (recusa de entrada e cobrança de saída) não têm teste nomeado — dívida 1 abaixo. |
| V. Context economy / boundary | ✅ O corte da linha paralela (backend W09 × tela W03) se manteve; os hooks saem de `scripts/` (instalador do método) para `painel/hooks/` (ferramenta), respeitando `boundary.json`. |
| VI. Living artifacts | ✅ Spec, plan, tasks, data-model, ux-design e qa-report em `specs/070-workflow-sqlite/`; CHANGELOG, roadmap F34 e ADR 0025 no mesmo PR. |
| VII. Light governance / YAGNI | ✅ Fila em SQLite WAL em vez de broker (19 sessões numa máquina); Redis Streams fica anotado para quando houver mais de uma máquina. |
| VIII. Intelligible communication | ✅ Siglas expandidas na primeira ocorrência; termos novos entram no glossário (T14). |

**No violations.**

## Artifacts of this cycle (declare all five — silence is not a decision)

| Artifact | Declaration | Why |
|---|---|---|
| `research.md` | `ART:research=no` | Nenhuma incógnita: o desenho veio pronto (`workflow-maestro.md` do Hindiana) e o código já roda; a única decisão de método (hooks de terceiro gravando SQLite) vai para o ADR 0025, não para pesquisa. |
| `data-model.md` | `ART:data-model=yes` | Quatro tabelas novas (rodadas, passos, transicoes, fila) com relações e gatilhos; o arquivo veio da linha paralela e descreve o `schema_workflow.sql`. |
| `contracts/` | `ART:contracts=no` | O contrato é o schema SQLite e a entrada/saída dos hooks do Claude Code (JSON em stdin, texto em stdout); a rota nova `/api/erros` devolve lista de pares caminho e motivo, descrita na DoD. |
| `checklist.md` | `ART:checklist=no` | Os critérios de aceite da spec já são executáveis; a DoD abaixo os cobre. |
| `ux-design.md` | `ART:ux-design=yes` | Toca tela: roadmap com rodadas, equipe real, aviso de leitura velha e erros de leitura; o arquivo veio da linha paralela. |

## Domain model (declare all four — silence is not a decision)

| Question | Declaration | Why |
|---|---|---|
| Aggregate root | `DOM:aggregate=Rodada` | Raiz nova: uma Rodada agrega seus Passos (entrada, resumo, saída, evidência) e as Transições permitidas; toda consulta do roadmap entra pela rodada. A Fila é um segundo agregado pequeno (`FilaOutbox` em `painel/fila_outbox.py`), independente da Rodada, porque mensagem entre sessões não pertence a rodada nenhuma. |
| Where the invariants live | `DOM:invariants=edge` | Declarado com honestidade: nenhuma invariante do workflow está imposta pelo domínio hoje — o "append-only" é convenção (sem `TRIGGER` em `painel/schema_workflow.sql`; `test_rodadas_append_only` e `test_passos_append_only` só conferem colunas), e a regra FR2 (recusar a entrada se o passo anterior não tem saída com evidência) mora no hook `painel/hooks/workflow_session_start.py`, que é adaptador do Claude Code, e sem teste nomeado. Dívida 1: extrair a regra para função pura em `painel/` e testá-la (ciclo 072). |
| Ubiquitous language | `DOM:glossary=changed` | Entram em `docs/governance/glossary.md` (T14, em inglês): **rodada** (one execution of the Maestro workflow, recorded step by step), **passo** (a step of a rodada, recorded three times: entry, summary, exit) e **outbox** (the SQLite queue sessions use to message each other without a broker). |
| Ports and adapters | `DOM:ports=new` | Duas portas novas de entrada: os hooks `SessionStart` e `Stop` do Claude Code (adaptadores em `painel/hooks/`, configurados por `settings.example.json`), que escrevem no SQLite do painel; uma porta de saída nova: a fila outbox lida pelos hooks. Rota HTTP nova: `/api/erros` em `painel/server.py`. |

## How

1. **Merge `--no-ff` de `b33bb81`** (`f37bf89`). Dois conflitos, ambos previstos no handoff § 3c: `painel/index.html` — B (chamados, dev) prevalece no roteamento por hash com id (`#chamados/id`); A contribui o corpo de `meta()` com o aviso de leitura velha (FR11) e os erros de leitura (FR6), que o `server.py` já servia (`ingerido_age_min`, `/api/erros`). `painel/projetos/hindiana.json` — removido: o único delta sobre a fixture `exemplo.json` são nomes de equipes do Hindiana (dado real num repositório público; decisão 3 do plano de integração).
2. **Hooks saem do instalador** (`8ef082f`, decisão 5): `git mv scripts/hooks/workflow_*.py painel/hooks/`. Referências corrigidas: o comentário de instalação no próprio hook, `settings.example.json`, `install_hooks.py` e `test_fr13_fr14.py` (`HOOKS_DIR`). As referências a `scripts/hooks/guard-immutables.py` e `session-state.sh` ficam, porque esses são do método.
3. **Renumeração** (`8ef082f`): `specs/064-workflow-painel/` → `specs/070-workflow-sqlite/`. A pasta `specs/070-conferidor-ordem-veredito/` (evidência importada do Hindiana pelo ciclo 069) mantém o 070 por ser o número do chamado de origem; o portão a isenta por forma (ADR 0024) e trata esta pasta como o ciclo 070. Dois diretórios com o mesmo número já acontecem no 066.
4. **ADR 0025 — hooks de terceiro gravando SQLite**: o painel passa a receber escrita de processos que não são o servidor (hooks do Claude Code), com schema próprio e `_ensure_schema` em cada hook. O número 0024 foi tomado pelo cabeçalho conferível; o handoff citava 0024 para esta decisão antes disso.
5. **Equipe "19 sessões" (FR10)**: a lista é do Hindiana; no Maestro ela vive na fixture `exemplo.json` (chave `equipes`) e o teste `test_meta_equipes_tem_19_sessoes` lê a fixture. Acoplamento a nomes reais já declarado como dívida do 072 no ciclo 068.
6. **Ciclo 071 (board, `6e9788f`)** contém `b33bb81`; segue como ciclo próprio depois deste.

## Verification (DoD)

- `python -m pytest painel/tests -q` → `46 passed`
- `python -m pytest painel/tests/test_workflow_schema.py -q` → `7 passed` (FR8, FR9: tabelas, WAL, append-only, evidência exigida, fila, passos abertos)
- `python -m pytest painel/tests/test_fr13_fr14.py -q` → `9 passed` (FR13, FR14, outbox, encoding e schema dos hooks)
- `python -m pytest painel/tests/test_workflow_painel.py -q` → `8 passed` (FR4, FR6, FR10, FR11, decisões)
- `ls painel/hooks/` → `workflow_session_start.py`, `workflow_stop.py`; `ls scripts/hooks/ | grep -c workflow_` → `0`
- `grep -c 'scripts/hooks/workflow_' painel/hooks/*.py specs/070-workflow-sqlite/*.json specs/070-workflow-sqlite/install_hooks.py painel/tests/test_fr13_fr14.py` → `0` em todos
- `git diff --stat 39a86ba f37bf89` → 17 arquivos (14 novos, 2 modificados, 1 removido)
- `test -f painel/projetos/hindiana.json` → ausente
- `grep -c 'Cycle 070' docs/governance/glossary.md` → `3`
- `grep -c 'ciclo 070' CHANGELOG.md` → ≥ 1; `grep -c 'F34' docs/roadmap.md` → ≥ 1; `ls docs/adr/0025-*` → 1 arquivo
- `scripts/check-conformance.sh 070` → verde; `scripts/check-conformance.sh --ticked-only` → verde
- `scripts/check-boundary.sh`, `check-language.sh`, `check-links.sh`, `check-install.sh`, `check-version.sh`, `check-adr.sh` → verdes

## Dívidas declaradas (vão para o 072)

1. FR2 e FR3 sem teste nomeado; regra FR2 no adaptador (hook) e não em função pura.
2. `_ensure_schema` duplicado nos dois hooks e no `fila_outbox.py` (três cópias da mesma função).
3. `install_hooks.py` escreve em `.claude/settings.json` do projeto alvo sem backup (mescla, não sobrescreve, mas não faz dry run).
4. Nomes reais do Hindiana na fixture `equipes` (herdada do 068).
5. "Append-only" não imposto: `schema_workflow.sql` não tem gatilho contra `UPDATE`/`DELETE` em `rodadas`, `passos` e `transicoes`; os testes `test_*_append_only` só conferem colunas. Achado deste ciclo ao escolher as mutações (qa-report § Findings).

<!--
  GATE (not delegable): the plan is approved by a human before it becomes tasks.
  Handoff: plan-architect → (approval) → tasks → dev-implementer.
-->
