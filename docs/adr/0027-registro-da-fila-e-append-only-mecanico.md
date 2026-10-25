# ADR 0027 — O registro da fila é arquivo do painel, e o append-only é mecânico

- **Status**: Aceito · **Data**: 2026-10-24 · **Ciclo**: 072 (rodada 1 do painel de regência; a rodada 2 fica declarada infra)
- **Supersede**: nada; complementa o ADR 0025 (tabelas do workflow como dado primário) e o ADR 0022 (painel como projeção). **Superado por**: —
- **Origem**: gate do plano do ciclo 072, aberto por delegação (ADR 0026) e aprovado com condições pelo crítico em contexto fresco: o plano havia escolhido o endereço do registro e os dois mecanismos de append-only, mas a decisão não estava escrita como ADR; o crítico pediu que endereço, backup e rodada 2 fossem registrados de forma durável **antes** de o código existir. Rascunho pelo Worker02 (`specs/072-painel-de-regencia/adr-0027-rascunho.md`); texto final pela sessão regente, porque a lista de negação dos Workers proíbe escrever em `docs/adr/` (decisão de segurança do ciclo 066).
- **Evidência que a sustenta**: `specs/072-painel-de-regencia/plan.md` § 2 e § 3 · `contracts/rotas.md` · `data-model.md` § 3 · `painel/tests/test_regencia.py` (24 testes vermelhos, o contrato executável) · `painel/.gitignore` (linha `dados/`) · `painel/server.py` (o `.db` já mora em `painel/dados/`).
- **Implementação**: tarefas W05 (fila) e W02 (gatilhos) do ciclo 072; esta linha e o arquivo entram antes delas.

Siglas: ADR (*Architecture Decision Record*, registro de decisão de arquitetura) · FR (*functional requirement*, requisito funcional) · JSONL (*JSON Lines*, um objeto JSON por linha) · WAL (*write-ahead log*, modo de escrita do SQLite) · AST (*abstract syntax tree*, árvore sintática do código).

## Contexto

A fila de decisões da rodada 1 (FR16) precisa de um **arquivo** onde o regente registre pedidos e
rulings, e o registro tem de ser **append-only**: o valor do registro está em nunca poder ser
reescrito em silêncio. Duas forças em conflito:

1. a **anti-regra 7** do `ux-design.md` § 4 é literal: "não escreve em arquivo do projeto"; o
   painel lê o projeto, não escreve nele;
2. a inclinação inicial do plano apontava para `docs/records/`, que é pasta do projeto (o painel
   a ingere) e cujo `decisoes.jsonl` é do método, não do painel.

## Opções avaliadas

- **(a) `docs/records/`**: versionado e visível em pull request, mas o painel passaria a escrever
  dentro do que ele lê, quebrando a anti-regra 7 e misturando o índice do método com dado de
  operação.
- **(b) `painel/dados/fila-<projeto>.jsonl`**, ao lado do `.db` que o servidor já cria: satisfaz a
  anti-regra 7 e o FR16; preço: a pasta é ignorada pelo git, a fila é local.
- **(c) SQLite (tabela `rulings`)**: mesma localidade de (b), mas perde a legibilidade de um
  arquivo de texto que o regente pode abrir, levar e auditar sem ferramenta.

## Decisão

**1. O endereço é `painel/dados/fila-<projeto>.jsonl`** (chave `cfg["fila_decisoes"]`; padrão ao
lado do `<projeto>.db`). `painel/dados/` é, por construção, o próprio dado do painel: o único lugar
que satisfaz a anti-regra 7 e o FR16 ao mesmo tempo.

**Troca declarada (D-072-1).** `painel/dados/` é ignorado pelo git. A fila é **local**: não é
versionada, não viaja no clone e não aparece em revisão de pull request. O índice versionado de
decisões continua sendo `docs/records/decisoes.jsonl`: outro artefato, outro dono.

**2. O append-only é mecânico, com duas provas.**

- **Fila (FR16)**: `painel/fila_registro.py` abre sempre em modo de acrescentar
  (`open(caminho, "a", encoding="utf-8")`), nunca `"w"`, `truncate` ou `seek`; escreve uma linha por
  chamada (`json.dumps(..., ensure_ascii=False)` mais `\n`), sob um `threading.Lock` de módulo
  (escritor único no processo). Provas: o prefixo de bytes anterior fica inalterado; um teste
  estático (AST) recusa qualquer `open` que não seja de acrescentar; um teste concorrente exige duas
  linhas de dois `POST` em paralelo, nenhuma perdida.
