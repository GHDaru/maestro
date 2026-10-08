#!/usr/bin/env python3
"""Validação de segurança da porta de entrada (P5 do chamado 068).

HMAC-SHA256 com compare_digest, janela de horário de 5 min e
lista de IPs permitidos. Suporta dois segredos (NFR-008):
o atual e o anterior, para rotação sem parar a entrada.

Stdlib only (hmac, hashlib, datetime).
"""
from __future__ import annotations

import datetime as dt
import hashlib
import hmac


def calcula_assinatura(corpo: bytes, segredo: str) -> str:
    """Calcula HMAC-SHA256 do corpo e retorna no formato 'sha256=<hex>'."""
    mac = hmac.new(segredo.encode("utf-8"), corpo, hashlib.sha256)
    return f"sha256={mac.hexdigest()}"


def valida_assinatura(corpo: bytes, assinatura_recebida: str, segredos: list[str]) -> tuple[bool, str]:
    """Valida a assinatura contra qualquer um dos segredos (atual + anterior).

    Usa hmac.compare_digest para não vazar timing.
    Retorna (ok, motivo).
    """
    for segredo in segredos:
        esperada = calcula_assinatura(corpo, segredo)
        if hmac.compare_digest(esperada, assinatura_recebida):
            return True, ""
    return False, "Assinatura inválida"


def _qual_segredo_validou(corpo: bytes, assinatura_recebida: str, segredos: list[str]) -> str | None:
    """Retorna 'atual' ou 'anterior' indicando qual segredo validou, sem o valor."""
    for i, segredo in enumerate(segredos):
        esperada = calcula_assinatura(corpo, segredo)
        if hmac.compare_digest(esperada, assinatura_recebida):
            return "atual" if i == 0 else "anterior"
    return None


def valida_horario(
    horario_recebido: dt.datetime,
    agora: dt.datetime | None = None,
    janela_min: int = 5,
) -> tuple[bool, str]:
    """Valida se o horário está dentro da janela de minutos da hora atual.

    Recusa horário no futuro ou mais antigo que a janela.
    Retorna (ok, motivo).
    """
    if agora is None:
        agora = dt.datetime.now().astimezone()
    # Normalizar timezone-aware
    if horario_recebido.tzinfo is None:
        horario_recebido = horario_recebido.astimezone()
    if agora.tzinfo is None:
        agora = agora.astimezone()
    delta = agora - horario_recebido
    # Recusa futuro (mais de 1 min à frente)
    if delta.total_seconds() < -60:
        return False, "Horário no futuro"
    # Recusa mais antigo que a janela
    if delta.total_seconds() > janela_min * 60:
        return False, "Horário fora da janela"
    return True, ""


def valida_ip(ip_recebido: str, ips_permitidos: list[str]) -> tuple[bool, str]:
    """Valida se o IP está na lista de permitidos."""
    if ip_recebido in ips_permitidos:
        return True, ""
    return False, f"IP não permitido: {ip_recebido}"


def verifica(
    corpo: bytes,
    assinatura: str,
    horario: dt.datetime,
    ip: str,
    segredos: list[str],
    ips_permitidos: list[str],
    agora: dt.datetime | None = None,
    janela_min: int = 5,
) -> tuple[bool, str, int | None, str | None]:
    """Verificação combinada: assinatura + horário + IP.

    Retorna (ok, motivo, status_http, qual_segredo).
    - ok=True: tudo válido, status=None, qual_segredo='atual'|'anterior'
    - ok=False: status=401, motivo explica o que falhou, qual_segredo=None
    """
    # IP primeiro (mais barato)
    ok, motivo = valida_ip(ip, ips_permitidos)
    if not ok:
        return False, motivo, 401, None

    # Horário
    ok, motivo = valida_horario(horario, agora=agora, janela_min=janela_min)
    if not ok:
        return False, motivo, 401, None

    # Assinatura
    ok, motivo = valida_assinatura(corpo, assinatura, segredos)
    if not ok:
        return False, motivo, 401, None

    qual = _qual_segredo_validou(corpo, assinatura, segredos)
    return True, "", None, qual
