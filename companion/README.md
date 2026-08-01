# Companion — o tutor do livro Maestro

Assistente que responde sobre o método **a partir do livro**, citando a página. Decidido
no [ADR 0011](../docs/adr/0011-livro-padrao-editorial-e-companion.md); construído no ciclo 015.

## Arquitetura

```
Navegador (site estático no GitHub Pages)
   │  widget flutuante (HTML/JS puro, sem build) — assets/companion.{js,css}
   ▼  POST /chat  {sessao, mensagem}
Backend FastAPI  (este diretório)
   ├─ corpus.py  → busca lexical nos 259 trechos do livro (sem embeddings)
   ├─ tutor.py   → prompt com as regras do livro (citar página, sigla por extenso)
   ├─ llm.py     → NVIDIA NIM (chave do projeto) | BYOK por requisição | echo
   └─ store.py   → Postgres/Neon; sem DATABASE_URL → memória
```

**Por que um backend?** O GitHub Pages é estático: não guarda segredo nem roda modelo. O
serviço segura a chave, busca no livro e persiste a conversa.

## Rodar local (sem chave, sem banco)

```bash
cd companion/backend
pip install -r requirements.txt
python build_corpus.py                 # gera corpus.json do livro
uvicorn app:app --port 8099
```

Sem `OPENAI_API_KEY`, o adaptador é `echo`: o fluxo roda, as **fontes do livro** aparecem
de verdade, só a redação da resposta não vem de um modelo.

Para ver o widget no site:

```bash
cd publicar && MAESTRO_COMPANION_URL="http://127.0.0.1:8099" node build.mjs
cd ../site && python3 -m http.server 8098
# e no backend: CORS_ORIGENS="http://127.0.0.1:8098"
```

> Sem a variável `MAESTRO_COMPANION_URL`, o widget **não é injetado** — o site funciona
> exatamente como antes. O companion é aditivo, nunca requisito.

## Endpoints

| Método | Rota | Papel |
|---|---|---|
| `GET` | `/health` | healthcheck + estado da configuração (sem vazar segredo) |
| `POST` | `/sessao` | cria a sessão anônima do navegador |
| `POST` | `/chat` | um turno: busca no livro → tutor → persistência |
| `GET` | `/historico?sessao=…` | retomar a conversa |
| `DELETE` | `/sessao/{id}` | apagar a sessão (direito ao esquecimento) |
| `GET` | `/sugestoes-de-inicio` | perguntas prontas para o widget |

## Configuração (só por variável de ambiente)

Copie `.env.example` para `.env` (ignorado pelo git) ou defina no painel do provedor:

| Variável | Efeito |
|---|---|
| `OPENAI_API_KEY` | chave do NVIDIA NIM; **ausente → modo echo** |
| `OPENAI_BASE_URL` | endpoint compatível com OpenAI (padrão: NVIDIA) |
| `LLM_MODEL` | modelo (padrão: `meta/llama-3.3-70b-instruct`) |
| `DATABASE_URL` | Postgres/Neon; **ausente → memória** |
| `CORS_ORIGENS` | origens permitidas, separadas por vírgula |
| `LIMITE_MENSAGENS_SESSAO` | teto por sessão (padrão 60) |

## Publicar

O serviço é um processo web comum (`Procfile` incluído). Opções com plano gratuito:
**Railway** (o que o `harness_engineering` usa), **Fly.io** ou **Render** — os dois
últimos hibernam quando ociosos, o que é aceitável para demanda baixa.

Depois de publicar, gere o site com a URL do serviço:

```bash
MAESTRO_COMPANION_URL="https://seu-servico.exemplo" node publicar/build.mjs
```

## Segurança

- **Nenhum segredo no repositório.** `.env` é gitignored; `/health` não expõe chave.
- **BYOK** (*bring your own key*, "traga sua própria chave") é usada só na requisição em
  que chega — nunca persistida, nunca logada.
- **CORS** restrito às origens configuradas; **limite** de mensagens por sessão e de
  tamanho por mensagem.
- O tutor é instruído a **não inventar**: se o livro não cobre, ele diz.

## Testes

```bash
cd companion/backend && python -m pytest tests/ -q     # 10 testes, sem rede e sem banco
```

## Manter o corpus fresco

O corpus é gerado do `publicar/sumario.json`. **Toda vez que o livro mudar**, rode
`python companion/backend/build_corpus.py` e publique o backend — senão o tutor responde
com o livro velho.
