"""Chamados gate a gate: lê specs/<id>/ direto do git e calcula o estado de cada gate.

Mesmas regras de hindiana scripts/maestro/conferir_chamado.py (padrão em
hindiana DOCS/processo/padrao-chamado.md). O estado nunca é digitado: vem dos
arquivos de gate e do git. Só lê; não grava nada.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import subprocess

GATES = [
    ("abertura", "Abertura", "Office"),
    ("G0", "Reprodução", "Sessão de testes"),
    ("GD", "Risco", "Office"),
    ("G1", "Spec", "Crítico de spec"),
    ("G2", "Vermelho", "Autor e crítico"),
    ("G3", "Crítica e runner2", "Críticos e runner2"),
    ("G4", "VM", "Office"),
    ("G5", "Barra no Dev", "Office"),
    ("G6", "Teste por tela", "Sessão de testes"),
    ("G7", "Aceite do cliente", "Cliente"),
    ("G8", "Ordem de produção", "Gilsiley"),
    ("G9", "Pospush", "Office"),
]
PREFIXO = {"abertura": "00-chamado"}
PASSA = {"G0": {"REPRODUZIDO"}, "G4": {"OK"}, "G5": {"PASSA"}, "G6": {"PASSA"}, "G7": {"ACEITO"},
         "G8": {"ORDEM"}, "G9": {"OK"}}
BARRA = {"G0": {"NAO_REPRODUZIDO"}, "G4": {"FALHA"}, "G5": {"REPROVA"}, "G6": {"FALHA"}, "G7": {"RECUSADO"},
         "G8": {"SEM_ORDEM"}, "G9": {"ROLLBACK"}}
OBRIG = {"abertura": ["gate", "tipo", "aberto_por", "data", "origem"], "GD": ["gate", "classe", "por", "data"],
         "_": ["gate", "objeto", "veredito", "por", "data"]}
RE_OBJ = re.compile(r"^(.+?) @ ([0-9a-f]{7,40})$")
RE_DATA = re.compile(r"^(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2})(?::\d{2})? ?([+-]\d{4})?$")


def _git(repo, *args):
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.stdout if r.returncode == 0 else None


def cabecalho(txt: str) -> dict:
    if not txt.startswith("---"):
        return {}
    fim = txt.find("\n---", 3)
    if fim < 0:
        return {}
    out = {}
    for linha in txt[3:fim].splitlines():
        if not linha.strip() or linha.lstrip().startswith("#") or ":" not in linha:
            continue
        k, v = linha.split(":", 1)
        out[k.strip()] = re.sub(r"\s+#.*$", "", v).strip().strip('"').strip("'")
    return out


def titulo(txt: str) -> str:
    m = re.search(r"^# (.+)$", txt, re.M)
    return m.group(1).strip() if m else ""


def data(s):
    m = RE_DATA.match(s or "")
    if not m:
        return None
    return dt.datetime.strptime(f"{m.group(1)} {m.group(2)} {m.group(3) or '-0300'}", "%Y-%m-%d %H:%M %z")


def valida(h, gate, data_hash, autores):
    erros = []
    for k in OBRIG.get(gate, OBRIG["_"]):
        if not h.get(k):
            erros.append(f"falta '{k}' no cabeçalho")
    if h.get("data") and not data(h["data"]):
        erros.append(f"data fora do formato: {h['data']}")
    obj = h.get("objeto")
    if obj:
        if re.search(r"[*`]", obj):
            erros.append("objeto com negrito ou crase")
        m = RE_OBJ.match(obj.replace("*", "").replace("`", ""))
        if not m:
            erros.append("objeto fora do formato '<caminho> @ <hash>'")
        else:
            real = data_hash(m.group(2))
            if real is None:
                erros.append(f"hash {m.group(2)} não existe no repo")
            else:
                dobj, dv = data(h.get("data_objeto", "")), data(h.get("data", ""))
                if dobj and abs((dobj - real).total_seconds()) > 120:
                    erros.append(f"data_objeto {h['data_objeto'][11:16]} não confere com o git ({real:%H:%M})")
                if dv and dv < real.replace(second=0) - dt.timedelta(minutes=2):
                    erros.append(f"veredito anterior ao objeto ({h['data'][11:16]} < {real:%H:%M})")
    if gate in ("G1", "G3") and h.get("por") in autores:
        erros.append(f"crítico {h['por']} é autor da peça")
    if gate == "G3" and h.get("papel") == "runner2" and h.get("numeros") and not re.search(r"/0/0\b", h["numeros"]):
        erros.append(f"runner2 sem 0 failed e 0 errors ({h['numeros']})")
    return erros


def confere(arquivos: dict, data_hash, tem_spec: bool) -> dict:
    """arquivos: {nome: texto} da pasta do chamado. data_hash(h) -> datetime | None."""
    ab_nome = next((n for n in sorted(arquivos) if n.startswith("00-chamado")), None)
    ab_txt = arquivos.get(ab_nome, "")
    hab = cabecalho(ab_txt)
    tipo = hab.get("tipo", "")
    autores = {a.strip() for a in hab.get("autores", "").split(",") if a.strip()}
    gates, datas = [], []
    for gid, nome, dono in GATES:
        pref = PREFIXO.get(gid, gid + "-")
        itens = []
        for n in sorted(arquivos):
            if not n.startswith(pref):
                continue
            h = cabecalho(arquivos[n])
            erros = valida(h, gid, data_hash, autores)
            m = RE_OBJ.match((h.get("objeto") or "").replace("*", "").replace("`", ""))
            itens.append({"arquivo": n, "papel": h.get("papel", ""), "veredito": h.get("veredito", ""),
                          "por": h.get("por", ""), "data": h.get("data", ""), "objeto": h.get("objeto", ""),
                          "hash": m.group(2) if m else "", "numeros": h.get("numeros", ""),
                          "transcrito_por": h.get("transcrito_por", ""), "erros": erros})
            if data(h.get("data")):
                datas.append(data(h["data"]))
        validos = [i for i in itens if not i["erros"]]
        est, det, falta = "falta", "sem entregável", []
        if gid == "G0" and tipo and tipo != "bug":
            est, det = "na", "não é bug"
        elif gid == "abertura":
            if ab_nome and not valida(hab, "abertura", data_hash, set()):
                est, det = "ok", f"{tipo}, aberto por {hab.get('aberto_por')}"
            else:
                falta = ["00-chamado.md com tipo, aberto_por, data e origem"]
        elif gid == "GD":
            if validos:
                c = cabecalho(arquivos[validos[-1]["arquivo"]])
                if c.get("classe") == "C" and not (c.get("adr") and c.get("decisao_gilsiley")):
                    est, det, falta = "run", "classe C sem ADR ou decisão", ["ADR e decisão do Gilsiley"]
                else:
                    est, det = "ok", f"classe {c.get('classe')}, decidido por {c.get('por')}"
            else:
                falta = ["GD-risco.md com classe, reversibilidade e impacto"]
        elif gid == "G1":
            minimo = 1 if hab.get("escopo") == "correcao" else 2
            ap = {}
            for i in validos:
                if i["veredito"] == "APPROVE":
                    ap.setdefault(i["hash"], set()).add(i["por"])
            ok = [k for k, v in ap.items() if len(v) >= minimo]
            if not tem_spec:
                det, falta = "sem spec.md", ["spec.md em EARS"]
            elif ok:
                est, det = "ok", f"{minimo} APPROVE na spec @ {ok[-1]}"
            else:
                est = "run"
                det = "spec sem crítica" if not validos else f"menos de {minimo} APPROVE no mesmo hash"
                falta = [f"{minimo} APPROVE de spec ({'correção' if minimo == 1 else 'feature'}), de quem não é autor"]
        elif gid == "G2":
            vs = [i["veredito"] for i in validos]
            if "FALHA_ESPERADA" in vs:
                est, det = "ok", "vermelho provado no hash base"
            elif itens:
                est = "bad" if "INVALIDO" in vs else "run"
                det = ", ".join(f"{i['hash'] or i['arquivo']}: {i['veredito']}" for i in itens)
                falta = ["teste falhando no hash base, com a saída colada (FALHA_ESPERADA)"]
            else:
                falta = ["G2-vermelho-<hash>.md"]
        elif gid == "G3":
            por_hash = {}
            for i in validos:
                por_hash.setdefault(i["hash"], []).append(i)
            if por_hash:
                ult = max(por_hash, key=lambda k: max(data(i["data"]) for i in por_hash[k]))
                its = por_hash[ult]
                papeis = {}
                for i in sorted(its, key=lambda i: data(i["data"])):
                    papeis[i["papel"]] = i["veredito"]
                ruim = [i for i in its if i["veredito"] in ("REPROVE", "RETURN", "FALHA")]
                if papeis.get("codigo") != "APPROVE":
                    falta.append(f"APPROVE de código @ {ult}")
                if papeis.get("criterio") != "APPROVE":
                    falta.append(f"APPROVE de critério @ {ult}")
                if papeis.get("runner2") != "OK":
                    falta.append(f"runner2 0/0 por não autor @ {ult}")
                est = "bad" if ruim else ("ok" if not falta else "run")
                det = f"@ {ult}: " + ", ".join(f"{i['papel']} {i['por']} {i['veredito']}" for i in its)
            else:
                falta = ["crítica de código, crítica de critério e runner2 no mesmo hash"]
                if itens:
                    est, det = "bad", "só há vereditos que não contam"
        else:
            if validos:
                v = validos[-1]["veredito"]
                est = "ok" if v in PASSA[gid] else "bad" if v in BARRA[gid] else "run"
                det = f"{validos[-1]['arquivo']}: {v}"
        gates.append({"gate": gid, "nome": nome, "dono": dono, "estado": est, "detalhe": det, "falta": falta,
                      "itens": itens, "desvios": sum(1 for i in itens if i["erros"])})
    atual = next((g for g in gates if g["estado"] not in ("ok", "na")), None)
    desde = max(datas) if datas else data(hab.get("data"))
    return {"titulo": titulo(ab_txt), "tipo": tipo, "escopo": hab.get("escopo", ""), "severidade": hab.get("severidade", ""),
            "aberto_por": hab.get("aberto_por", ""), "aberto_em": hab.get("data", ""), "origem": hab.get("origem", ""),
            "autores": sorted(autores), "gates": gates, "onde": atual["gate"] if atual else "entregue",
            "estado_atual": atual["estado"] if atual else "ok", "com_quem": atual["dono"] if atual else "",
            "falta": atual["falta"] if atual else [], "desde": desde.isoformat() if desde else "",
            "desvios": sum(g["desvios"] for g in gates)}


def le_chamados(cfg: dict) -> dict:
    """Varre cfg['chamados'] = [{repo, pasta, dias}] e devolve os chamados no padrão.

    Vale, para cada pasta specs/<id>/ com 00-chamado.md, o último commit (em qualquer
    branch) que a tocou nos últimos `dias` dias: é a versão mais recente do chamado.
    """
    raiz = cfg.get("raiz", ".")
    vistos = {}
    for fonte in cfg.get("chamados", []):
        repo = os.path.join(raiz, fonte["repo"])
        pasta = fonte.get("pasta", "specs").strip("/")
        saida = _git(repo, "log", "--all", f"--since={fonte.get('dias', 14)}.days", "--format=@%H %cI",
                     "--name-only", "--", f"{pasta}/*/00-chamado.md", f"{pasta}/*/G*.md", f"{pasta}/*/spec.md") or ""
        ultimo = {}
        commit = quando = None
        for linha in saida.splitlines():
            if linha.startswith("@"):
                commit, quando = linha[1:].split(" ", 1)
            elif linha.strip() and commit:
                partes = linha.strip().split("/")
                if len(partes) == 3 and partes[1] not in ultimo:
                    ultimo[partes[1]] = (commit, quando)
        for cid, (commit, quando) in ultimo.items():
            lista = _git(repo, "ls-tree", "--name-only", commit, "--", f"{pasta}/{cid}/") or ""
            nomes = [p.split("/")[-1] for p in lista.splitlines()]
            if not any(n.startswith("00-chamado") for n in nomes):
                continue
            arquivos = {n: _git(repo, "show", f"{commit}:{pasta}/{cid}/{n}") or "" for n in nomes
                        if n.endswith(".md") and (n.startswith(("00-", "G")) or n == "spec.md")}
            cache = {}

            def data_hash(h, repo=repo, cache=cache):
                if h not in cache:
                    ai = _git(repo, "log", "-1", "--format=%ai", h)
                    cache[h] = dt.datetime.strptime(ai.strip(), "%Y-%m-%d %H:%M:%S %z") if ai else None
                return cache[h]
            r = confere(arquivos, data_hash, "spec.md" in nomes)
            r.update({"id": cid, "fonte": f"{fonte['repo']} @ {commit[:7]}", "commit": commit[:7], "commit_em": quando,
                      "registro": "padrão"})
            vistos[cid] = r
    manual = []
    arq = cfg.get("chamados_manuais")
    if arq:
        caminho = os.path.join(raiz, arq) if not os.path.isabs(arq) else arq
        if os.path.exists(caminho):
            with open(caminho, encoding="utf-8") as f:
                manual = json.load(f).get("chamados", [])
            for m in manual:
                m["registro"] = "manual"
    out = list(vistos.values())
    ids = {c["id"] for c in out}
    out += [m for m in manual if m["id"] not in ids]
    return {"gates": [{"gate": g, "nome": n, "dono": d} for g, n, d in GATES], "chamados": out,
            "gerado_em": dt.datetime.now().astimezone().isoformat(timespec="seconds")}


# ---------- cache: o git desta máquina é lento (20 s por varredura); a tela lê o último resultado ----------
import threading
import time

_cache = {"dados": None, "t": 0.0, "rodando": False, "erro": ""}
_trava = threading.Lock()


def _atualiza(cfg):
    try:
        dados = le_chamados(cfg)
        with _trava:
            _cache.update(dados=dados, t=time.time(), erro="")
    except Exception as e:  # a tela mostra o erro; não derruba o servidor
        with _trava:
            _cache["erro"] = str(e)
    finally:
        with _trava:
            _cache["rodando"] = False


def em_cache(cfg, idade_max=120, forcar=False):
    with _trava:
        velho = forcar or time.time() - _cache["t"] > idade_max
        if velho and not _cache["rodando"]:
            _cache["rodando"] = True
            threading.Thread(target=_atualiza, args=(cfg,), daemon=True).start()
        dados = _cache["dados"]
        return {"pronto": dados is not None, "atualizando": _cache["rodando"], "erro": _cache["erro"],
                **(dados or {"gates": [{"gate": g, "nome": n, "dono": d} for g, n, d in GATES], "chamados": []})}
