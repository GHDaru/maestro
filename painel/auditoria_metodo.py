#!/usr/bin/env python3
"""Audit, piece by piece, whether the Maestro method was executed on an integration line.

For every merge on the first-parent line of a branch (each merge = one integrated piece) it checks,
from git alone (read-only):
  spec_id     some commit of the piece cites a spec/item id (NNN, D12, E21, N3, P5, achado...)
  ears        the piece touches a spec.md or *ears*.md under specs/
  qa_report   the piece touches a specs/**/qa-report*.md
  red_first   a test-only commit precedes the first commit that touches production code
  mesmo_commit  the first production commit also carries the tests (no red phase)
  cor_crua    added .tsx lines use raw palette/hex instead of design tokens
  branch_nome the merged branch is named NNN-slug (Spec Kit convention)

Usage: python auditoria_metodo.py <repo> <branch> [--desde 2026-09-30] [--md saida.md] [--registrar projetos/x.json]
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import subprocess
import sys

ID = re.compile(r"(\b\d{3}\b|\b[DEFNPSAVCLTR]\d{1,3}\b|achado|finding|EARS|spec)", re.I)
TESTE = re.compile(r"(^|/)(tests?|__tests__)/|test_[^/]*\.py$|\.test\.tsx?$|\.spec\.tsx?$")
PROD = re.compile(r"^(src|frontend/src|app|alembic|migrations)/")
COR = re.compile(r"^\+.*(\b(bg|text|border)-(red|blue|gray|green|yellow|slate|zinc|amber|emerald|indigo|purple|orange|neutral)-\d{2,3}\b|#[0-9a-fA-F]{6}\b)")
BRANCH = re.compile(r"Merge (?:branch|remote-tracking branch) '([^']+)'|integrat\w* (?:de |of )?([\w./-]+)", re.I)


def git(repo, *a):
    r = subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.stdout if r.returncode == 0 else ""


def arquivos(repo, h):
    return [l for l in git(repo, "show", "--name-only", "--format=", h).splitlines() if l.strip()]


def audita(repo, branch, desde):
    merges = git(repo, "log", branch, "--first-parent", "--merges", f"--since={desde}",
                 "--format=%H%x1f%cI%x1f%s").splitlines()
    out = []
    for linha in merges:
        m, ts, assunto = linha.split("\x1f")
        commits = git(repo, "log", "--reverse", "--format=%H%x1f%s", f"{m}^1..{m}^2").splitlines()
        if not commits:
            continue
        lista = [c.split("\x1f") for c in commits]
        mudados = [l for l in git(repo, "diff", "--name-only", f"{m}^1...{m}^2").splitlines() if l]
        primeiro_prod, teste_antes = None, False
        for h, _ in lista:
            fs = arquivos(repo, h)
            tem_prod = any(PROD.search(f) and not TESTE.search(f) for f in fs)
            so_teste = fs and all(TESTE.search(f) or f.startswith("specs/") for f in fs) and any(TESTE.search(f) for f in fs)
            if tem_prod:
                primeiro_prod = (h, fs)
                break
            if so_teste:
                teste_antes = True
        mesmo = bool(primeiro_prod and any(TESTE.search(f) for f in primeiro_prod[1]) and not teste_antes)
        diff_tsx = git(repo, "diff", f"{m}^1...{m}^2", "--", "*.tsx")
        cores = sum(1 for l in diff_tsx.splitlines() if COR.search(l))
        bm = BRANCH.search(assunto)
        nome = (bm.group(1) or bm.group(2)) if bm else ""
        out.append({
            "merge": m[:8], "quando": ts[:16], "assunto": assunto[:90], "branch": nome, "commits": len(lista),
            "spec_id": any(ID.search(s) for _, s in lista) or bool(ID.search(assunto)),
            "ears": any(re.search(r"^specs/.*(spec\.md|ears[^/]*\.md)$", f) for f in mudados),
            "qa_report": any(re.search(r"^specs/.*qa-report[^/]*\.md$", f) for f in mudados),
            "red_first": teste_antes,
            "mesmo_commit": mesmo,
            "sem_prod": primeiro_prod is None,
            "cor_crua": cores,
            "branch_nome": bool(re.match(r"^(origin/)?\d{3}-", nome)),
        })
    return out


def markdown(res, repo, branch, desde):
    ok = lambda b: "✓" if b else "✗"
    n = len(res) or 1
    taxa = lambda k: f"{sum(1 for r in res if r[k])}/{len(res)} ({round(sum(1 for r in res if r[k]) / n * 100)}%)"
    L = [f"# Auditoria do método: {os.path.basename(repo)} `{branch}` desde {desde}",
         f"Gerada em {dt.datetime.now():%d/%m %H:%M}. Fonte: só o git (leitura). Cada linha é uma peça integrada (merge).", "",
         "| Critério | Peças conformes |", "|---|---|",
         f"| Commit cita spec/id | {taxa('spec_id')} |", f"| Spec/EARS na peça | {taxa('ears')} |",
         f"| qa-report na peça | {taxa('qa_report')} |", f"| Teste vermelho antes do código | {taxa('red_first')} |",
         f"| Branch com nome NNN-slug | {taxa('branch_nome')} |",
         f"| Teste e código no mesmo commit (desvio) | {sum(1 for r in res if r['mesmo_commit'])} |",
         f"| Cores cruas adicionadas em .tsx (linhas) | {sum(r['cor_crua'] for r in res)} |", "",
         "| Merge | Quando | Branch | Commits | id | EARS | qa | red antes | mesmo commit | cores | Assunto |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in res:
        L.append(f"| `{r['merge']}` | {r['quando']} | {r['branch'] or '—'} | {r['commits']} | {ok(r['spec_id'])} | {ok(r['ears'])} | "
                 f"{ok(r['qa_report'])} | {'—' if r['sem_prod'] else ok(r['red_first'])} | {'⚠' if r['mesmo_commit'] else ''} | "
                 f"{r['cor_crua'] or ''} | {r['assunto']} |")
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("repo"); ap.add_argument("branch")
    ap.add_argument("--desde", default="2026-09-30"); ap.add_argument("--md"); ap.add_argument("--registrar")
    a = ap.parse_args(argv)
    res = audita(a.repo, a.branch, a.desde)
    md = markdown(res, a.repo, a.branch, a.desde)
    if a.md:
        os.makedirs(os.path.dirname(os.path.abspath(a.md)), exist_ok=True)
        open(a.md, "w", encoding="utf-8").write(md)
    print(md)
    if a.registrar:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import ingest, server
        cfg = ingest.carrega_cfg(a.registrar)
        db = ingest.abre(os.path.join(ingest.AQUI, "dados", f"{cfg.get('projeto')}.db"))
        resumo = "; ".join(l.strip("| ").replace(" | ", ": ") for l in md.splitlines()[5:12])
        server.grava_evento(db, {"tipo": "nota", "sessao": "Assistente", "peca": f"auditoria {a.branch}",
                                 "texto": f"Auditoria do método ({len(res)} peças): {resumo}", "autor": "auditoria_metodo.py"})
        db.close()


if __name__ == "__main__":
    sys.exit(main())
