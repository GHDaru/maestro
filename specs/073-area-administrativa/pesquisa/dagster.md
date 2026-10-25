# Dagster

- **URL**: https://dagster.io/docs (https://docs.dagster.io redireciona para cá)
- **Data da visita**: 2026-10-24
- **Como foi pesquisada**: WebFetch na documentação oficial (dagster.io/docs). Nenhum binário local foi executado (a instalação via `pip` foi considerada pesada e dispensada).
- **O que foi aberto de verdade**:
  - https://dagster.io/docs — porta de entrada: descreve o Dagster como "a data orchestrator built for data engineers" e lista as seções (Build, Automate, Operate, Observe, Test, Labs).
  - https://dagster.io/docs/getting-started/concepts — conceitos: asset, asset check, code location, job, op, resource, schedule, sensor.
  - https://dagster.io/docs/guides/operate/webserver — webserver/UI: páginas Overview, Assets (Asset catalog), Runs, Schedules e Sensors, Resources, Backfills, Jobs (com Launchpad), Deployment.
  - https://dagster.io/docs/guides/operate/managing-concurrency — run queue limits, concurrency pools, run executor e run tag limits.
  - https://dagster.io/docs/guides/operate/configuration — índice da configuração (run configuration, env vars e secrets).
  - https://dagster.io/docs/guides/operate/configuration/using-environment-variables-and-secrets — `dg.EnvVar` vs `os.getenv` e gestão de segredos.
  - https://dagster.io/docs/guides/operate/ui-user-settings — configurações de usuário na UI (timezone, tema, feature flags).
  - https://dagster.io/docs/guides/operate — índice da seção Operate.
  - https://dagster.io/docs/guides/automate/schedules — schedules por cron/intervalo.
  - https://dagster.io/docs/guides/automate/sensors — sensors, `DefaultSensorStatus.RUNNING`/`STOPPED`.
  - https://dagster.io/docs/guides/observe/alerts — visão geral dos alertas (Dagster+).
  - https://dagster.io/docs/guides/observe/alerts/alert-policy-types — os 7 tipos de política de alerta e canal.
  - https://dagster.io/docs/guides/observe/insights — Insights (métricas de uso e "Dagster credits").
  - https://dagster.io/docs/guides/observe/asset-catalog — Asset catalog (Dagster+).
  - https://dagster.io/docs/deployment — visão geral: Dagster+ (Serverless/Hybrid) vs Dagster OSS.
  - https://dagster.io/docs/deployment/oss — índice do deploy OSS.
  - https://dagster.io/docs/dagster-plus — entrou em https://dagster.io/docs/deployment/dagster-plus: seções do Dagster+.
  - https://dagster.io/docs/deployment/dagster-plus/hybrid — agentes Hybrid.
  - https://dagster.io/docs/deployment/dagster-plus/management — índice de config/gestão do Dagster+.
  - https://dagster.io/docs/deployment/dagster-plus/management/environment-variables — variáveis/segredos escopados por deployment/code location.
  - https://dagster.io/docs/deployment/dagster-plus/management/rate-limits — limites de eventos/logs por minuto.
  - https://dagster.io/docs/deployment/dagster-plus/management/credit-usage — o que consome "credits".
  - https://dagster.io/docs/deployment/dagster-plus/management/tokens — índice de tokens (agent/user tokens).
  - https://dagster.io/docs/deployment/dagster-plus/authentication-and-access-control/rbac — índice do RBAC (*Role-Based Access Control*).
  - https://dagster.io/docs/deployment/dagster-plus/authentication-and-access-control/rbac/user-roles-permissions — nomes e permissões dos papéis.
  - https://dagster.io/docs/deployment/dagster-plus/authentication-and-access-control/rbac/audit-logs — audit logs do Dagster+ Pro.
  - https://dagster.io/docs/getting-started/ai-tools — ferramentas de IA e o "Dagster+ MCP".

## Tabela fixa (spec 073)

