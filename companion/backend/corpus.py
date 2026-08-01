"""Busca no livro — sem embeddings, sem banco vetorial.

O corpus é gerado de `publicar/sumario.json` (`build_corpus.py`): cada seção de cada
página vira um trecho com título, página e URL. A busca é lexical com pesos simples
(termo no título vale mais) — suficiente para um livro de dezenas de páginas, e
verificável. YAGNI: só troca por embeddings quando a recuperação doer.
"""

from __future__ import annotations

import json
import math
import re
import unicodedata
from pathlib import Path

CORPUS_PADRAO = Path(__file__).parent / "corpus.json"

_PARADAS = {
    "a", "o", "as", "os", "de", "da", "do", "das", "dos", "e", "em", "no", "na", "nos",
    "nas", "um", "uma", "para", "por", "com", "que", "se", "ao", "à", "às", "aos", "é",
    "ou", "mas", "como", "qual", "quais", "quando", "onde", "the", "of",
}


def normalizar(texto: str) -> list[str]:
    """minúsculas, sem acento, só palavras com 3+ letras, sem palavras de parada."""
    t = unicodedata.normalize("NFD", texto.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return [p for p in re.findall(r"[a-z0-9]{3,}", t) if p not in _PARADAS]


class Corpus:
    def __init__(self, trechos: list[dict]):
        self.trechos = trechos
        self._tokens = [set(normalizar(t["titulo"] + " " + t["texto"])) for t in trechos]
        self._tokens_titulo = [set(normalizar(t["titulo"] + " " + t["pagina"])) for t in trechos]
        # frequência de documento, para dar mais peso a termo raro
        self._df: dict[str, int] = {}
        for toks in self._tokens:
            for tok in toks:
                self._df[tok] = self._df.get(tok, 0) + 1
        self._n = max(1, len(trechos))

    @classmethod
    def carregar(cls, caminho: Path | str = CORPUS_PADRAO) -> "Corpus":
        p = Path(caminho)
        if not p.exists():
            return cls([])
        return cls(json.loads(p.read_text(encoding="utf-8")))

    def buscar(self, pergunta: str, k: int = 4) -> list[dict]:
        consulta = set(normalizar(pergunta))
        if not consulta or not self.trechos:
            return []
        pontuados: list[tuple[float, dict]] = []
        for i, trecho in enumerate(self.trechos):
            comuns = consulta & self._tokens[i]
            if not comuns:
                continue
            score = sum(math.log(1 + self._n / self._df.get(tok, 1)) for tok in comuns)
            score += 2.0 * len(consulta & self._tokens_titulo[i])  # título pesa mais
            pontuados.append((score, trecho))
        pontuados.sort(key=lambda x: x[0], reverse=True)
        return [t for _, t in pontuados[:k]]

    def __len__(self) -> int:
        return len(self.trechos)
