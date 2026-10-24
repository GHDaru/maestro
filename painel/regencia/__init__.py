"""`regencia` — o pacote **puro** das regras do painel de regência (ciclo 072, rodada 1).

Corte hexagonal (plano 072, §1): as regras de domínio moram aqui e **não** importam
`http.server`, `sqlite3` nem `chamados`, e **não** abrem arquivo. Os adaptadores
(`painel/server.py` HTTP, `painel/fila_registro.py` JSONL) consomem estas funções.

Este `__init__` **reexporta todos os nomes públicos**: os testes resolvem as funções **pelo
pacote** (`import regencia`), nunca pelo submódulo — reexportar de menos é teste vermelho.
"""
from __future__ import annotations

from .fila import (
    PORTOES_DO_REGENTE,
    cabecalho_fila,
    ordena_fila,
    portao_derivado,
    portoes_do_regente,
    sai_da_fila,
    valida_pedido,
    valida_ruling,
)
from .kanban import (
    COLUNAS,
    cartao,
    coluna_do_cartao,
    faixa_abertura_gd,
    idade_do_carimbo,
    independencia,
    proposta_transicao,
)
from .normalizacao import (
    SELO_DECLARADA,
    SELO_REGISTRO,
    SELO_RELOGIO,
    aviso_ingestao,
    normaliza,
    parse_instante,
    sem_fonte,
)

__all__ = [
    # normalizacao
    "normaliza", "sem_fonte", "aviso_ingestao", "parse_instante",
    "SELO_REGISTRO", "SELO_RELOGIO", "SELO_DECLARADA",
    # kanban
    "coluna_do_cartao", "independencia", "idade_do_carimbo", "cartao",
    "proposta_transicao", "faixa_abertura_gd", "COLUNAS",
    # fila
    "valida_pedido", "valida_ruling", "sai_da_fila", "ordena_fila", "cabecalho_fila",
    "portao_derivado", "portoes_do_regente", "PORTOES_DO_REGENTE",
]
