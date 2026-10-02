"""T2+T3 (red) — Ingest materializa arvore_rodada, status_workers, excecoes_board.

T2 FRs: FR8, FR10, FR12 — arvore_rodada derivada das convenções.
T3 FRs: FR1, FR2, FR13 — status_workers e excecoes_board.

Convenções (FR12):
  - ID no spec.md (FR13) → nó folha sob spec
  - Tarefa cita requisito (T2 → FR13) → T2 filho de FR13
  - Commit cita tarefa (064 T2: …) → commit ligado a T2
  - Teste cita requisito (test_fr13_…) → teste filho de FR13
  - FR sem teste → status='descoberto' (FR10)
"""
from __future__ import annotations

import json
import os
import sqlite3
import sys
import tempfile

import pytest

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, ".."))
import ingest

SCHEMA_065_SQL = os.path.join(AQUI, "..", "schema_065.sql")
SCHEMA_WORKFLOW_SQL = os.path.join(AQUI, "..", "schema_workflow.sql")


def _cfg_com_spec(tmp_path):
    """Config mínima com uma spec de teste com FRs."""
    spec_dir = tmp_path / "specs" / "064-workflow-painel"
    spec_dir.mkdir(parents=True)
    (spec_dir / "spec.md").write_text(
        "# Spec 064 — Workflow painel\n\n"
        "## Functional requirements\n\n"
        "- **FR1**: O SISTEMA DEVE exibir o board.\n"
        "- **FR2**: O SISTEMA DEVE exibir linha por sessão.\n"
        "- **FR13**: SE status sem tarefa em 2 ciclos, contar na exceção.\n",
        encoding="utf-8",
    )
    # tasks.md com T→FR
    (spec_dir / "tasks.md").write_text(
        "# Tasks 064\n\n"
        "### T1 — Schema\n**FRs**: FR1\n\n"
        "### T2 — Ingest arvore\n**FRs**: FR8, FR10, FR12\n\n"
        "### T3 — Ingest status\n**FRs**: FR1, FR2, FR13\n",
        encoding="utf-8",
    )
    # teste que cita FR1
    test_dir = tmp_path / "painel" / "tests"
    test_dir.mkdir(parents=True)
    (test_dir / "test_fr1_excecoes_topo.py").write_text("# test FR1", encoding="utf-8")

    return {
        "projeto": "teste",
        "raiz": str(tmp_path),
        "equipes": {},
        "repos": [],
        "specs": [{"caminho": str(spec_dir / "spec.md"), "numero": "064"}],
        "documentos": {},
    }


