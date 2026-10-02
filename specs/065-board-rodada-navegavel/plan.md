# Plan 065 — Board enxuto, rodada navegável e workflow por tarefa

- **Spec**: `spec.md` · **UX**: `ux-design.md` (W03, ced12bf) · **Date**: 2026-10-02
- **Status**: Draft (pode haver revisão após emenda do Gilsiley)
- **Depende de**: 064 (workflow em SQLite — tabelas `rodadas`, `passos`, `transicoes`, `fila`)

## 1. Data model

### Tabelas derivadas (materializadas no ingest, swap atómico da 064)

#### `arvore_rodada` — árvore navegável da rodada (FR8, FR9, FR12)

| Campo        | Tipo    | Descrição                          |
|--------------|---------|------------------------------------|
| rodada       | TEXT    | ID da rodada (ex: "001")           |
| tipo         | TEXT    | "spec" \| "plan" \| "task" \| "critica" \| "teste" |
| id_no        | TEXT    | ID do nó (ex: "FR13", "T2", "test_fr13_…") |
| pai          | TEXT    | ID do nó pai (NULL = raiz)          |
| label        | TEXT    | Texto exibido                       |
| status       | TEXT    | "ok" \| "pendente" \| "descoberto"  |
| referencia   | TEXT    | Caminho/commit/teste referenciado   |
| hash         | TEXT    | Hash do commit ou teste             |
| evidencia_ok | INTEGER | 1 = hash confere, 0 = diverge       |

PK: (rodada, tipo, id_no)

#### `status_workers` — estado por sessão para o board (FR2, FR13)

| Campo           | Tipo    | Descrição                          |
|-----------------|---------|------------------------------------|
| sessao          | TEXT PK | Nome da sessão                     |
| estado          | TEXT    | "busy" \| "idle" \| "erro"         |
| peca            | TEXT    | Spec/tarefa atual                  |
| passo           | TEXT    | Passo do workflow                  |
| esperando       | TEXT    | Quem espera (NULL = ninguém)       |
| ultima_atividade| TEXT    | ISO-8601 do último evento          |
| sem_tarefa_ciclos| INTEGER | Ciclos consecutivos sem tarefa     |

#### `excecoes_board` — 3 exceções do topo (FR1)

| Campo        | Tipo    | Descrição                          |
|--------------|---------|------------------------------------|
| tipo         | TEXT PK | "gilsiley" \| "gate_push" \| "sem_tarefa_2ciclos" |
| contador     | INTEGER | Quantidade                          |
| detalhe_json | TEXT    | JSON com itens                     |

### Tabelas existentes (064, não modificadas)

- `rodadas` — id, desejo, criada_por, aberta_em, fechada_em
- `passos` — rodada, passo, sessao, entrada_em, resumo, saida_em, evidencia_json, resultado
- `transicoes` — passo, proximo, evidencia_exigida
- `fila` — outbox entre sessões
- `eventos` — append-only (status, deploy, incidente)

## 2. Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Arquivos    │────▶│   ingest.py  │────▶│  painel.db   │
│  (fonte de   │     │  (materializa│     │  (SQLite WAL)│
│   verdade)   │     │   árvore +   │     │              │
│              │     │   status +   │     │  arvore_     │
│  spec.md     │     │   exceções)  │     │  rodada      │
│  tasks.md    │     │              │     │  status_     │
│  commits     │     │  swap        │     │  workers     │
│  testes      │     │  atómico     │     │  excecoes_   │
│              │     │  (FR14)      │     │  board       │
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                  │
                                           ┌──────▼───────┐
                                           │  server.py   │
                                           │  (queries)   │
                                           │              │
                                           │  GET /api/   │
                                           │  rodadas     │
                                           │  GET /api/   │
                                           │  board       │
                                           │  GET /api/   │
                                           │  roadmap     │
                                           └──────┬───────┘
                                                  │
                                           ┌──────▼───────┐
                                           │  index.html  │
                                           │  (UI)        │
                                           │              │
                                           │  Board       │
                                           │  Árvore      │
                                           │  Workflow    │
                                           │  Roadmap     │
                                           └──────────────┘
