#!/usr/bin/env python3
"""Maestro painel: build the derived SQLite cache from the project's files.

Files are the source of truth (ADR 0008). Every derived table is dropped and rebuilt
on each run; only the append-only `eventos` table survives (facts that live in no file:
agent status, heartbeat, deploy). Stdlib only.

Usage: python ingest.py projeto.json [--db painel.db]
"""
from __future__ import annotations

import argparse
import datetime as dt
import glob
import json
import os
import re
import sqlite3
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))

# Paths the ingestion must never open (secrets, production personal data).
PROIBIDOS = (re.compile(r"(^|[\\/])\.env(\.|$)"), re.compile(r"backups_producao[\\/](?!diario[\\/]backup\.log$)"))

DERIVADAS = """
DROP TABLE IF EXISTS sessoes; DROP TABLE IF EXISTS commits; DROP TABLE IF EXISTS entregas;
DROP TABLE IF EXISTS decisoes; DROP TABLE IF EXISTS adrs; DROP TABLE IF EXISTS desvios;
DROP TABLE IF EXISTS barra_execucoes; DROP TABLE IF EXISTS defeitos; DROP TABLE IF EXISTS glossario;
DROP TABLE IF EXISTS documentos; DROP TABLE IF EXISTS specs; DROP TABLE IF EXISTS roadmap;
DROP TABLE IF EXISTS meta; DROP TABLE IF EXISTS worktrees; DROP TABLE IF EXISTS fases;
CREATE TABLE meta (chave TEXT PRIMARY KEY, valor TEXT);
CREATE TABLE worktrees (repo TEXT, caminho TEXT, branch TEXT, head TEXT, upstream TEXT,
  integrada INTEGER, ultimo_commit TEXT, idade_d REAL, sujeira INTEGER, risco TEXT,
  PRIMARY KEY (repo, caminho));
DROP TABLE IF EXISTS branches_risco;
CREATE TABLE branches_risco (repo TEXT, branch TEXT, upstream TEXT, PRIMARY KEY (repo, branch));
CREATE TABLE fases (n INTEGER PRIMARY KEY, ts TEXT, rodada TEXT, fase TEXT, quem TEXT, evento TEXT, nota TEXT);
CREATE TABLE sessoes (nome TEXT PRIMARY KEY, papel TEXT, arquivo TEXT, estado_em TEXT,
  estado_texto TEXT, worktree TEXT, ultimo_hash TEXT, proximo TEXT);
CREATE TABLE commits (repo TEXT, hash TEXT, ts TEXT, autor TEXT, assunto TEXT,
  pais INTEGER, primeiro_pai INTEGER, ts_autor TEXT, PRIMARY KEY (repo, hash));
CREATE TABLE entregas (repo TEXT, hash TEXT, ts TEXT, assunto TEXT, n_commits INTEGER,
  lead_h_mediana REAL, lead_h_max REAL, eh_correcao INTEGER, PRIMARY KEY (repo, hash));
CREATE TABLE decisoes (id TEXT, origem TEXT, quando TEXT, titulo TEXT, contexto TEXT,
  desfazer TEXT, PRIMARY KEY (origem, id));
CREATE TABLE adrs (arquivo TEXT PRIMARY KEY, data TEXT, titulo TEXT, estado TEXT);
CREATE TABLE desvios (n INTEGER PRIMARY KEY, quando TEXT, quem TEXT, fato TEXT, regra TEXT,
  acao TEXT, candidato TEXT, classe TEXT);
CREATE TABLE barra_execucoes (pasta TEXT PRIMARY KEY, quando TEXT, ambiente TEXT, hash TEXT,
  veredito TEXT, passos INTEGER, passos_com_erro INTEGER);
CREATE TABLE defeitos (volta TEXT, id TEXT, ocorrencias TEXT, criterio TEXT, descricao TEXT,
  com_quem TEXT, PRIMARY KEY (volta, id));
CREATE TABLE glossario (termo TEXT, definicao TEXT, evitar TEXT, fonte TEXT);
CREATE TABLE documentos (caminho TEXT PRIMARY KEY, tipo TEXT, titulo TEXT, modificado TEXT,
  linhas INTEGER, idade_h REAL);
CREATE TABLE specs (repo TEXT, numero TEXT, slug TEXT, titulo TEXT, status TEXT,
  tasks_total INTEGER, tasks_feitas INTEGER, tem_plan INTEGER, tem_qa INTEGER, modificado TEXT,
  PRIMARY KEY (repo, numero, slug));
CREATE TABLE roadmap (ordem INTEGER PRIMARY KEY, secao TEXT, colunas TEXT, linha TEXT);
"""

