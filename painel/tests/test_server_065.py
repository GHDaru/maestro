"""T4 (red) — Server endpoints para spec 065: /api/board, /api/arvore, /api/roadmap.

FRs: FR1, FR2, FR5, FR8, FR9, FR11.

- /api/board retorna exceções + sessões (FR1, FR2)
- /api/arvore?id=R001 retorna árvore materializada (FR8, FR9)
- /api/roadmap retorna raias por ciclo (FR11)
"""
from __future__ import annotations

import json
import os
import sqlite3
import sys
import tempfile
from urllib.request import urlopen
from urllib.parse import urlencode

import pytest

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, ".."))
import ingest
import server

SCHEMA_065_SQL = os.path.join(AQUI, "..", "schema_065.sql")


def _cfg_minima(tmpdir):
    return {
        "projeto": "teste",
        "raiz": str(tmpdir),
        "equipes": {},
        "repos": [],
        "specs": [],
        "documentos": {},
    }


class TestServerBoard:
    """T4: /api/board retorna exceções e sessões."""

    def test_board_retorna_excecoes(self, tmp_path):
        """/api/board tem chave 'excecoes' com 3 tipos."""
        db_path = str(tmp_path / "painel.db")
        cfg = _cfg_minima(tmp_path)
        ingest.ingere(cfg, db_path)

        db = server.conecta(db_path)
        result = server.v_board(db)
        db.close()

        assert "excecoes" in result or "board" in result, (
            "/api/board deve retornar exceções do board"
        )

    def test_board_retorna_sessoes(self, tmp_path):
        """/api/board tem chave com lista de sessões."""
        db_path = str(tmp_path / "painel.db")
        cfg = _cfg_minima(tmp_path)
        cfg["equipes"] = {"W09": {"papel": "Worker09"}}
        ingest.ingere(cfg, db_path)

        db = server.conecta(db_path)
        result = server.v_board(db)
        db.close()

        # Deve ter alguma chave com sessões
        has_sessoes = any(
            "sess" in k.lower() or "linha" in k.lower()
            for k in result
        )
        assert has_sessoes, "/api/board deve retornar sessões"


class TestServerArvore:
    """T4: /api/arvore?id=R001 retorna árvore materializada."""

    def test_arvore_retorna_nos(self, tmp_path):
        """v_arvore(db, '064') retorna nós da árvore."""
        db_path = str(tmp_path / "painel.db")
        cfg = _cfg_minima(tmp_path)
        ingest.ingere(cfg, db_path)

        # Inserir nó manualmente para testar a query
        conn = sqlite3.connect(db_path)
        conn.execute(
            "INSERT INTO arvore_rodada (rodada, tipo, id_no, pai, label, status, evidencia_ok) "
            "VALUES ('064', 'spec', 'FR1', NULL, 'FR1', 'ok', 1)"
        )
        conn.commit()
        conn.close()

        db = server.conecta(db_path)
        # v_arvore deve existir e retornar nós
        assert hasattr(server, "v_arvore"), "server.py deve ter função v_arvore"
        result = server.v_arvore(db, "064")
        db.close()

        assert isinstance(result, (list, dict))
        # Se for dict, deve ter chave 'nos' ou similar
        if isinstance(result, dict):
            assert "nos" in result or "arvore" in result or len(result) > 0
        else:
            assert len(result) > 0


class TestServerRoadmap065:
    """T4: /api/roadmap retorna raias por ciclo (FR11)."""

    def test_roadmap_retorna_raias(self, tmp_path):
        """v_roadmap retorna raias (atual, próximo, depois)."""
        db_path = str(tmp_path / "painel.db")
        cfg = _cfg_minima(tmp_path)
        ingest.ingere(cfg, db_path)

        db = server.conecta(db_path)
        result = server.v_roadmap(db)
        db.close()

        # v_roadmap já existe — deve retornar dados
        assert result is not None
