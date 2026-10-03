"""Tests for spec 065 — Board enxuto, rodada navegável e workflow por tarefa.

T5: Board com 3 exceções no topo (FR1), linha por sessão 5 colunas (FR2),
    filtro só exceções (FR3), hook event como última atividade (FR4).
T6: Árvore navegável da rodada (FR8, FR9, FR10).
T8: Roadmap com raias por ciclo (FR11).

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
    """Same fixture pattern as test_workflow_painel.py."""

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
            CREATE TABLE IF NOT EXISTS excecoes_board (
                tipo TEXT PRIMARY KEY, contador INTEGER, detalhe_json TEXT);
            CREATE TABLE IF NOT EXISTS status_workers (
                sessao TEXT PRIMARY KEY, estado TEXT, peca TEXT, passo TEXT,
                esperando TEXT, ultima_atividade TEXT, sem_tarefa_ciclos INTEGER);
            CREATE TABLE IF NOT EXISTS arvore_rodada (
                rodada TEXT, tipo TEXT, id_no TEXT, pai TEXT,
                label TEXT, status TEXT, referencia TEXT, hash TEXT,
                evidencia_ok INTEGER,
                PRIMARY KEY (rodada, tipo, id_no));
        """)


class T5BoardExcecoes(Fixture):
    """T5: Board com 3 exceções no topo (FR1), linha por sessão (FR2),
    filtro só exceções (FR3), hook event (FR4)."""

    def test_board_retorna_excecoes_do_topo(self):
        """FR1: board retorna 3 exceções: gilsiley, gate_push, sem_tarefa_2ciclos."""
        ingest.ingere(self.cfg, self.db)
        db = server.conecta(self.db)
        self.cria_tabelas_065(db)
        db.execute("INSERT OR REPLACE INTO excecoes_board VALUES (?,?,?)",
                   ("gilsiley", 2, '[{"item":"D18"},{"item":"D23"}]'))
        db.execute("INSERT OR REPLACE INTO excecoes_board VALUES (?,?,?)",
                   ("gate_push", 1, '[{"item":"065 T5"}]'))
        db.execute("INSERT OR REPLACE INTO excecoes_board VALUES (?,?,?)",
                   ("sem_tarefa_2ciclos", 0, '[]'))
        db.commit()

        result = server.v_board(db)
        self.assertIn("excecoes", result)
        exc = result["excecoes"]
        self.assertEqual(exc["gilsiley"]["contador"], 2)
        self.assertEqual(exc["gate_push"]["contador"], 1)
        self.assertEqual(exc["sem_tarefa_2ciclos"]["contador"], 0)

    def test_excecoes_zero_nao_vermelhas(self):
        """FR1: exceção com contador 0 não é vermelha."""
        ingest.ingere(self.cfg, self.db)
        db = server.conecta(self.db)
        self.cria_tabelas_065(db)
        db.execute("INSERT OR REPLACE INTO excecoes_board VALUES (?,?,?)",
                   ("gilsiley", 0, '[]'))
        db.execute("INSERT OR REPLACE INTO excecoes_board VALUES (?,?,?)",
                   ("gate_push", 0, '[]'))
        db.execute("INSERT OR REPLACE INTO excecoes_board VALUES (?,?,?)",
                   ("sem_tarefa_2ciclos", 0, '[]'))
        db.commit()

        result = server.v_board(db)
        for tipo in ("gilsiley", "gate_push", "sem_tarefa_2ciclos"):
            self.assertFalse(result["excecoes"][tipo]["contador"] > 0,
                             f"{tipo} deveria ser 0 (não vermelho)")

    def test_board_sem_tabelas_065_nao_quebra(self):
        """Graceful fallback: board funciona mesmo com tabelas 065 populadas pelo ingest."""
        ingest.ingere(self.cfg, self.db)
        db = server.conecta(self.db)
        result = server.v_board(db)
        self.assertIn("excecoes", result)
        self.assertIsInstance(result["excecoes"], dict)

    def test_linha_por_sessao_5_colunas(self):
        """FR2: cada sessão tem sessão, estado, peca/passo, esperando, idade_min."""
        ingest.ingere(self.cfg, self.db)
        db = server.conecta(self.db)
        self.cria_tabelas_065(db)
        db.execute("INSERT INTO status_workers VALUES (?,?,?,?,?,?,?)",
                   ("W03", "busy", "065/ux-design", "critica", "W13+W01",
                    "2026-10-02T19:00:00-03:00", 0))
        db.commit()

        result = server.v_board(db)
        self.assertIn("workers", result)
        w = next(w for w in result["workers"] if w["sessao"] == "W03")
        self.assertEqual(w["estado"], "busy")
        self.assertEqual(w["peca"], "065/ux-design")
        self.assertEqual(w["passo"], "critica")
        self.assertEqual(w["esperando"], "W13+W01")
        self.assertIsNotNone(w["ultima_atividade"])

    def test_filtro_so_excecoes(self):
        """FR3: ?so_excecoes=1 retorna só sessões com estado de exceção."""
        ingest.ingere(self.cfg, self.db)
        db = server.conecta(self.db)
        self.cria_tabelas_065(db)
        db.execute("INSERT INTO status_workers VALUES (?,?,?,?,?,?,?)",
                   ("W03", "busy", "065/tela", "implement", None,
                    "2026-10-02T19:00:00-03:00", 0))
        db.execute("INSERT INTO status_workers VALUES (?,?,?,?,?,?,?)",
                   ("W13", "idle", None, None, None, None, 2))
        db.commit()

        result = server.v_board(db, so_excecoes=True)
        self.assertIn("workers", result)
        sessoes = [w["sessao"] for w in result["workers"]]
        self.assertIn("W13", sessoes)  # sem_tarefa_2ciclos = 2 → exceção
        self.assertNotIn("W03", sessoes)  # busy, sem exceção


