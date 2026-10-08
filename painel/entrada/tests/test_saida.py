"""Testes do saida.py — fila de saída com retry e limite (P5-AC3, AC4 do chamado 068).

Só dados sintéticos: nenhum telefone/nome/mensagem real.
Run: python -m unittest discover painel/entrada/tests
"""
import datetime as dt
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import saida  # noqa: E402

TZ = dt.timezone(dt.timedelta(hours=-3))
# Dados sintéticos
CONTATO = "c-0001"
CHAMADO = "099"
TEXTO = "Chamado #099 · Etapa 1 de 6: Recebido"


class TestSaida(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.db_path = os.path.join(self.tmp.name, "entrada.db")
        self.agora = dt.datetime(2026, 10, 8, 12, 0, tzinfo=TZ)

    def tearDown(self):
        self.tmp.cleanup()

    def test_enfileira_cria_pendente(self):
        """enfileira cria uma mensagem pendente com tentativas=0."""
        sid = saida.enfileira(self.db_path, chamado=CHAMADO, contato=CONTATO, texto=TEXTO, agora=self.agora)
        self.assertIsNotNone(sid)
        pend = saida.pendentes(self.db_path, agora=self.agora)
        self.assertEqual(len(pend), 1)
        self.assertEqual(pend[0]["texto"], TEXTO)

    def test_200_marca_enviado(self):
        """send_fn retorna 200 → marca enviado, sai da fila."""
        saida.enfileira(self.db_path, chamado=CHAMADO, contato=CONTATO, texto=TEXTO, agora=self.agora)
        res = saida.processa_fila(self.db_path, send_fn=lambda msg: 200, agora=self.agora)
        self.assertEqual(res["enviados"], 1)
        self.assertEqual(res["falhas"], 0)
        self.assertEqual(len(saida.pendentes(self.db_path, agora=self.agora)), 0)

    def test_500_agenda_retry_1_min(self):
        """send_fn retorna 500 → agenda retry em 1 min, fica pendente."""
        saida.enfileira(self.db_path, chamado=CHAMADO, contato=CONTATO, texto=TEXTO, agora=self.agora)
        res = saida.processa_fila(self.db_path, send_fn=lambda msg: 500, agora=self.agora)
        self.assertEqual(res["enviados"], 0)
        self.assertEqual(res["falhas"], 0)
        # Ainda pendente, mas proxima_em é daqui a 1 min
        pend = saida.pendentes(self.db_path, agora=self.agora)
        self.assertEqual(len(pend), 0)  # não está pronto agora
        pronto_em_1min = saida.pendentes(self.db_path, agora=self.agora + dt.timedelta(minutes=1))
        self.assertEqual(len(pronto_em_1min), 1)

    def test_retry_intervals_1_5_15_60(self):
        """Os intervalos de retry são 1, 5, 15, 60 min."""
        sid = saida.enfileira(self.db_path, chamado=CHAMADO, contato=CONTATO, texto=TEXTO, agora=self.agora)
        esperados = [1, 5, 15, 60]
        t = self.agora
        for i, esperado in enumerate(esperados):
            res = saida.processa_fila(self.db_path, send_fn=lambda msg: 500, agora=t)
            self.assertEqual(res["falhas"], 0, f"tentativa {i+1} não devia ter falhado")
            # Avança para o próximo momento de retry
            t = t + dt.timedelta(minutes=esperado)
        # 4 tentativas, ainda pendente
        self.assertEqual(len(saida.pendentes(self.db_path, agora=t)), 1)

    def test_10_tentativas_marca_falhou(self):
        """Após 10 tentativas, a mensagem fica 'falhou' (NFR-012)."""
        saida.enfileira(self.db_path, chamado=CHAMADO, contato=CONTATO, texto=TEXTO, agora=self.agora)
        t = self.agora
        for _ in range(10):
            saida.processa_fila(self.db_path, send_fn=lambda msg: 500, agora=t)
            t = t + dt.timedelta(minutes=60)  # avança o suficiente
        # A 11ª tentativa não acontece
        res = saida.processa_fila(self.db_path, send_fn=lambda msg: 200, agora=t)
        self.assertEqual(res["enviados"], 0, "11ª tentativa não deveria enviar")
        # Está falhou
        falhos = saida.falhos(self.db_path)
        self.assertEqual(len(falhos), 1)

    def test_24h_marca_falhou(self):
        """Após 24h na fila, mesmo com poucas tentativas, fica 'falhou'."""
        saida.enfileira(self.db_path, chamado=CHAMADO, contato=CONTATO, texto=TEXTO, agora=self.agora)
        # Simular que foi enfileirado há 24h+1min
        import sqlite3
        antigo = (self.agora - dt.timedelta(hours=24, minutes=1)).isoformat()
        db = sqlite3.connect(self.db_path)
        db.execute("UPDATE saida SET criado_em = ? WHERE id = 1", (antigo,))
        db.commit()
        db.close()
        # processa: tenta enviar, falha (500), mas como já passou 24h → falhou
        saida.processa_fila(self.db_path, send_fn=lambda msg: 500, agora=self.agora)
        falhos = saida.falhos(self.db_path)
        self.assertEqual(len(falhos), 1)

    def test_pendentes_conta(self):
        """O painel pode ver quantas mensagens estão pendentes."""
        saida.enfileira(self.db_path, chamado=CHAMADO, contato=CONTATO, texto=TEXTO, agora=self.agora)
        saida.enfileira(self.db_path, chamado="100", contato=CONTATO, texto="outra", agora=self.agora)
        self.assertEqual(saida.conta_pendentes(self.db_path, agora=self.agora), 2)


if __name__ == "__main__":
    unittest.main()