- **Workflow herdado do 070 (FR17, a dívida 5 vira requisito)**: gatilhos em
  `painel/schema_workflow.sql`: `rodadas`, `transicoes` e `fila` recusam `UPDATE` e `DELETE`;
  `passos` recusa `DELETE` sempre e `UPDATE` a menos que `saida_em IS NULL` e só nas colunas
  `saida_em`, `resumo` e `resultado` (`BEFORE UPDATE ... WHEN ...` com `RAISE(ABORT, ...)`).

**3. O `WHEN` preserva o 070.** O hook `Stop` fecha o passo com `UPDATE passos SET saida_em, resultado`,
exatamente as colunas e o estado que o `WHEN` libera. Sem ele, o gatilho quebraria o fechamento do
passo (FR3 do 070). `painel/hooks/workflow_stop.py` fica intocado nesta rodada; a cobrança de verdade
do `Stop` (dívida 7) segue para a rodada 2.

**4. Backup datado do registro.** A fila é o único dado do regente e é local: `fila_registro.py`
chama `backup_datado(caminho, agora)` antes da primeira escrita de cada dia, copiando o arquivo para
`painel/dados/backup/fila-<projeto>-<AAAA-MM-DD>.jsonl` dentro do mesmo lock. O README do painel
documenta o comando manual de exportação. O backup mitiga a perda; não desfaz D-072-1.

**5. A rodada 2 é declarada infra.** As dívidas 3, 6, 7 e 10 do 070 (instalador sem dry run;
`SessionStart` imprimindo payload no stdout; FR3 invertido do `Stop`; troca atômica com WAL,
`PermissionError` no Windows e broadcast consumido pelo primeiro leitor) exigem
`wal_checkpoint(TRUNCATE)`, lock de ingest, backup antes da troca e teste de interrupção. Nenhuma se
paga nesta rodada e nenhuma é vendida como paga.

## Consequências

- O painel nunca escreve dentro do projeto que lê; o append é garantido pela base e pelo processo,
  não por convenção; o 070 não é mutilado para pagar a dívida 5; a perda da fila tem ponto de
  retorno diário.
- Aceitas e declaradas: a fila não é versionada (D-072-1); a dívida 2 do 070 (`_ensure_schema` em
  três cópias) piora um pouco, porque os `CREATE TRIGGER IF NOT EXISTS` entram nas cópias e precisam
  ficar em sincronia (D-072-2); o backup é uma cópia por dia, não um histórico por linha.
- Dívidas abertas: D-072-1 a D-072-8, em `plan.md` § Dívidas declaradas.

## Como desfazer

Trocar `cfg["fila_decisoes"]` para outro caminho não muda o código; mover a fila para o SQLite
(opção c) é uma migração de leitura com o mesmo contrato de `acrescenta`. Remover os gatilhos é um
`DROP TRIGGER` por tabela, com o teste `test_divida5_gatilho_recusa_update_e_delete` voltando a
vermelho como aviso. Um ADR posterior supersede este.

## Emenda (24/10/2026, tarefa 072-T07 — acréscimo, o texto acima não foi reescrito)

Ao implementar os gatilhos, o Worker02 mostrou dois fatos que a Decisão 2 não previa:

1. **`fila` também precisa do `WHEN`.** O `drenar` de `painel/fila_outbox.py` (ciclo 070) marca a
   mensagem lida com `UPDATE fila SET lida_em`; recusar todo `UPDATE` em `fila` quebraria três
   testes do 070 hoje verdes. Regra em vigor: `fila` recusa `DELETE` sempre e `UPDATE` a menos que
   `lida_em IS NULL` e só na coluna `lida_em`; `rodadas` e `transicoes` continuam recusando
   `UPDATE` e `DELETE`; `passos` como na Decisão 2.
2. **São oito gatilhos, não quatro**: o SQLite exige um gatilho por evento (`BEFORE UPDATE` e
   `BEFORE DELETE`) por tabela.

Evidência: `specs/072-painel-de-regencia/qa-report.md` § 072-T07 (commits `61e78b5`, `d1cb955` em
`w/worker02`; `TestDivida5Gatilho` verde; suíte do 070 com 48 e hooks com 26 verdes).

