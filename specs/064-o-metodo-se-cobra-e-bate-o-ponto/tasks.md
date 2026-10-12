# Tasks 064 — O método se cobra sozinho e bate o ponto

> Executado **pelo próprio livro de ponto**: cada tarefa abaixo foi distribuída com a etiqueta
> `[[TASK id=064-Tn ...]]` a uma sessão executora com o mod `maestro-ledger` e o hook `Stop`
> ativos. O registro está em `docs/records/tarefas.jsonl`.

## Verification first
- [x] T0 — protótipo medido antes da spec: hook `Stop` (5 casos + ao vivo), mod (7 testes, 7
      mutações, ao vivo contra o relatório da sessão), gravador (50 escritas simultâneas).
      O defeito do instalador (`CONFLICT` consigo mesmo) reproduzido.

## Implementation
- [x] T1 — instalador copia `stop-conformance.py` e `record-task.py`; `--no-hooks` preserva o
      hook; `scripts/*.py` executáveis. (FR1, FR3)
- [x] T2 — `merge-settings.py` ganha `UPGRADE` com `PREVIOUS_HOOKS`; o instalador o trata. (FR2)
      Tentativa 1 entregou o código; a 1 e a 2 ficaram `blocked` — o sandbox das executoras
      negou criar o projeto de teste. A prova de instalação real foi rodada pelo gerente.
- [x] T3 — segunda entrada no `marketplace.json`; o instalador imprime o passo do plugin. (FR4)
- [x] T4 — `docs/governance/task-ledger.md` + linha no bloco do `CLAUDE.md` + glossário. (FR5)
- [x] T5 — `scripts/report-tasks.py` + o portão `scripts/check-ledger.sh`. (FR6)
- [x] T6 — `check-installed.sh` exige que todo hook citado exista e seja executável; o
      instalador copia o `report-tasks.py`; passo do mod na integração contínua; índice de
      scripts. (FR7)
- [x] T7 — relatório não inventa custo por modelo; só `audit`/`review` dão veredito. A parte
      do mod foi feita pelo gerente (tentativa 2): o sandbox protege os arquivos de hook.

### Revisão independente R1 — reprovou: 3 bloqueantes, 10 importantes, 7 menores
- [x] F1 — hook `Stop`: só o ciclo mais novo, raiz em `$CLAUDE_PROJECT_DIR`, razão das linhas
      ✗ reais; `UPGRADE` testado contra JSON literal; UTF-8 partido; `--dry-run`; anti-padrão 21.
      (achados 1, 2, 4, 9, 15, 19)
- [x] F2 — `--cycle` mantém vereditos; gravador recusa tipos errados e exige `by`; relatório
      tolera linhas ruins, só conta vereditos de juízes, mostra "não medido" em vez de zero;
      escrita parcial repetida. (achados 3, 7, 13, 14)
- [x] F3 — mod: etiqueta sozinha na linha, primeira TASK e última DONE, `]` entre aspas,
      sessão alheia não substitui tarefa aberta, próxima tentativa substitui, DONE trocado
      registrado, modelo vazio vira `unknown`. Feito pelo gerente (sandbox). (achados 5, 6, 8, 20)
- [x] F4 — documentos alinhados ao código, raia no cabeçalho, siglas expandidas, pareamento
      por tentativa. (achados 11, 16, 17, 18)
- [x] F5 — gerente: limite do Windows declarado, ADR 0021, roadmap, CHANGELOG, este arquivo.
      (achados 10, 12, 14)

### Revisão independente R2 — aprovou com ressalvas (N1–N7)
- [x] F6 — relatório: veredito só conta se a sessão for a da auditoria; veredito de ciclo
      (`-cycle`); fixture de pareamento; limites declarados; roteiro de teste da spec refeito
      para a etiqueta sozinha na linha. (N1, N2, N3, N4, N7; resíduos 5, 6, 14)
- [x] F7 — mod: sessão alheia não volta a tentativa de uma tarefa aberta; testes de texto
      depois da etiqueta e de `bridge`/`sdk` como pessoa. Feito pelo gerente. (N5, N6)

## Closing tail — MANDATORY, one line each, never delete
<!-- TICK ONLY WHILE WRITING THE EVIDENCE, never in advance: the box records what happened.
     Do not delete a line to say it does not apply: write `n/a: <reason>` on it.
     check-conformance.sh requires the evidence of every non-n/a step in qa-report.md. -->
- [x] TAIL:review — independent review in fresh context, by whoever did not execute
- [x] TAIL:security — security pass proportional to the risk class
- [x] TAIL:mutation — every gate created or changed here, broken on purpose and seen refusing
- [x] TAIL:gate — DoD green -> guardian verdict -> human merge gate (not delegable)
