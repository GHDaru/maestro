# Flowise — construtor visual de agentes e fluxos com LLM (073-T1-W05)

- **URL**: https://flowiseai.com · https://docs.flowiseai.com (docs) · https://github.com/FlowiseAI/Flowise (código)
- **Data da visita**: 2026-10-24
- **Aberto de verdade**:
  - `https://docs.flowiseai.com/` — visão do produto: construtores visuais (*Assistant*, *Chatflow*,
    *Agentflow*), mais de 100 fontes/ferramentas/vector DBs, *template marketplace*, *Teams &
    Workspaces*, e uma seção de *Security Controls* que lista **RBAC, SSO, rate limit, restricted
    domains, encrypted credentials, secret managers** (visto 24/10).
  - `https://github.com/FlowiseAI/Flowise` — repositório (arquivado/descontinuado pelo autor);
    licença Apache-2.0; deploy via npm/Docker (visto 24/10).
- **Rodou local?**: **não** — nada instalado nem executado nesta máquina; sem capturas de tela.
- **Conta criada?**: **não**.

Acrônimos: LLM (*Large Language Model*), RBAC (*Role-Based Access Control*), SSO (*Single
Sign-On*), MCP (*Model Context Protocol*), A2A (*Agent-to-Agent*), SSE (*Server-Sent Events*),
API (*Application Programming Interface*).

## Tabela fixa (spec 073)

### CONTROLE

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| subir/derrubar sessão ou agente | não — o fluxo roda ao ser usado; não sobe/derruba agente pela UI | `docs.flowiseai.com` (visto 24/10) |
| pausar | — | `docs.flowiseai.com` (visto 24/10): não descrito |
| retomar | — | `docs.flowiseai.com` (visto 24/10): não descrito |
| limites de orçamento e de taxa | parcial — *Security Controls* lista **rate limit** (taxa), não orçamento | `docs.flowiseai.com` (visto 24/10): "rate limit" |
| políticas allow/deny/ask | parcial — *restricted domains* (allow/deny de domínios), não política geral | `docs.flowiseai.com` (visto 24/10): "restricted domains" |
| aprovação humana | sim — *Human in the Loop* listado entre os recursos | `docs.flowiseai.com` (visto 24/10) |

### ADMINISTRAÇÃO

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| cadastro de agentes | sim — construtores visuais (Assistant/Chatflow/Agentflow) criam agentes | `docs.flowiseai.com` (visto 24/10) |
| papéis e permissões RBAC | sim — *Security Controls* lista **RBAC** e **SSO** | `docs.flowiseai.com` (visto 24/10) |
| cadastro de skills/ferramentas/modelos | sim — +100 fontes/ferramentas/vector DBs e *template marketplace* | `docs.flowiseai.com` (visto 24/10) |
| chaves e segredos | sim — *Security Controls* lista "encrypted credentials" e "secret managers" | `docs.flowiseai.com` (visto 24/10) |
| configuração por projeto | sim — *Teams & Workspaces* | `docs.flowiseai.com` (visto 24/10) |
| auditoria | parcial — logs de execução/monitoramento; trilha de auditoria de administração não descrita | `docs.flowiseai.com` (visto 24/10) |

### GERENCIAMENTO

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| lista de agentes vivos com estado | — | `docs.flowiseai.com` (visto 24/10): não descrito |
| tarefa aberta | — | `docs.flowiseai.com` (visto 24/10): não descrito |
| última atividade | parcial — logs de execução/*monitoring* | `docs.flowiseai.com` (visto 24/10) |
| consumo por agente/sessão/modelo | — | `docs.flowiseai.com` (visto 24/10): não descrito |
| custo | — | `docs.flowiseai.com` (visto 24/10): não descrito |
| filas e workers | — | `docs.flowiseai.com` (visto 24/10): escala (vertical/horizontal) é citada; filas não |
| rastro/replay de sessão | parcial — depuração visual do fluxo + logs de execução; *replay* não citado | `docs.flowiseai.com` (visto 24/10) |
| alertas | — | `docs.flowiseai.com` (visto 24/10): não descrito |

### INTERCOMUNICAÇÃO

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| mensagem entre agentes | parcial — sistemas multiagente no *Agentflow* | `docs.flowiseai.com` (visto 24/10) |
| protocolos (A2A; MCP) | parcial — nós *MCP client/server* (tool listing, SSE, auth); A2A não citado | `docs.flowiseai.com` (visto 24/10) |
| caixa de entrada | — | `docs.flowiseai.com` (visto 24/10): não descrito |
| roteamento por nome/ref | — | `docs.flowiseai.com` (visto 24/10): não descrito |
| livro de mensagens | — | `docs.flowiseai.com` (visto 24/10): não descrito |
| colisão de nomes | — | `docs.flowiseai.com` (visto 24/10): não descrito |
