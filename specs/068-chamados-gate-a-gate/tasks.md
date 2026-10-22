# Tasks 068 — Chamados gate a gate (o estado vem dos arquivos; o custo vem das sessões)

> **Ciclo retroativo.** O código veio pronto da branch `067-painel-chamados`
> (`db6b89c..2796cbf`, 10 commits) e entrou pelo merge `120a32c`. As tarefas `[x]` já
> aconteceram e têm o hash como evidência; as `[ ]` são o que falta para o ciclo fechar pelo
> método — glossário, `data-model.md`, `contracts/`, apontador de UX, `qa-report.md`, revisão
> em contexto fresco, passagem de segurança, mutação e o portão humano. Nenhuma caixa da cauda
> é marcada antes de a evidência existir.
>
> Siglas: ADR (*Architecture Decision Record*, registro de decisão de arquitetura) · DoD
> (*Definition of Done*, definição de pronto) · FR (*functional requirement*, requisito
> funcional) · BPMN (*Business Process Model and Notation*, notação de modelagem de processos)
> · HTTP (*Hypertext Transfer Protocol*) · JSON (*JavaScript Object Notation*) · UX (*user
> experience*, experiência do usuário) · IA (*inteligência artificial*) · CI (*Continuous
> Integration*, integração contínua).

## Verification first

- [x] **T0** — DoD executável definida em `plan.md § Verification` a partir dos critérios de
      aceite da spec, cada linha com comando e resultado esperado. Medido em 20/10/2026 neste
      worktree: `test_chamados` `Ran 6 tests OK`; `test_painel` `Ran 12 tests OK`;
      `python painel/custo.py painel/projetos/exemplo.json` → `{"arquivos_lidos": 5,
      "mensagens_novas": 311}`; `check-adr`, `check-links`, `check-language`,
      `check-boundary`, `check-version` verdes após o merge. (Princípio IV violado — testes
      depois do código e três regras sem teste nomeado — registrado no Complexity Tracking.)

## Implementation (já feito — evidência: hash do commit)

- [x] **T1** — `painel/chamados.py` (420 linhas): `GATES`, `PASSA`, `BARRA`, `OBRIG`;
      funções puras `cabecalho`, `numeros_limpos`, `valida`, `confere`; `le_chamados` lê o
      git (`--all --since`); `em_cache` em thread; `trilha` com eventos e custo por janela.
      (FR1, FR2, FR3, FR4, FR6) Evidência: merge **`120a32c`**.
- [x] **T2** — `painel/custo.py` (143 linhas): esquema `arquivos`/`sessoes`/`uso`, `indexa`
      incremental por offset com deduplicação por `id`, `janela` por sessão e intervalo. (FR7)
      Evidência: **`120a32c`**.
- [x] **T3** — `painel/server.py:429-440`: `GET /workflow-chamado.bpmn`,
      `GET /api/chamados/<id>/trilha`, `GET /api/chamados[?atualizar=1]`. (FR6, FR8)
      Evidência: **`120a32c`**.
- [x] **T4** — `painel/index.html` (+287): aba Chamados com vistas "Lista por gate" e
      "Tabela (board)" (`:598`), gaveta do chamado com abas Resumo e "Trilha (IA e
      auditoria)" (`:695`), visualizador do BPMN (`:730`). (FR5, FR6, FR8) Evidência:
      **`120a32c`**.
- [x] **T5** — `painel/workflow-chamado.bpmn` (643 linhas, 12 raias, 11 gates) e
      `.maestro/controle/git-hooks/pre-commit` chamando `veredito_hook.py --pre-commit`.
      (FR8) Evidência: **`120a32c`**.
- [x] **T6** — `painel/tests/test_chamados.py`: 6 testes nomeados na spec § Critérios,
      um por regra (f, e, a+b+c, f, g, FR3). (FR9) Evidência: **`120a32c`**.
