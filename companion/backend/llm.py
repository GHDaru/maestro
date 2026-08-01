"""LLMPort — a porta do modelo, com dois adaptadores.

`echo` prova o fluxo sem rede (usado nos testes e sem chave configurada);
`openai` fala com qualquer endpoint compatível com a API da OpenAI — por padrão
o NVIDIA NIM. BYOK (*bring your own key*, "traga sua própria chave") é usado só
na requisição em que chega: nunca persistido, nunca registrado em log.
"""

from __future__ import annotations

from typing import Optional, Protocol

import httpx

import config

Mensagem = dict


class LLMPort(Protocol):
    def responder(self, mensagens: list[Mensagem], byok: Optional[str] = None) -> str: ...


class EchoAdapter:
    """Sem rede: devolve um eco explicando como ligar o modelo real."""

    def responder(self, mensagens: list[Mensagem], byok: Optional[str] = None) -> str:
        ultima = next((m for m in reversed(mensagens) if m.get("role") == "user"), {})
        pergunta = (ultima.get("content") or "").strip()
        return (
            f"(modo echo — sem modelo configurado) Você perguntou: “{pergunta}”.\n\n"
            "Para respostas reais, defina `OPENAI_API_KEY` (NVIDIA NIM) no ambiente do "
            "serviço. Enquanto isso, o trecho do livro mais próximo da sua pergunta "
            "aparece nas fontes abaixo."
        )


class OpenAICompatAdapter:
    """Endpoint compatível com OpenAI (NVIDIA NIM por padrão)."""

    def responder(self, mensagens: list[Mensagem], byok: Optional[str] = None) -> str:
        chave = (byok or "").strip() or config.OPENAI_API_KEY
        if not chave:
            return EchoAdapter().responder(mensagens)
        url = config.OPENAI_BASE_URL.rstrip("/") + "/chat/completions"
        corpo = {
            "model": config.LLM_MODEL,
            "messages": mensagens,
            "max_tokens": config.LLM_MAX_TOKENS,
            "temperature": 0.3,
        }
        try:
            with httpx.Client(timeout=config.LLM_TIMEOUT) as cliente:
                r = cliente.post(url, json=corpo, headers={"Authorization": f"Bearer {chave}"})
                r.raise_for_status()
                dados = r.json()
            return (dados["choices"][0]["message"]["content"] or "").strip()
        except httpx.HTTPStatusError as e:
            # Nunca ecoar a chave nem o corpo da requisição.
            return f"(erro do provedor: HTTP {e.response.status_code}) Tente novamente em instantes."
        except Exception:
            return "(o modelo não respondeu a tempo) Tente novamente — sua pergunta não foi perdida."


def obter() -> LLMPort:
    return OpenAICompatAdapter() if config.LLM_ADAPTER == "openai" else EchoAdapter()
