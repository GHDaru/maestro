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
| IV. Test-first / verifiable DoD | ⚠️ Parcial, declarado. 24 testes da linhagem A mais 22 da B, 46 verdes após o merge; dois pares vermelho/verde deste ciclo (`3d3da3b`, `04e559c`) levam a 48. A revisão em contexto fresco mostrou que a spec **não está toda implementada**: FR2 (recusar a entrada sem saída anterior) **não existe** no código; FR3 está **invertido** (o hook Stop fecha o passo sozinho, com `resultado='skip'`, em vez de cobrar); FR1 não grava branch nem hash; FR10 é provado por um teste que injeta os 19 nomes. Nada disso é vendido como verde: dívidas 1, 7, 8 e 9. |
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
| Where the invariants live | `DOM:invariants=edge` | Declarado com honestidade, depois da revisão: a única invariante imposta (troca atômica e preservação das tabelas do workflow no ingest, `04e559c`) vive na borda, em `painel/ingest.py`; nenhuma invariante do workflow em si está imposta hoje, nem no domínio nem na borda. O "append-only" é convenção (sem `TRIGGER` em `painel/schema_workflow.sql`; `test_rodadas_append_only` e `test_passos_append_only` só conferem colunas) e o próprio hook Stop faz `UPDATE passos`. A regra FR2 (recusar a entrada se o passo anterior não tem saída com evidência) **não está em lugar nenhum**: `workflow_session_start.py` só imprime os passos abertos e insere a linha. A única invariante provada é a do ingest (troca atômica e preservação das tabelas do workflow, `04e559c`). Dívida 1: implementar FR2 como função pura em `painel/` com teste, e o hook só a chama (ciclo 072). |
| Ubiquitous language | `DOM:glossary=changed` | Entram em `docs/governance/glossary.md` (T14, em inglês): **rodada** (one execution of the Maestro workflow, recorded step by step), **passo** (a step of a rodada, recorded three times: entry, summary, exit) e **outbox** (the SQLite queue sessions use to message each other without a broker). |
| Ports and adapters | `DOM:ports=new` | Duas portas novas de entrada: os hooks `SessionStart` e `Stop` do Claude Code (adaptadores em `painel/hooks/`, configurados por `settings.example.json`), que escrevem no SQLite do painel; uma porta de saída nova: a fila outbox lida pelos hooks. Rota HTTP nova: `/api/erros` em `painel/server.py`. |

## How

1. **Merge `--no-ff` de `b33bb81`** (`f37bf89`). Dois conflitos, ambos previstos no handoff § 3c: `painel/index.html` — B (chamados, dev) prevalece no roteamento por hash com id (`#chamados/id`); A contribui o corpo de `meta()` com o aviso de leitura velha (FR11) e os erros de leitura (FR6), que o `server.py` já servia (`ingerido_age_min`, `/api/erros`). `painel/projetos/hindiana.json` — removido: o único delta sobre a fixture `exemplo.json` são nomes de equipes do Hindiana (dado real num repositório público; decisão 3 do plano de integração).
2. **Hooks saem do instalador** (`8ef082f`, decisão 5): `git mv scripts/hooks/workflow_*.py painel/hooks/`. Referências corrigidas: o comentário de instalação no próprio hook, `settings.example.json`, `install_hooks.py` e `test_fr13_fr14.py` (`HOOKS_DIR`). As referências a `scripts/hooks/guard-immutables.py` e `session-state.sh` ficam, porque esses são do método.
3. **Renumeração** (`8ef082f`): `specs/064-workflow-painel/` → `specs/070-workflow-sqlite/`. A pasta `specs/070-conferidor-ordem-veredito/` (evidência importada do Hindiana pelo ciclo 069) mantém o 070 por ser o número do chamado de origem; o portão a isenta por forma (ADR 0024) e trata esta pasta como o ciclo 070. Dois diretórios com o mesmo número já acontecem no 066.
4. **ADR 0025 — hooks de terceiro gravando SQLite**: o painel passa a receber escrita de processos que não são o servidor (hooks do Claude Code), com schema próprio e `_ensure_schema` em cada hook. O número 0024 foi tomado pelo cabeçalho conferível; o handoff citava 0024 para esta decisão antes disso.
5. **Equipe "19 sessões" (FR10)**: a lista é do Hindiana. Corrigido pela revisão: a fixture `exemplo.json` tem 8 nomes (Coordenação 2, Workers 6) e o teste `test_meta_equipes_tem_19_sessoes` **injeta** os 19 nomes em `cfg["equipes"]` dentro do próprio teste — prova só que `/api/meta` repassa a configuração, não a lista real. FR10 é requisito do Hindiana, não do Maestro; no Maestro vale "a equipe configurada aparece" (dívida 9: reescrever o teste sobre a fixture).
6. **Ciclo 071 (board, `6e9788f`)** contém `b33bb81`; segue como ciclo próprio depois deste.

## Verification (DoD)

- `python -m pytest painel/tests -q` → `48 passed` (46 após o merge, mais os dois testes vermelho/verde deste ciclo)
- `python -m pytest painel/tests/test_workflow_schema.py -q` → `7 passed` (FR8, FR9: tabelas, WAL, colunas, evidência exigida, fila, passos abertos)
- `python -m pytest painel/tests/test_fr13_fr14.py -q` → `11 passed` (FR13, FR14, outbox, encoding e schema dos hooks; `test_payload_invalido_nao_envenena_a_fila` e `test_ingere_preserva_tabelas_do_workflow` nascidos neste ciclo)
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
5. "Append-only" não imposto: `schema_workflow.sql` não tem gatilho contra `UPDATE`/`DELETE` em `rodadas`, `passos` e `transicoes`; os testes `test_*_append_only` só conferem colunas, e o hook Stop faz `UPDATE passos`. Achado deste ciclo ao escolher as mutações (qa-report § Findings).
6. O hook `SessionStart` imprime no stdout `payload` e `sessao_origem` da fila e `passos.sessao`, texto que entra no contexto do modelo: vetor de injeção para quem escreve no banco (segurança, achado 1). Imprimir só campos conhecidos, truncados e sem caracteres de controle.
7. FR3 invertido: `workflow_stop.py` fecha o passo (`UPDATE passos SET saida_em`, `resultado='skip'`) antes de conferir o resumo, com aviso só no stderr e exit 0 (o docstring promete exit 2). Cobrar de verdade e testar (revisão, achado 3).
8. FR1 parcial: o schema não tem colunas de branch nem de hash de partida e o hook não as grava (revisão, achado 4).
9. FR10 provado por teste que injeta os dados; reescrever sobre a fixture (revisão, achado 6).
10. Troca atômica com WAL: `os.replace` pode deixar `painel.db-wal`/`-shm` velhos ao lado do banco novo se houver conexão aberta; no Windows levanta `PermissionError` e deixa o `.tmp`. Fazer `wal_checkpoint(TRUNCATE)` antes da troca e um lock de ingest (segurança, achado 3). Broadcast da fila consumido pelo primeiro leitor (revisão, achado 7b).

<!--
  GATE (not delegable): the plan is approved by a human before it becomes tasks.
  Handoff: plan-architect → (approval) → tasks → dev-implementer.
-->
