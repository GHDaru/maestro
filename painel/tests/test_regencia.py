"""Painel de regência — testes de contrato do ciclo 072, rodada 1.

Princípio IV: o teste nasce antes do código. Estes testes DEVEM falhar agora, **pela razão
certa** — o pacote `painel/regencia/`, o adaptador `painel/fila_registro.py` e as rotas do
painel de regência ainda não existem — e ficar verdes quando existirem. Nada aqui implementa
`painel/regencia/`, `server.py` nem `index.html`: só especifica o comportamento.

**Reconciliação T03b (attempt=2, gate do plano APROVADO COM CONDIÇÕES).** Os testes foram
acertados com a tabela **"Nomes fixados"** de `plan.md` (o contrato do plano com os testes):
os nomes fixados mandam, e onde o teste antigo divergia, o teste **adapta** — declarado, nunca
em silêncio. Adaptados: **F2** (`proposta_transicao` devolve `{permitido, falta?}`, não
`ValueError`), **F3** (rota `/api/regencia/transicao`, corpo `{chamado, de, para}`), **F6**
(`normaliza(valor, erros=None)` devolve **dict** `{canonico, original, motivo?}`), **F7**
(`idade_do_carimbo`), **F9** (`${…}` não conta como texto de botão, D-072-8), **F14**
(importa o adaptador `fila_registro`) e o gatilho de FR17 (o `WHEN` de `passos`). Ampliados:
os 2 negativos de FR20, a prova estática (AST) e a concorrente de FR16, `ordena_fila` (FR15),
`cabecalho_fila` (FR23), `independencia` (FR4), o parser `autor_da_peca` (FR5), as dez colunas
G0–G9 (FR1), o filtro por frente (FR7) e a anatomia do pedido (FR11).

As regras do conferidor (ciclos 068/069/070) NÃO são reimplementadas: os testes consomem
`painel/chamados.py` (`confere`, `ordem_veredito`, `cabecalho`, `valida`, `GATES`).

Contrato assumido — o plano fixa os NOMES de módulo/função/rota; a spec fixa o COMPORTAMENTO
(`specs/072-painel-de-regencia/spec.md`, 25 FR; `plan.md` §"Nomes fixados"). Os testes resolvem
as funções **pelo pacote** `regencia` (i.e. `painel/regencia/`, que reexporta todos os nomes
públicos); o adaptador de escrita é importado como `fila_registro`. A falha lista o nome que se
procurou, para o implementador casar com a tabela do plano.
"""
from __future__ import annotations

import ast
import contextlib
import datetime as dt
import io
import json
import os
import re
import sqlite3
import subprocess
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


# ---------- o pacote puro e o adaptador ainda não existem: falhar pela razão certa ----------

def _mod():
    """Importa o pacote de regras da regência. O plano fixa o nome (`painel/regencia/`)."""
    try:
        import regencia
        return regencia
    except ImportError as e:
        raise AssertionError(
            "painel/regencia/ ainda não existe: o pacote puro da regência (normalizacao.py, "
            "kanban.py, fila.py — reexportados por __init__.py; plan.md §1) precisa existir "
            "para este teste."
        ) from e


def _fn(nome, *alternativos):
    """Resolve uma função do pacote puro: o nome fixado pelo plano vem primeiro."""
    mod = _mod()
    for n in (nome,) + alternativos:
        f = getattr(mod, n, None)
        if callable(f):
            return f
    raise AssertionError(
        "painel/regencia/ não expõe " + ", ".join((nome,) + alternativos)
        + " (o plano fixa o nome em §'Nomes fixados')."
    )


def _adapter(nome="fila_registro"):
    """Importa um adaptador do painel (o registro da fila vive FORA do pacote puro)."""
    try:
        return __import__(nome)
    except ImportError as e:
        raise AssertionError(
            f"painel/{nome}.py ainda não existe: o adaptador do registro da fila (plan.md §1 e "
            "§2 — corte hexagonal) precisa existir para este teste."
        ) from e


def _escreve(caminho, texto):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(texto)


def _vermelho(marcador):
    """Normaliza o marcador de independência (bool, dict ou string) para 'está vermelho?'."""
    if isinstance(marcador, dict):
        return bool(marcador.get("vermelho") or marcador.get("red"))
    if isinstance(marcador, str):
        return "vermelh" in marcador.lower()
    return marcador is True


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


def _repo_de_verdade(raiz):
    """Cria um repositório git REAL na fixture e devolve `(hash_curto, quando)`.

    O conferidor (`chamados._git` → `git log -1 --format=%ai <hash>`) resolve o hash do
    `objeto` contra o git da raiz. Sem repo real nenhum cabeçalho de gate fica válido, e sem
    cabeçalho válido não há como provar a transição PERMITIDA (F3/FR8) pela rota — o teste
    antigo só olhava o 422 e por isso passava até com o crash (R1/T06).
    """
    def g(*args):
        return subprocess.run(
            ["git", "-C", raiz, "-c", "user.email=teste@teste.invalid",
             "-c", "user.name=Teste", "-c", "commit.gpgsign=false", *args],
            capture_output=True, text=True, check=True).stdout.strip()

    g("init", "-q")
    _escreve(os.path.join(raiz, "src", "x.py"), "print(1)\n")
    g("add", "-A")
    g("commit", "-qm", "objeto do gate")
    return g("rev-parse", "HEAD")[:7], g("log", "-1", "--format=%ai")


