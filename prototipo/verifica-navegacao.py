#!/usr/bin/env python3
"""Fitness function of cycle 074 — the navigable prototype of the regency panel.

Nine checks, run over `prototipo/` (the shell `index.html` plus the fragments under
`telas/`); each one prints a finding and fails the run:

  (a) every `href="#/..."` and every `data-vai-para` resolves to a fragment on disk;
  (b) every fragment is reachable in at most 3 clicks from `regencia/inicial` as the
      root of the graph, counting the six shell items as edges (S2 of the spec gate);
  (c) every write button carries the four attributes of decision 3 — data-acao,
      data-autoriza, data-simulado="sim" and data-efeito. A write button is the S1
      definition: a <button>, <form> or [role=button] WITHOUT href="#/..." and
      without data-vai-para (a link that navigates is not a write button);
  (d) every fragment declares data-contexto in exactly one of the five contexts of the
      context map, and it matches the folder the fragment lives in;
  (e) no external reference: no <link>/<script> pointing at http(s):// or a protocol
      relative // URL (FR6 — zero external dependency);
  (f) MUTATION CORPUS: the good fixture must pass with zero findings and the bad one
      must fail. A check that cannot fail proves nothing — the corpus under
      `verificacao/corpus/` is what proves this verifier discriminates;
  (g) the fragments pass the rules of the 073 verifier — its five rules of round 3, six
      after correction 2 — with zero findings. The 073 module is IMPORTED here with
      importlib, because its file name carries a hyphen; the module is never edited;
  (h) no button with data-acao="derrubar" without a data-alvo, and never with the
      Gerente as the target (B2 of the spec gate);
  (i) every irreversible button (data-irreversivel="sim") points at a confirmation
      (data-confirma="<id>") that exists and declares both data-perde and data-reverte.

The skeleton was born BEFORE the screens (T03-T06) on purpose: it is red until the
fragments land, and its first green belongs to the integration (T14). Messages and
docstring are in English (ADR 0014 — the installable surface).

Usage: python verifica-navegacao.py [--raiz <dir>]
Exit 0 = green; exit 1 = findings, one per line.
"""

import argparse
import importlib.util
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
CORPUS = HERE / "verificacao" / "corpus"
# the 073 verifier does NOT move with this prototype: it stays under specs/, one level up
# from the repo root (`HERE.parent` is the root while this script lives in `prototipo/`).
VERIFICADOR_073 = (HERE.parent / "specs" / "073-area-administrativa" / "prototipo"
                   / "verifica-prototipo.py")

# the five contexts of the bounded-context map (B1 / check (d)) — exactly these
CONTEXTOS = ["chamados-e-gates", "regencia", "workflow-de-sessoes",
             "administracao", "mensageria"]

ROTA_INICIAL = "regencia/inicial"
EXTERNO = re.compile(r"^(?:https?:)?//", re.IGNORECASE)
ROTA = re.compile(r"^#/(.+)$")

INTERATIVO = {"button", "form", "a", "input", "select", "textarea"}
ESCRITA_TAGS = {"button", "form"}


class Leitor(HTMLParser):
    """Collects, from one HTML file: links, write buttons, contexts, external refs,
    irreversible buttons, `derrubar` buttons and the confirmations they point at."""

    def __init__(self, nome):
        super().__init__()
        self.nome = nome
        self.rotas = []            # (kind, value) — kind: "href" | "vai-para"
        self.botoes = []           # (tag, attrs) for every write button
        self.contextos = []        # data-contexto values found
        self.externos = []         # (tag, value) for external <link>/<script>
        self.irreversiveis = []    # (tag, confirma-id, alvo)
        self.derrubar = []         # (data-alvo or None)
        self.ids = set()           # every id declared in the file
        self.marcas = {}           # id -> set of {"data-perde", "data-reverte"}
        self.pilha = []            # open elements: (tag, attrs, id-or-None)

    # -- helpers ------------------------------------------------------------

    def id_vigente(self, a):
        """The element's own id, or the nearest ancestor that has one — a confirmation
        carries data-perde/data-reverte on its children (ux-design §2.5)."""
        if a.get("id"):
            return a["id"]
        for _, _, ident in reversed(self.pilha):
            if ident:
                return ident
        return None

    def marcar(self, a, marca):
        ident = self.id_vigente(a)
        if ident:
            self.marcas.setdefault(ident, set()).add(marca)

    # -- HTMLParser ---------------------------------------------------------

    def error(self, message):
        pass

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if a.get("id"):
            self.ids.add(a["id"])
        if a.get("data-perde"):
            self.marcar(a, "data-perde")
        if a.get("data-reverte"):
            self.marcar(a, "data-reverte")

        href = a.get("href", "").strip()
        if href.startswith("#/"):
            self.rotas.append(("href", href[2:]))
        vai = a.get("data-vai-para", "").strip()
        if vai:
            self.rotas.append(("vai-para", vai))

        if tag in ("link", "script"):
            valor = a.get("href") or a.get("src") or ""
            if EXTERNO.match(valor.strip()):
                self.externos.append((tag, valor.strip()))

        if a.get("data-contexto"):
            self.contextos.append(a["data-contexto"].strip())

        # S1: a write button is a button/form/[role=button] that does not navigate
        eh_botao = tag in ESCRITA_TAGS or a.get("role", "").strip().lower() == "button"
        if eh_botao and not href and not vai:
            self.botoes.append((tag, a))
            if a.get("data-irreversivel", "").strip().lower() == "sim":
                self.irreversiveis.append(
                    (tag, a.get("data-confirma", "").strip(), a.get("data-acao", "")))
            if a.get("data-acao", "").strip().lower() == "derrubar":
                self.derrubar.append(a.get("data-alvo"))

        if tag in ("area", "base", "br", "col", "embed", "hr", "img", "input",
                   "link", "meta", "param", "source", "track", "wbr"):
            return
        self.pilha.append((tag, a, a.get("id") or None))

    def handle_endtag(self, tag):
        for i in range(len(self.pilha) - 1, -1, -1):
            if self.pilha[i][0] == tag:
                del self.pilha[i:]
                return


