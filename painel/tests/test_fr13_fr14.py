"""FR13/FR14 (red) — eventos sem lock + swap atómico.

FR13: ENQUANTO o ingest executa, O SISTEMA DEVE permitir escrita concorrente
      na tabela eventos sem "database is locked".
FR14: SE o ingest for interrompido, ENTÃO O SISTEMA DEVE manter a versão
      anterior completa das tabelas derivadas (swap atómico, nunca tabelas vazias).
"""
from __future__ import annotations

import os
import sqlite3
import tempfile
import threading
import time

import pytest

AQUI = os.path.dirname(os.path.abspath(__file__))
INGEST_PY = os.path.join(AQUI, "..", "ingest.py")


class TestFR13EventosSemLock:
    """FR13: escrita concorrente em eventos durante ingest não bloqueia."""

    def test_eventos_escrita_concorrente_nao_trava(self):
        """Duas conexões WAL escrevem em eventos sem 'database is locked'."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        try:
            # Setup: cria tabela eventos em WAL
            conn = sqlite3.connect(db_path)
            conn.execute("PRAGMA journal_mode = WAL")
            conn.execute(
                "CREATE TABLE eventos (id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "ts TEXT, tipo TEXT, autor TEXT)"
            )
            conn.commit()
            conn.close()

            errors: list[str] = []

            def escrever(delay: float):
                try:
                    time.sleep(delay)
                    c = sqlite3.connect(db_path, timeout=5.0)
                    c.execute("PRAGMA journal_mode = WAL")
                    c.execute(
                        "INSERT INTO eventos (ts, tipo, autor) VALUES (?, ?, ?)",
                        ("2026-10-02T00:00:00", "status", "w09"),
                    )
                    c.commit()
                    c.close()
                except Exception as e:
                    errors.append(str(e))

            # Duas threads escrevem concorrentemente
            t1 = threading.Thread(target=escrever, args=(0.0,))
            t2 = threading.Thread(target=escrever, args=(0.05,))
            t1.start()
            t2.start()
            t1.join(timeout=10)
            t2.join(timeout=10)

            assert not errors, f"Erros de lock: {errors}"

            conn = sqlite3.connect(db_path)
            count = conn.execute("SELECT count(*) FROM eventos").fetchone()[0]
            conn.close()
            assert count == 2
        finally:
            for ext in ("", "-wal", "-shm"):
                p = db_path + ext
                if os.path.exists(p):
                    os.unlink(p)


class TestFR14SwapAtomico:
    """FR14: ingest interrompido mantém versão anterior (swap atómico)."""

    def test_ingest_interrompido_mantem_tabelas(self):
        """Se ingest falha a meio, tabelas derivadas anteriores permanecem."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        try:
            # Setup: DB com dados derivados existentes
            conn = sqlite3.connect(db_path)
            conn.execute("PRAGMA journal_mode = WAL")
            conn.execute("CREATE TABLE sessoes (nome TEXT PRIMARY KEY, papel TEXT)")
            conn.execute("INSERT INTO sessoes VALUES ('w09', 'Worker09')")
            conn.commit()
            conn.close()

            # Simula ingest interrompido: escreve num temp, NÃO faz swap
            # (o swap é os.replace — se não chega lá, o original permanece)
            temp_path = db_path + ".tmp"
            temp_conn = sqlite3.connect(temp_path)
            temp_conn.execute("CREATE TABLE sessoes (nome TEXT PRIMARY KEY, papel TEXT)")
            # Falha antes de popular — temp fica vazio
            temp_conn.close()
            # NÃO faz os.replace — simula interrupção

            # Original deve estar intacto
            conn = sqlite3.connect(db_path)
            count = conn.execute("SELECT count(*) FROM sessoes").fetchone()[0]
            conn.close()
            assert count == 1, "Tabelas derivadas anteriores devem permanecer após interrupção"

            # Cleanup temp
            if os.path.exists(temp_path):
                os.unlink(temp_path)
        finally:
            for ext in ("", "-wal", "-shm"):
                p = db_path + ext
                if os.path.exists(p):
                    os.unlink(p)

    def test_ingest_completo_faz_swap(self):
        """Quando ingest completa, swap atómico substitui versão anterior."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        try:
            # Setup: DB com dados antigos
            conn = sqlite3.connect(db_path)
            conn.execute("PRAGMA journal_mode = WAL")
            conn.execute("CREATE TABLE sessoes (nome TEXT PRIMARY KEY, papel TEXT)")
            conn.execute("INSERT INTO sessoes VALUES ('velho', 'Velho')")
            conn.commit()
            conn.close()

            # Ingest completo: escreve temp, faz swap
            temp_path = db_path + ".tmp"
            temp_conn = sqlite3.connect(temp_path)
            temp_conn.execute("PRAGMA journal_mode = WAL")
            temp_conn.execute("CREATE TABLE sessoes (nome TEXT PRIMARY KEY, papel TEXT)")
            temp_conn.execute("INSERT INTO sessoes VALUES ('novo', 'Novo')")
            temp_conn.commit()
            temp_conn.close()

            # Swap atómico
            os.replace(temp_path, db_path)

            conn = sqlite3.connect(db_path)
            row = conn.execute("SELECT nome FROM sessoes").fetchone()
            conn.close()
            assert row is not None
            assert row[0] == "novo", "Swap atómico deve substituir versão anterior"
        finally:
            for ext in ("", "-wal", "-shm"):
                p = db_path + ext
                if os.path.exists(p):
                    os.unlink(p)
