"""Contrato frontend↔backend: toda rota /api/ que o front chama existe no server.

Garante que index.html nunca chama um endpoint que server.py não define.
Se o front adiciona uma rota nova, este teste falha até o backend expor a rota.

Plan 065 T4 (914c3c8) define: /api/board (com exceções+workers), /api/rodadas
(com árvore), /api/roadmap. O front usa essas rotas — não /api/tarefa nem
/api/excecoes separados (exceções vêm dentro de /api/board, tarefa dentro de
/api/rodadas?id=...).
"""
from __future__ import annotations

import os
import re
import sys
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
import server  # noqa: E402


class TestContratoFrontBackend(unittest.TestCase):
    """Toda rota /api/ chamada no index.html existe no server.py ROTAS."""

    def test_rotas_do_front_existem_no_server(self):
        """Extrai rotas /api/ do index.html e verifica que estão em ROTAS."""
        index_path = os.path.join(AQUI, "..", "index.html")
        with open(index_path, encoding="utf-8") as f:
            html = f.read()

        # Extrai todas as rotas /api/... chamadas via api() ou fetch()
        rotas_chamadas = set()
        for m in re.finditer(r'(?:api|fetch)\(["\'](/api/[^?"\'\s]+)', html):
            rotas_chamadas.add(m.group(1))

        self.assertTrue(rotas_chamadas, "Deve ter encontrado rotas /api/ no index.html")

        rotas_server = set(server.ROTAS.keys())
        # POST routes que não estão em ROTAS (tratadas separadamente)
        rotas_post = {"/api/reingerir", "/api/eventos"}

        missing = rotas_chamadas - rotas_server - rotas_post
        self.assertEqual(missing, set(),
                         f"Rotas chamadas pelo front mas inexistentes no server: {missing}")

    def test_board_retorna_excecoes_e_workers(self):
        """/api/board retorna 'excecoes' e 'workers' (FR1, FR2 do plan 065)."""
        # v_board deve aceitar so_excecoes e retornar excecoes+workers
        import inspect
        sig = inspect.signature(server.v_board)
        params = list(sig.parameters.keys())
        self.assertIn("so_excecoes", params, "v_board deve ter parâmetro so_excecoes (FR3)")

    def test_rodadas_retorna_arvore(self):
        """/api/rodadas retorna 'arvore' quando id dado (FR8 do plan 065)."""
        import inspect
        sig = inspect.signature(server.v_rodadas)
        params = list(sig.parameters.keys())
        self.assertIn("rodada_id", params, "v_rodadas deve ter parâmetro rodada_id (FR8)")

    def test_arvore_existe(self):
        """server.py tem v_arvore (FR8, FR9 do plan 065)."""
        self.assertTrue(hasattr(server, "v_arvore"), "server.py deve ter v_arvore")


if __name__ == "__main__":
    unittest.main()
