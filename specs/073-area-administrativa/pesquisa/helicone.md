# Helicone — observabilidade e gateway de LLM

- **URL**: https://www.helicone.ai/ · **Documentação**: https://docs.helicone.ai/
- **Data da visita**: 2026-10-24/25 (a sessão atravessou a meia-noite)
- **Nicho**: observabilidade de LLM (*Large Language Model*) com gateway próprio — *logs*,
  sessões, custo, limites de taxa e alertas
- **Modelo**: SaaS (nuvem) com versão de código aberto auto-hospedável (exigiria Docker,
  indisponível nesta máquina)

## O que foi aberto de verdade

**Não rodou local** (SaaS; a auto-hospedagem pede Docker e não há Docker nesta máquina).
Páginas abertas em 2026-10-24:

- https://docs.helicone.ai/llms.txt — índice completo da documentação
- https://docs.helicone.ai/getting-started/platform-overview.md — panorama: "AI Gateway",
  "Every request, searchable", "Session Debugging", "user tracking", "Cost Tracking",
  "Prompt Management", "Custom Rate Limits", "Caching", "LLM Security"
- https://docs.helicone.ai/features/sessions.md — sessões (`Helicone-Session-Id`,
  `Helicone-Session-Path`, `Helicone-Session-Name`)
- https://docs.helicone.ai/features/advanced-usage/user-metrics.md — métricas de usuário
  (`Helicone-User-Id`)
- https://docs.helicone.ai/features/advanced-usage/custom-rate-limits.md — limite de taxa
  customizado (`Helicone-RateLimit-Policy`)
- https://docs.helicone.ai/features/alerts.md — alertas
- https://docs.helicone.ai/integrations/tools/mcp.md — servidor MCP (*Model Context
  Protocol*) da Helicone

## Tabela fixa (spec.md § "Tabela fixa de funcionalidades")

### CONTROLE

| Funcionalidade | Resposta | Fonte (URL + o que foi visto) |
|---|---|---|
| Subir/derrubar sessão ou agente | não | `features/sessions.md`: sessão é agrupamento lógico de requisições — criada mandando `Helicone-Session-Id`/`-Path`/`-Name` no cabeçalho; não sobe nem derruba processo |
| Pausar | — | nenhuma página aberta |
| Retomar | — | nenhuma página aberta |
| Limites de orçamento e de taxa | parcial | `custom-rate-limits.md`: cabeçalho `Helicone-RateLimit-Policy` no formato `[quota];w=[time_window];u=[unit];s=[segment]`, com `u` = `"request"` (padrão) ou `"cents"`, escopo global, por usuário (`s=user`) ou por propriedade; estouro devolve **429**; cabeçalhos `Helicone-RateLimit-Limit`/`-Remaining`. **Orçamento por período (mensal/semanal) não aparece** |
| Políticas allow/deny/ask | parcial | `custom-rate-limits.md`: a única política documentada é a de taxa, que **nega** com 429; `platform-overview.md` lista "LLM Security" (página não aberta). Sem allow/deny/ask |
| Aprovação humana | — | nenhuma página aberta |

### ADMINISTRAÇÃO

| Funcionalidade | Resposta | Fonte (URL + o que foi visto) |
|---|---|---|
| Cadastro de agentes | — | `llms.txt` (índice) não tem nenhuma página de agentes; `platform-overview.md` lista apenas sessões, usuários, custo, prompts, limites, cache e gateway |
| Papéis e permissões RBAC | — | `llms.txt`: "Organizations — No dedicated pages appear in this index"; nenhuma página de papéis/permissões apareceu |
| Cadastro de skills/ferramentas/modelos | parcial | `platform-overview.md`: "Prompt Management" e "prompt versioning" (catálogo de *prompts*, não de ferramentas/modelos); `integrations/tools/mcp.md`: a Helicone **expõe** um servidor MCP, não cadastra ferramentas de terceiros |
| Chaves e segredos | parcial | `integrations/tools/mcp.md`: `HELICONE_API_KEY` (variável de ambiente do servidor MCP); `llms.txt`: "API keys — No dedicated pages appear in this index"; a página inicial aponta para `https://us.helicone.ai/settings/api-keys` (console, não aberto) |
| Configuração por projeto | — | `llms.txt` não traz página de organização/projeto; nada aberto sobre configuração por projeto |
| Auditoria | — | `llms.txt`: nenhuma página de auditoria em 147 de docs (o termo não aparece no índice nem em `platform-overview.md`) |

