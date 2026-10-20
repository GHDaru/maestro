# Plan 066 — Painel de coordenação v0 (projeção dos arquivos, só localhost)

- **Spec**: `spec.md` (aprovada pelo Darú em 20/10/2026, `decisao-066-daru-20-10`) · **Raia**: plena
  · **Data**: 2026-10-20 · **ADR** (*Architecture Decision Record*, registro de decisão de
  arquitetura): `docs/adr/0022-painel-de-coordenacao-como-projecao-dos-arquivos.md`

> **Plano retroativo.** O código já está integrado nesta branch: o merge `023694b` trouxe a
> branch `painel-controle` (ponta `a1172a2`) e o commit `4919f4a` acrescentou a spec, o ADR 0022,
> a fronteira em `boundary.json` e a fixture `painel/projetos/exemplo.json` no lugar de
> `hindiana.json`. Este plano não decide a arquitetura — ela está decidida no ADR — mas registra
> o COMO contra o qual a revisão em contexto fresco e o portão humano medem, e declara, sem
> suavizar, o que o v0 viola e o que fica de dívida.

## Constitution Check (governance/principles.md)

| Principle | Compliance |
|---|---|
| I. Spec-driven | ✅ Nove requisitos funcionais (FR, de *functional requirement*) numa spec retroativa aprovada; nada no plano vai além do que a branch faz. O escopo que o código traz e a spec não pediu está listado abaixo (§ Escopo não declarado) com uma decisão para cada item — não fica escondido. |
| II. Human-governed orchestration | ✅ O painel nunca promove peça, remove worktree, faz merge ou deploy: a lista de higiene é "para aprovação"; todo evento exige `autor`; o portão de merge deste ciclo é do Darú. |
| III. Reversibility / risk gates | ✅ Desfazer é apagar `painel/` e `.maestro/`, reverter duas entradas de `boundary.json` e uma linha do operating-model (ADR 0022 § Como desfazer). O servidor só escuta em `127.0.0.1`; a única escrita é `eventos`, só-acréscimo; a ingestão nunca escreve no projeto. Raio amplo, irreversibilidade baixa — gate humano de merge é proporcional. |
| IV. Test-first / verifiable DoD | ❌ **Violado no v0**: os 12 testes de `painel/tests/test_painel.py` e os 34 do hook foram escritos **depois** do código (desvio 2 da proposta Hindiana). Hoje a DoD (*Definition of Done*, definição de pronto) é executável (§ Verification), mas o teste não nasceu antes. Vai para **Complexity Tracking**. |
| V. Context economy / boundary | ✅ Quatro fatias com fronteira clara: ingestão (`ingest.py`, arquivos → projeção), leitura (`server.py`, rotas) e escrita (`registrar.py`/`mcp_painel.py`, só `eventos`), tela (`index.html`) e hook (`.maestro/controle/git-hooks/`). O hook não conhece o painel; o painel não conhece o hook. `painel/` e `.maestro/` entram no domínio `toolkit` de `boundary.json` (ADR 0018, decisão 2 do Darú). |
| VI. Living artifacts | ✅ ADR 0022, linha do operating-model §6, `boundary.json`, CHANGELOG e roadmap já estão no mesmo commit (`4919f4a`). O ADR é o rascunho da Hindiana movido com `git mv` — histórico preservado. Este plano, as tasks e o `qa-report.md` fecham a cadeia spec ↔ pull request ↔ testes. |
| VII. Light governance / YAGNI | ✅ Só biblioteca padrão do Python (stdlib), um `index.html` em JavaScript (JS) puro, sem build, sem autenticação, sem rede. Supera em parte o "Metrics dashboard — Later / YAGNI" porque a escala (16 sessões, ~160 worktrees) tornou o custo de coordenação mensurável — justificativa no ADR 0022. |
| VIII. Intelligible communication | ✅ A spec traz glossário próprio; este plano expande cada sigla na primeira ocorrência; `data-model.md` e `contracts/interfaces.md` nomeiam as entidades com as palavras do código (`eventos`, `peca`, `sessao`), não com códigos. |