| Grupo | Item | Resultado | Fonte (URL — o que foi visto) |
|---|---|---|---|
| CONTROLE | subir/derrubar sessão ou agente | parcial | https://dagster.io/docs/guides/operate/webserver — a aba Jobs tem o "Launchpad", "a configuration editor to let you experiment with configuration and launch runs"; https://dagster.io/docs/deployment/dagster-plus/authentication-and-access-control/rbac/user-roles-permissions — papel Launcher: "Launch, re-execute, terminate, and delete runs of jobs". Sobe/derruba runs, não agentes de IA. |
| CONTROLE | pausar | parcial | https://dagster.io/docs/guides/automate/sensors — `DefaultSensorStatus.STOPPED` "To explicitly disable a sensor"; https://dagster.io/docs/deployment/dagster-plus/authentication-and-access-control/rbac/user-roles-permissions — Editor pode "Start and stop schedules" e Launcher "Launch and cancel schedules". |
| CONTROLE | retomar | parcial | https://dagster.io/docs/guides/automate/sensors — `DefaultSensorStatus.RUNNING` habilita o sensor, feito em "Automation > Sensors" na UI; https://dagster.io/docs/deployment/dagster-plus/authentication-and-access-control/rbac/user-roles-permissions — "Start and stop schedules". |
| CONTROLE | limites de orçamento e de taxa | parcial | https://dagster.io/docs/deployment/dagster-plus/management/rate-limits — "40,000 user log events ... per minute" e "100MB of events per minute" por deployment, com "429 - Too Many Requests"; https://dagster.io/docs/guides/observe/alerts/alert-policy-types — política "Credit budget" (Experimental, Serverless) dispara no limite mensal de credits; https://dagster.io/docs/guides/operate/managing-concurrency — "Run queue limits" e "Concurrency pools". |
| CONTROLE | políticas allow/deny/ask | parcial | https://dagster.io/docs/deployment/dagster-plus/authentication-and-access-control/rbac/user-roles-permissions — modelo hierárquico em que cada papel "includes permissions specific to this role and all permissions in the" papéis abaixo. É concessão de permissão ("allow"); não há "deny" nem "ask". |
| CONTROLE | aprovação humana | — | — |
| ADMINISTRAÇÃO | cadastro de agentes | parcial | https://dagster.io/docs/deployment/dagster-plus/hybrid — "your code runs inside containers managed by an agent you operate" (Kubernetes/ECS/Docker/Azure); https://dagster.io/docs/deployment/dagster-plus/authentication-and-access-control/rbac/audit-logs — eventos "Create agent token"/"Revoke agent token". Agentes de execução, não de IA. |
| ADMINISTRAÇÃO | papéis e permissões RBAC | sim | https://dagster.io/docs/deployment/dagster-plus/authentication-and-access-control/rbac/user-roles-permissions — papéis Organization Admin, Admin, Editor, Launcher ("Pro plans only") e Viewer, com permissões detalhadas e escopo por deployment. |
| ADMINISTRAÇÃO | cadastro de skills/ferramentas/modelos | — | — |
| ADMINISTRAÇÃO | chaves e segredos | sim | https://dagster.io/docs/guides/operate/configuration/using-environment-variables-and-secrets — `dg.EnvVar` ("the variable's value is retrieved at runtime and **won't** be visible in the UI") vs `os.getenv`; https://dagster.io/docs/deployment/dagster-plus/management/environment-variables — no Dagster+ a UI guarda variáveis com "Amazon Key Management Services (KMS) and envelope encryption". |
| ADMINISTRAÇÃO | configuração por projeto | sim | https://dagster.io/docs/getting-started/concepts — "Code location ... a collection of Dagster entity definitions deployed in a specific environment"; https://dagster.io/docs/deployment/dagster-plus/management/environment-variables — variáveis "Scoped by deployment (full and branch) and optionally, code location". |
| ADMINISTRAÇÃO | auditoria | sim | https://dagster.io/docs/deployment/dagster-plus/authentication-and-access-control/rbac/audit-logs — "The Dagster+ audit log enables Dagster+ Pro organizations to track and attribute changes", com eventos (log in, update sensor/schedule, create/update/delete code location, create/update/delete secret) e campos `id`, `eventType`, `authorUserEmail`, `timestamp`. |
| GERENCIAMENTO | lista de agentes vivos com estado | parcial | https://dagster.io/docs/guides/observe/alerts/alert-policy-types — política "Agent downtime": "Triggers when a Hybrid agent hasn't heartbeated within the last five minutes". Confirma heartbeat de agentes; lista agentes de execução, não de IA. |
| GERENCIAMENTO | tarefa aberta | parcial | https://dagster.io/docs/guides/operate/webserver — página Runs, filtrável por "execution status"; https://dagster.io/docs/guides/observe/insights — métricas de deployment "Runs in progress" e "Runs queued". |
| GERENCIAMENTO | última atividade | parcial | https://dagster.io/docs/guides/operate/webserver — detalhe de schedule/sensor mostra "next tick, tick history, run history"; https://dagster.io/docs/deployment/dagster-plus/authentication-and-access-control/rbac/audit-logs — campo "timestamp" de cada entrada. |
| GERENCIAMENTO | consumo por agente/sessão/modelo | parcial | https://dagster.io/docs/guides/observe/insights — visões por "Assets, Selections, Jobs, and Deployments" com métricas como "Dagster credits", "Step execution time" e "Run duration"; não há corte por agente. |
| GERENCIAMENTO | custo | parcial | https://dagster.io/docs/deployment/dagster-plus/management/credit-usage — "1 credit per step execution" e "1 credit per asset materialization event"; https://dagster.io/docs/guides/observe/insights — "Dagster credits" como métrica de Jobs e Deployments (Dagster+ apenas). |
| GERENCIAMENTO | filas e workers | parcial | https://dagster.io/docs/guides/operate/managing-concurrency — "Run queue limits" (escopo Deployment) para evitar "Too many simultaneous runs"; o Dagster não tem o conceito de "worker" — usa agentes (ver https://dagster.io/docs/deployment/dagster-plus/hybrid). |
| GERENCIAMENTO | rastro/replay de sessão | parcial | https://dagster.io/docs/deployment/dagster-plus/authentication-and-access-control/rbac/user-roles-permissions — permissão "re-execute" runs; https://dagster.io/docs/deployment/dagster-plus/management/credit-usage — "Re-executing a run is different — that creates new step executions"; https://dagster.io/docs/guides/operate/webserver — run logs em "Structured event logs" e "Raw compute logs". Re-execução e logs, não um replay de sessão. |
| GERENCIAMENTO | alertas | sim | https://dagster.io/docs/guides/observe/alerts — "This feature is only available in Dagster+"; https://dagster.io/docs/guides/observe/alerts/alert-policy-types — 7 tipos de política (Asset, Run, Code location, Automation, Agent downtime, Insights metric, Credit budget). |
| INTERCOMUNICAÇÃO | mensagem entre agentes | — | — |
| INTERCOMUNICAÇÃO | protocolos (A2A, MCP) | parcial | https://dagster.io/docs/getting-started/ai-tools — "Dagster+ MCP allows you to access information and take actions in your Dagster+ deployment" (MCP — *Model Context Protocol*); nenhuma menção a A2A (*Agent2Agent*) nas páginas abertas. |
| INTERCOMUNICAÇÃO | caixa de entrada | — | — |
| INTERCOMUNICAÇÃO | roteamento por nome/ref | — | — |
| INTERCOMUNICAÇÃO | livro de mensagens | — | — |
| INTERCOMUNICAÇÃO | colisão de nomes | — | — |

