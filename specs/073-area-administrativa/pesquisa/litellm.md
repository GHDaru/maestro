# LiteLLM — gateway de LLM (Large Language Model) com console administrativo

- **URL**: https://www.litellm.ai/ · **Documentação**: https://docs.litellm.ai/
- **Data da visita**: 2026-10-24/25 (a sessão atravessou a meia-noite)
- **Nicho**: gateway/proxy de LLM de código aberto, com interface administrativa (Admin UI
  — *User Interface*) e registro de agentes por A2A (*Agent-to-Agent*)
- **Licença / modelo**: código aberto (proxy e gateway) + *Enterprise* para parte da
  administração (auditoria, projetos, *kill switch* com licença)

## O que foi aberto de verdade

### Rodou local (proxy + Admin UI, sem credencial real)

- `pip install "litellm[proxy]"` numa *virtualenv* temporária → **litellm 1.106.3**
  (Windows, Python 3.12).
- Servidor: `uvicorn litellm.proxy.proxy_server:app --host 127.0.0.1 --port 4000`, com um
  `config.yaml` local de **uma** entrada de modelo e uma chave local descartável
  (`sk-local-demo-073-nao-e-segredo`) — nenhuma credencial real, nenhum provedor externo
  chamado.
- Comandos verificados (respostas reais):
  - `GET /health/liveliness` → `200 "I'm alive!"`
  - `GET /v1/models` → `200 {"data":[{"id":"demo-sem-credencial",...}]}`
  - `GET /v1/agents` → `200 []` (lista de agentes do gateway)
- Capturas em `img/`: `litellm-01-ui-login.png` (tela de login da Admin UI, aberta em
  `http://127.0.0.1:4000/ui/`), `litellm-02-ui-login-sem-banco.png` (login recusado com a
  mensagem real do servidor).
- **Limite honesto**: entrar na Admin UI exige banco de dados — a resposta real foi
  `400 {"error":{"message":"Authentication Error, Not connected to DB!","type":"auth_error"}}`.
  Nesta máquina não há Docker, e o caminho `DATABASE_URL=sqlite:///` abortou o *boot* com
  `ModuleNotFoundError: No module named 'prisma'`. Logo: **a UI subiu e a tela de login foi
  capturada; as telas autenticadas (chaves, times, agentes, logs) não foram abertas aqui** —
  o que consta abaixo vem da documentação, com URL.

### Documentação aberta (WebFetch, 2026-10-24)

- https://docs.litellm.ai/docs/proxy/ui — Admin UI: papéis de login, "Model Management" /
  "Add Models" / "AI Hub", chaves virtuais, *break-glass admin*
- https://docs.litellm.ai/docs/proxy/virtual_keys — chaves virtuais: orçamento, limites,
  "Key Rotations", "Scheduled Key Rotations", "Spend Tracking"
- https://docs.litellm.ai/docs/proxy/users — orçamento e limite de taxa por usuário/time
- https://docs.litellm.ai/docs/proxy/audit_logs — auditoria (`store_audit_logs`,
  `LiteLLM-Changed-By`, tabelas `LiteLLM_TeamTable`, `LiteLLM_UserTable`,
  `LiteLLM_VerificationToken`) — **exige licença Enterprise**
- https://docs.litellm.ai/docs/proxy/access_control — papéis RBAC (*Role-Based Access
  Control*): `proxy_admin`, `proxy_admin_viewer`, `internal_user`, `org_admin`, `team_admin`
- https://docs.litellm.ai/docs/proxy/tool_policies — políticas de ferramenta
  (`untrusted` / `trusted` / `blocked`), com sobrescrita por chave/time
- https://docs.litellm.ai/docs/proxy/guardrails/quick_start — guardrails com modos
  `pre_call`, `post_call`, `during_call`, `logging_only`
- https://docs.litellm.ai/docs/mcp — gateway MCP (*Model Context Protocol*): cadastro de
  servidores, "List Tools"/"Call Tools", permissão por chave/time/organização
- https://docs.litellm.ai/docs/a2a — agentes A2A: `POST /a2a/{agent_id}/message/send`,
  `GET /v1/agents`, "Agentic > Agents > Add New Agent", *agent card*
- https://docs.litellm.ai/docs/a2a_agent_permissions — permissão de agente por chave/time
  (`object_permission.agents`), "most restrictive wins"; **sem roteamento por nome**
