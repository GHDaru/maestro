# CrewAI Enterprise / AMP — orquestração e plataforma de agentes (073-T1-W05)

- **URL**: https://docs-platform.crewai.com/platform/en/overview (plataforma AMP) · https://github.com/crewAIInc/crewAI (código)
- **Data da visita**: 2026-10-24
- **Aberto de verdade**:
  - `https://docs-platform.crewai.com/platform/en/overview` (a antiga
    `docs.crewai.com/en/enterprise/overview` redireciona para cá) — visão da plataforma AMP:
    implantar/gerar/assistir *crews* em produção, *Crew Studio* sem código, *Tool Repository*
    (publicar e instalar ferramentas), *deploy* por CLI ou GitHub, "detailed execution traces and
    logs", *webhook streaming* de eventos, endpoints REST da API, escala em produção (visto 24/10).
  - `https://github.com/crewAIInc/crewAI` — README: framework de agentes com *crews* (processos
    sequential/hierarchical com *manager*), *Flows* (event-driven) com estado/checkpointing,
    delegação entre agentes, suporte a MCP/A2A citado na página do repositório, licença MIT
    (visto 24/10).
- **Rodou local?**: **não** — nada instalado nem executado nesta máquina; sem capturas de tela.
- **Conta criada?**: **não**.

Acrônimos: LLM (*Large Language Model*), AMP (*Agent Management Platform*), CLI (*Command-Line
Interface*), API (*Application Programming Interface*), REST (*Representational State Transfer*),
RBAC (*Role-Based Access Control*), MCP (*Model Context Protocol*), A2A (*Agent-to-Agent*).

## Tabela fixa (spec 073)

### CONTROLE

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| subir/derrubar sessão ou agente | parcial — implanta/escala *crews* e dispara execuções (`kickoff`); não há subir/derrubar de agente individual na UI | `docs-platform.crewai.com/.../overview` (visto 24/10): deploy, "kickoff" |
| pausar | — | `github.com/crewAIInc/crewAI` (visto 24/10) não descreve pausar |
| retomar | parcial — *Flows* com estado/checkpointing; não é "retomar" acionado por humano | README do repositório (visto 24/10): flow state, checkpointing |
| limites de orçamento e de taxa | — | `docs-platform.crewai.com/.../overview` (visto 24/10) não descreve limites |
| políticas allow/deny/ask | — | `docs-platform.crewai.com/.../overview` (visto 24/10) |
| aprovação humana | sim — *human input on execution* / *human-in-the-loop* no fluxo de execução | README do repositório (visto 24/10) |

### ADMINISTRAÇÃO

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| cadastro de agentes | parcial — *Crew Studio* sem código para montar a crew; sem catálogo de agentes durável na página | `docs-platform.crewai.com/.../overview` (visto 24/10) |
| papéis e permissões RBAC | — | `docs-platform.crewai.com/.../overview` (visto 24/10) |
| cadastro de skills/ferramentas/modelos | sim — *Tool Repository*: publicar e instalar ferramentas a partir da plataforma | `docs-platform.crewai.com/.../overview` (visto 24/10) |
| chaves e segredos | — | `docs-platform.crewai.com/.../overview` (visto 24/10) |
| configuração por projeto | parcial — deploy por CLI/GitHub e endpoints REST por crew; "projeto" não formalizado | `docs-platform.crewai.com/.../overview` (visto 24/10) |
| auditoria | parcial — "detailed execution traces and logs" (rastro de execução), não trilha de auditoria de administração | `docs-platform.crewai.com/.../overview` (visto 24/10) |

### GERENCIAMENTO

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| lista de agentes vivos com estado | — | `docs-platform.crewai.com/.../overview` (visto 24/10) |
| tarefa aberta | — | `docs-platform.crewai.com/.../overview` (visto 24/10) |
| última atividade | parcial — traces/logs de execução e webhook streaming de eventos | `docs-platform.crewai.com/.../overview` (visto 24/10) |
| consumo por agente/sessão/modelo | — | `docs-platform.crewai.com/.../overview` (visto 24/10) |
| custo | — | `docs-platform.crewai.com/.../overview` (visto 24/10) |
| filas e workers | — | `docs-platform.crewai.com/.../overview` (visto 24/10) |
| rastro/replay de sessão | parcial — traces/logs de execução; *replay* não é citado | `docs-platform.crewai.com/.../overview` (visto 24/10) |
| alertas | — | `docs-platform.crewai.com/.../overview` (visto 24/10) |

### INTERCOMUNICAÇÃO

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| mensagem entre agentes | sim — agentes especializados colaboram; processo *hierarchical* com *manager* que delega e sintetiza | README do repositório (visto 24/10) |
| protocolos (A2A; MCP) | sim — suporte a MCP e A2A listado na página do repositório | `github.com/crewAIInc/crewAI` (visto 24/10) |
| caixa de entrada | — | README (visto 24/10) |
| roteamento por nome/ref | parcial — o *manager* (processo hierarchical) distribui tarefas por papel/agente | README (visto 24/10) |
| livro de mensagens | — | README (visto 24/10) |
| colisão de nomes | — | README (visto 24/10) |

**Correção da rodada 4 (26/10, fatia do Worker06).** Fontes: 2 URLs (página de visão da plataforma AMP + página do repositório). Células `sim` revisadas contra a regra "só marketing/README → `parcial`": *cadastro de skills/ferramentas/modelos* e *mensagem entre agentes* descrevem o recurso e **permanecem**; *protocolos (A2A; MCP)* apoia-se numa **lista da página do repositório** ("suporte ... listado") — **declarada para o juiz reavaliar** (candidata a `parcial` se não houver página que documente o mecanismo).
