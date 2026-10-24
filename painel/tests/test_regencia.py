"""Painel de regência — testes VERMELHOS de T0 (ciclo 072, rodada 1).

Princípio IV: o teste nasce antes do código. Estes testes DEVEM falhar agora, pela razão
certa — a tela, o módulo e as rotas do painel de regência ainda não existem — e ficar
verdes quando existirem. Nada aqui implementa `painel/regencia.py`, `server.py` nem
`index.html`: só especifica o comportamento a partir dos critérios de aceite da
`specs/072-painel-de-regencia/spec.md` (revisão T01b, gate DoR) e do `ux-design.md` §7 (F1–F10).

As regras do conferidor (ciclos 068/069) NÃO são reimplementadas: os testes consomem
`painel/chamados.py` (`confere`, `ordem_veredito`, `cabecalho`, `valida`, `GATES`).

Contrato assumido (a spec fixa o COMPORTAMENTO; o plano fixa os NOMES de módulo/rota —
`specs/072-painel-de-regencia/spec.md` § "Para o plano", item 4). O módulo de regras é
importado como `regencia` (i.e. `painel/regencia.py` ou o pacote `painel/regencia/`).
Onde a spec não fixa um nome de função, o teste aceita os candidatos do vocabulário dela
via `_fn(...)`; a falha lista o que se procurou, para o plano casar o nome:

    normaliza(valor)                 -> canônico (str) — aceita str ou mapping {"veredito","erros"}
    sai_da_fila(pedido, rulings)     -> bool          — True se há ruling do pedido (FR12)
    cartao(chamado)                  -> {"chamado", "gate", "faltas"}  (FR2/FR3)
    proposta_transicao(chamado, dst) -> None; ValueError(motivo) sem arquivo de gate válido (FR8)
    valida_ruling(ruling)            -> motivo (str) se recusado, senão None (FR14)
    registra(caminho, registro)      -> acrescenta 1 linha JSONL (FR16)
    idade(quando, agora=None, declarado=False) -> {"texto", "carimbo", "selo"} (FR23)
    cabecalho_fila(fila, agora=None) -> {"n", "mais_velho"}                    (FR23)
    sem_fonte(motivo, caminho="")    -> "— (motivo: …, caminho: …)"            (FR22)
    aviso_ingestao(ingerido_em, agora=None) -> "defasado …" ou falsy           (FR25)
    portoes_do_regente(chamado, commit_de=None) -> [{"id","gate","status","desde","somente_leitura"}] (FR20)
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import sqlite3
import sys
import tempfile
import threading
import unittest
from html import unescape
from http.server import ThreadingHTTPServer
from urllib import request as urlreq

AQUI = os.path.dirname(os.path.abspath(__file__))
PAINEL = os.path.dirname(AQUI)
sys.path.insert(0, PAINEL)
import chamados  # noqa: E402
import server  # noqa: E402

TZ = dt.timezone(dt.timedelta(hours=-3))
# O conferidor resolve o hash do 'objeto' contra o git; aqui a fixture fixa o hash e a data.
HASHES = {"aaaaaaa": dt.datetime(2026, 10, 5, 20, 36, tzinfo=TZ)}
data_hash = HASHES.get
SCHEMA_SQL = os.path.join(PAINEL, "schema_workflow.sql")
AGORA = dt.datetime(2026, 10, 24, 12, 0, tzinfo=TZ)


# ---------- o módulo de regras ainda não existe: falhar pela razão certa ----------

def _mod():
    """Importa o módulo de regras da regência. O plano fixa o nome; hoje não existe."""
    try:
        import regencia
        return regencia
    except ImportError as e:
        raise AssertionError(
            "painel/regencia.py ainda não existe: o módulo de regras da regência (o plano "
            "fixa o nome — spec 072, 'Para o plano', item 4) precisa existir para este teste."
        ) from e


def _fn(*nomes):
    """Resolve uma função do módulo de regras pelos candidatos do vocabulário da spec."""
    mod = _mod()
    for n in nomes:
        f = getattr(mod, n, None)
        if callable(f):
            return f
    raise AssertionError(
        "painel/regencia.py não expõe nenhuma de: " + ", ".join(nomes)
        + " (o plano fixa o nome; a spec fixa o comportamento)."
    )


def _escreve(caminho, texto):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(texto)


# ---------- fixtures do chamado (cabeçalhos de gate no padrão do 068) ----------

ABERTURA = """---
gate: abertura
tipo: bug
escopo: correcao
aberto_por: Cliente
origem: staging
data: 2026-10-05 18:13 -0300
autores: W09
---
# Chamado da fixture 072
"""


def _gate(gid, veredito, por="W13", papel="", data="2026-10-05 21:00 -0300",
          objeto="src/x.py @ aaaaaaa", data_objeto="2026-10-05 20:36 -0300", extra=""):
    p = f"papel: {papel}\n" if papel else ""
    return (f"---\ngate: {gid}\n{p}objeto: {objeto}\nveredito: {veredito}\npor: {por}\n"
            f"data: {data}\ndata_objeto: {data_objeto}\n{extra}---\n")


def _chamado_ate_g2():
    """G0/G1/G2 aprovados; G3 ausente. O cartão tem de ficar em G2 (F2)."""
    arqs = {
        "00-chamado.md": ABERTURA,
        "G0-reproducao-aaaaaaa.md": _gate("G0", "REPRODUZIDO", por="W07"),
        "G1-spec-W13.md": _gate("G1", "APPROVE", por="W13"),
        "G2-vermelho-aaaaaaa.md": _gate("G2", "FALHA_ESPERADA", por="W07"),
    }
    r = chamados.confere(arqs, data_hash, True)
    r["id"] = "072-teste-f2"
    return r


def _chamado_com_portoes():
    """G0–G6 aprovados; G7 (aceite) e G8 (ordem) pendentes por arquivo de gate (FR20)."""
    arqs = {
        "00-chamado.md": ABERTURA,
        "G0-reproducao-aaaaaaa.md": _gate("G0", "REPRODUZIDO", por="W07"),
        "G1-spec-W13.md": _gate("G1", "APPROVE", por="W13"),
        "G2-vermelho-aaaaaaa.md": _gate("G2", "FALHA_ESPERADA", por="W07"),
        "G3-codigo-W13-aaaaaaa.md": _gate("G3", "APPROVE", por="W13", papel="codigo"),
        "G3-criterio-W11-aaaaaaa.md": _gate("G3", "APPROVE", por="W11", papel="criterio"),
        "G3-runner2-W07-aaaaaaa.md": _gate("G3", "OK", por="W07", papel="runner2",
                                           extra='numeros: "pytest 10/0/0"\n'),
        "G4-vm.md": _gate("G4", "OK", por="Office"),
        "G5-barra.md": _gate("G5", "PASSA", por="Office"),
        "G6-tela.md": _gate("G6", "PASSA", por="Testes"),
        "G7-aceite.md": _gate("G7", "PENDENTE", por="Cliente"),
        "G8-ordem.md": _gate("G8", "PENDENTE", por="Gilsiley"),
    }
    r = chamados.confere(arqs, data_hash, True,
                         {"G7-aceite.md": "2026-10-05T21:10:00-03:00",
                          "G8-ordem.md": "2026-10-05T21:12:00-03:00"})
    r["id"] = "072-teste-portao"
    return r


# ---------- servidor local (HTML renderizado e rota de escrita) ----------

class _Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.raiz = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    def _cfg(self):
        return {"projeto": "teste", "raiz": self.raiz, "equipes": {}, "repos": [],
                "specs": [], "documentos": {}, "chamados": [{"repo": ".", "pasta": "specs", "dias": 14}]}

    def _sobe(self):
        """Sobe o painel numa porta efêmera e devolve (servidor, url base)."""
        db = os.path.join(self.raiz, "painel.db")
        srv = ThreadingHTTPServer(("127.0.0.1", 0), server.cria_handler(db, self._cfg()))
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        self.addCleanup(srv.shutdown)
        return srv, f"http://127.0.0.1:{srv.server_address[1]}"

    @staticmethod
    def _get(url):
        with urlreq.urlopen(url, timeout=15) as r:
            return r.read().decode("utf-8")

    def _foto_da_arvore(self):
        """Bytes de cada arquivo sob self.raiz, para provar que nada mudou (FR9)."""
        foto = {}
        for base, _, arquivos in os.walk(self.raiz):
            for n in arquivos:
                p = os.path.join(base, n)
                with open(p, "rb") as f:
                    foto[os.path.relpath(p, self.raiz)] = f.read()
        return foto


# ---------- F1 / F9: fitness functions sobre o HTML renderizado ----------

RE_METRICA = re.compile(r"<[a-zA-Z][^>]*?\bclass\s*=\s*[\"'][^\"']*\bmetrica\b[^\"']*[\"'][^>]*>", re.I)
RE_BOTAO = re.compile(r"<button\b([^>]*)>(.*?)</button>", re.I | re.S)
RE_ROTULO_REGENCIa = re.compile(
    r"aria-label\s*=\s*[\"'][^\"']*(responder|devolver|arrastar|abrir|evid[êe]ncia)", re.I)


def _texto_do_botao(inner):
    """Texto visível do <button>, sem tags e com interpolação tratada como texto."""
    t = re.sub(r"<[^>]+>", " ", inner)
    t = re.sub(r"\$\{[^}]*\}", " x ", t)
    return unescape(t).strip()


class TestF1MetricaComFonte(_Base):
    def test_f1_metrica_sem_data_fonte_zero_no_html_renderizado(self):
        """F1/FR21: todo número/selo do painel traz `data-fonte` com o comando ou caminho."""
        srv, url = self._sobe()
        html = self._get(url + "/")
        tags = RE_METRICA.findall(html)
        self.assertTrue(tags, "a tela de regência ainda não existe: nenhum elemento `.metrica` "
                              "no HTML renderizado do painel.")
        sem_fonte = [t for t in tags if not re.search(r"\bdata-fonte\b", t, re.I)]
        self.assertEqual(sem_fonte, [],
                         "F1: todo número/selo exibido precisa carregar `data-fonte` (FR21).")


class TestF9BotaoSoIcone(_Base):
    def test_f9_botao_so_icone_com_aria_label_no_html_renderizado(self):
        """F9/FR24: nenhum controle só-ícone sem `aria-label` (verbo + objeto)."""
        srv, url = self._sobe()
        html = self._get(url + "/")
        botoes = RE_BOTAO.findall(html)
        self.assertTrue(botoes, "o painel não serviu nenhum <button> — HTML inesperado.")
        sem_rotulo = [a for a, inner in botoes
                      if not _texto_do_botao(inner) and not re.search(r"aria-label", a, re.I)]
        self.assertEqual(sem_rotulo, [], "F9: botão só-ícone precisa de `aria-label` (FR24).")
        rotulados = [a for a, _ in botoes if RE_ROTULO_REGENCIa.search(a)]
        self.assertTrue(rotulados, "a tela de regência ainda não existe: nenhum controle só-ícone "
                                   "com `aria-label` de verbo+objeto (arrastar/responder/abrir evidência).")


# ---------- F2: o cartão está no último gate aprovado; arrasto exige arquivo válido ----------

class TestF2CartaoEmGn(unittest.TestCase):
    def test_f2_cartao_em_gn_exige_arquivo_do_gate(self):
        """F2 (FR2/FR8): G2 aprovado e G3 ausente → cartão em G2 e arrasto a G3 recusado."""
        chamado = _chamado_ate_g2()
        card = _fn("cartao", "cartao_do_chamado", "posicao_cartao", "kanban_cartao")(chamado)
        gate = card["gate"] if isinstance(card, dict) else card
        self.assertEqual(gate, "G2", "o cartão fica no último gate com veredito vigente aprovado (FR2).")

        proposta = _fn("proposta_transicao", "propoe_transicao", "transicao", "recusa_transicao")
        with self.assertRaises(ValueError) as ctx:
            proposta(chamado, "G3")
        msg = str(ctx.exception)
        self.assertIn("G3-*.md", msg, "F2: sem arquivo de gate, o arrasto é recusado na origem (FR8).")
        self.assertIn("cabeçalho válido", msg)


# ---------- F3: transição sem evidência devolve 422 e não toca arquivo algum ----------

class TestF3TransicaoSemArquivo(_Base):
    def test_f3_transicao_sem_arquivo_devolve_422(self):
        """F3 (FR9): POST /transicao sem arquivo de gate de destino válido → 422 com motivo."""
        _escreve(os.path.join(self.raiz, "specs/072-teste-f3/00-chamado.md"), ABERTURA)
        _escreve(os.path.join(self.raiz, "specs/072-teste-f3/G2-vermelho-aaaaaaa.md"),
                 _gate("G2", "FALHA_ESPERADA", por="W07"))
        antes = self._foto_da_arvore()

        srv, url = self._sobe()
        corpo = json.dumps({"chamado": "072-teste-f3", "gate": "G3", "destino": "G3"}).encode("utf-8")
        req = urlreq.Request(url + "/transicao", data=corpo,
                             headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urlreq.urlopen(req, timeout=15) as r:
                code, resposta = r.status, r.read().decode("utf-8")
        except urlreq.HTTPError as e:
            code, resposta = e.code, e.read().decode("utf-8")

        self.assertEqual(code, 422, "FR9: transição sem evidência responde 422 com o motivo "
                                    f"(recebido {code}: {resposta}).")
        self.assertTrue("motivo" in resposta.lower() or "erro" in resposta.lower(), resposta)
        self.assertEqual(self._foto_da_arvore(), antes, "FR9: nenhum arquivo muda na recusa.")


# ---------- F4: pedido sem ruling nunca sai da fila ----------

class TestF4Fila(unittest.TestCase):
    def test_f4_pedido_sem_ruling_fica_na_fila(self):
        """F4 (FR12): 3 pedidos, 1 ruling → 2 continuam na fila."""
        pedidos = [{"id": "D-001"}, {"id": "D-002"}, {"id": "D-003"}]
        rulings = [{"id": "R-001", "pedido": "D-002", "autor": "Darú", "destino": "W03", "texto": "ok"}]
        sai = _fn("sai_da_fila")
        fila = [p for p in pedidos if not sai(p, rulings)]
        self.assertEqual([p["id"] for p in fila], ["D-001", "D-003"], "FR12: só o ruling tira da fila.")
        self.assertFalse(sai(pedidos[0], rulings))
        self.assertTrue(sai(pedidos[1], rulings))


# ---------- F5: ruling sem autor humano ou destino é recusado ----------

class TestF5Ruling(unittest.TestCase):
    def test_f5_ruling_sem_autor_humano_ou_destino_e_recusado(self):
        """F5 (FR14): sem destino ou sem autor humano (pessoa) → recusado; delegação registra quem lançou."""
        valida = _fn("valida_ruling", "valida_ruling_humano")
        sem_destino = valida({"id": "R-1", "pedido": "D-1", "texto": "sim", "autor": "Darú"})
        self.assertTrue(sem_destino, "FR14: ruling sem destinatário é recusado.")
        self.assertIn("destino", sem_destino.lower())
        sem_autor = valida({"id": "R-2", "pedido": "D-1", "texto": "sim", "destino": "W03"})
        self.assertTrue(sem_autor, "FR14: ruling sem autor humano é recusado.")
        self.assertIn("autor", sem_autor.lower())
        self.assertFalse(valida({"id": "R-3", "pedido": "D-1", "texto": "sim",
                                 "autor": "Darú", "destino": "W03"}))
        # decisão do Darú (1a): a delegação registra quem lançou, sem confundir a autoria
        self.assertFalse(valida({"id": "R-4", "pedido": "D-1", "texto": "sim", "autor": "Darú",
                                 "destino": "W03", "registrado_por": "Office",
                                 "delegacao": "decisao-072-gates-delegados"}))


# ---------- F6: normalização tabela-dirigida ----------

class TestF6Normalizacao(unittest.TestCase):
    def test_f6_normalizacao_tabela_dirigida(self):
        """F6 (FR10): tabela fixa; qualquer outro valor cai em 'inválido' com o original visível."""
        normaliza = _fn("normaliza", "normaliza_veredito", "veredito_normalizado")
        tabela = [("APPROVE", "aprovado"), ("OK", "aprovado"), ("PASSA", "aprovado"), ("PASSOU", "aprovado"),
                  ("RETURN", "devolvido"), ("REPROVE", "devolvido"), ("FALHA", "devolvido"),
                  ("FALHA_ESPERADA", "vermelho provado"),
                  ("PENDENTE", "em curso"), ("REPRODUZIDO", "em curso"),
                  ("NÃO PASSA", "inválido"), ("DESCONHECIDO", "inválido"), ("", "inválido")]
        for valor, canon in tabela:
            self.assertEqual(normaliza(valor), canon, f"normaliza({valor!r})")
        # cabeçalho reprovado pelo conferidor (068) → inválido, sem reescrever o arquivo
        self.assertEqual(normaliza({"veredito": "APPROVE", "erros": ["falta 'por' no cabeçalho"]}),
                         "inválido", "FR10: cabeçalho reprovado normaliza como 'inválido'.")


# ---------- F7: idade vem do relógio/timestamp, com carimbo e selo ----------

class TestF7Idade(unittest.TestCase):
    def test_f7_idade_do_relogio_e_carimbo(self):
        """F7 (FR23): idade do relógio/registro, 'há Xh Ymin' + carimbo absoluto; digitada = 'declarada'."""
        idade = _fn("idade", "idade_do_pedido", "idade_item")
        # 2026-10-24 04:48 -0300 → 7 h 12 min antes de AGORA (12:00 -0300)
        r = idade("2026-10-24T04:48:00-03:00", AGORA)
        self.assertIn("7 h 12 min", r["texto"] if isinstance(r, dict) else str(r),
                      "FR23: a idade aparece como 'há 7 h 12 min'.")
        self.assertTrue(r["carimbo"] if isinstance(r, dict) else False,
                        "FR23: a idade aparece também como carimbo absoluto.")
        self.assertNotEqual((r or {}).get("selo"), "declarada",
                            "idade do relógio/registro não é 'declarada'.")
        declarada = idade("2026-10-20T07:04:00-03:00", AGORA, declarado=True)
        self.assertEqual(declarada["selo"], "declarada",
                         "FR23: data escrita à mão em arquivo aparece com o selo 'declarada'.")
        # contador no cabeçalho com a idade do item mais velho da fila
        fila = [{"id": "D-1", "criado_em": "2026-10-24T04:48:00-03:00"},
                {"id": "D-2", "criado_em": "2026-10-24T11:00:00-03:00"}]
        cab = _fn("cabecalho_fila", "contador_fila", "resumo_fila", "cabecalho")(fila, AGORA)
        self.assertEqual(cab["n"], len(fila))
        self.assertIn("mais_velho", cab)


# ---------- F8: "—" sempre com motivo ----------

class TestF8Traco(unittest.TestCase):
    def test_f8_traco_com_motivo(self):
        """F8 (FR22): fonte ausente → '—' com o motivo e o caminho; nunca '0' nem 'n/a'."""
        sem_fonte = _fn("sem_fonte", "traco", "valor_ou_traco", "com_motivo")
        t = sem_fonte("limite de idade não tem fonte", "padrao-chamado.md")
        self.assertIn("—", t)
        self.assertIn("motivo:", t)
        self.assertIn("padrao-chamado.md", t)


# ---------- F10: ingestão defasada é anunciada ----------

class TestF10IngestaoDefasada(unittest.TestCase):
    def test_f10_ingestao_defasada_anunciada(self):
        """F10 (FR25): meta.ingerido_em com mais de 1 h → cabeçalho anuncia 'defasado'."""
        aviso = _fn("aviso_ingestao", "cabecalho_ingestao", "ingestao_defasada", "defasado")

        def anuncia(v):
            if isinstance(v, str):
                return "defasado" in v.lower()
            if isinstance(v, dict):
                return "defasado" in json.dumps(v, ensure_ascii=False).lower()
            return v is True

        velho = aviso("2026-10-24T00:00:00-03:00", AGORA)  # 12 h
        novo = aviso("2026-10-24T11:30:00-03:00", AGORA)   # 30 min
        self.assertTrue(anuncia(velho), "FR25: ingestão com mais de 1 h é anunciada como 'defasada'.")
        self.assertFalse(anuncia(novo), "FR25: ingestão recente não é anunciada como defasada.")


# ---------- FR16: o registro da fila só cresce (append-only mecânico) ----------

class TestF14AppendOnly(_Base):
    def test_f14_registro_append_only_so_cresce(self):
        """FR16: acrescentar linha mantém inalterado o prefixo de bytes — o arquivo só cresce."""
        registra = _fn("registra", "acrescenta", "append_jsonl", "acrescenta_registro",
                       "registra_pedido", "registra_ruling")
        caminho = os.path.join(self.raiz, "fila.jsonl")
        with open(caminho, "w", encoding="utf-8") as f:
            f.write('{"id": "D-001", "tipo": "pedido"}\n')
        with open(caminho, "rb") as f:
            antes = f.read()
        registra(caminho, {"id": "D-002", "tipo": "ruling", "pedido": "D-001"})
        with open(caminho, "rb") as f:
            depois = f.read()
        self.assertTrue(depois.startswith(antes), "FR16: o prefixo de bytes anterior não muda.")
        self.assertGreater(len(depois), len(antes), "FR16: o arquivo cresce.")
        linhas = [l for l in depois.decode("utf-8").splitlines() if l.strip()]
        self.assertEqual(len(linhas), 2, "FR16: exatamente uma linha foi acrescentada.")
        self.assertEqual(json.loads(linhas[0])["id"], "D-001")
        self.assertEqual(json.loads(linhas[1])["id"], "D-002")


# ---------- FR17 (dívida 5 do 070): gatilho recusa UPDATE/DELETE ----------

class TestDivida5Gatilho(unittest.TestCase):
    def test_divida5_gatilho_recusa_update_e_delete(self):
        """FR17: append-only imposto por TRIGGER em rodadas/passos/transicoes, não por convenção."""
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as r:
            db = os.path.join(r, "workflow.db")
            con = sqlite3.connect(db)
            try:
                with open(SCHEMA_SQL, encoding="utf-8") as f:
                    con.executescript(f.read())
                con.execute("INSERT INTO rodadas (id, desejo, criada_por, aberta_em) "
                            "VALUES ('001', 'd', 'W09', '2026-10-22T16:00:00+00:00')")
                con.execute("INSERT INTO passos (rodada, passo, sessao, entrada_em) "
                            "VALUES ('001', 'T1', 'W09', '2026-10-22T16:01:00+00:00')")
                con.execute("INSERT INTO transicoes (passo, proximo, evidencia_exigida) "
                            "VALUES ('T1', 'T2', 1)")
                con.commit()
                tentativas = [("rodadas", "UPDATE rodadas SET desejo='x'"),
                              ("rodadas", "DELETE FROM rodadas"),
                              ("passos", "UPDATE passos SET resumo='x'"),
                              ("passos", "DELETE FROM passos"),
                              ("transicoes", "UPDATE transicoes SET evidencia_exigida=0"),
                              ("transicoes", "DELETE FROM transicoes")]
                for tabela, sql in tentativas:
                    with self.assertRaises(sqlite3.DatabaseError,
                                           msg=f"FR17: {tabela} aceitou '{sql}' — falta o TRIGGER."):
                        con.execute(sql)
                        con.commit()
            finally:
                con.close()


# ---------- FR20: portão do regente pendente é item da fila com id derivado ----------

class TestPortaoRegente(unittest.TestCase):
    def test_portao_do_regente_item_com_id_derivado(self):
        """FR20: G7/G8 pendentes viram itens da fila com id derivado (chamado+gate), status e 'desde'."""
        chamado = _chamado_com_portoes()
        commit_de = {"G7-aceite.md": "2026-10-05T21:10:00-03:00",
                     "G8-ordem.md": "2026-10-05T21:12:00-03:00"}
        itens = _fn("portoes_do_regente", "portao_do_regente", "portoes_pendentes")(chamado, commit_de)
        por_gate = {i["gate"]: i for i in itens}
        for g, arquivo in (("G7", "G7-aceite.md"), ("G8", "G8-ordem.md")):
            self.assertIn(g, por_gate, f"FR20: o portão {g} pendente tem de virar item da fila.")
            it = por_gate[g]
            self.assertIn(chamado["id"], it["id"], "FR20: o id do item é derivado do chamado.")
            self.assertIn(g, it["id"], "FR20: o id do item é derivado do gate.")
            self.assertTrue(it.get("status") or it.get("estado"),
                            "FR20: o item lê o status do arquivo de gate.")
            self.assertTrue(it.get("somente_leitura") or it.get("permissao") == "leitura",
                            "FR20: a um agente, o portão do regente aparece como somente leitura.")
            self.assertIn("2026-10-05", str(it.get("desde") or it.get("desde_quando") or ""),
                          "FR20: o 'desde quando' vem do commit do arquivo de gate.")


if __name__ == "__main__":
    unittest.main()