- [x] **T7** — Resolução do conflito do merge como fixture: `painel/projetos/hindiana.json`
      continua apagado; `chamados-manuais-hindiana.json` (1133 linhas, dado real) removido e
      substituído por `chamados-manuais-exemplo.json`; `exemplo.json` ganha `chamados`,
      `chamados_manuais` e `custo_pastas = ["C--Users-ghdaru-Documents-010-PROJETOS-410-MAESTRO"]`;
      docstrings das fixtures citam `decisao-066-daru-20-10`. Evidência: **`120a32c`**.

## Fechamento (a fazer)

- [x] **T8** — Escrever este plano com o Constitution Check (oito linhas), os cinco `ART` e os
      quatro tokens `DOM` com motivo. Evidência: `specs/068-chamados-gate-a-gate/plan.md`;
      critério: `scripts/check-conformance.sh 068` imprime `domain model declared (aggregate,
      invariants, glossary, ports) with a reason`. Marcar ao commitar o arquivo.
- [x] **T9** (`docs/governance/glossary.md`, linhas "Cycle 068") — Acrescentar, em inglês
      (ADR 0014), no formato das linhas existentes (termo · expansão · definição · onde):
      **chamado** (ticket — one folder, one deliverable per gate), **gate** (`abertura, G0, GD,
      G1…G9`, each with an owner), **veredito** (verdict file with header `gate / objeto /
      veredito / por / data`; counts only if it passes the conferidor rules), **conferidor**
      (the rule checker; `chamados.py` mirrors it), **runner2** (second run by a non-author,
      counts only with failed 0 and errors 0), **pendente** (what a passed gate left for
      later; blocks G8 until `pendencias_aceitas`), **classe C** (risk class requiring an ADR
      and the product owner's decision), **trilha** (the ticket's timeline with cost per
      step), **custo por sessão** (tokens per session and minute, from transcripts).
      Definições: `spec.md § Glossário`. Também corrigir na spec o caminho do apontador de UX
      (`066-painel-de-regencia` → `066-painel-de-coordenacao-v0`, plano § How, decisão 9).
      Critério: `grep -c 'Cycle 068' docs/governance/glossary.md` ≥ 8; `check-language.sh` e
      `check-links.sh` verdes.
- [x] **T10** (`data-model.md`) — Chamado, Gate, Veredito (item), Trilha e índice de custo,
      com campos lidos de `chamados.py` e `custo.py`. Critério: o arquivo existe (`ART:data-model=yes`).
- [x] **T11** (`contracts/interfaces.md`) — As três rotas HTTP com formas de resposta, a CLI
      de `custo.py`, a forma do JSON de chamados manuais, as chaves novas do `projeto.json`, o
      BPMN como contrato do fluxo e o hook. Critério: o arquivo existe (`ART:contracts=yes`).
- [x] **T12** (`ux-design.md`, apontador) — Papéis semânticos das duas vistas novas apontando
      para `specs/066-painel-de-coordenacao-v0/ux-design.md` (kanban por gate; jornada por
      peça); heurística datada e captura do build real ficam para o 072 (`living-journey`).
      Critério: o arquivo existe (`ART:ux-design=yes`) e `check-links.sh` verde.
- [x] **T13** (`qa-report.md`, saídas reais) — Colar a saída de cada linha da DoD do plano:
      os dois `unittest`, os `grep` de `chamados.py`, `custo.py`, BPMN (incluindo a contagem
      de 11 gateways), `server.py`, `index.html`, `exemplo.json` e do hook; os dois `ls`; as
      duas corridas de `custo.py` (a segunda provando o offset); os quatro `check-*.sh`; o
      `grep` do glossário. Registrar **como dívida, não como verde**: acoplamento ao Hindiana
      (`grep` com saída não vazia), as três regras sem teste nomeado, o padrão de privacidade
      de `custo_pastas` (decisão do Darú), `unittest.main()` antes de `TestPendencia`. Citar
      a violação do Princípio IV e as notas de medição no Windows. Critério: cada linha da DoD
      tem saída colada; `scripts/check-conformance.sh 068` verde.

