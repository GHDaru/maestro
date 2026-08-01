"""Configuração do companion — lida SÓ de variáveis de ambiente.

Princípio III (reversibilidade) e regra de segurança do método aplicados ao próprio
serviço: nenhuma credencial no código nem no repositório. Defaults são seguros —
sem chave, o adaptador é `echo`; sem banco, a persistência é em memória.
"""

from __future__ import annotations

import os
from pathlib import Path


def _carregar_dotenv() -> None:
    """Carrega um `.env` vizinho para o ambiente (sem dependência externa).

    O `.env` é ignorado pelo git; use `.env.example` como molde.
    """
    for pasta in (Path(__file__).parent, *Path(__file__).parents):
        env = pasta / ".env"
        if env.exists():
            for linha in env.read_text(encoding="utf-8").splitlines():
                linha = linha.strip()
                if linha and not linha.startswith("#") and "=" in linha:
                    chave, _, valor = linha.partition("=")
                    os.environ.setdefault(chave.strip(), valor.strip())
            return


_carregar_dotenv()


def _bool(nome: str, padrao: bool) -> bool:
    return os.environ.get(nome, str(padrao)).strip().lower() in ("1", "true", "yes", "on")


# --- modelo ---------------------------------------------------------------
# Sem OPENAI_API_KEY o adaptador cai para "echo" (prova o fluxo, não chama rede).
LLM_ADAPTER = os.environ.get("LLM_ADAPTER", "openai" if os.environ.get("OPENAI_API_KEY") else "echo")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://integrate.api.nvidia.com/v1")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
LLM_MODEL = os.environ.get("LLM_MODEL", "meta/llama-3.3-70b-instruct")
LLM_TIMEOUT = float(os.environ.get("LLM_TIMEOUT", "60"))
LLM_MAX_TOKENS = int(os.environ.get("LLM_MAX_TOKENS", "700"))

# --- persistência ---------------------------------------------------------
# Sem DATABASE_URL -> memória (dev). Com -> Postgres (Neon).
DATABASE_URL = os.environ.get("DATABASE_URL", "")

# --- serviço --------------------------------------------------------------
CORS_ORIGENS = [o.strip() for o in os.environ.get(
    "CORS_ORIGENS", "https://ghdaru.github.io,http://localhost:8000,http://127.0.0.1:8000"
).split(",") if o.strip()]
LIMITE_MENSAGENS_SESSAO = int(os.environ.get("LIMITE_MENSAGENS_SESSAO", "60"))
LIMITE_TAMANHO_MENSAGEM = int(os.environ.get("LIMITE_TAMANHO_MENSAGEM", "2000"))
PERMITIR_BYOK = _bool("PERMITIR_BYOK", True)


def resumo() -> dict:
    """Estado da configuração para o /health — sem vazar segredo."""
    return {
        "adapter": LLM_ADAPTER,
        "modelo": LLM_MODEL if LLM_ADAPTER != "echo" else None,
        "chave_projeto": bool(OPENAI_API_KEY),
        "persistencia": "postgres" if DATABASE_URL else "memoria",
        "byok": PERMITIR_BYOK,
    }
