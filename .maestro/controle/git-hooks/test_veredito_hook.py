"""Testes do hook de veredito (desejo 004).

Cobre os cenários da spec:
- Hora no texto > commit + 2min → recusado
- Hora no texto ≤ commit + 2min → aceito
- Sem hora no texto → aceito (usa hora do commit)
- Veredito anterior ao objeto → recusado
- Sem linha Objeto → recusado
- Hash inexistente → recusado
- Hora com -0300 e sem fuso dão o mesmo resultado
- Formatos reais da onda 0: bold, inglês, ISO+BRT, por extenso, dd/mm/aaaa
- Formato não reconhecido → recusado
- Standalone usa author date do commit, não mtime
- Cherry-pick: author date preservada
"""
from __future__ import annotations

import os
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

# Importa o módulo do hook
import sys
sys.path.insert(0, str(Path(__file__).parent))
from veredito_hook import (
    verificar_veredito,
    _eh_veredito,
    _parse_hora_texto,
    _autor_date_arquivo,
    BRT,
    TOLERANCIA,
    UNRECOGNIZED,
)


def _run(args, cwd):
    r = subprocess.run(args, capture_output=True, text=True, cwd=cwd)
    if r.returncode != 0:
        raise RuntimeError(f"{' '.join(args)}: {r.stderr}")
    return r.stdout.strip()


def _commit_at(repo, msg, date_iso, files=None):
    """Faz um commit com author/committer date definidos."""
    env = dict(
        os.environ,
        GIT_AUTHOR_DATE=date_iso,
        GIT_COMMITTER_DATE=date_iso,
    )
    args = ["git", "commit", "-m", msg]
    if files:
        args += files
    subprocess.run(args, cwd=repo, env=env, capture_output=True, text=True)


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
    _commit_at(repo, "objeto", "2026-10-03T12:00:00-03:00")
    objeto_hash = _run(["git", "rev-parse", "HEAD"], repo)[:7]
    return repo, objeto_hash


def _escrever_veredito(caminho, objeto_hash, hora_texto=None):
    """Escreve um arquivo de veredito de teste."""
    linhas = [f"Objeto: tasks.md @ {objeto_hash}", ""]
    if hora_texto:
        linhas.insert(0, hora_texto)
    caminho.write_text("\n".join(linhas) + "\n", encoding="utf-8")


# ── Testes básicos de hora no texto vs commit ──

class TestVereditoHora:
    """Testes de hora no texto vs commit."""

    def test_hora_texto_maior_que_commit_mais_2min_rejeita(self, repo_tmp):
        repo, objeto_hash = repo_tmp
        arq = repo / "veredito-teste.md"
        _escrever_veredito(arq, objeto_hash, "Data: 03/10/2026 12:50 -0300")
        hora_commit = datetime(2026, 10, 3, 12, 22, tzinfo=BRT)
        result = verificar_veredito(arq, hora_commit=hora_commit, git_cwd=repo)
        assert not result.ok
        assert "posterior ao commit" in result.motivo

    def test_hora_texto_igual_commit_aceita(self, repo_tmp):
        repo, objeto_hash = repo_tmp
        arq = repo / "veredito-teste.md"
        _escrever_veredito(arq, objeto_hash, "Data: 03/10/2026 12:10 -0300")
        hora_commit = datetime(2026, 10, 3, 12, 12, tzinfo=BRT)
        result = verificar_veredito(arq, hora_commit=hora_commit, git_cwd=repo)
        assert result.ok

    def test_hora_texto_dentro_tolerancia_aceita(self, repo_tmp):
        repo, objeto_hash = repo_tmp
        arq = repo / "veredito-teste.md"
        _escrever_veredito(arq, objeto_hash, "Data: 03/10/2026 12:13 -0300")
        hora_commit = datetime(2026, 10, 3, 12, 12, tzinfo=BRT)
        result = verificar_veredito(arq, hora_commit=hora_commit, git_cwd=repo)
        assert result.ok

    def test_hora_texto_exatamente_2min_aceita(self, repo_tmp):
        repo, objeto_hash = repo_tmp
        arq = repo / "veredito-teste.md"
        _escrever_veredito(arq, objeto_hash, "Data: 03/10/2026 12:14 -0300")
        hora_commit = datetime(2026, 10, 3, 12, 12, tzinfo=BRT)
        result = verificar_veredito(arq, hora_commit=hora_commit, git_cwd=repo)
        assert result.ok

    def test_hora_texto_3min_rejeita(self, repo_tmp):
        repo, objeto_hash = repo_tmp
        arq = repo / "veredito-teste.md"
        _escrever_veredito(arq, objeto_hash, "Data: 03/10/2026 12:15 -0300")
        hora_commit = datetime(2026, 10, 3, 12, 12, tzinfo=BRT)
        result = verificar_veredito(arq, hora_commit=hora_commit, git_cwd=repo)
        assert not result.ok


