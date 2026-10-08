"""Testes do contatos.py — cadastro de contatos do WhatsApp (P4 do chamado 068).

Só dados sintéticos: nenhum telefone, nome ou empresa real.
Run: python -m unittest discover painel/entrada/tests
"""
import datetime as dt
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import contatos  # noqa: E402

# Dados sintéticos — nenhum telefone/nome/empresa real
TEL_TESTE_1 = "559999900001"
TEL_TESTE_2 = "559999900002"
NOME_1 = "Contato Teste Um"
NOME_2 = "Contato Teste Dois"
EMPRESA = "Empresa Teste"


class TestContatos(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.db_path = os.path.join(self.tmp.name, "entrada.db")

    def tearDown(self):
        self.tmp.cleanup()

    def test_add_atribui_id_contato_e_grava(self):
        """add cria c-0001 com os dados e ativo=1."""
        res = contatos.add(self.db_path, telefone=TEL_TESTE_1, nome=NOME_1, empresa=EMPRESA)
        self.assertEqual(res["contato"], "c-0001")
        self.assertTrue(res["ativo"])
        c = contatos.lookup(self.db_path, TEL_TESTE_1)
        self.assertIsNotNone(c)
        self.assertEqual(c["nome"], NOME_1)
        self.assertEqual(c["empresa"], EMPRESA)
        self.assertEqual(c["contato"], "c-0001")

    def test_add_segundo_contato_incrementa_id(self):
        """O segundo contato é c-0002."""
        contatos.add(self.db_path, telefone=TEL_TESTE_1, nome=NOME_1, empresa=EMPRESA)
        res = contatos.add(self.db_path, telefone=TEL_TESTE_2, nome=NOME_2, empresa=EMPRESA)
        self.assertEqual(res["contato"], "c-0002")

    def test_add_telefone_duplicado_recusa(self):
        """O mesmo telefone não pode ser cadastrado duas vezes."""
        contatos.add(self.db_path, telefone=TEL_TESTE_1, nome=NOME_1, empresa=EMPRESA)
        with self.assertRaises(ValueError) as ctx:
            contatos.add(self.db_path, telefone=TEL_TESTE_1, nome="Outro", empresa=EMPRESA)
        self.assertIn("já cadastrado", str(ctx.exception).lower())

    def test_lookup_desconhecido_retorna_none(self):
        """Número não cadastrado retorna None — não recebe menu."""
        self.assertIsNone(contatos.lookup(self.db_path, "559999999999"))

    def test_list_retorna_so_ativos(self):
        """list mostra contatos ativos."""
        contatos.add(self.db_path, telefone=TEL_TESTE_1, nome=NOME_1, empresa=EMPRESA)
        contatos.add(self.db_path, telefone=TEL_TESTE_2, nome=NOME_2, empresa=EMPRESA)
        lista = contatos.lista(self.db_path)
        self.assertEqual(len(lista), 2)

    def test_rm_desativa_e_apaga_telefone(self):
        """rm desativa o contato e apaga o telefone (LGPD)."""
        res = contatos.add(self.db_path, telefone=TEL_TESTE_1, nome=NOME_1, empresa=EMPRESA)
        contatos.rm(self.db_path, res["contato"])
        # lookup por telefone não encontra mais
        self.assertIsNone(contatos.lookup(self.db_path, TEL_TESTE_1))
        # list não mostra
        self.assertEqual(len(contatos.lista(self.db_path)), 0)

    def test_rm_contato_inexistente_recusa(self):
        """rm de contato que não existe levanta erro."""
        with self.assertRaises(ValueError):
            contatos.rm(self.db_path, "c-9999")

    def test_cli_add_list_rm(self):
        """CLI: add → list → rm via linha de comando."""
        rc = contatos.cli(["add", "--telefone", TEL_TESTE_1, "--nome", NOME_1,
                           "--empresa", EMPRESA, "--db", self.db_path])
        self.assertEqual(rc, 0)
        rc = contatos.cli(["list", "--db", self.db_path])
        self.assertEqual(rc, 0)
        rc = contatos.cli(["rm", "c-0001", "--db", self.db_path])
        self.assertEqual(rc, 0)
        # depois do rm, list não mostra
        lista = contatos.lista(self.db_path)
        self.assertEqual(len(lista), 0)


if __name__ == "__main__":
    unittest.main()
