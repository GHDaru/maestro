# Confronto e decisão do que entra — as 26 funcionalidades + 6 acrescentadas (ciclo 073, rodada 2, passo 2; corrigido na rodada 4)

> A matriz de decisão da área administrativa do Maestro: para cada uma das **26 funcionalidades**
> da tabela fixa (a mesma de `pesquisa/plataformas.md`), a **melhor referência** entre as 25
> plataformas, o **estado no Maestro** (herdado de `confronto/inventario-maestro.md`) e a
> **decisão** — `ENTRA`, `NÃO PRECISA` ou `DEPOIS`. Cruza os dois insumos já revisados e aceitos.
>
> **Correção 1 da rodada 4** (decisão da regente, `rodada-4/correcao-1.md`): a linha 4 foi
> **desdobrada** (o orçamento fica `ENTRA`; a taxa passa a `DEPOIS`), a `auditoria` e o `custo`
> passam de `NÃO PRECISA` a **`ENTRA`** — viram **auditoria administrativa** (com `changed_by`) e
> **custo estimado por agente** — e cinco funcionalidades de intercomunicação que o juiz 3 mostrou
> faltarem (recibo de entrega, reentrega, *dead-letter*, *broadcast*/cópia, estabilidade de ref)
> entram como `DEPOIS` com gatilho escrito. O confronto passa a cobrir **32 funcionalidades**
> (26 + 6) e os totais foram refeitos.
>
> **Correção 2 da rodada 4** (decisão da regente, `rodada-4/correcao-2.md`): o **mecanismo de
> execução** do controle sai de `ENTRA` e vira `DEPOIS` com gatilho ("recusar a chamada seguinte" e
> "suspender a sessão" são **o mesmo ponto de execução** — um *hook* que lê o consumo medido, a
> desenhar na raia *infra*), então o **`ENTRA` 4 (limite de orçamento)** fica com **declarar o teto +
> avisar**; o **cadastro de agentes** sobe de `NÃO PRECISA` a **`ENTRA` 16**, como **leitura do
> catálogo de perfis** — os totais passam a **16/5/11 = 32**; a *"mensagem desviada"* sai de `alertas`
> (já tem tela) e as citações a `claude-code.md` foram **revalidadas contra o HEAD**.
>
> **Correção 3 da rodada 4** (decisão do Darú, `rodada-4/correcao-3.md`): fecha a rodada com três
> decisões **de escopo** — nenhuma linha muda de casa e os totais continuam **16/5/11 = 32**; o que
> muda é **o que cada `ENTRA` pede**. **(D1)** a linha "limites de orçamento e de taxa" volta a ficar
> **uma só** na matriz fixa (a tabela de 26 é mantida); o que a distingue é a leitura **por célula** —
> cada `sim`/`parcial` ganha a marca **`corta`** (estourou, a chamada é recusada ou limitada) ou
> **`avisa`** (só notifica), com a ficha da plataforma como fonte, e `avisa?` onde a ficha não
> distingue; é o que `pesquisa/plataformas.md` agora mostra: **12 `corta` · 1 `avisa`** (AgentOps) e
> **3 `avisa?`** (Claude Code, LangSmith/LG, Flowise). **(D2)** a **ferramenta MCP** (*Model Context
> Protocol*) entra como **escopo da política `allow/deny/ask` por agente** — não como tela própria: a
> regra de exemplo mora na tela de políticas (`prototipo/administracao-02-politicas.html`,
> `#regra-ferramenta-mcp`) e cada ferramenta do protocolo aponta de volta para ela. **(D3)** o
> **emissor do aviso de teto** é a **ingestão de consumo do painel** (`painel/custo.py`): ao ingerir,
> ela compara o consumo medido com o **teto** e o **limiar** declarados na Administração e, ao cruzar
> o limiar, **enfileira uma mensagem** na *fila (outbox)* endereçada à sessão dona **e** ao regente
> (`nome · ref · projeto`) — *aviso atrasado, nunca perdido*; o **corte** (recusar, suspender) segue
> em `DEPOIS`. Em uma linha: o **`ENTRA` 4** passa a se ler **"declarar teto + avisar, com emissor
> desenhado"** e o **`ENTRA` 5** ganha a ferramenta MCP como escopo.

- **Data**: 2026-10-25 · **Corrigido em**: 2026-10-27 (correções 2 e 3 da rodada 4) · **Ciclo**: 073 (área administrativa) · **Rodada**: 2 (confronto) · **Passo**: 2 (decisão)
- **Autor**: Worker03 · **Insumos**: `pesquisa/plataformas.md` (matriz 25×26, notação normalizada) + `confronto/inventario-maestro.md` (estado do Maestro, `tem 8 · parcial 16 · não tem 2`)
- **Prioridade do regente**: INTERCOMUNICAÇÃO decide primeiro — é onde **não se encontrou fonte na documentação lida** (caixa de entrada e livro de mensagens com **0 `sim` em 25**, o que é contagem de `—`, não prova de que não exista; `plataformas.md:42,88,90,210-213`) e onde o Maestro já opera à mão.

## Como cada linha foi decidida (as três regras)

1. **Fonte obrigatória para `ENTRA`** — ou uma plataforma citada (com a ficha da coluna) **ou** um
   requisito do método citado (princípio, ADR — *Architecture Decision Record* — ou `ux-design`).
   Nada entra por memória.
