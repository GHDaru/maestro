# Confronto e decisão do que entra — as 26 funcionalidades (ciclo 073, rodada 2, passo 2)

> A matriz de decisão da área administrativa do Maestro: para cada uma das **26 funcionalidades**
> da tabela fixa (a mesma de `pesquisa/plataformas.md`), a **melhor referência** entre as 25
> plataformas, o **estado no Maestro** (herdado de `confronto/inventario-maestro.md`) e a
> **decisão** — `ENTRA`, `NÃO PRECISA` ou `DEPOIS`. Cruza os dois insumos já revisados e aceitos.

- **Data**: 2026-10-25 · **Ciclo**: 073 (área administrativa) · **Rodada**: 2 (confronto) · **Passo**: 2 (decisão)
- **Autor**: Worker03 · **Insumos**: `pesquisa/plataformas.md` (matriz 25×26, notação normalizada) + `confronto/inventario-maestro.md` (estado do Maestro, `tem 8 · parcial 16 · não tem 2`)
- **Prioridade do regente**: INTERCOMUNICAÇÃO decide primeiro — é onde o mercado é vazio (caixa de entrada e livro de mensagens com **0 `sim` em 25**) e onde o Maestro já opera à mão.

## Como cada linha foi decidida (as três regras)

1. **Fonte obrigatória para `ENTRA`** — ou uma plataforma citada (com a ficha da coluna) **ou** um
   requisito do método citado (princípio, ADR — *Architecture Decision Record* — ou `ux-design`).
   Nada entra por memória.
2. **Célula `—` não é base.** `—` significa "nenhuma fonte encontrada" (não pesquisado), **nunca**
   "não existe". Nenhuma linha decide `ENTRA` sobre uma célula `—`: onde o mercado é vazio (a
   prioridade), o `ENTRA` se apoia no **requisito do método**, e a plataforma citada é só a melhor
   `parcial` — declarada como tal.