### GERENCIAMENTO

| Funcionalidade | Resposta | Fonte (URL + o que foi visto) |
|---|---|---|
| Lista de agentes vivos com estado | não | `platform-overview.md` descreve requisições, sessões e usuários — não há agente como entidade |
| Tarefa aberta | — | nenhuma página aberta |
| Última atividade | sim | `platform-overview.md`: "Every request is logged", "Every request, searchable"; `features/sessions.md`: a sessão mostra a árvore de chamadas ("trace the entire agent flow") com carimbo de tempo em cada requisição |
| Consumo por agente/sessão/modelo | parcial | `features/sessions.md`: métricas de sessão (`session_length_avg`, duração, mensagens por sessão) em `user-metrics.md`; `user-metrics.md` registra que **não** há métrica de custo nem de *tokens* por usuário — só "Request complexity - Token length". Por agente não aparece |
| Custo | sim | `platform-overview.md`: "Cost Tracking" com quebra "by user, feature, or any custom dimension"; `guides/cookbooks/cost-tracking.md` e `references/how-we-calculate-cost.md` (índice) |
| Filas e workers | — | nenhuma página aberta |
| Rastro/replay de sessão | parcial | `features/sessions.md`: sessão = rastro completo do fluxo do agente (LLM, vetor, ferramentas, "Any logged request") com hierarquia por `Helicone-Session-Path`; o índice lista o *cookbook* "Replaying LLM Sessions" (`guides/cookbooks/replay-session.md`), **não aberto** |
| Alertas | sim | `features/alerts.md`: métricas "Error Rate", "Cost", "Latency", "Total Tokens", "Prompt Tokens", "Completion Tokens", "Prompt Cache Read", "Prompt Cache Write", "Count", com "Time Frame", "Min Requests", "Grouping", "Aggregation" (Sum/Average/Min/Max/Percentile) e "Filter"; entrega por **Email** e **Slack** |

### INTERCOMUNICAÇÃO

| Funcionalidade | Resposta | Fonte (URL + o que foi visto) |
|---|---|---|
| Mensagem entre agentes | não | `platform-overview.md` e `llms.txt` não trazem mensageria; a entidade "agente" não existe |
| Protocolos (A2A; MCP) | parcial | MCP **parcial**: `integrations/tools/mcp.md` — a Helicone expõe um **servidor MCP** (`@helicone/mcp@latest`, ferramentas `query_requests` e `query_sessions`) para assistentes consultarem os dados dela; **não é gateway** para servidores MCP de terceiros. **A2A** (*Agent-to-Agent*) não aparece |
| Caixa de entrada | — | nenhuma página aberta |
| Roteamento por nome/ref | — | nenhuma página aberta |
| Livro de mensagens | — | nenhuma página aberta |
| Colisão de nomes | — | nenhuma página aberta |

## Observações para a rodada 2

- A Helicone é **observabilidade**, não administração: nada de papel, projeto, agente ou
  auditoria; a força está em **sessão como rastro** (árvore de chamadas) e **custo por
  dimensão customizada**.
- Dois itens aproveitáveis como referência de desenho: a **sessão por cabeçalho**
  (`Helicone-Session-Id` + `-Path` + `-Name`, com `Path` em sintaxe `/a/b/c` desenhando a
  árvore) e o **limite de taxa declarativo num cabeçalho**
  (`[quota];w=[janela];u=[request|cents];s=[escopo]`).
