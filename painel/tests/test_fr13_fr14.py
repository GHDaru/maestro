"""FR13/FR14 + issues W13 — testes de integração que chamam ingest.ingere() e fila_outbox.

FR13: ENQUANTO o ingest executa, O SISTEMA DEVE permitir escrita concorrente
      na tabela eventos sem "database is locked".
FR14: SE o ingest for interrompido, ENTÃO O SISTEMA DEVE manter a versão
      anterior completa das tabelas derivadas (swap atómico, nunca tabelas vazias).

Issue W13-1: open(SCHEMA_SQL) sem encoding="utf-8" → UnicodeDecodeError no Windows.
Issue W13-2: workflow_stop.py sem _ensure_schema() → OperationalError se tabelas não existem.
"""
from __future__ import annotations

import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import threading
import time
from unittest.mock import patch

import pytest

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, ".."))
import ingest
import fila_outbox

SCHEMA_SQL = os.path.join(AQUI, "..", "schema_workflow.sql")
HOOKS_DIR = os.path.join(AQUI, "..", "hooks")


def _cfg_minima(tmpdir: str) -> dict:
    """Config mínima para ingere() — sem fontes externas, só meta."""
    return {
        "projeto": "teste",
        "raiz": tmpdir,
        "equipes": {},
        "repos": [],
        "specs": [],
        "documentos": {},
    }


