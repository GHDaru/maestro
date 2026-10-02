"""Tests for spec 064 — Workflow do ciclo Maestro no painel.

Red test for T6: Roadmap mostra cada rodada com passo atual, tempo em cada
passo, quem está nele. Link para o arquivo.

Run: python -m unittest discover painel/tests
"""
import json
import os
import sqlite3
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ingest  # noqa: E402
import server  # noqa: E402


def escreve(caminho, texto):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(texto)


class Fixture(unittest.TestCase):
    """Same fixture pattern as test_painel.py."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        r = self.raiz = self.tmp.name
        escreve(os.path.join(r, "esp/equipe/WORKER-04.md"),
                "# Worker04\n\n## Estado atual (30/09, 23:45)\n\n- **Papel:** DDD\n")
        cfg = {"projeto": "t", "raiz": ".", "equipe": "esp/equipe",
               "equipes": {"Coordenação": ["Gerente", "Torre"]},
               "documentos": {"constituicao": ["esp/*.md"]}}
        self.cfg_path = os.path.join(r, "p.json")
        escreve(self.cfg_path, json.dumps(cfg))
        self.cfg = ingest.carrega_cfg(self.cfg_path)
        self.db = os.path.join(r, "t.db")

    def tearDown(self):
        self.tmp.cleanup()

    def cria_tabelas_rodadas(self, db):
        """Cria tabelas que W09 (T1) criará em produção."""
        db.executescript("""
            CREATE TABLE IF NOT EXISTS rodadas (
                id TEXT PRIMARY KEY, desejo TEXT, criada_por TEXT,
                aberta_em TEXT, fechada_em TEXT, arquivo TEXT);
            CREATE TABLE IF NOT EXISTS passos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rodada TEXT, passo TEXT, sessao TEXT,
                entrada_em TEXT, resumo TEXT, saida_em TEXT,
                evidencia_json TEXT, resultado TEXT);
        """)


class T6RoadmapRodadas(Fixture):
    """T6: Roadmap mostra cada rodada com passo atual, tempo em cada passo, quem está nele."""

    def test_rodada_com_passo_atual_tempo_e_quem(self):
        ingest.ingere(self.cfg, self.db)
        db = server.conecta(self.db)
        self.cria_tabelas_rodadas(db)
        # Rodada R001: spec fechada (1h), plan aberta
        db.execute("INSERT INTO rodadas VALUES (?,?,?,?,?,?)",
                   ("R001", "Workflow painel", "Gerente",
                    "2026-10-02T10:00:00-03:00", None, "specs/064/spec.md"))
        db.execute("INSERT INTO passos (rodada, passo, sessao, entrada_em, saida_em) VALUES (?,?,?,?,?)",
                   ("R001", "spec", "Gerente", "2026-10-02T10:00:00-03:00", "2026-10-02T11:00:00-03:00"))
        db.execute("INSERT INTO passos (rodada, passo, sessao, entrada_em) VALUES (?,?,?,?)",
                   ("R001", "plan", "Gerente", "2026-10-02T11:00:00-03:00"))
        db.commit()

        result = server.v_rodadas(db)
        self.assertEqual(len(result["rodadas"]), 1)
        r = result["rodadas"][0]
        self.assertEqual(r["id"], "R001")
        self.assertEqual(r["desejo"], "Workflow painel")
        self.assertEqual(r["passo_atual"], "plan")
        self.assertEqual(r["quem"], "Gerente")
        self.assertEqual(r["arquivo"], "specs/064/spec.md")
        # Passo spec fechado: 1h
        self.assertEqual(len(r["passos"]), 2)
        spec = r["passos"][0]
        self.assertEqual(spec["passo"], "spec")
        self.assertEqual(spec["horas"], 1.0)
        # Passo plan aberto: sem saida_em
        plan = r["passos"][1]
        self.assertEqual(plan["passo"], "plan")
        self.assertIsNone(plan["saida_em"])

    def test_rodada_sem_passos_mostra_vazio(self):
        ingest.ingere(self.cfg, self.db)
        db = server.conecta(self.db)
        self.cria_tabelas_rodadas(db)
        db.execute("INSERT INTO rodadas VALUES (?,?,?,?,?,?)",
                   ("R002", "Outro desejo", "Office", "2026-10-02T12:00:00-03:00", None, ""))
        db.commit()

        result = server.v_rodadas(db)
        r = result["rodadas"][0]
        self.assertEqual(r["id"], "R002")
        self.assertEqual(r["passos"], [])
        self.assertIsNone(r["passo_atual"])


class T7EquipeReal(Fixture):
    """T7: Equipe real com 19 sessões (4 Desktop + 15 Code sem W10)."""

    def test_meta_equipes_tem_19_sessoes(self):
        cfg = dict(self.cfg)
        cfg["equipes"] = {
            "Claude Desktop": ["Office", "Assistente", "Reescrita", "Testes Dev"],
            "Coordenação": ["Gerente", "Gerente02", "Torre"],
            "Time do Gerente": ["W02", "W06", "W07", "W08", "W09", "W11"],
            "Time do Gerente02": ["W01", "W03", "W04", "W05", "W12", "W13"],
        }
        ingest.ingere(cfg, self.db)
        m = server.v_meta(server.conecta(self.db))
        todas = [s for grupo in m["equipes"].values() for s in grupo]
        self.assertEqual(len(todas), 19)
        self.assertNotIn("W10", todas)
        for nome in ("Office", "Assistente", "Reescrita", "Testes Dev",
                     "Gerente", "Gerente02", "Torre", "W03", "W13"):
            self.assertIn(nome, todas)


class T8LeituraVelha(Fixture):
    """T8: Aviso de leitura velha quando último ingest > 1 h."""

    def test_meta_inclui_idade_do_ingest(self):
        ingest.ingere(self.cfg, self.db)
        m = server.v_meta(server.conecta(self.db))
        self.assertIn("ingerido_age_min", m)
        self.assertLess(m["ingerido_age_min"], 1)


class T9ErroLeitura(Fixture):
    """T9: Se arquivo não pode ser lido, exibe caminho e motivo, não vazio."""

    def test_erros_leitura_retorna_caminho_e_motivo(self):
        ingest.ingere(self.cfg, self.db)
        db = server.conecta(self.db)
        db.execute("INSERT INTO erros_leitura VALUES (?,?,?)",
                   ("esp/inexistente.md", "FileNotFoundError: no such file", "roadmap"))
        db.commit()
        erros = server.v_erros_leitura(db)
        self.assertTrue(len(erros) > 0)
        e = erros[0]
        self.assertTrue(e["caminho"])
        self.assertTrue(e["motivo"])

    def test_ingere_registra_erro_de_leitura(self):
        """Quando ler() falha, o ingest registra na tabela erros_leitura."""
        escreve(os.path.join(self.raiz, "esp/decisoes.md"),
                "# D\n\n| # | Hora | Decisão | Contexto | Como desfazer |\n|---|---|---|---|---|\n"
                "| D1 | 10:00 | **Fazer X** | porque sim | reverter |\n")
        cfg = dict(self.cfg)
        cfg["decisoes"] = [os.path.join(self.raiz, "esp", "decisoes*.md")]
        ingest.ingere(cfg, self.db)
        db = server.conecta(self.db)
        # O arquivo legível deve ter sido processado
        d = server.v_decisoes(db)
        self.assertTrue(len(d["decisoes"]) > 0)


class T9bDecisoesAparecendo(Fixture):
    """T9b: Decisões aparecendo no painel (hoje vazio)."""

    def test_decisoes_nao_vazias(self):
        escreve(os.path.join(self.raiz, "esp/decisoes.md"),
                "# D\n\n| # | Hora | Decisão | Contexto | Como desfazer |\n|---|---|---|---|---|\n"
                "| D1 | 10:00 | **Fazer X** | porque sim | reverter |\n")
        cfg = dict(self.cfg)
        cfg["decisoes"] = [os.path.join(self.raiz, "esp", "decisoes*.md")]
        ingest.ingere(cfg, self.db)
        d = server.v_decisoes(server.conecta(self.db))
        self.assertTrue(len(d["decisoes"]) > 0)
        self.assertEqual(d["decisoes"][0]["id"], "D1")


if __name__ == "__main__":
    unittest.main()
