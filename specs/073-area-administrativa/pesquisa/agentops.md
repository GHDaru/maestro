# AgentOps — observabilidade de agentes (073-T1-W05)

- **URL**: https://app.agentops.ai (produto) · https://docs.agentops.ai (docs) · https://github.com/AgentOps-AI/agentops (código)
- **Data da visita**: 2026-10-24
- **Aberto de verdade**:
  - `https://docs.agentops.ai/` — página inicial do produto: posicionamento ("observability and
    monitoring for your AI agents and LLM apps"), `agentops.init(<API KEY>)`, decorators
    (`@trace`, `@session`, `@agent`, `@operation`/`@task`, `@workflow`), `auto_start_session=False`,
    e as telas *Session Drilldown / Session Drawer / Session Waterfall / Session Overview* (visto 24/10).
  - `https://github.com/AgentOps-AI/agentops` — README: licença MIT, diretório `app/` para
    self-host ("Dashboard + API backend"), *Replay Analytics and Debugging* com "step-by-step
    agent execution graphs", *LLM Cost Management*, lista de integrações, `app.agentops.ai` como
    dashboard hospedado, `agentops_demo.mp4` (visto 24/10).
- **Rodou local?**: **não** — nada instalado nem executado nesta máquina; sem capturas de tela.
- **Conta criada?**: **não** (o dashboard `app.agentops.ai` exige conta; não foi aberto).

Acrônimos: LLM (*Large Language Model*), SDK (*Software Development Kit*), API (*Application
Programming Interface*), RBAC (*Role-Based Access Control*), MCP (*Model Context Protocol*),
A2A (*Agent-to-Agent*).

## Tabela fixa (spec 073)

### CONTROLE

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| subir/derrubar sessão ou agente | parcial — a **sessão** da SDK inicia/fecha sozinha e há `auto_start_session=False` para controle manual; não é subir/derrubar agente pela plataforma | `docs.agentops.ai` (visto 24/10): `auto_start_session=False`, "manual trace management" |
| pausar | — | `docs.agentops.ai` (visto 24/10) não descreve a função |
| retomar | — | `docs.agentops.ai` (visto 24/10) não descreve a função |
| limites de orçamento e de taxa | parcial — o README cita *flag* de estouro de tokens ("Token limit overflow flags"), que **detecta**, não configura limite | `github.com/AgentOps-AI/agentops` README (visto 24/10) |
| políticas allow/deny/ask | — | `docs.agentops.ai` (visto 24/10) não descreve a função |
| aprovação humana | — | `docs.agentops.ai` (visto 24/10) não descreve a função |

### ADMINISTRAÇÃO

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| cadastro de agentes | parcial — decorators (`@agent`, `@session`) registram agentes no código, sem catálogo/registro na plataforma | `docs.agentops.ai` (visto 24/10): decorators |
| papéis e permissões RBAC | — | `docs.agentops.ai` (visto 24/10) não descreve RBAC |
| cadastro de skills/ferramentas/modelos | parcial — instrumentação de ferramentas via `@operation`/`@task` e lista de integrações de framework/provedor; sem registro gerido | `docs.agentops.ai` + README (visto 24/10) |
| chaves e segredos | parcial — exige API key em `agentops.init(...)`; não há gestor de segredos descrito | `docs.agentops.ai` (visto 24/10): "INSERT YOUR API KEY HERE" |
| configuração por projeto | — | `docs.agentops.ai` (visto 24/10) não descreve projetos |
| auditoria | — | `docs.agentops.ai` (visto 24/10) não descreve auditoria |

### GERENCIAMENTO

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| lista de agentes vivos com estado | parcial — lista **sessões** (Session Overview), não agentes vivos com estado atual | `docs.agentops.ai` (visto 24/10): "Session Overview" |
| tarefa aberta | — | `docs.agentops.ai` (visto 24/10) não descreve tarefa corrente |
| última atividade | parcial — tempo total de execução da sessão e durações dos eventos | `docs.agentops.ai` (visto 24/10): "total execution time", "charts of event types and durations" |
| consumo por agente/sessão/modelo | parcial — métricas por sessão; sem quebra por modelo na página | `docs.agentops.ai` (visto 24/10): session-wide metrics |
| custo | parcial — "LLM Cost Management" é **linha de README**, não página que documente o mecanismo. Rebaixada de `sim` para `parcial` **na rodada 4 (26/10, juiz 2, P1)** | `github.com/AgentOps-AI/agentops` README (visto 24/10) |
| filas e workers | — | `docs.agentops.ai` (visto 24/10) não descreve filas/workers |
| rastro/replay de sessão | parcial — "Session Replays"/"Replay Analytics" aparecem só no **README** e na página de produto (`docs.agentops.ai/`), sem página que documente o mecanismo. Rebaixada de `sim` para `parcial` **na rodada 4 (26/10)** | README + `docs.agentops.ai` (visto 24/10) |
| alertas | parcial — não há alertas; há *Failure Detection* e flags de estouro de token (detecção, não notificação) | README (visto 24/10) |

### INTERCOMUNICAÇÃO

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| mensagem entre agentes | — | `docs.agentops.ai` (visto 24/10) não descreve mensageria entre agentes |
| protocolos (A2A; MCP) | parcial — só um *MCP Docs Server* (`npx mint-mcp add agentops`) para conversar com a **documentação**; nem A2A nem orquestração por MCP | `docs.agentops.ai` (visto 24/10) |
| caixa de entrada | — | `docs.agentops.ai` (visto 24/10) |
| roteamento por nome/ref | — | `docs.agentops.ai` (visto 24/10) |
| livro de mensagens | — | `docs.agentops.ai` (visto 24/10) |
| colisão de nomes | — | `docs.agentops.ai` (visto 24/10) |

**Correção da rodada 4 (26/10, fatia do Worker06).** Fontes desta ficha: 3 URLs (produto `app.agentops.ai`, docs, GitHub). As **duas** células `sim` da ficha — **custo** e **rastro/replay de sessão** — caíram para `parcial`: apoiavam-se só no README e na página de produto, sem página que documente o mecanismo (o juiz 3, P1, já registrava que os dois únicos `sim` vêm do README, não da UI).