EVENTOS = """
CREATE TABLE IF NOT EXISTS eventos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL,
  sessao TEXT,
  tipo TEXT NOT NULL CHECK (tipo IN ('status','deploy','incidente','recuperacao','peca','nota')),
  estado TEXT,
  peca TEXT,
  texto TEXT,
  evidencia TEXT,
  autor TEXT NOT NULL
);
CREATE TRIGGER IF NOT EXISTS eventos_sem_update BEFORE UPDATE ON eventos
  BEGIN SELECT RAISE(ABORT, 'eventos e append-only'); END;
CREATE TRIGGER IF NOT EXISTS eventos_sem_delete BEFORE DELETE ON eventos
  BEGIN SELECT RAISE(ABORT, 'eventos e append-only'); END;
CREATE TABLE IF NOT EXISTS ingest_log (id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, duracao_ms INTEGER, contagem TEXT);
"""


def proibido(caminho: str) -> bool:
    c = caminho.replace("\\", "/")
    return any(p.search(c) for p in PROIBIDOS)


def ler(caminho: str) -> str:
    if proibido(caminho):
        raise PermissionError(f"caminho proibido para a ingestao: {caminho}")
    with open(caminho, encoding="utf-8", errors="replace") as f:
        return f.read()


def agora() -> dt.datetime:
    return dt.datetime.now().astimezone()


# ---------- markdown helpers ----------

def tabelas_md(texto: str):
    """Yield (heading, header_cells, rows) for every pipe table in the text."""
    titulo = ""
    linhas = texto.splitlines()
    i = 0
    while i < len(linhas):
        l = linhas[i]
        if l.startswith("#"):
            titulo = l.lstrip("#").strip()
        if l.strip().startswith("|") and i + 1 < len(linhas) and re.match(r"^\s*\|[\s:\-|]+\|\s*$", linhas[i + 1]):
            cab = celulas(l)
            i += 2
            rows = []
            while i < len(linhas) and linhas[i].strip().startswith("|"):
                rows.append(celulas(linhas[i]))
                i += 1
            yield titulo, cab, rows
            continue
        i += 1


def celulas(linha: str):
    s = linha.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    partes = re.split(r"(?<!\\)\|", s)
    return [p.strip() for p in partes]


def limpa(md: str) -> str:
    return re.sub(r"\*\*|`", "", md or "").strip()


def norm(s: str) -> str:
    import unicodedata
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(ch for ch in s if not unicodedata.combining(ch))


def coluna(cab, *nomes):
    nc = [norm(c) for c in cab]
    for n in nomes:
        for i, c in enumerate(nc):
            if c.startswith(norm(n)):
                return i
    return None


# ---------- sources ----------

def ingere_sessoes(db, cfg):
    pasta = cfg.get("equipe")
    if not pasta:
        return 0
    n = 0
    for arq in sorted(glob.glob(os.path.join(pasta, "*.md"))):
        base = os.path.basename(arq)
        if base.upper().startswith("LEIA"):
            continue
        txt = ler(arq)
        m = re.search(r"^#\s+(.+)$", txt, re.M)
        nome = norm_sessao(m.group(1) if m else base[:-3])
        bloco = re.search(r"^##\s+Estado atual\s*\(?([^)\n]*)\)?[^\n]*\n(.*?)(?=^##\s|\Z)", txt, re.M | re.S)
        estado_em, corpo = (bloco.group(1).strip(), bloco.group(2).strip()) if bloco else ("", "")

        def campo(*rot):
            for r in rot:
                mm = re.search(r"\*\*" + r + r"[^*]*:\*\*\s*(.+)", corpo, re.I)
                if mm:
                    return limpa(mm.group(1))
            return ""

        papel = campo("Papel", "Pe[cç]a", "Bloco")
        worktree = campo("Worktree")
        hash_ = campo("[UÚ]ltimo hash")
        if not hash_:
            mh = re.search(r"`([0-9a-f]{7,40})`", corpo)
            hash_ = mh.group(1) if mh else ""
        proximo = campo("Pr[oó]ximo")
        if not proximo:
            mp = re.search(r"Pr[oó]ximo[^:]*:\s*(.+)", corpo)
            proximo = limpa(mp.group(1)) if mp else ""
        resumo = "\n".join(l for l in corpo.splitlines() if l.strip().startswith("-"))[:1200]
        db.execute("INSERT OR REPLACE INTO sessoes VALUES (?,?,?,?,?,?,?,?)",
                   (nome, papel, rel(cfg, arq), estado_em, limpa(resumo), worktree, hash_[:40], proximo))
        n += 1
    return n


