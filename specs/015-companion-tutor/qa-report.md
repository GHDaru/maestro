# QA-report 015 — Companion: o tutor do livro

- **Data**: 2026-08-01 · **Raia**: Plena · **Veredito**: ✅ CONFORME

## Fitness functions (DoD)

| Check | Esperado | Resultado |
|---|---|---|
| `pytest tests/ -q` | ≥8 passando (feliz + falha) | **10 passaram** ✅ |
| Build **sem** `MAESTRO_COMPANION_URL` | zero injeção, zero assets | 0 e 0 ✅ |
| Build **com** a variável | injeção em todas as páginas + 2 assets | 35 páginas, 2 assets ✅ |
| `GET /health` | sem segredo | ✅ (só booleanos e nomes) |
| `POST /chat` (pergunta coberta) | resposta + fontes com URL | ✅ 4 fontes relevantes |
| Mensagem acima do limite | HTTP 413 | ✅ |
| Widget legível nos dois temas | evidência visual | ✅ `companion/evidencia/` |

## Verificação ao vivo

Backend levantado (`uvicorn`), site servido (`http.server`) e widget exercitado por
navegador real: sugestões carregadas, pergunta enviada, resposta renderizada e **fontes
clicáveis** (Modelo operacional · 03 — Spec-Driven · 09 — DoR/DoD · Glossário) para a
pergunta "quando uma mudança precisa de spec completa?" — exatamente as páginas onde as
raias são definidas. A busca acerta sem embeddings.

## Dois defeitos encontrados e corrigidos

1. **Variável de tema inexistente**: o widget usava `var(--fg,…)`; o tema do livro define
   `--text`. Todo texto caía no *fallback* escuro → ilegível no tema claro. Só apareceu
   porque a verificação foi **visual, em navegador real** — nenhum teste de unidade pegaria.
2. **Assets órfãos**: ao remover a variável, `companion.{css,js}` permaneciam em `site/`
   (o build limpava apenas `.html`). Corrigido: assets são removidos quando não há endpoint.

## Lição para a retrospectiva

Meu primeiro check do DoD (`grep -l companion site/*.html`) deu **falso positivo**: casou
com menções legítimas no texto (o nome do arquivo do ADR 0011 e a nota da Jornada). O
comando provava a coisa errada. A skill `dod-verificavel` manda perguntar "que comando
prova isto?" — a correção foi verificar a **injeção** (`MAESTRO_COMPANION_URL`), não a
palavra. Candidato a anti-padrão novo: *check que casa com o texto em vez do artefato*.

## Pendência (fora do escopo, do Steward)

Publicar o serviço num provedor (Railway/Fly/Render) e definir `OPENAI_API_KEY`,
`DATABASE_URL` (Neon) e `CORS_ORIGENS=https://ghdaru.github.io`. Depois, gerar o site com
`MAESTRO_COMPANION_URL` apontando para o serviço.

## Gate

- Aprovação do Steward ("bora"); promovido via `promover-main.sh`.
