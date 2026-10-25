# Portkey — gateway de IA com governança e console administrativo

- **URL**: https://portkey.ai/ · **Documentação**: https://portkey.ai/docs
- **Data da visita**: 2026-10-24/25 (a sessão atravessou a meia-noite)
- **Nicho**: gateway de LLM (*Large Language Model*) com governança — catálogo de modelos,
  guardrails, limites por *workspace* e registro de agentes/MCP (*Model Context Protocol*)
- **Modelo**: SaaS (nuvem) · parte da administração é do plano **Enterprise** (auditoria,
  papéis, *log export*)

## O que foi aberto de verdade

**Não rodou local.** Não há Docker nesta máquina e o produto é SaaS — a doc descreve
"private-cloud hosting for enterprises" e SSO por OIDC, não uma instalação local de
avaliação. Tudo abaixo vem da documentação pública, aberta em 2026-10-24:

- https://portkey.ai/docs/llms.txt — índice (150 páginas de *Admin APIs*, 182 de docs)
- https://portkey.ai/docs/_llms/latest/docs.txt — índice navegável usado para achar as páginas
- https://portkey.ai/docs/product/enterprise-offering/org-management/user-roles-and-permissions.md
  — papéis e RBAC (*Role-Based Access Control*)
- https://portkey.ai/docs/product/enterprise-offering/audit-logs.md — auditoria (Enterprise)
- https://portkey.ai/docs/product/enterprise-offering/budget-policies.md — políticas de uso e
  limite de taxa
- https://portkey.ai/docs/product/observability/logs.md — logs de requisição, replay
- https://portkey.ai/docs/product/mcp-gateway.md — gateway MCP
- https://portkey.ai/docs/product/agent-gateway/registry.md — Agent Registry

## Tabela fixa (spec.md § "Tabela fixa de funcionalidades")

### CONTROLE

| Funcionalidade | Resposta | Fonte (URL + o que foi visto) |
|---|---|---|
| Subir/derrubar sessão ou agente | parcial | `agent-gateway/registry.md`: o Agent Gateway "lets admins **provision agents** and granularly control access to them" — provisiona e controla acesso; nada de subir/derrubar um processo |
| Pausar | não | `agent-gateway/registry.md` esgota o ciclo de vida documentado (provisionar + controlar acesso); "Not mentioned: Listing agents, health/status, or versions — none appear" |
| Retomar |  | nenhuma página aberta trata retomar |
| Limites de orçamento e de taxa | sim | `budget-policies.md`: "Usage Limit Policies" com tipos `"cost"`, `"tokens"`, `"requests"`, `credit_limit`, `group_by` (`api_key`, `workspace_id`, `metadata._user`); limite de taxa `"rpm"`/`"rph"`/`"rpd"`/`"rpw"`, `target` `"llm"`/`"mcp_tools"`; estouro devolve **429** e orçamento estourado **412**; `enforce-budget-and-rate-limit`, `enforce-workspace-budget-limts-and-rate-limits` |
| Políticas allow/deny/ask | parcial | `mcp-gateway.md`: guardrails = "Content filters and approval workflows per server"; `guardrails` (PII redaction, lista de checagens, "Bring Your Own Guardrails"). **Não há taxonomia allow/deny/ask** — há filtro/bloqueio e aprovação por servidor MCP |
| Aprovação humana | parcial | `mcp-gateway.md`: "Guardrails — Content filters and **approval workflows** per server"; nenhuma página aberta descreve a tela/fila de aprovação |

### ADMINISTRAÇÃO

