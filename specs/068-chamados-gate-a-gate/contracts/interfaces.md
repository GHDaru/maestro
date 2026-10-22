# Contracts 068 — Interfaces dos chamados gate a gate

> Lido do código em `120a32c`: `painel/server.py` (handler `do_GET`, linhas 429-440),
> `painel/chamados.py` (`em_cache`, 322-330; `trilha`, 347-420; `le_chamados`, 236-294),
> `painel/custo.py` (`indexa`, `janela`, bloco `__main__`), `painel/projetos/exemplo.json`,
> `painel/projetos/chamados-manuais-exemplo.json`, `painel/workflow-chamado.bpmn` e
> `.maestro/controle/git-hooks/pre-commit`. Os contratos do 066 (`/api/board`, eventos, MCP,
> `registrar.py`) continuam valendo; aqui só o que o 068 acrescenta. Formas em `data-model.md`.
>
> Siglas: HTTP (*Hypertext Transfer Protocol*) · JSON (*JavaScript Object Notation*) · CLI
> (*command-line interface*) · BPMN (*Business Process Model and Notation*, notação de
> modelagem de processos) · XML (*Extensible Markup Language*) · IA (*inteligência
> artificial*) · ISO 8601 (data e hora com fuso).

## 1. HTTP — três rotas novas em `painel/server.py` (só `GET`, só `127.0.0.1`)

Respostas JSON com `Content-Type: application/json; charset=utf-8` e `Cache-Control:
no-store`, como no 066. Nenhuma rota escreve no projeto nem no SQLite do painel.

### 1.1 `GET /api/chamados[?atualizar=1]` (`server.py:439`)

Devolve o **último resultado em cache** e dispara a varredura do git em thread quando o cache
tem mais de 120 s (ou sempre, com `atualizar`). A primeira chamada volta vazia com
`pronto: false`; a tela mostra "atualizando" e repete.

```json
{
  "pronto": true, "atualizando": false, "erro": "",
  "gates": [{"gate": "abertura", "nome": "Abertura", "dono": "Office"}, "... 12 entradas"],
  "chamados": [{"id": "0042-marco-trava", "titulo": "...", "tipo": "bug", "onde": "G3",
                "estado_atual": "run", "com_quem": "Críticos e runner2", "falta": ["runner2 0/0 por não autor @ a1b2c3d"],
                "gates": ["... 12 objetos Gate com itens"], "pendencias": [], "desvios": 1,
                "registro": "padrão", "commit": "a1b2c3d", "commit_em": "2026-10-05T21:00:00-03:00"}],
  "gerado_em": "2026-10-20T10:00:00-03:00"
}
```

Contrato: `gates` e `chamados` existem **sempre** (lista vazia antes da primeira leitura);
`erro` não vazio significa que a última varredura falhou e `chamados` é o resultado anterior.
Chamados manuais vêm com `registro: "manual"` e sem `gates` calculados.

### 1.2 `GET /api/chamados/<id>/trilha` (`server.py:437`)

`<id>` é o terceiro segmento do caminho (`u.path.split("/")[3]`), decodificado pela tela com
`encodeURIComponent`. Devolve `{id, titulo, onde, eventos[], metricas{}, apelidos_usados[]}`
(`data-model.md` §4). Se o chamado ainda não foi lido pela varredura:

```json
{"erro": "chamado ainda não lido (abra a aba Chamados e espere a leitura do git)"}
```

Contrato: `metricas.nota` existe **sempre** que há métricas e diz que o custo é estimativa;
`tokens` em cada evento é opcional (só quando `custo.db` tem a janela). A tela oferece o
link "JSON para IA" para esta rota — ela é a entrada de uma sessão de IA para "onde está o
chamado e o que faltou".

### 1.3 `GET /workflow-chamado.bpmn` (`server.py:429`)

Devolve o arquivo `painel/workflow-chamado.bpmn` como `application/xml; charset=utf-8`. É o
que o visualizador da aba lê (`index.html:730`) e o que abre no bpmn.io ou no Camunda Modeler.

## 2. CLI — `python painel/custo.py <projeto.json> [<custo.db>]`

| Posição | Valor | Obrigatório |
|---|---|---|
| `projeto` | caminho de `painel/projetos/<nome>.json` (lido por `ingest.carrega_cfg`) | sim |
| `db` | caminho do índice; padrão `painel/dados/custo.db` | não |

