"""Teste do processador: servidor -> conversa -> repositorio (T1-05).

Roda com: python -m painel.entrada.test_processador
"""

from __future__ import annotations

import json
import shutil
import sqlite3
import subprocess
import tempfile
import time
import unittest
from pathlib import Path

from painel.entrada.banco import inicializar
from painel.entrada.processador import processar_mensagem


def _git_init(repo: Path) -> None:
    subprocess.run(["git", "init"], cwd=str(repo), capture_output=True, check=True)
    subprocess.run(
        ["git", "config", "user.email", "teste@teste.com"],
        cwd=str(repo), capture_output=True, check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Teste"],
        cwd=str(repo), capture_output=True, check=True,
    )


class TestProcessador(unittest.TestCase):
    def setUp(self) -> None:
        self._dir = tempfile.mkdtemp()
        self.db_path = Path(self._dir) / "entrada.db"
        self.repo_chamados = Path(self._dir) / "chamados"
        self.repo_hindiana = Path(self._dir) / "hindiana"
        self.repo_chamados.mkdir()
        self.repo_hindiana.mkdir()
        (self.repo_hindiana / "specs").mkdir()
        _git_init(self.repo_chamados)
        (self.repo_chamados / ".gitkeep").write_text("")
        subprocess.run(["git", "add", ".gitkeep"], cwd=str(self.repo_chamados),
                       capture_output=True, check=True)
        subprocess.run(["git", "commit", "-m", "init"], cwd=str(self.repo_chamados),
                       capture_output=True, check=True)
        inicializar(self.db_path)

    def tearDown(self) -> None:
        shutil.rmtree(self._dir, ignore_errors=True)

    def _processar(self, mensagem: str) -> tuple[str, str | None]:
        resposta, numero, thread = processar_mensagem(
            contato="c-0001",
            nome="Mauricio",
            empresa="Neogrid",
            mensagem=mensagem,
            db_path=self.db_path,
            repo_chamados=self.repo_chamados,
            repo_hindiana_specs=self.repo_hindiana / "specs",
        )
        if thread:
            thread.join(timeout=30)
        return resposta, numero

    def test_oi_devolve_menu(self) -> None:
        resposta, numero = self._processar("oi")
        self.assertIn("Bug", resposta)
        self.assertIn("Melhoria", resposta)
        self.assertIsNone(numero)

    def test_estado_salvo_no_banco(self) -> None:
        self._processar("oi")
        conn = sqlite3.connect(str(self.db_path))
        row = conn.execute(
            "SELECT estado FROM conversas WHERE contato = ?", ("c-0001",)
        ).fetchone()
        conn.close()
        self.assertIsNotNone(row)
        self.assertEqual(row[0], "menu")

    def test_fluxo_bug_completo_cria_chamado(self) -> None:
        resp1, _ = self._processar("oi")
        self.assertIn("Bug", resp1)

        resp2, _ = self._processar("1")
        self.assertIn("aconteceu", resp2.lower())

        resp3, _ = self._processar("tela trava ao salvar")
        resp4, _ = self._processar("Ficha > Salvar")
        resp5, _ = self._processar("1. Abri 2. Cliquei")
        resp6, _ = self._processar("Esperava salvar mas deu erro")
        resp7, _ = self._processar("pular")

        resp8, numero = self._processar("sim")
        self.assertIsNotNone(numero)
        self.assertIn(f"#{numero}", resp8)

        # O chamado foi criado no repo
        chamados = list(self.repo_chamados.glob(f"{numero}-*"))
        self.assertTrue(chamados, f"Chamado {numero} nao encontrado no repo")
        pasta = chamados[0]
        self.assertTrue((pasta / "00-chamado.md").exists())
        self.assertTrue((pasta / "conversa.md").exists())
        self.assertTrue((pasta / "evidencias").is_dir())

    def test_resposta_em_menos_de_2s(self) -> None:
        inicio = time.monotonic()
        self._processar("oi")
        elapsed = time.monotonic() - inicio
        self.assertLess(elapsed, 2.0)

    def test_cancelar_salva_estado(self) -> None:
        self._processar("oi")
        self._processar("1")
        resposta, _ = self._processar("cancelar")
        conn = sqlite3.connect(str(self.db_path))
        row = conn.execute(
            "SELECT estado FROM conversas WHERE contato = ?", ("c-0001",)
        ).fetchone()
        conn.close()
        self.assertEqual(row[0], "cancelado")

    def test_chamado_md_sem_telefone(self) -> None:
        self._processar("oi")
        self._processar("1")
        self._processar("tela trava")
        self._processar("Ficha")
        self._processar("passos")
        self._processar("esperado")
        self._processar("pular")
        _, numero = self._processar("sim")

        chamados = list(self.repo_chamados.glob(f"{numero}-*"))
        conteudo = (chamados[0] / "00-chamado.md").read_text(encoding="utf-8")
        self.assertNotIn("telefone", conteudo.lower())
        self.assertNotIn("55119", conteudo)


if __name__ == "__main__":
    unittest.main()
