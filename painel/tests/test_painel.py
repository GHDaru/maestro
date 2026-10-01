"""Tests for the Maestro painel (stdlib unittest; run: python -m unittest discover painel/tests)."""
import builtins
import json
import os
import re
import sqlite3
import subprocess
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
        escreve(os.path.join(r, "proj/.env"), "DATABASE_URL=postgresql://user:SEGREDO@10.0.0.1/db\n")
        escreve(os.path.join(r, "backups_producao/x/pessoas.json"), '{"cpf":"000"}')
        escreve(os.path.join(r, "esp/equipe/WORKER-04.md"),
                "# Worker04\n\n## Estado atual (30/09, 23:45)\n\n- **Papel:** DDD\n- **Worktree:** wt-w04-x\n- **Último hash:** `05b5e17`\n- **Próximo passo:** aguardar\n\n## Estado anterior\n- velho\n")
        escreve(os.path.join(r, "esp/decisoes-a.md"),
                "# D\n\n| # | Hora | Decisão | Contexto e motivo | Como desfazer |\n|---|---|---|---|---|\n| D1 | 10:00 | **Fazer X** | porque sim | reverter |\n")
        escreve(os.path.join(r, "esp/retro.md"),
                "| When | Who | What happened | Rule involved | What was done | Candidate for the method |\n|---|---|---|---|---|---|\n| 30/09 | W05 | teste e código no mesmo commit, sem fase red | Princípio IV | devolvido | red antes |\n")
        escreve(os.path.join(r, "esp/ddd.md"), "### A5\n\n| Termo | Definição | Evitar |\n|---|---|---|\n| Gate | Estágio T0..T5 | fase |\n")
        escreve(os.path.join(r, "esp/barra/execucoes/20260930_2149_dev_603c44e/relatorio.md"),
                "# Barra\n\n**Veredito: PASSA.** 96 passos, 0 com erro; 0 linhas.\n")
        escreve(os.path.join(r, "specs/001-a/spec.md"), "# Spec A\n\n**Status**: Implementada\n")
        escreve(os.path.join(r, "specs/001-a/tasks.md"), "- [x] T1\n- [ ] T2\n")
        cfg = {"projeto": "t", "raiz": ".", "equipe": "esp/equipe", "decisoes": ["esp/decisoes-*.md"],
               "retro": ["esp/retro.md"], "glossario": ["esp/ddd.md"], "barra_execucoes": "esp/barra/execucoes",
               "specs": [{"nome": "p", "caminho": "specs"}],
               "documentos": {"constituicao": ["proj/.env", "esp/*.md"], "prod": ["backups_producao/**/*.json"]}}
        self.cfg_path = os.path.join(r, "p.json")
        escreve(self.cfg_path, json.dumps(cfg))
        self.cfg = ingest.carrega_cfg(self.cfg_path)
        self.db = os.path.join(r, "t.db")

    def tearDown(self):
        self.tmp.cleanup()


