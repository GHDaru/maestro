"""Teste vermelho de repositorio.cria() (T1-03).

Testa num repo git temporario:
- numero = max(chamados, hindiana/specs) + 1
- slug de 2 a 4 palavras em kebab-case
- 00-chamado.md com contato e SEM telefone
- commit com trailers Chamado: e Sessao:
- conversa.md e evidencias/ criados

Roda com: python -m painel.entrada.test_repositorio
"""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from painel.entrada.repositorio import cria


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


def _git_log_trailers(repo: Path) -> str:
    result = subprocess.run(
        ["git", "log", "-1", "--format=%B"],
        cwd=str(repo), capture_output=True, text=True, check=True,
    )
    return result.stdout


class TestRepositorioCria(unittest.TestCase):
    def setUp(self) -> None:
        self._dir = tempfile.mkdtemp()
        self.repo_chamados = Path(self._dir) / "chamados"
        self.repo_hindiana = Path(self._dir) / "hindiana"
        self.repo_chamados.mkdir()
        self.repo_hindiana.mkdir()
        (self.repo_hindiana / "specs").mkdir()
        _git_init(self.repo_chamados)
        # commit inicial vazio
        (self.repo_chamados / ".gitkeep").write_text("")
        subprocess.run(
            ["git", "add", ".gitkeep"],
            cwd=str(self.repo_chamados), capture_output=True, check=True,
        )
        subprocess.run(
            ["git", "commit", "-m", "init"],
            cwd=str(self.repo_chamados), capture_output=True, check=True,
        )

    def tearDown(self) -> None:
        import shutil
        try:
            shutil.rmtree(self._dir, ignore_errors=True)
        except OSError:
            pass

    def _dados_bug(self) -> dict:
        return {
            "tipo": "bug",
            "descricao": "tela trava ao salvar",
            "onde": "Ficha > Salvar",
            "passos": "1. Abri 2. Cliquei",
            "esperado": "salvar mas deu erro",
            "anexos": [],
        }

    def test_numero_primeiro_chamado(self) -> None:
        resultado = cria(
            repo_chamados=self.repo_chamados,
            repo_hindiana_specs=self.repo_hindiana / "specs",
            dados=self._dados_bug(),
            contato="c-0001",
            nome="Mauricio",
            empresa="Neogrid",
        )
        self.assertEqual(resultado["numero"], "001")

    def test_numero_max_mais_um(self) -> None:
        # Cria chamado 097 no hindiana/specs
        (self.repo_hindiana / "specs" / "097-marco-trava-pos-t3").mkdir()
        resultado = cria(
            repo_chamados=self.repo_chamados,
            repo_hindiana_specs=self.repo_hindiana / "specs",
            dados=self._dados_bug(),
            contato="c-0001",
            nome="Mauricio",
            empresa="Neogrid",
        )
        self.assertEqual(resultado["numero"], "098")

    def test_numero_max_entre_repos(self) -> None:
        # 097 no hindiana, 100 no chamados
        (self.repo_hindiana / "specs" / "097-outro-chamado").mkdir()
        (self.repo_chamados / "100-terceiro-chamado").mkdir()
        subprocess.run(
            ["git", "add", "-A"],
            cwd=str(self.repo_chamados), capture_output=True, check=True,
        )
        subprocess.run(
            ["git", "commit", "-m", "100"],
            cwd=str(self.repo_chamados), capture_output=True, check=True,
        )
        resultado = cria(
            repo_chamados=self.repo_chamados,
            repo_hindiana_specs=self.repo_hindiana / "specs",
            dados=self._dados_bug(),
            contato="c-0001",
            nome="Mauricio",
            empresa="Neogrid",
        )
        self.assertEqual(resultado["numero"], "101")

    def test_slug_2_a_4_palavras(self) -> None:
        resultado = cria(
            repo_chamados=self.repo_chamados,
            repo_hindiana_specs=self.repo_hindiana / "specs",
            dados=self._dados_bug(),
            contato="c-0001",
            nome="Mauricio",
            empresa="Neogrid",
        )
        slug = resultado["slug"]
        palavras = slug.split("-")
        self.assertGreaterEqual(len(palavras), 2)
        self.assertLessEqual(len(palavras), 4)

    def test_chamado_md_com_contato_sem_telefone(self) -> None:
        resultado = cria(
            repo_chamados=self.repo_chamados,
            repo_hindiana_specs=self.repo_hindiana / "specs",
            dados=self._dados_bug(),
            contato="c-0001",
            nome="Mauricio",
            empresa="Neogrid",
        )
        chamado_md = resultado["pasta"] / "00-chamado.md"
        conteudo = chamado_md.read_text(encoding="utf-8")
        self.assertIn("contato: c-0001", conteudo)
        self.assertNotIn("telefone", conteudo.lower())
        self.assertNotIn("55119", conteudo)  # nenhum numero de telefone

    def test_chamado_md_campos_obrigatorios(self) -> None:
        resultado = cria(
            repo_chamados=self.repo_chamados,
            repo_hindiana_specs=self.repo_hindiana / "specs",
            dados=self._dados_bug(),
            contato="c-0001",
            nome="Mauricio",
            empresa="Neogrid",
        )
        conteudo = (resultado["pasta"] / "00-chamado.md").read_text(encoding="utf-8")
        self.assertIn("gate: abertura", conteudo)
        self.assertIn("tipo: bug", conteudo)
        self.assertIn("aberto_por: Mauricio", conteudo)
        self.assertIn("empresa: Neogrid", conteudo)
        self.assertIn("origem: whatsapp", conteudo)

    def test_conversa_md_e_evidencias_criados(self) -> None:
        resultado = cria(
            repo_chamados=self.repo_chamados,
            repo_hindiana_specs=self.repo_hindiana / "specs",
            dados=self._dados_bug(),
            contato="c-0001",
            nome="Mauricio",
            empresa="Neogrid",
        )
        self.assertTrue((resultado["pasta"] / "conversa.md").exists())
        self.assertTrue((resultado["pasta"] / "evidencias").is_dir())

    def test_commit_com_trailers(self) -> None:
        cria(
            repo_chamados=self.repo_chamados,
            repo_hindiana_specs=self.repo_hindiana / "specs",
            dados=self._dados_bug(),
            contato="c-0001",
            nome="Mauricio",
            empresa="Neogrid",
        )
        log = _git_log_trailers(self.repo_chamados)
        self.assertIn("Chamado:", log)
        self.assertIn("Sessao: entrada", log)

    def test_conteudo_cliente_e_dado(self) -> None:
        """NFR-007: conteudo do cliente leva aviso de dado."""
        resultado = cria(
            repo_chamados=self.repo_chamados,
            repo_hindiana_specs=self.repo_hindiana / "specs",
            dados=self._dados_bug(),
            contato="c-0001",
            nome="Mauricio",
            empresa="Neogrid",
        )
        conteudo = (resultado["pasta"] / "00-chamado.md").read_text(encoding="utf-8")
        self.assertIn("Conteudo enviado pelo cliente", conteudo)


if __name__ == "__main__":
    unittest.main()