- https://docs.litellm.ai/docs/a2a_kill_switch — *kill switch*: só `proxy_admin` dispara,
  `POST /v1/agents/{agent_id}/kill_switch`, audita `kill_switch_fired`
- https://docs.litellm.ai/docs/skills_gateway — **Skills Registry**: cadastro de *skills* do
  Claude Code (`POST /claude-code/plugins`), `GET /claude-code/plugins`,
  `GET /public/skill_hub`, permissão por `object_permission.skills`
- https://docs.litellm.ai/docs/proxy/project_management — projetos: `POST /project/new`,
  `/project/list`, `/project/info`, orçamento e limites por projeto (Enterprise)
- https://docs.litellm.ai/docs/proxy/alerting — alertas (`budget_alerts`, `spend_reports`,
  `llm_exceptions`, `new_virtual_key_created`, …) via Slack, Discord, Teams, e-mail, webhook
- https://docs.litellm.ai/docs/proxy/ui_logs_sessions — sessões na UI por
  `litellm_session_id`
- https://docs.litellm.ai/docs/proxy/lens — Lens: *traces*, "Investigations", análise de
  sessões de agente (Claude Code, Codex)
- https://docs.litellm.ai/docs/proxy/reliability — fallbacks, `num_retries`,
  `request_timeout`, cooldowns (**sem** filas de requisição ou *workers*)
- Índice completo consultado: https://docs.litellm.ai/llms.txt

## Tabela fixa (spec.md § "Tabela fixa de funcionalidades")

### CONTROLE