## Observações

- **Versão livre vs. paga (Dagster OSS vs. Dagster+).** O núcleo open source inclui assets, jobs, ops, resources, schedules, sensors, asset checks, a Dagster UI/webserver e a gestão de concorrência (run queue, pools). Marcados como "Dagster+ feature": **Alerts**, **Insights**, **Asset catalog** (versão nova), **RBAC**, **audit logs** (Dagster+ Pro), **environment variables geridas pela UI** e os limites de taxa/credits. Os alertas e o Asset catalog declaram explicitamente "only available in Dagster+" / "only available in Dagster+".
- **Custo/consumo.** O consumo é medido em "Dagster credits" (por step e por materialization), visível no Insights e detalhado na página de credit usage; não há consumo por agente/sessão/modelo (o corte é por asset/job/deployment).
- **Lacunas.** Não foram encontradas nas páginas abertas: aprovação humana (human-in-the-loop), mensagens entre agentes, caixa de entrada, livro de mensagens, roteamento por nome/ref ou tratamento de colisão de nomes. O conceito de "worker" do Prefect não existe no Dagster — o papel equivalente é o agente Hybrid.
- **MCP.** O Dagster+ expõe um servidor MCP ("Dagster+ MCP"); o plugin `dagster` também traz a skill `dagster-expert` para agentes de código.
