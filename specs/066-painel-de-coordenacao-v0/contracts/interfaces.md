# Contracts 066 — Interfaces do painel de coordenação v0

> Lido do código em `4919f4a`: `painel/server.py` (`ROTAS`, linhas 354-357; handler, 394-456),
> `painel/mcp_painel.py` (`FERRAMENTAS`, 23-42; `responde`, 67-85), `painel/registrar.py` e
> `.maestro/controle/git-hooks/veredito_hook.py`. Quatro contratos; todos consomem a mesma
> validação (`server.valida_evento`) e o mesmo modelo (`data-model.md`).
>
> Siglas: HTTP (*Hypertext Transfer Protocol*) · JSON (*JavaScript Object Notation*) · MCP
> (*Model Context Protocol*, protocolo de contexto de modelo) · CLI (*command-line interface*)
> · DORA (*DevOps Research and Assessment*) · stdio (entrada e saída padrão).

## 1. HTTP — `painel/server.py <projeto.json> [--porta 8765] [--db caminho] [--reingerir]`

Escuta **só** em `127.0.0.1` (`server.py:473`). Respostas JSON com `Content-Type:
application/json; charset=utf-8` e `Cache-Control: no-store`. Rota desconhecida → 404
`{"erro": "rota inexistente"}`.

### 1.1 Páginas (GET)

| Rota | Devolve |
|---|---|
| `/`, `/index.html` | o painel (HTML + JavaScript puro, sem build) |
| `/arquitetura.html` | documento de arquitetura do painel (escopo não declarado, entregue — `plan.md`) |

### 1.2 Leitura (GET, `/api/...`)

| Rota | Parâmetros | Devolve |
|---|---|---|
| `/api/board` | — | sessões por coluna de estado: `sessao`, `estado`, `em`, `idade_min`, `peca`, `worktree`, `ultimo_hash`, `proximo`, alerta de sem sinal |
| `/api/pecas` | — | fluxo de peças com a coluna atual e selos de evidência (chaves presentes de `EVIDENCIA_EXIGIDA`) |
| `/api/specs` | — | specs com `tasks_feitas/tasks_total`, `tem_plan`, `tem_qa` |
| `/api/decisoes` | — | decisões do índice e ADRs |
| `/api/qualidade` | — | `barra`, `defeitos`, `desvios`, `classes` |
| `/api/documentos` | — | documentos com idade em horas |
| `/api/roadmap` | — | linhas do roadmap |
| `/api/dora` | `dias` (padrão 30) | `metricas` (cada uma com `fonte` ao lado; `—` sem registro), `notas`; merge só como `proxy_entregas_por_repo` |
| `/api/meta` | — | projeto, hora da última ingestão, estados e exigências (`exigencias` = `EVIDENCIA_EXIGIDA`) |
| `/api/higiene` | — | `total`, `integradas`, `candidatas_remocao` (**para aprovação, nunca executada**), `com_risco` |
| `/api/tempo` | — | tempo por fase e rodada |
| `/api/relatorio-lote` | `desde` (ISO; padrão: 24 h) | `{"markdown": ...}` — material de retro; a decisão MANTER/MUDAR/CORTAR é humana |
| `/api/estado-ia` | `sessao` (opcional) | ver §1.3 |

### 1.3 `GET /api/estado-ia?sessao=<id>` (`server.py:296-319`)

O estado derivado para a IA — substitui o "Estado atual" digitado à mão.

```json
{
  "gerado_em": "2026-10-20T10:00:00-03:00",
  "fonte": "painel Maestro (cache derivado; a verdade são os arquivos citados)",
  "equipe": [{"sessao": "W04", "estado": "trabalhando", "em": "...", "idade_min": 12}],
  "ultimas_decisoes": [...], "barra_ultima": [...], "desvios_recentes": [...],
  "riscos_git": [{"caminho": "...", "branch": "...", "risco": "..."}],
  "dora_7d": {...},
  "voce": {"sessao": "W04", "estado": "...", "em": "...", "peca": "...", "worktree": "...",
           "ultimo_hash": "...", "proximo": "...", "arquivo_papel": "...", "historico": [...]},
  "seus_desvios": [...]
}
```

Contrato: com `sessao`, a chave `voce` existe sempre — é o objeto acima **ou `null`** quando a
sessão não tem card (`server.py:315-316`). Os campos ficam **aninhados em `voce`**, não na
raiz; a chave do próximo passo chama-se `proximo`. Sem `sessao`, `voce` e `seus_desvios` não
existem. A busca por sessão ignora maiúsculas.

### 1.4 Escrita (POST)

| Rota | Corpo | Respostas |
|---|---|---|
| `/api/eventos` | JSON com `tipo`, `autor` e os campos do tipo (`data-model.md` §2) | `201 {"ok": true}` · `422 {"erro": "<motivo de valida_evento>"}` · `403 {"erro": "só localhost"}` se `client_address` ∉ {`127.0.0.1`, `::1`} |
| `/api/reingerir` | vazio | `200` com o resumo de `ingest.ingere` (contagens, duração); 403 fora de localhost |

Motivos de 422 (`valida_evento`, `server.py:360-380`): `tipo inválido` · `autor é obrigatório`
· `estado de sessão deve ser um de (...)` · `estado de peça deve ser um de (...)` · `peca é
obrigatória` · `evidencia deve ser JSON` · `sem prova não muda de coluna: faltam [...]`.