2. **Célula `—` não é base.** `—` significa "nenhuma fonte encontrada" (não pesquisado), **nunca**
   "não existe". Nenhuma linha decide `ENTRA` sobre uma célula `—`: onde não se encontrou fonte na
   documentação lida (a prioridade), o `ENTRA` se apoia no **requisito do método**, e a plataforma
   citada é só a melhor `parcial` — declarada como tal. Este documento **não escreve "lacuna de
   mercado"**: escreve **"não encontrado na documentação lida"** (decisão 6 da correção 1).
3. **YAGNI** (*You Aren't Gonna Need It*): o que o Maestro já cobre por inteiro (`tem`) **não se
   reconstrói** (`NÃO PRECISA`); o que contraria o método também não (`fora do método`); o que é
   lacuna real mas sem caso hoje fica `DEPOIS`, com o gatilho que o traz de volta — e o gatilho é
   **escrito** (sem gatilho escrito, `DEPOIS` é `NÃO PRECISA` disfarçado).

**Os três juízes (rodada 4)** — o bar dá nota 0 a 10 por peça, e só passa com os três em 9 ou mais:
**(1) controle**, **(2) administração e gerenciamento de agentes**, **(3) intercomunicabilidade**.
Cada `ENTRA` declara quais juízes serve.

---

## A tabela de decisão (26 × {referência, estado, lacuna, decisão})

### CONTROLE (7)

| Funcionalidade | Melhor referência (ficha) | Estado no Maestro | Lacuna | Decisão |
|---|---|---|---|---|
| subir/derrubar sessão ou agente | Claude Code — sessão de ponta a ponta (`claude-code.md`) | **parcial** — só **subir** (`scripts/multi-session.py:140`); derrubar fora de escopo (`specs/072-…/spec.md:229`) | **derrubar**; e o ciclo "sessão de agente" como objeto nomeado | **ENTRA** |
| pausar | Windmill (`windmill.md`) — 3 `sim` em 25 | **não tem** (`não encontrado`, inventário §CONTROLE) | suspender **sem perder o fio** e **cortar o gasto**: o ponto de execução (decisão 2) | **DEPOIS** |
| retomar | Claude Code — `claude attach <id\|name>`, `claude --resume` (`claude-code.md:61`, `sim`) | **não tem** — o `--resume` do lançador reabre a janela, não o estado (`multi-session.py:19`) | retomar o **estado** do trabalho | **DEPOIS** |
| limites de orçamento | OpenAI Platform — limite de gasto devolve 429 (`openai-platform.md:43`) | **parcial** — orçamento declarado (`operating-model.md:118-120`), teto 40% (`decisoes.jsonl:172`) | **declarar o teto + avisar** (mensagem endereçada ao dono e ao regente); o corte **executável** vira o ponto de execução em `DEPOIS` (decisão 2) | **ENTRA** |
| limite de taxa *(desdobrada da linha 4 — antes "limites de orçamento **e de taxa**", que cortava a taxa em silêncio)* | LiteLLM — `tpm_limit`/`rpm_limit` por projeto (`litellm.md:94`); OpenAI Platform — RPM (*requests per minute*)/TPM (*tokens per minute*) por organização e projeto (`openai-platform.md:43`) | **não tem** (inventário §CONTROLE: "taxa não existe") | teto de **taxa** por sessão/projeto, executável | **DEPOIS** |
| políticas allow/deny/ask | Agent 365 — plano de controle (`agent-365.md`) | **parcial** — declarado (Princípio III, `principles.md:37`); só o `deny` roda (`hooks/guard-immutables.py:149`) | **bloco `permissions` não declarado no repositório** | **ENTRA** |
| aprovação humana | LangSmith/LangGraph — *human-in-the-loop* (`langsmith-langgraph.md`) | **tem** — `operating-model.md:200`, `:186-198`; ADR 0026; `painel/regencia/fila.py:60` | — | **NÃO PRECISA** |

### ADMINISTRAÇÃO (6)

| Funcionalidade | Melhor referência (ficha) | Estado no Maestro | Lacuna | Decisão |
|---|---|---|---|---|
| cadastro de agentes | Portkey — *Agent Registry* (`portkey.md`) | **tem** — `docs/agents/README.md:14-40` (13 executáveis); `scripts/check-agents.sh`; os perfis são **arquivos versionados** (`.claude/agents/*.md`) | — o **cadastro é o arquivo**; a tela **lê** o catálogo de perfis (`ls .claude/agents`) e liga ao roteamento | **ENTRA** |
| papéis e permissões RBAC (*Role-Based Access Control*) | LiteLLM — 5 papéis (`litellm.md`) | **parcial** — RACI (*Responsible, Accountable, Consulted, Informed*) (`operating-model.md:67-93`); RBAC é termo de glossário (`glossary.md:13`) | **motor** RBAC — mas a autorização vive **fora** do modelo | **NÃO PRECISA** |
| cadastro de skills/ferramentas/modelos | LiteLLM — *Skills Registry* (`litellm.md`) | **parcial** — skills sim (`skills/<nome>/SKILL.md`); **modelos não** (escolhidos por sessão, `multi-session.py:91-92`) | registro de **modelos** | **ENTRA** |
| chaves e segredos | LiteLLM — backends Vault/Azure/AWS (`litellm.md`) | **parcial** — política: token fora do repo (`decisoes.jsonl:155`); **sem cofre nem gate de varredura** | cofre / gate de segredos | **DEPOIS** |
| configuração por projeto | Portainer CE — configuração por projeto (`portainer-ce.md`) | **tem** — `scripts/install-maestro.sh:492-526`; `boundary.json` (ADR 0018) | — | **NÃO PRECISA** |
| auditoria administrativa | LiteLLM — *audit logs* com `changed_by` (`litellm.md:95`) | **parcial** — índice append-only imutável (`scripts/record-decision.sh:46-50` + `hooks/guard-immutables.py:44-49`) e conferência (`check-adr.sh`), mas **sem `changed_by` por linha** e **fora da área administrativa** | **quem mudou o quê** na Administração (`changed_by`) | **ENTRA** |

### GERENCIAMENTO (8)

| Funcionalidade | Melhor referência (ficha) | Estado no Maestro | Lacuna | Decisão |
|---|---|---|---|---|
| lista de agentes vivos com estado | Claude Code — lista por estado (`claude-code.md`) | **parcial** — read-model do painel (`painel/server.py:60,27`); não por detecção de processo | **detecção** de processo vivo (não *heartbeat*) | **ENTRA** |
| tarefa aberta | Claude Code (`claude-code.md`) | **parcial** — "one active task per session" (`task-ledger.md:185`); kanban por portão (`server.py:369`) | objeto "tarefa aberta" **por agente** | **ENTRA** |
| última atividade | n8n — *Insights* (`n8n.md`) | **tem** — `painel/server.py:77,82`; `index.html:311` | — | **NÃO PRECISA** |
| consumo por agente/sessão/modelo | Copilot Studio — o mais completo (`copilot-studio.md`) | **parcial** — por sessão (`painel/custo.py`) e por modelo (`task-ledger.md:118,127`); **por agente não** | consumo **por agente** | **ENTRA** |
| custo estimado por agente | LiteLLM — custo por agente A2A (*Agent-to-Agent*) (`litellm.md`) | **parcial** — `cost_usd` (`task-ledger.md:129`) e `report-tasks.py:254-261`, **por sessão e modelo**; **dólar por agente não** | **custo estimado** em dólar **por agente** | **ENTRA** |
| filas e workers | Windmill — *queues*/*worker groups* (`windmill.md`) | **tem** — fila de decisões (`painel/regencia/fila.py:95`); *outbox* SQLite (`fila_outbox.py:109`) | — | **NÃO PRECISA** |
| rastro/replay de sessão | Temporal Web UI — History em 4 formatos (`temporal-web-ui.md`) | **parcial** — trilha por chamado (`painel/chamados.py:357`); **replay não** | **replay** de sessão | **DEPOIS** |
| alertas | Dagster — o mais forte (`dagster.md`) | **parcial** — gates que falham e avisos inline (`check-retro.sh:61-66`, `session-state.sh:52-59`) | **subsistema** de alerta/notificação | **DEPOIS** |

### INTERCOMUNICAÇÃO (6) — **decide primeiro** (prioridade do regente)

| Funcionalidade | Melhor referência (ficha) | Estado no Maestro | Lacuna | Decisão |
|---|---|---|---|---|
| mensagem entre agentes | CrewAI AMP (`crewai-amp.md`) | **tem** — protocolo `[[TASK]]`/`[[DONE]]` (`task-ledger.md:28-31`); *outbox* (`fila_outbox.py:121`) | superfície **nomeada** (o método prefere artefato a chat, `comunicacao.md:6`) | **ENTRA** |
| protocolos (A2A, MCP (*Model Context Protocol*)) | LiteLLM — A2A real (`litellm.md`) | **parcial** — MCP implementado (`painel/mcp_painel.py:2`; `glossary.md:34`); **A2A só nomeado** (`specs/066-…/ux-design.md:81`) | **A2A** construído | **ENTRA** |
| caixa de entrada | Maestri canvas — `parcial` (empatada com Claude Code; melhor por juízo — **0 `sim` em 25**) | **parcial** — *drain* do outbox (`fila_outbox.py:140`), sem feição/rota **nomeada** | caixa de entrada nomeada | **ENTRA** |
| roteamento por nome/ref | Claude Code — `SendMessage` por ID/nome, refs por `ListAgents` (`claude-code.md:82`, `sim`) | **parcial** — destinatário por nome livre (`server.py:479` — `contatos()`, `norm_sessao` `ingest.py:199`) | tabela de resolução de nome | **ENTRA** |
| livro de mensagens | Maestri canvas — `parcial` (empatada de seis; melhor por juízo — **0 `sim` em 25**) | **parcial** — registros append-only (`ingest.py:66,78`; `tarefas.jsonl`), sem livro unificado | livro de mensagens unificado | **ENTRA** |
| colisão de nomes | Kiro Crew `sim` × Claude Code `parcial` — **mesmo critério** (precedência de escopo) (`kiro-crew.md:57`, `claude-code.md:84`) | **parcial** — incidente real (`specs/066-…/qa-report.md:35`); guarda de ids (`fila.py:52-56`) | controle de colisão de **nomes** | **ENTRA** |

**Duas bases corrigidas na correção 1:**

- **Roteamento por nome/ref — Windmill não é a base.** A ficha do Windmill dá `sim` para *"o modelo
  seleciona a ferramenta por nome"* e para "roteamento de jobs por *tag* de worker group"
  (`windmill.md:49,51`) — isso é roteamento de **ferramenta** e de **job**, **não** endereçamento de
  **sessão** por nome/ref. A base passa a ser o Claude Code, que endereça por ID/nome na
  `SendMessage` e exibe refs por `ListAgents` (`claude-code.md:82`).
- **Colisão de nomes — Kiro Crew e Claude Code, com o MESMO critério.** Antes as duas eram julgadas
  com perguntas diferentes. O critério agora é um par explícito: *(i)* a plataforma resolve homônimo
  por **precedência de escopo**? — Kiro Crew **sim** ("workspace agents take precedence"), Claude
  Code **sim** (managed > `--agents` > projeto > usuário > plugin); *(ii)* a plataforma **detecta** a
  colisão? — **nenhuma das duas** (o Claude Code só resolve por precedência). Por isso o Claude Code
  fica `parcial`: mesma resolução, sem detecção (`kiro-crew.md:57`, `claude-code.md:84`).

### ACRESCENTADAS NA CORREÇÃO 1 (5) — `DEPOIS`, com gatilho escrito

Estas não estavam nas 26 da tabela fixa; o juiz 3 (P3/P4) mostrou que faltavam — nem como `DEPOIS`.

| Funcionalidade | Melhor referência (ficha) | Estado no Maestro | Lacuna | Decisão |
|---|---|---|---|---|
| recibo de entrega (*ack*) | não encontrado na documentação lida nas 25 (o mais próximo é o `[[DONE]]` do método, `task-ledger.md:28-31`) | **parcial** — o `[[DONE]]` responde, mas nada confirma que a mensagem **chegou** | entregue-ou-não da mensagem | **DEPOIS** |
| reentrega | não encontrado na documentação lida nas 25 | **não tem** | reenviar o que falhou | **DEPOIS** |
| *dead-letter* (fila das não entregues) | não encontrado na documentação lida nas 25 | **não tem** — o desvio é uma linha marcada no livro | depósito próprio das não entregues | **DEPOIS** |
| *broadcast*/cópia | não encontrado na documentação lida nas 25 | **não tem** — cada `[[TASK]]` tem um destinatário (`task-ledger.md:28-31`) | uma tarefa para N sessões de uma vez | **DEPOIS** |
| estabilidade de ref | não encontrado na documentação lida (o mais próximo: Kiro Crew, *cloud session store* sobrevive à desconexão, `kiro-crew.md:52`) | **não tem** — o ref muda quando a sessão reinicia | ref que sobrevive ao reinício | **DEPOIS** |

---

## Detalhe das decisões

### ENTRA — 16 (nome na linguagem ubíqua + juízes + fonte)

| # | Funcionalidade | Nome na linguagem ubíqua | Juízes (rodada 4) | Fonte |
|---|---|---|---|---|
| 1 | subir/derrubar sessão ou agente | **sessão de agente** *(novo)* | Controle · Administração/Gerenciamento | método: o "subir" existe (`multi-session.py:140`) e o derrubar é escopo declarado (`specs/072-…/spec.md:229`); plataforma: Claude Code:66 `sim`/Windmill:66 `parcial` |
| 4 | limites de orçamento | **limite de orçamento** *(novo)* | Controle | método: `operating-model.md:118-120` ("fixed time and variable scope") + teto de 40% (`decisoes.jsonl:172`); plataforma: OpenAI Platform:43 `sim` ("limite de gasto devolve 429"). **Escopo das correções 2 e 3 (decisões 2 e D3): declarar o teto + avisar, com emissor desenhado** — o **emissor** é a **ingestão de consumo** (`painel/custo.py`): ao cruzar o **limiar**, enfileira na *fila (outbox)* uma mensagem endereçada `nome · ref · projeto` à sessão dona **e** ao regente, com `data-fonte` apontando o módulo (`administracao-03-orcamento.html`, § "Quem emite o aviso"); o **corte executável** (recusar, suspender) é o ponto de execução, em `DEPOIS` |
| 5 | políticas allow/deny/ask | **política declarativa (allow/deny/ask)** — reusa **OPA** (*Open Policy Agent*, `glossary.md:36*) | Controle · Administração/Gerenciamento | método: Princípio III (`principles.md:37`) + `deny` que já roda (`guard-immutables.py:149`); plataforma: Agent 365:70 `sim`. **Escopo da correção 3 (decisão D2): a ferramenta MCP é escopo da política** — a regra de exemplo nomeia o **agente** e a **ferramenta** (`administracao-02-politicas.html`, `#regra-ferramenta-mcp`: `registrar_peca` em `ask` para Worker, `allow` para o regente por delegação, `deny` para sessão de outro projeto), e cada ferramenta do protocolo aponta de volta para ela |
| 7 | cadastro de agentes | **agente (perfil)** *(novo: **perfil** × **sessão**)* | Administração/Gerenciamento | método: os perfis são **arquivos versionados** (`docs/agents/README.md:14-40`, `.claude/agents/*.md`) e os invariantes já os verificam (`scripts/check-agents.sh`); plataforma: Portkey:72 `sim` (*Agent Registry*) |
| 9 | cadastro de skills/ferramentas/modelos | **catálogo de skills/ferramentas/modelos** *(novo)* | Administração/Gerenciamento | método: `skills/<nome>/SKILL.md` + catálogo gerado (`install-maestro.sh:99-104`); plataforma: LiteLLM:74 `sim` (*Skills Registry*) |
| 12 | auditoria administrativa | **auditoria administrativa** *(novo; extensão de **Auditoria**)* | Controle · Administração/Gerenciamento | método: índice append-only imutável (`record-decision.sh:46-50` + `guard-immutables.py:44-49`), mas sem `changed_by`; plataforma: LiteLLM:95 `sim` (*audit logs* com `changed_by`) |
| 13 | lista de agentes vivos com estado | **estado do agente vivo** *(novo)* | Administração/Gerenciamento · Controle | método: read-model existe (`painel/server.py:60,27`), falta detecção; plataforma: Claude Code:78 `sim` |
| 14 | tarefa aberta | **tarefa aberta** *(novo; ligado a **Task ledger**, `glossary.md:28`)* | Administração/Gerenciamento | método: `task-ledger.md:185` ("one active task per session"); plataforma: Claude Code:79 `sim` |
| 16 | consumo por agente/sessão/modelo | **consumo por agente** *(novo; extensão de **Custo por sessão**, `glossary.md:73`)* | Administração/Gerenciamento | método: por sessão (`painel/custo.py`) e por modelo (`task-ledger.md:118,127`); plataforma: Copilot Studio:81 `sim` |
| 17 | custo estimado por agente | **custo estimado por agente** *(novo; extensão de **Custo por sessão**)* | Administração/Gerenciamento · Controle | método: `cost_usd` (`task-ledger.md:129`) e `report-tasks.py:254-261`, por sessão/modelo; plataforma: LiteLLM:93 `sim` (custo por agente A2A). O dólar por agente é **estimado** — derivado da tabela de preços do modelo no catálogo, e marcado "estimado" na tela |
| 21 | mensagem entre agentes | **mensagem entre agentes** *(novo)* | Intercomunicabilidade | método: `[[TASK]]`/`[[DONE]]` (`task-ledger.md:28-31`) + *outbox* (`fila_outbox.py:121`); plataforma: CrewAI AMP:86 `sim` (mas é delegação, não par a par) |
| 22 | protocolos (A2A, MCP) | **protocolo de intercomunicação** — **MCP** no glossário (`glossary.md:34`), **A2A** a expandir | Intercomunicabilidade | método: MCP implementado (`painel/mcp_painel.py:2`); plataforma: LiteLLM:87 `sim` (A2A real) |
| 23 | caixa de entrada | **caixa de entrada** *(novo)* | Intercomunicabilidade | método: *drain* do *outbox* (`fila_outbox.py:140`), sem nome; **não encontrado na documentação lida: 0 `sim` em 25** (melhor: Maestri canvas:88 `parcial`, empatada com Claude Code — melhor por juízo) |
| 24 | roteamento por nome/ref | **roteamento por nome/ref** *(novo)* | Intercomunicabilidade | método: `server.py:479` (`contatos()`), `ingest.py:199` (`norm_sessao`); plataforma: Claude Code:82 `sim` (`SendMessage` por ID/nome) — **não** Windmill, que roteia ferramenta por nome e job por *tag* (`windmill.md:49,51`) |
| 25 | livro de mensagens | **livro de mensagens** *(novo; análogo a **Task ledger**)* | Intercomunicabilidade | método: registros append-only (`ingest.py:66,78`); **não encontrado na documentação lida: 0 `sim` em 25** (melhor: Maestri canvas:90 `parcial`, empatada de seis — melhor por juízo) |
| 26 | colisão de nomes | **colisão de nomes** *(novo)* | Intercomunicabilidade | método: incidente real (`specs/066-…/qa-report.md:35`); plataforma: Kiro Crew:91 e Claude Code:84 — **mesmo critério** (resolvem por precedência de escopo; nenhuma **detecta**) |

### NÃO PRECISA — 5 (com o motivo)

| Funcionalidade | Motivo |
|---|---|
| aprovação humana | **já coberto** — é o núcleo do método (Princípio II/III: gates humanos não delegáveis; `operating-model.md:200`, ADR 0026). Reconstruir seria duplicar função já servida (Princípio VI). |
| papéis e permissões RBAC | **fora do método** — papéis existem (RACI), mas a autorização vive **fora** do modelo (Princípio III; ABAC (*Attribute-Based Access Control*)/RBAC no glossário, `:12-13`). Não se constrói motor RBAC dentro da área administrativa. |
| configuração por projeto | **já coberto** — instalador grava `install-options.json`/`manifest.tsv` e a fronteira é o `boundary.json` (ADR 0018). |
| última atividade | **já coberto** — o painel já mostra `idade_min` e o histórico de status (`server.py:77,82`). |
| filas e workers | **já coberto** — fila de decisões (`regencia/fila.py:95`) + *outbox* SQLite (`fila_outbox.py:109`). |

*(A `auditoria` e o `custo` saíram daqui na correção 1: com `changed_by` e com o dólar por agente,
deixam de ser "já coberto" e viram `ENTRA`. Antes eles eram `NÃO PRECISA` apoiados em **índice de
decisões** e em **tokens** — que não dão ao administrador onde operar; era o achado P3 do juiz 2.)*

*(Na **correção 2** saiu também o **cadastro de agentes**: o argumento de "já coberto, é registro e
não processo vivo" confundia **registro** com **tela**. O cadastro continua sendo o arquivo
versionado, mas a área passa a **ler** o catálogo de perfis (`.claude/agents/*.md`) e a ligá-lo ao
roteamento — vira **`ENTRA` 16**, `agente (perfil)`.)*

### DEPOIS — 11 (com o gatilho escrito)

| Funcionalidade | Gatilho que a traz de volta |
|---|---|
| pausar | quando a **execução do controle** precisar suspender uma sessão **sem perdê-la**: existe um ponto de execução que corta **gasto de modelo** (não só uso de ferramenta) — um *hook* que lê o **consumo medido**, a desenhar na raia *infra* (decisão 2). "Recusar a chamada seguinte" e "suspender a sessão" são **o mesmo mecanismo** — por isso vivem aqui, em `DEPOIS`, e **não** em `ENTRA`: o `ENTRA` 4 pedir o teto **executável** era a circularidade que o juiz apontou, já que só `DEPOIS` desenha o ponto de execução. Justificativa do mercado: **não é vazio** — 3 `sim` em 25 (`windmill.md`), e os outros `—` são "não encontrado na documentação lida"; o que falta é fonte para o **estado suspenso**, não "o mercado não tem". |
| retomar | **acoplado a pausar**. Justificativa corrigida: **existe** no Claude Code (`claude attach <id\|name>`, `claude --resume`; `claude-code.md:61`) e o lançador do Maestro já reabre a janela (`multi-session.py:19`) — o que **não** existe, em nenhuma fonte lida, é retomar o **estado** do trabalho. "Sem fonte", não "o mercado não tem". |
| chaves e segredos | quando houver **>1 segredo por projeto** ou a **primeira rotação** que precise ser automatizada (aí o cofre se paga). |
| limite de taxa | quando a taxa passar a ser medida: é o **mesmo ponto de execução** do `DEPOIS` **pausar** (o *hook* que lê o consumo medido) que a torna necessária; hoje o Maestro não mede taxa, e a linha 4 a cortava em silêncio. |
| rastro/replay de sessão | quando uma sessão precisar ser **reproduzida** para diagnosticar — hoje a trilha por chamado basta. |
| recibo de entrega (*ack*) | quando a entrega tiver de ser **provada sem inspeção manual**: hoje o livro mostra pretendido × real, mas ninguém confirma o recebimento. |
| reentrega | quando a **primeira falha de entrega** deixar de ser visível a olho — hoje a linha desviada aparece no livro, mas não há retentativa. |
| *dead-letter* | quando o **volume de não entregues** exigir um depósito próprio — hoje o desvio é uma linha marcada no livro. |
| *broadcast*/cópia | quando uma mensagem/tarefa precisar ir a **mais de uma sessão de uma vez** — hoje cada `[[TASK]]` tem um destinatário (`task-ledger.md:28-31`). |
| estabilidade de ref | quando uma mensagem endereçada tiver de **sobreviver ao reinício** — hoje o ref muda (é o ciclo de vida do ref, achado P4 do juiz 3); depende de **colisão de endereço** (mapa § 7). |
| alertas | quando o **nº de sessões simultâneas** tornar os gates inline insuficientes (o aviso no início de sessão não escala) — a peça é a **notificação ativa** (empurra o alerta, em vez de esperar a sessão ler no início). A *"mensagem desviada"* **sai daqui** (decisão 8): já tem tela na Mensageria — o livro marca a linha desviada — e o `ux-design` do ciclo 066 já a pedia (`ux-design.md:79`). |

---

## Totais

| Decisão | Quantas | Funcionalidades |
|---|---|---|
| **ENTRA** | **16** | subir/derrubar · limites de orçamento · políticas allow/deny/ask · **cadastro de agentes (perfis)** · cadastro de skills/ferramentas/modelos · **auditoria administrativa** · lista de agentes vivos com estado · tarefa aberta · consumo por agente · **custo estimado por agente** · mensagem entre agentes · protocolos (A2A, MCP) · caixa de entrada · roteamento por nome/ref · livro de mensagens · colisão de nomes |
| **NÃO PRECISA** | **5** | aprovação humana · papéis e permissões RBAC · configuração por projeto · última atividade · filas e workers |
| **DEPOIS** | **11** | pausar · retomar · chaves e segredos · **limite de taxa** · rastro/replay de sessão · **recibo de entrega** · **reentrega** · ***dead-letter*** · ***broadcast*/cópia** · **estabilidade de ref** · alertas |
| **Total** | **32** | 26 da tabela fixa + 6 acrescentadas na correção 1 |

**Os quatro movimentos da correção 1** (para o total fechar): `auditoria` e `custo` passaram de
`NÃO PRECISA` a `ENTRA` (13 → 15 e 8 → 6); a linha 4 foi **desdobrada** — o orçamento fica `ENTRA`,
a taxa vira `DEPOIS`; e cinco funcionalidades de intercomunicação entram como `DEPOIS` (5 → 11).
Confere: 15 + 6 + 11 = 32 = 26 + 6.

**O movimento da correção 2**: `cadastro de agentes` passou de `NÃO PRECISA` a `ENTRA` (15 → 16 e
6 → 5); o mecanismo de execução do controle **não** mexeu no total — ele **realocou** o escopo do
`ENTRA` 4 para o `DEPOIS` `pausar`. Confere: **16 + 5 + 11 = 32** = 26 + 6.

Por grupo (nas **7** do CONTROLE — a linha 4 desdobrada — e nas 6/8/6 fixas): INTERCOMUNICAÇÃO
**6 ENTRA de 6** (a prioridade — nenhum `NÃO PRECISA`, nenhum `DEPOIS`), **+ 5 acrescentadas em
`DEPOIS`**; CONTROLE **3 ENTRA · 1 NÃO PRECISA · 3 DEPOIS** (**+ 1 acrescentada**, `limite de taxa`,
desdobrada); ADMINISTRAÇÃO **3 ENTRA de 6** (ganhou a auditoria na correção 1 e o cadastro de agentes
— leitura dos perfis — na correção 2); GERENCIAMENTO **4 ENTRA de 8** (ganhou o custo por agente).

## Glossário proposto (termos novos — a ratificar)

Nenhum nasce "com a sigla nua": cada um entra aqui com a definição curta; quem tem termo existente
no glossário **reusa** o existente.

| Termo proposto | Definição curta | Observação |
|---|---|---|
| **sessão de agente** | Uma execução de agente que o humano sobe, acompanha e derruba; a unidade de administração. | novo (hoje "sessão" só existe implícito no lançador) |
| **agente (perfil)** | O **perfil** versionado de um agente (`.claude/agents/*.md`) — o cadastro **é** o arquivo; a **sessão** é a instância com ref. | novo (correção 2, decisão 5; distingue-se de **sessão de agente**) |
| **estado do agente vivo** | O estado corrente de uma sessão (trabalhando/esperando/sem tarefa/bloqueado) com detecção de processo, não só *heartbeat*. | novo (reusa os estados de `server.py:27`) |
| **tarefa aberta** | A tarefa ativa **por agente** — o que ele está fazendo agora, com o `start` sem `stop`. | novo; análogo ao **Task ledger** |
| **consumo por agente** | Tokens por agente (não só por sessão/modelo). | novo; extensão de **Custo por sessão** |
| **limite de orçamento** | O teto de consumo de uma sessão/projeto, **declarado** pelo administrador — **teto** e **limiar** são campos da Administração — e **avisado** ao cruzar o limiar. | novo (correção 3, decisão D3: lê-se **"declarado + aviso"**; quem **emite o aviso** é a ingestão de consumo do painel, o **corte** vem depois) |
| **emissor do aviso** | A **ingestão de consumo** do painel (`painel/custo.py`) que compara o consumo medido com o **teto** e o **limiar** e, ao cruzar o limiar, **enfileira** a mensagem endereçada à sessão dona e ao regente. | novo (correção 3, decisão D3; *aviso atrasado, nunca perdido* — o **corte** não é do emissor) |
| **ferramenta MCP como escopo de política** | "Qual agente pode chamar qual **ferramenta MCP**" é **escopo da política `allow/deny/ask` por agente** — a regra nomeia a ferramenta; não há tela própria. | novo (correção 3, decisão D2; reusa **MCP**; regra de exemplo em `administracao-02-politicas.html`) |
| **catálogo de skills/ferramentas/modelos** | O registro consultável de skills, ferramentas e **modelos** por projeto. | novo (skills já existem em pasta) |
| **mensagem entre agentes** | Troca endereçada entre sessões, por artefato/*outbox*, não por chat. | novo; ligado a **Outbox** |
| **protocolo de intercomunicação** | O protocolo pelo qual agentes expõem e consomem ferramentas (**MCP**) e conversam entre pares (**A2A**). | **MCP** já no glossário; **A2A** entra expandido |
| **caixa de entrada** | A visão nomeada do que chegou para uma sessão e ainda não foi lido/*drenado*. | novo — **termo do regente; 0 `sim` em 25 = não encontrado na documentação lida** |
| **livro de mensagens** | O registro append-only unificado das mensagens entre sessões. | novo; análogo ao **Task ledger** |
| **roteamento por nome/ref** | Endereçar uma mensagem/tarefa a uma sessão por nome ou referência, com tabela de resolução. | novo |
| **colisão de nomes** | Duas sessões/agentes/skills com o mesmo nome; a regra que a evita. | novo (hoje só há regra para *ids*) |
| **colisão de endereço** | Duas sessões alcançáveis pelo **mesmo endereço** (mesmo nome em refs diferentes, ou o mesmo nome em dois projetos); a regra é **recusar, nunca resolver**. | novo (correção 1, decisão 3; ver `mapa-de-contextos.md` § 7) |
| **auditoria administrativa** | A trilha, na área administrativa, de **quem** mudou o quê (`changed_by`) — não só o índice de decisões. | novo; extensão de **Auditoria** |
| **custo estimado por agente** | O custo em dólar **por agente**, derivado da tabela de preços do modelo no catálogo e marcado **"estimado"**. | novo; extensão de **Custo por sessão** |
| **limite de taxa** | O teto de requisições por minuto (RPM, *requests per minute*) e de tokens por minuto (TPM, *tokens per minute*) por sessão/projeto — separado do **limite de orçamento**. | novo (desdobrado da linha 4) |
| **recibo de entrega** (*ack*) | A confirmação de que a mensagem **chegou** ao destinatário — hoje ausente. | novo |
| **reentrega** | O reenvio de uma mensagem cuja primeira entrega falhou. | novo |
| ***dead-letter*** | O depósito das mensagens que não puderam ser entregues. | novo; ligado a **Outbox** |
| ***broadcast*/cópia** | Endereçar a mesma mensagem/tarefa a mais de uma sessão de uma vez. | novo |
| **estabilidade de ref** | O ref de uma sessão **sobrevive ao reinício**; hoje ele muda. | novo; ligado a **colisão de endereço** |

**Reusados (já no glossário, não são termos novos):** **OPA** (*Open Policy Agent*, política
`allow/deny/ask`), **MCP**, **RBAC**, **Outbox**, **Task ledger**, **Custo por sessão**,
**Auditoria**, **Chamado**, **Painel de regência**.

## Limites desta decisão (declarados)

- **Nada construído**: esta é a rodada 2 (decisão documental); o software nasce — se nascer — das
  rodadas 3–4. Nenhuma arquitetura foi fixada aqui.
- **A prioridade do regente foi honrada**: INTERCOMUNICAÇÃO decidiu primeiro e levou 6 `ENTRA`.
- **Nenhum `ENTRA` se apoia em célula `—`** (regra 2): onde não se encontrou fonte na documentação
  lida, a fonte é o **requisito do método**, e a plataforma citada é a melhor `parcial`, declarada.
- **Força do veredito herdada**: os 2 `não tem` do inventário são `não encontrado` (piso, não
  prova) — por isso `pausar`/`retomar` ficam em `DEPOIS` (gatilho declarado), não em `NÃO PRECISA`.
- **Correção 1 da rodada 4** (o que mudou, e por quê):
  - os **totais foram refeitos** (13/8/5 → **15/6/11**, sobre 32 funcionalidades) — `auditoria` e
    `custo` subiram a `ENTRA` (com `changed_by` e com o dólar por agente) e a taxa foi **desdobrada**
    da linha 4, em vez de desaparecer com ela;
  - as bases de **roteamento** (Windmill roteia ferramenta por nome e job por *tag*, **não** sessão
    por nome/ref) e de **colisão** (Kiro Crew × Claude Code, agora com o **mesmo critério**) foram
    corrigidas; a citação de `contatos()` passou de `server.py:469` para **`server.py:479`**;
  - `pausar`/`retomar` deixaram de ser justificados como "o mercado não tem": **retomar existe** no
    Claude Code — o que falta é **fonte** para retomar o **estado**, e isso se escreve **"não
    encontrado na documentação lida"**, nunca "lacuna de mercado" (decisão 6);
  - o gatilho de todo `DEPOIS` passou a ser **escrito** (regra 3).
- **Correção 2 da rodada 4** (o que mudou, e por quê):
  - o **mecanismo de execução do controle** saiu de `ENTRA` para `DEPOIS` (decisão 2): "recusar a
    chamada seguinte" e "suspender a sessão" são **o mesmo ponto de execução** — *hook* que lê o
    **consumo medido**, a desenhar na raia *infra*. O `ENTRA` 4 fica com **declarar o teto + avisar**;
  - `cadastro de agentes` subiu de `NÃO PRECISA` a **`ENTRA` 16** — **leitura do catálogo de perfis**
    (o cadastro é o arquivo versionado, não a tela);
  - a *"mensagem desviada"* saiu de `alertas` (já tem tela): o `DEPOIS` passa a ser **notificação
    ativa**;
  - as citações a `claude-code.md` foram **revalidadas contra o HEAD** (`:47→:61`, `:68→:82`,
    `:71→:84`).
- **Correção 3 da rodada 4** (o que mudou, e por quê) — as três decisões são **de escopo**, e os
  totais seguem **16/5/11 = 32**; o que muda é **o que cada `ENTRA` pede**:
  - **D1** — a linha "limites de orçamento e de taxa" **não foi desdobrada na matriz fixa**: o que a
    distingue é a leitura **por célula** (`corta` / `avisa` / `avisa?`, com a ficha como fonte), como
    `pesquisa/plataformas.md` agora mostra. O desdobramento em duas linhas existe **no confronto**,
    por decisão da correção 1 — as duas leituras convivem de propósito: a matriz fixa mede o mercado,
    o confronto decide o escopo do Maestro;
  - **D2** — a **ferramenta MCP** vira **escopo da política `allow/deny/ask`** em vez de tela: a regra
    de exemplo em `administracao-02-politicas.html` (`#regra-ferramenta-mcp`) nomeia agente e
    ferramenta, e cada ferramenta do protocolo aponta de volta para ela;
  - **D3** — o **emissor do aviso de teto deixa de ser "a desenhar"**: é a **ingestão de consumo**
    (`painel/custo.py`), que ao cruzar o limiar enfileira a mensagem endereçada — desenhado em
    `administracao-03-orcamento.html`, § "Quem emite o aviso". Onde a correção 2 dizia "avisar", a
    correção 3 diz **como**: o `ENTRA` 4 passa a se ler **"declarar teto + avisar, com emissor
    desenhado"**, e o **corte** segue em `DEPOIS`.
- **Lacunas declaradas (não silenciadas)** — decisão 2, comuns ao confronto e ao inventário:
  - **o corte do controle é dívida — o aviso já não é**: o **emissor do aviso** está **desenhado**
    (a ingestão de consumo, `painel/custo.py` — decisão D3); o que falta é o **corte**, o *hook* que
    lê o consumo medido e corta o gasto de modelo, **a desenhar na raia *infra***;
  - **o caminho de aprovação do derrubar** (a passagem pelo pedido de decisão da Regência, relação 5
    do mapa; decisão 3) é **documentado**, não construído;
  - **o `tarefas.jsonl` (o *ledger* de tarefas) parou no ciclo 064** — todo custo por agente lido
    dele é **piso**, não total;
  - **a área administrativa é somente leitura nesta rodada**: nenhuma tela opera o sistema real.
- **Fora do alcance desta peça**: a identidade `nome · ref · projeto` (decisão 2) e o **roster**
  (decisão 1) são regra das **telas** e do **verificador** (regras 5 e 6,
  `prototipo/verifica-prototipo.py`), não desta tabela; a colisão de **endereço** (decisão 3) mora no
  **mapa de contextos** (§ 7), e a **ambiguidade de endereço não é verificada por script** — fica
  declarada no README do protótipo e no mapa (§ 8).
- **Siglas expandidas na primeira ocorrência** (Princípio VIII): RBAC (*Role-Based Access Control*),
  RACI (*Responsible, Accountable, Consulted, Informed*), MCP (*Model Context Protocol*), A2A
  (*Agent-to-Agent*), ADR (*Architecture Decision Record*), OPA (*Open Policy Agent*), YAGNI
  (*You Aren't Gonna Need It*), DDD (*Domain-Driven Design*).
