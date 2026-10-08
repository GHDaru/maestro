"""Orquestrador do ciclo de notificação ao cliente (P2).

Um ciclo: lê os chamados via `le_chamados()`, calcula a etapa atual
via `etapas.etapa()`, compara com a última notificação em `entrada.db`,
enfileira mensagens novas (incluindo recuo) via `saida.enfileirar()`.

Roda a cada 5 min pelo Agendador do Windows (T2-04).
"""
from __future__ import annotations

import json
import os
import sqlite3
from typing import Any

from . import etapas
from . import saida

# Tabela de estado: última etapa notificada por chamado.
_SCHEMA = """
CREATE TABLE IF NOT EXISTS notificado (
    chamado TEXT PRIMARY KEY,
    etapa TEXT NOT NULL,
    gate TEXT NOT NULL,
    atualizado_em TEXT NOT NULL
);
"""


def _db(dados_dir: str) -> sqlite3.Connection:
    conn = sqlite3.connect(os.path.join(dados_dir, "entrada.db"))
    conn.executescript(_SCHEMA)
    return conn


def _agora_iso() -> str:
    import datetime as dt
    return dt.datetime.now(dt.timezone.utc).isoformat()


def _ultima_etapa(dados_dir: str, chamado: str) -> str | None:
    conn = _db(dados_dir)
    try:
        row = conn.execute("SELECT etapa FROM notificado WHERE chamado = ?", (chamado,)).fetchone()
        return row[0] if row else None
    finally:
        conn.close()


def _registrar(dados_dir: str, chamado: str, etapa_id: str, gate: str) -> None:
    conn = _db(dados_dir)
    try:
        conn.execute(
            "INSERT INTO notificado (chamado, etapa, gate, atualizado_em) VALUES (?, ?, ?, ?) "
            "ON CONFLICT(chamado) DO UPDATE SET etapa = excluded.etapa, gate = excluded.gate, "
            "atualizado_em = excluded.atualizado_em",
            (chamado, etapa_id, gate, _agora_iso()),
        )
        conn.commit()
    finally:
        conn.close()


def _contato_do_chamado(chamado: dict[str, Any]) -> str:
    """Extrai o contato de teste do chamado. Dado sintético (P2-AC1)."""
    # O contato vem do campo `contato` no chamado, se houver.
    # Em P2, é sempre um número de teste (NFR-002).
    return chamado.get("contato", "")


def _nnn_do_chamado(chamado: dict[str, Any]) -> str:
    """Extrai o número do chamado para exibição ao cliente."""
    return str(chamado.get("numero", chamado.get("chamado", "?")))


def ciclo(dados_dir: str, chamados: list[dict[str, Any]]) -> dict[str, list[int]]:
    """Executa um ciclo do orquestrador.

    Args:
        dados_dir: diretório com entrada.db.
        chamados: lista de chamados (saída de `le_chamados()`).

    Returns:
        dict com "enfileirados" (lista de ids) e "recuos" (lista de ids).
    """
    enfileirados: list[int] = []
    recuos: list[int] = []

    for ch in chamados:
        gate_atual = ch.get("onde", "")
        if not gate_atual:
            continue

        etapa_atual = etapas.etapa(gate_atual)
        etapa_prev = _ultima_etapa(dados_dir, ch.get("chamado", ""))
        nnn = _nnn_do_chamado(ch)
        contato = _contato_do_chamado(ch)

        if not contato:
            # Sem contato de teste, não há para quem enviar.
            _registrar(dados_dir, ch.get("chamado", ""), etapa_atual, gate_atual)
            continue

        if etapa_prev is None:
            # Primeira notificação: etapa atual.
            msg = etapas.texto(etapa_atual, nnn)
            if etapas.texto_e_seguro(msg):
                mid = saida.enfileirar(dados_dir, ch.get("chamado", ""), contato, msg, etapa_atual)
                enfileirados.append(mid)
        elif etapa_prev != etapa_atual:
            if etapas.recuo(etapa_prev, etapa_atual):
                # Recuo: mensagem de exceção.
                mensagem_cliente = ch.get("mensagem_cliente", etapas.RECUO_PADRAO)
                msg = etapas.texto("recuo", nnn, mensagem=mensagem_cliente)
                if etapas.texto_e_seguro(msg):
                    mid = saida.enfileirar(dados_dir, ch.get("chamado", ""), contato, msg, "recuo")
                    recuos.append(mid)
            else:
                # Avanço de etapa: notifica a etapa atual.
                msg = etapas.texto(etapa_atual, nnn)
                if etapas.texto_e_seguro(msg):
                    mid = saida.enfileirar(dados_dir, ch.get("chamado", ""), contato, msg, etapa_atual)
                    enfileirados.append(mid)

        _registrar(dados_dir, ch.get("chamado", ""), etapa_atual, gate_atual)

    return {"enfileirados": enfileirados, "recuos": recuos}


def despachar(dados_dir: str, webhook_url: str, segredo: str) -> dict[str, int]:
    """Tenta enviar todas as mensagens pendentes. Devolve contagem."""
    msgs = saida.pendentes(dados_dir)
    enviados = 0
    falharam = 0
    for msg in msgs:
        if saida.enviar(dados_dir, msg, webhook_url, segredo):
            enviados += 1
        else:
            falharam += 1
    return {"enviados": enviados, "falharam": falharam}


def executar(dados_dir: str, cfg: dict[str, Any], webhook_url: str | None = None, segredo: str | None = None) -> dict[str, Any]:
    """Ciclo completo: notifica + despacha (se webhook configurado).

    Args:
        dados_dir: diretório com entrada.db.
        cfg: config para `le_chamados()`.
        webhook_url: URL do n8n (None = não despacha).
        segredo: segredo HMAC (None = não despacha).

    Returns:
        dict com resultado do ciclo e do despacho.
    """
    from ..chamados import le_chamados

    chamados = le_chamados(cfg)
    res_ciclo = ciclo(dados_dir, chamados)

    res_despacho = {"enviados": 0, "falharam": 0}
    if webhook_url and segredo:
        res_despacho = despachar(dados_dir, webhook_url, segredo)

    return {"ciclo": res_ciclo, "despacho": res_despacho}


if __name__ == "__main__":
    import sys

    dados_dir = os.environ.get("MAESTRO_DADOS_DIR", ".")
    webhook_url = os.environ.get("MAESTRO_WEBHOOK_URL")
    segredo = os.environ.get("MAESTRO_HMAC_SEGREDO")
    cfg_json = os.environ.get("MAESTRO_CFG_JSON", "{}")
    cfg = json.loads(cfg_json) if cfg_json else {}

    resultado = executar(dados_dir, cfg, webhook_url, segredo)
    print(json.dumps(resultado, indent=2))
    sys.exit(0)
