"""T1 (red) — Schema SQLite: tabelas rodadas, passos, transicoes, fila em modo WAL.

DoD: sqlite3 painel.db ".tables" → contém rodadas, passos, transicoes, fila.
     sqlite3 painel.db "PRAGMA journal_mode" → wal.
"""
from __future__ import annotations

import os
import sqlite3
import tempfile

import pytest

AQUI = os.path.dirname(os.path.abspath(__file__))
SCHEMA_SQL = os.path.join(AQUI, "..", "schema_workflow.sql")


class TestSchemaWorkflow:
    """T1: Schema SQLite com tabelas append-only em modo WAL."""

    def test_schema_cria_tabelas(self):
        """Schema cria rodadas, passos, transicoes, fila."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        try:
            conn = sqlite3.connect(db_path)
            with open(SCHEMA_SQL, encoding="utf-8") as sf:
                conn.executescript(sf.read())
            tables = {
                row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            }
            conn.close()
            assert "rodadas" in tables
            assert "passos" in tables
            assert "transicoes" in tables
            assert "fila" in tables
        finally:
            os.unlink(db_path)

    def test_schema_ativa_wal(self):
        """Schema ativa modo WAL."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        try:
            conn = sqlite3.connect(db_path)
            with open(SCHEMA_SQL, encoding="utf-8") as sf:
                conn.executescript(sf.read())
            mode = conn.execute("PRAGMA journal_mode").fetchone()[0]
            conn.close()
            assert mode == "wal"
        finally:
            os.unlink(db_path)

    def test_rodadas_append_only(self):
        """rodadas: id, desejo, criada_por, aberta_em, fechada_em."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        try:
            conn = sqlite3.connect(db_path)
            with open(SCHEMA_SQL, encoding="utf-8") as sf:
                conn.executescript(sf.read())
            cols = {row[1] for row in conn.execute("PRAGMA table_info(rodadas)")}
            conn.close()
            assert {"id", "desejo", "criada_por", "aberta_em", "fechada_em"} <= cols
        finally:
            os.unlink(db_path)

    def test_passos_append_only(self):
        """passos: rodada, passo, sessao, entrada_em, resumo, saida_em, evidencia_json, resultado."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        try:
            conn = sqlite3.connect(db_path)
            with open(SCHEMA_SQL, encoding="utf-8") as sf:
                conn.executescript(sf.read())
            cols = {row[1] for row in conn.execute("PRAGMA table_info(passos)")}
            conn.close()
            expected = {"rodada", "passo", "sessao", "entrada_em", "resumo", "saida_em", "evidencia_json", "resultado"}
            assert expected <= cols
        finally:
            os.unlink(db_path)

    def test_transicoes_tem_evidencia_exigida(self):
        """transicoes: passo, proximo, evidencia_exigida."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        try:
            conn = sqlite3.connect(db_path)
            with open(SCHEMA_SQL, encoding="utf-8") as sf:
                conn.executescript(sf.read())
            cols = {row[1] for row in conn.execute("PRAGMA table_info(transicoes)")}
            conn.close()
            assert {"passo", "proximo", "evidencia_exigida"} <= cols
        finally:
            os.unlink(db_path)

    def test_fila_outbox(self):
        """fila: id, sessao_origem, sessao_destino, payload, criada_em, lida_em."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        try:
            conn = sqlite3.connect(db_path)
            with open(SCHEMA_SQL, encoding="utf-8") as sf:
                conn.executescript(sf.read())
            cols = {row[1] for row in conn.execute("PRAGMA table_info(fila)")}
            conn.close()
            assert {"id", "sessao_origem", "sessao_destino", "payload", "criada_em", "lida_em"} <= cols
        finally:
            os.unlink(db_path)

    def test_passos_abertos_visiveis(self):
        """DoD: SELECT count(*) FROM passos WHERE entrada_em IS NOT NULL AND saida_em IS NULL → ≥ 0."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        try:
            conn = sqlite3.connect(db_path)
            with open(SCHEMA_SQL, encoding="utf-8") as sf:
                conn.executescript(sf.read())
            count = conn.execute(
                "SELECT count(*) FROM passos WHERE entrada_em IS NOT NULL AND saida_em IS NULL"
            ).fetchone()[0]
            conn.close()
            assert count >= 0
        finally:
            os.unlink(db_path)
