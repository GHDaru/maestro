# Tasks 067 — Trava de domínio no plan (o modelo de domínio é declarado, nunca omitido)

> **Ciclo retroativo.** O código veio pronto da branch `trava-dominio-plan` (`db6b89c`) e
> entrou pelo merge `b5775ac`. As tarefas `[x]` já aconteceram e têm o hash como evidência; as
> `[ ]` são o que falta para o ciclo fechar pelo método — glossário, `qa-report.md`, revisão
> em contexto fresco, passagem de segurança, mutação do portão e o portão humano. Nenhuma
> caixa da cauda é marcada antes de a evidência existir.
>
> Siglas: ADR (*Architecture Decision Record*, registro de decisão de arquitetura) · DoD
> (*Definition of Done*, definição de pronto) · FR (*functional requirement*, requisito
> funcional) · DDD (*Domain-Driven Design*, projeto dirigido pelo domínio) · DORA (*DevOps
> Research and Assessment*, as quatro métricas de entrega) · CI (*Continuous Integration*,
> integração contínua).

## Verification first

- [x] **T0** — DoD executável definida em `plan.md § Verification` a partir dos critérios de
      aceite da spec, cada linha com comando e resultado esperado, incluindo as três mutações
      do portão. Medido em 20/10/2026 neste worktree: painel `Ran 12 tests OK`;
      `check-language`, `check-boundary`, `check-links` verdes; `check-conformance 066` verde
      e imprime `domain-model declarations: not checked below cycle 67`. (Princípio IV
      violado — filtro do DORA sem teste — registrado no Complexity Tracking do plano.)

## Implementation (já feito — evidência: hash do commit)

- [x] **T1** — Seção "Domain model (declare all four — silence is not a decision)" no
      `.specify/templates/plan-template.md` (+22, linhas 49-69): quatro tokens `DOM:` em
      tabela com coluna de motivo e comentário explicando `none`/`changed`, `domain`/`edge`.
      (FR1) Origem `14f77a5`; evidência: merge **`b5775ac`**.
- [x] **T2** — Bloco 3b em `scripts/check-conformance.sh` (+62): piso `DOM_FLOOR=67` por
      `MAESTRO_MIN_CYCLE_DOMAIN`, só número e só ≤ 67 (senão exit 2); cada token exige valor e
      motivo; falha soft; abaixo do piso imprime que não checou. (FR2, FR3) Origem `14f77a5`;
      evidência: **`b5775ac`**.
- [x] **T3** — Forma itemizada `regra_a=domain | regra_b=edge(porquê)` em `DOM:invariants=`;
      item `=edge` sem parênteses reprova nomeando o item (`check-conformance.sh:369-389`).
      (FR4) Origem `a94574a`; evidência: **`b5775ac`**.
- [x] **T4** — `painel/index.html:293,299`: contador "N sem plan ou tasks" no cabeçalho do
      repositório e "falta" na coluna Plan da spec sem `tem_plan` ou sem `tasks_total`. (FR5)
      Origem `14f77a5`; evidência: **`b5775ac`**.
- [x] **T5** — `painel/server.py` `v_dora` (`:150`) conta só `deploy` com
      `_ambiente(e) in ("", "production", "producao", "produção")` (`:158`; `_ambiente` em
      `:141`). (FR6) Origem `db6b89c`; evidência: **`b5775ac`**.
- [x] **T6** — Spec retroativa `specs/067-trava-de-dominio-no-plan/spec.md` (seis FR lidos do
      diff, raia plena justificada pelo §3, limites declarados). Evidência: o arquivo neste
      diretório (não commitado ainda — entra no mesmo commit do plano e das tasks).

## Fechamento (a fazer)

- [x] **T7** — Escrever este plano com o Constitution Check (oito linhas), os cinco `ART` e os
      **quatro tokens `DOM` com motivo** — o ciclo que cria o portão não pode ser o primeiro a
      dispensá-lo. Evidência: `specs/067-trava-de-dominio-no-plan/plan.md § Domain model`;
      critério: `scripts/check-conformance.sh 067` imprime `domain model declared (aggregate,
      invariants, glossary, ports) with a reason` (a corrida completa só fica verde após T9).
- [x] **T8** (`docs/governance/glossary.md`, 5 linhas "Cycle 067") (`DOM:glossary=changed`) — Acrescentar a `docs/governance/glossary.md` (em inglês,
      ADR 0014; formato das linhas existentes: termo · expansão · definição · onde) os cinco
      termos que o template passa a exigir: **modelo de domínio declarado** (*declared domain
      model* — os quatro tokens `DOM`, ciclo 067), **raiz de agregado** (*aggregate root*),
      **invariante** (*invariant* — domínio ou borda com motivo), **porta/adaptador**
      (*port/adapter*), **linguagem ubíqua** (*ubiquitous language* — mora neste glossário).
      Definições: `spec.md § Glossário deste ciclo`. Critério: `grep -c 'aggregate root'
      docs/governance/glossary.md` ≥ 1; `scripts/check-language.sh` e `check-links.sh` verdes.