```

### Ingest materializa a árvore (FR12)

O `ingest.py` lê as convenções e popula `arvore_rodada`:

1. **Spec → FRs**: lê `spec.md`, extrai `FR1`…`FR13`, cria nós `tipo='spec'`
2. **Tasks → T**: lê `tasks.md`, extrai `T1`…`Tn`, cria nós `tipo='task'`
3. **T → FR**: lê `T2 → FR13` no tasks.md, liga `T2` como filho de `FR13`
4. **Commit → T**: lê `git log`, extrai `064 T2: …`, liga commit ao nó `T2`
5. **Teste → FR**: lê nomes de arquivos `test_fr13_…`, liga teste ao `FR13`
6. **Descoberto**: se FR não tem teste filho → `status='descoberto'` (FR10)
7. **Evidência**: se `evidencia_json.hash` ≠ hash do commit → `evidencia_ok=0` (FR7)

### UI consulta (não deriva em tempo real)

A UI faz `GET /api/rodadas?id=R001` → server.py query em `arvore_rodada` → JSON → renderiza árvore. Toda a derivação é no ingest (Clarify #2 da spec).

## 3. Tasks

### T1 — Schema: tabelas derivadas arvore_rodada, status_workers, excecoes_board
**FRs**: FR8, FR12 (arvore_rodada), FR2, FR13 (status_workers), FR1 (excecoes_board)
- `schema_065.sql` — CREATE TABLE IF NOT EXISTS para as 3 tabelas
- Índices: `idx_arvore_rodada_pai`, `idx_status_workers_estado`
- Test: `test_schema_065.py` — tabelas existem, colunas corretas, WAL

### T2 — Ingest: materializa arvore_rodada das convenções
**FRs**: FR8, FR12
- `ingest.py` — nova função `ingere_arvore(db, cfg)` que lê spec.md, tasks.md, commits, testes
- Popula `arvore_rodada` com nós spec/plan/task/critica/teste
- Liga T→FR, commit→T, teste→FR
- Marca `descoberto` onde FR sem teste (FR10)
- Test: `test_ingere_arvore.py` — árvore correta para spec 064 real

### T3 — Ingest: materializa status_workers e excecoes_board
**FRs**: FR1, FR2, FR13
- `ingest.py` — `ingere_status_workers(db, cfg)` lê estado das sessões
- `ingest.py` — `ingere_excecoes(db, cfg)` calcula as 3 exceções
- FR13: compara últimos 2 ciclos de status (30 min cada, ~60 min)
- Test: `test_ingere_status.py` — exceções corretas, sem_tarefa_2ciclos

### T4 — Server: endpoints /api/board, /api/rodadas, /api/roadmap
**FRs**: FR1, FR2, FR5, FR8, FR9, FR11
- `server.py` — `GET /api/board` retorna exceções + sessões
- `server.py` — `GET /api/rodadas?id=R001` retorna árvore materializada
- `server.py` — `GET /api/roadmap` retorna raias por ciclo
- Test: `test_server_065.py` — endpoints retornam JSON correto

### T5 — UI: Board enxuto (3 exceções + linha por sessão)
**FRs**: FR1, FR2, FR3, FR4
- `index.html` — view Board com 3 cards de exceção no topo
- Linha por sessão com 5 colunas (FR2)
- Filtro "só exceções" por padrão (FR3)
- Hook event como "última atividade há N min" (FR4)
- Test: `test_board_navegavel.py` — board renderiza, filtro funciona

### T6 — UI: Árvore navegável da rodada
**FRs**: FR8, FR9, FR10
- `index.html` — tree view da rodada com 4 ramos (spec, plan, tasks, críticas)
- Click no nó → artefato à direita com breadcrumb (FR9)
- Chip amarelo "descoberto" onde FR sem teste (FR10)
- Test: `test_board_navegavel.py` — árvore renderiza, click abre artefato

### T7 — UI: Workflow por tarefa (linha do tempo)
**FRs**: FR5, FR6, FR7
- `index.html` — click tarefa → linha do tempo dos passos (FR6)
- Passo atual + tempo (FR5)
- Chip amarelo se evidência ≠ hash (FR7)
- Test: `test_workflow_tarefa.py` — linha do tempo, chip de divergência

### T8 — UI: Roadmap com raias por ciclo
**FRs**: FR11
- `index.html` — view Roadmap com 3 raias (atual, próximo, depois)
- Card por rodada com barra de progresso, gates pendentes, gate push no topo
- Test: `test_board_navegavel.py` — roadmap renderiza, click card → árvore

### T9 — Ingest: evidência ≠ hash → marca divergência
**FRs**: FR7
- `ingest.py` — compara `evidencia_json.hash` com hash do commit
- Popula `arvore_rodada.evidencia_ok = 0` se divergir
- Test: `test_evidencia_divergencia.py` — divergência detectada

### T10 — data-model.md
- Documenta entidades, relações, invariantes
- Diagrama ER

## 4. Verification (DoD)

- `python -m pytest tests/test_board_navegavel.py` → todos passam
- `python -m pytest tests/test_workflow_tarefa.py` → todos passam
- `python -m pytest tests/test_schema_065.py` → todos passam
- `python -m pytest tests/test_ingere_arvore.py` → todos passam
- Board abre no filtro "só exceções" por padrão
- Click em tarefa → linha do tempo com evidência
- Evidência ≠ hash → chip amarelo
- Requisito sem teste → chip amarelo "descoberto"

## 5. Regra nova

Código de produto SÓ em `hindiana/`. Maestro é ferramenta. Em `ola/` só `especificacao/` + `ferramentas/` + `testes/`.

## 6. Dependências

- 064 (W09): tabelas `rodadas`, `passos`, `transicoes`, `fila` — já integradas (6056e97)
- UX design (W03): `ux-design.md` — ced12bf
- `spec.md` e `tasks.md` das rodadas — lidos pelo ingest

## 7. Risks

- Árvore materializada pode ficar stale se ingest não rodar após commit novo (mitigado por FR11 da 064 — aviso de leitura velha >1h)
- Convenções (T→FR, commit→T) dependem de formato consistente — se worker usar formato diferente, nó não liga (mitigado por validação no ingest)
- `status_workers` precisa do loop de status de 30 min rodando — se parar, FR13 não atualiza