def ler(caminho):
    leitor = Leitor(caminho.name)
    leitor.feed(caminho.read_text(encoding="utf-8"))
    return leitor


def rota_do_fragmento(caminho, raiz):
    relativo = caminho.relative_to(raiz / "telas")
    return relativo.with_suffix("").as_posix()


def telas(raiz):
    pasta = raiz / "telas"
    return sorted(p for p in pasta.rglob("*.html") if p.is_file()) if pasta.exists() else []


def ler_tudo(raiz):
    arquivos = []
    casca = raiz / "index.html"
    if casca.exists():
        arquivos.append(casca)
    return arquivos + telas(raiz)


def verificador_073():
    """The 073 rules are imported, never copied and never edited (check (g))."""
    spec = importlib.util.spec_from_file_location("verifica_prototipo_073", VERIFICADOR_073)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def checar(raiz, com_corpus=True):
    """Runs (a)-(i) over one root; returns the list of findings."""
    achados = []
    fragmentos = telas(raiz)
    arquivos = ler_tudo(raiz)

    if not fragmentos:
        achados.append(
            f"(b) no fragment found under {raiz / 'telas'} — the screens are "
            f"deliverables T03-T06, so this run is red by design (the first green "
            f"belongs to the integration)")

    rotas_no_disco = {rota_do_fragmento(p, raiz) for p in fragmentos}

    for caminho in arquivos:
        leitor = ler(caminho)
        nome = caminho.relative_to(raiz).as_posix()

        # (a) every route reference resolves to a fragment on disk
        for tipo, valor in leitor.rotas:
            if tipo == "href":
                if valor not in rotas_no_disco:
                    achados.append(
                        f"(a) {nome}: href=\"#/{valor}\" does not resolve to a fragment")
            else:  # data-vai-para="telas/<contexto>/<tela>.html"
                destino = raiz / valor if valor.startswith("telas/") else raiz / "telas" / valor
                if not destino.is_file():
                    achados.append(
                        f"(a) {nome}: data-vai-para=\"{valor}\" does not resolve to a fragment")

        # (c) the four attributes of decision 3
        for tag, a in leitor.botoes:
            faltando = []
            if not a.get("data-acao", "").strip():
                faltando.append("data-acao")
            if not a.get("data-autoriza", "").strip():
                faltando.append("data-autoriza")
            if a.get("data-simulado", "").strip().lower() != "sim":
                faltando.append('data-simulado="sim"')
            if not a.get("data-efeito", "").strip():
                faltando.append("data-efeito")
            if faltando:
                achados.append(
                    f"(c) {nome}: write <{tag}> without {', '.join(faltando)}")

        # (e) zero external dependency (FR6)
        for tag, valor in leitor.externos:
            achados.append(
                f"(e) {nome}: external <{tag}> reference \"{valor}\"")

        # (h) `derrubar` needs a target, and the target is never the Gerente
        for alvo in leitor.derrubar:
            if not alvo or not alvo.strip():
                achados.append(
                    f"(h) {nome}: data-acao=\"derrubar\" without data-alvo")
            elif alvo.strip().startswith("Gerente"):
                achados.append(
                    f"(h) {nome}: data-acao=\"derrubar\" with the Gerente as target "
                    f"(\"{alvo.strip()}\") — the Gerente is never destructible")

        # (i) irreversible buttons point at a real confirmation, with both marks
        for tag, confirma, acao in leitor.irreversiveis:
            if not confirma:
                achados.append(
                    f"(i) {nome}: irreversible <{tag}> (data-acao=\"{acao}\") without "
                    f"data-confirma")
                continue
            if confirma not in leitor.ids:
                achados.append(
                    f"(i) {nome}: irreversible <{tag}> points at confirmation "
                    f"\"{confirma}\", which does not exist in this fragment")
                continue
            marcas = leitor.marcas.get(confirma, set())
            faltando = sorted({"data-perde", "data-reverte"} - marcas)
            if faltando:
                achados.append(
                    f"(i) {nome}: confirmation \"{confirma}\" without "
                    f"{', '.join(faltando)}")

    # (d) data-contexto in the five contexts of the map, matching the folder
    for caminho in fragmentos:
        leitor = ler(caminho)
        nome = caminho.relative_to(raiz).as_posix()
        pasta = caminho.relative_to(raiz / "telas").parts[0]
        if not leitor.contextos:
            achados.append(f"(d) {nome}: fragment without data-contexto")
            continue
        for contexto in leitor.contextos:
            if contexto not in CONTEXTOS:
                achados.append(
                    f"(d) {nome}: data-contexto=\"{contexto}\" is outside the five "
                    f"contexts of the map ({', '.join(CONTEXTOS)})")
            elif contexto != pasta:
                achados.append(
                    f"(d) {nome}: data-contexto=\"{contexto}\" does not match the folder "
                    f"\"{pasta}\"")

    # (b) every fragment reachable in <= 3 clicks from the initial screen
    if fragmentos:
        arestas = {}
        for caminho in arquivos:
            leitor = ler(caminho)
            origem = rota_do_fragmento(caminho, raiz) if caminho in fragmentos else None
            for tipo, valor in leitor.rotas:
                destino = valor[6:-5] if tipo == "vai-para" and valor.startswith("telas/") else valor
                if destino.endswith(".html"):
                    destino = destino[:-5]
                arestas.setdefault(origem, set()).add(destino)
        # the six shell items are edges from the initial screen (S2)
        alcancadas = {ROTA_INICIAL: 0}
        frente = [ROTA_INICIAL]
        for _ in range(3):
            proxima = []
            for rota in frente:
                for destino in arestas.get(rota, set()) | arestas.get(None, set()):
                    if destino not in alcancadas:
                        alcancadas[destino] = alcancadas[rota] + 1
                        proxima.append(destino)
            frente = proxima
        for rota in sorted(rotas_no_disco - set(alcancadas)):
            achados.append(
                f"(b) fragment \"{rota}\" is not reachable in <= 3 clicks from "
                f"\"{ROTA_INICIAL}\" (the six shell items count as edges)")

    # (g) the 073 rules over the fragments
    modulo = verificador_073()
    termos = modulo.glossary_terms()
    for caminho in fragmentos:
        parser = modulo.ScreenParser(caminho, termos)
        parser.feed(caminho.read_text(encoding="utf-8"))
        parser.finish()
        achados.extend(f"(g) {a}" for a in parser.findings)

    # (f) the mutation corpus proves the verifier discriminates
    if com_corpus and CORPUS.exists():
        achados.extend(corpus_discrimina())

    return achados