**Complexity Tracking:**

- **Princípio IV — testes depois do código.** Inevitável aqui porque o ciclo é retroativo: o
  código pré-existe (`a1172a2`, 01–03/10/2026) e foi construído sob pressão da escala do Hindiana,
  sem spec. O que torna a violação **limitada**: (a) está declarada na spec (§ Limites
  declarados) e no ADR 0022 (§ Consequências); (b) a DoD de hoje é inteiramente executável e
  cada regra do princípio 6 e os triggers de `eventos` têm teste nomeado; (c) o `qa-report.md`
  cita o fato em vez de o apagar. **Regra que vale a partir do próximo ciclo** (072, painel de
  regência): teste vermelho antes de cada mudança no painel — sem exceção. O portão humano
  decide se aceita o v0 com esta dívida declarada.

## Artifacts of this cycle (declare all five — silence is not a decision)

<!-- Read by scripts/check-conformance.sh. Declaring =yes means the file MUST exist here.
     What each one is for: docs/governance/artifacts.md -->

| Artifact | Declaration | Why |
|---|---|---|
| `research.md` | `ART:research=no` | Nenhuma incógnita técnica: stdlib, SQLite (*Structured Query Language lite*, banco em um arquivo) e HTTP (*Hypertext Transfer Protocol*) local já estavam fixados pelo princípio 7 da proposta; o custo foi medido em uso diário no Hindiana. |
| `data-model.md` | `ART:data-model=yes` | A tabela `eventos` (colunas, triggers, vocabulários fechados, evidência exigida por estado) e as quinze tabelas de projeção são entidades novas com relações. |
| `contracts/` | `ART:contracts=yes` | Treze rotas HTTP, três ferramentas MCP (*Model Context Protocol*, protocolo de contexto de modelo), a linha de comando (CLI, *command-line interface*) do `registrar.py` e o contrato do hook de pre-commit — é o que torna seguro outra sessão consumir o painel. |
| `checklist.md` | `ART:checklist=no` | Os critérios de aceite da spec são todos executáveis e estão na DoD abaixo. |
| `ux-design.md` | `ART:ux-design=yes` | **Tem tela** (onze visões no `index.html`), logo não é opcional. O v0 nasceu sem papel semântico antes do componente — mais um fato retroativo. O `ux-design.md` semântico do painel vive no ciclo seguinte, `specs/066-painel-de-regencia/ux-design.md` (esqueleto a renumerar para 072 conforme o mapa de integração); este ciclo **não** escreve um segundo. **Tensão declarada**: `=yes` obriga o arquivo a existir neste diretório para o gate; a tarefa T8 em `tasks.md` deixa ao gerente a escolha entre um ponteiro de uma página para o 072 ou a decisão do Darú de aceitar o gate vermelho nesse item. |

**Tokens `DOM:`**: nem o `plan-template.md` nem o `check-conformance.sh` deste worktree leem
um token `DOM:`; o piso declarado pelo gerente para esse token é o ciclo 067. Para o 066 ele é
opcional e **não é declarado**.

## How

**1. Os arquivos são a fonte; o SQLite é projeção (FR1, ADR 0008 + 0022).** `ingest.py` apaga
e recria as quinze tabelas derivadas (`DERIVADAS`, `ingest.py:27-62`) a cada ingestão e só
cria `eventos` e `ingest_log` com `IF NOT EXISTS`. Padrão CQRS (*Command Query Responsibility
Segregation*, separação entre escrita e leitura): os arquivos recebem a escrita; o `.db` é o
modelo de leitura reconstruível. Duas ingestões sem mudança nos arquivos produzem `.dump`
idênticos.

**2. A única escrita direta é `eventos`, só-acréscimo (FR2).** Dois triggers
(`eventos_sem_update`, `eventos_sem_delete`, `ingest.py:76-79`) fazem `RAISE(ABORT)`. `tipo`
tem `CHECK` com vocabulário fechado; `autor` e `ts` são `NOT NULL`.

