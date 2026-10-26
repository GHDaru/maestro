#!/usr/bin/env python3
"""Fitness function of cycle 073, round 3 — checks the wireframe prototypes.

Mandate (regent, 2026-10-25): a script that walks the prototype HTML files and
FAILS when it finds:
  1. an interactive element without a `data-fonte` attribute (where the idea
     came from: platform + URL of the ficha, or a Maestro principle/ADR/ux-design);
  2. a label outside the glossary (allowlist extracted from
     docs/governance/glossary.md plus the 12 terms ratified in round 2);
  3. a number without the "exemplo" mark (no invented values);
  4. (ratification condition) a collision-prone term used unqualified: "fila"
     without its qualifier (decisões/outbox) and "portão" without its owner
     (chamado/regente) — the five name collisions the context map exposed.
     The round-3 review proved NO real screen exercised this rule (it ran only
     from check_label, so it saw labels alone, while the naked terms lived in
     <p>, <td> and attribute values). It now runs on EVERY VISIBLE TEXT NODE
     and on EVERY ATTRIBUTE VALUE. Two exemptions, both DECLARED, never
     inferred:
       (a) a text node or attribute inside a COLLISION-NAMING TABLE — a <table>
           whose header declares data-rotulo="colisão de nomes" — names the
           colliding terms on purpose (map §7, reproduced in mensageria-03) and
           is skipped;
       (b) an example-marked value (a data-exemplo ancestor, or "exemplo" in
           the text), exactly as in rule 3.
     Declared limit: the fence of (a) is the whole table — prose inside such a
     table is exempt from rule 4, and the fresh review is what covers it.
     Rule 4 does NOT exempt citation contexts (data-fonte/data-referencia): the
     review found the naked terms precisely in citation prose, so exempting it
     would leave the rule with nothing to accuse on the real screens.

Markup contract (agreed with the screen authors — v2, after the first run over
the real screens flagged citations as if they were metrics):
  - `data-rotulo="<term>"`  marks a DOMAIN LABEL: the VALUE must be a glossary
    term (validated here); the visible text is human phrasing and is not
    re-checked. Any element carrying data-rotulo is treated as a label.
  - `data-exemplo="true"`   marks an example VALUE (rule 3 satisfied).
  - `data-rotulo="colisão de nomes"` on a HEADER CELL (`th`/`dt`) marks the
    enclosing table as a COLLISION-NAMING TABLE: rule 4 does not run inside it.
  - `data-fonte` / `data-referencia` mark a CITATION context: digits inside are
    references (§7, ADR 0027, ciclo 073, file:line…), not metric values, so
    rule 3 exempts them. Digit-bearing acronyms (A2A, F1, T16…) are exempt
    everywhere.
  - th/label/legend/h1/dt WITHOUT data-rotulo are label-checked by their text
    (a glossary term inside, or stopwords only). h2+ are section prose; button
    text is action phrasing — both are covered by rule 1/4 and the fresh
    review, not by the glossary check.

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
# h1 names the screen (domain); h2+ are section prose — not label-checked
LABEL_TAGS = {"th", "label", "legend", "h1", "dt"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}
RAW_TEXT = {"style", "script", "head", "title"}

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
# The "moldura" (interface frame) vocabulary declared by the screen authors
# (Worker04's interpretation 2) lives here; a NEW domain word is NOT added here
# — it gets a data-rotulo or it flags.
STOPWORDS = {
    "novo", "nova", "abrir", "fechar", "buscar", "salvar", "cancelar", "voltar",
    "exemplo", "exemplos", "sim", "não", "nao", "ok", "detalhes", "mais",
    "configurações", "configuracoes", "nome", "descrição", "descricao", "data",
    "estado", "ação", "acao", "filtro", "ordenar", "por", "de", "da", "do", "e",
    "em", "com", "sem", "para", "o", "a", "os", "as", "um", "uma", "que", "no",
    "na", "aos", "às", "the", "of", "and", "new", "open", "close", "save",
    "cancel", "back", "details", "more", "name", "date", "state", "action",
    "filter", "sort", "example", "yes", "no", "none",
    # interface frame ("moldura") words — declared, not domain
    "tipo", "consultar", "filtrar", "regra", "objeto", "efeito", "onde", "vive",
    "invariante", "verifica", "quem", "decide", "hoje", "aplicar", "moldura",
}

NUMBER = re.compile(r"\d")
WORD = re.compile(r"[\wà-ú/=-]+")
# digit-bearing acronyms are references, not metric values (A2A, F1, T16…)
ACRONYM = re.compile(r"\b[A-Za-z]+\d+[A-Za-z]*\b")


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
    carries the example mark (data-exemplo) or a citation context
    (data-fonte / data-referencia).
    """

    def __init__(self, path, terms):
        super().__init__()
        self.path = path
        self.terms = terms
        self.findings = []
        self.stack = []  # [tag, attrs-dict, label-text-so-far or None]
        self.tables = []  # one bool per open <table>: collision-naming?

    def error(self, message):
        pass

    # -- tree bookkeeping --------------------------------------------------

    def ancestor_attr(self, name):
        return any(name in a for _, a, _ in self.stack)

    def inside_example(self):
        return self.ancestor_attr("data-exemplo")

    def inside_citation(self):
        return self.ancestor_attr("data-fonte") or self.ancestor_attr("data-referencia")

    def inside_raw(self):
        return any(t in RAW_TEXT for t, _, _ in self.stack)

    def inside_label(self):
        """True while a label element is open — its text is checked by
        check_label, so rule 4 must not also run over the raw data node."""
        return any(text is not None for _, _, text in self.stack)

    def inside_collision_table(self):
        """Rule 4 exemption (a): inside a table that declares a
        data-rotulo="colisão de nomes" header, the colliding terms are named on
        purpose (map §7 reproduced) — declared in the markup, not inferred."""
        return any(self.tables)

    def collision_exempt(self, attrs=None):
        """Rule 4 exemptions. `attrs` is passed when we are looking at the
        element's OWN attributes (its data-exemplo is not on the stack yet)."""
        if self.inside_collision_table() or self.inside_example():
            return True
        return "data-exemplo" in (attrs or {})

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag in INTERACTIVE and not a.get("data-fonte", "").strip():
            self.findings.append(
                f"{self.path.name}: interactive <{tag}> without data-fonte")
        if tag == "table":
            self.tables.append(False)
        if tag in ("th", "dt") and self.tables \
                and "colisão de nomes" in a.get("data-rotulo", "").lower():
            self.tables[-1] = True
        # 4 (attribute pass). Attributes are read by whoever inspects the page:
        # an aria-label, a tooltip or a citation can carry the naked term too.
        if not self.collision_exempt(a):
            for value in a.values():
                self.check_collisions(value)
        if tag in VOID:
            return
        is_label = tag in LABEL_TAGS or "data-rotulo" in a
        self.stack.append([tag, a, "" if is_label else None])

    def handle_endtag(self, tag):
        # pop up to the matching open tag (tolerates stray closers)
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                closed = self.stack[i:]
                del self.stack[i:]
                if any(e[0] == "table" for e in closed) and self.tables:
                    self.tables.pop()
                for _, attrs, text in closed:
                    if text is not None:
                        self.check_label(text.strip(), attrs)
                return

    def handle_data(self, data):
        if not self.stack or self.inside_raw():
            return
        # 3. numbers must be marked as example — in every text node, unless
        #    it is a citation context or a digit-bearing acronym (A2A, F1…)
        stripped = ACRONYM.sub("", data)
        if NUMBER.search(stripped) and "exemplo" not in data.lower() \
                and not self.inside_example() and not self.inside_citation():
            self.findings.append(
                f'{self.path.name}: number without the "exemplo" mark: "{data.strip()}"')
        # 4 (visible-text pass). Not inside a label (check_label runs rule 4 for
        # those, at the closing tag) and not exempt: the naked term in prose is
        # where the review found the real violations.
        if not self.inside_label() and not self.collision_exempt():
            self.check_collisions(data)
        # feed the innermost open label collector
        for entry in reversed(self.stack):
            if entry[2] is not None:
                entry[2] += data
                break

    # -- the label rules ---------------------------------------------------

    def check_label(self, text, attrs):
        rotulo = attrs.get("data-rotulo", "").strip().lower()
        if rotulo:
            # a declared domain label: the VALUE must be a glossary term
            if not any(t.search(rotulo) for t in self.terms):
                self.findings.append(
                    f'{self.path.name}: data-rotulo outside the glossary: "{rotulo}"')
        elif text:
            low = text.lower()
            # 2. label outside the glossary: no glossary term inside and at
            #    least one word that is neither a stopword nor a number
            if not any(t.search(low) for t in self.terms):
                words = [w for w in WORD.findall(low)
                         if w not in STOPWORDS and not w.isdigit()]
                if words:
                    self.findings.append(
                        f'{self.path.name}: label outside the glossary: "{text}"')
        if not text:
            return
        # 4. collision-prone terms must be qualified — same test as the visible
        #    text and the attribute passes (check_collisions)
        if not self.collision_exempt(attrs):
            self.check_collisions(text)

    def check_collisions(self, text):
        """Rule 4: the colliding terms must be qualified wherever they surface.

        The qualifier must be a WORD of its own (word-boundary, not a substring):
        `painel/fila_outbox.py` names a file, it does not qualify the sentence
        around it — without this, the naked "fila" inside an attribute that also
        cites that path went unnoticed (R1b of the round-3 review). Same class of
        false negative as RACI ⊂ "operacional", fixed the same way.
        """
        low = text.lower()
        if re.search(r"\bfila\b", low) and not re.search(r"\bdecis\w*|\boutbox\b", low):
            self.findings.append(
                f'{self.path.name}: "fila" unqualified (decisões or outbox?): "{text.strip()}"')
        if re.search(r"\bport[ãa]o\b", low) and not re.search(r"\bchamado\b|\bregente\b", low):
            self.findings.append(
                f'{self.path.name}: "portão" unqualified (chamado or regente?): "{text.strip()}"')


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