def corpus_discrimina():
    """(f) the good fixture is clean and the bad one fails — no check, no proof."""
    achados = []
    boa = CORPUS / "boa"
    ruim = CORPUS / "ruim"
    if not boa.exists() or not ruim.exists():
        achados.append(
            f"(f) mutation corpus incomplete under {CORPUS} — expected the fixtures "
            f"\"boa\" and \"ruim\"")
        return achados
    achados_boa = checar(boa, com_corpus=False)
    achados_ruim = checar(ruim, com_corpus=False)
    if achados_boa:
        achados.append(
            f"(f) the GOOD fixture of the corpus is not clean ({len(achados_boa)} "
            f"finding(s), first: {achados_boa[0]})")
    if not achados_ruim:
        achados.append(
            f"(f) the BAD fixture of the corpus passed — the verifier does not "
            f"discriminate (a check that cannot fail proves nothing)")
    return achados


def main():
    ap = argparse.ArgumentParser(description="Cycle 074 navigation verifier.")
    ap.add_argument("--raiz", default=str(HERE),
                    help="prototype root (default: this script's folder)")
    args = ap.parse_args()
    raiz = Path(args.raiz).resolve()

    achados = checar(raiz)
    for a in achados:
        print("FINDING:", a)
    print(f"-- verifica-navegacao: {len(telas(raiz))} fragment(s), "
          f"{len(achados)} finding(s)")
    return 1 if achados else 0


if __name__ == "__main__":
    sys.exit(main())
