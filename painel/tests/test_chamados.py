"""Regras dos gates do chamado (padrão hindiana DOCS/processo/padrao-chamado.md)."""
import datetime as dt
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import chamados  # noqa: E402

TZ = dt.timezone(dt.timedelta(hours=-3))
HASHES = {"aaaaaaa": dt.datetime(2026, 10, 5, 20, 36, tzinfo=TZ)}
data_hash = HASHES.get

ABERTURA = """---
gate: abertura
tipo: bug
escopo: correcao
aberto_por: Cliente
origem: staging
data: 2026-10-05 18:13 -0300
autores: W09
---
# Marco trava
"""


def g3(papel, veredito, por, data="2026-10-05 21:00 -0300", numeros="", objeto="src/x.py @ aaaaaaa", data_objeto="2026-10-05 20:36 -0300"):
    n = f'numeros: "{numeros}"\n' if numeros else ""
    return (f"---\ngate: G3\npapel: {papel}\nobjeto: {objeto}\nveredito: {veredito}\npor: {por}\n"
            f"data: {data}\ndata_objeto: {data_objeto}\n{n}---\n")


class TestG3(unittest.TestCase):
    def estado(self, arquivos):
        r = chamados.confere({"00-chamado.md": ABERTURA, **arquivos}, data_hash, True)
        return next(g for g in r["gates"] if g["gate"] == "G3")

    def test_passa_com_codigo_criterio_e_runner2_limpo_no_mesmo_hash(self):
        g = self.estado({"G3-codigo-W13-aaaaaaa.md": g3("codigo", "APPROVE", "W13"),
                         "G3-criterio-W11-aaaaaaa.md": g3("criterio", "APPROVE", "W11"),
                         "G3-runner2-W07-aaaaaaa.md": g3("runner2", "OK", "W07", numeros="pytest 10/0/0, vitest 5/0/0")})
        self.assertEqual(g["estado"], "ok")

    def test_runner2_com_errors_nao_conta(self):
        g = self.estado({"G3-runner2-W13-aaaaaaa.md": g3("runner2", "OK", "W13", numeros="pytest 2751/0/14")})
        self.assertTrue(any("0 errors" in e for i in g["itens"] for e in i["erros"]))

    def test_critico_autor_veredito_antes_do_objeto_e_negrito_nao_contam(self):
        g = self.estado({"G3-codigo-W09-aaaaaaa.md": g3("codigo", "APPROVE", "W09", data="2026-10-05 20:00 -0300",
                                                        objeto="**src/x.py** @ aaaaaaa")})
        erros = " | ".join(g["itens"][0]["erros"])
        for trecho in ("autor da peça", "anterior ao objeto", "negrito"):
            self.assertIn(trecho, erros)
        self.assertNotEqual(g["estado"], "ok")

    def test_reprove_barra(self):
        g = self.estado({"G3-codigo-W13-aaaaaaa.md": g3("codigo", "REPROVE", "W13")})
        self.assertEqual(g["estado"], "bad")


class TestG1(unittest.TestCase):
    def test_correcao_passa_com_um_approve(self):
        spec = "---\ngate: G1\nobjeto: specs/x/spec.md @ aaaaaaa\nveredito: APPROVE\npor: W13\ndata: 2026-10-05 21:00 -0300\n---\n"
        r = chamados.confere({"00-chamado.md": ABERTURA, "G1-spec-W13.md": spec}, data_hash, True)
        self.assertEqual(next(g for g in r["gates"] if g["gate"] == "G1")["estado"], "ok")
        self.assertEqual(r["onde"], "G0")  # bug sem reprodução ainda para no G0


if __name__ == "__main__":
    unittest.main()