def _gate_objeto(gid, veredito, por, hash_, quando, papel=""):
    """Cabeçalho de gate apontando para um `objeto` que EXISTE no repo (senão `valida` recusa)."""
    return _gate(gid, veredito, por=por, papel=papel, data=quando,
                 objeto=f"src/x.py @ {hash_}", data_objeto=quando)


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


# ---------- servidor local (HTML renderizado e rotas de leitura/escrita) ----------

class _Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.raiz = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    def _cfg(self):
        # Chaves novas desta rodada: `frentes` (FR7), `regencia.pessoas` (FR20) e o endereço do
        # registro da fila (FR16) apontado para dentro da fixture, para o teste poder lê-lo.
        return {"projeto": "teste", "raiz": self.raiz, "equipes": {}, "repos": [],
                "specs": [], "documentos": {},
                "chamados": [{"repo": ".", "pasta": "specs", "dias": 14}],
                "frentes": {"painel": ["specs/072-painel-de-regencia"]},
                "regencia": {"pessoas": ["Darú", "Gilsiley"]},
                "fila_decisoes": os.path.join(self.raiz, "fila.jsonl")}

    def _sobe(self):
        """Sobe o painel numa porta efêmera e devolve (servidor, url base)."""
        db = os.path.join(self.raiz, "painel.db")
        con = sqlite3.connect(db)
        try:  # o mínimo para as rotas de leitura de meta responderem 200 (não é o schema do painel)
            con.execute("CREATE TABLE IF NOT EXISTS meta (chave TEXT PRIMARY KEY, valor TEXT)")
            con.commit()
        finally:
            con.close()
        srv = ThreadingHTTPServer(("127.0.0.1", 0), server.cria_handler(db, self._cfg()))
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        self.addCleanup(srv.shutdown)
        return srv, f"http://127.0.0.1:{srv.server_address[1]}"

    @staticmethod
    def _get(url):
        with urlreq.urlopen(url, timeout=15) as r:
            return r.read().decode("utf-8")

    def _get_json(self, url, caminho):
        """GET de uma rota JSON; exige 200 e devolve o objeto (falha clara na recusa)."""
        try:
            with urlreq.urlopen(url + caminho, timeout=15) as r:
                return json.loads(r.read().decode("utf-8"))
        except urlreq.HTTPError as e:
            corpo = e.read().decode("utf-8")
            raise AssertionError(f"GET {caminho} → {e.code} (esperado 200): {corpo}") from e

    def _post_json(self, url, caminho, corpo):
        """POST de uma rota JSON; devolve (code, texto) sem levantar na recusa."""
        dados = json.dumps(corpo).encode("utf-8")
        req = urlreq.Request(url + caminho, data=dados,
                             headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urlreq.urlopen(req, timeout=15) as r:
                return r.status, r.read().decode("utf-8")
        except urlreq.HTTPError as e:
            return e.code, e.read().decode("utf-8")

    def _grava_meta(self, chave, valor):
        """Escreve uma linha em `meta` no banco da fixture (072-T16: as rotas releem a cada request)."""
        con = sqlite3.connect(os.path.join(self.raiz, "painel.db"))
        try:
            con.execute("INSERT OR REPLACE INTO meta (chave, valor) VALUES (?, ?)", (chave, valor))
            con.commit()
        finally:
            con.close()

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
    """Texto visível do <button>, sem tags; a interpolação `${…}` NÃO conta como texto (D-072-8)."""
    t = re.sub(r"<[^>]+>", " ", inner)
    t = re.sub(r"\$\{[^}]*\}", " ", t)
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


# ---------- F2: o cartão está no último gate aprovado; a proposta exige arquivo do gate ----------

class TestF2CartaoEmGn(unittest.TestCase):
    def test_f2_cartao_em_gn_exige_arquivo_do_gate(self):
        """F2 (FR2/FR8): G2 aprovado e G3 ausente → cartão em G2; proposta a G3 recusada com `falta`."""
        chamado = _chamado_ate_g2()
        card = _fn("cartao")(
            chamado)
        gate = card["gate"] if isinstance(card, dict) else card
        self.assertEqual(gate, "G2", "o cartão fica no último gate com veredito vigente aprovado (FR2).")

        proposta = _fn("proposta_transicao")
        # sem o arquivo G3 na pasta, a proposta é recusada (devolve dict, não levanta — plano §'Nomes fixados')
        recusa = proposta(chamado, "G2", "G3", {})
        self.assertFalse(recusa["permitido"], "FR8: sem arquivo do gate de destino, a proposta é recusada.")
        falta = recusa.get("falta") or ""
        if isinstance(falta, (list, tuple)):
            falta = " ".join(str(x) for x in falta)
        self.assertIn("G3-*.md", falta, "F2: o motivo nomeia o arquivo que falta (FR8).")
        self.assertIn("cabeçalho válido", falta, "F2: o motivo exige cabeçalho válido (FR8).")

        # com o arquivo do gate de destino válido, a proposta é permitida (nada é movido: só a proposta)
        ok = proposta(chamado, "G2", "G3",
                      {"G3": {"caminho": "specs/072-teste-f2/G3-codigo.md", "cabecalho_valido": True}})
        self.assertTrue(ok["permitido"], "FR8: com `G3-*.md` de cabeçalho válido, a proposta é permitida.")


# ---------- F3: transição sem evidência devolve 422 e não toca arquivo algum ----------

class TestF3Transicao(_Base):
    """F3 (FR8/FR9), corrigida na R1/072-T12: o teste tinha de provar as DUAS metades.

    Antes ele só olhava `422` + um corpo com "motivo|erro|falta" — e o 422 de crash (a rota
    estourava `ValueError` em `_arquivos_do_gate` e o `except ValueError` do `do_POST` o
    convertia em recusa) satisfazia a asserção. Ou seja: a F3 passava com a rota quebrada e
    não provava nada. Agora ela exige a transição **permitida** respondendo 200 e, na recusa,
    exige que ela seja **decidida**, não um `ValueError` disfarçado.
    """

    def test_f3_transicao_valida_permite_e_ausente_recusa_sem_excecao(self):
        """F3 (FR8/FR9): com o arquivo do gate de destino e cabeçalho válido → 200 `permitido: true`;
        sem o arquivo → 422 com "falta" no motivo — e o 422 nunca vem de exceção."""
        hash_, quando = _repo_de_verdade(self.raiz)
        _escreve(os.path.join(self.raiz, "specs/072-teste-f3/00-chamado.md"), ABERTURA)
        _escreve(os.path.join(self.raiz, "specs/072-teste-f3/G1-spec-W13.md"),
                 _gate_objeto("G1", "APPROVE", "W13", hash_, quando))
        _escreve(os.path.join(self.raiz, "specs/072-teste-f3/G2-vermelho-aaaaaaa.md"),
                 _gate_objeto("G2", "FALHA_ESPERADA", "W07", hash_, quando))

        srv, url = self._sobe()
        # W04 (V0b iii): a foto vem DEPOIS de subir o servidor — `_sobe()` cria `<raiz>/painel.db`,
        # então fotografar antes tornaria o assert impossível por um artefato da fixture, não da
        # transição. O intento (FR9: nenhum arquivo muda na recusa) fica preservado.
        antes = self._foto_da_arvore()

        erro = io.StringIO()
        with contextlib.redirect_stderr(erro):
            # METADE 1 — de G1 para G2 com o arquivo G2 presente e de cabeçalho válido: PERMITIDO.
            code_ok, resp_ok = self._post_json(
                url, "/api/regencia/transicao",
                {"chamado": "072-teste-f3", "de": "G1", "para": "G2"})
            # METADE 2 — de G2 para G5 sem arquivo de G5 na pasta: RECUSA decidida.
            code_no, resp_no = self._post_json(
                url, "/api/regencia/transicao",
                {"chamado": "072-teste-f3", "de": "G2", "para": "G5"})

        self.assertEqual(code_ok, 200, "FR8: transição válida (G1→G2, arquivo de G2 presente e "
                                       f"válido) responde 200 (recebido {code_ok}: {resp_ok}).")
        self.assertIs(json.loads(resp_ok).get("permitido"), True,
                      f"FR8: a transição permitida devolve `permitido: true` ({resp_ok}).")

        self.assertEqual(code_no, 422, "FR9: transição sem evidência responde 422 com o motivo "
                                       f"(recebido {code_no}: {resp_no}).")
        corpo_no = json.loads(resp_no)
        self.assertIn("falta", json.dumps(corpo_no, ensure_ascii=False).lower(),
                      f"FR9: o motivo do 422 acusa a falta do arquivo ({resp_no}).")

        # O ponto da R1: o 422 tem de ser recusa DECIDIDA. Se a rota estourar, o `except ValueError`
        # do `do_POST` responde 422 igual — então o que separa os dois casos não é o código HTTP, é
        # o servidor não ter imprimido um traceback.
        self.assertNotIn("Traceback", erro.getvalue(),
                         "FR9/R1: o 422 é recusa decidida, não exceção não tratada — nenhum "
                         f"Traceback pode aparecer no stderr do servidor:\n{erro.getvalue()}")
        self.assertEqual(self._foto_da_arvore(), antes, "FR9: nenhum arquivo muda na transição.")


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


# ---------- F5 (ruling) + FR4 (independência) ----------

class TestF5Ruling(unittest.TestCase):
    def test_f5_ruling_sem_autor_humano_ou_destino_e_recusado(self):
        """F5 (FR14): sem destino ou sem autor humano (pessoa) → recusado; delegação registra quem lançou."""
        valida = _fn("valida_ruling")
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


class TestF4Independencia(unittest.TestCase):
    def test_f4_independencia_builder_e_critico(self):
        """FR4 (Princípio II): mesmo autor da peça e do veredito → vermelho; sem autor_da_peca → "—" com motivo."""
        ind = _fn("independencia")
        self.assertTrue(_vermelho(ind("W13", "W13")),
                        "FR4: `autor_da_peca == por` marca vermelho (quem executa não verifica a si).")
        self.assertFalse(_vermelho(ind("W07", "W13")),
                         "FR4: autores diferentes → 'builder != crítico', sem vermelho.")
        sem = ind("", "W13")
        self.assertFalse(_vermelho(sem),
                         "FR4/FR5: sem `autor_da_peca` não há verde presumido (FR5, '—' com motivo).")
        if not isinstance(sem, bool):  # o marcador pode vir como texto/dict: precisa nomear o motivo
            texto = sem if isinstance(sem, str) else json.dumps(sem, ensure_ascii=False)
            self.assertTrue("—" in texto or "motivo" in texto.lower(),
                            "FR4/FR5: sem `autor_da_peca`, o marcador é '—' com motivo.")


class TestF5ParserAutorDaPeca(unittest.TestCase):
    def test_f5_parser_expoe_autor_da_peca(self):
        """F5 (FR5): `chamados.confere` expõe `autor_da_peca` no item, ao lado de `por`."""
        arqs = {"00-chamado.md": ABERTURA,
                "G2-vermelho-aaaaaaa.md": _gate("G2", "FALHA_ESPERADA", por="W07",
                                                extra="autor_da_peca: W13\n")}
        r = chamados.confere(arqs, data_hash, True)
        itens = [i for g in r["gates"] if g["gate"] == "G2" for i in g["itens"]]
        self.assertTrue(itens, "a fixture precisa produzir ao menos um item no G2.")
        self.assertEqual(itens[0].get("autor_da_peca"), "W13",
                         "FR5: o item do gate expõe `autor_da_peca`, ao lado de `por`.")
        # sem o campo, o item não presume autor (o marcador de FR4 exibe '—' com motivo)
        arqs2 = {"00-chamado.md": ABERTURA,
                 "G2-vermelho-aaaaaaa.md": _gate("G2", "FALHA_ESPERADA", por="W07")}
        r2 = chamados.confere(arqs2, data_hash, True)
        it2 = [i for g in r2["gates"] if g["gate"] == "G2" for i in g["itens"]][0]
        self.assertFalse(it2.get("autor_da_peca"),
                         "FR5: sem o campo, nada de autor presumido (nunca verde presumido).")


# ---------- F6: normalização tabela-dirigida (devolve dict) ----------

class TestF6Normalizacao(unittest.TestCase):
    def test_f6_normalizacao_tabela_dirigida(self):
        """F6 (FR10): tabela fixa; `{canonico, original, motivo?}`; outro valor cai em `inválido`."""
        normaliza = _fn("normaliza")
        tabela = [("APPROVE", "aprovado"), ("OK", "aprovado"), ("PASSA", "aprovado"), ("PASSOU", "aprovado"),
                  ("RETURN", "devolvido"), ("REPROVE", "devolvido"), ("FALHA", "devolvido"),
                  ("FALHA_ESPERADA", "vermelho provado"),
                  ("PENDENTE", "em curso"), ("REPRODUZIDO", "em curso"),
                  ("NÃO PASSA", "inválido"), ("DESCONHECIDO", "inválido"), ("", "inválido")]
        for valor, canon in tabela:
            r = normaliza(valor)
            self.assertEqual(r["canonico"], canon, f"normaliza({valor!r})['canonico']")
            self.assertEqual(r["original"], valor,
                             f"normaliza({valor!r})['original'] mantém a palavra do arquivo (anti-regra 6).")
        # cabeçalho reprovado pelo conferidor (068): o sinal entra pelos `erros` → inválido, com o original
        r = normaliza("APPROVE", erros=["falta 'por' no cabeçalho"])
        self.assertEqual(r["canonico"], "inválido",
                         "FR10: cabeçalho reprovado normaliza como 'inválido'.")
        self.assertEqual(r["original"], "APPROVE", "FR10: o original fica visível.")


# ---------- F7: idade vem do relógio/timestamp, com carimbo e selo ----------

class TestF7Idade(unittest.TestCase):
    def test_f7_idade_do_relogio_e_carimbo(self):
        """F7 (FR23): idade `{texto, carimbo, selo}`; digitada à mão → selo 'declarada'."""
        idade = _fn("idade_do_carimbo")
        # 2026-10-24 04:48 -0300 → 7 h 12 min antes de AGORA (12:00 -0300)
        r = idade("2026-10-24T04:48:00-03:00", AGORA)
        self.assertIn("7 h 12 min", r["texto"], "FR23: a idade aparece como 'há 7 h 12 min'.")
        self.assertTrue(r["carimbo"], "FR23: a idade aparece também como carimbo absoluto.")
        self.assertNotEqual(r["selo"], "declarada", "idade do relógio/registro não é 'declarada'.")
        declarada = idade("2026-10-20T07:04:00-03:00", AGORA, declarado=True)
        self.assertEqual(declarada["selo"], "declarada",
                         "FR23: data escrita à mão em arquivo aparece com o selo 'declarada'.")


# ---------- F8: "—" sempre com motivo ----------

class TestF8Traco(unittest.TestCase):
    def test_f8_traco_com_motivo(self):
        """F8 (FR22): fonte ausente → '—' com o motivo e o caminho; nunca '0' nem 'n/a'."""
        sem_fonte = _fn("sem_fonte")
        t = sem_fonte("limite de idade não tem fonte", "padrao-chamado.md")
        self.assertIn("—", t)
        self.assertIn("motivo:", t)
        self.assertIn("padrao-chamado.md", t)


# ---------- F10: ingestão defasada é anunciada ----------

class TestF10IngestaoDefasada(unittest.TestCase):
    def test_f10_ingestao_defasada_anunciada(self):
        """F10 (FR25): meta.ingerido_em com mais de 1 h → cabeçalho anuncia 'defasado'."""
        aviso = _fn("aviso_ingestao")

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
        fila_registro = _adapter()
        caminho = os.path.join(self.raiz, "fila.jsonl")
        with open(caminho, "w", encoding="utf-8") as f:
            f.write('{"id": "D-001", "tipo": "pedido"}\n')
        with open(caminho, "rb") as f:
            antes = f.read()
        fila_registro.acrescenta(caminho, {"id": "D-002", "tipo": "ruling", "pedido": "D-001"})
        with open(caminho, "rb") as f:
            depois = f.read()
        self.assertTrue(depois.startswith(antes), "FR16: o prefixo de bytes anterior não muda.")
        self.assertGreater(len(depois), len(antes), "FR16: o arquivo cresce.")
        linhas = [l for l in depois.decode("utf-8").splitlines() if l.strip()]
        self.assertEqual(len(linhas), 2, "FR16: exatamente uma linha foi acrescentada.")
        self.assertEqual(json.loads(linhas[0])["id"], "D-001")
        self.assertEqual(json.loads(linhas[1])["id"], "D-002")


# ---------- FR17 (dívida 5 do 070): gatilho recusa UPDATE/DELETE (WHEN em `passos`) ----------

class TestDivida5Gatilho(unittest.TestCase):
    def test_divida5_gatilho_recusa_update_e_delete(self):
        """FR17: append-only por TRIGGER; em `passos` o WHEN libera só o fechamento (saida_em/resumo/resultado)."""
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
                con.execute("INSERT INTO fila (sessao_origem, payload, criada_em) "
                            "VALUES ('W09', '{}', '2026-10-22T16:02:00+00:00')")
                con.commit()
                recusados = [("rodadas", "UPDATE rodadas SET desejo='x'"),
                             ("rodadas", "DELETE FROM rodadas"),
                             ("transicoes", "UPDATE transicoes SET evidencia_exigida=0"),
                             ("transicoes", "DELETE FROM transicoes"),
                             ("fila", "UPDATE fila SET payload='x'"),
                             ("fila", "DELETE FROM fila"),
                             ("passos", "DELETE FROM passos"),
                             # coluna fora das três liberadas: o WHEN não cobre → recusado
                             ("passos", "UPDATE passos SET passo='T9'")]
                for tabela, sql in recusados:
                    with self.assertRaises(sqlite3.DatabaseError,
                                           msg=f"FR17: {tabela} aceitou '{sql}' — falta o TRIGGER."):
                        con.execute(sql)
                        con.commit()
                # o fechamento do passo (WHEN: `saida_em IS NULL` e só nas colunas liberadas) PASSA
                con.execute("UPDATE passos SET saida_em='2026-10-22T16:05:00+00:00', "
                            "resumo='ok', resultado='ok' WHERE passo='T1'")
                con.commit()
                # passo já fechado → recusado
                with self.assertRaises(sqlite3.DatabaseError,
                                       msg="FR17: passo já fechado não aceita novo UPDATE."):
                    con.execute("UPDATE passos SET resumo='de novo' WHERE passo='T1'")
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
        itens = _fn("portoes_do_regente")(chamado, commit_de)
        por_gate = {i["gate"]: i for i in itens}
        for g in ("G7", "G8"):
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


# ============================================================================
# --- FATIA W03 (072-T03b: reconciliação do gate do plano) — testes ampliados ---
# Apensados por T03b. Vermelhos pela razão certa: o pacote puro, o adaptador e as rotas
# ainda não existem. Nomes conforme `plan.md` §"Nomes fixados" e `contracts/`.
# ============================================================================

class TestF20Negativos(unittest.TestCase):
    def test_f20_autor_fora_das_pessoas_recusado(self):
        """FR20/ambiguidade 1a: autor fora de `cfg.regencia.pessoas` → recusado, mesmo com `registrado_por`."""
        valida = _fn("valida_ruling")
        pessoas, pedidos = ["Darú", "Gilsiley"], ["D-1"]
        motivo = valida({"id": "R-9", "pedido": "D-1", "escolha": "a", "autor": "Office",
                         "destinatario": "W03", "registrado_por": "Office"}, pessoas, pedidos)
        self.assertTrue(motivo, "FR20: autor fora de `regencia.pessoas` é recusado (a Office registra, "
                                "não assume a autoria).")
        self.assertIn("pessoa", motivo.lower())
        # quem É pessoa do projeto e tem destino passa
        self.assertFalse(valida({"id": "R-10", "pedido": "D-1", "escolha": "a", "autor": "Darú",
                                 "destinatario": "W03"}, pessoas, pedidos))

    def test_f20_ruling_para_pedido_inexistente_recusado(self):
        """FR20: ruling para pedido inexistente → recusado."""
        valida = _fn("valida_ruling")
        motivo = valida({"id": "R-11", "pedido": "D-404", "escolha": "a", "autor": "Darú",
                         "destinatario": "W03"}, ["Darú"], ["D-1"])
        self.assertTrue(motivo, "FR20: ruling para pedido desconhecido é recusado.")
        self.assertIn("pedido", motivo.lower())


class TestF14AbreEmAppend(unittest.TestCase):
    def test_f14_registro_abre_sempre_em_append(self):
        """FR16 (prova estática): nenhum `open` de `fila_registro.py` reescreve; a escrita é append."""
        caminho = os.path.join(PAINEL, "fila_registro.py")
        self.assertTrue(os.path.exists(caminho),
                        "painel/fila_registro.py ainda não existe (adaptador do registro, W05).")
        with open(caminho, encoding="utf-8") as f:
            arvore = ast.parse(f.read(), filename=caminho)

        def _modo(no):
            modo = "r"  # default do `open`
            if len(no.args) >= 2 and isinstance(no.args[1], ast.Constant):
                modo = no.args[1].value
            for kw in no.keywords:
                if kw.arg == "mode" and isinstance(kw.value, ast.Constant):
                    modo = kw.value.value
            return modo

        aberturas = [(no.lineno, _modo(no)) for no in ast.walk(arvore)
                     if isinstance(no, ast.Call) and getattr(no.func, "id", None) == "open"]
        self.assertTrue(aberturas, "FR16: o adaptador precisa abrir o arquivo para acrescentar.")
        perigosos = [(ln, m) for ln, m in aberturas
                     if any(ch in m for ch in ("w", "x")) or m == "r+"]
        self.assertEqual(perigosos, [],
                         "FR16: o registro never é aberto em modo de reescrita/truncagem — só append.")
        self.assertTrue([m for _, m in aberturas if "a" in m],
                        "FR16: o acréscimo abre o registro em modo append ('a').")


class TestF14Concorrente(_Base):
    def test_f14_registro_concorrente_sem_perda(self):
        """FR16: dois POST paralelos na fila → duas linhas no registro, nenhuma perdida."""
        caminho = os.path.join(self.raiz, "fila.jsonl")
        srv, url = self._sobe()

        def um(i):
            return self._post_json(url, "/api/regencia/fila", {
                "tipo": "pedido", "id": f"D-00{i}", "pedido_por": "W03/sess",
                "pergunta": f"pergunta {i}", "opcoes": [{"id": "a", "descricao": "sim"}],
                "recomendacao": "a", "prazo": "2026-10-30T12:00:00-03:00",
                "destrava": ["072"], "destino": "Regente", "status": "aguardando"})

        respostas = []
        fios = [threading.Thread(target=lambda i=i: respostas.append(um(i))) for i in (1, 2)]
        for f in fios:
            f.start()
        for f in fios:
            f.join()
        self.assertEqual(sorted(c for c, _ in respostas), [200, 200],
                         f"FR16: os dois POST paralelos precisam ser aceitos (recebido {respostas}).")
        self.assertTrue(os.path.exists(caminho), "FR16: o registro da fila não foi criado no endereço da config.")
        with open(caminho, encoding="utf-8") as f:
            linhas = [l for l in f.read().splitlines() if l.strip()]
        self.assertEqual(len(linhas), 2, "FR16: dois POST paralelos → duas linhas, nenhuma perdida.")
        ids = {json.loads(l).get("id") for l in linhas}
        self.assertEqual(ids, {"D-001", "D-002"}, "FR16: as duas linhas são as duas escritas.")


class TestF15OrdemDaFila(unittest.TestCase):
    def test_f15_ordena_fila_por_prazo_e_bloqueio(self):
        """FR15: ordena por prazo (o que estoura antes primeiro); empate pelo nº de destravados."""
        ordena = _fn("ordena_fila")
        itens = [{"id": "D-3", "prazo": "2026-10-30T12:00:00-03:00", "destrava": ["a"]},
                 {"id": "D-1", "prazo": "2026-10-25T12:00:00-03:00", "destrava": ["a"]},
                 {"id": "D-2", "prazo": "2026-10-25T12:00:00-03:00", "destrava": ["a", "b", "c"]}]
        ordem = [i["id"] for i in ordena(itens, AGORA)]
        self.assertEqual(ordem, ["D-2", "D-1", "D-3"],
                         "FR15: prazo mais próximo primeiro; no empate, quem destrava mais vem antes.")


class TestF23CabecalhoDaFila(unittest.TestCase):
    def test_f23_cabecalho_fila_conta_e_mais_velho(self):
        """FR23: cabeçalho da fila conta os itens e traz a idade do mais velho."""
        cabecalho = _fn("cabecalho_fila")
        fila = [{"id": "D-1", "criado_em": "2026-10-24T04:48:00-03:00"},
                {"id": "D-2", "criado_em": "2026-10-24T11:00:00-03:00"}]
        cab = cabecalho(fila, AGORA)
        self.assertEqual(cab["n"], 2, "FR23: o cabeçalho conta os itens da fila.")
        self.assertIn("idade_mais_velha", cab, "FR23: o cabeçalho traz a idade do item mais velho.")
        v = cab["idade_mais_velha"]
        texto = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
        self.assertTrue("7 h 12 min" in texto or "04:48" in texto,
                        f"FR23: a idade do mais velho sai do relógio/registro (recebido {v!r}).")


class TestF1DezColunas(_Base):
    def test_f1_dez_colunas_g0_g9_na_ordem_de_gates(self):
        """FR1: o kanban tem exatamente dez colunas G0–G9, na ordem de `GATES`; abertura e GD fora."""
        esperado = [g for g, _, _ in chamados.GATES if g not in ("abertura", "GD")]
        self.assertEqual(esperado, ["G0", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9"],
                         "sanidade da fixture: `GATES` traz dez gates G0–G9 além de abertura/GD.")
        srv, url = self._sobe()
        dados = self._get_json(url, "/api/regencia/kanban")
        colunas = [c["gate"] if isinstance(c, dict) else c for c in dados.get("colunas", [])]
        self.assertEqual(colunas, esperado,
                         "FR1: dez colunas G0–G9 na ordem de GATES; abertura e GD não viram coluna.")


class TestF7FiltroPorFrente(_Base):
    def test_f7_meta_publica_as_frentes(self):
        """FR7: `/api/meta` publica as frentes do projeto (`cfg.frentes`); sem escolha, todas."""
        srv, url = self._sobe()
        dados = self._get_json(url, "/api/meta")
        self.assertIn("frentes", dados, "FR7: `/api/meta` publica `frentes` (lido de projetos/<nome>.json).")
        self.assertEqual(set(dados["frentes"]), set(self._cfg()["frentes"]),
                         "FR7: as frentes exibidas são as do projeto, não inventadas.")


class TestF11AnatomiaDoPedido(unittest.TestCase):
    def test_f11_valida_pedido_exige_os_campos(self):
        """FR11: o pedido exige id, quem pediu, pergunta, opções (com descrição), recomendação, prazo,
        o que destrava, destino e status."""
        valida = _fn("valida_pedido")
        completo = {"tipo": "pedido", "id": "D-1", "pedido_por": "W03/sess",
                    "pergunta": "Aceitar a rodada 1?", "opcoes": [{"id": "a", "descricao": "sim"}],
                    "recomendacao": "a", "prazo": "2026-10-30T12:00:00-03:00",
                    "destrava": ["072"], "destino": "Regente", "status": "aguardando"}
        self.assertFalse(valida(completo), "FR11: pedido completo é aceito.")
        for campo in ("id", "pedido_por", "pergunta", "opcoes", "recomendacao", "prazo",
                      "destrava", "destino", "status"):
            falta = {k: v for k, v in completo.items() if k != campo}
            self.assertTrue(valida(falta), f"FR11: sem '{campo}' o pedido é recusado.")
        self.assertTrue(valida({**completo, "opcoes": []}), "FR11: pedido sem nenhuma opção é recusado.")
        self.assertTrue(valida({**completo, "opcoes": [{"id": "a"}]}),
                        "FR11: opção sem descrição é recusada.")


# ---------- 072-T16: correções da rodada (id do chamado; avisos de leitura velha) ----------

class TestT16ChamadoNaoNavega(_Base):
    """072-T16(1): o `chamado` do POST /api/regencia/transicao é um **id**, não um caminho.

    O adaptador monta a pasta com `os.path.join(raiz, …, chamado)`: com `chamado=".."` a pasta
    resolvia para a **raiz** do repositório e o `os.listdir` seguinte listava o que estivesse lá —
    inclusive um arquivo de gate válido fora de `specs/`. O id passa a aceitar só `^[\\w.-]+$` e
    nunca `.` nem `..`, e a recusa é um 422 que acusa o chamado.
    """

    def test_t16_chamado_com_navegacao_recusa_422_e_nao_le_fora_de_specs(self):
        hash_, quando = _repo_de_verdade(self.raiz)
        _escreve(os.path.join(self.raiz, "specs/072-teste-t16/00-chamado.md"), ABERTURA)
        _escreve(os.path.join(self.raiz, "specs/072-teste-t16/G2-vermelho-aaaaaaa.md"),
                 _gate_objeto("G2", "FALHA_ESPERADA", "W07", hash_, quando))
        # A isca: um gate de G2 com cabeçalho VÁLIDO na raiz — um nível acima de `specs/`, que é
        # exatamente onde `chamado=".."` chegava. Se a rota respondesse 200 com este caminho, o
        # painel estaria servindo arquivo de fora de `specs/`.
        _escreve(os.path.join(self.raiz, "G2-armadilha-aaaaaaa.md"),
                 _gate_objeto("G2", "FALHA_ESPERADA", "W07", hash_, quando))
        srv, url = self._sobe()

        for cid in ("..", "../..", ".", "specs/..", "a/b", "a\\b", ""):
            code, resposta = self._post_json(url, "/api/regencia/transicao",
                                             {"chamado": cid, "de": "G1", "para": "G2"})
            self.assertEqual(code, 422, f"072-T16: `chamado={cid!r}` tem de ser recusado "
                                        f"(recebido {code}: {resposta}).")
            self.assertIn("chamado", resposta.lower(),
                          f"072-T16: a recusa de {cid!r} acusa o CHAMADO, não a falta de arquivo — "
                          f"o motivo aponta para o lugar certo ({resposta}).")
            self.assertNotIn("armadilha", resposta,
                             f"072-T16: nada de fora de `specs/` pode aparecer na resposta ({resposta}).")

        # e o id legítimo segue passando: a guarda não é um bloqueio geral
        code, resposta = self._post_json(url, "/api/regencia/transicao",
                                         {"chamado": "072-teste-t16", "de": "G1", "para": "G2"})
        self.assertEqual(code, 200, f"072-T16: o id legítimo continua permitido "
                                    f"(recebido {code}: {resposta}).")
        self.assertIs(json.loads(resposta).get("permitido"), True, resposta)


RE_IDADE = re.compile(r"(\d+)\s*h\s*(\d+)\s*m", re.I)


def _h_m_do_texto(texto):
    """`(horas, minutos)` lidos de "1h59m" ou de "1 h 59 min" — a mesma leitura para as duas formas."""
    m = RE_IDADE.search(texto or "")
    return (int(m.group(1)), int(m.group(2))) if m else None


class TestT16LeituraVelhaConcorda(_Base):
    """072-T16(2): o aviso de cima (`/api/meta`) e o de dentro da página (`/api/regencia/kanban`)
    descrevem a MESMA ingestão — logo, o mesmo número.

    O de cima fazia a conta em JavaScript (`Math.round(ingerido_age_min % 60)` sobre um valor já
    arredondado a 0,1 min): em 119,9 min de idade imprimia "1h60m" enquanto o de baixo imprimia
    "1 h 59 min".
    """

    def test_t16_os_dois_avisos_trazem_o_mesmo_numero(self):
        srv, url = self._sobe()
        # 7194 s = 1 h 59 min e 54 s → "1 h 59 min". Era o caso que separava os dois avisos.
        self._grava_meta("ingerido_em",
                         (dt.datetime.now().astimezone() - dt.timedelta(seconds=7194)).isoformat())

        topo = self._get_json(url, "/api/meta")
        dentro = self._get_json(url, "/api/regencia/kanban")["meta"]

        self.assertEqual(_h_m_do_texto(topo.get("leitura_velha")), (1, 59),
                         f"072-T16: idade de 119,9 min = 1 h 59 min no aviso de cima "
                         f"(recebido {topo.get('leitura_velha')!r}).")
        self.assertEqual(_h_m_do_texto(dentro.get("aviso")), (1, 59),
                         f"072-T16: e o aviso de dentro da página diz o mesmo "
                         f"(recebido {dentro.get('aviso')!r}).")
        self.assertEqual(_h_m_do_texto(topo.get("leitura_velha")), _h_m_do_texto(dentro.get("aviso")),
                         "072-T16: dois avisos da mesma ingestão, um número só — nunca 1h60m "
                         f"contra 1 h 59 min ({topo.get('leitura_velha')!r} × {dentro.get('aviso')!r}).")

        # ingestão fresca: os dois se calam (nenhum dos banners aparece)
        self._grava_meta("ingerido_em",
                         (dt.datetime.now().astimezone() - dt.timedelta(minutes=30)).isoformat())
        self.assertFalse(self._get_json(url, "/api/meta").get("leitura_velha"),
                         "072-T16: ingestão fresca não gera aviso de leitura velha.")
        self.assertFalse(self._get_json(url, "/api/regencia/kanban")["meta"].get("aviso"),
                         "072-T16: e o aviso de dentro da página também se cala.")


if __name__ == "__main__":
    unittest.main()
