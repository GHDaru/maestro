# Prefect

- **URL**: https://docs.prefect.io/
- **Data da visita**: 2026-10-24
- **Como foi pesquisada**: WebFetch na documentação oficial (índice `llms.txt`, páginas de conceitos, how-to guides e páginas do Prefect Cloud). Nenhum binário local foi executado (a instalação via `pip` foi considerada pesada e dispensada).
- **O que foi aberto de verdade**:
  - https://docs.prefect.io/ — porta de entrada: descreve o Prefect como "open-source orchestration engine" em Python, com seções Get started / How-to guides / Advanced.
  - https://docs.prefect.io/llms.txt — índice para LLM (*Large Language Model*): listou as URLs de Cloud (RBAC, service accounts, auditoria, ACLs), blocks, deployments, limits de concorrência e rate limits.
  - https://docs.prefect.io/v3/concepts/automations.md — catálogo de gatilhos e ações de automação.
  - https://docs.prefect.io/v3/how-to-guides/automations/creating-automations.md — como criar automações por UI, CLI, Terraform, API e Python.
  - https://docs.prefect.io/v3/concepts/work-pools.md — work pools, filas, prioridade e concorrência.
  - https://docs.prefect.io/v3/concepts/workers.md — workers, polling, heartbeats e status.
  - https://docs.prefect.io/v3/concepts/blocks.md — blocks, `SecretStr` e tipo `Secret`.
  - https://docs.prefect.io/v3/concepts/deployments.md — o que é um deployment e como é disparado.
  - https://docs.prefect.io/v3/concepts/rate-limits.md — rate limits por plano, limite de tamanho de request e retenção.
  - https://docs.prefect.io/v3/concepts/global-concurrency-limits.md — limites globais de concorrência e *slot decay* como rate limit.
  - https://docs.prefect.io/v3/advanced/interactive.md — fluxos interativos (pausar/suspender/retomar com entrada humana).
  - https://docs.prefect.io/v3/how-to-guides/deployments/run-deployments.md — disparar runs de deployment por CLI e Python.
  - https://docs.prefect.io/v3/how-to-guides/configuration/manage-settings.md — configuração por profile, por projeto (`prefect.toml`/`.env`) e por variável de ambiente.
  - https://docs.prefect.io/v3/how-to-guides/configuration/store-secrets.md — guardar segredos com o block `Secret`.
  - https://docs.prefect.io/v3/how-to-guides/ai/use-prefect-mcp-server.md — servidor MCP (*Model Context Protocol*) do Prefect.
  - https://docs.prefect.io/v3/how-to-guides/cloud/connect-to-cloud.md — login no Prefect Cloud, API keys e workspaces.
  - https://docs.prefect.io/v3/how-to-guides/cloud/manage-users/manage-roles.md — papéis e permissões (RBAC — *Role-Based Access Control*).
  - https://docs.prefect.io/v3/how-to-guides/cloud/manage-users/service-accounts.md — service accounts e suas API keys.
  - https://docs.prefect.io/v3/how-to-guides/cloud/manage-users/audit-logs.md — audit logs do Cloud.
  - https://docs.prefect.io/v3/how-to-guides/cloud/manage-users/object-access-control-lists.md — ACLs (*Access Control Lists*) de objeto.

## Tabela fixa (spec 073)

