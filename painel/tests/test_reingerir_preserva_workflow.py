"""Reingerir NÃO apaga tabelas de workflow (rodadas, passos, transicoes, fila).

Essas tabelas são registro PRIMÁRIO (gravado pelos hooks), não derivado.
O ingere() faz swap atómico: escreve num temp, os.replace no fim.
Se o temp não copiar as tabelas de workflow, o swap apaga o histórico.

Cenário: grava 1 rodada com 3 passos, roda ingere(), verifica que
a rodada e os 3 passos continuam lá.
"""
from __future__ import annotations

import os
import sqlite3
import sys
import tempfile

import pytest

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, ".."))
import ingest

SCHEMA_WORKFLOW_SQL = os.path.join(AQUI, "..", "schema_workflow.sql")


def _cfg_minima(tmpdir):
    return {
        "projeto": "teste",
        "raiz": str(tmpdir),
        "equipes": {},
        "repos": [],
        "specs": [],
        "documentos": {},
    }


def _cria_db_com_workflow(db_path):
    """Cria DB com schema workflow + 1 rodada com 3 passos."""
    conn = sqlite3.connect(db_path)
    with open(SCHEMA_WORKFLOW_SQL, encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.execute(
        "INSERT INTO rodadas (id, desejo, criada_por, aberta_em) "
        "VALUES ('001', 'Workflow painel', 'Gerente', '2026-10-02T10:00:00')"
    )
    for i in range(1, 4):
        conn.execute(
            "INSERT INTO passos (rodada, passo, sessao, entrada_em, resumo, saida_em, resultado) "
            "VALUES ('001', ?, 'W09', ?, ?, ?, 'ok')",
            (f"T{i}", f"2026-10-02T10:0{i}:00", f"T{i} done", f"2026-10-02T10:0{i}:30"),
        )
    conn.execute(
        "INSERT INTO transicoes (passo, proximo, evidencia_exigida) VALUES ('T1', 'T2', 1)"
    )
    conn.execute(
        "INSERT INTO fila (sessao_origem, payload, criada_em) "
        "VALUES ('W09', '{\"ok\":true}', '2026-10-02T10:00:00')"
    )
    conn.commit()
    conn.close()


class TestReingerirPreservaWorkflow:
    """Reingerir preserva tabelas de workflow (registro primário)."""

    def test_rodadas_sobrevive_reingerir(self, tmp_path):
        """rodadas: 1 rodada antes do ingere() → 1 rodada depois."""
        db_path = str(tmp_path / "painel.db")
        _cria_db_com_workflow(db_path)
        cfg = _cfg_minima(tmp_path)

        # Verificar antes
        conn = sqlite3.connect(db_path)
        before = conn.execute("SELECT count(*) FROM rodadas").fetchone()[0]
        conn.close()
        assert before == 1

        ingest.ingere(cfg, db_path)

        # Verificar depois
        conn = sqlite3.connect(db_path)
        after = conn.execute("SELECT count(*) FROM rodadas").fetchone()[0]
        conn.close()
        assert after == 1, f"rodadas apagadas pelo reingerir: {before} → {after}"

    def test_passos_sobrevive_reingerir(self, tmp_path):
        """passos: 3 passos antes do ingere() → 3 passos depois."""
        db_path = str(tmp_path / "painel.db")
        _cria_db_com_workflow(db_path)
        cfg = _cfg_minima(tmp_path)

        ingest.ingere(cfg, db_path)

        conn = sqlite3.connect(db_path)
        after = conn.execute("SELECT count(*) FROM passos").fetchone()[0]
        conn.close()
        assert after == 3, f"passos apagados pelo reingerir: 3 → {after}"

    def test_transicoes_sobrevive_reingerir(self, tmp_path):
        """transicoes: 1 transicao antes → 1 depois."""
        db_path = str(tmp_path / "painel.db")
        _cria_db_com_workflow(db_path)
        cfg = _cfg_minima(tmp_path)

        ingest.ingere(cfg, db_path)

        conn = sqlite3.connect(db_path)
        after = conn.execute("SELECT count(*) FROM transicoes").fetchone()[0]
        conn.close()
        assert after == 1, f"transicoes apagadas: 1 → {after}"

    def test_fila_sobrevive_reingerir(self, tmp_path):
        """fila: 1 mensagem antes → 1 depois."""
        db_path = str(tmp_path / "painel.db")
        _cria_db_com_workflow(db_path)
        cfg = _cfg_minima(tmp_path)

        ingest.ingere(cfg, db_path)

        conn = sqlite3.connect(db_path)
        after = conn.execute("SELECT count(*) FROM fila").fetchone()[0]
        conn.close()
        assert after == 1, f"fila apagada: 1 → {after}"

    def test_dados_especificos_preservados(self, tmp_path):
        """Os dados específicos da rodada sobrevivem (id, desejo, passos)."""
        db_path = str(tmp_path / "painel.db")
        _cria_db_com_workflow(db_path)
        cfg = _cfg_minima(tmp_path)

        ingest.ingere(cfg, db_path)

        conn = sqlite3.connect(db_path)
        rod = conn.execute("SELECT id, desejo FROM rodadas WHERE id='001'").fetchone()
        passos = conn.execute(
            "SELECT passo, resumo FROM passos WHERE rodada='001' ORDER BY id"
        ).fetchall()
        conn.close()

        assert rod is not None
        assert rod[0] == "001"
        assert rod[1] == "Workflow painel"
        assert len(passos) == 3
        assert passos[0][0] == "T1"
        assert passos[2][0] == "T3"