class TestVereditoSemHora:
    """Veredito sem hora no texto."""

    def test_sem_hora_aceita(self, repo_tmp):
        repo, objeto_hash = repo_tmp
        arq = repo / "veredito-teste.md"
        _escrever_veredito(arq, objeto_hash, hora_texto=None)
        hora_commit = datetime(2026, 10, 3, 12, 30, tzinfo=BRT)
        result = verificar_veredito(arq, hora_commit=hora_commit, git_cwd=repo)
        assert result.ok


class TestVereditoAnteriorAoObjeto:
    """Veredito anterior ao objeto criticado."""

    def test_veredito_anterior_ao_objeto_rejeita(self, repo_tmp):
        repo, objeto_hash = repo_tmp
        arq = repo / "veredito-teste.md"
        _escrever_veredito(arq, objeto_hash, "Data: 03/10/2026 11:00 -0300")
        hora_commit = datetime(2026, 10, 3, 11, 0, tzinfo=BRT)
        result = verificar_veredito(arq, hora_commit=hora_commit, git_cwd=repo)
        assert not result.ok
        assert "anterior ao objeto" in result.motivo


class TestVereditoObjeto:
    """Testes da linha Objeto."""

    def test_sem_linha_objeto_rejeita(self, repo_tmp):
        repo, objeto_hash = repo_tmp
        arq = repo / "veredito-teste.md"
        arq.write_text("Data: 03/10/2026 12:30 -0300\n\nAPROVADO\n", encoding="utf-8")
        hora_commit = datetime(2026, 10, 3, 12, 30, tzinfo=BRT)
        result = verificar_veredito(arq, hora_commit=hora_commit, git_cwd=repo)
        assert not result.ok
        assert "Objeto" in result.motivo

    def test_hash_inexistente_rejeita(self, repo_tmp):
        repo, objeto_hash = repo_tmp
        arq = repo / "veredito-teste.md"
        _escrever_veredito(arq, "0000000", "Data: 03/10/2026 12:30 -0300")
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
        _escrever_veredito(arq1, objeto_hash, "Data: 03/10/2026 12:10 -0300")
        _escrever_veredito(arq2, objeto_hash, "Data: 03/10/2026 12:10")
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


# ── Testes dos formatos reais da onda 0 ──

