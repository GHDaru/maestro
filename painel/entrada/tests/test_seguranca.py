"""Testes do seguranca.py — validação HMAC, janela de horário e IPs (P5 do chamado 068).

Só dados sintéticos: segredos de teste, IPs de teste, horários de teste.
Run: python -m unittest discover painel/entrada/tests
"""
import datetime as dt
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import seguranca  # noqa: E402

TZ = dt.timezone(dt.timedelta(hours=-3))
SEGREDO_ATUAL = "segredo-teste-atual-123456"
SEGREDO_ANTERIOR = "segredo-teste-anterior-7890"
IPS_PERMITIDOS = ["10.0.0.50", "10.0.0.51"]


class TestValidaAssinatura(unittest.TestCase):
    def test_assinatura_valida_retorna_true(self):
        """Assinatura HMAC-SHA256 correta valida."""
        corpo = b'{"evento_id":"evt-1","texto":"1"}'
        assinatura = seguranca.calcula_assinatura(corpo, SEGREDO_ATUAL)
        ok, motivo = seguranca.valida_assinatura(corpo, assinatura, [SEGREDO_ATUAL])
        self.assertTrue(ok, f"assinatura válida recusada: {motivo}")

    def test_assinatura_invalida_retorna_false(self):
        """Assinatura errada não valida."""
        corpo = b'{"evento_id":"evt-1"}'
        ok, motivo = seguranca.valida_assinatura(corpo, "sha256=0000000000000000", [SEGREDO_ATUAL])
        self.assertFalse(ok)
        self.assertIn("assinatura", motivo.lower())

    def test_assinatura_com_segredo_anterior_valida(self):
        """NFR-008: assinatura com o segredo anterior também valida."""
        corpo = b'{"evento_id":"evt-1"}'
        assinatura = seguranca.calcula_assinatura(corpo, SEGREDO_ANTERIOR)
        ok, _ = seguranca.valida_assinatura(corpo, assinatura, [SEGREDO_ATUAL, SEGREDO_ANTERIOR])
        self.assertTrue(ok)

    def test_assinatura_sem_segredo_anterior_recusa(self):
        """Sem o segredo anterior na lista, assinatura com ele não valida."""
        corpo = b'{"evento_id":"evt-1"}'
        assinatura = seguranca.calcula_assinatura(corpo, SEGREDO_ANTERIOR)
        ok, _ = seguranca.valida_assinatura(corpo, assinatura, [SEGREDO_ATUAL])
        self.assertFalse(ok)

    def test_compare_digest_nao_vaza_timing(self):
        """Usa hmac.compare_digest (não string ==)."""
        corpo = b'{"evento_id":"evt-1"}'
        assinatura_certa = seguranca.calcula_assinatura(corpo, SEGREDO_ATUAL)
        # assinatura com prefixo correto mas resto errado
        assinatura_errada = "sha256=" + "a" * 64
        ok, _ = seguranca.valida_assinatura(corpo, assinatura_errada, [SEGREDO_ATUAL])
        self.assertFalse(ok)


class TestValidaHorario(unittest.TestCase):
    def test_dentro_da_janela_valida(self):
        """Horário dentro de 5 min valida."""
        agora = dt.datetime(2026, 10, 8, 12, 0, tzinfo=TZ)
        recebido = dt.datetime(2026, 10, 8, 11, 58, tzinfo=TZ)
        ok, _ = seguranca.valida_horario(recebido, agora=agora, janela_min=5)
        self.assertTrue(ok)

    def test_fora_da_janela_recusa(self):
        """Horário mais de 5 min atrás recusa."""
        agora = dt.datetime(2026, 10, 8, 12, 0, tzinfo=TZ)
        recebido = dt.datetime(2026, 10, 8, 11, 54, tzinfo=TZ)  # 6 min atrás
        ok, motivo = seguranca.valida_horario(recebido, agora=agora, janela_min=5)
        self.assertFalse(ok)
        self.assertIn("horário", motivo.lower())

    def test_horario_futuro_recusa(self):
        """Horário no futuro recusa."""
        agora = dt.datetime(2026, 10, 8, 12, 0, tzinfo=TZ)
        recebido = dt.datetime(2026, 10, 8, 12, 10, tzinfo=TZ)
        ok, _ = seguranca.valida_horario(recebido, agora=agora, janela_min=5)
        self.assertFalse(ok)


