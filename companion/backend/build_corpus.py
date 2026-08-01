"""Gera `corpus.json` a partir do sumário do livro.

Uma entrada por seção (`##`) de cada página publicada: título da seção, página,
URL relativa no site e o texto limpo. Rodar sempre que o livro mudar:

    python companion/backend/build_corpus.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
SUMARIO = RAIZ / "publicar" / "sumario.json"
SAIDA = Path(__file__).parent / "corpus.json"
TAMANHO_MAX = 1400  # caracteres por trecho — cabe no contexto sem sufocar


def slug_de(arquivo: str) -> str:
    """Mesma regra do motor do site (README usa o diretório pai)."""
    p = Path(arquivo)
    base = p.stem.lower()
    if base not in ("readme", "index"):
        return base
    pai = p.parent.name.lower()
    return base if pai in ("", ".", "docs") else pai


def limpar(md: str) -> str:
    md = re.sub(r"```.*?```", " ", md, flags=re.S)          # blocos de código
    md = re.sub(r"^\s*>\s?", "", md, flags=re.M)             # citações
    md = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", md)         # links -> texto
    md = re.sub(r"[*_`#|]+", " ", md)                        # marcação
    md = re.sub(r"\s+", " ", md)
    return md.strip()


def main() -> int:
    sumario = json.loads(SUMARIO.read_text(encoding="utf-8"))
    trechos: list[dict] = []
    for parte in sumario["partes"]:
        for item in parte["itens"]:
            caminho = RAIZ / item["arquivo"]
            if not caminho.exists():
                print(f"  ⚠ ausente: {item['arquivo']}")
                continue
            md = caminho.read_text(encoding="utf-8")
            slug = slug_de(item["arquivo"])
            # divide por seções de nível 2; o preâmbulo vira "Abertura"
            partes = re.split(r"^##\s+(.+)$", md, flags=re.M)
            blocos = [("Abertura", partes[0])] + [
                (partes[i].strip(), partes[i + 1]) for i in range(1, len(partes) - 1, 2)
            ]
            for titulo, corpo in blocos:
                texto = limpar(corpo)
                if len(texto) < 80:
                    continue
                for k in range(0, len(texto), TAMANHO_MAX):
                    trechos.append({
                        "trilha": parte["nome"],
                        "pagina": item["titulo"],
                        "titulo": titulo,
                        "url": f"{slug}.html",
                        "texto": texto[k:k + TAMANHO_MAX],
                    })
    SAIDA.write_text(json.dumps(trechos, ensure_ascii=False), encoding="utf-8")
    print(f"✓ corpus: {len(trechos)} trechos de {len(set(t['pagina'] for t in trechos))} páginas → {SAIDA.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
