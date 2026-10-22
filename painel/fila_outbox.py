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


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


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
                msgs.append(FilaMensagem(
                    id=r_id,
                    sessao_origem=r_origem,
                    sessao_destino=r_dest,
                    payload=json.loads(r_payload),
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
