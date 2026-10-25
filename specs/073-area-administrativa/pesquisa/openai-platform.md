# OpenAI Platform — console administrativo da plataforma de API

- **URL**: https://platform.openai.com/ · **Documentação**: https://developers.openai.com/api/docs
  (a antiga `platform.openai.com/docs` redireciona para lá) · **Central de ajuda**:
  https://help.openai.com/
- **Data da visita**: 2026-10-24/25 (a sessão atravessou a meia-noite)
- **Nicho**: plataforma de API de LLM (*Large Language Model*) — administração de
  organização/projetos, uso, chaves de API e agentes
- **Modelo**: SaaS (nuvem). `platform.openai.com/docs` **não renderiza sem JavaScript**
  (a visita devolveu só o título "OpenAI Platform"); a documentação foi lida em
  `developers.openai.com`, que é para onde ela redireciona.

## O que foi aberto de verdade

**Não rodou local** (SaaS; sem Docker nesta máquina). Páginas abertas em 2026-10-24:

- https://developers.openai.com/api/docs/llms.txt — índice das seções (Actions, Assistants,
  Agents, Admin APIs, Evals, MCP, Models, Pricing…)
- https://developers.openai.com/api/docs/guides/admin-apis.md — "Admin API keys", "Audit
  logs", "Invites", "Users", "Projects", "Spend limits"
- https://developers.openai.com/api/docs/guides/rbac.md — papéis de organização e de projeto
- https://developers.openai.com/api/docs/guides/spend-limits.md — limite de gasto e alertas
- https://developers.openai.com/api/docs/guides/rate-limits.md — limites de taxa por
  organização/projeto/modelo
- https://developers.openai.com/api/docs/guides/agents.md — Agents API/Agents SDK:
  ferramentas, MCP, sessões, *handoffs*, aprovações
- https://openai.github.io/openai-agents-python/ — Agents SDK: *Agents*, *Handoffs*,
  *Guardrails*, *Sessions*, *Tracing*, "Human in the loop", "MCP server tool calling"
- https://openai.com/index/introducing-agentkit/ — AgentKit: "Agent Builder", "Connector
  Registry", "ChatKit", guardrails, Evals
- https://help.openai.com/en/articles/9186755-managing-your-work-in-the-api-platform-with-projects
  — projetos, membros, *service accounts*, chaves e limites (Limits → Model usage, spend)

## Tabela fixa (spec.md § "Tabela fixa de funcionalidades")

### CONTROLE

| Funcionalidade | Resposta | Fonte (URL + o que foi visto) |
|---|---|---|
| Subir/derrubar sessão ou agente | parcial | `guides/agents.md`: sessões são recursos com ciclo de vida ("An Agents API session, an SDK session, a Responses conversation, and a sandbox are different resources", com contabilização e limpeza); `introducing-agentkit`: Agent Builder permite **preview runs** e versionamento. Não há "subir/derrubar agente" como processo |
| Pausar | não | nenhuma página aberta documenta pausar execução (nem no Agent Builder, nem no Agents SDK) |
| Retomar |  | nenhuma página aberta |
| Limites de orçamento e de taxa | sim | `spend-limits.md`: limite de organização ("across all projects") e de projeto, "Enforce a hard limit" → **429** `organization_spend_limit_exceeded` / `project_spend_limit_exceeded`, "Spend alert" notifica sem capar; `rate-limits.md`: "RPM", "RPD", "TPM", "TPD", "IPM", definidos "at the organization level and at the project level, not user level", com *tiers* (Free/Build/Launch/Grow) e `Retry-After` |
| Políticas allow/deny/ask | parcial | `introducing-agentkit`: Guardrails — "an open-source, modular safety layer" (mascarar PII, detectar *jailbreak*); `openai-agents-python`: guardrails validam entrada/saída do agente; `guides/rbac.md`: níveis `Read`, `Write`, `Request`, `Use`, `Manage`. Não há taxonomia allow/deny/ask explícita |
| Aprovação humana | parcial | `openai-agents-python`: "Human in the loop: Built-in mechanisms for involving humans during agent runs"; `introducing-agentkit`: nó "User approval" no canvas do Agent Builder (beta) |

### ADMINISTRAÇÃO