3. **YAGNI** (*You Aren't Gonna Need It*): o que o Maestro já cobre por inteiro (`tem`) **não se
   reconstrói** (`NÃO PRECISA`); o que contraria o método também não (`fora do método`); o que é
   lacuna real mas sem caso hoje fica `DEPOIS`, com o gatilho que o traz de volta.

**Os três juízes (rodada 4)** — o bar dá nota 0 a 10 por peça, e só passa com os três em 9 ou mais:
**(1) controle**, **(2) administração e gerenciamento de agentes**, **(3) intercomunicabilidade**.
Cada `ENTRA` declara quais juízes serve.

---

## A tabela de decisão (26 × {referência, estado, lacuna, decisão})

### CONTROLE (6)

| Funcionalidade | Melhor referência (ficha) | Estado no Maestro | Lacuna | Decisão |
|---|---|---|---|---|
| subir/derrubar sessão ou agente | Claude Code — sessão de ponta a ponta (`claude-code.md`) | **parcial** — só **subir** (`scripts/multi-session.py:140`); derrubar fora de escopo (`specs/072-…/spec.md:229`) | **derrubar**; e o ciclo "sessão de agente" como objeto nomeado | **ENTRA** |
| pausar | Windmill (`windmill.md`) — 3 `sim` em 25 | **não tem** (`não encontrado`, inventário §CONTROLE) | suspender sem perder o fio | **DEPOIS** |
| retomar | Claude Code (`claude-code.md`) | **não tem** — o `--resume` do lançador reabre janelas, não o estado (`multi-session.py:19`) | retomar o estado do trabalho | **DEPOIS** |
| limites de orçamento e de taxa | OpenAI Platform — limite de gasto devolve 429 (`openai-platform.md`) | **parcial** — orçamento declarado (`operating-model.md:118-120`), teto 40% (`decisoes.jsonl:172`); **taxa não existe** | limite **executável** por sessão/projeto | **ENTRA** |
| políticas allow/deny/ask | Agent 365 — plano de controle (`agent-365.md`) | **parcial** — declarado (Princípio III, `principles.md:37`); só o `deny` roda (`hooks/guard-immutables.py:149`) | `allow`/`ask` **executáveis** | **ENTRA** |
| aprovação humana | LangSmith/LangGraph — *human-in-the-loop* (`langsmith-langgraph.md`) | **tem** — `operating-model.md:200`, `:186-198`; ADR 0026; `painel/regencia/fila.py:60` | — | **NÃO PRECISA** |

### ADMINISTRAÇÃO (6)

| Funcionalidade | Melhor referência (ficha) | Estado no Maestro | Lacuna | Decisão |
|---|---|---|---|---|
| cadastro de agentes | Portkey — Agent Registry (`portkey.md`) | **tem** — `docs/agents/README.md:14-40` (13 executáveis); `scripts/check-agents.sh` | — | **NÃO PRECISA** |
| papéis e permissões RBAC | LiteLLM — 5 papéis (`litellm.md`) | **parcial** — RACI (`operating-model.md:67-93`); RBAC é termo de glossário (`glossary.md:13`) | **motor** RBAC — mas a autorização vive **fora** do modelo | **NÃO PRECISA** |
| cadastro de skills/ferramentas/modelos | LiteLLM — *Skills Registry* (`litellm.md`) | **parcial** — skills sim (`skills/<nome>/SKILL.md`); **modelos não** (escolhidos por sessão, `multi-session.py:91-92`) | registro de **modelos** | **ENTRA** |
| chaves e segredos | LiteLLM — backends Vault/Azure/AWS (`litellm.md`) | **parcial** — política: token fora do repo (`decisoes.jsonl:155`); **sem cofre nem gate de varredura** | cofre / gate de segredos | **DEPOIS** |
| configuração por projeto | Portainer CE — configuração por projeto (`portainer-ce.md`) | **tem** — `scripts/install-maestro.sh:492-526`; `boundary.json` (ADR 0018) | — | **NÃO PRECISA** |
| auditoria | Windmill — *audit logs* (`windmill.md`) | **tem** — `scripts/record-decision.sh:46-50` + imutabilidade `hooks/guard-immutables.py:44-49`; `check-adr.sh` | — | **NÃO PRECISA** |

### GERENCIAMENTO (8)

| Funcionalidade | Melhor referência (ficha) | Estado no Maestro | Lacuna | Decisão |
|---|---|---|---|---|
| lista de agentes vivos com estado | Claude Code — lista por estado (`claude-code.md`) | **parcial** — read-model do painel (`painel/server.py:60,27`); não por detecção de processo | **detecção** de processo vivo (não *heartbeat*) | **ENTRA** |
| tarefa aberta | Claude Code (`claude-code.md`) | **parcial** — "one active task per session" (`task-ledger.md:185`); kanban por portão (`server.py:369`) | objeto "tarefa aberta" **por agente** | **ENTRA** |
| última atividade | n8n — *Insights* (`n8n.md`) | **tem** — `painel/server.py:77,82`; `index.html:311` | — | **NÃO PRECISA** |
| consumo por agente/sessão/modelo | Copilot Studio — o mais completo (`copilot-studio.md`) | **parcial** — por sessão (`painel/custo.py`) e por modelo (`task-ledger.md:118,127`); **por agente não** | consumo **por agente** | **ENTRA** |
| custo | LiteLLM — custo por agente A2A (`litellm.md`) | **tem** — `cost_usd` (`task-ledger.md:129`); `report-tasks.py:254-261` | — | **NÃO PRECISA** |
| filas e workers | Windmill — *queues*/*worker groups* (`windmill.md`) | **tem** — fila de decisões (`painel/regencia/fila.py:95`); *outbox* SQLite (`fila_outbox.py:109`) | — | **NÃO PRECISA** |
| rastro/replay de sessão | Temporal Web UI — History em 4 formatos (`temporal-web-ui.md`) | **parcial** — trilha por chamado (`painel/chamados.py:357`); **replay não** | **replay** de sessão | **DEPOIS** |
| alertas | Dagster — o mais forte (`dagster.md`) | **parcial** — gates que falham e avisos inline (`check-retro.sh:61-66`, `session-state.sh:52-59`) | **subsistema** de alerta/notificação | **DEPOIS** |

### INTERCOMUNICAÇÃO (6) — **decide primeiro** (prioridade do regente)

| Funcionalidade | Melhor referência (ficha) | Estado no Maestro | Lacuna | Decisão |
|---|---|---|---|---|
| mensagem entre agentes | CrewAI AMP (`crewai-amp.md`) | **tem** — protocolo `[[TASK]]`/`[[DONE]]` (`task-ledger.md:28-31`); *outbox* (`fila_outbox.py:121`) | superfície **nomeada** (o método prefere artefato a chat, `comunicacao.md:6`) | **ENTRA** |
| protocolos (A2A, MCP) | LiteLLM — A2A real (`litellm.md`) | **parcial** — MCP implementado (`painel/mcp_painel.py:2`; `glossary.md:34`); **A2A só nomeado** (`specs/066-…/ux-design.md:81`) | **A2A** construído | **ENTRA** |
| caixa de entrada | Maestri canvas — `parcial` (melhor; **0 `sim` em 25**) | **parcial** — *drain* do outbox (`fila_outbox.py:140`), sem feição/rota **nomeada** | caixa de entrada nomeada | **ENTRA** |
| roteamento por nome/ref | Windmill — roteamento por *tag* (`windmill.md`) | **parcial** — destinatário por nome livre (`server.py:469`, `norm_sessao` `ingest.py:199`) | tabela de resolução de nome | **ENTRA** |
| livro de mensagens | Maestri canvas — `parcial` (melhor; **0 `sim` em 25**) | **parcial** — registros append-only (`ingest.py:66,78`; `tarefas.jsonl`), sem livro unificado | livro de mensagens unificado | **ENTRA** |
| colisão de nomes | Kiro Crew / Windmill — `sim` (`kiro-crew.md`, `windmill.md`) | **parcial** — incidente real (`specs/066-…/qa-report.md:35`); guarda de ids (`fila.py:52-56`) | controle de colisão de **nomes** | **ENTRA** |

---

## Detalhe das decisões

### ENTRA — 13 (nome na linguagem ubíqua + juízes + fonte)

| # | Funcionalidade | Nome na linguagem ubíqua | Juízes (rodada 4) | Fonte |
|---|---|---|---|---|
| 1 | subir/derrubar sessão ou agente | **sessão de agente** *(novo)* | Controle · Administração/Gerenciamento | método: o "subir" existe (`multi-session.py:140`) e o derrubar é escopo declarado (`specs/072-…/spec.md:229`); plataforma: Claude Code:66 `sim`/Windmill:66 `parcial` |
| 4 | limites de orçamento e de taxa | **limite de orçamento** *(novo)* | Controle | método: `operating-model.md:118-120` ("fixed time and variable scope") + teto de 40% (`decisoes.jsonl:172`); plataforma: OpenAI Platform:69 `sim` ("limite de gasto devolve 429") |
| 5 | políticas allow/deny/ask | **política declarativa (allow/deny/ask)** — reusa **OPA** (*Open Policy Agent*, `glossary.md:36*) | Controle · Administração/Gerenciamento | método: Princípio III (`principles.md:37`) + `deny` que já roda (`guard-immutables.py:149`); plataforma: Agent 365:70 `sim` |
| 9 | cadastro de skills/ferramentas/modelos | **catálogo de skills/ferramentas/modelos** *(novo)* | Administração/Gerenciamento | método: `skills/<nome>/SKILL.md` + catálogo gerado (`install-maestro.sh:99-104`); plataforma: LiteLLM:74 `sim` (*Skills Registry*) |
| 13 | lista de agentes vivos com estado | **estado do agente vivo** *(novo)* | Administração/Gerenciamento · Controle | método: read-model existe (`painel/server.py:60,27`), falta detecção; plataforma: Claude Code:78 `sim` |
| 14 | tarefa aberta | **tarefa aberta** *(novo; ligado a **Task ledger**, `glossary.md:28`)* | Administração/Gerenciamento | método: `task-ledger.md:185` ("one active task per session"); plataforma: Claude Code:79 `sim` |
| 16 | consumo por agente/sessão/modelo | **consumo por agente** *(novo; extensão de **Custo por sessão**, `glossary.md:73`)* | Administração/Gerenciamento | método: por sessão (`painel/custo.py`) e por modelo (`task-ledger.md:118,127`); plataforma: Copilot Studio:81 `sim` |
| 21 | mensagem entre agentes | **mensagem entre agentes** *(novo)* | Intercomunicabilidade | método: `[[TASK]]`/`[[DONE]]` (`task-ledger.md:28-31`) + *outbox* (`fila_outbox.py:121`); plataforma: CrewAI AMP:86 `sim` (mas é delegação, não par a par) |
| 22 | protocolos (A2A, MCP) | **protocolo de intercomunicação** — **MCP** no glossário (`glossary.md:34`), **A2A** a expandir | Intercomunicabilidade | método: MCP implementado (`painel/mcp_painel.py:2`); plataforma: LiteLLM:87 `sim` (A2A real) |
| 23 | caixa de entrada | **caixa de entrada** *(novo)* | Intercomunicabilidade | método: *drain* do *outbox* (`fila_outbox.py:140`), sem nome; **mercado: 0 `sim` em 25** (melhor: Maestri canvas:88 `parcial`) |
| 24 | roteamento por nome/ref | **roteamento por nome/ref** *(novo)* | Intercomunicabilidade | método: `server.py:469` (`contatos()`), `ingest.py:199` (`norm_sessao`); plataforma: Windmill:89 `sim` |
| 25 | livro de mensagens | **livro de mensagens** *(novo; análogo a **Task ledger**)* | Intercomunicabilidade | método: registros append-only (`ingest.py:66,78`); **mercado: 0 `sim` em 25** (melhor: Maestri canvas:90 `parcial`) |
| 26 | colisão de nomes | **colisão de nomes** *(novo)* | Intercomunicabilidade | método: incidente real (`specs/066-…/qa-report.md:35`); plataforma: Kiro Crew:91 `sim` |

### NÃO PRECISA — 8 (com o motivo)

| Funcionalidade | Motivo |
|---|---|
| aprovação humana | **já coberto** — é o núcleo do método (Princípio II/III: gates humanos não delegáveis; `operating-model.md:200`, ADR 0026). Reconstruir seria duplicar função já servida (Princípio VI). |
| cadastro de agentes | **já coberto** — 13 executáveis com invariantes que os verificam (`check-agents.sh`, `check-roles.sh`); é registro, não processo vivo. Exibir já é coberto por *estado do agente vivo*. |
| papéis e permissões RBAC | **fora do método** — papéis existem (RACI), mas a autorização vive **fora** do modelo (Princípio III; `ABAC`/`RBAC` no glossário, `:12-13`). Não se constrói motor RBAC dentro da área administrativa. |
| configuração por projeto | **já coberto** — instalador grava `install-options.json`/`manifest.tsv` e a fronteira é o `boundary.json` (ADR 0018). |
| auditoria | **já coberto** — índice append-only imutável (`record-decision.sh` + `guard-immutables.py`), com conferência por `check-adr.sh`. |
| última atividade | **já coberto** — o painel já mostra `idade_min` e o histórico de status (`server.py:77,82`). |
| custo | **já coberto** — `cost_usd` no livro de ponto e o relatório `report-tasks.py` ("how much am I spending?"). O que falta (por agente) entra em *consumo por agente*. |
| filas e workers | **já coberto** — fila de decisões (`regencia/fila.py:95`) + *outbox* SQLite (`fila_outbox.py:109`). |

### DEPOIS — 5 (com o gatilho)

| Funcionalidade | Gatilho que a traz de volta |
|---|---|
| pausar | quando o **teto de orçamento** precisar suspender uma sessão sem perdê-la (ou com ≥ N sessões simultâneas). Hoje o mercado também quase não tem (3 `sim` em 25) — não há de onde copiar. |
| retomar | **acoplado a pausar** (retomar só existe depois de pausar). Mesmo gatilho. |
| chaves e segredos | quando houver **>1 segredo por projeto** ou a **primeira rotação** que precise ser automatizada (aí o cofre se paga). |
| rastro/replay de sessão | quando uma sessão precisar ser **reproduzida** para diagnosticar — hoje a trilha por chamado basta. |
| alertas | quando o **nº de sessões simultâneas** tornar os gates inline insuficientes (o aviso no início de sessão não escala). |

---

## Totais

| Decisão | Quantas | Funcionalidades |
|---|---|---|
| **ENTRA** | **13** | subir/derrubar · limites de orçamento e de taxa · políticas allow/deny/ask · cadastro de skills/ferramentas/modelos · lista de agentes vivos com estado · tarefa aberta · consumo por agente · mensagem entre agentes · protocolos (A2A, MCP) · caixa de entrada · roteamento por nome/ref · livro de mensagens · colisão de nomes |
| **NÃO PRECISA** | **8** | aprovação humana · cadastro de agentes · papéis e permissões RBAC · configuração por projeto · auditoria · última atividade · custo · filas e workers |
| **DEPOIS** | **5** | pausar · retomar · chaves e segredos · rastro/replay de sessão · alertas |
| **Total** | **26** | — |

Por grupo: INTERCOMUNICAÇÃO **6 ENTRA de 6** (a prioridade — nenhum `NÃO PRECISA`, nenhum `DEPOIS`);
CONTROLE **3 ENTRA · 1 NÃO PRECISA · 2 DEPOIS**; ADMINISTRAÇÃO **1 ENTRA de 6** (o grupo mais
coberto); GERENCIAMENTO **3 ENTRA de 8**.

## Glossário proposto (termos novos — a ratificar)

Nenhum nasce "com a sigla nua": cada um entra aqui com a definição curta; quem tem termo existente
no glossário **reusa** o existente.

| Termo proposto | Definição curta | Observação |
|---|---|---|
| **sessão de agente** | Uma execução de agente que o humano sobe, acompanha e derruba; a unidade de administração. | novo (hoje "sessão" só existe implícito no lançador) |
| **estado do agente vivo** | O estado corrente de uma sessão (trabalhando/esperando/sem tarefa/bloqueado) com detecção de processo, não só *heartbeat*. | novo (reusa os estados de `server.py:27`) |
| **tarefa aberta** | A tarefa ativa **por agente** — o que ele está fazendo agora, com o `start` sem `stop`. | novo; análogo ao **Task ledger** |
| **consumo por agente** | Tokens por agente (não só por sessão/modelo). | novo; extensão de **Custo por sessão** |
| **limite de orçamento** | O teto de consumo de uma sessão/projeto, **executável** (não só declarado). | novo |
| **catálogo de skills/ferramentas/modelos** | O registro consultável de skills, ferramentas e **modelos** por projeto. | novo (skills já existem em pasta) |
| **mensagem entre agentes** | Troca endereçada entre sessões, por artefato/*outbox*, não por chat. | novo; ligado a **Outbox** |
| **protocolo de intercomunicação** | O protocolo pelo qual agentes expõem e consomem ferramentas (**MCP**) e conversam entre pares (**A2A**). | **MCP** já no glossário; **A2A** entra expandido |
| **caixa de entrada** | A visão nomeada do que chegou para uma sessão e ainda não foi lido/*drenado*. | novo — **termo do regente, mercado 0 `sim`** |
| **livro de mensagens** | O registro append-only unificado das mensagens entre sessões. | novo; análogo ao **Task ledger** |
| **roteamento por nome/ref** | Endereçar uma mensagem/tarefa a uma sessão por nome ou referência, com tabela de resolução. | novo |
| **colisão de nomes** | Duas sessões/agentes/skills com o mesmo nome; a regra que a evita. | novo (hoje só há regra para *ids*) |

**Reusados (já no glossário, não são termos novos):** **OPA** (*Open Policy Agent*, política
`allow/deny/ask`), **MCP**, **RBAC**, **Outbox**, **Task ledger**, **Custo por sessão**,
**Chamado**, **Painel de regência**.

## Limites desta decisão (declarados)

- **Nada construído**: esta é a rodada 2 (decisão documental); o software nasce — se nascer — das
  rodadas 3–4. Nenhuma arquitetura foi fixada aqui.
- **A prioridade do regente foi honrada**: INTERCOMUNICAÇÃO decidiu primeiro e levou 6 `ENTRA`.
- **Nenhum `ENTRA` se apoia em célula `—`** (regra 2): onde o mercado é vazio, a fonte é o
  **requisito do método**, e a plataforma citada é a melhor `parcial`, declarada.
- **Força do veredito herdada**: os 2 `não tem` do inventário são `não encontrado` (piso, não
  prova) — por isso `pausar`/`retomar` ficam em `DEPOIS` (gatilho declarado), não em `NÃO PRECISA`.
- **Siglas expandidas na primeira ocorrência** (Princípio VIII): RBAC (*Role-Based Access Control*),
  RACI (*Responsible, Accountable, Consulted, Informed*), MCP (*Model Context Protocol*), A2A
  (*Agent-to-Agent*), ADR (*Architecture Decision Record*), OPA (*Open Policy Agent*), YAGNI
  (*You Aren't Gonna Need It*), DDD (*Domain-Driven Design*).
