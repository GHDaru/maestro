#!/usr/bin/env python3
"""T3: Hook Stop — cobra resumo e saída do passo, recusa sem evidência.

Lê MAESTRO_RODADA e MAESTRO_PASSO. Verifica se o passo tem resumo e evidência.
Se a transição exige evidência (transicoes.evidencia_exigida = 1) e o passo
não tem resumo ou evidencia_json, escreve no stderr e retorna exit code 2
(Claude Code mostra stderr de hooks Stop ao usuário).

O hook NÃO bloqueia a sessão (exit 0 sempre que há resumo). O objetivo é
cobrar, não impedir — o resumo é escrito pelo próprio Claude na conversa.

Env vars:
  CLAUDE_SESSION_ID  — id da sessão
  CLAUDE_PROJECT_DIR — raiz do projeto
  MAESTRO_RODADA     — id da rodada ativa
  MAESTRO_PASSO      — passo atual
"""
from __future__ import annotations

import datetime as dt
import os
import sqlite3
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
DB_DEFAULT = os.path.join(AQUI, "..", "..", "painel", "painel.db")


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def _db_path() -> str:
    return os.environ.get("MAESTRO_DB", DB_DEFAULT)


SCHEMA_SQL = os.path.join(AQUI, "..", "..", "painel", "schema_workflow.sql")


def _ensure_schema(conn: sqlite3.Connection) -> None:
    """Cria tabelas workflow se não existem."""
    tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    if "rodadas" not in tables and os.path.exists(SCHEMA_SQL):
        with open(SCHEMA_SQL, encoding="utf-8") as f:
            conn.executescript(f.read())


def main() -> int:
    db_path = _db_path()
    rodada = os.environ.get("MAESTRO_RODADA", "")
    passo = os.environ.get("MAESTRO_PASSO", "")
    sessao = os.environ.get("CLAUDE_SESSION_ID", "unknown")

    if not os.path.exists(db_path):
        return 0
    if not rodada or not passo:
        return 0

    conn = sqlite3.connect(db_path)
    _ensure_schema(conn)

    # Busca o passo atual
    row = conn.execute(
        """SELECT id, resumo, evidencia_json, saida_em
           FROM passos
           WHERE rodada = ? AND passo = ? AND sessao = ?
           ORDER BY id DESC LIMIT 1""",
        (rodada, passo, sessao),
    ).fetchone()

    if row is None:
        # Passo sem entrada registrada — nada a cobrar
        conn.close()
        return 0

    passo_id, resumo, evidencia, saida_em = row

    if saida_em is not None:
        # Já fechado — nada a fazer
        conn.close()
        return 0

    # Verifica se a transição exige evidência
    exige = conn.execute(
        "SELECT evidencia_exigida FROM transicoes WHERE passo = ? LIMIT 1",
        (passo,),
    ).fetchone()
    evidencia_exigida = exige[0] if exige else 1  # default: exige

    # Registra saída do passo
    now = _now()
    resultado = "ok" if resumo else "skip"
    conn.execute(
        """UPDATE passos SET saida_em = ?, resultado = ?
           WHERE id = ?""",
        (now, resultado, passo_id),
    )
    conn.commit()

    # Se exige evidência e não tem resumo, cobra
    if evidencia_exigida and not resumo:
        print(
            f"⚠️  Passo {passo} da rodada {rodada} fechado sem resumo.\n"
            f"    Para registrar evidência: UPDATE passos SET resumo = '...', "
            f"evidencia_json = '...' WHERE id = {passo_id};",
            file=sys.stderr,
        )

    # Enfileira mensagem na fila para o painel
    conn.execute(
        """INSERT INTO fila (sessao_origem, sessao_destino, payload, criada_em)
           VALUES (?, NULL, ?, ?)""",
        (sessao, f'{{"rodada": "{rodada}", "passo": "{passo}", "resultado": "{resultado}"}}', now),
    )
    conn.commit()

    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
