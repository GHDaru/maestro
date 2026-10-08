"""Testes do eventos.py — idempotência por evento_id (P5-AC2 do chamado 068).

Só dados sintéticos: nenhum telefone/nome/mensagem real.
Run: python -m unittest discover painel/entrada/tests
"""
import datetime as dt
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import eventos  # noqa: E402

TZ = dt.timezone(dt.timedelta(hours=-3))


class TestEventos(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.db_path = os.path.join(self.tmp.name, "entrada.db")

    def tearDown(self):
        self.tmp.cleanup()

    def test_primeira_chamada_registra_e_retorna(self):
        """processa: primeira vez executa fn e guarda o resultado."""
        res = eventos.processa(self.db_path, "evt-001", lambda: {"responder": [{"texto": "menu"}]})
        self.assertEqual(res["responder"][0]["texto"], "menu")

    def test_segunda_chamada_mesmo_id_retorna_copiado(self):
        """processa: mesmo evento_id não chama fn de novo; retorna o mesmo resultado."""
        contador = {"n": 0}

        def fn():
            contador["n"] += 1
            return {"responder": [{"texto": "menu"}], "chamado": None}

        res1 = eventos.processa(self.db_path, "evt-001", fn)
        res2 = eventos.processa(self.db_path, "evt-001", fn)
        self.assertEqual(res1, res2)
        self.assertEqual(contador["n"], 1, "fn foi chamada duas vezes")

    def test_ids_diferentes_executa_fn(self):
        """eventos diferentes executam fn independentemente."""
        contador = {"n": 0}

        def fn():
            contador["n"] += 1
            return {"ok": True}

        eventos.processa(self.db_path, "evt-001", fn)
        eventos.processa(self.db_path, "evt-002", fn)
        self.assertEqual(contador["n"], 2)

    def test_limpa_remove_eventos_antigos(self):
        """limpa remove eventos com mais de N dias."""
        eventos.processa(self.db_path, "evt-001", lambda: {"ok": True})
        # Simular que o evento foi registrado há 10 dias
        import sqlite3
        antigo = (dt.datetime.now(TZ) - dt.timedelta(days=10)).isoformat()
        db = sqlite3.connect(self.db_path)
        db.execute("UPDATE eventos SET recebido_em = ? WHERE evento_id = ?", (antigo, "evt-001"))
        db.commit()
        db.close()
        # limpa com 7 dias
        removidos = eventos.limpa(self.db_path, dias=7)
        self.assertEqual(removidos, 1)
        # consultar retorna None
        self.assertIsNone(eventos.consulta(self.db_path, "evt-001"))

    def test_limpa_nao_remove_recentes(self):
        """limpa não remove eventos dentro do prazo."""
        eventos.processa(self.db_path, "evt-001", lambda: {"ok": True})
        removidos = eventos.limpa(self.db_path, dias=7)
        self.assertEqual(removidos, 0)
        self.assertIsNotNone(eventos.consulta(self.db_path, "evt-001"))

    def test_consulta_retorna_none_se_nao_existe(self):
        self.assertIsNone(eventos.consulta(self.db_path, "evt-inexistente"))


if __name__ == "__main__":
    unittest.main()
