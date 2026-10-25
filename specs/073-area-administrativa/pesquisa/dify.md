# Dify — plataforma de aplicações com LLM (073-T1-W05)

- **URL**: https://dify.ai · https://docs.dify.ai/en/introduction (docs) · https://github.com/langgenius/dify (código)
- **Data da visita**: 2026-10-24
- **Aberto de verdade**:
  - `https://docs.dify.ai/en/introduction` — introdução: "one collaborative workspace", *Agent
    Sandbox*, canvas visual (chatflow/workflow), centenas de modelos suportados, *Tools* a partir
    de Marketplace/MCP/APIs, *plugin* dev, "Backend-as-a-Service" e "corresponding APIs",
    "LLMOps": monitorar e analisar logs e desempenho da aplicação ao longo do tempo,
    observabilidade por Langfuse/LangSmith/Phoenix/Opik, versão *Community* (MIT, self-host) e
    *Enterprise* (visto 24/10).
  - `https://github.com/langgenius/dify` — README: projeto *open source*, ~centenas de milhares de
    estrelas, deploy via Docker Compose, *Enterprise* com SSO/RBAC, edição de *plugins*, e o selo
    "Backend-as-a-Service" (visto 24/10).
- **Rodou local?**: **não** — nada instalado nem executado nesta máquina; sem capturas de tela.
- **Conta criada?**: **não** (a demo hospedada exigiria conta; não foi aberta).

Acrônimos: LLM (*Large Language Model*), LLMOps (*Large Language Model Operations*), RBAC
(*Role-Based Access Control*), SSO (*Single Sign-On*), MCP (*Model Context Protocol*), A2A
(*Agent-to-Agent*), API (*Application Programming Interface*), OSS (*Open Source Software*).

## Tabela fixa (spec 073)

### CONTROLE

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| subir/derrubar sessão ou agente | não — a aplicação roda ao ser publicada/usada; não há subir/derrubar de agente pela UI | `docs.dify.ai/en/introduction` (visto 24/10) |
| pausar | não — não descrito | `docs.dify.ai/en/introduction` (visto 24/10) |
| retomar | não — não descrito | `docs.dify.ai/en/introduction` (visto 24/10) |
| limites de orçamento e de taxa | não — não descrito nas fontes vistas | `docs.dify.ai/en/introduction` (visto 24/10) |
| políticas allow/deny/ask | não — não descrito nas fontes vistas | `docs.dify.ai/en/introduction` (visto 24/10) |
| aprovação humana | não — não descrito nas fontes vistas | `docs.dify.ai/en/introduction` (visto 24/10) |

### ADMINISTRAÇÃO

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| cadastro de agentes | parcial — constrói agentes num canvas visual; sem catálogo durável de agentes | `docs.dify.ai/en/introduction` (visto 24/10): "Agent Sandbox", canvas |
| papéis e permissões RBAC | parcial — *Enterprise* cita SSO e RBAC | `github.com/langgenius/dify` README (visto 24/10) |
| cadastro de skills/ferramentas/modelos | sim — modelos (centenas), ferramentas via Marketplace/MCP/APIs e desenvolvimento de *plugins* | `docs.dify.ai/en/introduction` + README (visto 24/10) |
| chaves e segredos | parcial — "Backend-as-a-Service"/"corresponding APIs" (chaves de API implícitas); gestão de chaves não descrita | `docs.dify.ai/en/introduction` (visto 24/10) |
| configuração por projeto | sim — "one collaborative workspace" como escopo de trabalho | `docs.dify.ai/en/introduction` (visto 24/10) |
| auditoria | não — não descrito nas fontes vistas | `docs.dify.ai/en/introduction` (visto 24/10) |

### GERENCIAMENTO

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| lista de agentes vivos com estado | não — não descrito nas fontes vistas | `docs.dify.ai/en/introduction` (visto 24/10) |
| tarefa aberta | não — não descrito nas fontes vistas | `docs.dify.ai/en/introduction` (visto 24/10) |
| última atividade | sim — LLMOps: "Monitor and analyze application logs and performance over time" | `docs.dify.ai/en/introduction` (visto 24/10) |
| consumo por agente/sessão/modelo | parcial — logs e observabilidade terceirizada (Langfuse/LangSmith/Phoenix/Opik) | `docs.dify.ai/en/introduction` (visto 24/10) |
| custo | parcial — via integrações de observabilidade citadas; métrica de custo própria não descrita | `docs.dify.ai/en/introduction` (visto 24/10) |
| filas e workers | não — não descrito nas fontes vistas | `docs.dify.ai/en/introduction` (visto 24/10) |
| rastro/replay de sessão | parcial — logs + observabilidade externa; *replay* nativo não citado | `docs.dify.ai/en/introduction` (visto 24/10) |
| alertas | não — não descrito nas fontes vistas | `docs.dify.ai/en/introduction` (visto 24/10) |

### INTERCOMUNICAÇÃO

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| mensagem entre agentes | não — não descrito nas fontes vistas | `docs.dify.ai/en/introduction` (visto 24/10) |
| protocolos (A2A; MCP) | parcial — suporte a MCP (conectar ferramentas); A2A não citado | `docs.dify.ai/en/introduction` (visto 24/10) |
| caixa de entrada | não — não descrito | `docs.dify.ai/en/introduction` (visto 24/10) |
| roteamento por nome/ref | não — não descrito | `docs.dify.ai/en/introduction` (visto 24/10) |
| livro de mensagens | não — não descrito | `docs.dify.ai/en/introduction` (visto 24/10) |
| colisão de nomes | não — não descrito | `docs.dify.ai/en/introduction` (visto 24/10) |
