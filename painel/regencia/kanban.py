"""Projeção do kanban por gate sobre o que o 068 já calculou (regras **puras**).

Corte hexagonal do plano 072 (§1): este módulo não importa `http.server`, `sqlite3` nem
`chamados`, e não abre arquivo. Ele **consome** o resultado de `painel/chamados.confere` (a
lista de gates, cada um com o `estado` já resolvido) — não há segundo conferidor (anti-padrão
22). Quem lê o git é o adaptador; aqui só se projeta.

- FR2 — `coluna_do_cartao(gates)`: o cartão fica no **último gate aprovado** (`estado == "ok"`),
  entre as colunas G0–G9 (abertura e GD não viram coluna — viram faixa).
- FR4 — `independencia(autor_da_peca, por)`: mesma pessoa nas duas pontas → marcador vermelho.
- FR23 — `idade_do_carimbo(carimbo, agora=None, declarado=False)`: `{texto, carimbo, selo}`.
- FR8 — `proposta_transicao(chamado, de, para, arquivos=None)`: pura; recebe os `arquivos` já
  resolvidos pelo adaptador e devolve `{permitido, falta?}` — não levanta.
- FR1 — `faixa_abertura_gd(gates)`: a faixa acima do kanban com abertura e GD.
"""
from __future__ import annotations

import datetime as dt

from .normalizacao import SELO_DECLARADA, SELO_REGISTRO, parse_instante, texto_idade

# As dez colunas do kanban (FR1): G0–G9. Abertura e GD são faixa, não coluna.
COLUNAS = [f"G{i}" for i in range(10)]


def coluna_do_cartao(gates):
    """FR2: o último gate com estado aprovado (`ok`) entre as colunas; ``""`` se não houver."""
    if isinstance(gates, dict):
        gates = gates.get("gates", [])
    aprovados = [g.get("gate") for g in (gates or [])
                 if g.get("gate") in COLUNAS and g.get("estado") == "ok"]
    return aprovados[-1] if aprovados else ""


def independencia(autor_da_peca, por):
    """FR4: `True` (vermelho) quando quem fez a peça também assina o veredito.

    Sem `autor_da_peca` (ou sem `por`) não há verde presumido: devolve `False` — o cartão mostra
    "—" com motivo (FR5), nunca "independente" por omissão.
    """
    a = (autor_da_peca or "").strip()
    p = (por or "").strip()
    if not a or not p:
        return False
    return a == p


def _texto_idade(idade):
    """FR23: "há X h Y min" (ou "há Y min" na primeira hora). O "há" é rótulo; a conta é de
    `normalizacao.texto_idade` — a mesma que o aviso de leitura velha usa (072-T16)."""
    return f"há {texto_idade(idade)}"


def idade_do_carimbo(carimbo, agora=None, declarado=False):
    """FR23: `{texto, carimbo, selo}` — idade do **relógio/registro** (nunca de campo digitado)."""
    t = parse_instante(carimbo)
    if not t:
        return {"texto": "", "carimbo": "", "selo": SELO_DECLARADA if declarado else SELO_REGISTRO}
    if agora is None:
        agora = dt.datetime.now(t.tzinfo) if t.tzinfo else dt.datetime.now()
    if t.tzinfo and not agora.tzinfo:
        agora = agora.replace(tzinfo=t.tzinfo)
    return {"texto": _texto_idade(agora - t),
            "carimbo": t.strftime("%Y-%m-%d %H:%M %z").strip(),
            "selo": SELO_DECLARADA if declarado else SELO_REGISTRO}


def cartao(chamado):
    """FR2: `{chamado, gate, faltas}` — o cartão no último gate aprovado, com o que falta."""
    if isinstance(chamado, dict):
        gates = chamado.get("gates", [])
        cid = chamado.get("id", "")
        faltas = list(chamado.get("falta") or [])
    else:
        gates, cid, faltas = chamado or [], "", []
    return {"chamado": cid, "gate": coluna_do_cartao(gates), "faltas": faltas}


def proposta_transicao(chamado, de, para, arquivos=None):
    """FR8: só permite a transição se o **arquivo do gate de destino** existe e tem cabeçalho válido.

    Pura: recebe `arquivos` já resolvido pelo adaptador (mapa `gate → {"caminho",
    "cabecalho_valido"}`). Devolve `{permitido, falta?}` — **não levanta** (nome fixado; F2 adapta).
    """
    info = (arquivos or {}).get(para) or {}
    if info.get("cabecalho_valido") and (info.get("caminho") or info.get("existe", True)):
        return {"permitido": True, "chamado": chamado, "de": de, "para": para,
                "exige": f"{para}-*.md", "caminho": info.get("caminho", "")}
    return {"permitido": False, "chamado": chamado, "de": de, "para": para,
            "falta": f"falta {para}-*.md com cabeçalho válido"}


def faixa_abertura_gd(gates):
    """FR1: a faixa acima do kanban — `abertura` e `GD`, com estado e motivo (não viram coluna)."""
    faixa = {}
    for g in (gates or []):
        if g.get("gate") in ("abertura", "GD"):
            faixa[g["gate"]] = {"nome": g.get("nome", ""), "estado": g.get("estado", ""),
                                "motivo": g.get("detalhe", ""), "falta": list(g.get("falta") or [])}
    return faixa
