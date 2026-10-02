-- T1: Schema 065 — tabelas derivadas para board enxuto, rodada navegável e workflow por tarefa.
-- Materializadas no ingest, swap atómico herdado da 064. Stdlib sqlite3 compatível.
--
-- arvore_rodada:   árvore navegável da rodada (FR8, FR9, FR12)
-- status_workers:  estado por sessão para o board (FR2, FR13)
-- excecoes_board:  3 exceções do topo do board (FR1)

PRAGMA journal_mode = WAL;

CREATE TABLE IF NOT EXISTS arvore_rodada (
  rodada        TEXT    NOT NULL,           -- ID da rodada (ex: "064")
  tipo          TEXT    NOT NULL,           -- "spec" | "plan" | "task" | "critica" | "teste"
  id_no         TEXT    NOT NULL,           -- ID do nó (ex: "FR13", "T2", "test_fr13_…")
  pai           TEXT,                       -- ID do nó pai (NULL = raiz)
  label         TEXT    NOT NULL,           -- texto exibido
  status        TEXT    NOT NULL DEFAULT 'pendente',  -- "ok" | "pendente" | "descoberto"
  referencia    TEXT,                       -- caminho/commit/teste referenciado
  hash          TEXT,                       -- hash do commit ou teste
  evidencia_ok  INTEGER NOT NULL DEFAULT 1, -- 1 = hash confere, 0 = diverge
  PRIMARY KEY (rodada, tipo, id_no)
);

CREATE TABLE IF NOT EXISTS status_workers (
  sessao            TEXT    PRIMARY KEY,    -- nome da sessão
  estado            TEXT    NOT NULL DEFAULT 'idle',  -- "busy" | "idle" | "erro"
  peca              TEXT,                   -- spec/tarefa atual
  passo             TEXT,                   -- passo do workflow
  esperando         TEXT,                   -- quem espera (NULL = ninguém)
  ultima_atividade  TEXT,                   -- ISO-8601 do último evento
  sem_tarefa_ciclos INTEGER NOT NULL DEFAULT 0  -- ciclos consecutivos sem tarefa
);

CREATE TABLE IF NOT EXISTS excecoes_board (
  tipo          TEXT    PRIMARY KEY,        -- "gilsiley" | "gate_push" | "sem_tarefa_2ciclos"
  contador      INTEGER NOT NULL DEFAULT 0, -- quantidade
  detalhe_json  TEXT                        -- JSON com itens
);

-- Índices para queries do board e árvore
CREATE INDEX IF NOT EXISTS idx_arvore_rodada_pai ON arvore_rodada(rodada, pai);
CREATE INDEX IF NOT EXISTS idx_status_workers_estado ON status_workers(estado);
