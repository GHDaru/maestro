"""NFR-010, NFR-011, NFR-012: requisitos não-funcionais do P2.

- NFR-010/SC-006: dados/ no .gitignore
- NFR-011/SC-007: logs só metadados (sem telefone/texto)
- NFR-012: falhou avisa à Office
"""
import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from entrada import saida  # noqa: E402


class TestDadosGitignore(unittest.TestCase):
    """NFR-010, SC-006: dados/ ignorado pelo git."""

    def test_dados_no_gitignore(self):
        repo = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        result = subprocess.run(
            ["git", "check-ignore", "dados/"],
            cwd=repo, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, f"dados/ não está no .gitignore: {result.stderr}")


class TestLogSoMetadados(unittest.TestCase):
    """NFR-011, SC-007: logs só metadados (sem telefone/texto)."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="entrada-log-")
        self.dados_dir = self._tmp

    def tearDown(self):
        import shutil
        shutil.rmtree(self._tmp, ignore_errors=True)

    def test_log_nao_tem_coluna_contato(self):
        """A tabela log_envio não tem coluna 'contato' (telefone)."""
        import sqlite3
        conn = sqlite3.connect(os.path.join(self.dados_dir, "entrada.db"))
        saida._SCHEMA  # garante que o módulo está carregado
        conn.executescript(saida._SCHEMA)
        cols = [r[1] for r in conn.execute("PRAGMA table_info(log_envio)").fetchall()]
        conn.close()
        self.assertNotIn("contato", cols, "log_envio tem coluna 'contato' (telefone)")
        self.assertNotIn("texto", cols, "log_envio tem coluna 'texto' (mensagem)")

    def test_log_registra_metadados(self):
        """Envio falhado registra log com metadados."""
        saida.enfileirar(self.dados_dir, "068", "5599999999999", "Olá cliente", "recebido")
        msg = saida.pendentes(self.dados_dir)[0]
        saida.enviar(self.dados_dir, msg, "http://localhost:1/invalid", "segredo")

        logs = saida.log_envio_todos(self.dados_dir)
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]["chamado"], "068")
        self.assertEqual(logs[0]["etapa"], "recebido")
        self.assertIn("status", logs[0])
        self.assertIn("timestamp", logs[0])
        self.assertIn("evento_id", logs[0])


class TestFalhouAvisaOffice(unittest.TestCase):
    """NFR-012: quando status='falhou', alerta à Office é criado."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="entrada-falha-")
        self.dados_dir = self._tmp

    def tearDown(self):
        import shutil
        shutil.rmtree(self._tmp, ignore_errors=True)

    def test_falhou_cria_alerta(self):
        """Forçar falha definitiva e verificar alerta na tabela alertas_office."""
        import sqlite3
        # Enfileira e força MAX_TENTATIVAS falhas.
        mid = saida.enfileirar(self.dados_dir, "068", "5599", "Olá", "recebido")

        db_path = os.path.join(self.dados_dir, "entrada.db")
        for _ in range(saida.MAX_TENTATIVAS):
            msg = saida.pendentes(self.dados_dir)
            if not msg:
                break
            saida.enviar(self.dados_dir, msg[0], "http://localhost:1/invalid", "segredo")
            # Forçar proxima_tentativa para o passado para a próxima iteração.
            conn = sqlite3.connect(db_path)
            conn.execute("UPDATE saida SET proxima_tentativa = '2000-01-01T00:00:00+00:00' WHERE status = 'pendente'")
            conn.commit()
            conn.close()

        alertas = saida.alertas_nao_lidos(self.dados_dir)
        self.assertGreater(len(alertas), 0, "Nenhum alerta à Office criado após falha definitiva")
        self.assertEqual(alertas[0]["chamado"], "068")


if __name__ == "__main__":
    unittest.main()
