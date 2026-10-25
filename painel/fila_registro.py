"""Adaptador de escrita do registro da fila de decisões (ciclo 072, FR16).

Corte hexagonal (plano 072, §1): as regras **puras** da fila vivem em `painel/regencia/`; este
módulo é a **borda** — é o único que abre o arquivo. Duas invariantes de borda moram aqui
(plano §"Invariantes"): o acréscimo **só cresce** o arquivo (FR16) e o **backup datado** do dia
(ADR 0027 §4).

- FR16 — `acrescenta(caminho, linha)`: `open(..., "a", encoding="utf-8")`, uma linha JSON por
  chamada (`json.dumps(..., ensure_ascii=False)` + `\\n`), **nunca** `"w"`/`truncate`/`seek`.
- FR16 — `le(caminho)`: leitura tolerante — linha inválida é ignorada com aviso, sem derrubar
  a fila; o leitor não escreve.
- ADR 0027 §4 — `backup_datado(caminho, agora)`: cópia do dia (`shutil.copy2`) para a pasta
  `backup/` ao lado do registro, antes da primeira escrita de cada dia.

Escritor único no processo: `acrescenta` e `backup_datado` correm sob um `threading.Lock` de
módulo, de modo que o `POST` **não grava antes de o backup do dia existir** (ADR 0027 §4).
"""
from __future__ import annotations

import datetime as dt
import json
import os
import shutil
import sys
import threading

AQUI = os.path.dirname(os.path.abspath(__file__))
_LOCK = threading.Lock()


def caminho(cfg):
    """O endereço do registro: `cfg["fila_decisoes"]` ou o padrão do painel (plano 072, §2).

    Padrão `painel/dados/fila-<projeto>.jsonl`, ao lado do `<projeto>.db` que o servidor já cria
    ali (`painel/server.py`) — `painel/dados/` é o **próprio dado do painel** (anti-regra 7 /
    FR16; ADR 0027 §1).
    """
    cfg = cfg or {}
    if cfg.get("fila_decisoes"):
        return cfg["fila_decisoes"]
    projeto = cfg.get("projeto") or "painel"
    return os.path.join(AQUI, "dados", f"fila-{projeto}.jsonl")


def _caminho_do_backup(registro, agora):
    """`<pasta do registro>/backup/<nome-sem-`.jsonl`>-<AAAA-MM-DD>.jsonl` (ADR 0027 §4)."""
    base = os.path.basename(registro)
    raiz, ext = os.path.splitext(base)
    pasta = os.path.join(os.path.dirname(os.path.abspath(registro)), "backup")
    return os.path.join(pasta, f"{raiz}-{agora.strftime('%Y-%m-%d')}{ext or '.jsonl'}")


def _backup_do_dia(registro, agora=None):
    """Cópia do dia criada só na primeira vez; devolve o caminho do backup, ou None.

    Sem o arquivo de origem não há o que copiar (primeira escrita da vida do registro) → None, e
    a escrita segue: o backup **mitiga** a perda, não a impede (ADR 0027 §4).
    """
    agora = agora or dt.datetime.now().astimezone()
    if not os.path.exists(registro):
        return None
    destino = _caminho_do_backup(registro, agora)
    if os.path.exists(destino):
        return None
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    shutil.copy2(registro, destino)
    return destino


def backup_datado(registro, agora=None):
    """Cópia do dia do registro: devolve o caminho do backup criado, ou None — sob o lock."""
    with _LOCK:
        return _backup_do_dia(registro, agora)


def acrescenta(registro, linha):
    """Acrescenta **uma** linha ao registro e devolve o backup do dia, se o criou nesta chamada.

    Sempre em modo de acrescentar: o arquivo só cresce (FR16). O backup do dia é garantido
    **antes** da escrita, dentro do mesmo lock (ADR 0027 §4).
    """
    with _LOCK:
        os.makedirs(os.path.dirname(os.path.abspath(registro)), exist_ok=True)
        backup = _backup_do_dia(registro)
        with open(registro, "a", encoding="utf-8") as f:
            f.write(json.dumps(linha, ensure_ascii=False) + "\n")
        return backup


def le(registro):
    """Lê o registro em ordem: lista de objetos; linha inválida é ignorada com aviso (FR16)."""
    if not os.path.exists(registro):
        return []
    out = []
    with open(registro, encoding="utf-8") as f:
        for n, linha in enumerate(f, 1):
            linha = linha.strip()
            if not linha:
                continue
            try:
                out.append(json.loads(linha))
            except ValueError:
                print(f"aviso: linha {n} inválida no registro {registro} (ignorada)", file=sys.stderr)
    return out
