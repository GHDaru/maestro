# Tasks 069 — Conferidor pela data (o veredito vigente é o mais novo, não o último no alfabeto)

> **Ciclo retroativo.** O código veio pronto da branch `067-painel-chamados`
> (`2796cbf..aa0efd1`, 21 commits de 09/10/2026, chamado 070 do Hindiana) e entrou pelo merge
> `23f8325`. As tarefas `[x]` já aconteceram e têm o hash como evidência; as `[ ]` são o que
> falta para o ciclo fechar pelo método — plano, glossário, `qa-report.md`, revisão em contexto
> fresco, passagem de segurança, registro das mutações e o portão humano. Nenhuma caixa da
> cauda é marcada antes de a evidência existir.
>
> Siglas: ADR (*Architecture Decision Record*, registro de decisão de arquitetura) · DoD
> (*Definition of Done*, definição de pronto) · FR (*functional requirement*, requisito
> funcional) · DoR (*Definition of Ready*, definição de pronto para começar) · CI (*Continuous
> Integration*, integração contínua).

## Verification first

- [x] **T0** — DoD executável definida em `plan.md § Verification` a partir dos critérios de
      aceite da spec, cada linha com comando e resultado esperado. Medido em 20/10/2026 neste
      worktree: `test_chamados` `Ran 10 tests OK`; `test_painel` `Ran 12 tests OK`;
      `git merge-base --is-ancestor 6741315 d2822ef` → `0`. Princípio IV **vale** para FR1
      (par vermelho/verde `6741315` → `d2822ef`, assinado por não autor); FR2 e FR3 são testes
      de regressão sobre comportamento que a base já tinha — declarado no plano, não vendido
      como vermelho/verde.

## Implementation (já feito — evidência: hash do commit)

- [x] **T1** — `painel/chamados.py`: `MINIMO` (`:112`) e a função pura
      `ordem_veredito(item, commit_de)` (`:115-118`), tupla data do cabeçalho, commit do
      arquivo, nome; `confere` a aplica em `validos = sorted(...)` (`:151`). (FR1, FR2)
      Origem: `d2822ef` na linha paralela. Evidência: merge **`23f8325`**.
- [x] **T2** — `painel/tests/test_chamados.py`, classe `TestOrdemDoVeredito` (`:88`):
      `test_mais_novo_vence_mesmo_vindo_antes_no_alfabeto` (FR1, vermelho em `6741315`),
      `test_empate_de_data_desempata_pelo_commit_do_arquivo` (FR1 desempate),
      `test_r4_trilha_em_ordem_de_data_nao_de_nome` (FR3, mutante verificado em `98a62a1`),
      `test_r3_veredito_sem_data_legivel_nao_vence` (FR2, `6ea2347`). (FR1–FR4)
      Evidência: **`23f8325`**.
- [x] **T3** — `specs/070-conferidor-ordem-veredito/` com os dez arquivos de gate, sem edição:
      `00-chamado.md`, `spec.md`, `G0-reproducao.md`, `GD-risco.md`, `G1-W11.md`,
      `G2-vermelho-W13-6741315.md`, `G3-codigo-W10.md`, `G3-criterio-W01-d2822ef.md`,
      `G3-runner2-W13-d2822ef-8adb545a.md`, `G3-runner2-W13-98a62a1.md`. Pasta mantém o id
      070 (plano § How, decisão 4). (FR5) Evidência: **`23f8325`**.
- [x] **T4** — Branch lateral `699bddb` (`w10/070-g3-codigo`) **não** integrada: só carece
      de 8 arquivos e não acrescenta nada (`git diff --stat aa0efd1 699bddb -- specs/070-*`);
      preservada na tag local `arquivo/paralela/w10-070-g3-codigo`. (plano § How, decisão 5)

## Fechamento (a fazer)

- [x] **T5** — Escrever este plano com o Constitution Check (oito linhas), os cinco `ART` e os
      quatro tokens `DOM` com motivo. Evidência: `specs/069-conferidor-pela-data/plan.md`;
      critério: `scripts/check-conformance.sh 069` imprime `domain model declared (aggregate,
      invariants, glossary, ports) with a reason`. Marcar ao commitar o arquivo.
- [x] **T6** (`docs/governance/glossary.md`, linhas "Cycle 069") — Acrescentar, em inglês
      (ADR 0014), no formato das linhas existentes (termo · expansão · definição · onde), dois
      termos: **veredito vigente** (the one verdict that decides a single-verdict gate — GD,
      G4 to G9 — when more than one is valid: the latest header `data:` on the right hash; tie
      by the file's commit date, then by name; before cycle 069 it was the last file in
      alphabetical order) e **data legível** (a header `data:` that matches `RE_DATA`,
      `YYYY-MM-DD HH:MM ±ZZZZ`; a verdict without one is rejected by `valida` and never wins).
      A linha **Veredito** do 068 passa a remeter a "veredito vigente". Definições:
      `spec.md § Glossário deste ciclo`. Critério: `grep -c 'Cycle 069'
      docs/governance/glossary.md` ≥ 2; `check-language.sh` e `check-links.sh` verdes.