| Funcionalidade | Resposta | Fonte (URL + o que foi visto) |
|---|---|---|
| Subir/derrubar sessão ou agente | parcial | `a2a_kill_switch`: existe o *kill switch* — `POST /v1/agents/{agent_id}/kill_switch` dispara um webhook de desligamento, mas "the agent stays registered and enabled on the LiteLLM side". Não há "subir" agente pela UI (cadastro ≠ processo vivo) |
| Pausar | não | `a2a_kill_switch` esgota o controle de ciclo de vida que a doc oferece (disparar *kill switch*); nada de pausar aparece |
| Retomar | não | idem: nenhuma página do índice trata retomar/religar |
| Limites de orçamento e de taxa | sim | `virtual_keys` (`max_budget`, `budget_duration`, `tpm_limit`, `rpm_limit`, "Spend Tracking"), `users` (orçamento por usuário/time), índice: "Setting Team Budgets", "Tag Budgets", "Dynamic TPM/RPM Allocation", "Budget Reset Times" |
| Políticas allow/deny/ask | parcial | `tool_policies`: `input_policy` = `untrusted`/`trusted`/**`blocked`** por ferramenta, com sobrescrita por `team_id`/`key_hash`; guardrails bloqueiam ("Violated guardrail policy"). **Não existe o "ask"** — nenhuma aprovação no meio da chamada |
| Aprovação humana | não | `tool_policies` e `guardrails/quick_start` documentam bloqueio/máscara; nada de fila de aprovação humana (o único modo "humano" é `logging_only`, que não bloqueia) |

### ADMINISTRAÇÃO

| Funcionalidade | Resposta | Fonte (URL + o que foi visto) |
|---|---|---|
| Cadastro de agentes | sim | `a2a`: "Agentic > Agents > Add New Agent", `agents` no `config.yaml` (`agent_name`, `agent_card_params`), `POST /v1/agents`, listagem em `GET /v1/agents` |
| Papéis e permissões RBAC | sim | `access_control`: `proxy_admin`, `proxy_admin_viewer`, `internal_user`, `org_admin`, `team_admin`; `team_member_permissions` enumera rotas liberáveis (`/key/generate`, `/key/delete`, `/key/block`, …) |
| Cadastro de skills/ferramentas/modelos | sim | `skills_gateway`: **Skills Registry** (`POST /claude-code/plugins`, `GET /claude-code/plugins`, `GET /public/skill_hub`, `marketplace.json`); `mcp` (cadastro de servidores MCP e "List Tools"); `ui` ("Model Management", "Add Models", "AI Hub") |
| Chaves e segredos | sim | `virtual_keys`: gerar/bloquear/rotacionar ("Key Rotations", "Scheduled Key Rotations"), `block`/`unblock`; `audit_logs` mascara segredos (`REDACTED_BY_LITELM`, como a doc grafa) |
| Configuração por projeto | sim | `project_management`: hierarquia "Organizations > Teams > Projects > Keys", `POST /project/new|update`, `/project/list|info|delete`, `max_budget`/`tpm_limit`/`rpm_limit`/`budget_duration` por projeto, chave amarrada por `project_id` |
| Auditoria | sim | `audit_logs`: registra "Keys, Teams, Users, Models" com `changed_by` (tabelas `LiteLLM_TeamTable`, `LiteLLM_UserTable`, `LiteLLM_VerificationToken`), exporta para S3 — **exige licença Enterprise** |

### GERENCIAMENTO

| Funcionalidade | Resposta | Fonte (URL + o que foi visto) |
|---|---|---|
| Lista de agentes vivos com estado | parcial | `a2a`: `GET /v1/agents` lista os agentes **cadastrados** (nome, URL, `protocolVersion`) — é registro, não estado de execução; nenhuma página documenta saúde/liveness do agente |
| Tarefa aberta |  | nenhuma página aberta documenta a tarefa em curso de um agente |
| Última atividade | parcial | `a2a`: cada chamada ao agente guarda log de requisição/resposta com "User, Key, Team", latência e custo; `ui_logs_sessions` agrupa por sessão |
| Consumo por agente/sessão/modelo | sim | `a2a`: "Agent Usage (A2A)" e `a2a_cost_tracking`; `virtual_keys`: "Spend Tracking" (`/key/info`, `/user/info`, `/team/info`) e "The cost per model is stored here"; índice: `a2a_iteration_budgets`, `mcp_cost` |
| Custo | sim | `virtual_keys` ("Spend Tracking"), `a2a` (custo por agente), `project_management` (`spend`, `model_spend` em `/project/info`) |
| Filas e workers | não | `ui` (só "worker" no sentido de contador de login: "each worker counts on its own") e `reliability` (fallbacks, retries, cooldowns — "Not covered: request queues, queueing, worker processes") |
| Rastro/replay de sessão | parcial | `ui_logs_sessions`: agrupa requisições por `litellm_session_id` (sem replay); `lens`: "Lens > Traces" e "Lens > Investigations" analisam execuções — "replay is not mentioned" |
| Alertas | sim | `alerting`: tipos `budget_alerts`, `spend_reports`, `llm_exceptions`, `llm_too_slow`, `new_virtual_key_created`, `virtual_key_deleted`, `mcp_pinned_tools_changed`; entrega em Slack, Discord, Teams, e-mail e webhook |

### INTERCOMUNICAÇÃO

| Funcionalidade | Resposta | Fonte (URL + o que foi visto) |
|---|---|---|
| Mensagem entre agentes | sim | `a2a`: `POST /a2a/{agent_id}` ("Primary — all A2A methods") e `POST /a2a/{agent_id}/message/send` — um cliente/agente envia mensagem a outro agente |
| Protocolos (A2A; MCP) | sim | `a2a` (`/.well-known/agent-card.json`, `protocolVersion` `0.3`/`1.0`) e `mcp` ("MCP Gateway", `mcp_servers`, transporte HTTP/SSE/STDIO) |
| Caixa de entrada | não | `mcp`: "Inbox/message routing: Not documented. No inbox, mailbox, queue, or message-routing section or key appears" |
| Roteamento por nome/ref | parcial | `a2a`: roteia por `agent_id` (`POST /a2a/{agent_id}`) e busca por `GET /v1/agents?query=&top_k=`; `a2a_agent_permissions`: "No. Access is keyed on `agent_id`… names like 'Support Agent' are display-only, not routing keys" |
| Livro de mensagens | parcial | `a2a`: os logs de requisição guardam conteúdo de requisição/resposta por agente (com usuário, chave, time, latência, custo) — é histórico de chamadas, não um livro de mensagens entre agentes |
| Colisão de nomes |  | `a2a_agent_permissions` fixa o roteamento por `agent_id`, mas nenhuma página aberta trata colisão de nomes |

## Observações para a rodada 2

- O **Skills Registry** da LiteLLM (`/claude-code/plugins`, `marketplace.json`,
  `object_permission.skills`) é o item mais próximo do "cadastro de skills" da spec 073 e
  conversa direto com o Maestro (skills versionadas por *plugin*).
- O controle de ciclo de vida é o ponto fraco: existe **derrubar** (kill switch, Enterprise,
  com webhook) e **não** existe subir/pausar/retomar no gateway.
- Não há fila nem *worker* de agente: o gateway roteia chamadas, não conduz processos.
