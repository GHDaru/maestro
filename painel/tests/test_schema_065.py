"""T1 (red) — Schema 065: tabelas derivadas arvore_rodada, status_workers, excecoes_board.

FRs: FR8, FR12 (arvore_rodada), FR2, FR13 (status_workers), FR1 (excecoes_board).

DoD: sqlite3 painel.db ".tables" → contém arvore_rodada, status_workers, excecoes_board.
     Todas em modo WAL (herdado do schema_workflow.sql).
"""
from __future__ import annotations

import os
import sqlite3
import tempfile

import pytest

AQUI = os.path.dirname(os.path.abspath(__file__))
SCHEMA_065_SQL = os.path.join(AQUI, "..", "schema_065.sql")


class TestSchema065:
    """T1: Schema 065 com tabelas derivadas em modo WAL."""

    def test_schema_cria_arvore_rodada(self):
        """Schema cria tabela arvore_rodada."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        try:
            conn = sqlite3.connect(db_path)
            with open(SCHEMA_065_SQL, encoding="utf-8") as sf:
                conn.executescript(sf.read())
            tables = {
                row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            }
            conn.close()
            assert "arvore_rodada" in tables
        finally:
            os.unlink(db_path)

    def test_arvore_rodada_colunas(self):
        """arvore_rodada: rodada, tipo, id_no, pai, label, status, referencia, hash, evidencia_ok."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        try:
            conn = sqlite3.connect(db_path)
            with open(SCHEMA_065_SQL, encoding="utf-8") as sf:
                conn.executescript(sf.read())
            cols = {row[1] for row in conn.execute("PRAGMA table_info(arvore_rodada)")}
            conn.close()
            expected = {
                "rodada", "tipo", "id_no", "pai", "label",
                "status", "referencia", "hash", "evidencia_ok",
            }
            assert expected <= cols
        finally:
            os.unlink(db_path)

    def test_arvore_rodada_pk_composta(self):
        """PK: (rodada, tipo, id_no) — não pode haver duplicata."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        try:
            conn = sqlite3.connect(db_path)
            with open(SCHEMA_065_SQL, encoding="utf-8") as sf:
                conn.executescript(sf.read())
            conn.execute(
                "INSERT INTO arvore_rodada (rodada, tipo, id_no, pai, label, status, evidencia_ok) "
                "VALUES ('001', 'spec', 'FR1', NULL, 'FR1', 'ok', 1)"
            )
            conn.commit()
            with pytest.raises(sqlite3.IntegrityError):
                conn.execute(
                    "INSERT INTO arvore_rodada (rodada, tipo, id_no, pai, label, status, evidencia_ok) "
                    "VALUES ('001', 'spec', 'FR1', NULL, 'FR1', 'ok', 1)"
                )
            conn.close()
        finally:
            os.unlink(db_path)

    def test_schema_cria_status_workers(self):
        """Schema cria tabela status_workers."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        try:
            conn = sqlite3.connect(db_path)
            with open(SCHEMA_065_SQL, encoding="utf-8") as sf:
                conn.executescript(sf.read())
            tables = {
                row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            }
            conn.close()
            assert "status_workers" in tables
        finally:
            os.unlink(db_path)

    def test_status_workers_colunas(self):
        """status_workers: sessao, estado, peca, passo, esperando, ultima_atividade, sem_tarefa_ciclos."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        try:
            conn = sqlite3.connect(db_path)
            with open(SCHEMA_065_SQL, encoding="utf-8") as sf:
                conn.executescript(sf.read())
            cols = {row[1] for row in conn.execute("PRAGMA table_info(status_workers)")}
            conn.close()
            expected = {
                "sessao", "estado", "peca", "passo", "esperando",
                "ultima_atividade", "sem_tarefa_ciclos",
            }
            assert expected <= cols
        finally:
            os.unlink(db_path)

    def test_schema_cria_excecoes_board(self):
        """Schema cria tabela excecoes_board."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        try:
            conn = sqlite3.connect(db_path)
            with open(SCHEMA_065_SQL, encoding="utf-8") as sf:
                conn.executescript(sf.read())
            tables = {
                row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            }
            conn.close()
            assert "excecoes_board" in tables
        finally:
            os.unlink(db_path)

    def test_excecoes_board_colunas(self):
        """excecoes_board: tipo, contador, detalhe_json."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        try:
            conn = sqlite3.connect(db_path)
            with open(SCHEMA_065_SQL, encoding="utf-8") as sf:
                conn.executescript(sf.read())
            cols = {row[1] for row in conn.execute("PRAGMA table_info(excecoes_board)")}
            conn.close()
            expected = {"tipo", "contador", "detalhe_json"}
            assert expected <= cols
        finally:
            os.unlink(db_path)

    def test_schema_ativa_wal(self):
        """Schema 065 ativa modo WAL."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        try:
            conn = sqlite3.connect(db_path)
            with open(SCHEMA_065_SQL, encoding="utf-8") as sf:
                conn.executescript(sf.read())
            mode = conn.execute("PRAGMA journal_mode").fetchone()[0]
            conn.close()
            assert mode == "wal"
        finally:
            os.unlink(db_path)

    def test_indice_arvore_rodada_pai(self):
        """Índice idx_arvore_rodada_pai existe para query por pai."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        try:
            conn = sqlite3.connect(db_path)
            with open(SCHEMA_065_SQL, encoding="utf-8") as sf:
                conn.executescript(sf.read())
            indexes = {
                row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='index'")
            }
            conn.close()
            assert "idx_arvore_rodada_pai" in indexes
        finally:
            os.unlink(db_path)

    def test_indice_status_workers_estado(self):
        """Índice idx_status_workers_estado existe para query por estado."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        try:
            conn = sqlite3.connect(db_path)
            with open(SCHEMA_065_SQL, encoding="utf-8") as sf:
                conn.executescript(sf.read())
            indexes = {
                row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='index'")
            }
            conn.close()
            assert "idx_status_workers_estado" in indexes
        finally:
            os.unlink(db_path)