- [x] **T7** (`qa-report.md`, saídas reais) — Colar a saída de cada linha da DoD do plano: os
      dois `unittest`; os `grep` de `test_chamados.py` e `chamados.py`; as duas mutações com o
      resultado observado (ver TAIL:mutation); o `git diff --exit-code` da restauração; o `ls`
      da pasta 070 e os quatro `grep` nos arquivos de gate (`FALHA_ESPERADA`, `APPROVE`,
      `escopo: correcao`, `classe: A`); o `merge-base`; o `diff --stat` de `699bddb`; os
      `check-*.sh`; o `grep` do glossário. Registrar **como dívida, não como verde**: `data()`
      sem `try/except` (security-pass achado 1), o ramo `or MINIMO` sem teste (mutante
      equivalente), o desempate por nome sem teste, a author date forjável. Citar a nota de
      método (GD depois do G3) e as notas de medição no Windows. Critério: cada linha da DoD
      tem saída colada; `scripts/check-conformance.sh 069` verde.

## Living documentation (same pull request)

- [x] **T8** (CHANGELOG `[Unreleased]` e roadmap F33) — Conferir que `23f8325` já trouxe a
      entrada "ciclo 069" no CHANGELOG (`:13`, gate de CI) e a linha **F33** no roadmap
      (`:139`); ajustar só se o plano mudar o enunciado. Critério: `grep -c 'ciclo 069'
      CHANGELOG.md` ≥ 1; `grep -c 'F33' docs/roadmap.md` ≥ 1. Glossário: T6. ADR:
      **nenhum** (plano § How, decisão 6 — correção de feature, não decisão de metodologia; a
      ambiguidade "adotar o padrão de gates do Hindiana" é do Darú e terá ADR em ciclo próprio).

## Closing tail — MANDATORY, one line each, never delete

<!-- TICK ONLY WHILE WRITING THE EVIDENCE, never in advance: the box records what happened.
     Do not delete a line to say it does not apply: write `n/a: <reason>` on it.
     check-conformance.sh requires the evidence of every non-n/a step in qa-report.md. -->

- [x] **TAIL:review** — independent review in **fresh context**, by whoever did not execute
  (Theorem 2). Evidence: the verdict, in `qa-report.md`. Aqui: revisar a **integração**
  (`23f8325` + spec + este plano) contra os cinco FR; conferir que `ordem_veredito` faz o que
  FR1 diz (data, depois commit, depois nome) e que `validos[-1]` (`:219`) é quem decide nos
  gates de veredito único; conferir que a pasta 070 entrou **sem edição** (`git diff aa0efd1
  HEAD -- specs/070-*` vazio) e que o Princípio IV está relatado com honestidade (só FR1 é
  vermelho/verde).
- [x] **TAIL:security** — security pass proportional to the risk class. Classe **baixa**
  (função pura; arquivos de evidência). Já feita em contexto fresco: `security-pass.md`
  (20/10/2026, sobre HEAD `23f8325`) — veredito OK sem bloqueio; achado 1 (média,
  pré-existente: `data()` deixa `strptime` levantar e derruba a vista do painel) e achado 2
  (baixa: author date forjável) viram dívidas 1 e 4 do plano. A tarefa aqui é **citar** o
  arquivo e os achados no `qa-report.md`. Evidence: `security-pass.md` + `qa-report.md`.
- [x] **TAIL:mutation** — every gate this cycle created or changed was **broken on purpose
  and seen refusing**. Nenhum `scripts/check-*.sh` é tocado; o "portão" deste ciclo é
  `ordem_veredito`, provada pelos 4 testes. Mutações **já rodadas e restauradas byte a byte**
  em 20/10 — a tarefa é **registrá-las** no `qa-report.md` com a saída: (a) `ordem_veredito`
  devolve `(item["arquivo"],)` (ordem alfabética antiga) → `FAILED (failures=2)`,
  `test_mais_novo_vence...` e `test_empate_de_data...` vermelhos — o portão recusa; (b)
  `or MINIMO` da data trocado por uma data do ano 2999 → `Ran 10 tests OK` — **mutante
  equivalente** no cenário testado, porque `valida` exclui a data ilegível antes do `sort` e
  o ramo só é alcançável com `data:` ausente, caso sem teste (plano § How, decisão 3; dívida
  2). Registrar (b) como lacuna, não como verde. Evidence: the mutation and its output, in
  `qa-report.md`.
- [ ] **TAIL:gate** — DoD green → guardian verdict → **human merge gate (not delegable)**;
  promotion via `scripts/promote-main.sh` (records `gate-main-<sha>` automatically, ADR 0009).
