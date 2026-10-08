"""Fila de saída e envio assinado ao n8n (FR-007, P2).

A fila vive em dados/entrada.db (tabela `saida`). O envio é assinado
com HMAC-SHA256 (NFR-004). O retry segue 1/5/15/60 min (P5-AC3).
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import sqlite3
import time
import urllib.request
import urllib.error

# Tabela da fila de saída.
_SCHEMA = """
CREATE TABLE IF NOT EXISTS saida (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chamado TEXT NOT NULL,
    contato TEXT NOT NULL,
    texto TEXT NOT NULL,
    etapa TEXT NOT NULL,
    criado_em TEXT NOT NULL,
    tentativas INTEGER DEFAULT 0,
    proxima_tentativa TEXT,
    status TEXT DEFAULT 'pendente',
    ultimo_erro TEXT
);
CREATE INDEX IF NOT EXISTS idx_saida_status ON saida(status);
"""

# Espera crescente entre tentativas (segundos): 1, 5, 15, 60 min.
ESPERAS = [60, 300, 900, 3600]

# Limite de tentativas (NFR-012).
MAX_TENTATIVAS = 10
MAX_IDADE_SEGUNDOS = 24 * 3600


def _db(dados_dir: str) -> sqlite3.Connection:
    conn = sqlite3.connect(os.path.join(dados_dir, "entrada.db"))
    conn.executescript(_SCHEMA)
    return conn


def enfileirar(dados_dir: str, chamado: str, contato: str, texto: str, etapa: str) -> int:
    """Enfileira uma mensagem de saída. Devolve o id."""
    conn = _db(dados_dir)
    try:
        cur = conn.execute(
            "INSERT INTO saida (chamado, contato, texto, etapa, criado_em, proxima_tentativa, status) "
            "VALUES (?, ?, ?, ?, ?, ?, 'pendente')",
            (chamado, contato, texto, etapa,
             _agora_iso(), _agora_iso()),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def pendentes(dados_dir: str) -> list[dict]:
    """Devolve mensagens pendentes prontas para tentar agora."""
    conn = _db(dados_dir)
    try:
        agora = _agora_iso()
        rows = conn.execute(
            "SELECT * FROM saida WHERE status = 'pendente' AND (proxima_tentativa IS NULL OR proxima_tentativa <= ?) "
            "ORDER BY id",
            (agora,),
        ).fetchall()
        cols = [d[0] for d in conn.execute("SELECT * FROM saida LIMIT 0").description]
        return [dict(zip(cols, r)) for r in rows]
    finally:
        conn.close()


def enviar(dados_dir: str, msg: dict, webhook_url: str, segredo: str) -> bool:
    """Envia uma mensagem ao webhook do n8n, assinada. True se 200."""
    corpo = json.dumps({
        "chamado": msg["chamado"],
        "contato": msg["contato"],
        "texto": msg["texto"],
    }).encode()
    assinatura = hmac.new(segredo.encode(), corpo, hashlib.sha256).hexdigest()
    headers = {
        "Content-Type": "application/json",
        "X-Maestro-Assinatura": f"sha256={assinatura}",
        "X-Maestro-Horario": _agora_iso(),
        "X-Maestro-Evento-Id": f"saida-{msg['id']}",
    }
    try:
        req = urllib.request.Request(webhook_url, data=corpo, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=10) as resp:
            ok = resp.status == 200
    except (urllib.error.URLError, OSError) as e:
        ok = False
        e_str = str(e)
    else:
        e_str = ""
    _atualizar(dados_dir, msg["id"], ok, e_str)
    return ok


def _atualizar(dados_dir: str, msg_id: int, ok: bool, erro: str) -> None:
    conn = _db(dados_dir)
    try:
        row = conn.execute("SELECT tentativas FROM saida WHERE id = ?", (msg_id,)).fetchone()
        tentativas = (row[0] if row else 0) + 1
        if ok:
            conn.execute("UPDATE saida SET status = 'enviado', tentativas = ? WHERE id = ?",
                         (tentativas, msg_id))
        else:
            idade = _idade_segundos(dados_dir, msg_id)
            if tentativas >= MAX_TENTATIVAS or idade >= MAX_IDADE_SEGUNDOS:
                conn.execute(
                    "UPDATE saida SET status = 'falhou', tentativas = ?, ultimo_erro = ? WHERE id = ?",
                    (tentativas, erro, msg_id),
                )
            else:
                espera = ESPERAS[min(tentativas - 1, len(ESPERAS) - 1)]
                conn.execute(
                    "UPDATE saida SET tentativas = ?, proxima_tentativa = ?, ultimo_erro = ? WHERE id = ?",
                    (tentativas, _futuro_iso(espera), erro, msg_id),
                )
        conn.commit()
    finally:
        conn.close()


def _agora_iso() -> str:
    import datetime as dt
    return dt.datetime.now(dt.timezone.utc).isoformat()


def _futuro_iso(segundos: int) -> str:
    import datetime as dt
    return (dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=segundos)).isoformat()


def _idade_segundos(dados_dir: str, msg_id: int) -> float:
    import datetime as dt
    conn = _db(dados_dir)
    try:
        row = conn.execute("SELECT criado_em FROM saida WHERE id = ?", (msg_id,)).fetchone()
        if not row:
            return 0
        criado = dt.datetime.fromisoformat(row[0])
        return (dt.datetime.now(dt.timezone.utc) - criado).total_seconds()
    finally:
        conn.close()