**3. Sem prova não muda de coluna (FR3).** `EVIDENCIA_EXIGIDA` (`server.py:27-33`) é a tabela
estado → campos obrigatórios; `valida_evento` (`server.py:360-380`) é o único juiz, e é chamado
por `grava_evento`, que as três entradas de escrita (HTTP `POST /api/eventos`, MCP
`registrar_peca`, CLI `registrar.py`) compartilham. `registrar.py` devolve `2` antes do `INSERT`
(`registrar.py:39-41`).

**4. Só localhost (FR4).** `ThreadingHTTPServer(("127.0.0.1", porta))` em `server.py:473`; o
`do_POST` ainda recusa com 403 qualquer `client_address` fora de `127.0.0.1`/`::1`. Sem
autenticação porque não há rede — e isso é um limite declarado, não uma lacuna.

**5. Mesma leitura por MCP (FR5).** `mcp_painel.py` é um servidor MCP por stdio que chama
`server.v_estado_ia` e `server.grava_evento` — nenhuma lógica própria, para que HTTP e MCP não
divirjam.

**6. Projeto por configuração; fixture, não dado real (FR7, decisão 3 do Darú).**
`painel/projetos/exemplo.json` substitui `hindiana.json`. O dado real fica no repositório do
Hindiana. Medido em `a1172a2`: o arquivo trazia só caminhos e nomes, nunca IP (*Internet
Protocol*, endereço de rede), token ou usuário.

**7. Hook de veredito (FR8).** `.maestro/controle/git-hooks/veredito_hook.py --pre-commit` lê
`git diff --cached --name-only`, filtra `veredito*.md`/`critica*.md` e recusa (exit 1) o que não
traz `Objeto: <caminho> @ <hash>` e hora verificável. Independente do painel.

**8. O ADR viajou com `git mv`.** O rascunho "ADR 0021 (RASCUNHO)" de `painel/docs/` virou
`docs/adr/0022-...md` por `git mv`, para que `git log --follow` mostre a autoria da Hindiana
Assistente em 01/10/2026 e a decisão do Darú em 20/10.

### Escopo não declarado — decisão do plano

A revisão independente mediu em `a1172a2` cinco coisas que a spec não pediu. Decisão:

| Item | Decisão |
|---|---|
| `painel/auditoria_metodo.py` | **Entregue como está**; sem rota, sem teste. O ciclo 072 decide manter com teste ou remover. |
| `painel/arquitetura.html` (servido por `server.py:409-414`) | **Entregue**: é documentação do próprio painel, lida pelo navegador. |
| `painel/docs/roteiro-painel.md` | **Entregue** como roteiro de uso; o livro não o referencia ainda. |
| tipos `nota` e `recuperacao` no `registrar.py` | **Entregue**: estão no `CHECK` da tabela e no `data-model.md`; `recuperacao` é o que o DORA (*DevOps Research and Assessment*, as quatro métricas de entrega) precisa para tempo de restauração. |
| opção `--ts` do `registrar.py` | **Dívida para o 072**: aceita carimbo informado pelo autor e fura o "carimbo verificável" do FR2. Não se corrige aqui (raia retroativa, diff mínimo). |

### Dívidas entregues ao ciclo 072 (painel de regência)

1. **Acoplamento ao Hindiana.** Em `a1172a2`: `hindiana` em `registrar.py` (4), `server.py` (3),
   `mcp_painel.py` (1); `"Hindiana Office"` e `"Gilsiley"` fixos em `server.py`. Em `4919f4a` a
   troca da fixture já apagou as ocorrências dos exemplos de `registrar.py` e `mcp_painel.py`:
   restam **4, todas em `server.py`** (linhas 25, 87, 275, 342). Critério do 072:
   `grep -rin "hindiana\|Gilsiley" painel/*.py` → vazio fora de docstrings.
2. **Decisão definitiva sobre o escopo não declarado** (tabela acima): `auditoria_metodo.py`
   ganha teste ou sai.
3. **Teste da CLI** para `registrar.py peca` sem `--evidencia` → exit 2 e zero linhas inseridas.
   O teste de hoje (`test_peca_sem_evidencia_e_recusada`) cobre `valida_evento`, não a linha de
   comando.
