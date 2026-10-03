"""Fixes W12 RETURN 6fb791d — red tests para 2 blocking + 2 menores + 2 mutantes.

#1 BLOCKING: T2 faltam nós plan/critica/teste (FR8 exige 4 ramos)
#2 MENOR: commit→T não implementado (hash/evidencia_ok nunca populados)
#3 BLOCKING: FR13 sem_tarefa_ciclos sempre 0
#4 MENOR: status_workers campos sempre defaults
MUTANTE 1: task multi-FR (pai=t_frs[0] vs t_frs[-1])
MUTANTE 2: idempotência (re-ingest não testado)
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


def _cfg_com_spec(tmp_path):
    """Config com spec 064 + tasks + testes + plan artefatos."""
    spec_dir = tmp_path / "specs" / "064-workflow-painel"
    spec_dir.mkdir(parents=True)
    (spec_dir / "spec.md").write_text(
        "# Spec 064 — Workflow painel\n\n"
        "## Functional requirements\n\n"
        "- **FR1**: O SISTEMA DEVE exibir o board.\n"
        "- **FR2**: O SISTEMA DEVE exibir linha por sessão.\n"
        "- **FR8**: O SISTEMA DEVE exibir rodada em árvore.\n"
        "- **FR10**: O SISTEMA DEVE marcar requisito sem teste.\n"
        "- **FR12**: O SISTEMA DEVE derivar árvore de convenções.\n"
        "- **FR13**: SE status sem tarefa em 2 ciclos, contar.\n",
        encoding="utf-8",
    )
    (spec_dir / "tasks.md").write_text(
        "# Tasks 064\n\n"
        "### T1 — Schema\n**FRs**: FR1\n\n"
        "### T2 — Ingest arvore\n**FRs**: FR8, FR10, FR12\n\n"
        "### T3 — Ingest status\n**FRs**: FR1, FR2, FR13\n",
        encoding="utf-8",
    )
    (spec_dir / "plan.md").write_text("# Plan 064\n", encoding="utf-8")
    (spec_dir / "ux-design.md").write_text("# UX 064\n", encoding="utf-8")

    test_dir = tmp_path / "painel" / "tests"
    test_dir.mkdir(parents=True)
    (test_dir / "test_fr1_excecoes_topo.py").write_text("# test FR1", encoding="utf-8")
    (test_dir / "test_fr8_arvore.py").write_text("# test FR8", encoding="utf-8")

    return {
        "projeto": "teste",
        "raiz": str(tmp_path),
        "equipes": {},
        "repos": [],
        "specs": [{"caminho": str(spec_dir / "spec.md"), "numero": "064"}],
        "documentos": {},
    }


# ---------------------------------------------------------------------------
# #1 BLOCKING: T2 faltam nós plan/critica/teste
# ---------------------------------------------------------------------------

class TestArvoreNosPlanCriticaTeste:
    """#1: ingere_arvore deve criar nós tipo plan, critica, teste (FR8)."""

    def test_arvore_tem_nos_plan(self, tmp_path):
        """ingere() cria nós tipo='plan' para artefatos do plan."""
        db_path = str(tmp_path / "painel.db")
        cfg = _cfg_com_spec(tmp_path)
        ingest.ingere(cfg, db_path)

        conn = sqlite3.connect(db_path)
        nos_plan = conn.execute(
            "SELECT id_no FROM arvore_rodada WHERE tipo = 'plan' AND rodada = '064'"
        ).fetchall()
        conn.close()
        assert len(nos_plan) > 0, "Deve haver nós tipo='plan' (ux-design.md, plan.md, tasks.md)"

    def test_arvore_tem_nos_teste(self, tmp_path):
        """ingere() cria nós tipo='teste' para arquivos de teste."""
        db_path = str(tmp_path / "painel.db")
        cfg = _cfg_com_spec(tmp_path)
        ingest.ingere(cfg, db_path)

        conn = sqlite3.connect(db_path)
        nos_teste = conn.execute(
            "SELECT id_no FROM arvore_rodada WHERE tipo = 'teste' AND rodada = '064'"
        ).fetchall()
        conn.close()
        ids = {r[0] for r in nos_teste}
        assert len(nos_teste) > 0, "Deve haver nós tipo='teste' (test_fr1_…, test_fr8_…)"
        assert "test_fr1_excecoes_topo" in ids or any("fr1" in i.lower() for i in ids)

    def test_teste_filho_de_fr(self, tmp_path):
        """Nó teste é filho do FR correspondente (test_fr1_* → pai=FR1)."""
        db_path = str(tmp_path / "painel.db")
        cfg = _cfg_com_spec(tmp_path)
        ingest.ingere(cfg, db_path)

        conn = sqlite3.connect(db_path)
        row = conn.execute(
            "SELECT pai FROM arvore_rodada WHERE tipo='teste' AND rodada='064' "
            "AND id_no LIKE '%fr1%'"
        ).fetchone()
        conn.close()
        assert row is not None, "Deve haver teste filho de FR1"
        assert row[0] == "FR1"


