# Data model 066 — Painel de coordenação v0

> Fonte: `painel/ingest.py` (`DERIVADAS`, linhas 27-62; `EVENTOS`, linhas 64-81) e
> `painel/server.py` (`ESTADOS_SESSAO`, `ESTADOS_PECA`, `EVIDENCIA_EXIGIDA`, linhas 24-34),
> lidos em `4919f4a`. Banco: SQLite (*Structured Query Language lite*, banco de dados em um
> arquivo), em `painel/dados/<projeto>.db`. Padrão: CQRS (*Command Query Responsibility
> Segregation*) — os arquivos do projeto são a fonte de verdade; o `.db` é projeção.

## 1. Duas classes de tabela

| Classe | Tabelas | Ciclo de vida | Quem escreve |
|---|---|---|---|
| **Projeção** (derivadas) | 15, listadas em §3 | `DROP TABLE IF EXISTS` + `CREATE TABLE` a **cada** ingestão | só `ingest.py`, a partir dos arquivos |
| **Fato** (só-acréscimo) | `eventos`, `ingest_log` | `CREATE TABLE IF NOT EXISTS`; sobrevivem à ingestão | `eventos`: `grava_evento` (HTTP, MCP, CLI); `ingest_log`: `ingest.py` |

Regra: **só entra direto no SQLite o que não existe em arquivo nenhum**. Tudo o mais é
reconstruível e, por isso, descartável.

## 2. A tabela `eventos` (fonte dos fatos sem arquivo)

```sql
CREATE TABLE IF NOT EXISTS eventos (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  ts        TEXT NOT NULL,          -- ISO 8601 com fuso; gerado por grava_evento se ausente
  sessao    TEXT,                   -- ex.: W04, Gerente02
  tipo      TEXT NOT NULL CHECK (tipo IN ('status','deploy','incidente','recuperacao','peca','nota')),
  estado    TEXT,                   -- vocabulário depende do tipo (§2.2)
  peca      TEXT,                   -- obrigatório quando tipo = 'peca'
  texto     TEXT,
  evidencia TEXT,                   -- JSON serializado; obrigatório conforme §2.3
  autor     TEXT NOT NULL           -- humano ou sessão identificada (Princípio II)
);
CREATE TRIGGER IF NOT EXISTS eventos_sem_update BEFORE UPDATE ON eventos
  BEGIN SELECT RAISE(ABORT, 'eventos e append-only'); END;
CREATE TRIGGER IF NOT EXISTS eventos_sem_delete BEFORE DELETE ON eventos
  BEGIN SELECT RAISE(ABORT, 'eventos e append-only'); END;
```

### 2.1 Tipos de evento

| `tipo` | O que registra | Campos usados | Quem consome |
|---|---|---|---|
| `status` | estado de uma sessão (sinal de vida) | `sessao`, `estado` (§2.2a), `texto`, `peca` | board (`/api/board`), `/api/estado-ia` |
| `peca` | transição de peça entre colunas | `peca`, `estado` (§2.2b), `evidencia` (§2.3) | fluxo de peças, selos de evidência |
| `deploy` | deploy real registrado | `estado` (`SUCCESS`/`sucesso`/`ok` = sucesso), `texto`, `evidencia` | DORA (*DevOps Research and Assessment*): frequência e taxa de falha |
| `incidente` | incidente em produção | `peca`, `texto` | DORA: taxa de falha, tempo de restauração |
| `recuperacao` | fim de um incidente | `peca`, `texto` | DORA: tempo de restauração |
| `nota` | observação livre, sem efeito em métrica | `texto` | relatório de lote |

### 2.2 Vocabulários fechados (`server.py:24-26`)

- **(a) `ESTADOS_SESSAO`**: `trabalhando` · `esperando` · `sem tarefa` · `bloqueado`.
- **(b) `ESTADOS_PECA`** (ordem do fluxo): `spec` → `red` → `entregue` → `suites aceitas` →
  `aprovada as cegas` → `integrada` → `em producao`.

`valida_evento` recusa `status` fora de (a) e `peca` fora de (b).

### 2.3 Evidência exigida por estado (`EVIDENCIA_EXIGIDA`, `server.py:27-33`)

"Sem prova não muda de coluna." `evidencia` é JSON; cada chave abaixo tem de existir e ser
não-vazia. Faltou uma, o registro é recusado (`ValueError` → HTTP 422 / MCP `isError` / CLI
exit 2) e **nenhuma linha é inserida**.