def norm_sessao(nome: str) -> str:
    nome = nome.strip()
    m = re.match(r"(?i)worker[\s\-_]*0?(\d+)", nome)
    if m:
        return f"W{int(m.group(1)):02d}"
    m = re.match(r"(?i)w0?(\d+)$", nome)
    if m:
        return f"W{int(m.group(1)):02d}"
    if re.match(r"(?i)gerente[\s\-_]*0?2", nome):
        return "Gerente02"
    return nome.split(":")[0].split("(")[0].strip()


def git(repo, *args):
    for tentativa in range(3):
        try:
            r = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True,
                               encoding="utf-8", errors="replace")
            break
        except OSError:  # transient process-creation failure on Windows
            if tentativa == 2:
                return ""
    if r.returncode != 0:
        return ""
    return r.stdout


CORRECAO = re.compile(r"(?i)\b(hotfix|fix|corrige|corre[cç][aã]o|revert|rollback)\b")


def ingere_git(db, cfg):
    total = 0
    for rep in cfg.get("repos", []):
        nome, caminho = rep["nome"], rep["caminho"]
        ref = rep.get("principal", "main")
        if not git(caminho, "rev-parse", "--verify", "--quiet", ref).strip():
            continue
        limite = str(rep.get("limite", 3000))
        fp = set(git(caminho, "rev-list", "--first-parent", ref, "-n", limite).split())
        out = git(caminho, "log", ref, "-n", limite, "--format=%H%x1f%cI%x1f%an%x1f%s%x1f%P%x1f%aI")
        for linha in out.splitlines():
            h, ts, autor, assunto, pais, ts_autor = (linha.split("\x1f") + [""] * 6)[:6]
            npais = len(pais.split())
            db.execute("INSERT OR REPLACE INTO commits VALUES (?,?,?,?,?,?,?,?)",
                       (nome, h, ts, autor, assunto, npais, 1 if h in fp else 0, ts_autor))
            total += 1
        # deliveries: each first-parent commit on the main line; lead time = author date -> landing
        for h in fp:
            row = db.execute("SELECT ts, assunto, pais, ts_autor FROM commits WHERE repo=? AND hash=?", (nome, h)).fetchone()
            if not row:
                continue
            ts_main, assunto, npais, ts_autor = row
            if npais > 1:
                datas = git(caminho, "log", f"{h}^1..{h}", "--format=%aI").split()
            else:
                datas = [ts_autor] if ts_autor else []
            t_main = dt.datetime.fromisoformat(ts_main)
            leads = sorted(max(0.0, (t_main - dt.datetime.fromisoformat(d)).total_seconds() / 3600) for d in datas)
            if not leads:
                continue
            med = leads[len(leads) // 2]
            db.execute("INSERT OR REPLACE INTO entregas VALUES (?,?,?,?,?,?,?,?)",
                       (nome, h, ts_main, assunto, len(leads), round(med, 2), round(leads[-1], 2),
                        1 if CORRECAO.search(assunto) else 0))
    return total


def ingere_decisoes(db, cfg):
    n = 0
    for arq in expande(cfg.get("decisoes", [])):
        txt = ler(arq)
        for _, cab, rows in tabelas_md(txt):
            ci, ch, cd, cc, cu = (coluna(cab, "#"), coluna(cab, "hora", "quando", "data"),
                                  coluna(cab, "decis"), coluna(cab, "contexto"), coluna(cab, "como desfazer"))
            if ci is None or cd is None:
                continue
            for r in rows:
                g = lambda k: limpa(r[k]) if k is not None and k < len(r) else ""
                if not g(ci):
                    continue
                db.execute("INSERT OR REPLACE INTO decisoes VALUES (?,?,?,?,?,?)",
                           (g(ci), rel(cfg, arq), g(ch), g(cd)[:600], g(cc)[:800], g(cu)[:300]))
                n += 1
    jsonl = cfg.get("decisoes_jsonl")
    if jsonl and os.path.exists(jsonl):
        for linha in ler(jsonl).splitlines():
            try:
                d = json.loads(linha)
            except ValueError:
                continue
            db.execute("INSERT OR REPLACE INTO decisoes VALUES (?,?,?,?,?,?)",
                       (d.get("id", ""), rel(cfg, jsonl), d.get("data", ""), d.get("titulo", ""),
                        d.get("status", ""), d.get("registro", "")))
            n += 1
    return n


def ingere_adrs(db, cfg):
    n = 0
    for arq in expande(cfg.get("adrs", [])):
        txt = ler(arq)
        m = re.search(r"^#\s+(.+)$", txt, re.M)
        est = re.search(r"(?im)^\**\s*(?:estado|status)\**\s*[:|]\s*\**([^\n|*]+)", txt)
        data = re.search(r"(\d{4}-\d{2}-\d{2})", os.path.basename(arq)) or re.search(r"(\d{4}-\d{2}-\d{2})", txt)
        db.execute("INSERT OR REPLACE INTO adrs VALUES (?,?,?,?)",
                   (rel(cfg, arq), data.group(1) if data else "", limpa(m.group(1)) if m else os.path.basename(arq),
                    limpa(est.group(1)) if est else ""))
        n += 1
    return n


CLASSES = [
    ("TDD / teste antes", r"red|vermelh|mesmo commit|sem teste|tdd|princ[ií]pio iv"),
    ("Spec / EARS", r"ears|spec-driven|princ[ií]pio i\b|sem spec"),
    ("Caminho real / contrato", r"contrato|mock|caminho real|fixture|formato"),
    ("Evidencia / prova", r"✅|evid[eê]ncia|sem prova|runner2|tsc|n[uú]meros? locais"),
    ("Critico / par cego", r"cr[ií]tic|par cego|[aà]s cegas"),
    ("Segredo / dado de producao", r"segredo|senha|chave|token|produ[cç][aã]o"),
    ("Git / caminho / branch", r"worktree|branch|caminho|commit -a|hash"),
    ("Infra / ensaio", r"ensaio|bash -n|fila|vm|bancada|banca"),
]


def classe_desvio(texto: str) -> str:
    t = texto.lower()
    for nome, rx in CLASSES:
        if re.search(rx, t):
            return nome
    return "Outro"


def ingere_desvios(db, cfg):
    n = 0
    for arq in expande(cfg.get("retro", [])):
        for _, cab, rows in tabelas_md(ler(arq)):
            cq, cw, cf = coluna(cab, "when", "quando"), coluna(cab, "who", "quem"), coluna(cab, "what happened", "o que")
            if cq is None or cw is None or cf is None:
                continue
            cr, ca, cc = coluna(cab, "rule", "regra"), coluna(cab, "what was done", "o que foi feito", "acao"), coluna(cab, "candidat")
            for r in rows:
                g = lambda k: limpa(r[k]) if k is not None and k < len(r) else ""
                n += 1
                db.execute("INSERT INTO desvios VALUES (?,?,?,?,?,?,?,?)",
                           (n, g(cq), g(cw), g(cf)[:900], g(cr)[:300], g(ca)[:400], g(cc)[:400],
                            classe_desvio(g(cf) + " " + g(cr))))
    return n


def ingere_barra(db, cfg):
    n = 0
    pasta = cfg.get("barra_execucoes")
    if pasta and os.path.isdir(pasta):
        for d in sorted(os.listdir(pasta)):
            rel_md = os.path.join(pasta, d, "relatorio.md")
            if not os.path.exists(rel_md):
                continue
            txt = ler(rel_md)
            m = re.match(r"(\d{8})_(\d{4})_([a-z0-9]+)_([0-9a-f]+)", d)
            quando = ""
            if m:
                quando = f"{m.group(1)[:4]}-{m.group(1)[4:6]}-{m.group(1)[6:]}T{m.group(2)[:2]}:{m.group(2)[2:]}"
            v = re.search(r"Veredito:\s*([A-ZÇÃ]+)", txt)
            p = re.search(r"(\d+)\s+passos,\s+(\d+)\s+com erro", txt)
            db.execute("INSERT OR REPLACE INTO barra_execucoes VALUES (?,?,?,?,?,?,?)",
                       (d, quando, m.group(3) if m else "", m.group(4) if m else "",
                        v.group(1) if v else "", int(p.group(1)) if p else None, int(p.group(2)) if p else None))
            n += 1
    for arq in expande(cfg.get("barra_resultados", [])):
        txt = ler(arq)
        for titulo, cab, rows in tabelas_md(txt):
            cd = coluna(cab, "defeito")
            if cd is None:
                continue
            co, cc, cq, cw = coluna(cab, "ocorr"), coluna(cab, "crit"), coluna(cab, "o que"), coluna(cab, "com quem")
            for r in rows:
                g = lambda k: limpa(r[k]) if k is not None and k < len(r) else ""
                db.execute("INSERT OR REPLACE INTO defeitos VALUES (?,?,?,?,?,?)",
                           (titulo[:120], g(cd), g(co), g(cc), g(cq)[:400], g(cw)))
    return n


def ingere_glossario(db, cfg):
    n = 0
    for arq in expande(cfg.get("glossario", [])):
        for _, cab, rows in tabelas_md(ler(arq)):
            ct, cd = coluna(cab, "termo", "term"), coluna(cab, "defini")
            if ct is None or cd is None:
                continue
            ce = coluna(cab, "evitar", "avoid")
            for r in rows:
                g = lambda k: limpa(r[k]) if k is not None and k < len(r) else ""
                if g(ct):
                    db.execute("INSERT INTO glossario VALUES (?,?,?,?)", (g(ct), g(cd)[:600], g(ce), rel(cfg, arq)))
                    n += 1
    return n


def ingere_documentos(db, cfg):
    n = 0
    t0 = agora()
    for tipo, padroes in cfg.get("documentos", {}).items():
        for arq in expande(padroes):
            if proibido(arq):
                continue
            st = os.stat(arq)
            mod = dt.datetime.fromtimestamp(st.st_mtime).astimezone()
            try:
                txt = ler(arq)
            except (OSError, PermissionError):
                continue
            m = re.search(r"^#\s+(.+)$", txt, re.M)
            db.execute("INSERT OR REPLACE INTO documentos VALUES (?,?,?,?,?,?)",
                       (rel(cfg, arq), tipo, limpa(m.group(1)) if m else os.path.basename(arq), mod.isoformat(timespec="minutes"),
                        txt.count("\n") + 1, round((t0 - mod).total_seconds() / 3600, 1)))
            n += 1
    return n


def ingere_specs(db, cfg):
    n = 0
    for rep in cfg.get("specs", []):
        for d in sorted(glob.glob(os.path.join(rep["caminho"], "[0-9][0-9][0-9]-*"))):
            if not os.path.isdir(d):
                continue
            base = os.path.basename(d)
            numero, slug = base[:3], base[4:]
            spec = os.path.join(d, "spec.md")
            titulo, status = slug, ""
            if os.path.exists(spec):
                t = ler(spec)
                m = re.search(r"^#\s+(.+)$", t, re.M)
                titulo = limpa(m.group(1)) if m else slug
                s = re.search(r"(?im)\**status\**\s*[:|]\s*\**([^\n|*·]+)", t)
                status = limpa(s.group(1)) if s else ""
            tot = feitas = 0
            tasks = os.path.join(d, "tasks.md")
            if os.path.exists(tasks):
                tt = ler(tasks)
                tot = len(re.findall(r"^\s*-\s*\[[ xX]\]", tt, re.M))
                feitas = len(re.findall(r"^\s*-\s*\[[xX]\]", tt, re.M))
            mods = [os.stat(os.path.join(d, f)).st_mtime for f in os.listdir(d)] or [os.stat(d).st_mtime]
            db.execute("INSERT OR REPLACE INTO specs VALUES (?,?,?,?,?,?,?,?,?,?)",
                       (rep["nome"], numero, slug, titulo[:200], status[:60], tot, feitas,
                        int(os.path.exists(os.path.join(d, "plan.md"))),
                        int(bool(glob.glob(os.path.join(d, "qa-report*.md")))),
                        dt.datetime.fromtimestamp(max(mods)).astimezone().isoformat(timespec="minutes")))
            n += 1
    return n


def ingere_roadmap(db, cfg):
    n = 0
    for arq in expande(cfg.get("roadmap", [])):
        for titulo, cab, rows in tabelas_md(ler(arq)):
            for r in rows:
                n += 1
                db.execute("INSERT INTO roadmap VALUES (?,?,?,?)",
                           (n, titulo, json.dumps(cab, ensure_ascii=False), json.dumps([limpa(x) for x in r], ensure_ascii=False)))
    return n


def ingere_worktrees(db, cfg):
    """Worktree hygiene: integrated/abandoned trees and branches whose upstream is the production line."""
    n = 0
    t0 = agora()
    for rep in cfg.get("repos", []):
        caminho, ref = rep["caminho"], rep.get("principal", "main")
        integradas = {b.strip().lstrip("*+ ").strip() for b in git(caminho, "branch", "--merged", ref).splitlines()}
        ups = {}
        for l in git(caminho, "for-each-ref", "--format=%(refname:short)|%(upstream:short)|%(committerdate:iso-strict)",
                     "refs/heads").splitlines():
            b, u, d = (l.split("|") + ["", ""])[:3]
            ups[b] = (u, d)
            if u and re.search(r"(^|/)(main|master)$", u) and b not in ("main", "master"):
                db.execute("INSERT OR REPLACE INTO branches_risco VALUES (?,?,?)", (rep["nome"], b, u))
        blocos =git(caminho, "worktree", "list", "--porcelain").strip().split("\n\n")
        for bl in blocos:
            campos = dict((l.split(" ", 1) + [""])[:2] for l in bl.splitlines() if l)
            wt = campos.get("worktree")
            if not wt or os.path.normcase(os.path.normpath(wt)) == os.path.normcase(os.path.normpath(caminho)):
                continue
            branch = campos.get("branch", "").replace("refs/heads/", "")
            up, data = ups.get(branch, ("", ""))
            t = dt.datetime.fromisoformat(data) if data else None
            idade = round((t0 - t).total_seconds() / 86400, 1) if t else None
            integrada = int(branch in integradas) if branch else 0
            riscos = []
            if up and re.search(r"(^|/)(main|master)$", up) and branch not in ("main", "master"):
                riscos.append("upstream na linha de producao: git push vai para a main")
            if "prunable" in campos:
                riscos.append("pasta sumiu (prunable)")
            if "detached" in campos:
                riscos.append("HEAD destacado")
            if any(re.search(p, rel(cfg, wt)) for p in cfg.get("worktree_protegidas", [])):
                riscos.append("protegida (em uso pela entrega)")
            sujeira = None
            if cfg.get("worktree_sujeira") and os.path.isdir(wt) and (integrada or (idade or 0) > 3):
                sujeira = int(bool(git(wt, "status", "--porcelain", "--untracked-files=no").strip()))
            db.execute("INSERT OR REPLACE INTO worktrees VALUES (?,?,?,?,?,?,?,?,?,?)",
                       (rep["nome"], rel(cfg, wt), branch, campos.get("HEAD", "")[:10], up, integrada,
                        data, idade, sujeira, "; ".join(riscos)))
            n += 1
    return n


def ingere_fases(db, cfg):
    arq = cfg.get("ponto")
    if not arq or not os.path.exists(arq):
        return 0
    n = 0
    for linha in ler(arq).splitlines():
        try:
            d = json.loads(linha)
        except ValueError:
            continue
        n += 1
        db.execute("INSERT INTO fases VALUES (?,?,?,?,?,?,?)",
                   (n, d.get("timestamp"), d.get("rodada"), d.get("fase"), d.get("quem"), d.get("evento"), d.get("nota")))
    return n


# ---------- plumbing ----------

def expande(padroes):
    if isinstance(padroes, str):
        padroes = [padroes]
    saida = []
    for p in padroes:
        saida.extend(sorted(glob.glob(p, recursive=True)))
    return [s for s in saida if os.path.isfile(s) and not proibido(s)]


def rel(cfg, caminho):
    raiz = cfg.get("raiz")
    try:
        return os.path.relpath(caminho, raiz).replace("\\", "/") if raiz else caminho
    except ValueError:
        return caminho


def carrega_cfg(caminho):
    with open(caminho, encoding="utf-8") as f:
        cfg = json.load(f)
    base = os.path.dirname(os.path.abspath(caminho))
    raiz = os.path.normpath(os.path.join(base, cfg.get("raiz", ".")))
    cfg["raiz"] = raiz

    def absol(v):
        if isinstance(v, str):
            return os.path.normpath(os.path.join(raiz, v))
        if isinstance(v, list):
            return [absol(x) for x in v]
        return v

    for k in ("equipe", "decisoes", "decisoes_jsonl", "adrs", "retro", "barra_execucoes",
              "barra_resultados", "glossario", "roadmap", "ponto"):
        if k in cfg:
            cfg[k] = absol(cfg[k])
    for k in ("repos", "specs"):
        for rep in cfg.get(k, []):
            rep["caminho"] = absol(rep["caminho"])
    cfg["documentos"] = {t: absol(v) for t, v in cfg.get("documentos", {}).items()}
    return cfg


def abre(db_path):
    db = sqlite3.connect(db_path)
    db.executescript(EVENTOS)
    return db


def ingere(cfg, db_path):
    inicio = agora()
    db = abre(db_path)
    db.executescript(DERIVADAS)
    contagem = {}
    for nome, fn in [("sessoes", ingere_sessoes), ("commits", ingere_git), ("decisoes", ingere_decisoes),
                     ("adrs", ingere_adrs), ("desvios", ingere_desvios), ("barra", ingere_barra),
                     ("glossario", ingere_glossario), ("documentos", ingere_documentos),
                     ("specs", ingere_specs), ("roadmap", ingere_roadmap),
                     ("worktrees", ingere_worktrees), ("fases", ingere_fases)]:
        try:
            contagem[nome] = fn(db, cfg)
        except PermissionError:
            raise
        except Exception as e:  # one broken source must not hide the others
            contagem[nome] = f"erro: {e}"
    db.execute("INSERT INTO meta VALUES ('projeto', ?)", (cfg.get("projeto", ""),))
    db.execute("INSERT INTO meta VALUES ('ingerido_em', ?)", (agora().isoformat(timespec="seconds"),))
    db.execute("INSERT INTO meta VALUES ('contagem', ?)", (json.dumps(contagem, ensure_ascii=False),))
    db.execute("INSERT INTO meta VALUES ('limiar_parado_min', ?)", (str(cfg.get("limiar_parado_min", 60)),))
    db.execute("INSERT INTO meta VALUES ('equipes', ?)", (json.dumps(cfg.get("equipes", {}), ensure_ascii=False),))
    db.execute("INSERT INTO meta VALUES ('titulo', ?)", (cfg.get("titulo", cfg.get("projeto", "")),))
    db.execute("INSERT INTO ingest_log (ts, duracao_ms, contagem) VALUES (?,?,?)",
               (agora().isoformat(timespec="seconds"), int((agora() - inicio).total_seconds() * 1000),
                json.dumps(contagem, ensure_ascii=False)))
    db.commit()
    db.close()
    return contagem


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("projeto")
    ap.add_argument("--db", default=None)
    a = ap.parse_args(argv)
    cfg = carrega_cfg(a.projeto)
    db_path = a.db or os.path.join(AQUI, "dados", f"{cfg.get('projeto', 'painel')}.db")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    c = ingere(cfg, db_path)
    print(json.dumps({"db": db_path, "contagem": c}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    sys.exit(main())