# ---------------------------------------------------------------------------
# #3 BLOCKING: FR13 sem_tarefa_ciclos sempre 0
# ---------------------------------------------------------------------------

class TestFR13SemTarefaCiclos:
    """#3: ingere_status_workers deve calcular sem_tarefa_ciclos."""

    def test_sem_tarefa_ciclos_calculado(self, tmp_path):
        """Worker com 2 ciclos sem tarefa → sem_tarefa_ciclos=2."""
        db_path = str(tmp_path / "painel.db")
        cfg = _cfg_com_spec(tmp_path)
        cfg["equipes"] = {"W99": {"papel": "Worker99"}}

        ingest.ingere(cfg, db_path)

        # Simular 2 eventos de status "sem tarefa" consecutivos
        conn = sqlite3.connect(db_path)
        for i in range(2):
            conn.execute(
                "INSERT INTO eventos (ts, sessao, tipo, estado, autor) "
                "VALUES (?, 'W99', 'status', 'sem tarefa', 'sistema')",
                (f"2026-10-02T00:0{i}:00",),
            )
        conn.commit()
        conn.close()

        # Re-ingerir para calcular sem_tarefa_ciclos
        ingest.ingere(cfg, db_path)

        conn = sqlite3.connect(db_path)
        row = conn.execute(
            "SELECT sem_tarefa_ciclos FROM status_workers WHERE sessao = 'W99'"
        ).fetchone()
        conn.close()
        assert row is not None
        assert row[0] >= 2, f"sem_tarefa_ciclos deve ser >= 2, got {row[0]}"

    def test_com_tarefa_ciclos_zero(self, tmp_path):
        """Worker com tarefa → sem_tarefa_ciclos=0."""
        db_path = str(tmp_path / "painel.db")
        cfg = _cfg_com_spec(tmp_path)
        cfg["equipes"] = {"W01": {"papel": "Worker01"}}

        ingest.ingere(cfg, db_path)

        # Evento de status "busy" (com tarefa)
        conn = sqlite3.connect(db_path)
        conn.execute(
            "INSERT INTO eventos (ts, sessao, tipo, estado, peca, autor) "
            "VALUES ('2026-10-02T00:00:00', 'W01', 'status', 'busy', '065/T1', 'sistema')"
        )
        conn.commit()
        conn.close()

        ingest.ingere(cfg, db_path)

        conn = sqlite3.connect(db_path)
        row = conn.execute(
            "SELECT sem_tarefa_ciclos FROM status_workers WHERE sessao = 'W01'"
        ).fetchone()
        conn.close()
        assert row is not None
        assert row[0] == 0


# ---------------------------------------------------------------------------
# #2 MENOR: commit→T hash/evidencia_ok nunca populados
# ---------------------------------------------------------------------------

class TestCommitParaT:
    """#2: ingere_arvore deve popular hash e evidencia_ok nos nós task."""

    def test_task_hash_populado(self, tmp_path):
        """Nó task tem hash populado quando commit cita a task."""
        db_path = str(tmp_path / "painel.db")
        cfg = _cfg_com_spec(tmp_path)
        # Simular commits que citam T1 e T2
        cfg["repos"] = [{"caminho": str(tmp_path), "nome": "teste"}]

        # Criar um repo git fake com commits
        import subprocess
        subprocess.run(["git", "init"], cwd=str(tmp_path), capture_output=True)
        subprocess.run(["git", "config", "user.email", "t@t.com"], cwd=str(tmp_path), capture_output=True)
        subprocess.run(["git", "config", "user.name", "test"], cwd=str(tmp_path), capture_output=True)
        subprocess.run(["git", "add", "."], cwd=str(tmp_path), capture_output=True)
        subprocess.run(["git", "commit", "-m", "064 T1: schema"], cwd=str(tmp_path), capture_output=True)
        subprocess.run(["git", "commit", "-m", "064 T2: ingest arvore", "--allow-empty"], cwd=str(tmp_path), capture_output=True)

        ingest.ingere(cfg, db_path)

        conn = sqlite3.connect(db_path)
        row = conn.execute(
            "SELECT hash FROM arvore_rodada WHERE tipo='task' AND rodada='064' AND id_no='T1'"
        ).fetchone()
        conn.close()
        assert row is not None
        assert row[0] is not None and len(row[0]) > 0, "T1 deve ter hash do commit"


# ---------------------------------------------------------------------------
# #4 MENOR: status_workers campos sempre defaults
# ---------------------------------------------------------------------------

