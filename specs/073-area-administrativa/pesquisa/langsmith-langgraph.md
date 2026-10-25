# LangSmith / LangGraph Platform — observabilidade e runtime de agentes (073-T1-W05)

- **URL**: https://docs.langchain.com/langsmith (LangSmith) · https://docs.langchain.com/langgraph (LangGraph/LangGraph Platform)
- **Data da visita**: 2026-10-24
- **Aberto de verdade**:
  - `https://docs.langchain.com/langsmith` (a antiga `docs.smith.langchain.com` redireciona para
    cá) — visão do LangSmith: rastreio ("full visibility into your LLM application"), avaliação,
    "Build dashboards and set alerts", API keys em *Settings*, *threads* (traces como fio),
    "cloud, hybrid, or self-hosted", automações/webhooks, anotação e feedback (visto 24/10).
  - `https://docs.langchain.com/langgraph` — o runtime: "low-level orchestration framework and
    runtime", pilha = *durable execution, streaming, human-in-the-loop, persistence*; "incorporate
    human oversight by inspecting and modifying agent state at any point"; *LangSmith Deployment*
    como plataforma de implantação; *LangSmith Fleet* (construtor sem código) (visto 24/10).
- **Rodou local?**: **não** — nada instalado nem executado nesta máquina; sem capturas de tela.
- **Conta criada?**: **não**.

Acrônimos: LLM (*Large Language Model*), API (*Application Programming Interface*), RBAC
(*Role-Based Access Control*), MCP (*Model Context Protocol*), A2A (*Agent-to-Agent*), SDK
(*Software Development Kit*).

## Tabela fixa (spec 073)

### CONTROLE

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| subir/derrubar sessão ou agente | parcial — *LangSmith Deployment* implanta/gerencia *deploys* de agentes; não há subir/derrubar de uma entidade viva na UI | `docs.langchain.com/langgraph` (visto 24/10): "LangSmith Deployment ... deploy ... agents" |
| pausar | não — não descrito nas páginas vistas | `docs.langchain.com/langgraph` (visto 24/10) não descreve pausar |
| retomar | parcial — *durable execution/persistence*: o run retoma de onde parou; não é um "retomar" acionado por humano | `docs.langchain.com/langgraph` (visto 24/10): "resuming from where they left off" |
| limites de orçamento e de taxa | parcial — limites de uso são assunto de *billing* ("pricing, retention, and limits"), não política do agente | `docs.langchain.com/langsmith` (visto 24/10): "Usage and billing" |
| políticas allow/deny/ask | não — não descrito | `docs.langchain.com/langsmith` (visto 24/10) |
| aprovação humana | sim — *human-in-the-loop*: inspecionar e modificar o estado do agente a qualquer ponto (interrupts) | `docs.langchain.com/langgraph` (visto 24/10) |

### ADMINISTRAÇÃO

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| cadastro de agentes | parcial — *LangSmith Fleet* (construtor sem código) e "discover, reuse, configure, and share agents" | `docs.langchain.com/langgraph` (visto 24/10) |
| papéis e permissões RBAC | não — não abordado nas páginas vistas | `docs.langchain.com/langsmith` (visto 24/10) não descreve RBAC |
| cadastro de skills/ferramentas/modelos | parcial — *prompt engineering*/gestão de prompts; sem registro de ferramentas/modelos | `docs.langchain.com/langsmith` (visto 24/10) |
| chaves e segredos | parcial — API keys criadas em *Settings → API Keys* e guardadas; sem gestor de segredos descrito | `docs.langchain.com/langsmith` (visto 24/10) |
| configuração por projeto | não — organizações/workspaces não abordados | `docs.langchain.com/langsmith` (visto 24/10) |
| auditoria | não — *audit logs* não abordados nas páginas vistas | `docs.langchain.com/langsmith` (visto 24/10) |

### GERENCIAMENTO

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| lista de agentes vivos com estado | não — mostra traces/threads, não agentes vivos | `docs.langchain.com/langsmith` (visto 24/10) |
| tarefa aberta | não — não descrito | `docs.langchain.com/langsmith` (visto 24/10) |
| última atividade | parcial — traces como *threads* com visões Messages/Turns/Details | `docs.langchain.com/langsmith` (visto 24/10) |
| consumo por agente/sessão/modelo | não — só remete a *billing*; sem quebra por agente/modelo na página | `docs.langchain.com/langsmith` (visto 24/10) |
| custo | parcial — assunto de *billing/usage*; sem métrica de custo por agente na página | `docs.langchain.com/langsmith` (visto 24/10) |
| filas e workers | não — não abordado nas páginas vistas | `docs.langchain.com/langgraph` (visto 24/10) |
| rastro/replay de sessão | sim — rastreio completo e *threads*; "Trace requests, evaluate outputs, and monitor deployments in one place" | `docs.langchain.com/langsmith` + `/langgraph` (visto 24/10) |
| alertas | sim — "Build dashboards and set alerts to track quality and catch issues early" | `docs.langchain.com/langsmith` (visto 24/10) |

### INTERCOMUNICAÇÃO

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| mensagem entre agentes | não — não descrito | `docs.langchain.com/langgraph` (visto 24/10) |
| protocolos (A2A; MCP) | parcial — MCP só como "conecte estes docs ao seu agente"; nem A2A | `docs.langchain.com/langsmith` (visto 24/10) |
| caixa de entrada | não — não descrito | `docs.langchain.com/langsmith` (visto 24/10) |
| roteamento por nome/ref | não — não descrito | `docs.langchain.com/langsmith` (visto 24/10) |
| livro de mensagens | não — não descrito | `docs.langchain.com/langsmith` (visto 24/10) |
| colisão de nomes | não — não descrito | `docs.langchain.com/langsmith` (visto 24/10) |