class TestIngereArvore:
    """T2: ingere_arvore materializa arvore_rodada das convenções."""

    def test_arvore_tem_nos_spec(self, tmp_path):
        """ingere() cria nós tipo='spec' para cada FR encontrado na spec.md."""
        db_path = str(tmp_path / "painel.db")
        cfg = _cfg_com_spec(tmp_path)

        ingest.ingere(cfg, db_path)

        conn = sqlite3.connect(db_path)
        nos_spec = conn.execute(
            "SELECT id_no FROM arvore_rodada WHERE tipo = 'spec' AND rodada = '064'"
        ).fetchall()
        conn.close()
        ids = {r[0] for r in nos_spec}
        assert "FR1" in ids
        assert "FR2" in ids
        assert "FR13" in ids

    def test_arvore_tem_nos_task(self, tmp_path):
        """ingere() cria nós tipo='task' para cada T encontrado no tasks.md."""
        db_path = str(tmp_path / "painel.db")
        cfg = _cfg_com_spec(tmp_path)

        ingest.ingere(cfg, db_path)

        conn = sqlite3.connect(db_path)
        nos_task = conn.execute(
            "SELECT id_no FROM arvore_rodada WHERE tipo = 'task' AND rodada = '064'"
        ).fetchall()
        conn.close()
        ids = {r[0] for r in nos_task}
        assert "T1" in ids
        assert "T2" in ids
        assert "T3" in ids

    def test_task_filho_de_fr(self, tmp_path):
        """T1 → FR1: T1 é filho de FR1 na árvore (pai = FR1)."""
        db_path = str(tmp_path / "painel.db")
        cfg = _cfg_com_spec(tmp_path)

        ingest.ingere(cfg, db_path)

        conn = sqlite3.connect(db_path)
        row = conn.execute(
            "SELECT pai FROM arvore_rodada WHERE rodada='064' AND tipo='task' AND id_no='T1'"
        ).fetchone()
        conn.close()
        assert row is not None
        assert row[0] == "FR1"

    def test_fr_sem_teste_descoberto(self, tmp_path):
        """FR10: FR sem teste ligado → status='descoberto'."""
        db_path = str(tmp_path / "painel.db")
        cfg = _cfg_com_spec(tmp_path)

        ingest.ingere(cfg, db_path)

        conn = sqlite3.connect(db_path)
        # FR2 não tem teste (só FR1 tem test_fr1_…)
        row = conn.execute(
            "SELECT status FROM arvore_rodada WHERE rodada='064' AND tipo='spec' AND id_no='FR2'"
        ).fetchone()
        conn.close()
        assert row is not None
        assert row[0] == "descoberto"

    def test_fr_com_teste_ok(self, tmp_path):
        """FR1 tem teste (test_fr1_…) → status='ok'."""
        db_path = str(tmp_path / "painel.db")
        cfg = _cfg_com_spec(tmp_path)

        ingest.ingere(cfg, db_path)

        conn = sqlite3.connect(db_path)
        row = conn.execute(
            "SELECT status FROM arvore_rodada WHERE rodada='064' AND tipo='spec' AND id_no='FR1'"
        ).fetchone()
        conn.close()
        assert row is not None
        assert row[0] == "ok"


class TestIngereStatus:
    """T3: ingere_status_workers materializa status_workers e excecoes_board."""

    def test_status_workers_populado(self, tmp_path):
        """ingere() popula status_workers com sessões do cfg."""
        db_path = str(tmp_path / "painel.db")
        cfg = _cfg_com_spec(tmp_path)
        cfg["equipes"] = {
            "W09": {"papel": "Worker09"},
            "W03": {"papel": "Worker03"},
        }

        ingest.ingere(cfg, db_path)

        conn = sqlite3.connect(db_path)
        rows = conn.execute("SELECT sessao FROM status_workers").fetchall()
        conn.close()
        sessoes = {r[0] for r in rows}
        assert "W09" in sessoes
        assert "W03" in sessoes

    def test_excecoes_board_tres_tipos(self, tmp_path):
        """ingere() cria 3 exceções: gilsiley, gate_push, sem_tarefa_2ciclos."""
        db_path = str(tmp_path / "painel.db")
        cfg = _cfg_com_spec(tmp_path)

        ingest.ingere(cfg, db_path)

        conn = sqlite3.connect(db_path)
        tipos = {r[0] for r in conn.execute("SELECT tipo FROM excecoes_board")}
        conn.close()
        assert "gilsiley" in tipos
        assert "gate_push" in tipos
        assert "sem_tarefa_2ciclos" in tipos

    def test_excecao_sem_tarefa_2ciclos(self, tmp_path):
        """FR13: worker com sem_tarefa_ciclos >= 2 conta na exceção."""
        db_path = str(tmp_path / "painel.db")
        cfg = _cfg_com_spec(tmp_path)
        cfg["equipes"] = {
            "W99": {"papel": "Worker99"},
        }

        ingest.ingere(cfg, db_path)

        conn = sqlite3.connect(db_path)
        # Inserir status manualmente para simular 2 ciclos sem tarefa
        conn.execute(
            "UPDATE status_workers SET sem_tarefa_ciclos = 2, estado = 'idle' WHERE sessao = 'W99'"
        )
        conn.commit()

        # Re-ingerir excecoes
        if hasattr(ingest, "ingere_excecoes"):
            ingest.ingere_excecoes(conn, cfg)

        row = conn.execute(
            "SELECT contador FROM excecoes_board WHERE tipo = 'sem_tarefa_2ciclos'"
        ).fetchone()
        conn.close()
        assert row is not None
        assert row[0] >= 1
