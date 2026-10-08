#!/usr/bin/env python3
"""Idempotência por evento_id na porta de entrada (P5-AC2 do chamado 068).

O n8n pode reenviar o mesmo evento (retry). A tabela eventos
guarda o evento_id e a resposta JSON por 7 dias (NFR-004).
Uma repetição retorna a mesma resposta sem reexecutar.

Stdlib only (sqlite3, datetime, json).
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sqlite3

DEFAULT_DB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dados", "entrada.db")

_SCHEMA = """
CREATE TABLE IF NOT EXISTS eventos (
    evento_id     TEXT PRIMARY KEY,
    recebido_em   TEXT NOT NULL,
    resposta_json TEXT NOT NULL
);
"""


def abre(db_path: str) -> sqlite3.Connection:
    """Abre (ou cria) o banco e garante o schema."""
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    db.executescript(_SCHEMA)
    return db


def consulta(db_path: str, evento_id: str) -> dict | None:
    """Retorna a resposta guardada para evento_id, ou None se não existe."""
    db = abre(db_path)
    try:
        row = db.execute(
            "SELECT resposta_json FROM eventos WHERE evento_id = ?", (evento_id,)
        ).fetchone()
        if row:
            return json.loads(row["resposta_json"])
        return None
    finally:
        db.close()


def registra(db_path: str, evento_id: str, resposta: dict) -> None:
    """Guarda a resposta para evento_id."""
    db = abre(db_path)
    try:
        agora = dt.datetime.now().astimezone().isoformat()
        db.execute(
            "INSERT OR REPLACE INTO eventos (evento_id, recebido_em, resposta_json) VALUES (?, ?, ?)",
            (evento_id, agora, json.dumps(resposta, ensure_ascii=False)),
        )
        db.commit()
    finally:
        db.close()


def processa(db_path: str, evento_id: str, fn) -> dict:
    """Idempotência: se evento_id já existe, retorna a resposta guardada;
    senão chama fn(), guarda e retorna o resultado.
    """
    existente = consulta(db_path, evento_id)
    if existente is not None:
        return existente
    resposta = fn()
    registra(db_path, evento_id, resposta)
    return resposta


def limpa(db_path: str, dias: int = 7) -> int:
    """Remove eventos com mais de N dias. Retorna quantos removeu."""
    db = abre(db_path)
    try:
        limite = (dt.datetime.now().astimezone() - dt.timedelta(days=dias)).isoformat()
        cur = db.execute("DELETE FROM eventos WHERE recebido_em < ?", (limite,))
        db.commit()
        return cur.rowcount
    finally:
        db.close()
