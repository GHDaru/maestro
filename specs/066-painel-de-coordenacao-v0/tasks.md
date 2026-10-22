# Tasks 066 — Painel de coordenação v0 (projeção dos arquivos, só localhost)

> **Ciclo retroativo.** O código veio pronto da branch `painel-controle` (`a1172a2`). As tarefas
> marcadas `[x]` já aconteceram e têm o hash do commit como evidência; as `[ ]` são o que falta
> para o ciclo fechar pelo método — `qa-report.md`, revisão em contexto fresco, passagem de
> segurança, mutação dos portões tocados e o portão humano. Nenhuma caixa da cauda é marcada
> antes de a evidência existir: é isso que o hook `Stop` bloqueia.
>
> Siglas: ADR (*Architecture Decision Record*, registro de decisão de arquitetura) · DoD
> (*Definition of Done*, definição de pronto) · FR (*functional requirement*, requisito
> funcional) · CLI (*command-line interface*, linha de comando) · MCP (*Model Context Protocol*).

## Verification first

- [x] **T0** — DoD executável definida em `plan.md § Verification` a partir dos critérios de
      aceite da spec, cada linha com comando e resultado esperado. Medido em 20/10/2026 neste
      worktree: `Ran 12 tests OK`; `34 passed`; `check-boundary`, `check-language`,
      `check-adr`, `check-version`, `check-links` verdes; `check-conformance 066` vermelho só por
      `plan.md`/`tasks.md`/`qa-report.md` ausentes. (Princípio IV violado no v0 — testes depois
      do código — registrado no Complexity Tracking do plano.)

## Implementation (já feito — evidência: hash do commit)

- [x] **T1** — Integrar a branch `painel-controle` (`a1172a2`, 12 commits de 01 a 03/10/2026):
      `painel/` (ingest, server, registrar, mcp_painel, index.html, testes) e
      `.maestro/controle/git-hooks/` (hook de veredito + 34 testes). (FR1–FR6, FR8, FR9)
      Evidência: merge **`023694b`**.
- [x] **T2** — Spec retroativa `specs/066-painel-de-coordenacao-v0/spec.md`, aprovada pelo Darú
      em 20/10/2026 (`decisao-066-daru-20-10`: ciclo 066, fronteira toolkit, fixture).
      Evidência: **`4919f4a`**.
- [x] **T3** — ADR 0022 por `git mv` do rascunho "ADR 0021 (RASCUNHO)" de `painel/docs/`
      (histórico preservado) + linha no índice de decisões + operating-model §6 ("Metrics
      dashboard — Later / YAGNI" → "Coordination panel"). Evidência: **`4919f4a`**.
- [x] **T4** — Fronteira: `painel/` e `.maestro/` em `toolkit.owns` de `boundary.json`
      (ADR 0018; decisão 2 do Darú); `check-boundary.sh` verde. Evidência: **`4919f4a`**.
- [x] **T5** — Fixture `painel/projetos/exemplo.json` substitui `hindiana.json` (decisão 3 do
      Darú); os exemplos de `registrar.py` e `mcp_painel.py` passam a citar `exemplo.json`.
      (FR7) Evidência: **`4919f4a`**.
- [x] **T6** — CHANGELOG `[Unreleased]` e `docs/roadmap.md` atualizados no mesmo commit.
      Evidência: **`4919f4a`**.

## Fechamento (a fazer)

- [x] **T7** (`qa-report.md`, saídas reais) — Escrever `qa-report.md`: colar a saída de cada linha da DoD do plano (os dois
      comandos de teste, os três `registrar.py`, os dois `sqlite3`, a dupla ingestão, o
      `git status --porcelain`, o `grep -a -c SEGREDO`, o grep de imports, o `grep` de
      `127.0.0.1`, o `GET /api/estado-ia?sessao=W04` e com sessão inexistente, os `grep proxy`,
      os cinco `check-*.sh`). Registrar **como dívida, não como verde**: `grep -rin
      "hindiana\|Gilsiley" painel/*.py` → 4 em `server.py` (25, 87, 275, 342). Citar a violação
      do Princípio IV (testes depois do código) e as notas de medição no Windows (Git Bash,
      `python3` shim, `PYTHONUTF8=1`, `core.autocrlf=false`). Critério: cada linha da DoD tem
      saída colada; `scripts/check-conformance.sh 066` verde.
- [x] **T8** (`5161449`: `ux-design.md` apontador, opção a) — `ART:ux-design=yes` exige `ux-design.md` neste diretório; o semântico vive em
      `specs/066-painel-de-regencia/ux-design.md` (ciclo 072). **Decisão do gerente/Darú**:
      (a) ponteiro de uma página para o 072, ou (b) aceitar o item vermelho no gate com a razão
      registrada no `qa-report.md`. Nenhum segundo `ux-design.md` semântico é escrito aqui.
- [x] **T9** (`qa-report.md` §cobertura e §achados) — Registrar no `qa-report.md` a decisão do plano sobre o escopo não declarado
      (`auditoria_metodo.py`, `arquitetura.html`, `roteiro-painel.md`, tipos `nota`/`recuperacao`,
      opção `--ts`) e as cinco dívidas entregues ao ciclo 072 (acoplamento Hindiana, escopo,
      teste da CLI sem `--evidencia`, `--ts`, `ux-design.md` semântico).

## Living documentation (same pull request)

- [x] **T10** — ADR 0022, `decisoes.jsonl`, CHANGELOG, roadmap, operating-model §6, glossário
      da spec. Evidência: **`4919f4a`**. Nada mais a tocar nestes arquivos neste ciclo.

## Closing tail — MANDATORY, one line each, never delete

<!-- TICK ONLY WHILE WRITING THE EVIDENCE, never in advance: the box records what happened.
     Do not delete a line to say it does not apply: write `n/a: <reason>` on it.
     check-conformance.sh requires the evidence of every non-n/a step in qa-report.md. -->

- [x] **TAIL:review** — independent review in **fresh context**, by whoever did not execute
  (Theorem 2). Evidence: the verdict, in `qa-report.md`. Aqui: revisar a **integração**
  (`023694b` + `4919f4a`) contra a spec e o plano — a revisão de `a1172a2` já existe e é insumo,
  não substituto.
- [x] **TAIL:security** — security pass proportional to the risk class. Superfície: servidor
  HTTP local (`127.0.0.1`, 403 fora de localhost no `POST`), ingestão que nunca abre `.env` nem
  `backups_producao/` (exceção `diario/backup.log`), fixture sem IP/token/usuário, hook que roda
  `git` em subprocess. Evidence: `qa-report.md`.
- [x] **TAIL:mutation** — every gate this cycle created or changed was **broken on purpose
  and seen refusing**. Portões tocados: (1) `boundary.json` é insumo de `check-boundary.sh` —
  remover `painel/` de `toolkit.owns`, ver o script ficar vermelho, restaurar; (2) o hook de
  pre-commit — commit de veredito sem `Objeto:` recusado (exit 1); (3) os triggers de
  `eventos` — `UPDATE`/`DELETE` abortados. Evidence: the mutation and its output, in
  `qa-report.md`.
- [x] **TAIL:gate** (Darú, 20/10/2026, chat: "está aprovado" — os quatro ciclos 066–069 em bloco) — DoD green → guardian verdict → **human merge gate (not delegable)**;
  promotion via `scripts/promote-main.sh` (records `gate-main-<sha>` automatically, ADR 0009).
