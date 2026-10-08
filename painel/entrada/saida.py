#!/usr/bin/env python3
"""Fila de saída com retry e limite de tentativas (P5-AC3, AC4 do chamado 068).

Mensagens saem pelo webhook do n8n. Se o n8n devolver erro (não-200),
a mensagem fica na fila com retry crescente: 1, 5, 15, 60 min.
Após 10 tentativas ou 24 h na fila, a mensagem fica 'falhou' e
a Office recebe aviso (NFR-012).

Stdlib only (sqlite3, datetime, json).
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sqlite3

DEFAULT_DB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dados", "entrada.db")

# Intervalos de retry em minutos (1, 5, 15, 60). Depois do 4º, repete 60.
RETRY_INTERVALS = [1, 5, 15, 60]
MAX_TENTATIVAS = 10
MAX_HORAS = 24

_SCHEMA = """
CREATE TABLE IF NOT EXISTS saida (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    chamado     TEXT,
    contato     TEXT,
    texto       TEXT,
    botoes_json TEXT,
    tentativas  INTEGER NOT NULL DEFAULT 0,
    proxima_em  TEXT NOT NULL,
    criado_em   TEXT NOT NULL,
    estado      TEXT NOT NULL DEFAULT 'pendente',
    ultimo_erro TEXT
);
"""


def abre(db_path: str) -> sqlite3.Connection:
    """Abre (ou cria) o banco e garante o schema."""
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    db.executescript(_SCHEMA)
    return db


def enfileira(
    db_path: str, chamado: str, contato: str, texto: str, botoes: list | None = None,
    agora: dt.datetime | None = None,
) -> int:
    """Adiciona uma mensagem à fila de saída. Retorna o id."""
    if agora is None:
        agora = dt.datetime.now().astimezone()
    db = abre(db_path)
    try:
        ts = agora.isoformat()
        cur = db.execute(
            "INSERT INTO saida (chamado, contato, texto, botoes_json, tentativas, proxima_em, criado_em, estado) "
            "VALUES (?, ?, ?, ?, 0, ?, ?, 'pendente')",
            (chamado, contato, texto, json.dumps(botoes or [], ensure_ascii=False), ts, ts),
        )
        db.commit()
        return cur.lastrowid
    finally:
        db.close()


def pendentes(db_path: str, agora: dt.datetime | None = None) -> list[dict]:
    """Lista mensagens prontas para enviar (estado='pendente' e proxima_em <= agora)."""
    if agora is None:
        agora = dt.datetime.now().astimezone()
    db = abre(db_path)
    try:
        rows = db.execute(
            "SELECT id, chamado, contato, texto, botoes_json, tentativas, criado_em FROM saida "
            "WHERE estado = 'pendente' AND proxima_em <= ? ORDER BY id",
            (agora.isoformat(),),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        db.close()


def conta_pendentes(db_path: str, agora: dt.datetime | None = None) -> int:
    """Conta mensagens pendentes (qualquer proxima_em)."""
    db = abre(db_path)
    try:
        return db.execute("SELECT COUNT(*) FROM saida WHERE estado = 'pendente'").fetchone()[0]
    finally:
        db.close()


def avisa_falhos(db_path: str) -> list[dict]:
    """Lista mensagens falhou para aviso direto à Office (NFR-012).

    Retorna chamado, etapa (ultimo_erro) e tentativas, sem o texto.
    A Assistente chama no ciclo de 30 min até alguém reenviar ou descartar.
    """
    return falhos(db_path)


def falhos(db_path: str) -> list[dict]:
    """Lista mensagens que excederam o limite de tentativas ou tempo."""
    db = abre(db_path)
    try:
        rows = db.execute(
            "SELECT id, chamado, contato, tentativas, criado_em, ultimo_erro FROM saida WHERE estado = 'falhou'"
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        db.close()


def _proximo_retry(tentativas: int, agora: dt.datetime) -> dt.datetime:
    """Calcula o próximo momento de retry baseado no número de tentativas."""
    idx = min(tentativas - 1, len(RETRY_INTERVALS) - 1)
    minutos = RETRY_INTERVALS[idx]
    return agora + dt.timedelta(minutes=minutos)


def _parse_ts(s: str) -> dt.datetime:
    t = dt.datetime.fromisoformat(s)
    return t if t.tzinfo else t.astimezone()


def processa_fila(db_path: str, send_fn, agora: dt.datetime | None = None) -> dict:
    """Tenta enviar todas as mensagens pendentes.

    send_fn(msg) -> int: recebe a mensagem e retorna o status HTTP.
      200 = enviado, qualquer outro = falha.

    Retorna {'enviados': N, 'falhas': N, 'falhou': N}.
    """
    if agora is None:
        agora = dt.datetime.now().astimezone()
    enviados = 0
    retries = 0
    falhou = 0

    msgs = pendentes(db_path, agora=agora)
    db = abre(db_path)
    try:
        for msg in msgs:
            criado = _parse_ts(msg["criado_em"])

            # Verificar limite de 24h
            if (agora - criado).total_seconds() > MAX_HORAS * 3600:
                db.execute(
                    "UPDATE saida SET estado = 'falhou', ultimo_erro = 'excedeu 24h na fila' WHERE id = ?",
                    (msg["id"],),
                )
                falhou += 1
                continue

            # Verificar limite de tentativas
            if msg["tentativas"] >= MAX_TENTATIVAS:
                db.execute(
                    "UPDATE saida SET estado = 'falhou', ultimo_erro = ? WHERE id = ?",
                    (f"excedeu {MAX_TENTATIVAS} tentativas", msg["id"]),
                )
                falhou += 1
                continue

            # Tentar enviar
            status = send_fn(msg)
            if status == 200:
                db.execute("UPDATE saida SET estado = 'enviado' WHERE id = ?", (msg["id"],))
                enviados += 1
            else:
                nova_tentativa = msg["tentativas"] + 1
                if nova_tentativa >= MAX_TENTATIVAS or (agora - criado).total_seconds() > MAX_HORAS * 3600:
                    db.execute(
                        "UPDATE saida SET tentativas = ?, estado = 'falhou', ultimo_erro = ? WHERE id = ?",
                        (nova_tentativa, f"status {status}, tentativa {nova_tentativa}", msg["id"]),
                    )
                    falhou += 1
                else:
                    proxima = _proximo_retry(nova_tentativa, agora)
                    db.execute(
                        "UPDATE saida SET tentativas = ?, proxima_em = ?, ultimo_erro = ? WHERE id = ?",
                        (nova_tentativa, proxima.isoformat(), f"status {status}", msg["id"]),
                    )
                    retries += 1
        db.commit()
    finally:
        db.close()

    return {"enviados": enviados, "falhas": falhou, "falhou": falhou, "retries": retries}
