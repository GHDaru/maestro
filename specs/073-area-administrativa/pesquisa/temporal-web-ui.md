# Temporal Web UI

- **URL**: https://docs.temporal.io/web-ui
- **Data da visita**: 2026-10-24
- **Como foi pesquisada**: WebFetch na documentação oficial (docs.temporal.io) — ver lista
  abaixo. O binário `temporal` foi procurado localmente e **não está instalado** ("O termo
  'temporal' não é reconhecido..."); `docker` também **não existe** nesta máquina. Nada foi
  executado localmente; nenhuma demo pública do Temporal foi aberta. Tudo veio de leitura de
  documentação.
- **O que foi aberto de verdade** (todos via WebFetch, HTTP 200 salvo indicação):
  - https://docs.temporal.io/web-ui — Visão geral da Web UI (User Interface / interface do
    usuário). Traz as telas **Workflows** ("The main Workflows page displays a table of all
    Workflow Executions within the retention period"), **Saved Views**, **Task Failures**
    ("a pre-defined Saved View that displays Workflows that have a Workflow Task failure"),
    **History** (abas Timeline/All/Compact/JSON; "Approximately 40 different Events can appear
    in a Workflow Execution's Event History"; botões "Download Event History" e "Workflow
    Actions" que incluem "request Cancellation", "send Signal or Update", "Reset/Terminate",
    "Start Workflow Like This One"), **Relationships**, **Workers** ("Displays the Workers
    currently polling on the Workflow Task Queue with a count"), **Pending Activities**,
    **Queries**, **Metadata**, **Schedules** e **Archive** (self-hosted). Cita
    "Namespace-level permissions" e papeis "Account Owner and Global Admin" só no Temporal
    Cloud. Auth e read-only não são abordados nesta página.
  - https://docs.temporal.io/references/web-ui-configuration — Referência de configuração da
    Web UI. Seção `auth` "controls who can access the Web UI, not authorization against the
    Temporal Service"; nenhuma chave de autorização é documentada. Traz `disableWriteActions`
    ("Set to `true` to disable every action in the Web UI that changes a Workflow Execution or
    Activity, including batch actions") e as chaves granulares `workflowTerminateDisabled`,
    `workflowCancelDisabled`, `workflowSignalDisabled`, `workflowUpdateDisabled`,
    `workflowResetDisabled`, `workflowPauseDisabled`, `batchActionsDisabled`,
    `startWorkflowDisabled`, `activityCommandsDisabled`, além de `refreshInterval`, `enableUi`,
    `cloudUi`, `showTemporalSystemNamespace`, `cors`, `tls`, `uiServerTLS`, `codec`.
  - https://docs.temporal.io/cloud/manage-access/users — Papéis e permissões no Temporal Cloud
    (RBAC / *Role-Based Access Control*). Papeis de conta: **Global Admin**, **Developer**,
    **Read-Only**, **Account Owner**, **Finance Admin**; permissões por Namespace:
    **Namespace Admin**, **Write**, **Read-Only**.
  - https://docs.temporal.io/cloud/manage-access/custom-roles — Custom Roles no Cloud, criadas
    em "Identities → Custom Roles tab"; "the effective access is the union of both".
  - https://docs.temporal.io/cloud/manage-access/service-accounts — Service Accounts são
    "machine identities that authenticate to Temporal Cloud with API Keys".
  - https://docs.temporal.io/cloud/api-keys — Chaves de API: "will be displayed only once for
    security purposes"; "You can enable or disable API keys"; "Up to 10 non-expired keys per
    user and 20 non-expired keys per Service Account"; alternativa ao mTLS.
  - https://docs.temporal.io/cloud/limits — Limites: "Default limit: 500 actions per second
    (APS)"; RPS dinâmico; "10 schedule requests per second"; "30 Visibility API calls per
    second"; throttling ("Low-priority operations are throttled first"). Nada sobre orçamento
    monetário.
  - https://docs.temporal.io/cloud/audit-logs — Audit Logs (Cloud, Control Plane): "provides
    forensic access information for a variety of operations in the Temporal Cloud Control
    Plane"; "do not capture data plane events, such as Workflow Start, Workflow Terminate";
    exige papel "Account Owner or Global Administrator".
  - https://docs.temporal.io/cloud/metrics — Observabilidade (Cloud + SDK); recomenda "create
    monitors and alerts"; baseada em OpenMetrics.
  - https://docs.temporal.io/workers — Workers e Task Queues: Worker "responsible for polling
    a Task Queue, dequeueing a Task, executing your code in response to a Task"; identidade
    "\${process.pid}@\${os.hostname()}".
  - https://docs.temporal.io/workflow-execution — Ciclo de vida: "Paused: The Workflow
    Execution has been Paused"; "doesn't dispatch new Workflow Tasks until the Workflow
    Execution is Unpaused"; "A Workflow Execution is uniquely identified by its Namespace,
    Workflow Id, and Run Id"; status Open/Closed.
  - https://docs.temporal.io/visibility — Visibility: List Filters SQL-like, Search Attributes,
    Count API com GROUP BY; "Batch operations: `ListBatchOperations`".
  - https://docs.temporal.io/schedules — Schedules: "A Schedule can be Paused"; Overlap
    Policy (Skip default, BufferOne, CancelOther, TerminateOther...).
  - https://docs.temporal.io/nexus — Nexus: "connects Temporal Applications across (and within)
    isolated Namespaces"; "Nexus is peer-to-peer, not hierarchical".
  - https://docs.temporal.io/encyclopedia/workflow-message-passing — Mensageria: "Workflows
    can be thought of as stateful web services that can receive messages"; Signals, Updates,
    Queries.
  - https://docs.temporal.io/mcp — Servidor MCP (Model Context Protocol) em
    `https://temporal.mcp.kapa.ai`, "Connect Temporal expertise directly to your AI assistant".
  - https://docs.temporal.io/cli — Temporal CLI: "local Temporal development service",
    `temporal server start-dev`; extensão para o Cloud.
  - https://docs.temporal.io/self-hosted-guide — Auto-hospedagem: opções Docker/Kubernetes/
    manual; "Configure TLS/mTLS, authentication, authorization"; nenhum RBAC nomeado.
  - https://docs.temporal.io/security — Apenas página-índice; não trata de autorização/RBAC.
  - https://docs.temporal.io/visibility/batch-operations — **HTTP 404**.
  - https://docs.temporal.io/batch-operations — **HTTP 404**.

## Tabela fixa (spec 073)

| Grupo | Item | Resultado | Fonte (URL — o que foi visto) |
|---|---|---|---|
| CONTROLE | subir/derrubar sessão ou agente | sim | docs.temporal.io/web-ui — botão "Start Workflow Like This One" e "Workflow Actions" com "request Cancellation" / "Reset/Terminate"; docs.temporal.io/references/web-ui-configuration — chaves `startWorkflowDisabled` e `workflowTerminateDisabled` (existem ações de iniciar/terminar) |
| CONTROLE | pausar | sim | docs.temporal.io/references/web-ui-configuration — chave `workflowPauseDisabled`; docs.temporal.io/workflow-execution — "Paused: The Workflow Execution has been Paused"; docs.temporal.io/schedules — "A Schedule can be Paused" |
| CONTROLE | retomar | sim | docs.temporal.io/workflow-execution — "doesn't dispatch new Workflow Tasks until the Workflow Execution is Unpaused" (existe o despausar) |
| CONTROLE | limites de orçamento e de taxa | parcial | docs.temporal.io/cloud/limits — "Default limit: 500 actions per second (APS)"; RPS dinâmico; throttling. **Só taxa (Cloud); não achei limite/orçamento monetário** |
| CONTROLE | políticas allow/deny/ask | — | — |
| CONTROLE | aprovação humana | — | — |
| ADMINISTRAÇÃO | cadastro de agentes | — | — |
| ADMINISTRAÇÃO | papéis e permissões RBAC | parcial | docs.temporal.io/cloud/manage-access/users — papeis Global Admin/Developer/Read-Only/Account Owner/Finance Admin e Namespace Admin/Write/Read-Only; **só no Temporal Cloud**; docs.temporal.io/references/web-ui-configuration — `auth` "controls who can access the Web UI, not authorization" (self-hosted sem autorização) |
| ADMINISTRAÇÃO | cadastro de skills/ferramentas/modelos | — | — |
| ADMINISTRAÇÃO | chaves e segredos | sim | docs.temporal.io/cloud/api-keys — API keys "displayed only once for security purposes", "You can enable or disable API keys"; alternativa ao mTLS (Cloud) |
| ADMINISTRAÇÃO | configuração por projeto | sim | docs.temporal.io/web-ui — lista e seletor de **Namespaces**; docs.temporal.io/cloud/manage-access/users — permissões no nível de Namespace |
| ADMINISTRAÇÃO | auditoria | parcial | docs.temporal.io/cloud/audit-logs — Audit Logs do Control Plane, "You need the Account Owner or Global Administrator role"; **não captura eventos de data plane**; só Cloud |
| GERENCIAMENTO | lista de agentes vivos com estado | parcial | docs.temporal.io/web-ui — aba **Workers**: "Displays the Workers currently polling on the Workflow Task Queue with a count". O *worker* é **processo que faz polling** de uma Task Queue, **não** um agente (a própria ficha registra: "Workers são efêmeros e apenas fazem *polling*") — por isso **parcial**, não sim |
| GERENCIAMENTO | tarefa aberta | parcial | docs.temporal.io/web-ui — "The main Workflows page displays a table of all Workflow Executions"; docs.temporal.io/workflow-execution — status "Open" / "Running: The Workflow Execution is actively progressing". É a lista de **execuções de workflow** (a unidade de trabalho do motor), **não** a tarefa aberta de um agente — por isso **parcial** |
| GERENCIAMENTO | última atividade | parcial | docs.temporal.io/web-ui — Metadata da History com "Start/Close Time and Duration", "State Transitions" e "Current Details"; docs.temporal.io/workers — Worker Identity por processo |
| GERENCIAMENTO | consumo por agente/sessão/modelo | parcial | docs.temporal.io/web-ui — Metadata traz "Billable Actions Count" (só Cloud); docs.temporal.io/cloud/metrics — métricas com "Namespace-level activity" |
| GERENCIAMENTO | custo | parcial | docs.temporal.io/web-ui — "Billable Actions Count" (só Cloud); docs.temporal.io/cloud/manage-access/users — papel **Finance Admin** "Has permissions to view billing information" |
| GERENCIAMENTO | filas e workers | sim | docs.temporal.io/workers — Worker "responsible for polling a Task Queue"; docs.temporal.io/web-ui — aba Workers e "Pending Activities" |
| GERENCIAMENTO | rastro/replay de sessão | sim | docs.temporal.io/web-ui — History em Timeline/All/Compact/JSON, "Download Event History", ação "Reset"/"Reset/Terminate"; docs.temporal.io/visibility — "event history" |
| GERENCIAMENTO | alertas | parcial | docs.temporal.io/cloud/metrics — texto recomenda "create monitors and alerts" / "route alerts to your monitoring tools" (orientação, não um produto de alertas embutido) |
| INTERCOMUNICAÇÃO | mensagem entre agentes | sim | docs.temporal.io/encyclopedia/workflow-message-passing — "stateful web services that can receive messages"; Signals "asynchronous write requests", Updates "synchronous, tracked write requests" |
| INTERCOMUNICAÇÃO | protocolos (A2A, MCP) | parcial | docs.temporal.io/nexus — "Nexus connects Temporal Applications across (and within) isolated Namespaces" (protocolo de interoperabilidade); docs.temporal.io/mcp — servidor MCP em `temporal.mcp.kapa.ai`. **A2A não encontrado** |
| INTERCOMUNICAÇÃO | caixa de entrada | — | — |
| INTERCOMUNICAÇÃO | roteamento por nome/ref | sim | docs.temporal.io/workers — Worker Entity "listens and polls on a single Task Queue"; docs.temporal.io/nexus — "Callers never need to know the handler's Namespace, Task Queue, or internal implementation" (Endpoints) |
| INTERCOMUNICAÇÃO | livro de mensagens | — | — |
| INTERCOMUNICAÇÃO | colisão de nomes | parcial | docs.temporal.io/workflow-execution — "A Workflow Execution is uniquely identified by its Namespace, Workflow Id, and Run Id"; "Workflow Execution Chain is a sequence of Workflow Executions that share the same Workflow Id" (identidade evita colisão; não achei a política de reúso de Id documentada nas páginas abertas) |

## Observações

- **Raia**: a Temporal Web UI é a interface do **Temporal Server** (auto-hospedado) e também é
  oferecida no **Temporal Cloud**. Várias capacidades de administração (RBAC, auditoria,
  API keys, limites, "Billable Actions Count") são **exclusivas do Temporal Cloud**; o
  self-hosted não tem autorização embutida (a configuração `auth` "controls who can access the
  Web UI, not authorization").
- **Não achei** (célula vazia) conceitos de: política `allow/deny/ask`, aprovação humana,
  "cadastro de agentes" (Workers são efêmeros e apenas fazem *polling*), catálogo de skills/
  ferramentas/modelos, "caixa de entrada" e "livro de mensagens". Signals/Updates são o mais
  próximo de mensageria, mas não há um *inbox* persistente nomeado.
- **Tentado e não obtido**: `docs.temporal.io/visibility/batch-operations` e
  `docs.temporal.io/batch-operations` retornaram **HTTP 404**. As ações em lote aparecem
  apenas descritas indiretamente (chave `batchActionsDisabled` e `ListBatchOperations`).
- **Ambiente local**: `temporal` **não** está instalado e `docker` **não** existe nesta
  máquina — nada foi executado; a pesquisa é 100% documental.
- **Limite de custo**: a página de limites não trata de orçamento monetário; "custo" só
  aparece como "Billable Actions Count" (Cloud) e papel Finance Admin. Marquei como
  **parcial** por isso.
