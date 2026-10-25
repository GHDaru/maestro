# ADR 0027 (rascunho) — O registro da fila é arquivo do painel, e o append-only é mecânico

> **Rascunho do ciclo 072.** O ADR **formal** vai para
> `docs/adr/0027-registro-da-fila-e-append-only-mecanico.md` (com o cabeçalho do padrão, ver os
> vizinhos `docs/adr/0026-*.md`), escrito na sessão **Worker01 [21d8d2]** (task `072-T09`), que também
> **acrescenta a linha** ao índice `docs/records/decisoes.jsonl` via `scripts/record-decision.sh`.
> Este arquivo é **novo** — nenhum ADR, `decisoes.jsonl` ou ideia é reescrito (guard
> `guard-immutables.py`).
>
> **Ordem obrigatória:** o arquivo do ADR **e** a linha no índice entram **ANTES** do código do
> registro (`072-T05`) — o caminho de escrita que este ADR fixa **precede** quem o implementa.
> Gravar depois seria decidir com o código já feito.
>
> Siglas: ADR (*Architecture Decision Record*) · FR (*functional requirement*) · JSONL (*JSON Lines*) ·
> WAL (*Write-Ahead Logging*).

- **Status**: proposto (rascunho) · **Data**: 2026-10-24 · **Ciclo**: 072 · **Raia**: plena (a
  rodada 2 fica declarada **infra**)
- **Supersede**: nada · **Emenda**: nada (a decisão é nova) · **Superado por**: —
- **Origem**: gate do plano do ciclo 072, aprovado **com condições** (delegado ao crítico independente,
  ADR 0026): o plano tinha escolhido o endereço do registro e os dois mecanismos de append-only, mas a
  decisão não estava escrita como ADR; o crítico pediu que o endereço, o backup e a rodada 2 fossem
  registrados em forma durável antes de o código existir.
- **Evidência que a sustenta**: `specs/072-painel-de-regencia/plan.md` §2 e §3 ·
  `contracts/rotas.md` · `data-model.md` §3/§3.1 · `painel/tests/test_regencia.py` (o contrato
  executável) · `painel/.gitignore` (a linha `dados/`) · `painel/server.py:540` (o `.db` já mora em
  `painel/dados/`).

## Contexto

A fila de decisões da rodada 1 (FR16) precisa de um **arquivo** onde o regente registre pedidos e
*rulings*, e o registro tem de ser **append-only** — o valor do registro está em nunca poder ser
reescrito em silêncio. Havia duas forças em conflito:

1. a **anti-regra 7** do `ux-design.md` §4 (`specs/066-painel-de-regencia/ux-design.md:120`) é
   literal: *"Não escreve em arquivo do projeto"* — o painel **lê** o projeto, não escreve nele; e
2. a inclinação inicial do plano apontava para `docs/records/`, que **é** pasta do projeto (o painel
   a ingere) e cujo `decisoes.jsonl` é **do método**, não do painel.

## Decisão

**1. O endereço é `painel/dados/fila-<projeto>.jsonl`** (chave `cfg["fila_decisoes"]`; padrão ao lado
do `<projeto>.db` que o servidor já cria em `painel/dados/`). `painel/dados/` é, por construção, *o
próprio dado do painel* — o único lugar que satisfaz a anti-regra 7 **e** o FR16 ao mesmo tempo.
Gravar em `docs/records/` faria o painel **escrever dentro do que ele lê**.

**Troca declarada (e aceita) — D-072-1.** `painel/dados/` é **ignorado pelo git**
(`painel/.gitignore`, linha `dados/`). Logo a fila é **local**: não é versionada, não viaja no clone e
não aparece em revisão de pull request. É o preço de a anti-regra 7 ser literal. O índice
**versionado** de decisões continua sendo `docs/records/decisoes.jsonl`, outro artefato, outro dono.

**2. O append-only é mecânico, e tem duas provas** (`plan.md` §3):

