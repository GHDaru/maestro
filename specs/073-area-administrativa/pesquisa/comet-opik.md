# Comet Opik — observabilidade e avaliação de LLM (073-T1-W05)

> Extra além da lista do despacho: encontrado no mesmo nicho ("com o mesmo rigor") como alternativa
> *open source* de observabilidade/avaliação, inclusive de agentes.

- **URL**: https://www.comet.com/site/products/opik · https://github.com/comet-ml/opik (código)
- **Data da visita**: 2026-10-24
- **Aberto de verdade**:
  - `https://github.com/comet-ml/opik` — README: rastreamento completo (*trace trees*/*agent
    tracing*), avaliações (LLM-as-a-judge, *heuristic metrics*, PyTest integração), *prompt
    playground*/gestão de prompts, *Opik Agent Optimizer* (otimizador de prompts/agentes),
    *production monitoring* com dashboards (uso de tokens, feedback, latência), *online evaluation
    rules*, e um **servidor `opik-mcp`** para interoperar por MCP; *open source* (Apache-2.0),
    self-host via Docker Compose ou *Comet Cloud* (visto 24/10).
  - `https://www.comet.com/docs/opik/` — retornou **404** na visita; o README acima foi a fonte
    efetivamente lida (visto 24/10).
- **Rodou local?**: **não** — nada instalado nem executado nesta máquina; sem capturas de tela.
- **Conta criada?**: **não**.

Acrônimos: LLM (*Large Language Model*), RBAC (*Role-Based Access Control*), MCP (*Model Context
Protocol*), A2A (*Agent-to-Agent*), OSS (*Open Source Software*), API (*Application Programming
Interface*).

## Tabela fixa (spec 073)

### CONTROLE

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| subir/derrubar sessão ou agente | não — observabilidade/avaliação; não sobe nem derruba agente | `github.com/comet-ml/opik` README (visto 24/10) |
| pausar | — | README (visto 24/10): não descrito |
| retomar | — | README (visto 24/10): não descrito |
| limites de orçamento e de taxa | — | README (visto 24/10): não descrito |
| políticas allow/deny/ask | — | README (visto 24/10): não descrito |
| aprovação humana | — | README (visto 24/10) não descreve aprovação: há anotação com escores de feedback, não portão de aprovação |

### ADMINISTRAÇÃO

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| cadastro de agentes | não — não há catálogo de agentes | README (visto 24/10) |
| papéis e permissões RBAC | — | README (visto 24/10): não descrito nas fontes vistas |
| cadastro de skills/ferramentas/modelos | parcial — gestão de prompts, playground e *Agent Optimizer*; sem registro de ferramentas/modelos | README (visto 24/10) |
| chaves e segredos | parcial — requer API key da Comet (`opik configure`); sem gestor de segredos | README (visto 24/10) |
| configuração por projeto | parcial — `opik configure` pede workspace/projeto; "projeto" como agrupamento de traces | README (visto 24/10) |
| auditoria | — | README (visto 24/10): não descrito nas fontes vistas |

### GERENCIAMENTO

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| lista de agentes vivos com estado | não — mostra traces, não agentes vivos | README (visto 24/10) |
| tarefa aberta | — | README (visto 24/10): não descrito |
| última atividade | sim — *production monitoring* com dashboards de traces/feedback/latência | README (visto 24/10) |
| consumo por agente/sessão/modelo | parcial — dashboards de **uso de tokens**; quebra por modelo/agente não explicitada | README (visto 24/10): "token usage" |
| custo | parcial — uso de tokens é medido; custo em moeda não é citado | README (visto 24/10) |
| filas e workers | — | README (visto 24/10): não descrito |
| rastro/replay de sessão | sim — *trace trees*/*agent tracing* com visualização passo a passo | README (visto 24/10) |
| alertas | parcial — *online evaluation rules* automatizadas na produção (próximo de alerta); notificação não citada | README (visto 24/10) |

### INTERCOMUNICAÇÃO

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| mensagem entre agentes | — | README (visto 24/10): não descrito |
| protocolos (A2A; MCP) | parcial — servidor **`opik-mcp`** para interoperar por MCP; A2A não citado | README (visto 24/10) |
| caixa de entrada | — | README (visto 24/10): não descrito |
| roteamento por nome/ref | — | README (visto 24/10): não descrito |
| livro de mensagens | — | README (visto 24/10): não descrito |
| colisão de nomes | — | README (visto 24/10): não descrito |