class TestFR13EventosSemLock:
    """FR13: escrita concorrente em eventos durante ingest não bloqueia."""

    def test_eventos_escrita_concorrente_nao_trava(self):
        """Duas conexões WAL escrevem em eventos sem 'database is locked'."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        try:
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


class TestFR14SwapAtomicoViaIngere:
    """FR14: ingere() faz swap atómico — DB anterior permanece se interrompido."""

    def test_ingere_completo_faz_swap(self, tmp_path):
        """ingere() completa cria DB com tabelas derivadas via swap atómico."""
        db_path = str(tmp_path / "painel.db")
        cfg = _cfg_minima(str(tmp_path))

        contagem = ingest.ingere(cfg, db_path)

        assert os.path.exists(db_path)
        conn = sqlite3.connect(db_path)
        tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        conn.close()
        assert "meta" in tables
        assert "sessoes" in tables
        assert not os.path.exists(db_path + ".tmp")

    def test_ingere_interrompido_mantem_anterior(self, tmp_path):
        """Se ingere() crasha antes do swap, DB anterior permanece intacto."""
        db_path = str(tmp_path / "painel.db")
        cfg = _cfg_minima(str(tmp_path))

        # Primeiro ingest — cria DB original
        ingest.ingere(cfg, db_path)
        conn = sqlite3.connect(db_path)
        conn.execute("INSERT INTO sessoes (nome, papel) VALUES ('w09', 'Worker09')")
        conn.commit()
        conn.close()

        # Segundo ingest crasha no os.replace — simula interrupção
        with patch("os.replace", side_effect=OSError("disk full")):
            with pytest.raises(OSError):
                ingest.ingere(cfg, db_path)

        # DB original permanece com dados intactos
        conn = sqlite3.connect(db_path)
        row = conn.execute("SELECT nome FROM sessoes WHERE nome = 'w09'").fetchone()
        conn.close()
        assert row is not None
        assert row[0] == "w09"

    def test_ingere_preserva_eventos(self, tmp_path):
        """ingere() preserva eventos append-only através do swap."""
        db_path = str(tmp_path / "painel.db")
        cfg = _cfg_minima(str(tmp_path))

        ingest.ingere(cfg, db_path)

        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA journal_mode = WAL")
        conn.execute(
            "INSERT INTO eventos (ts, tipo, autor) VALUES (?, ?, ?)",
            ("2026-10-02T00:00:00", "status", "w09"),
        )
        conn.commit()
        conn.close()

        ingest.ingere(cfg, db_path)

        conn = sqlite3.connect(db_path)
        count = conn.execute("SELECT count(*) FROM eventos").fetchone()[0]
        conn.close()
        assert count == 1, "Eventos append-only devem sobreviver ao swap"

    def test_ingere_fonte_quebrada_nao_crasha(self, tmp_path):
        """Uma fonte quebrada registra erro, não crasha o ingest."""
        db_path = str(tmp_path / "painel.db")
        cfg = _cfg_minima(str(tmp_path))
        cfg["repos"] = [{"caminho": "/inexistente", "nome": "quebrado"}]

        contagem = ingest.ingere(cfg, db_path)
        assert "commits" in contagem  # git source tentou e falhou graciosa


class TestFilaOutboxIntegracao:
    """T5: Fila outbox — testes de integração com SQLite real."""

    def test_enfileirar_drenar(self, tmp_path):
        """enfileirar → drenar marca como lida."""
        db_path = str(tmp_path / "painel.db")
        conn = sqlite3.connect(db_path)
        with open(SCHEMA_SQL, encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.close()

        fila = fila_outbox.FilaOutbox(db_path)
        id1 = fila.enfileirar(origem="sessao-w09", payload={"passo": "T1", "ok": True})
        id2 = fila.enfileirar(origem="sessao-gerente", payload={"passo": "T2", "ok": False})

        assert fila.pendentes() == 2

        msgs = fila.drenar()
        assert len(msgs) == 2
        assert msgs[0].payload["passo"] == "T1"
        assert msgs[1].payload["passo"] == "T2"
        assert fila.pendentes() == 0

    def test_drenar_destino_especifico(self, tmp_path):
        """drenar(destino) só lê mensagens para aquele destino."""
        db_path = str(tmp_path / "painel.db")
        conn = sqlite3.connect(db_path)
        with open(SCHEMA_SQL, encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.close()

        fila = fila_outbox.FilaOutbox(db_path)
        fila.enfileirar(origem="a", payload={"x": 1}, destino="w09")
        fila.enfileirar(origem="b", payload={"x": 2}, destino="w03")

        msgs = fila.drenar(destino="w09")
        assert len(msgs) == 1
        assert msgs[0].payload["x"] == 1
        assert fila.pendentes() == 1


    def test_payload_invalido_nao_envenena_a_fila(self, tmp_path):
        """Achado 2 da passagem de segurança do 070: uma linha com JSON inválido
        não pode derrubar drenar() para sempre — é lida, marcada e devolvida com _erro."""
        db_path = str(tmp_path / "painel.db")
        conn = sqlite3.connect(db_path)
        with open(SCHEMA_SQL, encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.execute(
            "INSERT INTO fila (sessao_origem, sessao_destino, payload, criada_em) VALUES (?, ?, ?, ?)",
            ("a", "w09", '{"rodada": "x", "passo": "y"z}', "2026-10-22T16:50:00+00:00"),
        )
        conn.commit()
        conn.close()

        fila = fila_outbox.FilaOutbox(db_path)
        fila.enfileirar(origem="b", payload={"x": 2}, destino="w09")
        msgs = fila.drenar(destino="w09")
        assert len(msgs) == 2
        assert "_erro" in msgs[0].payload
        assert msgs[1].payload["x"] == 2
        assert fila.pendentes() == 0
        assert fila.drenar(destino="w09") == []


class TestW13Issue1Encoding:
    """W13 Issue 1: workflow_session_start.py deve abrir schema com encoding=utf-8."""

    def test_hook_le_schema_sem_unicodeBunicode_error(self, tmp_path):
        """Hook SessionStart lê schema_workflow.sql sem UnicodeDecodeError no Windows."""
        db_path = str(tmp_path / "painel.db")
        # Cria DB com schema (tabelas workflow)
        conn = sqlite3.connect(db_path)
        with open(SCHEMA_SQL, encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.close()

        # Executa o hook — se encoding estiver errado, crasha com UnicodeDecodeError
        env = os.environ.copy()
        env["MAESTRO_DB"] = db_path
        env["MAESTRO_RODADA"] = "001"
        env["MAESTRO_PASSO"] = "T1"
        env["CLAUDE_SESSION_ID"] = "test-session"
        hook_path = os.path.join(HOOKS_DIR, "workflow_session_start.py")
        result = subprocess.run(
            [sys.executable, hook_path],
            env=env,
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0, f"Hook crashou: {result.stderr}"


class TestW13Issue2EnsureSchema:
    """W13 Issue 2: workflow_stop.py deve garantir tabelas antes da query."""

    def test_stop_com_db_sem_tabelas_workflow(self, tmp_path):
        """Hook Stop em DB sem tabelas workflow não crasha com OperationalError."""
        db_path = str(tmp_path / "painel.db")
        # Cria DB SEM tabelas workflow (só eventos)
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA journal_mode = WAL")
        conn.execute(
            "CREATE TABLE eventos (id INTEGER PRIMARY KEY, ts TEXT, tipo TEXT, autor TEXT)"
        )
        conn.commit()
        conn.close()

        env = os.environ.copy()
        env["MAESTRO_DB"] = db_path
        env["MAESTRO_RODADA"] = "001"
        env["MAESTRO_PASSO"] = "T1"
        env["CLAUDE_SESSION_ID"] = "test-session"
        hook_path = os.path.join(HOOKS_DIR, "workflow_stop.py")
        result = subprocess.run(
            [sys.executable, hook_path],
            env=env,
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0, f"Hook crashou: {result.stderr}"
