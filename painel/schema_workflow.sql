-- T1: Schema SQLite para workflow do painel Maestro.
-- Tabelas append-only em modo WAL. Stdlib sqlite3 compatível.
--
-- rodadas:    uma rodada de trabalho (ex: "Rodada 001: melhorar painel")
-- passos:     cada passo de cada rodada, com entrada/saída/evidência
-- transicoes: qual passo vem depois de qual, e se exige evidência
-- fila:       outbox de mensagens entre sessões (hooks escrevem, painel lê)

PRAGMA journal_mode = WAL;

CREATE TABLE IF NOT EXISTS rodadas (
  id          TEXT    PRIMARY KEY,   -- ex: "001"
  desejo      TEXT    NOT NULL,      -- objetivo da rodada
  criada_por  TEXT    NOT NULL,      -- sessão que abriu
  aberta_em   TEXT    NOT NULL,      -- ISO-8601 timestamp
  fechada_em  TEXT                    -- NULL = aberta
);

CREATE TABLE IF NOT EXISTS passos (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  rodada          TEXT    NOT NULL REFERENCES rodadas(id),
  passo           TEXT    NOT NULL,   -- ex: "T1", "T2"
  sessao          TEXT    NOT NULL,   -- sessão que executou
  entrada_em      TEXT,               -- ISO-8601: quando entrou no passo
  resumo          TEXT,               -- resumo do que foi feito
  saida_em        TEXT,               -- ISO-8601: quando saiu do passo (NULL = aberto)
  evidencia_json  TEXT,               -- JSON: hashes, contagens, logs
  resultado       TEXT                -- "ok" | "erro" | "skip" | NULL
);

CREATE TABLE IF NOT EXISTS transicoes (
  passo            TEXT    NOT NULL,  -- passo de origem
  proximo          TEXT    NOT NULL,  -- passo de destino
  evidencia_exigida INTEGER NOT NULL DEFAULT 1,  -- 1 = exige resumo+evidência, 0 = não
  PRIMARY KEY (passo, proximo)
);

CREATE TABLE IF NOT EXISTS fila (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  sessao_origem  TEXT    NOT NULL,    -- sessão que enfileirou
  sessao_destino TEXT,                 -- NULL = broadcast
  payload        TEXT    NOT NULL,     -- JSON
  criada_em      TEXT    NOT NULL,     -- ISO-8601
  lida_em        TEXT                   -- NULL = pendente
);

-- Índices para queries dos hooks
CREATE INDEX IF NOT EXISTS idx_passos_abertos ON passos(rodada) WHERE saida_em IS NULL;
CREATE INDEX IF NOT EXISTS idx_fila_pendente ON fila(criada_em) WHERE lida_em IS NULL;
