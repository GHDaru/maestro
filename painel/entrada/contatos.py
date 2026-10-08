#!/usr/bin/env python3
"""Ferramenta de cadastro de contatos do WhatsApp (P4 do chamado 068).

O telefone nunca entra no repositório git — fica em dados/entrada.db,
fora do .gitignore. O contato é identificado por c-NNNN.

Uso:
  python contatos.py add --telefone 55... --nome "Mauricio" --empresa "Neogrid" [--db dados/entrada.db]
  python contatos.py list [--db dados/entrada.db]
  python contatos.py rm c-0001 [--db dados/entrada.db]

Stdlib only (sqlite3, argparse).
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import sqlite3
import sys

DEFAULT_DB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dados", "entrada.db")

_SCHEMA = """
CREATE TABLE IF NOT EXISTS contatos (
    contato    TEXT PRIMARY KEY,
    telefone   TEXT,
    nome       TEXT,
    empresa    TEXT,
    ativo      INTEGER NOT NULL DEFAULT 1,
    criado_em  TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS contatos_seq (
    seq INTEGER NOT NULL
);
INSERT INTO contatos_seq (seq) SELECT 0 WHERE NOT EXISTS (SELECT 1 FROM contatos_seq);
"""


def abre(db_path: str) -> sqlite3.Connection:
    """Abre (ou cria) o banco e garante o schema."""
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    db.executescript(_SCHEMA)
    return db


def _proxima_id(db: sqlite3.Connection) -> str:
    """Reserva o próximo c-NNNN de forma atômica."""
    db.execute("UPDATE contatos_seq SET seq = seq + 1")
    seq = db.execute("SELECT seq FROM contatos_seq").fetchone()[0]
    return f"c-{seq:04d}"


def add(db_path: str, telefone: str, nome: str, empresa: str) -> dict:
    """Cadastra um contato. Recusa telefone duplicado ativo."""
    db = abre(db_path)
    try:
        existente = db.execute(
            "SELECT contato FROM contatos WHERE telefone = ? AND ativo = 1", (telefone,)
        ).fetchone()
        if existente:
            raise ValueError(f"Telefone já cadastrado: {existente['contato']}")
        contato = _proxima_id(db)
        agora = dt.datetime.now().astimezone().isoformat()
        db.execute(
            "INSERT INTO contatos (contato, telefone, nome, empresa, ativo, criado_em) VALUES (?, ?, ?, ?, 1, ?)",
            (contato, telefone, nome, empresa, agora),
        )
        db.commit()
        return {"contato": contato, "telefone": telefone, "nome": nome, "empresa": empresa, "ativo": True}
    finally:
        db.close()


def lista(db_path: str) -> list[dict]:
    """Lista contatos ativos."""
    db = abre(db_path)
    try:
        rows = db.execute(
            "SELECT contato, nome, empresa, criado_em FROM contatos WHERE ativo = 1 ORDER BY contato"
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        db.close()


def rm(db_path: str, contato_id: str) -> None:
    """Desativa o contato e apaga o telefone (LGPD art. 18)."""
    db = abre(db_path)
    try:
        row = db.execute("SELECT contato FROM contatos WHERE contato = ?", (contato_id,)).fetchone()
        if not row:
            raise ValueError(f"Contato não encontrado: {contato_id}")
        db.execute(
            "UPDATE contatos SET ativo = 0, telefone = NULL WHERE contato = ?", (contato_id,)
        )
        db.commit()
    finally:
        db.close()


def lookup(db_path: str, telefone: str) -> dict | None:
    """Busca um contato ativo pelo telefone. Retorna None se não encontrado."""
    db = abre(db_path)
    try:
        row = db.execute(
            "SELECT contato, nome, empresa FROM contatos WHERE telefone = ? AND ativo = 1",
            (telefone,),
        ).fetchone()
        return dict(row) if row else None
    finally:
        db.close()


def cli(argv: list[str] | None = None) -> int:
    """Interface de linha de comando."""
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("acao", choices=["add", "list", "rm"])
    ap.add_argument("contato_id", nargs="?", help="ID do contato (c-NNNN) para rm")
    ap.add_argument("--telefone")
    ap.add_argument("--nome")
    ap.add_argument("--empresa")
    ap.add_argument("--db", default=DEFAULT_DB, help="Caminho do banco (default: dados/entrada.db)")
    a = ap.parse_args(argv)

    if a.acao == "add":
        if not a.telefone or not a.nome or not a.empresa:
            print("add requer --telefone, --nome e --empresa", file=sys.stderr)
            return 2
        res = add(a.db, a.telefone, a.nome, a.empresa)
        print(f"ok: {res['contato']} — {res['nome']} ({res['empresa']})")
        return 0

    if a.acao == "list":
        for c in lista(a.db):
            print(f"{c['contato']}  {c['nome']}  {c['empresa']}  {c['criado_em']}")
        return 0

    if a.acao == "rm":
        if not a.contato_id:
            print("rm requer o ID do contato (c-NNNN)", file=sys.stderr)
            return 2
        rm(a.db, a.contato_id)
        print(f"ok: {a.contato_id} desativado")
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(cli())
