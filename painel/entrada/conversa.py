"""Maquina de estados da conversa de abertura de chamado (chamado 068, T1-02).

Funcao pura: conversa(estado, mensagem, dados) -> (novo_estado, resposta, acao, novos_dados).

Fluxo bug:
    inicio -> menu -> descricao -> onde -> passos -> esperado_aconteceu
           -> anexos -> confirmacao -> criado

Fluxo melhoria/sugestao:
    inicio -> menu -> descricao -> anexos -> confirmacao -> criado

Cancelar em qualquer passo. Expirar em 30 min.

Stdlib only. Sem IO, sem rede, sem tempo real — pura.
"""

from __future__ import annotations

from typing import Any

ESTADO_INICIO = "inicio"
TEMPO_EXPIRACAO_SEG = 1800  # 30 min

_MENU_TEXTO = "1 Bug, 2 Melhoria, 3 Sugestao"
_CANCELADO_TEXTO = "Chamado cancelado. Se precisar, e so mandar 'oi' de novo."
_EXPIRADO_TEXTO = "Conversa expirada apos 30 min sem resposta. Mande 'oi' para recomecar."

# Passos do fluxo bug (em ordem)
_PASSOS_BUG = ["descricao", "onde", "passos", "esperado_aconteceu"]
# Passos do fluxo melhoria/sugestao
_PASSOS_CURTO = ["descricao"]

# Prompts por estado
_PROMPTS = {
    "descricao": {
        "bug": "O que aconteceu?",
        "melhoria": "O que voce gostaria?",
        "sugestao": "O que voce sugere?",
    },
    "onde": "Onde (tela)?",
    "passos": "Quais os passos para reproduzir?",
    "esperado_aconteceu": "O que voce esperava? O que aconteceu?",
    "anexos": "Mande capturas ou digite 'pular'.",
    "confirmacao": "Confirma o chamado? (sim / nao)",
}


def _menu() -> tuple[str, str, None, dict]:
    return "menu", _MENU_TEXTO, None, {}


def _cancelar(dados: dict) -> tuple[str, str, None, dict]:
    return "cancelado", _CANCELADO_TEXTO, None, dados


def _expirar(dados: dict) -> tuple[str, str, None, dict]:
    return "expirado", _EXPIRADO_TEXTO, None, dados


def _resumo(dados: dict) -> str:
    partes = [f"Tipo: {dados['tipo']}", f"Descricao: {dados['descricao']}"]
    if dados.get("onde"):
        partes.append(f"Onde: {dados['onde']}")
    if dados.get("passos"):
        partes.append(f"Passos: {dados['passos']}")
    if dados.get("esperado"):
        partes.append(f"Esperado/aconteceu: {dados['esperado']}")
    anexos = dados.get("anexos", [])
    if anexos:
        partes.append(f"Anexos: {', '.join(anexos)}")
    return " | ".join(partes)


def _criar(dados: dict) -> tuple[str, str, dict, dict]:
    acao = {"tipo": "criar", "dados": dict(dados)}
    resp = "Recebemos seu chamado #NNN. Etapa 1 de 6: Recebido. Avisaremos a cada passo."
    return "criado", resp, acao, dados


def conversa(
    estado: str, mensagem: str, dados: dict
) -> tuple[str, str, dict | None, dict]:
    """Processa uma mensagem e devolve o novo estado, resposta, acao e dados.

    Args:
        estado: estado atual da conversa.
        mensagem: texto enviado pelo cliente (ou "expirar" do orquestrador).
        dados: dados coletados ate agora (dict mutavel internamente).

    Returns:
        (novo_estado, resposta, acao, novos_dados)
        acao e None ou {"tipo": "criar", "dados": {...}}.
    """
    msg = mensagem.strip().lower()
    novos_dados = dict(dados)

    # Cancelar e expirar valem em qualquer estado (exceto cancelado/expirado/criado).
    if msg == "cancelar" and estado not in ("cancelado", "expirado", "criado"):
        return _cancelar(novos_dados)
    if msg == "expirar" and estado not in ("cancelado", "expirado", "criado"):
        return _expirar(novos_dados)

    # Estados terminais: ignoram novas mensagens.
    if estado in ("cancelado", "expirado", "criado"):
        return estado, "", None, novos_dados

    # --- inicio ---
    if estado == ESTADO_INICIO or estado == "":
        return _menu()

    # --- menu ---
    if estado == "menu":
        if msg == "1":
            novos_dados["tipo"] = "bug"
            prompt = _PROMPTS["descricao"]["bug"]
            return "descricao", prompt, None, novos_dados
        if msg == "2":
            novos_dados["tipo"] = "melhoria"
            prompt = _PROMPTS["descricao"]["melhoria"]
            return "descricao", prompt, None, novos_dados
        if msg == "3":
            novos_dados["tipo"] = "sugestao"
            prompt = _PROMPTS["descricao"]["sugestao"]
            return "descricao", prompt, None, novos_dados
        # Opcao invalida: mantem menu
        return "menu", f"Opcao invalida. {_MENU_TEXTO}", None, novos_dados

    # --- descricao ---
    if estado == "descricao":
        novos_dados["descricao"] = mensagem.strip()
        tipo = novos_dados.get("tipo", "")
        if tipo == "bug":
            return "onde", _PROMPTS["onde"], None, novos_dados
        # melhoria/sugestao: pula para anexos
        return "anexos", _PROMPTS["anexos"], None, novos_dados

    # --- onde ---
    if estado == "onde":
        novos_dados["onde"] = mensagem.strip()
        return "passos", _PROMPTS["passos"], None, novos_dados

    # --- passos ---
    if estado == "passos":
        novos_dados["passos"] = mensagem.strip()
        return "esperado_aconteceu", _PROMPTS["esperado_aconteceu"], None, novos_dados

    # --- esperado_aconteceu ---
    if estado == "esperado_aconteceu":
        novos_dados["esperado"] = mensagem.strip()
        return "anexos", _PROMPTS["anexos"], None, novos_dados

    # --- anexos ---
    if estado == "anexos":
        if msg == "pular":
            resumo = _resumo(novos_dados)
            return "confirmacao", f"{resumo}\n{_PROMPTS['confirmacao']}", None, novos_dados
        # Acumula anexo
        anexos = list(novos_dados.get("anexos", []))
        anexos.append(mensagem.strip())
        novos_dados["anexos"] = anexos
        return "anexos", "Recebido. Mande mais capturas ou digite 'pular'.", None, novos_dados

    # --- confirmacao ---
    if estado == "confirmacao":
        if msg in ("sim", "s", "confirma", "confirmo"):
            return _criar(novos_dados)
        if msg in ("nao", "n", "cancelar"):
            return _menu()
        # Resposta invalida: mantem confirmacao
        return "confirmacao", _PROMPTS["confirmacao"], None, novos_dados

    # Estado desconhecido: reinicia
    return _menu()
