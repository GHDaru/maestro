# Data Model — Workflow do Painel Maestro

## Entidades

### rodadas
Uma rodada de trabalho coordenada pelo painel Maestro.

| Campo       | Tipo | Descrição                          |
|-------------|------|------------------------------------|
| id          | TEXT PK | Identificador (ex: "001")        |
| desejo      | TEXT | Objetivo da rodada                  |
| criada_por  | TEXT | Sessão que abriu                    |
| aberta_em   | TEXT | ISO-8601 timestamp de abertura      |
| fechada_em  | TEXT | ISO-8601 ou NULL (aberta)           |

### passos
Cada passo executado dentro de uma rodada. Append-only.

| Campo           | Tipo | Descrição                              |
|-----------------|------|----------------------------------------|
| id              | INTEGER PK | Auto-increment                    |
| rodada          | TEXT FK → rodadas.id | Rodada pai              |
| passo           | TEXT | Identificador do passo (ex: "T1")      |
| sessao          | TEXT | Sessão que executou                    |
| entrada_em      | TEXT | ISO-8601: quando entrou (NULL = não entrou) |
| resumo          | TEXT | Resumo do que foi feito                |
| saida_em        | TEXT | ISO-8601: quando saiu (NULL = aberto)  |
| evidencia_json  | TEXT | JSON: hashes, contagens, logs          |
| resultado       | TEXT | "ok" \| "erro" \| "skip" \| NULL       |

### transicoes
Define o grafo de passos e quais transições exigem evidência.

| Campo             | Tipo | Descrição                          |
|-------------------|------|------------------------------------|
| passo             | TEXT | Passo de origem                    |
| proximo           | TEXT | Passo de destino                   |
| evidencia_exigida | INTEGER | 1 = exige resumo+evidência, 0 = não |

PK: (passo, proximo)

### fila
Outbox de mensagens entre sessões. Hooks escrevem, painel lê.

| Campo          | Tipo | Descrição                          |
|----------------|------|------------------------------------|
| id             | INTEGER PK | Auto-increment               |
| sessao_origem  | TEXT | Sessão que enfileirou              |
| sessao_destino | TEXT | Destino ou NULL (broadcast)        |
| payload        | TEXT | JSON                               |
| criada_em      | TEXT | ISO-8601                           |
| lida_em        | TEXT | ISO-8601 ou NULL (pendente)        |

## Relações

```
rodadas 1───* passos
transicoes: passo → proximo (grafo de passos)
fila: sessao_origem → sessao_destino (mensagens assíncronas)
```

## Invariantes

1. **Append-only**: `passos` nunca tem linha deletada ou campo sobrescrito. Correção = nova linha.
2. **WAL**: `PRAGMA journal_mode = wal` para leitura concorrente sem bloquear escrita.
3. **Passo aberto**: `entrada_em IS NOT NULL AND saida_em IS NULL` → passo em execução.
4. **Evidência obrigatória**: se `transicoes.evidencia_exigida = 1`, `passos.resumo` e `passos.evidencia_json` devem ser não-NULL antes de `saida_em`.
5. **Fila outbox**: `lida_em IS NULL` → mensagem pendente; hook Stop enfileira, hook SessionStart drena.

## Modo WAL

SQLite WAL permite leitores concorrentes enquanto o hook escreve. O painel (leitor) nunca bloqueia. O `-wal` e `-shm` ficam ao lado do `.db`.

## FR13 — Eventos sem lock

A tabela `eventos` (append-only, triggers de UPDATE/DELETE) vive no mesmo DB em modo WAL.
Transações de escrita em `eventos` são curtas (INSERT + COMMIT), então o WAL nunca segura o lock
por mais que alguns milissegundos. O ingest (T4) reconstrói tabelas derivadas num DB temporário
e faz swap atómico (`os.replace`), nunca tocando nas tabelas append-only durante a reconstrução.

## FR14 — Swap atómico

O ingest (T4) escreve as tabelas derivadas num arquivo temporário (`painel.db.tmp`).
Só quando todas as tabelas estão populadas ele faz `os.replace(tmp, db)` — atómico no SO.
Se o ingest for interrompido antes do `os.replace`, o `.tmp` fica incompleto mas o `.db`
original permanece intacto com a versão anterior completa.
