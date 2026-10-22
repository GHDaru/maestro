# TAIL:security — ciclo 066 (painel de coordenação v0)

Passagem independente em contexto fresco (agente `security`, 20/10/2026, só leitura; sem shell,
medido por leitura e grep sobre a árvore do worktree em `5161449`). Classe de risco declarada no
plano: **média** (lê o repositório, grava um `.db` local, serve HTTP em localhost, roda como hook).

## Achados

1. **[média] CSRF / DNS rebinding contra `POST /api/eventos` e `POST /api/reingerir`.**
   `server.py:473` liga só em `127.0.0.1` e `server.py:438` checa `client_address` — mas qualquer
   página aberta no navegador do usuário também é `127.0.0.1`. Não há verificação de
   `Host`/`Origin` nem token. Uma página hostil pode gravar eventos forjados (`autor` livre) ou
   disparar reingestão (que executa `git` em todos os repos configurados). Fix mínimo: em
   `do_POST`, recusar se `Host` não for `127.0.0.1:<porta>`/`localhost:<porta>` e se `Origin`
   existir e não for o mesmo; ou exigir header `X-Painel: 1` (o `fetch` de `index.html:223` passa
   a enviá-lo).
2. **[média] Impersonação do `autor` via MCP e HTTP (Princípio II).** `mcp_painel.py:31-41` e
   `server.py:364` aceitam `autor` como string livre; um modelo conectado pode registrar
   `--autor Darú` e promover peça a `aprovada às cegas` com evidência fabricada (só se checa a
   presença das chaves, `server.py:377`). Fix mínimo: no MCP, fixar `autor` a partir do nome da
   sessão/config do servidor e marcar `origem='mcp'`; reservar valores humanos (lista em config)
   para o `registrar.py` local.
3. **[baixa] `PROIBIDOS` cobre `.env*` mas não symlinks nem `..`.** `ingest.py:25` casa `.env`,
   `.env.local`, `.env.production`; a exceção `backups_producao/diario/backup.log` é anexo exato.
   Porém `expande()`/`carrega_cfg` (`ingest.py:516-555`) aceitam `../fora/**` e `glob` segue
   symlinks; nada confina a `raiz`. Fix: em `expande`, descartar `os.path.islink` e caminhos cujo
   `realpath` não começa por `raiz`.
4. **[ok] Servidor de arquivos.** `server.py:409-411` serve apenas `index.html` e
   `arquitetura.html` por whitelist; sem join de URL.
5. **[ok] Injeção.** SQL parametrizado em todo lugar (`server.py:388`, `ingest.py`); `subprocess`
   sempre lista, sem `shell=True` (`ingest.py:209`, `veredito_hook.py:108`). `index.html` usa
   `innerHTML`, mas todo dado de eventos/specs/git passa por `esc()` (`index.html:155`). Sem XSS.
6. **[baixa] Segredos / dados pessoais.** Nenhum token, IP, host ou senha; `exemplo.json` aponta
   para o próprio repo; `painel/dados/` está em `painel/.gitignore:1`. O `.db` grava caminhos
   relativos à raiz e nomes de autor de commit (dado pessoal se publicado). `v_meta` expõe
   `contatos` da config em `/api/meta` (`server.py:242`): com o achado 1, uma página hostil lê isso.
   Fix: remover `contatos` da API ou servi-lo só com o header do item 1.
7. **[ok] Hook pre-commit.** Bypass por `--no-verify` é esperado; só lê conteúdo via regex e
   chama `git log/cat-file` com hash validado por `[0-9a-f]{7,40}` (`veredito_hook.py:56`). Não
   executa nada do commit.

## Veredito

Sem segredo nem injeção; dois achados médios (CSRF/rebinding no POST sem checagem de
Origin/Host, `server.py:438`; `autor` forjável via MCP, `mcp_painel.py:31`). Classe média
confirmada; **gate humano antes de uso com modelo conectado**.

## Decisão deste ciclo

O ciclo é retroativo: o código de `a1172a2` entra como está, e os achados 1, 2, 3 e 6 viram
**dívida declarada com dono**, a pagar no ciclo 072 (painel de regência), que reescreve a
superfície HTTP/MCP. Até lá: não ligar o MCP do painel a uma sessão de modelo e não abrir o
painel com outras páginas no mesmo navegador. Registrado no `qa-report.md` e no plano do 072.