class Seguranca(Fixture):
    def test_ingestao_nunca_abre_env_nem_backups(self):
        abertos = []
        orig = builtins.open

        def espia(f, *a, **k):
            abertos.append(str(f))
            return orig(f, *a, **k)

        builtins.open = espia
        try:
            ingest.ingere(self.cfg, self.db)
        finally:
            builtins.open = orig
        self.assertFalse([a for a in abertos if a.replace("\\", "/").endswith("/.env")], abertos)
        self.assertFalse([a for a in abertos if "backups_producao" in a], abertos)

    def test_ler_recusa_caminho_proibido(self):
        with self.assertRaises(PermissionError):
            ingest.ler(os.path.join(self.raiz, "proj/.env"))
        with self.assertRaises(PermissionError):
            ingest.ler(os.path.join(self.raiz, "backups_producao/x/pessoas.json"))

    def test_sqlite_sem_segredo_nem_ip(self):
        ingest.ingere(self.cfg, self.db)
        con = sqlite3.connect(self.db)
        dump = "\n".join(con.iterdump())
        self.assertNotIn("SEGREDO", dump)
        self.assertNotIn("postgresql://", dump)
        self.assertIsNone(re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", dump))

    def test_ingestao_nunca_escreve_nos_arquivos(self):
        modos = []
        orig = builtins.open

        def espia(f, mode="r", *a, **k):
            if str(f) != self.db:
                modos.append(mode)
            return orig(f, mode, *a, **k)

        builtins.open = espia
        try:
            ingest.ingere(self.cfg, self.db)
        finally:
            builtins.open = orig
        self.assertTrue(all(m.startswith("r") for m in modos), modos)


class AppendOnly(Fixture):
    def test_eventos_recusam_update_e_delete(self):
        db = ingest.abre(self.db)
        server.grava_evento(db, {"tipo": "status", "sessao": "W04", "estado": "trabalhando", "autor": "t"})
        with self.assertRaises(sqlite3.DatabaseError):
            db.execute("UPDATE eventos SET estado='sem tarefa'")
        with self.assertRaises(sqlite3.DatabaseError):
            db.execute("DELETE FROM eventos")

    def test_reingestao_preserva_eventos_e_e_idempotente(self):
        ingest.ingere(self.cfg, self.db)
        db = ingest.abre(self.db)
        server.grava_evento(db, {"tipo": "deploy", "estado": "SUCCESS", "texto": "x", "autor": "Office"})
        db.close()

        def derivadas():
            c = sqlite3.connect(self.db)
            out = {t: c.execute(f"SELECT * FROM {t} ORDER BY 1").fetchall()
                   for t in ("sessoes", "decisoes", "desvios", "glossario", "barra_execucoes", "specs")}
            c.close()
            return out

        a = derivadas()
        ingest.ingere(self.cfg, self.db)
        self.assertEqual(a, derivadas())
        c = sqlite3.connect(self.db)
        self.assertEqual(c.execute("SELECT COUNT(*) FROM eventos").fetchone()[0], 1)


class SemProvaNaoMove(unittest.TestCase):
    def test_peca_sem_evidencia_e_recusada(self):
        self.assertIn("runner2", server.valida_evento(
            {"tipo": "peca", "peca": "P6", "estado": "suites aceitas", "evidencia": '{"hash":"bf2916c"}', "autor": "x"}))
        self.assertIn("descricao_factual", server.valida_evento(
            {"tipo": "peca", "peca": "P6", "estado": "aprovada as cegas",
             "evidencia": '{"hash":"a","par_montado_por":"Assistente"}', "autor": "x"}))
        self.assertIsNone(server.valida_evento(
            {"tipo": "peca", "peca": "P6", "estado": "suites aceitas",
             "evidencia": '{"hash":"bf2916c","runner2":"1646+775"}', "autor": "x"}))

    def test_status_so_com_vocabulario_fechado_e_autor(self):
        self.assertIsNotNone(server.valida_evento({"tipo": "status", "estado": "ok ✅", "autor": "x"}))
        self.assertIsNotNone(server.valida_evento({"tipo": "status", "estado": "trabalhando"}))


class Extracao(Fixture):
    def test_extrai_fontes(self):
        ingest.ingere(self.cfg, self.db)
        c = sqlite3.connect(self.db)
        s = c.execute("SELECT nome, papel, worktree, ultimo_hash, estado_em FROM sessoes").fetchone()
        self.assertEqual(s, ("W04", "DDD", "wt-w04-x", "05b5e17", "30/09, 23:45"))
        self.assertEqual(c.execute("SELECT id, titulo, desfazer FROM decisoes").fetchone(), ("D1", "Fazer X", "reverter"))
        self.assertEqual(c.execute("SELECT classe FROM desvios").fetchone()[0], "TDD / teste antes")
        self.assertEqual(c.execute("SELECT veredito, passos, passos_com_erro, ambiente, hash FROM barra_execucoes").fetchone(),
                         ("PASSA", 96, 0, "dev", "603c44e"))
        self.assertEqual(c.execute("SELECT status, tasks_total, tasks_feitas FROM specs").fetchone(), ("Implementada", 2, 1))
        self.assertEqual(c.execute("SELECT termo, evitar FROM glossario").fetchone(), ("Gate", "fase"))

    def test_dora_nao_conta_merge_como_deploy(self):
        ingest.ingere(self.cfg, self.db)
        d = server.v_dora(server.conecta(self.db), 30)
        self.assertIsNone(d["metricas"]["frequencia_deploy"]["valor"])
        self.assertTrue(any("merge na main não é deploy" in n for n in d["notas"]))


class Mcp(Fixture):
    def test_mcp_lista_ferramentas_e_recusa_peca_sem_prova(self):
        import mcp_painel
        ingest.ingere(self.cfg, self.db)
        nomes = [t["name"] for t in mcp_painel.responde({"id": 1, "method": "tools/list"}, self.db)["tools"]]
        self.assertEqual(nomes, ["estado_atual", "registrar_status", "registrar_peca"])
        r = mcp_painel.responde({"id": 2, "method": "tools/call", "params": {"name": "registrar_peca", "arguments": {
            "peca": "P", "estado": "integrada", "evidencia": {"hash": "a"}, "autor": "t"}}}, self.db)
        self.assertTrue(r.get("isError"))
        r = mcp_painel.responde({"id": 3, "method": "tools/call", "params": {"name": "registrar_status", "arguments": {
            "sessao": "W04", "estado": "trabalhando", "texto": "x", "autor": "W04"}}}, self.db)
        self.assertFalse(r.get("isError"))
        r = mcp_painel.responde({"id": 4, "method": "tools/call", "params": {"name": "estado_atual", "arguments": {"sessao": "W04"}}}, self.db)
        self.assertEqual(json.loads(r["content"][0]["text"])["voce"]["estado"], "trabalhando")


class HigieneGit(unittest.TestCase):
    def test_detecta_branch_com_upstream_na_main(self):
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as r:
            g = lambda *a: subprocess.run(["git", "-C", r, *a], capture_output=True, check=True)
            g("init", "-q", "-b", "main")
            g("-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q", "--allow-empty", "-m", "c0")
            g("remote", "add", "origin", r)
            g("fetch", "-q", "origin")
            g("branch", "-q", "perigo", "origin/main")  # tracks origin/main: git push goes to main
            g("branch", "-q", "segura")
            cfg = {"raiz": r, "repos": [{"nome": "x", "caminho": r, "principal": "main"}]}
            db = sqlite3.connect(":memory:")
            db.executescript(ingest.DERIVADAS)
            ingest.ingere_worktrees(db, cfg)
            self.assertEqual(db.execute("SELECT branch FROM branches_risco").fetchall(), [("perigo",)])


if __name__ == "__main__":
    unittest.main()