- [x] **T9** (`qa-report.md`, saídas reais) (`qa-report.md`, saídas reais) — Colar a saída de cada linha da DoD do plano: os
      dois `grep` do template, os três `MAESTRO_MIN_CYCLE_DOMAIN` (abc, 99, 60), o
      `check-conformance 066` e `067`, o teste do painel, os `grep` de `server.py`,
      `index.html` e `ingest.py`, os três `check-*.sh`, o `grep` do glossário. Registrar
      **como dívida, não como verde**: filtro de ambiente do DORA sem teste; `ambiente`
      ausente = produção (decisão do Darú em ciclo posterior); forma itemizada × célula Why
      (plano § How, decisão 3). Citar a violação do Princípio IV e as notas de medição no
      Windows (Git Bash, `python3` shim, `PYTHONUTF8=1`, `core.autocrlf=false`, `echo $?`).
      Critério: cada linha da DoD tem saída colada; `scripts/check-conformance.sh 067` verde.
- [x] **T10** (opção a: ADR 0023 escrito; a revisão apontou que a constituição o exige) (decisão do gerente/Darú) — O merge `b5775ac` não trouxe ADR, e este ciclo
      muda o método (declaração obrigatória nova + bloco novo no portão). Escolher: (a) ADR
      0023 "modelo de domínio declarado no plan, cobrado pelo portão a partir do 067" +
      linha via `scripts/record-decision.sh` + `check-adr.sh` verde, ou (b) registrar a
      ausência como dívida no `qa-report.md` com a razão. Nenhuma das duas é silêncio.

## Living documentation (same pull request)

- [x] **T11** (CHANGELOG `[Unreleased]` e roadmap F31) — Conferir se `b5775ac` tocou `CHANGELOG.md` `[Unreleased]` e `docs/roadmap.md`
      para este ciclo (`git show --stat b5775ac` lista só 4 arquivos — provavelmente **não**).
      Se não: uma entrada no CHANGELOG (gate de CI) e uma linha no roadmap, no mesmo commit
      do plano. Glossário: T8. ADR: T10.

## Closing tail — MANDATORY, one line each, never delete

<!-- TICK ONLY WHILE WRITING THE EVIDENCE, never in advance: the box records what happened.
     Do not delete a line to say it does not apply: write `n/a: <reason>` on it.
     check-conformance.sh requires the evidence of every non-n/a step in qa-report.md. -->

- [x] **TAIL:review** — independent review in **fresh context**, by whoever did not execute
  (Theorem 2). Evidence: the verdict, in `qa-report.md`. Aqui: revisar a **integração**
  (`b5775ac` + spec + este plano) contra os seis FR, e ler o **conteúdo** dos quatro `DOM`
  deste plano — o portão só lê a forma; julgar se o motivo da borda é bom é desta revisão.
- [x] **TAIL:security** — security pass proportional to the risk class. Classe **baixa**, e a
  passagem acontece (sem dispensa): o bloco 3b roda em todo push de CI e em toda promoção.
  O que a passagem checa: (1) o `sed`/`grep` do bloco 3b sobre `plan.md` forjado — linha
  `DOM:` com `$(...)`, aspas, `|` em excesso, `\r` — não executa nada nem trava o script;
  (2) a validação de `MAESTRO_MIN_CYCLE_DOMAIN` (não numérico, vazio, negativo, `067` com
  zero à esquerda, acima do piso) sempre falha **fechada**; (3) o filtro de `_ambiente` não
  lê nada fora da evidência do evento. Evidence: `qa-report.md`.
- [x] **TAIL:mutation** — every gate this cycle created or changed was **broken on purpose
  and seen refusing**. Portão tocado: bloco 3b de `check-conformance.sh`, sobre o
  **próprio `plan.md` deste ciclo**: (a) apagar a linha `DOM:aggregate` →
  `scripts/check-conformance.sh 067` imprime `domain model never declared in plan.md:
  aggregate` e sai `1` (`--ticked-only`: `·` e `0`); (b) trocar a declaração das invariantes
  por `` `DOM:invariants=edge` `` com a célula Why vazia → `declared DOM:invariants=edge
  with no reason`; (b') forma itemizada `regra_dora=edge` sem parênteses → `'regra_dora=edge'
  is edge with no reason`; (c) `MAESTRO_MIN_CYCLE_DOMAIN=abc` → exit `2`; **restaurar** o
  plano e a variável → verde. Evidence: the mutation and its output, in `qa-report.md`.
- [ ] **TAIL:gate** — DoD green → guardian verdict → **human merge gate (not delegable)**;
  promotion via `scripts/promote-main.sh` (records `gate-main-<sha>` automatically, ADR 0009).
