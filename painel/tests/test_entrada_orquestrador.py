"""T2-01/T2-02: orquestrador do ciclo de notificação (P2).

Cobre: primeira notificação, avanço de etapa, mesma etapa (não enfileira),
recuo G6→G3 com mensagem_cliente.
"""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from entrada import orquestrador  # noqa: E402
from entrada import saida  # noqa: E402


class TestCiclo(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="entrada-test-")
        self.dados_dir = self._tmp

    def tearDown(self):
        import shutil
        shutil.rmtree(self._tmp, ignore_errors=True)

    def _chamado(self, chamado="068", gate="G0", contato="5599999999999", numero="068", **extra):
        ch = {"chamado": chamado, "onde": gate, "contato": contato, "numero": numero}
        ch.update(extra)
        return ch

    def test_primeira_notificacao_enfileira(self):
        """T2-01: primeira vez enfileira mensagem da etapa atual."""
        chamados = [self._chamado(gate="G0")]
        res = orquestrador.ciclo(self.dados_dir, chamados)
        self.assertEqual(len(res["enfileirados"]), 1)
        self.assertEqual(len(res["recuos"]), 0)

        # A mensagem enfileirada é da etapa "recebido".
        msgs = saida.pendentes(self.dados_dir)
        self.assertEqual(len(msgs), 1)
        self.assertIn("#068", msgs[0]["texto"])
        self.assertIn("Etapa 1 de 6", msgs[0]["texto"])

    def test_mesma_etapa_nao_enfileira(self):
        """T2-01: segunda vez na mesma etapa não enfileira."""
        ch = [self._chamado(gate="G1")]
        orquestrador.ciclo(self.dados_dir, ch)
        ch = [self._chamado(gate="G1")]
        res = orquestrador.ciclo(self.dados_dir, ch)
        self.assertEqual(len(res["enfileirados"]), 0)
        self.assertEqual(len(res["recuos"]), 0)

    def test_avanco_enfileira(self):
        """T2-01: avanço de etapa enfileira nova mensagem."""
        ch = [self._chamado(gate="G1")]
        orquestrador.ciclo(self.dados_dir, ch)

        ch = [self._chamado(gate="G2")]
        res = orquestrador.ciclo(self.dados_dir, ch)
        self.assertEqual(len(res["enfileirados"]), 1)
        self.assertEqual(len(res["recuos"]), 0)

        msgs = saida.pendentes(self.dados_dir)
        # 2 mensagens: etapa 2 e etapa 3.
        self.assertEqual(len(msgs), 2)
        self.assertIn("Etapa 3 de 6", msgs[1]["texto"])

    def test_recuo_g6_para_g3_enfileira_recuo(self):
        """T2-07: recuo G6→G3 enfileira mensagem de recuo."""
        ch = [self._chamado(gate="G6")]
        orquestrador.ciclo(self.dados_dir, ch)

        ch = [self._chamado(gate="G3")]
        res = orquestrador.ciclo(self.dados_dir, ch)
        self.assertEqual(len(res["recuos"]), 1)
        self.assertEqual(len(res["enfileirados"]), 0)

        msgs = saida.pendentes(self.dados_dir)
        # 2 mensagens: etapa 4 (em_testes) + recuo.
        self.assertEqual(len(msgs), 2)
        self.assertIn("Voltou para ajuste", msgs[1]["texto"])

    def test_recuo_com_mensagem_cliente(self):
        """T2-08: recuo usa mensagem_cliente do chamado."""
        ch = [self._chamado(gate="G5")]
        orquestrador.ciclo(self.dados_dir, ch)

        ch = [self._chamado(gate="G2", mensagem_cliente="Bug encontrado nos testes")]
        res = orquestrador.ciclo(self.dados_dir, ch)
        self.assertEqual(len(res["recuos"]), 1)

        msgs = saida.pendentes(self.dados_dir)
        self.assertIn("Bug encontrado nos testes", msgs[1]["texto"])

    def test_sem_contato_nao_enfileira(self):
        """Sem contato de teste, não enfileira mas registra etapa."""
        ch = [self._chamado(gate="G0", contato="")]
        res = orquestrador.ciclo(self.dados_dir, ch)
        self.assertEqual(len(res["enfileirados"]), 0)

    def test_gate_vazio_ignorado(self):
        """Chamado sem gate atual é ignorado."""
        ch = [self._chamado(gate="")]
        res = orquestrador.ciclo(self.dados_dir, ch)
        self.assertEqual(len(res["enfileirados"]), 0)
        self.assertEqual(len(res["recuos"]), 0)

    def test_texto_inseguro_nao_enfileira(self):
        """Se mensagem_cliente contém padrão proibido, não enfileira."""
        ch = [self._chamado(gate="G6")]
        orquestrador.ciclo(self.dados_dir, ch)

        ch = [self._chamado(gate="G3", mensagem_cliente="Ver commit a1b2c3d4")]
        res = orquestrador.ciclo(self.dados_dir, ch)
        # Recuo detectado mas texto inseguro → não enfileira.
        self.assertEqual(len(res["recuos"]), 0)


class TestSaidaFila(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.mkdtemp(prefix="entrada-saida-")
        self.dados_dir = self._tmp

    def tearDown(self):
        import shutil
        shutil.rmtree(self._tmp, ignore_errors=True)

    def test_enfileirar_e_pendentes(self):
        mid = saida.enfileirar(self.dados_dir, "068", "5599", "Olá", "recebido")
        self.assertGreater(mid, 0)
        msgs = saida.pendentes(self.dados_dir)
        self.assertEqual(len(msgs), 1)
        self.assertEqual(msgs[0]["texto"], "Olá")

    def test_enviar_falha_sem_webhook(self):
        """Envio para URL inalcançável marca como falha e agenda retry."""
        mid = saida.enfileirar(self.dados_dir, "068", "5599", "Olá", "recebido")
        msg = saida.pendentes(self.dados_dir)[0]
        ok = saida.enviar(self.dados_dir, msg, "http://localhost:1/invalid", "segredo")
        self.assertFalse(ok)
        # Ainda pendente (retry agendado).
        conn = __import__("sqlite3").connect(os.path.join(self.dados_dir, "entrada.db"))
        row = conn.execute("SELECT status, tentativas FROM saida WHERE id = ?", (mid,)).fetchone()
        conn.close()
        self.assertEqual(row[0], "pendente")
        self.assertEqual(row[1], 1)


if __name__ == "__main__":
    unittest.main()
