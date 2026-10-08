"""T2-05/T2-06: modelos de texto são seguros e gate→etapa (FR-008).

P2-AC2: nenhum texto contém hash, W01-W13, runner2, VM, barra,
APPROVE, REPROVE ou caminho de arquivo.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from entrada import etapas  # noqa: E402


class TestGateParaEtapa(unittest.TestCase):
    """FR-008: mapa gate → etapa do cliente."""

    def test_abertura_recebido(self):
        self.assertEqual(etapas.etapa("abertura"), "recebido")

    def test_g0_recebido(self):
        self.assertEqual(etapas.etapa("G0"), "recebido")

    def test_gd_em_analise(self):
        self.assertEqual(etapas.etapa("GD"), "em_analise")

    def test_g1_em_analise(self):
        self.assertEqual(etapas.etapa("G1"), "em_analise")

    def test_g2_em_desenvolvimento(self):
        self.assertEqual(etapas.etapa("G2"), "em_desenvolvimento")

    def test_g3_em_desenvolvimento(self):
        self.assertEqual(etapas.etapa("G3"), "em_desenvolvimento")

    def test_g4_em_testes(self):
        self.assertEqual(etapas.etapa("G4"), "em_testes")

    def test_g5_em_testes(self):
        self.assertEqual(etapas.etapa("G5"), "em_testes")

    def test_g6_em_testes(self):
        self.assertEqual(etapas.etapa("G6"), "em_testes")

    def test_g7_suas_validacao(self):
        self.assertEqual(etapas.etapa("G7"), "suas_validacao")

    def test_g8_publicado(self):
        self.assertEqual(etapas.etapa("G8"), "publicado")

    def test_g9_publicado(self):
        self.assertEqual(etapas.etapa("G9"), "publicado")

    def test_gate_desconhecido_recebe_default(self):
        self.assertEqual(etapas.etapa("XYZ"), "recebido")


class TestEtapaNumero(unittest.TestCase):
    """As 6 etapas são numeradas 1-6."""

    def test_numeros_1_a_6(self):
        self.assertEqual(etapas.numero("recebido"), 1)
        self.assertEqual(etapas.numero("em_analise"), 2)
        self.assertEqual(etapas.numero("em_desenvolvimento"), 3)
        self.assertEqual(etapas.numero("em_testes"), 4)
        self.assertEqual(etapas.numero("suas_validacao"), 5)
        self.assertEqual(etapas.numero("publicado"), 6)


class TestTextosSeguros(unittest.TestCase):
    """P2-AC2: nenhum texto de etapa contém padrão proibido."""

    def test_todos_textos_de_etapa_sao_seguros(self):
        for etapa_id, tpl in etapas.TEXTOS.items():
            msg = tpl.format(nnn="042")
            self.assertTrue(
                etapas.texto_e_seguro(msg),
                f"Texto da etapa '{etapa_id}' não é seguro: {msg!r}",
            )

    def test_todos_textos_de_excecao_sao_seguros(self):
        msg_ag = etapas.TEXTOS_EXCECAO["aguardando_informacao"].format(nnn="042")
        self.assertTrue(etapas.texto_e_seguro(msg_ag), f"Texto exceção aguardando_informacao não é seguro: {msg_ag!r}")

        msg_na = etapas.TEXTOS_EXCECAO["nao_aprovado"].format(nnn="042", motivo="Falta evidência")
        self.assertTrue(etapas.texto_e_seguro(msg_na), f"Texto exceção nao_aprovado não é seguro: {msg_na!r}")

        msg_re = etapas.TEXTOS_EXCECAO["recuo"].format(nnn="042", mensagem=etapas.RECUO_PADRAO)
        self.assertTrue(etapas.texto_e_seguro(msg_re), f"Texto exceção recuo não é seguro: {msg_re!r}")

    def test_texto_recuo_padrao_e_seguro(self):
        self.assertTrue(etapas.texto_e_seguro(etapas.RECUO_PADRAO))

    def test_hash_e_proibido(self):
        self.assertFalse(etapas.texto_e_seguro("Commit a1b2c3d4 feito"))

    def test_worker_e_proibido(self):
        self.assertFalse(etapas.texto_e_seguro("Aprovado por W01"))

    def test_runner2_e_proibido(self):
        self.assertFalse(etapas.texto_e_seguro("Testou no runner2"))

    def test_vm_e_proibido(self):
        self.assertFalse(etapas.texto_e_seguro("Na VM 202"))

    def test_barra_e_proibido(self):
        self.assertFalse(etapas.texto_e_seguro("Barra v2 passou"))

    def test_approve_e_proibido(self):
        self.assertFalse(etapas.texto_e_seguro("APPROVE do gate"))

    def test_caminho_e_proibido(self):
        self.assertFalse(etapas.texto_e_seguro("Arquivo em src/torre/domain"))


class TestRecuo(unittest.TestCase):
    """T2-07/T2-08: detecção de recuo entre etapas."""

    def test_recuo_g6_para_g3(self):
        # G6 = em_testes (4), G3 = em_desenvolvimento (3)
        self.assertTrue(etapas.recuo("em_testes", "em_desenvolvimento"))

    def test_avanco_nao_e_recuo(self):
        self.assertFalse(etapas.recuo("em_analise", "em_desenvolvimento"))

    def test_mesma_etapa_nao_e_recuo(self):
        self.assertFalse(etapas.recuo("em_testes", "em_testes"))

    def test_recuo_publicado_para_recebido(self):
        self.assertTrue(etapas.recuo("publicado", "recebido"))


class TestTextoMontagem(unittest.TestCase):
    """texto() substitui {nnn} e kwargs."""

    def test_texto_etapa(self):
        msg = etapas.texto("recebido", "042")
        self.assertIn("#042", msg)
        self.assertIn("Etapa 1 de 6", msg)

    def test_texto_excecao_com_motivo(self):
        msg = etapas.texto("nao_aprovado", "042", motivo="Falta evidência")
        self.assertIn("#042", msg)
        self.assertIn("Falta evidência", msg)

    def test_texto_excecao_recuo_com_mensagem(self):
        msg = etapas.texto("recuo", "042", mensagem="Voltou para análise")
        self.assertIn("#042", msg)
        self.assertIn("Voltou para análise", msg)


if __name__ == "__main__":
    unittest.main()