| Funcionalidade | Resposta | Fonte (URL + o que foi visto) |
|---|---|---|
| Cadastro de agentes | parcial | `introducing-agentkit`: "Agent Builder — a visual canvas for creating and versioning multi-agent workflows"; `guides/agents.md`: agentes reutilizáveis no SDK. **Não há registro de agentes**: o único *registry* é o "Connector Registry" ("how data and tools connect") |
| Papéis e permissões RBAC | sim | `guides/rbac.md`: "Org owner permissions", "Org reader permissions", "Project owner permissions", "Project member permissions", "Project viewer permissions"; níveis `Read`/`Write`/`Request`/`Use`/`Manage`; "Custom role eligible"; "Users can have multiple roles, and their access is the union of those roles" |
| Cadastro de skills/ferramentas/modelos | parcial | `introducing-agentkit`: "Connector Registry" (dados e ferramentas), Evals com "Datasets"; `guides/llms.txt`: "Add custom MCP server", "MCP servers", "All models", "Compare models". "Skills" não é conceito da plataforma (é do Claude Code) |
| Chaves e segredos | sim | `help.openai.com` (artigo de projetos): chave por projeto ("+ Create new secret key") com permissões "All", "Restricted", "Read Only"; *service accounts* com escopo de projeto, cujo segredo "You can't view it again"; `guides/admin-apis.md`: "Admin API keys" |
| Configuração por projeto | sim | `help.openai.com`: projetos com membros ("Owner"/"Member"), *service accounts*, "Limits" → "Model usage" (modelos e limites por modelo), cotas de arquivo ("100 GB"), arquivamento permanente; `guides/terraform/projects-and-access.md`, `project-controls.md` (índice) |
| Auditoria | sim | `guides/admin-apis.md`: "Audit logs — retrieve/list user actions and config changes; `client.admin.organization.auditLogs.list`", junto de "Invites", "Users", "Projects" e "data retention" |

### GERENCIAMENTO

| Funcionalidade | Resposta | Fonte (URL + o que foi visto) |
|---|---|---|
| Lista de agentes vivos com estado | não | `guides/agents.md` cita "Agents API observability and usage" (observabilidade e uso), mas nenhuma página aberta lista agentes vivos com estado |
| Tarefa aberta |  | nenhuma página aberta |
| Última atividade | parcial | `openai-agents-python`: "Tracing: Built-in tracing for visualizing, debugging, and monitoring workflows"; `introducing-agentkit`: "Trace grading — run end-to-end assessments of agentic workflows" — dá para ver a última execução, não a atividade de um agente vivo |
| Consumo por agente/sessão/modelo | parcial | `help.openai.com`: "Usage Dashboard" (visível se "Visible to organization owners") e "Model usage" por projeto; `openai-agents-python` lista o recurso "Usage"; `rate-limits.md`: limites por modelo. Por **agente** não aparece |
| Custo | sim | `spend-limits.md` (gasto por organização e por projeto, alerta e limite rígido), `help.openai.com` (Usage Dashboard), `guides/admin-apis.md` ("Spend limits", "spend alerts") |
| Filas e workers | parcial | `rate-limits.md`: "Batch: queue limits count total queued input tokens; completed jobs no longer count" — há fila **do Batch API**; *workers* não aparecem |
| Rastro/replay de sessão | parcial | `openai-agents-python`: "Sessions: A persistent memory layer", "Tracing"; `introducing-agentkit`: "Trace grading"; `guides/trace-grading.md` (índice). *Replay* não é documentado |
| Alertas | sim | `spend-limits.md`: "Spend alert" (padrão em 100 %, "Add Alert" acrescenta limiares; alerta não capa o gasto); `guides/admin-apis.md`: "spend alerts" por projeto |

### INTERCOMUNICAÇÃO

| Funcionalidade | Resposta | Fonte (URL + o que foi visto) |
|---|---|---|
| Mensagem entre agentes | parcial | `openai-agents-python`: "Handoffs … letting agents delegate to other agents for specific tasks"; `guides/agents.md`: o runner do SDK "handles the agent loop and handoffs" e cita "multi-agent orchestration" — delegação dentro do processo, não mensageria entre agentes independentes |
| Protocolos (A2A; MCP) | parcial | MCP **sim**: `guides/llms.txt` ("MCP servers", "MCP connections", "Secure MCP Tunnel", "Add custom MCP server"), `openai-agents-python` ("MCP server tool calling"); **A2A não aparece** em nenhuma página aberta |
| Caixa de entrada |  | nenhuma página aberta |
| Roteamento por nome/ref | não | `openai-agents-python`: *handoffs* entregam a um objeto de agente no código; nenhuma página aberta mostra roteamento por nome/ref num registro |
| Livro de mensagens | parcial | `openai-agents-python` / `guides/agents.md`: "a Responses conversation" e "Sessions" guardam o histórico de contexto de uma conversa (memória persistente), não um livro de mensagens entre agentes |
| Colisão de nomes |  | nenhuma página aberta |

## Observações para a rodada 2

- **Alerta de tempo de vida**: o post do AgentKit traz a atualização de 2026-06-03 dizendo
  que **Agent Builder e Evals serão descontinuados — indisponíveis depois de 30/11/2026**.
  Para a rodada 2, isso rebaixa tudo que depende do Agent Builder a "não apostar".
- O que a plataforma ensina bem: **RBAC em dois níveis (organização × projeto) com papéis
  customizáveis**, **limite rígido + alerta de gasto** e **auditoria por Admin API**.
- Não há registro de agentes, fila de agentes nem mensageria entre agentes: a metáfora da
  plataforma é "projeto + chave + requisição", não "agente vivo".
