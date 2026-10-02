"""Tests for spec 065 T7 — Workflow por tarefa (linha do tempo).

FR5: passo atual + tempo por tarefa.
FR6: click na tarefa → linha do tempo dos passos (entrada, resumo, saída,
     sessão, hash, evidência) e evidência que falta para o próximo passo.
FR7: evidência ≠ hash → chip amarelo (divergência).

Run: python -m unittest discover painel/tests
"""
import json
import os
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

    def cria_tabelas_065(self, db):
        db.executescript("""
            CREATE TABLE IF NOT EXISTS rodadas (
                id TEXT PRIMARY KEY, desejo TEXT, criada_por TEXT,
                aberta_em TEXT, fechada_em TEXT, arquivo TEXT);
            CREATE TABLE IF NOT EXISTS passos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rodada TEXT, passo TEXT, sessao TEXT,
                entrada_em TEXT, resumo TEXT, saida_em TEXT,
                evidencia_json TEXT, resultado TEXT);
            CREATE TABLE IF NOT EXISTS arvore_rodada (
                rodada TEXT, tipo TEXT, id_no TEXT, pai TEXT,
                label TEXT, status TEXT, referencia TEXT, hash TEXT,
                evidencia_ok INTEGER,
                PRIMARY KEY (rodada, tipo, id_no));
        """)