4. **Opção `--ts`**: remover ou restringir a carimbo verificável.
5. `ux-design.md` semântico do painel (papel antes do componente) — nasce no 072, não aqui.

### Como foi medido no Windows

Windows 11, Git Bash (não PowerShell) para os scripts `scripts/check-*.sh`; `python3` é um
shim para o `python` do Windows; `PYTHONUTF8=1` no ambiente, porque sem ele o `print` de
acentos no `registrar.py` quebra em `cp1252`; `core.autocrlf=false` no worktree, porque o
`.dump` do SQLite e o `git status --porcelain` da fixture só comparam iguais com fim de linha
estável. O hook de pre-commit depende de `python` no caminho do Git Bash — limite da spec.

## Verification (DoD)

Medido em 20/10/2026 neste worktree (`integra/linha-paralela-066`); o `qa-report.md` cola a saída.

| Comando | Esperado |
|---|---|
| `python -m unittest discover -s painel/tests -p test_painel.py` | `Ran 12 tests`, `OK`, exit 0 |
| `python -m pytest .maestro/controle/git-hooks/test_veredito_hook.py -q` | `34 passed`, exit 0 |
| `python painel/registrar.py painel/projetos/exemplo.json peca --peca P1 --estado entregue --autor X --db <tmp.db>` (sem `--evidencia`) | exit 2, `recusado:` no stderr, `COUNT(*)` de `eventos` inalterado |
| idem com `--estado "suites aceitas" --evidencia '{"hash":"abc"}'` | exit ≠ 0 (falta `runner2`) |
| idem com `--evidencia '{"hash":"abc","runner2":"r2"}'` | exit 0, `COUNT(*)` cresce em 1 |
| `sqlite3 <db> "UPDATE eventos SET autor='x'"` · `"DELETE FROM eventos"` | erro de trigger `eventos e append-only`, exit ≠ 0 |
| `ingest.py` duas vezes sobre a fixture; `.dump` das derivadas | `diff` vazio; `eventos` intacta |
| `git -C <fixture> status --porcelain` antes/depois de `ingest.py` | idêntico |
| `grep -a -c SEGREDO <db>` após ingerir fixture com `.env` e `backups_producao/` | `0` (exceção declarada: `backups_producao/diario/backup.log` é lido — `ingest.py:25`) |
| grep de imports da spec (só stdlib + `__future__`, `builtins`, `ingest`, `server`, `mcp_painel`) | vazio |
| `grep -c 'ThreadingHTTPServer(("127.0.0.1"' painel/server.py` | `1` |
| `GET http://127.0.0.1:8765/api/estado-ia?sessao=W04` | 200; `voce` com `estado`, `peca`, `proximo`; `voce` = `null` para sessão inexistente |
| `grep -c proxy painel/server.py` · `painel/index.html` | ≥ 1 cada (merge só como proxy rotulado) |
| `grep -rin "hindiana\|Gilsiley" painel/*.py` | **registrado como dívida**, não como verde: 4 em `server.py` |
| `scripts/check-boundary.sh`, `check-language.sh`, `check-adr.sh`, `check-version.sh`, `check-links.sh` | verdes (medido em 20/10) |
| **mutação**: remover `painel/` de `toolkit.owns` em `boundary.json` | `check-boundary.sh` vermelho; restaurar → verde |
| **mutação**: veredito sem linha `Objeto:` em commit | `veredito_hook.py --pre-commit` exit 1 (recusa: `test_sem_linha_objeto_rejeita`, `test_hash_inexistente_rejeita`, `test_veredito_anterior_ao_objeto_rejeita`; aceite com carimbo válido → 0: `test_normal_aceita`, `test_hora_texto_igual_commit_aceita`, `test_hora_texto_dentro_tolerancia_aceita`) |
| `scripts/check-conformance.sh 066` | verde após `qa-report.md` (hoje vermelho só por plan/tasks/qa-report ausentes) |

<!--
  GATE (not delegable): o plano é aprovado pelo Darú antes de virar tasks.
  Handoff: plan-architect → (aprovação) → tasks → dev-implementer / qa.
-->
