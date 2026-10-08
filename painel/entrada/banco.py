"""Criação idempotente do banco de entrada (chamado 068, T0-03).

Stdlib only: sqlite3. As tabelas vivem em dados/entrada.db (fora do git).
CREATE TABLE IF NOT EXISTS — pode rodar quantas vezes quiser.

Esquema:

    contatos       contato (c-NNNN), telefone, nome, empresa, ativo, criado_em
    conversas      contato, estado, dados_json, atualizado_em
    eventos        evento_id, recebido_em, resposta_json  (idempotência, 7 dias)
    notificacoes   chamado, etapa, enviado_em
    saida          id, chamado, contato, texto, botoes_json, tentativas, proxima_em, estado
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

_SCHEMA = """
CREATE TABLE IF NOT EXISTS contatos (
    contato    TEXT PRIMARY KEY,
    telefone   TEXT NOT NULL,
    nome       TEXT NOT NULL DEFAULT '',
    empresa    TEXT NOT NULL DEFAULT '',
    ativo      INTEGER NOT NULL DEFAULT 1,
    criado_em  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);

CREATE TABLE IF NOT EXISTS conversas (
    contato      TEXT PRIMARY KEY REFERENCES contatos(contato),
    estado       TEXT NOT NULL DEFAULT 'inicio',
    dados_json   TEXT NOT NULL DEFAULT '{}',
    atualizado_em TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);

CREATE TABLE IF NOT EXISTS eventos (
    evento_id    TEXT PRIMARY KEY,
    recebido_em  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    resposta_json TEXT NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS notificacoes (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    chamado     TEXT NOT NULL,
    etapa       TEXT NOT NULL,
    enviado_em  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    UNIQUE(chamado, etapa)
);

CREATE TABLE IF NOT EXISTS saida (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    chamado     TEXT,
    contato     TEXT,
    texto       TEXT NOT NULL,
    botoes_json TEXT NOT NULL DEFAULT '[]',
    tentativas  INTEGER NOT NULL DEFAULT 0,
    proxima_em  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    estado      TEXT NOT NULL DEFAULT 'pendente'
);

CREATE INDEX IF NOT EXISTS idx_saida_pendente ON saida(estado, proxima_em);
CREATE INDEX IF NOT EXISTS idx_eventos_recebido ON eventos(recebido_em);
"""


def caminho_db() -> Path:
    """Devolve o caminho de dados/entrada.db relativo à raiz do painel."""
    raiz_painel = Path(__file__).resolve().parent.parent  # painel/
    return raiz_painel.parent / "dados" / "entrada.db"


def inicializar(db_path: Path | None = None) -> Path:
    """Cria todas as tabelas (idempotente) e devolve o caminho do banco."""
    if db_path is None:
        db_path = caminho_db()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(str(db_path)) as conn:
        conn.executescript(_SCHEMA)
        conn.commit()
    return db_path


def conectar(db_path: Path | None = None) -> sqlite3.Connection:
    """Abre uma conexão com o banco, criando as tabelas se necessário."""
    if db_path is None:
        db_path = caminho_db()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.executescript(_SCHEMA)
    conn.commit()
    return conn
