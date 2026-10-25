#!/usr/bin/env python3
"""Fitness function of cycle 073, round 3 — checks the wireframe prototypes.

Mandate (regent, 2026-10-25): a script that walks the prototype HTML files and
FAILS when it finds:
  1. an interactive element without a `data-fonte` attribute (where the idea
     came from: platform + URL of the ficha, or a Maestro principle/ADR/ux-design);
  2. a label outside the glossary (allowlist extracted from
     docs/governance/glossary.md plus the 12 terms ratified in round 2);
  3. a number without the "exemplo" mark (no invented values) — checked in
     every text node, not only labels;
  4. (ratification condition) a collision-prone term used unqualified: "fila"
     without its qualifier (decisões/outbox) and "portão" without its owner
     (chamado/regente) — the five name collisions the context map exposed.

Usage: python verifica-prototipo.py   (from anywhere; paths are repo-relative)
Exit 0 = every screen passes; exit 1 = findings, printed one per line.
"""

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROTO = ROOT / "specs" / "073-area-administrativa" / "prototipo"
GLOSSARY = ROOT / "docs" / "governance" / "glossary.md"

INTERACTIVE = {"button", "a", "input", "select", "textarea"}
LABEL_TAGS = {"button", "th", "label", "legend", "h1", "h2", "h3", "h4", "h5", "h6", "dt"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}
RAW_TEXT = {"style", "script"}

# The 12 terms ratified by the regent (round 2) — also extracted from the
# glossary once Worker01 lands them; kept here so the check is exact.
RATIFIED = [
    "sessão de agente", "agent session",
    "estado do agente vivo", "live agent state",
    "tarefa aberta", "open task",
    "consumo por agente", "per-agent usage",
    "limite de orçamento", "budget limit",
    "catálogo de skills/ferramentas/modelos", "skill/tool/model catalog",
    "mensagem entre agentes", "agent-to-agent message",
    "protocolo de intercomunicação", "intercommunication protocol",
    "caixa de entrada", "inbox",
    "livro de mensagens", "message ledger",
    "roteamento por nome/ref", "name/ref routing",
    "colisão de nomes", "name collision",
]

# Generic UI words a label may consist of without citing any glossary term.
STOPWORDS = {
    "novo", "nova", "abrir", "fechar", "buscar", "salvar", "cancelar", "voltar",
    "exemplo", "exemplos", "sim", "não", "nao", "ok", "detalhes", "mais",
    "configurações", "configuracoes", "nome", "descrição", "descricao", "data",
    "estado", "ação", "acao", "filtro", "ordenar", "por", "de", "da", "do", "e",
    "em", "com", "sem", "para", "o", "a", "os", "as", "um", "uma", "que", "no",
    "na", "aos", "às", "the", "of", "and", "new", "open", "close", "save",
    "cancel", "back", "details", "more", "name", "date", "state", "action",
    "filter", "sort", "example", "yes", "no", "none",
}

NUMBER = re.compile(r"\d")
WORD = re.compile(r"[\wà-ú/=-]+")


def glossary_terms():
    """Terms from glossary.md (first column, bold) + the 12 ratified ones.

    Returns compiled word-boundary regexes: a bare substring match would let
    "RACI" match inside "opeRACIonal" (found while smoke-testing).
    """
    terms = set(t.lower() for t in RATIFIED)
    if GLOSSARY.exists():
        for line in GLOSSARY.read_text(encoding="utf-8").splitlines():
            if not line.startswith("| **"):
                continue
            cell = line.split("|")[1]
            cell = re.sub(r"\([^)]*\)", "", cell)  # drop the parenthetical
            for term in re.findall(r"\*\*(.+?)\*\*", cell):
                terms.add(term.strip().lower())
    return [re.compile(r"\b" + re.escape(t) + r"\b") for t in sorted(terms)]


class ScreenParser(HTMLParser):
    """Collects the findings of one screen.

    Keeps a stack of open elements so a number is accepted when ANY ancestor
    carries the example mark (data-exemplo, or "exemplo" inside data-fonte).
    """

    def __init__(self, path, terms):
        super().__init__()
        self.path = path
        self.terms = terms
        self.findings = []
        self.stack = []  # [tag, attrs-dict, label-text-so-far or None]

    def error(self, message):
        pass

    # -- tree bookkeeping --------------------------------------------------

    def inside_example(self):
        return any("data-exemplo" in a or "exemplo" in a.get("data-fonte", "").lower()
                   for _, a, _ in self.stack)

    def inside_raw(self):
        return any(t in RAW_TEXT for t, _, _ in self.stack)

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag in INTERACTIVE and not a.get("data-fonte", "").strip():
            self.findings.append(
                f"{self.path.name}: interactive <{tag}> without data-fonte")
        if tag in VOID:
            return
        self.stack.append([tag, a, "" if tag in LABEL_TAGS else None])

    def handle_endtag(self, tag):
        # pop up to the matching open tag (tolerates stray closers)
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                closed = self.stack[i:]
                del self.stack[i:]
                for _, attrs, text in closed:
                    if text is not None:
                        self.check_label(text.strip(), attrs)
                return

    def handle_data(self, data):
        if not self.stack or self.inside_raw():
            return
        # 3. numbers must be marked as example — in every text node
        if NUMBER.search(data) and "exemplo" not in data.lower() \
                and not self.inside_example():
            self.findings.append(
                f'{self.path.name}: number without the "exemplo" mark: "{data.strip()}"')
        # feed the innermost open label collector
        for entry in reversed(self.stack):
            if entry[2] is not None:
                entry[2] += data
                break

    # -- the label rules ---------------------------------------------------

    def check_label(self, text, attrs):
        if not text:
            return
        low = text.lower()
        # 2. label outside the glossary: no glossary term inside and at least
        #    one word that is neither a stopword nor a number
        if not any(t.search(low) for t in self.terms):
            words = [w for w in WORD.findall(low)
                     if w not in STOPWORDS and not w.isdigit()]
            if words:
                self.findings.append(
                    f'{self.path.name}: label outside the glossary: "{text}"')
        # 4. collision-prone terms must be qualified
        if re.search(r"\bfila\b", low) and "decis" not in low and "outbox" not in low:
            self.findings.append(
                f'{self.path.name}: "fila" unqualified (decisões or outbox?): "{text}"')
        if re.search(r"\bport[ãa]o\b", low) and "chamado" not in low \
                and "regente" not in low:
            self.findings.append(
                f'{self.path.name}: "portão" unqualified (chamado or regente?): "{text}"')


def main():
    terms = glossary_terms()
    # "_" prefix = scratch/sandbox file, not a screen — skipped on purpose
    screens = sorted(p for p in PROTO.glob("*.html") if not p.name.startswith("_"))
    if not screens:
        print(f"no screens found under {PROTO} — nothing to check")
        return 1
    findings = []
    for path in screens:
        parser = ScreenParser(path, terms)
        parser.feed(path.read_text(encoding="utf-8"))
        findings.extend(parser.findings)
    for f in findings:
        print("FINDING:", f)
    print(f"-- verifica-prototipo: {len(screens)} screen(s), "
          f"{len(findings)} finding(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
