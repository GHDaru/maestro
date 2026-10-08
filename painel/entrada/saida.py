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

-- Log de envio: SÓ metadados (NFR-011, SC-007). Sem contato (telefone) e sem texto.
CREATE TABLE IF NOT EXISTS log_envio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    evento_id TEXT NOT NULL,
    chamado TEXT NOT NULL,
    etapa TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    status TEXT NOT NULL,
    tentativas INTEGER
);

-- Alertas à Office quando mensagem falha definitivamente (NFR-012).
CREATE TABLE IF NOT EXISTS alertas_office (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    evento_id TEXT NOT NULL,
    chamado TEXT NOT NULL,
    motivo TEXT,
    timestamp TEXT NOT NULL,
    lido INTEGER DEFAULT 0
);
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


def _log(dados_dir: str, evento_id: str, chamado: str, etapa: str, status: str, tentativas: int) -> None:
    """Registra SÓ metadados no log (NFR-011, SC-007).

    Sem telefone (contato) e sem texto da mensagem.
    """
    conn = _db(dados_dir)
    try:
        conn.execute(
            "INSERT INTO log_envio (evento_id, chamado, etapa, timestamp, status, tentativas) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (evento_id, chamado, etapa, _agora_iso(), status, tentativas),
        )
        conn.commit()
    finally:
        conn.close()


def _avisar_falha(dados_dir: str, evento_id: str, chamado: str, motivo: str) -> None:
    """Registra alerta à Office quando mensagem falha definitivamente (NFR-012)."""
    conn = _db(dados_dir)
    try:
        conn.execute(
            "INSERT INTO alertas_office (evento_id, chamado, motivo, timestamp) VALUES (?, ?, ?, ?)",
            (evento_id, chamado, motivo, _agora_iso()),
        )
        conn.commit()
    finally:
        conn.close()


def alertas_nao_lidos(dados_dir: str) -> list[dict]:
    """Devolve alertas à Office ainda não lidos."""
    conn = _db(dados_dir)
    try:
        rows = conn.execute("SELECT * FROM alertas_office WHERE lido = 0 ORDER BY id").fetchall()
        cols = [d[0] for d in conn.execute("SELECT * FROM alertas_office LIMIT 0").description]
        return [dict(zip(cols, r)) for r in rows]
    finally:
        conn.close()


def log_envio_todos(dados_dir: str) -> list[dict]:
    """Devolve todos os registros de log de envio (só metadados)."""
    conn = _db(dados_dir)
    try:
        rows = conn.execute("SELECT * FROM log_envio ORDER BY id").fetchall()
        cols = [d[0] for d in conn.execute("SELECT * FROM log_envio LIMIT 0").description]
        return [dict(zip(cols, r)) for r in rows]
    finally:
        conn.close()


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
    _log(dados_dir, f"saida-{msg['id']}", msg["chamado"], msg["etapa"],
         "enviado" if ok else "falhou", msg.get("tentativas", 0) + 1)
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
                conn.commit()
                conn.close()
                _avisar_falha(dados_dir, f"saida-{msg_id}", _chamado_da_msg(dados_dir, msg_id), erro)
                return
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


def _chamado_da_msg(dados_dir: str, msg_id: int) -> str:
    conn = _db(dados_dir)
    try:
        row = conn.execute("SELECT chamado FROM saida WHERE id = ?", (msg_id,)).fetchone()
        return row[0] if row else ""
    finally:
        conn.close()