| Funcionalidade | Resposta | Fonte (URL + o que foi visto) |
|---|---|---|
| Cadastro de agentes | sim | `agent-gateway/registry.md`: "The Agent Registry is where agents are configured and managed", "register your agents by following the getting started guide"; `agent-gateway/servers.md` (Agent Servers) |
| Papéis e permissões RBAC | sim | `user-roles-and-permissions.md`: "a comprehensive role-based access control (RBAC) system"; organização — "Owner", "Admin", "Member"; workspace — "Admin", "Manager", "Member"; "A user cannot modify an API key that carries permissions exceeding their own role" |
| Cadastro de skills/ferramentas/modelos | sim | `mcp-gateway.md`: `mcp-registry` ("where MCP servers are configured and managed"), `tool-provisioning` ("Enable or disable specific tools per user"); `model-catalog` (integrações, modelos customizados, `model-provisioning`) |
| Chaves e segredos | sim | `api-keys-authn-and-authz.md`, `api-key-rotation.md`, `virtual-keys`, `secret-references.md`, `kms.md` (índice `docs.txt`) |
| Configuração por projeto | sim | `org-management/workspaces.md`: "Each workspace maintains its own access control structure with three distinct roles"; `configure-workspace-provisioning-for-your-ai-integrations.md` |
| Auditoria | sim | `audit-logs.md`: campos Timestamp, User, Workspace, Action, Resource, Response Status, Client IP, Country; filtros Method, Request ID, Resource Type, Action, Response Status, Workspace, User, Client IP, Country, Time Range; "Indefinite log retention" e "Custom retention policies"; acesso só de "org owners and admins" em `Admin Settings > Audit Logs` — **Enterprise** |

### GERENCIAMENTO

| Funcionalidade | Resposta | Fonte (URL + o que foi visto) |
|---|---|---|
| Lista de agentes vivos com estado | não | `agent-gateway/registry.md`: "Not mentioned: Listing agents, health/status, or versions — none appear" (o registro serve para provisionar e permissionar, não para listar estado) |
| Tarefa aberta |  | nenhuma página aberta |
| Última atividade | parcial | `observability/logs.md`: cada log traz "timestamp, request type, LLM used, tokens generated, thinking tokens and cost" — atividade por requisição, não por agente |
| Consumo por agente/sessão/modelo | parcial | `budget-policies.md` (orçamento por `api_key`, `workspace_id`, `metadata._user`), `observability/cost-management.md` e `observability/analytics.md` (índice); por **agente** não aparece na doc aberta |
| Custo | sim | `observability/logs.md` ("cost" por requisição), `observability/cost-management.md` ("Model Pricing and Cost Management"), `budget-policies.md` (política de custo com `credit_limit`) |
| Filas e workers |  | nenhuma página aberta documenta fila ou *worker* |
| Rastro/replay de sessão | parcial | `observability/logs.md`: "Debug Requests with Log Replay — `Replay` button opens your request in a fresh prompt playground" (replay de **requisição**); `observability/traces.md` está no índice, não foi aberta |
| Alertas | parcial | `budget-policies.md`: `alert_threshold` grava evento em "audit logs"; "proactive email alerts are **work in progress** and not sent today" |

### INTERCOMUNICAÇÃO

| Funcionalidade | Resposta | Fonte (URL + o que foi visto) |
|---|---|---|
| Mensagem entre agentes | não | `agent-gateway/registry.md`: provisionamento e permissão de acesso ao agente; nada sobre mensagem entre agentes (nem o termo A2A — *Agent-to-Agent* — aparece) |
| Protocolos (A2A; MCP) | parcial | `mcp-gateway.md`: gateway MCP completo (registry, provisionamento por workspace, OAuth/JWT/custom auth, limites de taxa, guardrails) — MCP **sim**; **A2A não aparece** em nenhuma página aberta |
| Caixa de entrada |  | nenhuma página aberta |
| Roteamento por nome/ref | parcial | `mcp-gateway.md`: cliente conecta em `https://mcp.portkey.ai/{server-slug}/mcp` — rota por *slug* do servidor e a chave "determines which servers and tools are accessible"; roteamento de agente por nome não aparece |
| Livro de mensagens |  | nenhuma página aberta |
| Colisão de nomes |  | nenhuma página aberta |

## Observações para a rodada 2

- O que a Portkey tem de mais forte para a área administrativa do Maestro: **papéis
  explícitos por organização e por workspace**, **auditoria com retenção indefinida** e
  **políticas de uso/limite** com `group_by` (permite orçamento por agente/sessão via
  metadado).
- O ponto fraco é o ciclo de vida: registro e permissão de agente sem estado vivo, sem
  fila e sem mensageria entre agentes.
