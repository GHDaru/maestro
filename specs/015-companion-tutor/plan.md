# Plan 015 — Companion: o tutor do livro

- **Spec**: `spec.md` · **Raia**: Plena · **Data**: 2026-08-01

## Constitution Check (principios-maestro.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven | ✅ nasce da spec 015 (decisão registrada no ADR 0011) |
| II. Orquestração humano-governada | ✅ o companion informa; não decide nem altera o repositório |
| III. Reversibilidade / gates de risco | ✅ aditivo: sem a variável de ambiente o site é idêntico; sem chave, echo; sem banco, memória |
| IV. Test-First / DoD verificável | ✅ 10 testes (feliz + falha), critérios em EARS, evidência visual |
| V. Economia de contexto / fronteira | ✅ portas separadas (corpus · tutor · modelo · store); o tutor recebe só 4 trechos |
| VI. Artefatos vivos | ✅ README + regra de regenerar o corpus a cada mudança do livro |
| VII. Governança leve / YAGNI | ✅ busca lexical, sem banco vetorial; sem tools; sem painel |
| VIII. Comunicação inteligível | ✅ o prompt **obriga** a expandir sigla — o princípio virou comportamento |

**Sem violações.**

## Como

- **Portas** (mesmo padrão hexagonal do método): `LLMPort`, `StorePort` e o corpus como
  módulo isolado — cada um com adaptador seguro por padrão.
- **Corpus**: `build_corpus.py` lê o `sumario.json` (fonte única do livro), divide por
  seção `##`, limpa marcação e grava `corpus.json` com página, trilha e URL.
- **Widget**: sem framework nem build; usa as variáveis do tema do livro para herdar
  claro/escuro.
- **Injeção condicional** no motor do site: `MAESTRO_COMPANION_URL` vazia → nada é copiado
  nem referenciado.

## Verificação (DoD)

- `pytest tests/ -q` → 10 passando.
- `node build.mjs` sem a variável → `grep -c companion site/*.html` = 0.
- `curl /health` → sem segredo; `POST /chat` → resposta + fontes com URL.
- Capturas do widget nos dois temas.