class T7WorkflowTarefa(Fixture):
    """T7: Workflow por tarefa — linha do tempo (FR5, FR6, FR7)."""

    def test_passo_atual_e_tempo_por_tarefa(self):
        """FR5: cada tarefa mostra passo atual do workflow e tempo nele."""
        ingest.ingere(self.cfg, self.db)
        db = server.conecta(self.db)
        self.cria_tabelas_065(db)
        db.execute("INSERT INTO rodadas VALUES (?,?,?,?,?,?)",
                   ("R001", "Workflow painel", "Gerente",
                    "2026-10-02T10:00:00-03:00", None, "specs/064/spec.md"))
        db.execute("INSERT INTO passos (rodada, passo, sessao, entrada_em, saida_em, resultado) VALUES (?,?,?,?,?,?)",
                   ("R001", "T9", "W03", "2026-10-02T14:00:00-03:00",
                    "2026-10-02T15:00:00-03:00", "ok"))
        db.execute("INSERT INTO passos (rodada, passo, sessao, entrada_em) VALUES (?,?,?,?)",
                   ("R001", "critica", "W13", "2026-10-02T15:00:00-03:00"))
        db.commit()

        result = server.v_rodadas(db, rodada_id="R001")
        r = result["rodadas"][0]
        self.assertEqual(r["passo_atual"], "critica")
        self.assertEqual(r["quem"], "W13")
        # T9 teve 1h
        t9 = next(p for p in r["passos"] if p["passo"] == "T9")
        self.assertEqual(t9["horas"], 1.0)

    def test_linha_do_tempo_com_hash_e_evidencia(self):
        """FR6: linha do tempo mostra entrada, resumo, saída, sessão, hash, evidência."""
        ingest.ingere(self.cfg, self.db)
        db = server.conecta(self.db)
        self.cria_tabelas_065(db)
        db.execute("INSERT INTO rodadas VALUES (?,?,?,?,?,?)",
                   ("R001", "Workflow painel", "Gerente",
                    "2026-10-02T10:00:00-03:00", None, "specs/064/spec.md"))
        db.execute("INSERT INTO passos (rodada, passo, sessao, entrada_em, saida_em, resumo, evidencia_json, resultado) VALUES (?,?,?,?,?,?,?,?)",
                   ("R001", "T9", "W03", "2026-10-02T14:00:00-03:00",
                    "2026-10-02T15:00:00-03:00", "T9 red test",
                    '{"hash":"58cf24e","runner2":"20/20"}', "ok"))
        db.commit()

        result = server.v_rodadas(db, rodada_id="R001")
        p = result["rodadas"][0]["passos"][0]
        self.assertEqual(p["resumo"], "T9 red test")
        self.assertEqual(p["entrada_em"], "2026-10-02T14:00:00-03:00")
        self.assertEqual(p["saida_em"], "2026-10-02T15:00:00-03:00")
        self.assertEqual(p["sessao"], "W03")
        # FR6: hash e evidência extraídos do evidencia_json
        self.assertEqual(p["hash"], "58cf24e")
        self.assertEqual(p["evidencia"]["runner2"], "20/20")

    def test_evidencia_diverge_hash(self):
        """FR7: evidência ≠ hash → evidencia_ok=0 (chip amarelo)."""
        ingest.ingere(self.cfg, self.db)
        db = server.conecta(self.db)
        self.cria_tabelas_065(db)
        db.execute("INSERT INTO rodadas VALUES (?,?,?,?,?,?)",
                   ("R001", "Workflow painel", "Gerente",
                    "2026-10-02T10:00:00-03:00", None, "specs/064/spec.md"))
        # Passo com hash que diverge do hash registrado na árvore
        db.execute("INSERT INTO passos (rodada, passo, sessao, entrada_em, saida_em, evidencia_json, resultado) VALUES (?,?,?,?,?,?,?)",
                   ("R001", "T9", "W03", "2026-10-02T14:00:00-03:00",
                    "2026-10-02T15:00:00-03:00",
                    '{"hash":"a145b07"}', "ok"))
        # Árvore registra hash diferente
        db.execute("INSERT INTO arvore_rodada VALUES (?,?,?,?,?,?,?,?,?)",
                   ("R001", "task", "T9", None, "T9: erro de leitura", "ok",
                    "painel/index.html", "41f3b60", 0))
        db.commit()

        result = server.v_rodadas(db, rodada_id="R001")
        # FR7: árvore mostra evidencia_ok=0 (divergência)
        no = next(n for n in result["arvore"] if n["id_no"] == "T9")
        self.assertEqual(no["evidencia_ok"], 0)
        self.assertEqual(no["hash"], "41f3b60")
        # Passo registra hash da evidência (a145b07) ≠ hash da árvore (41f3b60)
        p = result["rodadas"][0]["passos"][0]
        self.assertEqual(p["hash"], "a145b07")

    def test_evidencia_confere_hash(self):
        """FR7: evidência = hash → evidencia_ok=1 (chip verde)."""
        ingest.ingere(self.cfg, self.db)
        db = server.conecta(self.db)
        self.cria_tabelas_065(db)
        db.execute("INSERT INTO rodadas VALUES (?,?,?,?,?,?)",
                   ("R001", "Workflow painel", "Gerente",
                    "2026-10-02T10:00:00-03:00", None, "specs/064/spec.md"))
        db.execute("INSERT INTO passos (rodada, passo, sessao, entrada_em, saida_em, evidencia_json, resultado) VALUES (?,?,?,?,?,?,?)",
                   ("R001", "T9", "W03", "2026-10-02T14:00:00-03:00",
                    "2026-10-02T15:00:00-03:00",
                    '{"hash":"41f3b60"}', "ok"))
        db.execute("INSERT INTO arvore_rodada VALUES (?,?,?,?,?,?,?,?,?)",
                   ("R001", "task", "T9", None, "T9: erro de leitura", "ok",
                    "painel/index.html", "41f3b60", 1))
        db.commit()

        result = server.v_rodadas(db, rodada_id="R001")
        no = next(n for n in result["arvore"] if n["id_no"] == "T9")
        self.assertEqual(no["evidencia_ok"], 1)

    def test_linha_do_tempo_passo_aberto_sem_saida(self):
        """FR6: passo aberto (sem saida_em) mostra '—' no tempo e None no hash."""
        ingest.ingere(self.cfg, self.db)
        db = server.conecta(self.db)
        self.cria_tabelas_065(db)
        db.execute("INSERT INTO rodadas VALUES (?,?,?,?,?,?)",
                   ("R001", "Workflow painel", "Gerente",
                    "2026-10-02T10:00:00-03:00", None, "specs/064/spec.md"))
        db.execute("INSERT INTO passos (rodada, passo, sessao, entrada_em) VALUES (?,?,?,?)",
                   ("R001", "critica", "W13", "2026-10-02T15:00:00-03:00"))
        db.commit()

        result = server.v_rodadas(db, rodada_id="R001")
        p = result["rodadas"][0]["passos"][0]
        self.assertIsNone(p["horas"])
        self.assertIsNone(p["hash"])
