# Langfuse — observabilidade de LLM e agentes (073-T1-W05)

- **URL**: https://langfuse.com · https://langfuse.com/docs (docs) · https://github.com/langfuse/langfuse (código)
- **Data da visita**: 2026-10-24
- **Aberto de verdade**:
  - `https://langfuse.com/docs` — visão do produto: tracing via OpenTelemetry, *Sessions* para
    conversas/workflows multi-passo, dashboard de qualidade/custo/latência, *alerts* por
    Slack/GitHub Actions/Webhook por limiar, gestão de prompts com versionamento e labels,
    avaliações (LLM-as-a-judge, code evaluators, annotation queues), e menção a *MCP server*/CLI
    para configurar (visto 24/10).
  - `https://langfuse.com/security` — RBAC, `projectId` e API keys por projeto, SSO/SCIM,
    *audit logs*, retenção/mascaramento/exclusão de dados; licenciamento: OSS MIT self-hostable
    + *Enterprise Edition* comercial (visto 24/10).
  - `https://langfuse.com/docs/demo` — a "demo pública" aponta para
    `https://langfuse.com/cloud/demo`, um **projeto compartilhado** que exige **criar conta**
    (sem acesso anônimo somente-leitura). **Não foi aberta** (a regra do ciclo proíbe criar conta).
- **Rodou local?**: **não** — nada instalado nem executado nesta máquina; sem capturas de tela.
- **Conta criada?**: **não**.

Acrônimos: LLM (*Large Language Model*), RBAC (*Role-Based Access Control*), SSO (*Single
Sign-On*), SCIM (*System for Cross-domain Identity Management*), API (*Application Programming
Interface*), MCP (*Model Context Protocol*), A2A (*Agent-to-Agent*), OSS (*Open Source Software*),
SDK (*Software Development Kit*).

## Tabela fixa (spec 073)

### CONTROLE

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| subir/derrubar sessão ou agente | — | `langfuse.com/docs` (visto 24/10) não descreve controle de execução |
| pausar | — | `langfuse.com/docs` (visto 24/10) |
| retomar | — | `langfuse.com/docs` (visto 24/10) |
| limites de orçamento e de taxa | — | `langfuse.com/docs` (visto 24/10) não descreve limite de orçamento |
| políticas allow/deny/ask | — | `langfuse.com/docs` (visto 24/10) |
| aprovação humana | parcial — há *annotation queues* e rotulagem manual (revisão humana), não portão de aprovação de execução | `langfuse.com/docs` (visto 24/10): "annotation queues", "manual labeling" |

### ADMINISTRAÇÃO

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| cadastro de agentes | — | `langfuse.com/docs` (visto 24/10) |
| papéis e permissões RBAC | sim — "Requests are checked via RBAC before any query runs"; SSO/SCIM | `langfuse.com/security` (visto 24/10) |
| cadastro de skills/ferramentas/modelos | parcial — gestão de *prompts* (versão/labels) e playground; sem registro de ferramentas | `langfuse.com/docs` (visto 24/10): prompt management |
| chaves e segredos | sim — "API keys are project-scoped" | `langfuse.com/security` (visto 24/10) |
| configuração por projeto | sim — "Every record is associated with a `projectId`" (projetos como escopo) | `langfuse.com/security` (visto 24/10) |
| auditoria | sim — *audit logs* listados entre os controles | `langfuse.com/security` (visto 24/10) |

### GERENCIAMENTO

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| lista de agentes vivos com estado | — | `langfuse.com/docs` (visto 24/10) |
| tarefa aberta | — | `langfuse.com/docs` (visto 24/10) |
| última atividade | parcial — *timeline view* de traces e sessões com carimbos de tempo | `langfuse.com/docs` (visto 24/10): "traces, a timeline view for debugging latency" |
| consumo por agente/sessão/modelo | parcial — custo/uso por `userId` e métricas de sessão; quebra por modelo não consta da página | `langfuse.com/docs` (visto 24/10): "monitor costs and usage per user" |
| custo | sim — "Quality, cost, and latency metrics" no dashboard | `langfuse.com/docs` (visto 24/10) |
| filas e workers | — | `langfuse.com/docs` (visto 24/10) |
| rastro/replay de sessão | parcial — *Sessions* rastreiam o workflow multi-passo e há *timeline view*; "no dedicated replay feature is documented here" | `langfuse.com/docs` (visto 24/10) |
| alertas | sim — notificação por Slack, GitHub Actions ou Webhook quando a métrica cruza o limiar | `langfuse.com/docs` (visto 24/10) |

### INTERCOMUNICAÇÃO

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| mensagem entre agentes | — | `langfuse.com/docs` (visto 24/10) |
| protocolos (A2A; MCP) | parcial — só um *MCP server* para configurar/consultar o projeto ("Halo"); nem A2A | `langfuse.com/docs` (visto 24/10) |
| caixa de entrada | — | `langfuse.com/docs` (visto 24/10) |
| roteamento por nome/ref | — | `langfuse.com/docs` (visto 24/10) |
| livro de mensagens | — | `langfuse.com/docs` (visto 24/10) |
| colisão de nomes | — | `langfuse.com/docs` (visto 24/10) |