class TestStatusWorkersCampos:
    """#4: ingere_status_workers deve popular peca, passo, ultima_atividade."""

    def test_peca_populada_de_evento(self, tmp_path):
        """status_workers.peca populado do último evento de status."""
        db_path = str(tmp_path / "painel.db")
        cfg = _cfg_com_spec(tmp_path)
        cfg["equipes"] = {"W01": {"papel": "Worker01"}}

        ingest.ingere(cfg, db_path)

        conn = sqlite3.connect(db_path)
        conn.execute(
            "INSERT INTO eventos (ts, sessao, tipo, estado, peca, autor) "
            "VALUES ('2026-10-02T00:00:00', 'W01', 'status', 'busy', '065/T1', 'sistema')"
        )
        conn.commit()
        conn.close()

        ingest.ingere(cfg, db_path)

        conn = sqlite3.connect(db_path)
        row = conn.execute(
            "SELECT peca, estado, ultima_atividade FROM status_workers WHERE sessao = 'W01'"
        ).fetchone()
        conn.close()
        assert row is not None
        assert row[0] is not None and "065" in row[0], f"peca deve ser populada, got {row[0]}"
        assert row[1] == "busy", f"estado deve ser 'busy', got {row[1]}"
        assert row[2] is not None, "ultima_atividade deve ser populada"


# ---------------------------------------------------------------------------
# MUTANTE 1: task multi-FR (pai=t_frs[0] vs t_frs[-1])
# ---------------------------------------------------------------------------

class TestMutanteTaskMultiFR:
    """Mutante 1: T2 tem FRs=[FR8, FR10, FR12] — pai deve ser FR8 (primeiro)."""

    def test_t2_pai_eh_primeiro_fr(self, tmp_path):
        """T2 → FR8, FR10, FR12: pai deve ser FR8 (primeiro), não FR12 (último)."""
        db_path = str(tmp_path / "painel.db")
        cfg = _cfg_com_spec(tmp_path)
        ingest.ingere(cfg, db_path)

        conn = sqlite3.connect(db_path)
        row = conn.execute(
            "SELECT pai FROM arvore_rodada WHERE rodada='064' AND tipo='task' AND id_no='T2'"
        ).fetchone()
        conn.close()
        assert row is not None
        assert row[0] == "FR8", f"T2 pai deve ser FR8 (primeiro FR), got {row[0]}"

    def test_t2_referencia_todos_frs(self, tmp_path):
        """T2 referencia deve conter todos os FRs: FR8, FR10, FR12."""
        db_path = str(tmp_path / "painel.db")
        cfg = _cfg_com_spec(tmp_path)
        ingest.ingere(cfg, db_path)

        conn = sqlite3.connect(db_path)
        row = conn.execute(
            "SELECT referencia FROM arvore_rodada WHERE rodada='064' AND tipo='task' AND id_no='T2'"
        ).fetchone()
        conn.close()
        assert row is not None
        ref = row[0] or ""
        assert "FR8" in ref, "referencia deve conter FR8"
        assert "FR10" in ref, "referencia deve conter FR10"
        assert "FR12" in ref, "referencia deve conter FR12"


# ---------------------------------------------------------------------------
# MUTANTE 2: idempotência (re-ingest não testado)
# ---------------------------------------------------------------------------

class TestIdempotencia:
    """Mutante 2: re-ingest produz o mesmo resultado (sem duplicatas)."""

    def test_re_ingest_mesma_arvore(self, tmp_path):
        """Ingere() duas vezes → arvore_rodada tem o mesmo número de nós."""
        db_path = str(tmp_path / "painel.db")
        cfg = _cfg_com_spec(tmp_path)

        ingest.ingere(cfg, db_path)
        conn = sqlite3.connect(db_path)
        count1 = conn.execute("SELECT count(*) FROM arvore_rodada").fetchone()[0]
        conn.close()

        ingest.ingere(cfg, db_path)
        conn = sqlite3.connect(db_path)
        count2 = conn.execute("SELECT count(*) FROM arvore_rodada").fetchone()[0]
        conn.close()

        assert count1 == count2, f"Re-ingest deve produzir mesmo count: {count1} vs {count2}"

    def test_re_ingest_mesmos_nos(self, tmp_path):
        """Ingere() duas vezes → mesmos id_no na arvore_rodada."""
        db_path = str(tmp_path / "painel.db")
        cfg = _cfg_com_spec(tmp_path)

        ingest.ingere(cfg, db_path)
        conn = sqlite3.connect(db_path)
        nos1 = {r[0] + "|" + r[1] for r in conn.execute(
            "SELECT id_no, tipo FROM arvore_rodada WHERE rodada='064'"
        )}
        conn.close()

        ingest.ingere(cfg, db_path)
        conn = sqlite3.connect(db_path)
        nos2 = {r[0] + "|" + r[1] for r in conn.execute(
            "SELECT id_no, tipo FROM arvore_rodada WHERE rodada='064'"
        )}
        conn.close()

        assert nos1 == nos2, f"Re-ingest deve produzir mesmos nós: {nos1} vs {nos2}"
