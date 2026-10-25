#!/usr/bin/env python3
"""T2: Hook SessionStart — mostra passos abertos e escreve entrada no passo atual.

Lê a rodada ativa e os passos abertos do SQLite. Se há passos abertos,
exibe-os no stdout (Claude Code mostra stdout de hooks SessionStart ao usuário).
Registra a entrada no passo atual (entrada_em = now) se o passo ainda não tem entrada.

Env vars esperadas:
  CLAUDE_SESSION_ID  — id da sessão atual
  CLAUDE_PROJECT_DIR — raiz do projeto (onde está painel/)
  MAESTRO_RODADA     — id da rodada ativa (ex: "001")
  MAESTRO_PASSO      — passo atual (ex: "T1")

Uso em .claude/settings.json:
  "SessionStart": [{ "hooks": [{ "type": "command",
    "command": "python \"$CLAUDE_PROJECT_DIR/painel/hooks/workflow_session_start.py\"" }] }]
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sqlite3
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
DB_DEFAULT = os.path.join(AQUI, "..", "..", "painel", "painel.db")
SCHEMA_SQL = os.path.join(AQUI, "..", "..", "painel", "schema_workflow.sql")

# FR17 (a dívida 5 do 070 vira requisito): append-only imposto pela base. As MESMAS
# sentenças vivem em `painel/schema_workflow.sql`; duplicá-las nesta cópia é o preço que
# D-072-2 declara (a dívida 2 piora — as cópias precisam ficar em sincronia). O SQLite
# aceita um só evento por gatilho, então há dois por tabela.
TRIGGERS_SQL = """
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
"""


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def _db_path() -> str:
    return os.environ.get("MAESTRO_DB", DB_DEFAULT)


def _ensure_schema(conn: sqlite3.Connection) -> None:
    """Cria tabelas se não existem e aplica os gatilhos append-only (FR17).

    Os gatilhos são aplicados SEMPRE (não só no banco novo): um banco vivo, que já tem as
    tabelas, também precisa ganhar o append-only mecânico.
    """
    tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    if "rodadas" not in tables and os.path.exists(SCHEMA_SQL):
        with open(SCHEMA_SQL, encoding="utf-8") as f:
            conn.executescript(f.read())
    conn.executescript(TRIGGERS_SQL)


def main() -> int:
    db_path = _db_path()
    rodada = os.environ.get("MAESTRO_RODADA", "")
    passo = os.environ.get("MAESTRO_PASSO", "")
    sessao = os.environ.get("CLAUDE_SESSION_ID", "unknown")

    if not os.path.exists(db_path):
        # Sem DB ainda — silencioso
        return 0

    conn = sqlite3.connect(db_path)
    _ensure_schema(conn)

    # 1. Mostra passos abertos da rodada
    abertos = conn.execute(
        """SELECT passo, sessao, entrada_em
           FROM passos
           WHERE rodada = ? AND saida_em IS NULL
           ORDER BY entrada_em""",
        (rodada,),
    ).fetchall()

    if abertos:
        print(f"📋 Rodada {rodada} — passos abertos:")
        for p_passo, p_sessao, p_entrada in abertos:
            print(f"  • {p_passo} (sessão {p_sessao}, entrou {p_entrada})")
        print()

    # 2. Registra entrada no passo atual
    if rodada and passo:
        existe = conn.execute(
            "SELECT 1 FROM passos WHERE rodada = ? AND passo = ? AND sessao = ? AND entrada_em IS NOT NULL",
            (rodada, passo, sessao),
        ).fetchone()
        if not existe:
            conn.execute(
                """INSERT INTO passos (rodada, passo, sessao, entrada_em)
                   VALUES (?, ?, ?, ?)""",
                (rodada, passo, sessao, _now()),
            )
            conn.commit()

    # 3. Drena fila: mensagens pendentes para esta sessão
    pendentes = conn.execute(
        """SELECT id, sessao_origem, payload
           FROM fila
           WHERE (sessao_destino = ? OR sessao_destino IS NULL)
             AND lida_em IS NULL
           ORDER BY criada_em""",
        (sessao,),
    ).fetchall()
    if pendentes:
        print("📬 Mensagens na fila:")
        for f_id, f_origem, f_payload in pendentes:
            print(f"  • de {f_origem}: {f_payload}")
            conn.execute("UPDATE fila SET lida_em = ? WHERE id = ?", (_now(), f_id))
        conn.commit()
        print()

    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