| Estado-alvo | Chaves obrigatórias | Significado |
|---|---|---|
| `spec`, `red` | — | entrada no fluxo; sem prova exigida |
| `entregue` | `hash` | commit entregue |
| `suites aceitas` | `hash`, `runner2` | segundo runner executou as suítes |
| `aprovada as cegas` | `hash`, `runner2`, `runner2_por`, `par_montado_por`, `descricao_factual` | `runner2_por` nunca é o autor (regra de 02/10) |
| `integrada` | `hash`, `merge` | commit de merge |
| `em producao` | `hash`, `deploy` | deploy registrado — merge **não** vale |

## 3. Tabelas de projeção (reconstruídas a cada ingestão)

| Tabela | Chave | Fonte (arquivo do projeto) | Serve a |
|---|---|---|---|
| `meta` | `chave` | `projeto.json`, hora da ingestão | `/api/meta` |
| `sessoes` | `nome` | arquivos de papel de cada sessão | board, `estado-ia` (`papel`, `proximo`, `ultimo_hash`) |
| `commits` | `(repo, hash)` | `git log` dos repositórios listados | DORA, `entregas` |
| `entregas` | `(repo, hash)` | merges em `commits` | DORA como `proxy_entregas_por_repo` (rotulado proxy) |
| `decisoes` | `(origem, id)` | índice de decisões | `/api/decisoes`, `estado-ia` |
| `adrs` | `arquivo` | `docs/adr/` | `/api/decisoes` |
| `desvios` | `n` | registro de desvios da retro | `/api/qualidade`, `estado-ia` |
| `barra_execucoes` | `pasta` | voltas da barra | `/api/qualidade`, relatório de lote |
| `defeitos` | `(volta, id)` | defeitos por volta | `/api/qualidade` |
| `glossario` | — | linguagem ubíqua do projeto | tela "Linguagem ubíqua" |
| `documentos` | `caminho` | `mtime` e linhas dos documentos listados | `/api/documentos` (idade) |
| `specs` | `(repo, numero, slug)` | `specs/*/` (tasks feitas, tem plan, tem qa) | `/api/specs` |
| `roadmap` | `ordem` | `docs/roadmap.md` | `/api/roadmap` |
| `worktrees` | `(repo, caminho)` | `git worktree list`, upstream, sujeira | `/api/higiene` (lista **para aprovação**) |
| `branches_risco` | `(repo, branch)` | branches com upstream em `main` | `/api/higiene`, `estado-ia.riscos_git` |
| `fases` | `n` | linha do tempo de fases por rodada | `/api/tempo` |

`ingest_log (id, ts, duracao_ms, contagem)` guarda uma linha por ingestão — fato, não projeção.

## 4. Relações

- `eventos.sessao` ↔ `sessoes.nome` (junção por nome, sem chave estrangeira — a sessão pode
  registrar status antes de ter arquivo de papel).
- `eventos.peca` agrupa a linha do tempo de uma peça; a coluna atual é o **último** evento
  `peca` por `peca`, ordenado por `ts`.
- `eventos.tipo='deploy'` é a **única** fonte do DORA de deploy; `entregas` entra só como proxy.
- `commits` → `entregas` (merge = entrega; `lead_h_mediana` calculado dos pais).

## 5. Invariantes que os testes provam (`painel/tests/test_painel.py`)

| Invariante | Teste |
|---|---|
| `UPDATE`/`DELETE` em `eventos` abortam | `test_eventos_recusam_update_e_delete` |
| reingestão preserva `eventos` e é idempotente | `test_reingestao_preserva_eventos_e_e_idempotente` |
| peça sem evidência exigida é recusada | `test_peca_sem_evidencia_e_recusada` (cobre `valida_evento`; a CLI fica para o 072) |
| status só com vocabulário fechado e `autor` | `test_status_so_com_vocabulario_fechado_e_autor` |
| DORA não conta merge como deploy | `test_dora_nao_conta_merge_como_deploy` |
| ingestão nunca abre `.env`/backups, nunca escreve no projeto, nunca guarda segredo/IP | `test_ingestao_nunca_abre_env_nem_backups`, `test_ler_recusa_caminho_proibido`, `test_ingestao_nunca_escreve_nos_arquivos`, `test_sqlite_sem_segredo_nem_ip` |
| branch com upstream em `main` é detectada | `test_detecta_branch_com_upstream_na_main` |

## 6. Limites

- `--ts` do `registrar.py` permite carimbo informado pelo autor (dívida do ciclo 072).
- Sem evento registrado, o painel mostra "sem registro"/"—": é desenho, nunca inventa número.
- O schema não tem versão; uma mudança nas derivadas é absorvida pela reingestão, uma mudança
  em `eventos` exigiria migração — não há nenhuma no v0.
