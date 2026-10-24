"""Regras **puras** da fila de decisões: validação, permanência, ordem e portões derivados.

Corte hexagonal do plano 072 (§1): este módulo não importa `http.server`, `sqlite3` nem
`chamados`, e não abre arquivo. Os parâmetros que vêm da configuração (`pessoas`, `pedidos`)
chegam **já resolvidos** pelo adaptador HTTP — a função pura não lê `projetos/<nome>.json`.

- FR11 — `valida_pedido(pedido)`: anatomia obrigatória do pedido de decisão.
- FR14/FR20 — `valida_ruling(ruling, pessoas=None, pedidos=None)`: sem autor humano ou sem
  destino → recusado; autor fora de `pessoas` e pedido fora de `pedidos` → recusado.
- FR12 — `sai_da_fila(pedido, rulings)`: só um ruling com o pedido fecha o pedido.
- FR15 — `ordena_fila(itens, agora=None)`: prazo × bloqueio (nº de destravados).
- FR23 — `cabecalho_fila(itens, agora=None)`: `{n, idade_mais_velha}`.
- FR20 — `portao_derivado(...)` / `portoes_do_regente(...)`: G7/G8 pendentes viram itens da fila.
"""
from __future__ import annotations

import datetime as dt

from .kanban import idade_do_carimbo
from .normalizacao import parse_instante

# Campos obrigatórios do pedido de decisão (FR11) — só os de texto simples; `opcoes` e `destrava`
# têm checagem própria (lista com descrição / lista não vazia).
_CAMPOS_TEXTO = ("id", "pedido_por", "pergunta", "recomendacao", "prazo", "destino", "status")

# Portões que só o humano registra (FR20): viram item da fila, somente leitura para um agente.
PORTOES_DO_REGENTE = ("G7", "G8")


def valida_pedido(pedido):
    """FR11: devolve o motivo da recusa (str) ou `None` se o pedido tem a anatomia completa."""
    if not isinstance(pedido, dict):
        return "pedido não é um objeto"
    for campo in _CAMPOS_TEXTO:
        if not isinstance(pedido.get(campo), str) or not pedido.get(campo).strip():
            return f"falta '{campo}' no pedido"
    opcoes = pedido.get("opcoes")
    if not isinstance(opcoes, list) or not opcoes:
        return "pedido sem nenhuma opcao"
    for op in opcoes:
        if not isinstance(op, dict) or not op.get("id") or not (op.get("descricao") or "").strip():
            return "opcao sem id ou descricao"
    destrava = pedido.get("destrava")
    if not isinstance(destrava, list) or not destrava:
        return "pedido sem o que destrava"
    return None


def valida_ruling(ruling, pessoas=None, pedidos=None):
    """FR14/FR20: devolve o motivo da recusa (str) ou `None` quando o ruling é aceito.

    `pessoas` = a lista `cfg["regencia"]["pessoas"]` (autor fora dela → recusado, **mesmo com
    `registrado_por`**); `pedidos` = os ids conhecidos (ruling para pedido inexistente →
    recusado). Ambos opcionais para o teste puro de 1 arg.
    """
    if not isinstance(ruling, dict):
        return "ruling não é um objeto"
    autor = (ruling.get("autor") or "").strip()
    destino = (ruling.get("destinatario") or ruling.get("destino") or "").strip()
    if not autor:
        return "ruling sem autor humano"
    if not destino:
        return "ruling sem destino (destinatario)"
    if pessoas is not None and autor not in pessoas:
        return f"autor não é pessoa do projeto: '{autor}'"
    if pedidos is not None and ruling.get("pedido") not in pedidos:
        return f"pedido desconhecido: '{ruling.get('pedido')}'"
    return None


def sai_da_fila(pedido, rulings):
    """FR12: `True` quando existe um ruling que fecha este pedido — só então ele sai da fila."""
    pid = pedido.get("id") if isinstance(pedido, dict) else str(pedido)
    return any((r or {}).get("pedido") == pid for r in (rulings or []))


def _n_destravados(item):
    destrava = item.get("destrava")
    if isinstance(destrava, list):
        return len(destrava)
    return 1 if destrava else 0


def ordena_fila(itens, agora=None):
    """FR15: prazo mais próximo primeiro; empate pelo **nº de itens destravados** (maior primeiro)."""
    limite = dt.datetime.max.replace(tzinfo=dt.timezone.utc)

    def chave(item):
        quando = parse_instante(item.get("prazo")) or limite
        if quando.tzinfo is None:
            quando = quando.replace(tzinfo=dt.timezone.utc)
        return (quando, -_n_destravados(item), str(item.get("id", "")))

    return sorted(itens or [], key=chave)


def _quando_do_item(item):
    """FR23: o instante do item sai do registro/relógio, nunca de campo digitado."""
    for chave in ("criado_em", "registrado_em", "desde", "carimbo", "entrada_em", "data"):
        t = parse_instante(item.get(chave) if isinstance(item, dict) else None)
        if t:
            return t
    return None


def cabecalho_fila(itens, agora=None):
    """FR23: `{n, idade_mais_velha}` — o contador do cabeçalho da fila."""
    itens = itens or []
    instantes = [t for t in (_quando_do_item(i) for i in itens) if t]
    mais_velha = None
    if instantes:
        mais = min(instantes)
        mais_velha = idade_do_carimbo(mais.isoformat(), agora)
    return {"n": len(itens), "idade_mais_velha": mais_velha}


def portao_derivado(chamado, gate, status, commit):
    """FR20: item **derivado** (não gravado) de um portão do regente pendente.

    `id = f"{chamado}+{gate}"` (ex.: `072+T7`) — o ruling aceita esse id.
    """
    return {"id": f"{chamado}+{gate}", "chamado": chamado, "gate": gate, "status": status or "pendente",
            "desde": commit or "", "evidencia": f"specs/{chamado}/{gate}-*.md",
            "somente_leitura": True, "origem": "portao_do_regente"}


def _arquivo_do_gate(gate):
    itens = gate.get("itens") or []
    return itens[-1].get("arquivo", "") if itens else ""


def portoes_do_regente(chamado, commit_de=None):
    """FR20: monta a lista de itens derivados dos portões do regente **pendentes** (G7/G8).

    Pura: usa o `estado` que o 068 já calculou e o `commit_de` (arquivo → quando) que o
    adaptador resolveu — o "desde quando" vem do commit do arquivo, não de data digitada.
    """
    commit_de = commit_de or {}
    gates = chamado.get("gates", []) if isinstance(chamado, dict) else (chamado or [])
    cid = chamado.get("id", "") if isinstance(chamado, dict) else ""
    itens = []
    for g in gates:
        gate = g.get("gate")
        if gate not in PORTOES_DO_REGENTE:
            continue
        if g.get("estado") in ("ok", "na"):
            continue
        itens_gate = g.get("itens") or []
        status = (itens_gate[-1].get("veredito") if itens_gate else "") or g.get("estado") or "pendente"
        desde = commit_de.get(_arquivo_do_gate(g)) or g.get("desde", "")
        itens.append(portao_derivado(cid, gate, status, desde))
    return itens
