"""Testes do hook de veredito (desejo 004).

Cobre os cenários da spec:
- Hora no texto > commit + 2min → recusado
- Hora no texto ≤ commit + 2min → aceito
- Sem hora no texto → aceito (usa hora do commit)
- Veredito anterior ao objeto → recusado
- Sem linha Objeto → recusado
- Hash inexistente → recusado
- Hora com -0300 e sem fuso dão o mesmo resultado
"""
from __future__ import annotations

import os
import shutil
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

# Importa o módulo do hook
import sys
sys.path.insert(0, str(Path(__file__).parent))
from veredito_hook import verificar_veredito, _eh_veredito, BRT, TOLERANCIA

BRT = timezone(timedelta(hours=-3))


def _run(args, cwd):
    r = subprocess.run(args, capture_output=True, text=True, cwd=cwd)
    if r.returncode != 0:
        raise RuntimeError(f"{' '.join(args)}: {r.stderr}")
    return r.stdout.strip()


@pytest.fixture
def repo_tmp(tmp_path):
    """Cria um repo git temporário com commits de teste."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _run(["git", "init"], repo)
    _run(["git", "config", "user.email", "test@test.com"], repo)
    _run(["git", "config", "user.name", "Test"], repo)
    # Commit inicial (objeto)
    (repo / "tasks.md").write_text("# Tasks\n", encoding="utf-8")
    _run(["git", "add", "tasks.md"], repo)
    # Define a data do autor para ter controle
    env = dict(os.environ, GIT_AUTHOR_DATE="2026-10-03T12:00:00-03:00",
               GIT_COMMITTER_DATE="2026-10-03T12:00:00-03:00")
    subprocess.run(["git", "commit", "-m", "objeto"], cwd=repo, env=env,
                   capture_output=True, text=True)
    objeto_hash = _run(["git", "rev-parse", "HEAD"], repo)[:7]
    return repo, objeto_hash


def _escrever_veredito(caminho, objeto_hash, hora_texto=None):
    """Escreve um arquivo de veredito de teste."""
    linhas = [f"Objeto: tasks.md @ {objeto_hash}", ""]
    if hora_texto:
        linhas.insert(0, f"Data: {hora_texto}")
    caminho.write_text("\n".join(linhas) + "\n", encoding="utf-8")


class TestVereditoHora:
    """Testes de hora no texto vs commit."""

    def test_hora_texto_maior_que_commit_mais_2min_rejeita(self, repo_tmp):
        """'12:50' num commit de 12:22 é recusado."""
        repo, objeto_hash = repo_tmp
        arq = repo / "veredito-teste.md"
        _escrever_veredito(arq, objeto_hash, "03/10/2026 12:50 -0300")
        hora_commit = datetime(2026, 10, 3, 12, 22, tzinfo=BRT)
        result = verificar_veredito(arq, hora_commit=hora_commit, git_cwd=repo)
        assert not result.ok
        assert "posterior ao commit" in result.motivo

    def test_hora_texto_igual_commit_aceita(self, repo_tmp):
        """'12:10' num commit de 12:12 é aceito."""
        repo, objeto_hash = repo_tmp
        arq = repo / "veredito-teste.md"
        _escrever_veredito(arq, objeto_hash, "03/10/2026 12:10 -0300")
        hora_commit = datetime(2026, 10, 3, 12, 12, tzinfo=BRT)
        result = verificar_veredito(arq, hora_commit=hora_commit, git_cwd=repo)
        assert result.ok

    def test_hora_texto_dentro_tolerancia_aceita(self, repo_tmp):
        """'12:13' num commit de 12:12 é aceito (tolerância 2min)."""
        repo, objeto_hash = repo_tmp
        arq = repo / "veredito-teste.md"
        _escrever_veredito(arq, objeto_hash, "03/10/2026 12:13 -0300")
        hora_commit = datetime(2026, 10, 3, 12, 12, tzinfo=BRT)
        result = verificar_veredito(arq, hora_commit=hora_commit, git_cwd=repo)
        assert result.ok

    def test_hora_texto_exatamente_2min_aceita(self, repo_tmp):
        """'12:14' num commit de 12:12 é aceito (exatamente 2min)."""
        repo, objeto_hash = repo_tmp
        arq = repo / "veredito-teste.md"
        _escrever_veredito(arq, objeto_hash, "03/10/2026 12:14 -0300")
        hora_commit = datetime(2026, 10, 3, 12, 12, tzinfo=BRT)
        result = verificar_veredito(arq, hora_commit=hora_commit, git_cwd=repo)
        assert result.ok

    def test_hora_texto_3min_rejeita(self, repo_tmp):
        """'12:15' num commit de 12:12 é recusado (> 2min)."""
        repo, objeto_hash = repo_tmp
        arq = repo / "veredito-teste.md"
        _escrever_veredito(arq, objeto_hash, "03/10/2026 12:15 -0300")
        hora_commit = datetime(2026, 10, 3, 12, 12, tzinfo=BRT)
        result = verificar_veredito(arq, hora_commit=hora_commit, git_cwd=repo)
        assert not result.ok


class TestVereditoSemHora:
    """Veredito sem hora no texto."""

    def test_sem_hora_aceita(self, repo_tmp):
        """Sem linha de data é aceito, usa hora do commit."""
        repo, objeto_hash = repo_tmp
        arq = repo / "veredito-teste.md"
        _escrever_veredito(arq, objeto_hash, hora_texto=None)
        hora_commit = datetime(2026, 10, 3, 12, 30, tzinfo=BRT)
        result = verificar_veredito(arq, hora_commit=hora_commit, git_cwd=repo)
        assert result.ok


class TestVereditoAnteriorAoObjeto:
    """Veredito anterior ao objeto criticado."""

    def test_veredito_anterior_ao_objeto_rejeita(self, repo_tmp):
        """Veredito de 11:00 sobre objeto de 12:00 é recusado."""
        repo, objeto_hash = repo_tmp
        arq = repo / "veredito-teste.md"
        _escrever_veredito(arq, objeto_hash, "03/10/2026 11:00 -0300")
        hora_commit = datetime(2026, 10, 3, 11, 0, tzinfo=BRT)
        result = verificar_veredito(arq, hora_commit=hora_commit, git_cwd=repo)
        assert not result.ok
        assert "anterior ao objeto" in result.motivo


class TestVereditoObjeto:
    """Testes da linha Objeto."""

    def test_sem_linha_objeto_rejeita(self, repo_tmp):
        """Veredito sem 'Objeto: <caminho> @ <hash>' é recusado."""
        repo, objeto_hash = repo_tmp
        arq = repo / "veredito-teste.md"
        arq.write_text("Data: 03/10/2026 12:30 -0300\n\nAPROVADO\n", encoding="utf-8")
        hora_commit = datetime(2026, 10, 3, 12, 30, tzinfo=BRT)
        result = verificar_veredito(arq, hora_commit=hora_commit, git_cwd=repo)
        assert not result.ok
        assert "Objeto" in result.motivo

    def test_hash_inexistente_rejeita(self, repo_tmp):
        """Veredito com hash inexistente é recusado."""
        repo, objeto_hash = repo_tmp
        arq = repo / "veredito-teste.md"
        _escrever_veredito(arq, "0000000", "03/10/2026 12:30 -0300")
        hora_commit = datetime(2026, 10, 3, 12, 30, tzinfo=BRT)
        result = verificar_veredito(arq, hora_commit=hora_commit, git_cwd=repo)
        assert not result.ok
        assert "não existe" in result.motivo


class TestFuso:
    """Hora com -0300 e sem fuso dão o mesmo resultado."""

    def test_com_fuso_e_sem_fuso_iguais(self, repo_tmp):
        repo, objeto_hash = repo_tmp
        arq1 = repo / "veredito-com-fuso.md"
        arq2 = repo / "veredito-sem-fuso.md"
        _escrever_veredito(arq1, objeto_hash, "03/10/2026 12:10 -0300")
        _escrever_veredito(arq2, objeto_hash, "03/10/2026 12:10")
        hora_commit = datetime(2026, 10, 3, 12, 12, tzinfo=BRT)
        r1 = verificar_veredito(arq1, hora_commit=hora_commit, git_cwd=repo)
        r2 = verificar_veredito(arq2, hora_commit=hora_commit, git_cwd=repo)
        assert r1.ok == r2.ok
        assert r1.ok


class TestEhVeredito:
    """Testa _eh_veredito."""

    def test_veredito_md(self):
        assert _eh_veredito("veredito-w02.md")

    def test_critica_md(self):
        assert _eh_veredito("critica-w08.md")

    def test_tasks_md_nao(self):
        assert not _eh_veredito("tasks.md")

    def test_veredito_sem_md_nao(self):
        assert not _eh_veredito("veredito-w02")

    def test_veredito_com_caminho(self):
        assert _eh_veredito("blocos/A8/veredito-w02.md")
