"""Testes de fumaça do companion — caso feliz e caso de falha por comportamento.

Rodam sem rede e sem banco (adaptador echo + store em memória).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient  # noqa: E402

import app as app_mod  # noqa: E402
from corpus import Corpus, normalizar  # noqa: E402
from store import MemoriaStore  # noqa: E402
import tutor  # noqa: E402

cliente = TestClient(app_mod.app)


# --- corpus ---------------------------------------------------------------

def test_normalizar_remove_acento_e_palavras_de_parada():
    assert normalizar("A Definição de Pronto é verificável") == ["definicao", "pronto", "verificavel"]


def test_busca_encontra_pagina_relevante():
    c = Corpus.carregar()
    assert len(c) > 50, "corpus não gerado — rode build_corpus.py"
    achados = c.buscar("como abrir um ciclo", k=3)
    assert achados, "busca não retornou nada"
    assert any("ciclo" in t["pagina"].lower() or "ciclo" in t["titulo"].lower() for t in achados)


def test_busca_sem_termo_util_devolve_vazio():
    """Caso de falha: pergunta só com palavras de parada não casa nada."""
    assert Corpus.carregar().buscar("e o de a") == []


# --- tutor ----------------------------------------------------------------

def test_prompt_exige_citar_pagina_e_expandir_sigla():
    msgs = tutor.montar_mensagens("o que é DoD?", [], [])
    sistema = msgs[0]["content"]
    assert "Cite a página" in sistema
    assert "por extenso" in sistema


def test_fontes_sao_distintas_por_url():
    trechos = [
        {"pagina": "P", "url": "a.html", "trilha": "T", "titulo": "x", "texto": "y"},
        {"pagina": "P", "url": "a.html", "trilha": "T", "titulo": "z", "texto": "w"},
    ]
    assert len(tutor.fontes(trechos)) == 1


# --- store ----------------------------------------------------------------

def test_memoria_store_anexa_conta_e_apaga():
    s = MemoriaStore()
    s.anexar("s1", "usuario", "oi")
    s.anexar("s1", "assistente", "olá")
    assert s.contar("s1") == 2
    assert s.historico("s1")[-1]["conteudo"] == "olá"
    s.apagar("s1")
    assert s.contar("s1") == 0


# --- API ------------------------------------------------------------------

def test_health_responde_sem_vazar_segredo():
    r = cliente.get("/health")
    assert r.status_code == 200
    corpo = r.json()
    assert corpo["ok"] is True and corpo["trechos_no_corpus"] > 0
    assert "OPENAI_API_KEY" not in r.text and "sk-" not in r.text


def test_chat_responde_com_fontes():
    sessao = cliente.post("/sessao").json()["sessao"]
    r = cliente.post("/chat", json={"sessao": sessao, "mensagem": "por que a spec é a fonte de verdade?"})
    assert r.status_code == 200
    corpo = r.json()
    assert corpo["resposta"]
    assert corpo["fontes"] and corpo["fontes"][0]["url"].endswith(".html")


def test_chat_recusa_mensagem_grande():
    """Caso de falha: acima do limite, o serviço devolve 413 e não processa."""
    sessao = cliente.post("/sessao").json()["sessao"]
    r = cliente.post("/chat", json={"sessao": sessao, "mensagem": "x" * 5000})
    assert r.status_code == 413


def test_historico_e_apagar():
    sessao = cliente.post("/sessao").json()["sessao"]
    cliente.post("/chat", json={"sessao": sessao, "mensagem": "o que é uma raia?"})
    assert len(cliente.get("/historico", params={"sessao": sessao}).json()["mensagens"]) == 2
    cliente.delete(f"/sessao/{sessao}")
    assert cliente.get("/historico", params={"sessao": sessao}).json()["mensagens"] == []

def test_corpus_cobre_todas_as_paginas_do_livro():
    """Fitness function: página do livro ausente do corpus.

    Se uma página entrar no sumário e o corpus não for regenerado, este teste falha —
    o esquecimento que o README só *pedia* para não cometer.

    LIMITE (honesto): compara títulos, então pega página **faltando**, não conteúdo
    **desatualizado** dentro de uma página existente. Para isso, a regra continua sendo
    rodar `build_corpus.py` a cada mudança do livro.
    """
    import json

    raiz = Path(__file__).resolve().parents[3]
    sumario = json.loads((raiz / "publicar" / "sumario.json").read_text(encoding="utf-8"))
    esperadas = {i["titulo"] for p in sumario["partes"] for i in p["itens"]}
    no_corpus = {t["pagina"] for t in json.loads(Path(__file__).parents[1].joinpath("corpus.json").read_text(encoding="utf-8"))}
    faltando = esperadas - no_corpus
    assert not faltando, (
        "corpus desatualizado — rode `python companion/backend/build_corpus.py`. "
        f"Páginas ausentes: {sorted(faltando)}"
    )