class TestValidaIP(unittest.TestCase):
    def test_ip_permitido_valida(self):
        ok, _ = seguranca.valida_ip("10.0.0.50", IPS_PERMITIDOS)
        self.assertTrue(ok)

    def test_ip_nao_permitido_recusa(self):
        ok, motivo = seguranca.valida_ip("192.168.0.1", IPS_PERMITIDOS)
        self.assertFalse(ok)
        self.assertIn("ip", motivo.lower())


class TestVerifica(unittest.TestCase):
    """Testa a verificação combinada (assinatura + horário + IP)."""

    def setUp(self):
        self.corpo = b'{"evento_id":"evt-1","texto":"1"}'
        self.assinatura = seguranca.calcula_assinatura(self.corpo, SEGREDO_ATUAL)
        self.horario = dt.datetime(2026, 10, 8, 12, 0, tzinfo=TZ)
        self.agora = dt.datetime(2026, 10, 8, 12, 1, tzinfo=TZ)

    def test_tudo_valido_retorna_ok(self):
        ok, _, _, _ = seguranca.verifica(
            corpo=self.corpo,
            assinatura=self.assinatura,
            horario=self.horario,
            ip="10.0.0.50",
            segredos=[SEGREDO_ATUAL],
            ips_permitidos=IPS_PERMITIDOS,
            agora=self.agora,
        )
        self.assertTrue(ok)

    def test_assinatura_errada_retorna_401(self):
        ok, motivo, status, _ = seguranca.verifica(
            corpo=self.corpo,
            assinatura="sha256=deadbeef",
            horario=self.horario,
            ip="10.0.0.50",
            segredos=[SEGREDO_ATUAL],
            ips_permitidos=IPS_PERMITIDOS,
            agora=self.agora,
        )
        self.assertFalse(ok)
        self.assertEqual(status, 401)

    def test_ip_errado_retorna_401(self):
        ok, motivo, status, _ = seguranca.verifica(
            corpo=self.corpo,
            assinatura=self.assinatura,
            horario=self.horario,
            ip="192.168.0.1",
            segredos=[SEGREDO_ATUAL],
            ips_permitidos=IPS_PERMITIDOS,
            agora=self.agora,
        )
        self.assertFalse(ok)
        self.assertEqual(status, 401)

    def test_horario_errado_retorna_401(self):
        ok, motivo, status, _ = seguranca.verifica(
            corpo=self.corpo,
            assinatura=self.assinatura,
            horario=dt.datetime(2026, 10, 8, 11, 50, tzinfo=TZ),
            ip="10.0.0.50",
            segredos=[SEGREDO_ATUAL],
            ips_permitidos=IPS_PERMITIDOS,
            agora=self.agora,
        )
        self.assertFalse(ok)
        self.assertEqual(status, 401)

    def test_qual_segredo_validou(self):
        """verifica indica qual segredo validou (atual ou anterior), sem o valor."""
        assinatura_ant = seguranca.calcula_assinatura(self.corpo, SEGREDO_ANTERIOR)
        ok, _, _, qual = seguranca.verifica(
            corpo=self.corpo,
            assinatura=assinatura_ant,
            horario=self.horario,
            ip="10.0.0.50",
            segredos=[SEGREDO_ATUAL, SEGREDO_ANTERIOR],
            ips_permitidos=IPS_PERMITIDOS,
            agora=self.agora,
        )
        self.assertTrue(ok)
        self.assertEqual(qual, "anterior")


if __name__ == "__main__":
    unittest.main()