@pytest.fixture
def repo_onda0(tmp_path):
    """Repo com controle total sobre datas de objeto e veredito."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _run(["git", "init"], repo)
    _run(["git", "config", "user.email", "test@test.com"], repo)
    _run(["git", "config", "user.name", "Test"], repo)
    _run(["git", "config", "core.autocrlf", "false"], repo)
    return repo


def _mkobj(repo, date_iso):
    """Cria um commit de objeto e retorna o hash curto."""
    (repo / "tasks.md").write_text(f"tasks {os.getpid()}\n", encoding="utf-8")
    _run(["git", "add", "tasks.md"], repo)
    _commit_at(repo, "obj", date_iso)
    return _run(["git", "rev-parse", "--short", "HEAD"], repo)


def _mkveredito(repo, nome, objeto_hash, texto_data, veredito_date):
    """Cria um veredito commitado e depois toca o arquivo (atualiza mtime)."""
    f = repo / f"veredito-{nome}.md"
    f.write_text(
        f"Objeto: tasks.md @ {objeto_hash}\n{texto_data}\n\nAPPROVE\n",
        encoding="utf-8",
    )
    _run(["git", "add", f.name], repo)
    _commit_at(repo, "v", veredito_date)
    # touch para simular que o arquivo foi editado depois do commit
    f.touch()
    return f


class TestOnda0CasosReais:
    """Os 9 casos reais da onda 0, texto exato dos vereditos."""

    def test_B1_md_ingles_recusa(self, repo_onda0):
        """B1: **Data:** Sat Oct 3 16:00:00 2026, commit 15:00:56 → RECUSA."""
        repo = repo_onda0
        o = _mkobj(repo, "2026-10-03T14:50:00-0300")
        f = _mkveredito(
            repo, "B1_md_ingles", o,
            "**Data:** Sat Oct 3 16:00:00 2026",
            "2026-10-03T15:00:56-0300",
        )
        r = verificar_veredito(f, git_cwd=repo)  # standalone: hora_commit=None
        assert not r.ok
        assert "posterior ao commit" in r.motivo

    def test_B1_plain_recusa(self, repo_onda0):
        """B1: Data: 03/10/2026 16:00 -0300, commit 15:00:56 → RECUSA."""
        repo = repo_onda0
        o = _mkobj(repo, "2026-10-03T14:50:00-0300")
        f = _mkveredito(
            repo, "B1_plain", o,
            "Data: 03/10/2026 16:00 -0300",
            "2026-10-03T15:00:56-0300",
        )
        r = verificar_veredito(f, git_cwd=repo)
        assert not r.ok
        assert "posterior ao commit" in r.motivo

    def test_B4_iso_antes_recusa(self, repo_onda0):
        """B4: **Data:** 2026-10-03 14:04:08 BRT, objeto 14:20 → RECUSA (anterior)."""
        repo = repo_onda0
        o = _mkobj(repo, "2026-10-03T14:20:00-0300")
        f = _mkveredito(
            repo, "B4_iso_antes", o,
            "**Data:** 2026-10-03 14:04:08 BRT (`date`)",
            "2026-10-03T14:30:00-0300",
        )
        r = verificar_veredito(f, git_cwd=repo)
        assert not r.ok
        assert "anterior ao objeto" in r.motivo

    def test_B4_antes_plain_recusa(self, repo_onda0):
        """B4: Data: 14:25, objeto 14:30, commit 14:28 → RECUSA (anterior)."""
        repo = repo_onda0
        o = _mkobj(repo, "2026-10-03T14:30:00-0300")
        f = _mkveredito(
            repo, "B4_antes_plain", o,
            "Data: 03/10/2026 14:25 -0300",
            "2026-10-03T14:28:00-0300",
        )
        r = verificar_veredito(f, git_cwd=repo)
        assert not r.ok
        assert "anterior ao objeto" in r.motivo

    def test_formato_desconhecido_recusa(self, repo_onda0):
        """Data: ontem à tarde → RECUSA (formato não reconhecido)."""
        repo = repo_onda0
        o = _mkobj(repo, "2026-10-03T14:50:00-0300")
        f = _mkveredito(
            repo, "fmt_desc", o,
            "Data: ontem à tarde",
            "2026-10-03T15:02:00-0300",
        )
        r = verificar_veredito(f, git_cwd=repo)
        assert not r.ok
        assert "não reconhecido" in r.motivo

    def test_B7_so_data_aceita(self, repo_onda0):
        """B7: **Data:** 03/10/2026 (só data), commit 15:03 → OK."""
        repo = repo_onda0
        o = _mkobj(repo, "2026-10-03T14:50:00-0300")
        f = _mkveredito(
            repo, "B7_so_data", o,
            "**Data:** 03/10/2026",
            "2026-10-03T15:03:00-0300",
        )
        r = verificar_veredito(f, git_cwd=repo)
        assert r.ok

    def test_normal_aceita(self, repo_onda0):
        """Data: 15:01, commit 15:02 → OK."""
        repo = repo_onda0
        o = _mkobj(repo, "2026-10-03T14:50:00-0300")
        f = _mkveredito(
            repo, "normal", o,
            "Data: 03/10/2026 15:01 -0300",
            "2026-10-03T15:02:00-0300",
        )
        r = verificar_veredito(f, git_cwd=repo)
        assert r.ok

    def test_md_ingles_ok_aceita(self, repo_onda0):
        """**Data:** Sat Oct 3 15:01:30 2026, commit 15:02 → OK."""
        repo = repo_onda0
        o = _mkobj(repo, "2026-10-03T14:50:00-0300")
        f = _mkveredito(
            repo, "md_ingles_ok", o,
            "**Data:** Sat Oct 3 15:01:30 2026",
            "2026-10-03T15:02:00-0300",
        )
        r = verificar_veredito(f, git_cwd=repo)
        assert r.ok

    def test_mtime_vs_commit_recusa(self, repo_onda0):
        """Data: 15:10, commit 15:02, mtime=now → RECUSA (usa commit, não mtime)."""
        repo = repo_onda0
        o = _mkobj(repo, "2026-10-03T14:50:00-0300")
        f = _mkveredito(
            repo, "mtime_vs_commit", o,
            "Data: 03/10/2026 15:10 -0300",
            "2026-10-03T15:02:00-0300",
        )
        r = verificar_veredito(f, git_cwd=repo)
        assert not r.ok
        assert "posterior ao commit" in r.motivo


# ── Testes de parse dos formatos ──

class TestParseFormatos:
    """Testa _parse_hora_texto com cada formato real."""

    def test_bold_ddmmaaaa_hhmm(self):
        s = "**Data:** 03/10/2026 16:00 -0300"
        dt = _parse_hora_texto(s)
        assert dt == datetime(2026, 10, 3, 16, 0, tzinfo=BRT)

    def test_plain_ddmmaaaa_hhmm(self):
        s = "Data: 03/10/2026 16:00 -0300"
        dt = _parse_hora_texto(s)
        assert dt == datetime(2026, 10, 3, 16, 0, tzinfo=BRT)

    def test_bold_ingles(self):
        s = "**Data:** Sat Oct 3 16:00:00 2026"
        dt = _parse_hora_texto(s)
        assert dt == datetime(2026, 10, 3, 16, 0, 0, tzinfo=BRT)

    def test_bold_iso_brt(self):
        s = "**Data:** 2026-10-03 14:04:08 BRT (`date`)"
        dt = _parse_hora_texto(s)
        assert dt == datetime(2026, 10, 3, 14, 4, 8, tzinfo=BRT)

    def test_extenso_pt(self):
        s = "Data: sáb,  3 de out de 2026 13:19:15"
        dt = _parse_hora_texto(s)
        assert dt == datetime(2026, 10, 3, 13, 19, 15, tzinfo=BRT)

    def test_bold_extenso_pt(self):
        s = "**Data:** sáb,  3 de out de 2026 13:19:15"
        dt = _parse_hora_texto(s)
        assert dt == datetime(2026, 10, 3, 13, 19, 15, tzinfo=BRT)

    def test_so_data_retorna_none(self):
        """Data sem hora → None (usa commit)."""
        s = "**Data:** 03/10/2026"
        assert _parse_hora_texto(s) is None

    def test_sem_data_retorna_none(self):
        assert _parse_hora_texto("APPROVE\n") is None

    def test_formato_desconhecido(self):
        s = "Data: ontem à tarde"
        assert _parse_hora_texto(s) == UNRECOGNIZED


# ── Teste do cherry-pick ──

class TestCherryPick:
    """Cherry-pick preserva author date; comparação dá o mesmo resultado."""

    def test_author_date_preservada(self, repo_onda0, tmp_path):
        repo = repo_onda0
        # Objeto
        o = _mkobj(repo, "2026-10-03T14:50:00-0300")
        # Veredito na branch original
        _run(["git", "checkout", "-b", "branch-original"], repo)
        f = _mkveredito(
            repo, "cherry", o,
            "Data: 03/10/2026 15:01 -0300",
            "2026-10-03T15:02:00-0300",
        )
        # Author date na branch original
        ad_orig = _autor_date_arquivo(f, repo)
        # Cherry-pick para nova branch
        _run(["git", "checkout", "master"], repo)
        _run(["git", "checkout", "-b", "branch-consolidada"], repo)
        _run(["git", "cherry-pick", "branch-original"], repo)
        f2 = repo / f.name
        ad_cherry = _autor_date_arquivo(f2, repo)
        # Author date tem de ser igual
        assert ad_orig == ad_cherry
        # Veredito dá o mesmo resultado nas duas branches
        _run(["git", "checkout", "branch-original"], repo)
        r_orig = verificar_veredito(f, git_cwd=repo)
        _run(["git", "checkout", "branch-consolidada"], repo)
        r_cherry = verificar_veredito(f2, git_cwd=repo)
        assert r_orig.ok == r_cherry.ok
        assert r_orig.ok  # deve ser aceito