class T6ArvoreNavegavel(Fixture):
    """T6: Árvore navegável da rodada (FR8, FR9, FR10)."""

    def test_arvore_rodada_retornada(self):
        """FR8: /api/rodadas?id=R001 retorna árvore com nós spec/plan/task/critica."""
        ingest.ingere(self.cfg, self.db)
        db = server.conecta(self.db)
        self.cria_tabelas_065(db)
        db.execute("INSERT INTO rodadas VALUES (?,?,?,?,?,?)",
                   ("R001", "Workflow painel", "Gerente",
                    "2026-10-02T10:00:00-03:00", None, "specs/064/spec.md"))
        db.execute("INSERT INTO arvore_rodada VALUES (?,?,?,?,?,?,?,?,?)",
                   ("R001", "spec", "FR1", None, "FR1: 3 exceções", "ok",
                    "test_fr1_excecoes", "abc123", 1))
        db.execute("INSERT INTO arvore_rodada VALUES (?,?,?,?,?,?,?,?,?)",
                   ("R001", "spec", "FR8", None, "FR8: árvore navegável", "ok",
                    "test_fr8_arvore", "def456", 1))
        db.execute("INSERT INTO arvore_rodada VALUES (?,?,?,?,?,?,?,?,?)",
                   ("R001", "task", "T5", "FR1", "T5: Board enxuto", "ok",
                    "painel/index.html", "1cb8468", 1))
        db.commit()

        result = server.v_rodadas(db, rodada_id="R001")
        self.assertIn("arvore", result)
        nos = result["arvore"]
        self.assertTrue(any(n["id_no"] == "FR1" for n in nos))
        self.assertTrue(any(n["id_no"] == "FR8" for n in nos))
        self.assertTrue(any(n["id_no"] == "T5" for n in nos))

    def test_no_descoberto_sem_teste(self):
        """FR10: requisito sem teste ligado → status='descoberto'."""
        ingest.ingere(self.cfg, self.db)
        db = server.conecta(self.db)
        self.cria_tabelas_065(db)
        db.execute("INSERT INTO rodadas VALUES (?,?,?,?,?,?)",
                   ("R001", "Workflow painel", "Gerente",
                    "2026-10-02T10:00:00-03:00", None, "specs/064/spec.md"))
        db.execute("INSERT INTO arvore_rodada VALUES (?,?,?,?,?,?,?,?,?)",
                   ("R001", "spec", "FR7", None, "FR7: evidência ≠ hash",
                    "descoberto", None, None, 0))
        db.commit()

        result = server.v_rodadas(db, rodada_id="R001")
        no = next(n for n in result["arvore"] if n["id_no"] == "FR7")
        self.assertEqual(no["status"], "descoberto")

    def test_arvore_sem_tabela_nao_quebra(self):
        """Graceful fallback: v_rodadas funciona sem arvore_rodada."""
        ingest.ingere(self.cfg, self.db)
        db = server.conecta(self.db)
        result = server.v_rodadas(db, rodada_id="R001")
        self.assertIn("arvore", result)
        self.assertEqual(result["arvore"], [])


class T8RoadmapRaias(Fixture):
    """T8: Roadmap com raias por ciclo (FR11)."""

    def test_roadmap_retorna_raias_por_ciclo(self):
        """FR11: roadmap retorna raias: atual, próximo, depois."""
        ingest.ingere(self.cfg, self.db)
        db = server.conecta(self.db)
        self.cria_tabelas_065(db)
        db.execute("INSERT INTO rodadas VALUES (?,?,?,?,?,?)",
                   ("R001", "Workflow painel", "Gerente",
                    "2026-10-02T10:00:00-03:00", None, "specs/064/spec.md"))
        db.execute("INSERT INTO rodadas VALUES (?,?,?,?,?,?)",
                   ("R002", "Board navegável", "Gerente",
                    "2026-10-02T14:00:00-03:00", None, "specs/065/spec.md"))
        db.commit()

        result = server.v_roadmap(db)
        self.assertIn("raias", result)
        raias = result["raias"]
        self.assertTrue(any(r["ciclo"] == "atual" for r in raias))
        self.assertTrue(any(r["ciclo"] in ("proximo", "próximo") for r in raias))

    def test_roadmap_card_tem_progresso(self):
        """FR11: cada card tem barra de progresso dos 15 passos."""
        ingest.ingere(self.cfg, self.db)
        db = server.conecta(self.db)
        self.cria_tabelas_065(db)
        db.execute("INSERT INTO rodadas VALUES (?,?,?,?,?,?)",
                   ("R001", "Workflow painel", "Gerente",
                    "2026-10-02T10:00:00-03:00", None, "specs/064/spec.md"))
        # 12 passos concluídos de 15
        for i in range(12):
            db.execute("INSERT INTO passos (rodada, passo, sessao, entrada_em, saida_em, resultado) VALUES (?,?,?,?,?,?)",
                       ("R001", f"T{i+1}", "W03", "2026-10-02T10:00:00-03:00",
                        "2026-10-02T11:00:00-03:00", "ok"))
        db.commit()

        result = server.v_roadmap(db)
        raias = result["raias"]
        cards = [c for r in raias for c in r.get("cards", [])]
        self.assertTrue(len(cards) > 0)
        card = next(c for c in cards if c["id"] == "R001")
        self.assertIn("passos_concluidos", card)
        self.assertIn("passos_total", card)
        self.assertEqual(card["passos_total"], 15)
        self.assertEqual(card["passos_concluidos"], 12)