## 2. MCP — `painel/mcp_painel.py <projeto.json>` (stdio, JSON-RPC)

`serverInfo`: `{"name": "maestro-painel", "version": "0.1"}`. Métodos: `initialize`,
`tools/list`, `tools/call`, `ping`. Erro de validação volta como `{"content": [{"type":
"text", "text": "recusado: <motivo>"}], "isError": true}` — nunca como exceção do protocolo.

| Ferramenta | Entrada (`inputSchema`) | Faz |
|---|---|---|
| `estado_atual` | `sessao` (opcional) | devolve `v_estado_ia(db, sessao)` — o mesmo JSON de §1.3, como texto |
| `registrar_status` | obrigatórios `sessao`, `estado` (enum `ESTADOS_SESSAO`), `texto`, `autor`; opcional `peca` | `grava_evento` com `tipo="status"` |
| `registrar_peca` | obrigatórios `peca`, `estado` (enum `ESTADOS_PECA`), `evidencia` (**objeto**, serializado antes de gravar), `autor`; opcionais `texto`, `sessao` | `grava_evento` com `tipo="peca"`; recusado sem a evidência do estado |

Não há ferramenta de deploy, incidente ou recuperação por MCP: esses fatos entram pela CLI ou
pelo HTTP, com autor humano.

## 3. CLI — `painel/registrar.py <projeto.json> <tipo> --autor X [opções]`

| Posição/opção | Valores | Obrigatório |
|---|---|---|
| `projeto` | caminho de `painel/projetos/<nome>.json` | sim |
| `tipo` | `status` · `deploy` · `incidente` · `recuperacao` · `peca` · `nota` | sim |
| `--autor` | texto | **sim** (argparse) |
| `--sessao`, `--estado`, `--peca`, `--texto` | texto | conforme o tipo (`valida_evento`) |
| `--evidencia` | string JSON, ex.: `'{"hash":"abc","runner2":"r2"}'` | para `peca` a partir de `entregue` |
| `--ts` | carimbo ISO informado pelo autor | não — **dívida 072**: fura o carimbo verificável |
| `--db` | caminho do `.db` (padrão `painel/dados/<projeto>.db`) | não |

Saída: `ok` em stdout e **exit 0** quando grava; `recusado: <motivo>` em stderr e **exit 2**
quando `valida_evento` recusa — antes do `INSERT`, logo `COUNT(*)` de `eventos` não muda
(`registrar.py:38-41`). Erro de argparse (sem `--autor`, tipo fora da lista) → exit 2 do próprio
argparse. Exemplos na docstring do arquivo usam `projetos/exemplo.json`.

## 4. Hook de pre-commit — `.maestro/controle/git-hooks/veredito_hook.py`

| Modo | Comando | Exit |
|---|---|---|
| pre-commit | `python veredito_hook.py --pre-commit` (a partir da raiz do repositório) | `0` se nenhum veredito staged ou todos aceitos; `1` se algum recusado |
| standalone | `python veredito_hook.py <arquivo>` | `0` aceito (`OK:`) · `1` recusado (`RECUSADO: <arquivo>: <motivo>`) |
| sem argumentos | — | `2` (imprime ajuda) |

Arquivos alvo: staged (`git diff --cached --name-only --diff-filter=ACM`) cujo nome contém
`veredito` ou `critica` e termina em `.md`. Regras (docstring, linhas 7-15):

1. tem linha `Objeto: <caminho> @ <hash>` (7-40 hex) — sem ela, recusado;
2. o hash existe e não é posterior ao commit do veredito;
3. `Data:` no texto não pode exceder a hora do commit + 2 min;
4. a hora do veredito é posterior à hora do commit do objeto (author date `%ai`);
5. sem `Data:`, usa a hora do commit (ou `mtime` em pre-commit);
6. cherry-pick usa data do autor, não do committer;
7. `Data:` com formato não reconhecido → recusado;
8. formatos aceitos: `dd/mm/aaaa hh:mm [±hhmm]`, `dd/mm/aaaa`, `aaaa-mm-dd hh:mm:ss BRT`,
   inglês (`Sat Oct 3 16:00:00 2026`), extenso em português; com ou sem `**Data:**` em negrito.

Instalação: `git config core.hooksPath .maestro/controle/git-hooks` (ou ligação em
`.git/hooks/pre-commit`); depende de `python` no caminho do Git Bash no Windows. Testes que
provam cada caso: `test_sem_linha_objeto_rejeita`, `test_hash_inexistente_rejeita`,
`test_veredito_anterior_ao_objeto_rejeita`, `test_hora_texto_3min_rejeita`,
`test_formato_desconhecido_recusa`, `test_normal_aceita`, `test_B7_so_data_aceita`,
`test_sem_hora_aceita`, `test_author_date_preservada`, `test_tasks_md_nao` (não é veredito).

## 5. O que atravessa a fronteira

| De → para | Contrato |
|---|---|
| sessão de IA → painel | `estado_atual` (MCP) ou `GET /api/estado-ia` — leitura, sem efeito |
| sessão/humano → `eventos` | `registrar_status`/`registrar_peca` (MCP), `POST /api/eventos`, `registrar.py` — todos passam por `valida_evento` |
| arquivos do projeto → projeção | `ingest.py <projeto.json>`; `POST /api/reingerir`; nunca escreve de volta |
| git → veredito | hook de pre-commit; independente do painel |
