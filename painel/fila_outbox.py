#!/usr/bin/env python3
"""T5: Fila outbox em SQLite — leitura e escrita da tabela `fila`.

Os hooks escrevem na fila (workflow_stop.py). O painel lê e marca como lida.
Esta módulo centraliza as operações para evitar SQL espalhado.

Uso:
  from fila_outbox import FilaOutbox
  fila = FilaOutbox("painel.db")
  fila.enfileirar(origem="sessao-w09", payload={"passo": "T1", "ok": True})
  msgs = fila.drenar(destino="sessao-painel")  # lista de FilaMensagem
"""
from __future__ import annotations

import dataclasses
import datetime as dt
import json
import os
import sqlite3

AQUI = os.path.dirname(os.path.abspath(__file__))
DB_DEFAULT = os.path.join(AQUI, "painel.db")
SCHEMA_SQL = os.path.join(AQUI, "schema_workflow.sql")

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


def _ensure_schema(conn: sqlite3.Connection) -> None:
    """Cria tabelas se não existem e aplica os gatilhos append-only (FR17).

    Terceira cópia da função (as outras duas vivem em `painel/hooks/`): a dívida 2 do 070
    piora, como D-072-2 declara — as cópias precisam ficar em sincronia. Os gatilhos são
    aplicados SEMPRE, para um banco vivo ganhar o append-only mecânico.
    """
    tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    if "rodadas" not in tables and os.path.exists(SCHEMA_SQL):
        with open(SCHEMA_SQL, encoding="utf-8") as f:
            conn.executescript(f.read())
    conn.executescript(TRIGGERS_SQL)


@dataclasses.dataclass
class FilaMensagem:
    id: int
    sessao_origem: str
    sessao_destino: str | None
    payload: dict
    criada_em: str
    lida_em: str | None


class FilaOutbox:
    """Fila outbox em SQLite. Append-only, leitura marca como lida."""

    def __init__(self, db_path: str | None = None):
        self.db_path = db_path or DB_DEFAULT

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA journal_mode = WAL")
        _ensure_schema(conn)  # FR17: garante tabelas e os gatilhos append-only
        return conn

    def enfileirar(
        self,
        origem: str,
        payload: dict,
        destino: str | None = None,
    ) -> int:
        """Escreve uma mensagem na fila. Retorna o id."""
        conn = self._connect()
        try:
            cur = conn.execute(
                """INSERT INTO fila (sessao_origem, sessao_destino, payload, criada_em)
                   VALUES (?, ?, ?, ?)""",
                (origem, destino, json.dumps(payload, ensure_ascii=False), _now()),
            )
            conn.commit()
            return cur.lastrowid
        finally:
            conn.close()

    def drenar(self, destino: str | None = None) -> list[FilaMensagem]:
        """Lê e marca como lidas todas as mensagens pendentes para `destino`.

        Se destino=None, lê mensagens broadcast (sessao_destino IS NULL).
        """
        conn = self._connect()
        try:
            rows = conn.execute(
                """SELECT id, sessao_origem, sessao_destino, payload, criada_em, lida_em
                   FROM fila
                   WHERE lida_em IS NULL
                     AND (? IS NULL AND sessao_destino IS NULL
                          OR sessao_destino = ?)
                   ORDER BY criada_em""",
                (destino, destino),
            ).fetchall()
            now = _now()
            msgs = []
            for r_id, r_origem, r_dest, r_payload, r_criada, r_lida in rows:
                conn.execute("UPDATE fila SET lida_em = ? WHERE id = ?", (now, r_id))
                try:
                    payload = json.loads(r_payload)
                except ValueError:
                    # Uma linha inválida é marcada como lida e devolvida com o erro, nunca
                    # deixada pendente: senão todo drenar() seguinte falharia na mesma linha
                    # (passagem de segurança do ciclo 070, achado 2).
                    payload = {"_erro": "payload não é JSON", "bruto": str(r_payload)[:200]}
                msgs.append(FilaMensagem(
                    id=r_id,
                    sessao_origem=r_origem,
                    sessao_destino=r_dest,
                    payload=payload,
                    criada_em=r_criada,
                    lida_em=now,
                ))
            conn.commit()
            return msgs
        finally:
            conn.close()

    def pendentes(self) -> int:
        """Conta mensagens não lidas."""
        conn = self._connect()
        try:
            return conn.execute(
                "SELECT count(*) FROM fila WHERE lida_em IS NULL"
            ).fetchone()[0]
        finally:
            conn.close()
