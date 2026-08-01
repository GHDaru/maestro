# Tasks 015 — Companion: o tutor do livro

## Verificação primeiro
- [x] **T0** — Checks: pytest, build sem/com a variável, /health sem segredo, capturas.

## Implementação
- [x] **T1** — FR1: `corpus.py` (busca lexical com peso de título) + `build_corpus.py`
  (259 trechos de 34 páginas, gerado do `sumario.json`).
- [x] **T2** — FR2: `tutor.py` — prompt com as regras do livro (citar página, sigla por
  extenso, não inventar, Diátaxis, uma ideia por vez).
- [x] **T3** — FR3: `llm.py` — `OpenAICompatAdapter` (NVIDIA NIM) + `EchoAdapter`; BYOK
  só na requisição; erro do provedor nunca vaza chave.
- [x] **T4** — FR4: `store.py` — memória e Postgres/Neon; banco fora do ar não derruba.
- [x] **T5** — FR5: `app.py` — 6 endpoints, CORS restrito, limites por sessão/mensagem.
- [x] **T6** — FR6: widget (`companion.js`/`.css`) + injeção condicional no motor do site.
- [x] **T7** — FR7: `companion/README.md` + `.env.example` + `Procfile` + `.gitignore`.

## Correções de defeito (encontradas no ciclo)
- [x] **T8** — CSS do widget usava `--fg`, variável que **não existe** no tema do livro
  (é `--text`): todo texto caía no fallback escuro e ficava ilegível no tema claro.
- [x] **T9** — Assets `companion.{css,js}` ficavam órfãos no site quando a variável era
  removida; o build agora os apaga.

## Documentação viva (mesmo PR)
- [x] **T10** — Evidência visual commitada (dois temas); CHANGELOG.

## Gate
- [x] **T11** — DoD verde → `promover-main.sh`.
