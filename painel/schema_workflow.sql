-- T1: Schema SQLite para workflow do painel Maestro.
-- Tabelas append-only em modo WAL. Stdlib sqlite3 compatível.
--
-- Append-only imposto pela base (FR17 — a dívida 5 do 070 vira requisito): os gatilhos ao
-- fim deste arquivo recusam UPDATE/DELETE por TRIGGER, não por convenção. O SQLite aceita
-- um só evento por gatilho, então há dois por tabela. `passos` e `fila` guardam um
-- fechamento legítimo herdado do 070 — o hook Stop fecha o passo e o drain marca a
-- mensagem como lida — e o `WHEN` libera só esse fechamento; qualquer outra escrita é
-- recusada. `rodadas` e `transicoes` não têm fechamento: recusam todo UPDATE e DELETE.
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

-- ---------------------------------------------------------------------------
-- Append-only mecânico (FR17). Sem fechamento: UPDATE e DELETE recusados.
-- ---------------------------------------------------------------------------

CREATE TRIGGER IF NOT EXISTS rodadas_no_update
BEFORE UPDATE ON rodadas
BEGIN SELECT RAISE(ABORT, 'append-only: rodadas recusa UPDATE'); END;

CREATE TRIGGER IF NOT EXISTS rodadas_no_delete
BEFORE DELETE ON rodadas
BEGIN SELECT RAISE(ABORT, 'append-only: rodadas recusa DELETE'); END;

CREATE TRIGGER IF NOT EXISTS transicoes_no_update
BEFORE UPDATE ON transicoes
BEGIN SELECT RAISE(ABORT, 'append-only: transicoes recusa UPDATE'); END;

CREATE TRIGGER IF NOT EXISTS transicoes_no_delete
BEFORE DELETE ON transicoes
BEGIN SELECT RAISE(ABORT, 'append-only: transicoes recusa DELETE'); END;

-- ---------------------------------------------------------------------------
-- `fila`: o único UPDATE legítimo é o fechamento da leitura (`lida_em`, NULL -> valor);
-- é o que o drain do 070 faz (`fila_outbox.drenar`, `workflow_session_start.py`). Fora
-- disso — outra coluna, ou uma linha já lida — a base recusa.
-- ---------------------------------------------------------------------------

CREATE TRIGGER IF NOT EXISTS fila_no_update
BEFORE UPDATE ON fila
WHEN NOT (
  OLD.lida_em IS NULL
  AND OLD.id IS NEW.id
  AND OLD.sessao_origem IS NEW.sessao_origem
  AND OLD.sessao_destino IS NEW.sessao_destino
  AND OLD.payload IS NEW.payload
  AND OLD.criada_em IS NEW.criada_em
)
BEGIN SELECT RAISE(ABORT, 'append-only: fila so aceita o fechamento da leitura (lida_em)'); END;

CREATE TRIGGER IF NOT EXISTS fila_no_delete
BEFORE DELETE ON fila
BEGIN SELECT RAISE(ABORT, 'append-only: fila recusa DELETE'); END;

-- ---------------------------------------------------------------------------
-- `passos`: o único UPDATE legítimo é o fechamento do passo (`saida_em`, `resumo`,
-- `resultado`, com `saida_em IS NULL`) — exatamente o que o hook Stop faz. Fora disso —
-- uma coluna não liberada, ou um passo já fechado — a base recusa (FR3 do 070 preservado).
-- ---------------------------------------------------------------------------

CREATE TRIGGER IF NOT EXISTS passos_no_update
BEFORE UPDATE ON passos
WHEN NOT (
  OLD.saida_em IS NULL
  AND OLD.id IS NEW.id
  AND OLD.rodada IS NEW.rodada
  AND OLD.passo IS NEW.passo
  AND OLD.sessao IS NEW.sessao
  AND OLD.entrada_em IS NEW.entrada_em
  AND OLD.evidencia_json IS NEW.evidencia_json
)
BEGIN SELECT RAISE(ABORT, 'append-only: passo so aceita o fechamento (saida_em, resumo, resultado)'); END;

CREATE TRIGGER IF NOT EXISTS passos_no_delete
BEFORE DELETE ON passos
BEGIN SELECT RAISE(ABORT, 'append-only: passos recusa DELETE'); END;
