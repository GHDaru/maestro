#!/usr/bin/env python3
"""Maestro painel: localhost server (stdlib only).

Serves index.html and a read-mostly JSON API over the derived SQLite cache.
The only write is POST /api/eventos (append-only; the table refuses UPDATE/DELETE).

Usage: python server.py projetos/hindiana.json [--porta 8765] [--reingerir]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sqlite3
import statistics
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

import ingest

AQUI = os.path.dirname(os.path.abspath(__file__))
ESTADOS_SESSAO = ("trabalhando", "esperando", "sem tarefa", "bloqueado")
# Closed vocabulary of a piece, in order (hindiana, retro 30/09 02:01).
ESTADOS_PECA = ("spec", "red", "entregue", "suites aceitas", "aprovada as cegas", "integrada", "em producao")
EVIDENCIA_EXIGIDA = {
    "entregue": ("hash",),
    "suites aceitas": ("hash", "runner2"),
    "aprovada as cegas": ("hash", "par_montado_por", "descricao_factual"),
    "integrada": ("hash", "merge"),
    "em producao": ("hash", "deploy"),
}
ESTADOS_DEPLOY_OK = ("SUCCESS", "sucesso", "ok")


def conecta(db_path):
    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    return db


def linhas(db, sql, *args):
    return [dict(r) for r in db.execute(sql, args)]


def parse_ts(s):
    try:
        t = dt.datetime.fromisoformat(s)
        return t if t.tzinfo else t.astimezone()
    except (TypeError, ValueError):
        return None


# ---------- views ----------

def v_board(db):
    agora = dt.datetime.now().astimezone()
    limiar = int((db.execute("SELECT valor FROM meta WHERE chave='limiar_parado_min'").fetchone() or [60])[0])
    sessoes = {r["nome"]: r for r in linhas(db, "SELECT * FROM sessoes")}
    ult = linhas(db, """SELECT e.* FROM eventos e JOIN (SELECT sessao, MAX(id) mid FROM eventos
                        WHERE tipo='status' GROUP BY sessao) u ON e.id=u.mid""")
    status = {r["sessao"]: r for r in ult}
    nomes = sorted(set(sessoes) | set(status), key=ordem_sessao)
    cards = []
    for n in nomes:
        s, e = sessoes.get(n, {}), status.get(n)
        t = parse_ts(e["ts"]) if e else None
        idade = round((agora - t).total_seconds() / 60) if t else None
        estado = (e["estado"] if e else "") or "sem registro"
        cards.append({
            "sessao": n, "estado": estado, "em": (e or {}).get("texto") or s.get("papel", ""),
            "peca": (e or {}).get("peca") or "", "evidencia": (e or {}).get("evidencia") or "",
            "status_ts": e["ts"] if e else None, "idade_min": idade,
            "parado": idade is None or idade > limiar,
            "arquivo_papel": s.get("arquivo"), "estado_em_arquivo": s.get("estado_em"),
            "resumo_arquivo": s.get("estado_texto"), "worktree": s.get("worktree"),
            "ultimo_hash": s.get("ultimo_hash"), "proximo": s.get("proximo"),
            "historico": linhas(db, "SELECT ts, estado, texto, autor FROM eventos WHERE sessao=? AND tipo='status' ORDER BY id DESC LIMIT 8", n),
        })
    colunas = {k: [c for c in cards if c["estado"] == k] for k in ESTADOS_SESSAO}
    colunas["sem registro"] = [c for c in cards if c["estado"] not in ESTADOS_SESSAO]
    return {"limiar_min": limiar, "colunas": colunas, "total": len(cards)}


def ordem_sessao(n):
    ordem = {"Office": 0, "Hindiana Office": 0, "Torre": 1, "Assistente": 2, "Gerente": 3, "Gerente02": 4}
    if n in ordem:
        return (0, ordem[n], n)
    return (1, 0, n)


def v_pecas(db):
    evs = linhas(db, "SELECT * FROM eventos WHERE tipo='peca' ORDER BY id")
    pecas = {}
    for e in evs:
        p = pecas.setdefault(e["peca"], {"peca": e["peca"], "historico": []})
        p["historico"].append(e)
        p["estado"], p["sessao"], p["ts"] = e["estado"], e["sessao"], e["ts"]
        try:
            p["evidencia"] = json.loads(e["evidencia"] or "{}")
        except ValueError:
            p["evidencia"] = {"texto": e["evidencia"]}
    return {"estados": ESTADOS_PECA, "exigencias": EVIDENCIA_EXIGIDA,
            "colunas": {k: [p for p in pecas.values() if p["estado"] == k] for k in ESTADOS_PECA}}


def v_specs(db):
    return linhas(db, "SELECT * FROM specs ORDER BY repo, numero DESC")


def v_decisoes(db):
    return {"decisoes": linhas(db, "SELECT * FROM decisoes ORDER BY origem, rowid"),
            "adrs": linhas(db, "SELECT * FROM adrs ORDER BY data DESC")}


def v_qualidade(db):
    return {"barra": linhas(db, "SELECT * FROM barra_execucoes ORDER BY quando DESC"),
            "defeitos": linhas(db, "SELECT * FROM defeitos"),
            "desvios": linhas(db, "SELECT * FROM desvios ORDER BY n"),
            "classes": linhas(db, "SELECT classe, COUNT(*) n FROM desvios GROUP BY classe ORDER BY n DESC")}


def v_documentos(db):
    return {"documentos": linhas(db, "SELECT * FROM documentos ORDER BY tipo, idade_h"),
            "glossario": linhas(db, "SELECT * FROM glossario")}


def v_roadmap(db):
    out = []
    for r in linhas(db, "SELECT * FROM roadmap ORDER BY ordem"):
        out.append({"secao": r["secao"], "colunas": json.loads(r["colunas"]), "linha": json.loads(r["linha"])})
    return out


def v_rodadas(db):
    """T6: cada rodada com passo atual, tempo em cada passo, quem está nele."""
    try:
        rodadas = linhas(db, "SELECT * FROM rodadas ORDER BY aberta_em DESC")
    except sqlite3.OperationalError:
        return {"rodadas": []}
    out = []
    for r in rodadas:
        passos = linhas(db, "SELECT * FROM passos WHERE rodada=? ORDER BY id", r["id"])
        passo_atual = None
        quem = None
        passos_out = []
        for p in passos:
            if p["entrada_em"] and not p["saida_em"]:
                passo_atual = p["passo"]
                quem = p["sessao"]
            horas = None
            if p["entrada_em"] and p["saida_em"]:
                t0, t1 = parse_ts(p["entrada_em"]), parse_ts(p["saida_em"])
                if t0 and t1:
                    horas = round((t1 - t0).total_seconds() / 3600, 2)
            passos_out.append({
                "passo": p["passo"], "sessao": p["sessao"],
                "entrada_em": p["entrada_em"], "saida_em": p["saida_em"],
                "horas": horas, "resumo": p.get("resumo"), "resultado": p.get("resultado"),
            })
        out.append({
            "id": r["id"], "desejo": r["desejo"], "criada_por": r["criada_por"],
            "aberta_em": r["aberta_em"], "fechada_em": r["fechada_em"],
            "arquivo": r.get("arquivo", ""),
            "passo_atual": passo_atual, "quem": quem, "passos": passos_out,
        })
    return {"rodadas": out}


def semana(t):
    y, w, _ = t.isocalendar()
    return f"{y}-S{w:02d}"


def v_dora(db, dias=30):
    agora = dt.datetime.now().astimezone()
    ini = agora - dt.timedelta(days=dias)
    out = {"janela_dias": dias, "metricas": {}, "notas": []}

    # 1. Deploy frequency: real deploys (eventos) first; merges on main only as a labelled proxy.
    deps = [e for e in linhas(db, "SELECT * FROM eventos WHERE tipo='deploy' ORDER BY ts")
            if (parse_ts(e["ts"]) or ini) >= ini]
    ok = [d for d in deps if (d.get("estado") or "").lower() in [s.lower() for s in ESTADOS_DEPLOY_OK]]
    ent = linhas(db, "SELECT * FROM entregas WHERE repo IN (SELECT repo FROM entregas) ORDER BY ts")
    por_repo = {}
    for e in ent:
        t = parse_ts(e["ts"])
        if t and t >= ini:
            por_repo.setdefault(e["repo"], []).append(e)
    out["metricas"]["frequencia_deploy"] = {
        "valor": round(len(ok) / dias * 7, 2) if deps else None, "unidade": "deploys/semana",
        "fonte": "eventos tipo=deploy (registrados pela Office a partir do Railway)",
        "n": len(ok), "tentativas": len(deps),
        "proxy_entregas_por_repo": {r: round(len(v) / dias * 7, 2) for r, v in por_repo.items()},
        "serie": serie([parse_ts(d["ts"]) for d in ok]),
    }
    if not deps:
        out["notas"].append("Nenhum deploy registrado: merge na main não é deploy (push de 1e135b5 em 30/09). "
                            "Registre cada deploy com registrar.py deploy.")

    # 2. Lead time for changes: author date -> landing on the main line (per repo).
    lt = {}
    pais = {(r["repo"], r["hash"]): r["pais"] for r in linhas(db, "SELECT repo, hash, pais FROM commits WHERE primeiro_pai=1")}
    for r, v in por_repo.items():
        merges = [x for x in v if pais.get((r, x["hash"]), 1) > 1]
        base, criterio = (merges, "só merges (integração de branch)") if len(merges) >= 3 else (v, "todos os commits da linha principal")
        meds = sorted(x["lead_h_mediana"] for x in base if x["lead_h_mediana"] is not None)
        if meds:
            lt[r] = {"mediana_h": round(statistics.median(meds), 2), "p90_h": round(meds[max(0, int(len(meds) * 0.9) - 1)], 2),
                     "n": len(meds), "criterio": criterio}
    for r, x in lt.items():
        if x["mediana_h"] == 0:
            out["notas"].append(f"{r}: lead time 0 h porque os commits entram direto na linha principal (sem merge); "
                                "a medida útil para este repositório é hash entregue → integrado, registrado como peça.")
    out["metricas"]["lead_time"] = {"por_repo": lt, "unidade": "horas",
                                     "fonte": "git: data do autor -> commit na linha principal (first-parent)"}

    # 3. Change failure rate: failed deploys; bar runs that failed; corrective commits on the main line.
    barra = [b for b in linhas(db, "SELECT * FROM barra_execucoes") if (parse_ts(b["quando"]) or ini) >= ini]
    reprova = [b for b in barra if b["veredito"] == "REPROVA"]
    cfr_corr = {r: round(sum(x["eh_correcao"] for x in v) / len(v) * 100, 1) for r, v in por_repo.items() if v}
    out["metricas"]["taxa_falha"] = {
        "deploys_falhos_pct": round((len(deps) - len(ok)) / len(deps) * 100, 1) if deps else None,
        "barra_reprova_pct": round(len(reprova) / len(barra) * 100, 1) if barra else None,
        "barra_n": len(barra), "correcoes_na_linha_principal_pct": cfr_corr,
        "fonte": "eventos deploy; barra/execucoes; assunto de commit com fix/hotfix/revert/corrige",
    }

    # 4. Time to restore: incident -> recovery events; fallback bar REPROVA -> next PASSA per environment.
    inc = linhas(db, "SELECT * FROM eventos WHERE tipo IN ('incidente','recuperacao') ORDER BY ts")
    abertos, tempos = {}, []
    for e in inc:
        k = e["peca"] or e["texto"]
        if e["tipo"] == "incidente":
            abertos[k] = parse_ts(e["ts"])
        elif k in abertos and abertos[k]:
            tempos.append((parse_ts(e["ts"]) - abertos.pop(k)).total_seconds() / 3600)
    rec_barra = []
    for amb in {b["ambiente"] for b in barra}:
        seq = sorted([b for b in barra if b["ambiente"] == amb], key=lambda b: b["quando"])
        primeira = None
        for b in seq:
            if b["veredito"] == "REPROVA" and primeira is None:
                primeira = parse_ts(b["quando"])
            elif b["veredito"] == "PASSA" and primeira is not None:
                rec_barra.append((parse_ts(b["quando"]) - primeira).total_seconds() / 3600)
                primeira = None
    out["metricas"]["tempo_restauracao"] = {
        "incidentes_mediana_h": round(statistics.median(tempos), 2) if tempos else None,
        "incidentes_n": len(tempos), "incidentes_abertos": len(abertos),
        "barra_reprova_ate_passa_mediana_h": round(statistics.median(rec_barra), 2) if rec_barra else None,
        "fonte": "eventos incidente/recuperacao; barra: primeira REPROVA -> próxima PASSA no mesmo ambiente",
    }
    out["entregas_por_semana"] = {r: serie([parse_ts(x["ts"]) for x in v]) for r, v in por_repo.items()}
    return out


def serie(ts):
    s = {}
    for t in ts:
        if t:
            s[t.date().isoformat()] = s.get(t.date().isoformat(), 0) + 1
    return dict(sorted(s.items()))


def v_meta(db):
    m = {r["chave"]: r["valor"] for r in linhas(db, "SELECT * FROM meta")}
    m["equipes"] = json.loads(m.get("equipes") or "{}")
    # T8: idade do ingest para o frontend avisar se >1h
    if "ingerido_em" in m:
        t = parse_ts(m["ingerido_em"])
        if t:
            m["ingerido_age_min"] = round((dt.datetime.now().astimezone() - t).total_seconds() / 60, 1)
    return m


def v_erros_leitura(db):
    """T9: erros de leitura de arquivos — caminho e motivo, não vazio."""
    try:
        return linhas(db, "SELECT caminho, motivo, fonte FROM erros_leitura ORDER BY rowid")
    except sqlite3.OperationalError:
        return []


def v_higiene(db):
    wts = linhas(db, "SELECT * FROM worktrees ORDER BY integrada DESC, idade_d DESC")
    candidatas = [w for w in wts if w["integrada"] and not w["sujeira"] and not w["risco"]]
    return {"worktrees": wts, "total": len(wts), "integradas": sum(w["integrada"] for w in wts),
            "com_risco": [w for w in wts if w["risco"] and "protegida" not in w["risco"]],
            "branches_upstream_producao": linhas(db, "SELECT * FROM branches_risco"),
            "candidatas_remocao": candidatas,
            "regra": "candidata = branch já integrada na linha principal, sem alteração rastreada pendente e sem risco. "
                     "Remover só com ordem do Gilsiley (git worktree remove <caminho>)."}


def v_tempo(db):
    evs = linhas(db, "SELECT * FROM fases ORDER BY n")
    abertos, fechados = {}, []
    for e in evs:
        k = (e["rodada"], e["fase"], e["quem"])
        if e["evento"] == "inicio":
            abertos[k] = e
        elif e["evento"] == "fim" and k in abertos:
            i = abertos.pop(k)
            t0, t1 = parse_ts(i["ts"]), parse_ts(e["ts"])
            fechados.append({"rodada": k[0], "fase": k[1], "quem": k[2], "inicio": i["ts"], "fim": e["ts"],
                             "horas": round((t1 - t0).total_seconds() / 3600, 2) if t0 and t1 else None})
    por_fase = {}
    for f in fechados:
        por_fase[f["fase"]] = round(por_fase.get(f["fase"], 0) + (f["horas"] or 0), 2)
    return {"fechados": fechados, "abertos": list(abertos.values()), "por_fase": por_fase,
            "fonte": "ola/especificacao/tempos/ponto.jsonl (ponto.py do W04)"}


def v_estado_ia(db, sessao=None):
    """The 'active context' an agent reads at session start (memory-bank style, derived)."""
    b = v_board(db)
    q = v_qualidade(db)
    d = v_dora(db, 7)
    cards = [c for col in b["colunas"].values() for c in col]
    out = {
        "gerado_em": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "fonte": "painel Maestro (cache derivado; a verdade são os arquivos citados)",
        "equipe": [{"sessao": c["sessao"], "estado": c["estado"], "em": c["em"], "idade_min": c["idade_min"]} for c in cards],
        "ultimas_decisoes": linhas(db, "SELECT id, quando, titulo, desfazer FROM decisoes ORDER BY rowid LIMIT 8"),
        "barra_ultima": q["barra"][:1],
        "desvios_recentes": [{k: x[k] for k in ("quando", "quem", "classe", "candidato")} for x in q["desvios"][:6]],
        "riscos_git": [{k: w[k] for k in ("caminho", "branch", "risco")} for w in v_higiene(db)["com_risco"]],
        "dora_7d": d["metricas"],
    }
    if sessao:
        eu = next((c for c in cards if c["sessao"].lower() == sessao.lower()), None)
        out["voce"] = eu and {k: eu[k] for k in ("sessao", "estado", "em", "peca", "worktree", "ultimo_hash",
                                                  "proximo", "arquivo_papel", "historico")}
        out["seus_desvios"] = [x for x in q["desvios"] if sessao.lower() in (x["quem"] or "").lower()][:10]
        out["riscos_git"] = [r for r in out["riscos_git"] if sessao.lower() in (r["caminho"] or "").lower()] or out["riscos_git"]
    return out


def v_relatorio_lote(db, desde=None):
    """End-of-batch retro material (Markdown). Evidence only; MANTER/MUDAR/CORTAR stays human."""
    agora = dt.datetime.now().astimezone()
    ini = parse_ts(desde) if desde else agora - dt.timedelta(days=1)
    q, d, h = v_qualidade(db), v_dora(db, max(1, (agora - ini).days or 1)), v_higiene(db)
    barra = [b for b in q["barra"] if (parse_ts(b["quando"]) or agora) >= ini]
    L = [f"# Relatório de lote: {ini:%d/%m %H:%M} a {agora:%d/%m %H:%M}", "",
         "> Gerado pelo painel Maestro a partir dos arquivos. É evidência para a retro; a decisão "
         "(MANTER/MUDAR/CORTAR) é humana.", "", "## 1. Barra", ""]
    L += [f"- {b['quando']} {b['ambiente']} `{b['hash']}`: **{b['veredito']}** ({b['passos_com_erro']} de {b['passos']} passos com erro)"
          for b in barra] or ["- nenhuma volta no período"]
    L += ["", "## 2. DORA (com fonte)", ""]
    for k, v in d["metricas"].items():
        L.append(f"- **{k}**: " + ", ".join(f"{a}={b}" for a, b in v.items() if a not in ("serie", "fonte")) + f"  _(fonte: {v.get('fonte')})_")
    L += [f"- nota: {n}" for n in d["notas"]]
    L += ["", "## 3. Desvios por classe (todo o registro)", ""]
    L += [f"- {c['classe']}: {c['n']}" for c in q["classes"]]
    L += ["", "## 4. Desvios mais recentes e o candidato ao método", ""]
    L += [f"- {x['quando']} · {x['quem']} · {x['classe']}: {x['candidato']}" for x in q["desvios"][:10]]
    L += ["", "## 5. Higiene do git", "",
          f"- {h['total']} worktrees; {h['integradas']} com branch já integrada; {len(h['candidatas_remocao'])} candidatas à remoção (só com ordem do Gilsiley)."]
    L += [f"- RISCO {w['caminho']} ({w['branch']}): {w['risco']}" for w in h["com_risco"]]
    docs = linhas(db, "SELECT caminho, idade_h FROM documentos WHERE idade_h > 168 ORDER BY idade_h DESC")
    L += ["", "## 6. Documentos parados há mais de 7 dias", ""]
    L += [f"- {x['caminho']} ({round(x['idade_h'] / 24)} d)" for x in docs[:30]] or ["- nenhum"]
    L += ["", "## 7. Perguntas para a cerimônia", "",
          "1. Qual erro se repetiu, e por que a regra existente não o pegou?",
          "2. Qual regra não pagou por si e deve ser cortada?",
          "3. Qual passo manual se repetiu idêntico e deve virar ferramenta?"]
    return {"markdown": "\n".join(L)}


ROTAS = {"/api/board": v_board, "/api/pecas": v_pecas, "/api/specs": v_specs, "/api/decisoes": v_decisoes,
         "/api/qualidade": v_qualidade, "/api/documentos": v_documentos, "/api/roadmap": v_roadmap,
         "/api/rodadas": v_rodadas,
         "/api/dora": v_dora, "/api/meta": v_meta, "/api/estado-ia": v_estado_ia,
         "/api/erros": v_erros_leitura,
         "/api/higiene": v_higiene, "/api/tempo": v_tempo, "/api/relatorio-lote": v_relatorio_lote}


def valida_evento(ev):
    tipo = ev.get("tipo")
    if tipo not in ("status", "deploy", "incidente", "recuperacao", "peca", "nota"):
        return "tipo inválido"
    if not ev.get("autor"):
        return "autor é obrigatório"
    if tipo == "status" and ev.get("estado") not in ESTADOS_SESSAO:
        return f"estado de sessão deve ser um de {ESTADOS_SESSAO}"
    if tipo == "peca":
        if ev.get("estado") not in ESTADOS_PECA:
            return f"estado de peça deve ser um de {ESTADOS_PECA}"
        if not ev.get("peca"):
            return "peca é obrigatória"
        try:
            evid = json.loads(ev.get("evidencia") or "{}")
        except ValueError:
            return "evidencia deve ser JSON"
        faltam = [k for k in EVIDENCIA_EXIGIDA.get(ev["estado"], ()) if not evid.get(k)]
        if faltam:
            return f"sem prova não muda de coluna: faltam {faltam}"
    return None


def grava_evento(db, ev):
    erro = valida_evento(ev)
    if erro:
        raise ValueError(erro)
    ts = ev.get("ts") or dt.datetime.now().astimezone().isoformat(timespec="seconds")
    db.execute("INSERT INTO eventos (ts, sessao, tipo, estado, peca, texto, evidencia, autor) VALUES (?,?,?,?,?,?,?,?)",
               (ts, ev.get("sessao"), ev["tipo"], ev.get("estado"), ev.get("peca"), ev.get("texto"),
                ev.get("evidencia"), ev["autor"]))
    db.commit()


def cria_handler(db_path, cfg):
    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _json(self, obj, code=200):
            corpo = json.dumps(obj, ensure_ascii=False, default=str).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(corpo)

        def do_GET(self):
            u = urlparse(self.path)
            if u.path in ("/", "/index.html"):
                with open(os.path.join(AQUI, "index.html"), "rb") as f:
                    corpo = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(corpo)
                return
            fn = ROTAS.get(u.path)
            if not fn:
                return self._json({"erro": "rota inexistente"}, 404)
            db = conecta(db_path)
            qs = parse_qs(u.query)
            try:
                if u.path == "/api/dora":
                    return self._json(fn(db, int(qs.get("dias", ["30"])[0])))
                if u.path == "/api/estado-ia":
                    return self._json(fn(db, qs.get("sessao", [None])[0]))
                if u.path == "/api/relatorio-lote":
                    return self._json(fn(db, qs.get("desde", [None])[0]))
                return self._json(fn(db))
            finally:
                db.close()

        def do_POST(self):
            u = urlparse(self.path)
            if self.client_address[0] not in ("127.0.0.1", "::1"):
                return self._json({"erro": "só localhost"}, 403)
            if u.path == "/api/reingerir":
                return self._json(ingest.ingere(cfg, db_path))
            if u.path != "/api/eventos":
                return self._json({"erro": "rota inexistente"}, 404)
            n = int(self.headers.get("Content-Length") or 0)
            try:
                ev = json.loads(self.rfile.read(n) or b"{}")
                db = conecta(db_path)
                try:
                    grava_evento(db, ev)
                finally:
                    db.close()
            except ValueError as e:
                return self._json({"erro": str(e)}, 422)
            return self._json({"ok": True}, 201)

    return H


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("projeto")
    ap.add_argument("--porta", type=int, default=8765)
    ap.add_argument("--db", default=None)
    ap.add_argument("--reingerir", action="store_true")
    a = ap.parse_args(argv)
    cfg = ingest.carrega_cfg(a.projeto)
    db_path = a.db or os.path.join(AQUI, "dados", f"{cfg.get('projeto', 'painel')}.db")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    if a.reingerir or not os.path.exists(db_path):
        ingest.ingere(cfg, db_path)
    srv = ThreadingHTTPServer(("127.0.0.1", a.porta), cria_handler(db_path, cfg))
    print(f"painel em http://127.0.0.1:{a.porta}  (projeto {cfg.get('projeto')}, db {db_path})")
    srv.serve_forever()


if __name__ == "__main__":
    sys.exit(main())
