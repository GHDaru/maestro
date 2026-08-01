"""API do companion do livro Maestro (FastAPI).

Endpoints enxutos — cada um com um papel:

| Método | Rota            | Papel                                            |
|--------|-----------------|--------------------------------------------------|
| GET    | /health         | healthcheck + estado da configuração (sem segredo)|
| POST   | /sessao         | garante a sessão anônima do navegador             |
| POST   | /chat           | um turno: busca no livro + tutor + persistência   |
| GET    | /historico      | retomar a conversa                                |
| DELETE | /sessao/{id}    | apagar a sessão (direito ao esquecimento)         |
| GET    | /sugestoes-de-inicio | perguntas prontas para o widget              |
"""

from __future__ import annotations

import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import config
import llm as llm_mod
import store as store_mod
import tutor
from corpus import Corpus

app = FastAPI(title="Maestro — companion do livro", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGENS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)

CORPUS = Corpus.carregar()
STORE = store_mod.obter()
LLM = llm_mod.obter()

SUGESTOES = [
    "O que é o Maestro em uma frase?",
    "Por que a spec é a fonte de verdade?",
    "Quando uma mudança precisa de spec completa?",
    "Como escrevo um critério de aceite verificável?",
    "Quais gates são indelegáveis?",
]


class EntradaChat(BaseModel):
    sessao: str = Field(min_length=6, max_length=64)
    mensagem: str = Field(min_length=1)
    byok: str | None = None


@app.get("/health")
def health() -> dict:
    return {"ok": True, "trechos_no_corpus": len(CORPUS), **config.resumo()}


@app.get("/sugestoes-de-inicio")
def sugestoes() -> dict:
    return {"sugestoes": SUGESTOES}


@app.post("/sessao")
def criar_sessao() -> dict:
    return {"sessao": "anon-" + uuid.uuid4().hex[:16]}


@app.post("/chat")
def chat(entrada: EntradaChat) -> dict:
    mensagem = entrada.mensagem.strip()
    if len(mensagem) > config.LIMITE_TAMANHO_MENSAGEM:
        raise HTTPException(413, f"mensagem acima de {config.LIMITE_TAMANHO_MENSAGEM} caracteres")
    if STORE.contar(entrada.sessao) >= config.LIMITE_MENSAGENS_SESSAO:
        raise HTTPException(429, "limite de mensagens desta sessão atingido")

    trechos = CORPUS.buscar(mensagem, k=4)
    historico = STORE.historico(entrada.sessao, limite=12)
    byok = entrada.byok if config.PERMITIR_BYOK else None  # nunca persistido
    resposta = LLM.responder(tutor.montar_mensagens(mensagem, trechos, historico), byok=byok)

    STORE.anexar(entrada.sessao, "usuario", mensagem)
    STORE.anexar(entrada.sessao, "assistente", resposta)
    return {"resposta": resposta, "fontes": tutor.fontes(trechos)}


@app.get("/historico")
def historico(sessao: str) -> dict:
    return {"mensagens": STORE.historico(sessao, limite=40)}


@app.delete("/sessao/{sessao}")
def apagar(sessao: str) -> dict:
    STORE.apagar(sessao)
    return {"ok": True}
