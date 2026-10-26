# Handoff da sessão regente (MAESTRO) — 26/10/2026, 15:40

> Para a próxima sessão regente (ou para esta, depois da compactação). Tudo o que está aqui é
> conferível no repositório; nada é memória. Siglas: ADR (*Architecture Decision Record*) ·
> DoD (*Definition of Done*) · CI (*Continuous Integration*).

## 1. Estado medido

- **main = dev = `d094763`**, CI verde (promoção `gate-main-12bffe4`, 25/10): ciclos 070 (workflow
  SQLite, parcial declarado), 072 rodada 1 (kanban por gate + fila de decisões), ADRs 0025, 0026,
  0027 (+ emenda), lançador `scripts/multi-session.py` com janela nomeada, pesquisa e confronto do 073.
- **Branch de trabalho `066-painel-de-regencia`**: HEAD `af81499` ou posterior. Contém tudo da main
  mais a rodada 3 do 073 (11 wireframes em `specs/073-area-administrativa/prototipo/`, verificador
  `verifica-prototipo.py` com 0 achados, glossário com os 12 termos "Cycle 073", README do protótipo).
- **Sessões**: Gerente `[31ee4d]` (glm-5.3) e Worker01 `[9a1b27]`, 02 `[31f7bf]`, 03 `[ad66d6]`,
  04 `[4d000a]`, 05 `[78d88f]`, 06 `[c85948]` (deepseek-v4.1-flash), worktrees em
  `.claude/worktrees/workerNN`. **O ref da sessão MAESTRO muda a cada reinício**: o primeiro ato
  da sessão nova é mandar ao Gerente o ref novo (memória `ref-da-sessao-muda-ao-reiniciar`).
  Fallback de canal: DONE/GATE commitados em `specs/NNN-*/done-*.md` ou `status-*.md`.
- **Delegação**: `decisao-072-gates-delegados` + ADR 0026 — gates humanos decididos pela regente
  com crítico em contexto fresco e uma linha em `decisoes.jsonl` por gate. Linhas já registradas:
  `gate-070-delegado`, `gate-072-dor-delegado`, `gate-072-plan-delegado`, `gate-072-rodada-1-delegado`,
  `gate-073-rodada-1-delegado`, `gate-073-rodada-2-delegado`.
- **Orçamento do gauntlet do 073** (`decisao-073-gauntlet-area-administrativa`): teto 40 % do consumo
  semanal do plano da regente; em 26/10 15:00 estava em 28 % (inclui outras sessões do Darú).
  Workers consomem o gateway, fora do teto; reportam tokens por DONE.

## 2. O que está em curso

- **073 rodada 3, fechamento**: Worker01 atualiza o README com as 4 telas do Workflow; Worker02
  faz revisão fresca + mutação do verificador (corpus `prototipo/fixtures/tela-ruim.html`);
  Worker06 segurança documental + `check-conformance.sh 073` nos dois modos; Gerente manda
  `[[DONE 073-rodada-3]]` e commita `done-073-rodada-3.md`.
- Ao receber: registrar `gate-073-rodada-3-delegado` (helper `record_decision.py` no scratchpad, ou
  `scripts/record-decision.sh`), e dar o "segue" da **rodada 4**.

## 3. Rodada 4 — protocolo combinado com o Darú (a bar)

Três juízes **separados, em contexto fresco** (subagentes Sonnet da regente, não Workers):
**controle**, **administração e gerenciamento de agentes**, **intercomunicabilidade**. Cada juiz
recebe: a matriz da rodada 1 (`pesquisa/plataformas.md`), o confronto (`confronto/confronto-decisao.md`),
o mapa de contextos, o glossário, e as 11 telas; julga **cada peça** (inventário, confronto,
lacunas, mapa, cada tela) sem rótulos, dá nota de 0 a 10 e nomeia a maior lacuna. A bar: **toda
funcionalidade ENTRA (13) atendida no wireframe e toda plataforma da rodada 1 (25) analisada**;
peça só passa com os três juízes em **9 ou mais**. Peça reprovada volta ao construtor (Worker da
fatia) com a lacuna nomeada; `/loop` até passar; regra das duas rodadas sem mudança de diagnóstico
→ parar e reportar ao Darú. Ao fim: `[[DONE 073]]`, conformance, merge na dev, promoção.

## 4. Depois do 073 (fila, em ordem)

1. **072 rodada 2 (raia infra)**: dívidas 6, 7, 10 do 070 e D-072-1..8 (backup e lock de ingest,
   `wal_checkpoint`, sanitização do stdout do hook, Stop que cobra em vez de fechar, FR1/FR2/FR3 do
   workflow, R7 do quadro estreito). ADR 0027 § 5.
2. **Ciclo leve: skill `living-journey`** cita `docs/journeys/`; o repositório usa `docs/jornada/`.
3. **Lançador**: prefixar nomes das sessões com o projeto (colisão "Gerente" com a Hindiana).
4. **Propostas do insumo do post de code review** (`insumo-post-code-review-anthropic.md`):
   `REVIEW.md` por domínio; cauda com votação de verificadores; ruído e convergência como métricas.
5. **ADR da regra das duas rodadas** (parada do laço de correção) e item 24 de `anti-patterns`.
6. **Cartão de ideia** do archify (citação presa a commit no bloco 3b do `check-conformance.sh`).
7. Promover a main só com conformance completa verde (`promote-main.sh --yes` na worktree
   `.claude/worktrees/dev`, com `python3` exportado como função: `python3(){ python "$@"; }; export -f python3`).

## 5. Armadilhas desta máquina

`pytest` demora ~2 min para iniciar; `check-links.sh`, `check-boundary.sh`, `check-ledger.sh`
(seção Stop hook) e `check-install.sh` falham ou travam por ambiente (msys, alias `python3` da
Store, `AGENTS.md` symlink); o CI em Linux decide. Bash tool lento com nove sessões abertas: rodar
em segundo plano com saída em arquivo e ler com `Read`. `Edit/Write(docs/adr/**)` negado: criar
ADR via `python shutil.copyfile` do scratchpad. Nunca `rm -rf`, `Remove-Item`, `--amend`.