- **Fila (FR16)** — `painel/fila_registro.py` abre **sempre** em modo de acrescentar
  (`open(caminho, "a", encoding="utf-8")`) e **nunca** `"w"`/`truncate`/`seek`; escreve **uma** linha
  por chamada (`json.dumps(..., ensure_ascii=False)` + `\n`), tudo sob um `threading.Lock` de módulo
  (**escritor único** no processo). Provas: o **prefixo de bytes** anterior fica byte a byte
  inalterado; um teste **estático (AST)** recusa qualquer `open` que não seja de acrescentar; e um
  teste **concorrente** exige duas linhas de dois `POST` em paralelo, nenhuma perdida.
- **Workflow herdado do 070 (FR17 — a dívida 5 vira FR)** — quatro `TRIGGER`s em
  `painel/schema_workflow.sql`: `rodadas`, `transicoes` e `fila` recusam `UPDATE` **e** `DELETE`;
  `passos` recusa `DELETE` sempre e `UPDATE` **a menos que** `saida_em IS NULL` **e** só nas colunas
  `saida_em`, `resumo` e `resultado` (`BEFORE UPDATE ... WHEN ...` → `RAISE(ABORT, …)`).

**3. O `WHEN` não é detalhe — é o que preserva o 070.** O hook `Stop` fecha o passo com
`UPDATE passos SET saida_em=…, resultado=…`, exatamente as colunas e o estado que o `WHEN` libera.
Sem o `WHEN`, o gatilho **quebraria o fechamento do passo** (FR3 do 070) e a saída seria "consertar" o
hook — invertendo o FR3 (dívida 7). **Decidimos não fazer isso**: `painel/hooks/workflow_stop.py`
fica **intocado** nesta rodada, e a cobrança de verdade do `Stop` (dívida 7) segue para a rodada 2.

**4. Backup datado do registro.** A fila é o único dado do regente e é local: `painel/fila_registro.py`
chama `backup_datado(caminho, agora)` **antes da primeira escrita de cada dia**, copiando o arquivo
para `painel/dados/backup/fila-<projeto>-<AAAA-MM-DD>.jsonl` (`shutil.copy2`), dentro do **mesmo
lock** — não se grava antes de o backup do dia existir. O `README` do painel ganha o **comando manual
de exportação** para o regente levar a fila embora. O backup **mitiga** a perda; **não** desfaz a
troca declarada em D-072-1.

**5. A rodada 2 é declarada infra.** As dívidas 3, 6, 7 e 10 do 070 (backup/dry run do
`install_hooks.py`; `SessionStart` imprimindo payload no stdout; o FR3 invertido do `Stop`; a troca
atômica com WAL — `-wal`/`-shm` velhos, `PermissionError` no Windows, broadcast consumido pelo
primeiro leitor) exigem `wal_checkpoint(TRUNCATE)`, lock de ingest, backup antes da troca e teste de
interrupção. Nenhuma delas se paga nesta rodada, e **nenhuma é vendida como paga** aqui.

## Consequências

- **Positivas**: o painel nunca escreve dentro do projeto que ele lê; o append é garantido pela base e
  pelo processo, não por convenção; o 070 não é mutilado para pagar a dívida 5; a perda da fila tem
  ponto de retorno diário.
- **Negativas (aceitas e declaradas)**: a fila não é versionada (D-072-1); a dívida 2 do 070
  (`_ensure_schema` em três cópias) **piora** um pouco, porque os `CREATE TRIGGER IF NOT EXISTS` entram
  nas cópias e precisam ficar em sincronia (D-072-2); o backup é **uma cópia por dia**, não um
  histórico por linha.
- **Dívidas que ficam abertas**: D-072-1 a D-072-8, detalhadas em `plan.md` §"Dívidas declaradas".

## Linha para o índice (`docs/records/decisoes.jsonl`, só acréscimo)

A ser executada por `072-T09` (Worker01), **antes** de `072-T05`:

```text
scripts/record-decision.sh '{"id":"adr-0027","data":"2026-10-24","titulo":"O registro da fila e um arquivo do painel (fora do projeto) e o append-only e mecanico","status":"aceita","registro":"docs/adr/0027-registro-da-fila-e-append-only-mecanico.md"}'
```

> O `registro` cita um arquivo que **precisa existir completo** quando a linha entra — o
> `record-decision.sh` recusa apontar para placeholder (checagem 3 do script). Por isso o `072-T09`
> escreve o ADR **e** a linha na mesma entrega, antes do código.
