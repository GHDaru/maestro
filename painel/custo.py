"""Custo por sessão em série temporal: índice incremental dos transcripts do Claude Code.

Lê ~/.claude/projects/<pasta do projeto>/*.jsonl a partir de onde parou (offset por
arquivo) e soma o uso de tokens por sessão e por minuto, com o nome da sessão
(custom-title: Worker09 vira W09). A trilha do chamado usa isto para dizer quantos
tokens cada passo custou. Só lê os transcripts; grava só em dados/custo.db.

    python painel/custo.py projetos/exemplo.json      # atualiza o índice
"""
from __future__ import annotations

import glob
import json
import os
import re
import sqlite3
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ESQUEMA = """
CREATE TABLE IF NOT EXISTS arquivos (caminho TEXT PRIMARY KEY, offset INTEGER NOT NULL, sessao TEXT, ultimo_id TEXT);
CREATE TABLE IF NOT EXISTS sessoes (sessao TEXT PRIMARY KEY, titulo TEXT, nome TEXT, pasta TEXT);
CREATE TABLE IF NOT EXISTS uso (sessao TEXT NOT NULL, minuto TEXT NOT NULL, turnos INTEGER, entrada INTEGER, saida INTEGER,
                                cache_lido INTEGER, cache_escrito INTEGER, PRIMARY KEY (sessao, minuto));
"""


def nome_canonico(titulo: str) -> str:
    m = re.match(r"^Worker\s*0*(\d+)$", titulo or "")
    if m:
        return f"W{int(m.group(1)):02d}"
    t = (titulo or "").strip()
    if t.startswith("Hindiana") and "Office" in t:
        return "Hindiana Office"
    if "Assistente" in t:
        return "Assistente"
    return t


def abre(db_path):
    db = sqlite3.connect(db_path, timeout=30)
    db.executescript(ESQUEMA)
    return db


def pastas_do_projeto(cfg) -> list[str]:
    base = os.path.expanduser(os.path.join("~", ".claude", "projects"))
    filtros = cfg.get("custo_pastas", ["180-HINDIANA"])
    return [p for p in glob.glob(os.path.join(base, "*")) if any(f in os.path.basename(p) for f in filtros)]


def indexa(cfg, db_path=None) -> dict:
    db = abre(db_path or os.path.join(AQUI, "dados", "custo.db"))
    lidos = novos = 0
    for pasta in pastas_do_projeto(cfg):
        for f in glob.glob(os.path.join(pasta, "*.jsonl")):
            row = db.execute("SELECT offset, ultimo_id FROM arquivos WHERE caminho=?", (f,)).fetchone()
            offset, ultimo = (row or (0, ""))
            tam = os.path.getsize(f)
            if tam <= offset:
                continue
            sessao = os.path.splitext(os.path.basename(f))[0]
            titulo = None
            soma = {}
            consumido = 0
            with open(f, "rb") as fh:
                fh.seek(offset)
                resto = b""
                while True:
                    pedaco = fh.read(32 << 20)
                    if not pedaco:
                        break
                    bloco = resto + pedaco
                    corte = bloco.rfind(b"\n")
                    if corte < 0:
                        resto = bloco
                        continue
                    resto = bloco[corte + 1:]
                    consumido += corte + 1
                    for ln in bloco[:corte].split(b"\n"):
                        if b'"custom-title"' not in ln and b'"usage"' not in ln:
                            continue
                        try:
                            e = json.loads(ln)
                        except ValueError:
                            continue
                        if e.get("type") == "custom-title" and e.get("customTitle"):
                            titulo = e["customTitle"]
                            continue
                        m = e.get("message") or {}
                        u = m.get("usage")
                        if e.get("type") != "assistant" or not u or not e.get("timestamp"):
                            continue
                        mid = m.get("id") or e.get("uuid")
                        if mid == ultimo:  # streamed chunks repeat the same message id
                            continue
                        ultimo = mid
                        k = e["timestamp"][:16]
                        a = soma.setdefault(k, [0, 0, 0, 0, 0])
                        a[0] += 1
                        a[1] += int(u.get("input_tokens") or 0)
                        a[2] += int(u.get("output_tokens") or 0)
                        a[3] += int(u.get("cache_read_input_tokens") or 0)
                        a[4] += int(u.get("cache_creation_input_tokens") or 0)
                        novos += 1
            if not consumido:
                continue
            for k, a in soma.items():
                db.execute("""INSERT INTO uso VALUES (?,?,?,?,?,?,?) ON CONFLICT(sessao, minuto) DO UPDATE SET
                              turnos=turnos+excluded.turnos, entrada=entrada+excluded.entrada, saida=saida+excluded.saida,
                              cache_lido=cache_lido+excluded.cache_lido, cache_escrito=cache_escrito+excluded.cache_escrito""",
                           (sessao, k, *a))
            if titulo:
                db.execute("INSERT INTO sessoes VALUES (?,?,?,?) ON CONFLICT(sessao) DO UPDATE SET titulo=excluded.titulo, nome=excluded.nome",
                           (sessao, titulo, nome_canonico(titulo), os.path.basename(pasta)))
            db.execute("INSERT INTO arquivos VALUES (?,?,?,?) ON CONFLICT(caminho) DO UPDATE SET offset=excluded.offset, ultimo_id=excluded.ultimo_id",
                       (f, offset + consumido, sessao, ultimo))
            db.commit()
            lidos += 1
    db.close()
    return {"arquivos_lidos": lidos, "mensagens_novas": novos}


def janela(db_path, nome: str, ini_utc: str, fim_utc: str) -> dict:
    """Tokens da sessão `nome` entre dois instantes UTC ('YYYY-MM-DDTHH:MM')."""
    if not os.path.exists(db_path):
        return {}
    db = sqlite3.connect(db_path, timeout=30)
    try:
        r = db.execute("""SELECT COALESCE(SUM(turnos),0), COALESCE(SUM(entrada),0), COALESCE(SUM(saida),0),
                                 COALESCE(SUM(cache_lido),0), COALESCE(SUM(cache_escrito),0)
                          FROM uso JOIN sessoes USING (sessao) WHERE sessoes.nome=? AND minuto>? AND minuto<=?""",
                       (nome, ini_utc, fim_utc)).fetchone()
    finally:
        db.close()
    return dict(zip(("turnos", "entrada", "saida", "cache_lido", "cache_escrito"), r))


if __name__ == "__main__":
    sys.path.insert(0, AQUI)
    import ingest
    cfg = ingest.carrega_cfg(sys.argv[1])
    print(json.dumps(indexa(cfg, sys.argv[2] if len(sys.argv) > 2 else None), ensure_ascii=False))
