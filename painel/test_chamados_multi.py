"""Teste do chamados.py multi-repo (T1-06).

Testa que le_chamados() le de repos com pasta="" (repo chamados)
e resolve hashes cross-repo (chamado no repo chamados referenciando
hash do hindiana).

Roda com: python -m painel.test_chamados_multi
"""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

# Importa do diretorio painel/
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))

from chamados import le_chamados, confere, _git


def _git_init(repo: Path) -> None:
    subprocess.run(["git", "init"], cwd=str(repo), capture_output=True, check=True)
    subprocess.run(["git", "config", "user.email", "teste@teste.com"],
                   cwd=str(repo), capture_output=True, check=True)
    subprocess.run(["git", "config", "user.name", "Teste"],
                   cwd=str(repo), capture_output=True, check=True)


def _commit(repo: Path, msg: str = "commit") -> str:
    subprocess.run(["git", "add", "-A"], cwd=str(repo), capture_output=True, check=True)
    subprocess.run(["git", "commit", "-m", msg], cwd=str(repo), capture_output=True, check=True)
    r = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(repo),
                       capture_output=True, text=True, check=True)
    return r.stdout.strip()


class TestChamadosMultiRepo(unittest.TestCase):
    def setUp(self) -> None:
        self._dir = tempfile.mkdtemp()
        self.raiz = Path(self._dir)
        self.chamados = self.raiz / "chamados"
        self.hindiana = self.raiz / "hindiana"
        self.chamados.mkdir()
        self.hindiana.mkdir()
        (self.hindiana / "specs").mkdir()
        _git_init(self.chamados)
        _git_init(self.hindiana)

    def tearDown(self) -> None:
        shutil.rmtree(self._dir, ignore_errors=True)

    def _criar_chamado_simples(self, repo: Path, cid: str, pasta: str = "") -> None:
        """Cria um chamado minimo no repo."""
        base = repo / pasta / cid if pasta else repo / cid
        base.mkdir(parents=True, exist_ok=True)
        (base / "00-chamado.md").write_text(
            "---\n"
            "gate: abertura\n"
            "tipo: bug\n"
            "aberto_por: Mauricio\n"
            "empresa: Neogrid\n"
            "contato: c-0001\n"
            "origem: whatsapp\n"
            "data: 2026-10-08 14:00 -0300\n"
            "---\n"
            "# Teste\n",
            encoding="utf-8",
        )

    def test_le_chamados_de_repo_com_pasta_vazia(self) -> None:
        """le_chamados() le do repo chamados com pasta=''."""
        self._criar_chamado_simples(self.chamados, "001-teste-bug")
        _commit(self.chamados, "chamado 001")

        cfg = {
            "raiz": str(self.raiz),
            "chamados": [
                {"repo": "chamados", "dias": 14, "pasta": ""},
            ],
        }
        resultado = le_chamados(cfg)
        ids = [c["id"] for c in resultado["chamados"]]
        self.assertIn("001-teste-bug", ids)

    def test_le_chamados_de_dois_repos(self) -> None:
        """le_chamados() le de chamados + hindiana."""
        self._criar_chamado_simples(self.chamados, "001-teste-bug")
        _commit(self.chamados, "chamado 001")
        self._criar_chamado_simples(self.hindiana, "097-outro-chamado", pasta="specs")
        _commit(self.hindiana, "chamado 097")

        cfg = {
            "raiz": str(self.raiz),
            "chamados": [
                {"repo": "chamados", "dias": 14, "pasta": ""},
                {"repo": "hindiana", "dias": 14, "pasta": "specs"},
            ],
        }
        resultado = le_chamados(cfg)
        ids = [c["id"] for c in resultado["chamados"]]
        self.assertIn("001-teste-bug", ids)
        self.assertIn("097-outro-chamado", ids)

    def test_hash_resolvido_cross_repo(self) -> None:
        """Um chamado no repo chamados referencia hash do hindiana."""
        # Cria um commit no hindiana para ter um hash
        (self.hindiana / "arquivo.txt").write_text("conteudo", encoding="utf-8")
        hash_hind = _commit(self.hindiana, "arquivo")
        hash_curto = hash_hind[:7]

        # Cria um chamado no repo chamados com G1 que referencia o hash do hindiana
        cid = "001-teste-bug"
        base = self.chamados / cid
        base.mkdir()
        (base / "00-chamado.md").write_text(
            "---\n"
            "gate: abertura\n"
            "tipo: bug\n"
            "aberto_por: Mauricio\n"
            "empresa: Neogrid\n"
            "contato: c-0001\n"
            "origem: whatsapp\n"
            "data: 2026-10-08 14:00 -0300\n"
            "---\n"
            "# Teste\n",
            encoding="utf-8",
        )
        (base / "spec.md").write_text("# Spec\n", encoding="utf-8")
        (base / f"G1-spec-Tester.md").write_text(
            "---\n"
            "gate: G1\n"
            "objeto: spec.md @ " + hash_curto + "\n"
            "veredito: APPROVE\n"
            "por: Tester\n"
            "data: 2026-10-08 14:05 -0300\n"
            "---\n",
            encoding="utf-8",
        )
        _commit(self.chamados, "chamado 001")

        cfg = {
            "raiz": str(self.raiz),
            "chamados": [
                {"repo": "chamados", "dias": 14, "pasta": ""},
                {"repo": "hindiana", "dias": 14, "pasta": "specs"},
            ],
        }
        resultado = le_chamados(cfg)
        chamado = next(c for c in resultado["chamados"] if c["id"] == cid)
        # O G1 deve ter sido conferido; se o hash nao resolvesse, teria erro.
        g1 = next(g for g in chamado["gates"] if g["gate"] == "G1")
        # O hash foi resolvido cross-repo (sem erro de hash inexistente)
        for item in g1["itens"]:
            self.assertFalse(
                any("nao existe" in e for e in item["erros"]),
                f"Hash nao resolvido cross-repo: {item['erros']}",
            )


if __name__ == "__main__":
    unittest.main()
