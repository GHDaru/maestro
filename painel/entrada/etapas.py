"""Mapa gate → etapa do cliente e modelos de texto (FR-008).

O cliente vê 6 etapas, nunca gates internos. As exceções cobrem recuo
e pontos em que o cliente precisa agir.

Spec: specs/068-chamados-whatsapp/spec.md (P2, FR-008).
"""
from __future__ import annotations

import re

# Gate interno → etapa do cliente (FR-008).
# "entregue" cobre G9 PASSOU (Publicado).
GATE_PARA_ETAPA: dict[str, str] = {
    "abertura": "recebido",
    "G0": "recebido",
    "GD": "em_analise",
    "G1": "em_analise",
    "G2": "em_desenvolvimento",
    "G3": "em_desenvolvimento",
    "G4": "em_testes",
    "G5": "em_testes",
    "G6": "em_testes",
    "G7": "suas_validacao",
    "G8": "publicado",
    "G9": "publicado",
}

# Ordem das etapas (para detectar recuo).
ETAPAS_ORDADAS = [
    "recebido",
    "em_analise",
    "em_desenvolvimento",
    "em_testes",
    "suas_validacao",
    "publicado",
]
_ETAPA_IDX = {e: i for i, e in enumerate(ETAPAS_ORDADAS)}

# Número da etapa (1 de 6, 2 de 6, ...).
ETAPA_NUMERO = {e: i + 1 for i, e in enumerate(ETAPAS_ORDADAS)}

# Textos das 6 etapas. #NNN é substituído pelo número do chamado.
# Nenhum texto contém hash, W01-W13, runner2, VM, barra, APPROVE, REPROVE ou caminho.
TEXTOS: dict[str, str] = {
    "recebido": "Recebemos seu chamado #{nnn}. Etapa 1 de 6: Recebido. Avisaremos a cada passo.",
    "em_analise": "Chamado #{nnn} · Etapa 2 de 6: Em análise.",
    "em_desenvolvimento": "Chamado #{nnn} · Etapa 3 de 6: Em desenvolvimento.",
    "em_testes": "Chamado #{nnn} · Etapa 4 de 6: Em testes.",
    "suas_validacao": "Chamado #{nnn} · Etapa 5 de 6: Sua validação. Pronto para você conferir.",
    "publicado": "Chamado #{nnn} · Etapa 6 de 6: Publicado em produção.",
}

# Textos das 3 exceções.
TEXTOS_EXCECAO: dict[str, str] = {
    "aguardando_informacao": "Chamado #{nnn}: Aguardando informação sua para continuar.",
    "nao_aprovado": "Chamado #{nnn}: Não aprovado. {motivo}",
    "recuo": "Chamado #{nnn}: Voltou para ajuste. {mensagem}",
}

# Texto padrão do recuo quando não há `mensagem_cliente:` no gate.
RECUO_PADRAO = "A correção voltou para ajuste e será retomada."


def etapa(gate: str) -> str:
    """Devolve a etapa do cliente para um gate interno."""
    return GATE_PARA_ETAPA.get(gate, "recebido")


def numero(etapa_id: str) -> int:
    """Devolve o número da etapa (1-6)."""
    return ETAPA_NUMERO.get(etapa_id, 1)


def texto(etapa_id: str, nnn: str, **kwargs) -> str:
    """Monta a mensagem para uma etapa.

    Substitui {nnn} e quaisquer kwargs extras (ex: motivo, mensagem).
    """
    tpl = TEXTOS.get(etapa_id, "")
    if not tpl:
        tpl = TEXTOS_EXCECAO.get(etapa_id, "")
    return tpl.format(nnn=nnn, **kwargs)


def recuo(etapa_anterior: str, etapa_atual: str) -> bool:
    """True se a etapa recuou (ex: em_testes → em_desenvolvimento)."""
    ia = _ETAPA_IDX.get(etapa_atual, 0)
    ib = _ETAPA_IDX.get(etapa_anterior, 0)
    return ia < ib


# Padrões proibidos no texto de saída (P2-AC2).
_PADROES_PROIBIDOS = [
    re.compile(r"\b[0-9a-f]{7,40}\b"),  # hash de commit
    re.compile(r"\bW\d{2}\b"),  # W01-W13
    re.compile(r"runner2", re.I),
    re.compile(r"\bVM\b"),
    re.compile(r"barra", re.I),
    re.compile(r"APPROVE", re.I),
    re.compile(r"REPROVE", re.I),
    re.compile(r"/[\w./-]+"),  # caminho de arquivo
]


def texto_e_seguro(msg: str) -> bool:
    """True se a mensagem não contém padrões proibidos (P2-AC2)."""
    for pat in _PADROES_PROIBIDOS:
        if pat.search(msg):
            return False
    return True