| Grupo | Item | Resultado | Fonte (URL — o que foi visto) |
|---|---|---|---|
| CONTROLE | subir/derrubar sessão ou agente | parcial | https://docs.prefect.io/v3/concepts/workers.md — worker é um "lightweight polling service" iniciado por `prefect worker start -p "my-pool"`, com status `ONLINE`/`OFFLINE`; sobe/derruba workers, não agentes de IA. |
| CONTROLE | pausar | parcial | https://docs.prefect.io/v3/concepts/automations.md — ações `pause-deployment`, `pause-work-pool`, `pause-work-queue`, `pause-automation`; https://docs.prefect.io/v3/advanced/interactive.md — `pause_flow_run`. Vale para fluxos/recursos, não para agentes. |
| CONTROLE | retomar | parcial | https://docs.prefect.io/v3/concepts/automations.md — ações `resume-flow-run`, `resume-deployment`, `resume-work-pool`, `resume-work-queue`, `resume-automation`; https://docs.prefect.io/v3/advanced/interactive.md — `resume_flow_run(flow_run_id, run_input=...)`. |
| CONTROLE | limites de orçamento e de taxa | parcial | https://docs.prefect.io/v3/concepts/rate-limits.md — limits por plano (Hobby 625 req/min; Pro 5.000 req/min), corpo de request máx. "5 MiB", retenção 7–30 dias; https://docs.prefect.io/v3/concepts/global-concurrency-limits.md — `slot_decay_per_second` faz o limite funcionar como rate limit. Não há teto de orçamento em dinheiro. |
| CONTROLE | políticas allow/deny/ask | parcial | https://docs.prefect.io/v3/how-to-guides/cloud/manage-users/manage-roles.md — "Role-based access controls (RBAC) enable you to assign users granular permissions"; https://docs.prefect.io/v3/how-to-guides/cloud/manage-users/object-access-control-lists.md — ACLs de objeto (allow-list para blocks, deployments e work pools, Enterprise). Só existe o lado "allow"; não há "deny" nem "ask". |
| CONTROLE | aprovação humana | parcial | https://docs.prefect.io/v3/advanced/interactive.md — `pause_flow_run`/`suspend_flow_run` com `wait_for_input` criam "human-in-the-loop (HITL) systems"; retomada por `resume_flow_run(..., run_input={...})`. Aplica-se a flow runs, não a agentes. |
| ADMINISTRAÇÃO | cadastro de agentes | parcial | https://docs.prefect.io/v3/concepts/workers.md — cada worker tem um *type* e "can only poll work pools that match their type"; registro via `prefect worker start`; no Cloud exige papel `Worker` + `PREFECT_API_KEY`. Mapeia workers de execução, não agentes de IA. |
| ADMINISTRAÇÃO | papéis e permissões RBAC | sim | https://docs.prefect.io/v3/how-to-guides/cloud/manage-users/manage-roles.md — papéis de conta (Owner/Admin/Member) e de workspace (Viewer/Runner/Developer/Owner/Worker), com "custom roles" (Enterprise); disponível em Pro/Enterprise. |
| ADMINISTRAÇÃO | cadastro de skills/ferramentas/modelos | — | — |
| ADMINISTRAÇÃO | chaves e segredos | sim | https://docs.prefect.io/v3/concepts/blocks.md — campos `SecretStr` "stored with additional encryption and not displayed by default in the UI" e o block type `Secret`; https://docs.prefect.io/v3/how-to-guides/configuration/store-secrets.md — "Secret values are encrypted at rest"; https://docs.prefect.io/v3/how-to-guides/cloud/manage-users/service-accounts.md — API key por service account. |
| ADMINISTRAÇÃO | configuração por projeto | sim | https://docs.prefect.io/v3/how-to-guides/configuration/manage-settings.md — `prefect.toml` ou `.env` no diretório do projeto, profiles (`prefect profile create/use`) e variáveis `PREFECT_*`. |
| ADMINISTRAÇÃO | auditoria | sim | https://docs.prefect.io/v3/how-to-guides/cloud/manage-users/audit-logs.md — "a chronological record of activities performed by members in your account", com eventos de login, criação/remoção de API key, workspaces, convites e service accounts; filtros por workspace/usuário/tipo; retenção varia por plano (Pro/Enterprise). |
| GERENCIAMENTO | lista de agentes vivos com estado | parcial | https://docs.prefect.io/v3/concepts/workers.md — status `ONLINE` quando o worker "sends regular heartbeat messages"; 3 heartbeats perdidos → `OFFLINE`; a página "Worker Details" mostra estado e logs ao clicar no nome do worker na Work Pool list. Lista workers, não agentes de IA. |
| GERENCIAMENTO | tarefa aberta | parcial | https://docs.prefect.io/v3/concepts/deployments.md — o deployment expõe UI/API para "managing runs"; https://docs.prefect.io/v3/how-to-guides/ai/use-prefect-mcp-server.md — ferramentas consultam "deployments, flow runs, task runs, and work pools". |
| GERENCIAMENTO | última atividade | parcial | https://docs.prefect.io/v3/concepts/workers.md — heartbeats regulares (`PREFECT_WORKER_HEARTBEAT_SECONDS`); https://docs.prefect.io/v3/how-to-guides/cloud/manage-users/audit-logs.md — "Each entry ... indicates when an action was taken". |
| GERENCIAMENTO | consumo por agente/sessão/modelo | — | — |
| GERENCIAMENTO | custo | — | — |
| GERENCIAMENTO | filas e workers | sim | https://docs.prefect.io/v3/concepts/work-pools.md — work pools com filas ("default" + extras), prioridade ("`1` being the highest priority") e limite de concorrência por fila, além do "global work pool concurrency limit"; workers consomem essas filas. |
| GERENCIAMENTO | rastro/replay de sessão | parcial | https://docs.prefect.io/v3/advanced/interactive.md — suspender e retomar um flow run (`resume_flow_run`); https://docs.prefect.io/v3/concepts/deployments.md — no Cloud "configuration is versioned and each update creates a new deployment version". Há histórico/retomada, mas não um "replay" de sessão. |
| GERENCIAMENTO | alertas | sim | https://docs.prefect.io/v3/concepts/automations.md — ações de notificação `send-notification`, `call-webhook`, `send-email-notification` e `declare-incident` (as duas últimas "Prefect Cloud" only), disparadas por gatilhos de estado/evento. |
| INTERCOMUNICAÇÃO | mensagem entre agentes | — | — |
| INTERCOMUNICAÇÃO | protocolos (A2A, MCP) | parcial | https://docs.prefect.io/v3/how-to-guides/ai/use-prefect-mcp-server.md — servidor MCP (*Model Context Protocol*) em beta, com ferramentas somente leitura, conectável por Claude Code/Cursor/Codex; nenhuma menção a A2A (*Agent2Agent*) nas páginas abertas. |
| INTERCOMUNICAÇÃO | caixa de entrada | — | — |
| INTERCOMUNICAÇÃO | roteamento por nome/ref | parcial | https://docs.prefect.io/v3/concepts/work-pools.md — "Work pools are like pub/sub topics"; trocar o pool de um deployment "changes which worker runs it"; filas com prioridade determinam a ordem de entrega. |
| INTERCOMUNICAÇÃO | livro de mensagens | — | — |
| INTERCOMUNICAÇÃO | colisão de nomes | — | — |

## Observações

- **Versão livre vs. paga.** Núcleo de orquestração (flows, tasks, work pools, workers, blocks/segredos, automações básicas, concorrência) é do Prefect open source. São **Cloud/pago**: RBAC e custom roles (Pro/Enterprise), audit logs (Pro/Enterprise), ACLs de objeto (Enterprise), `send-email-notification` e `declare-incident`, service accounts, SSO e limites de taxa/retenção por plano.
- **Lacunas.** Não há, na documentação aberta, gestão de custo/orçamento em dinheiro nem consumo por agente/modelo; o "custo" aparece apenas como limites de taxa e retenção de plano. Não há conceitos de agente de IA, mensagens entre agentes, caixa de entrada ou livro de mensagens.
- **MCP.** O servidor MCP do Prefect é read-only e está em beta ("APIs, features, and behaviors may change without notice").