Saída: uma linha JSON `{"arquivos_lidos": N, "mensagens_novas": M}` em stdout e **exit 0**.
Lê `~/.claude/projects/<pasta>/*.jsonl` das pastas cujo nome **contém** algum item de
`custo_pastas` (substring — ver §5), a partir do `offset` gravado; segunda corrida sem
transcript novo → `arquivos_lidos` menor (zero se nada mudou). Grava **só** em `db`. O
servidor chama `custo.indexa` a cada varredura de chamados; falha no índice não derruba a
varredura (a trilha fica sem tokens).

Porta de consulta: `custo.janela(db, nome, ini, fim)` → `{turnos, entrada, saida, cache_lido,
cache_escrito}` da sessão `nome` (canônico) entre dois instantes UTC `YYYY-MM-DDTHH:MM`; `{}`
se o banco não existe.

## 3. Configuração — chaves novas em `painel/projetos/<nome>.json`

| Chave | Forma | Efeito |
|---|---|---|
| `chamados` | lista de `{repo, pasta, dias}` — `repo` é o nome em `repos[]`, `pasta` padrão `specs`, `dias` padrão 14 | pastas `specs/<id>/` com `00-chamado.md` tocadas por algum commit (qualquer branch) nos últimos `dias` |
| `chamados_manuais` | caminho (relativo a `raiz` ou absoluto) de um JSON (§4) | chamados digitados, anteriores ao padrão |
| `custo_pastas` | lista de textos; **padrão do código `["180-HINDIANA"]`** (dívida 1 do plano) | filtro das pastas de transcript lidas por `custo.py` |

`exemplo.json` (fixture) aponta para este próprio repositório e para a pasta de transcripts
`C--Users-ghdaru-Documents-010-PROJETOS-410-MAESTRO` pelo nome inteiro.

## 4. JSON de chamados manuais (`chamados-manuais-exemplo.json`)

```json
{"_": "comentário livre",
 "chamados": [{"id": "000-exemplo", "tipo": "bug", "titulo": "...", "aberto_em": "01/10 09:00",
               "escopo": "correcao", "severidade": "baixa", "aberto_por": "Regente", "origem": "exemplo",
               "estado": "G1", "pendente": "", "nota": "..."}]}
```

Contrato: cada entrada recebe `registro: "manual"` ao ser lida; **não passa pelas regras**; é
descartada se existir pasta derivada com o mesmo `id`. O arquivo real do Hindiana (1133 linhas)
**não** vive neste repositório (`decisao-066-daru-20-10`).

## 5. O que atravessa a fronteira

| De → para | Contrato |
|---|---|
| git do projeto → domínio | `chamados._git(repo, *args)` — `git log --all --since … --name-only` e `git show <commit>:<caminho>`; argumentos em lista (nunca shell); retorno `None` em erro |
| `~/.claude/projects/` → `custo.db` | `custo.indexa(cfg, db)` — lê só `*.jsonl` das pastas filtradas, só do offset em diante, grava só contagens. **Ambiguidade registrada no plano (decisão 8)**: o filtro é por substring; recomendação para ciclo posterior é nome inteiro e chave obrigatória |
| `custo.db` → trilha | `custo.janela` (§2) |
| sessão de IA → painel | `GET /api/chamados/<id>/trilha` — leitura, sem efeito |
| tela → painel | as três rotas de §1; `index.html` não tem outra fonte |
| git → veredito | `.maestro/controle/git-hooks/pre-commit` chama `python veredito_hook.py --pre-commit` (contrato do hook: 066 `contracts/interfaces.md` §4); independente do painel |

## 6. BPMN como contrato do fluxo (`painel/workflow-chamado.bpmn`)

`bpmn:process id="Proc_chamado"`, não executável (`isExecutable="false"`): 12 raias (cliente,
dono do produto, Office, especificação, …) e 10 `exclusiveGateway` com `id` igual ao gate (G0–G7, G9, GD); o G8 é `bpmn:userTask id="T_ordem"` (linha 329), porque a ordem de produção é tarefa humana, não decisão automática
(`G0`, `GD`, `G1` … `G9`). Contrato com `chamados.GATES`: **os mesmos ids** — a DoD do plano
conta 11 gateways e os compara à tabela. O BPMN diz quem faz o quê entre os gates; as tabelas
`PASSA`/`BARRA`/`confere` dizem o que faz um gate passar. Mudar um sem o outro é achado de
retro. Nomes de pessoas nas raias (`Lane_dono`) são o mesmo acoplamento da dívida 1.