## Living documentation (same pull request)

- [x] **T14** (CHANGELOG `[Unreleased]` e roadmap F32) — `git show --stat 120a32c` não lista
      `CHANGELOG.md` nem `docs/roadmap.md`: uma entrada no CHANGELOG (gate de CI) e a linha
      F32 no roadmap, no mesmo commit do plano. Glossário: T9. ADR: **nenhum** (plano § How,
      decisão 7 — o ciclo não muda o método).

## Closing tail — MANDATORY, one line each, never delete

<!-- TICK ONLY WHILE WRITING THE EVIDENCE, never in advance: the box records what happened.
     Do not delete a line to say it does not apply: write `n/a: <reason>` on it.
     check-conformance.sh requires the evidence of every non-n/a step in qa-report.md. -->

- [x] **TAIL:review** — independent review in **fresh context**, by whoever did not execute
  (Theorem 2). Evidence: the verdict, in `qa-report.md`. Aqui: revisar a **integração**
  (`120a32c` + spec + este plano) contra os nove FR; conferir regra a regra que
  `chamados.py` faz o que a spec § FR2 diz (o portão só lê a forma dos `DOM`; julgar se as
  invariantes estão mesmo no domínio é desta revisão); conferir que a fixture não carrega
  dado real do Hindiana.
- [x] **TAIL:security** — security pass proportional to the risk class. Classe **média**: o
  indexador lê o diretório pessoal do usuário (`~/.claude/projects/`). O que a passagem checa:
  (1) `custo.py` só abre `*.jsonl` das pastas que casam `custo_pastas` e só grava em
  `painel/dados/custo.db` — nunca escreve no projeto nem fora de `painel/dados/`; (2) o que vai
  para `custo.db` é contagem de tokens, título da sessão e caminho do transcript — **nenhum
  conteúdo de mensagem**; (3) `chamados.py` só chama `git log`/`git show` com argumentos
  fixos e o `id` do chamado vem da URL sem ir para o shell (`subprocess.run` em lista);
  (4) as três rotas são `GET` em `127.0.0.1`; (5) registrar a ambiguidade da substring
  (plano § How, decisão 8) como achado para o Darú, não como verde. Evidence: `qa-report.md`.
- [x] **TAIL:mutation** — every gate this cycle created or changed was **broken on purpose
  and seen refusing**. Nenhum `scripts/check-*.sh` é tocado; o "portão" deste ciclo são as
  regras do conferidor em `chamados.py`, provadas pelos 6 testes, e o fio do hook. Mutações:
  (a) em `numeros_limpos` trocar `e == "0"` por `True` →
  `test_runner2_com_errors_nao_conta` vermelho; (b) em `confere` apagar a condição
  `and not validos[-1]["pendencias_aceitas"]` (`:213`) →
  `test_pendente_passa_o_gate_mas_trava_o_g8_ate_ser_aceita` vermelho; (c) na fixture do
  teste (b) trocar `pytest 2751/0/14` por `pytest 2751/0/0` → o mesmo teste vermelho (prova
  que o teste discrimina, não só que passa); (d) apagar `--pre-commit` de
  `.maestro/controle/git-hooks/pre-commit` → `grep -c 'veredito_hook.py --pre-commit'` = `0`;
  **restaurar** os quatro → `Ran 6 tests OK` e `grep` = `1`. Evidence: the mutation and its
  output, in `qa-report.md`.
- [x] **TAIL:gate** (Darú, 20/10/2026, chat: "está aprovado" — os quatro ciclos 066–069 em bloco) — DoD green → guardian verdict → **human merge gate (not delegable)**;
  promotion via `scripts/promote-main.sh` (records `gate-main-<sha>` automatically, ADR 0009).
