# Arize Phoenix — observabilidade e avaliação de LLM (073-T1-W05)

> Extra além da lista do despacho: encontrado no mesmo nicho ("com o mesmo rigor") como alternativa
> *open source* de observabilidade de agentes.

- **URL**: https://phoenix.arize.com · https://arize.com/docs/phoenix (docs) · https://github.com/Arize-ai/phoenix (código)
- **Data da visita**: 2026-10-24
- **Aberto de verdade**:
  - `https://arize.com/docs/phoenix` — visão do produto: rastreamento (*OpenTelemetry*-based),
    avaliações (LLM-as-a-judge, code evaluators), *prompt management*/playground, anotação humana
    e *datasets*, e o recurso **Span Replay** para inspecionar/reproduzir um passo do trace; roda
    local (notebook/Docker) ou self-host (visto 24/10).
  - `https://github.com/Arize-ai/phoenix` — repositório: licença Elastic License 2.0, `pip install
    arize-phoenix`, uso em notebook/container (visto 24/10).
- **Rodou local?**: **não** — nada instalado nem executado nesta máquina; sem capturas de tela.
- **Conta criada?**: **não**.

Acrônimos: LLM (*Large Language Model*), RBAC (*Role-Based Access Control*), MCP (*Model Context
Protocol*), A2A (*Agent-to-Agent*), OSS (*Open Source Software*).

## Tabela fixa (spec 073)

### CONTROLE

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| subir/derrubar sessão ou agente | não — observabilidade/avaliação; não sobe nem derruba agente | `arize.com/docs/phoenix` (visto 24/10) |
| pausar | não — não descrito | `arize.com/docs/phoenix` (visto 24/10) |
| retomar | não — não descrito | `arize.com/docs/phoenix` (visto 24/10) |
| limites de orçamento e de taxa | não — não descrito | `arize.com/docs/phoenix` (visto 24/10) |
| políticas allow/deny/ask | não — não descrito | `arize.com/docs/phoenix` (visto 24/10) |
| aprovação humana | não — há anotação humana (rotulagem), não portão de aprovação | `arize.com/docs/phoenix` (visto 24/10) não descreve aprovação |

### ADMINISTRAÇÃO

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| cadastro de agentes | não — não há catálogo de agentes | `arize.com/docs/phoenix` (visto 24/10) |
| papéis e permissões RBAC | não — não descrito nas fontes vistas | `arize.com/docs/phoenix` (visto 24/10) |
| cadastro de skills/ferramentas/modelos | parcial — *prompt management* e avaliadores; sem registro de ferramentas/modelos | `arize.com/docs/phoenix` (visto 24/10) |
| chaves e segredos | não — não descrito nas fontes vistas | `arize.com/docs/phoenix` (visto 24/10) |
| configuração por projeto | não — não descrito nas fontes vistas | `arize.com/docs/phoenix` (visto 24/10) |
| auditoria | não — não descrito nas fontes vistas | `arize.com/docs/phoenix` (visto 24/10) |

### GERENCIAMENTO

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| lista de agentes vivos com estado | não — mostra traces/spans, não agentes vivos | `arize.com/docs/phoenix` (visto 24/10) |
| tarefa aberta | não — não descrito | `arize.com/docs/phoenix` (visto 24/10) |
| última atividade | parcial — traces com carimbos de tempo | `arize.com/docs/phoenix` (visto 24/10) |
| consumo por agente/sessão/modelo | não — não descrito nas fontes vistas | `arize.com/docs/phoenix` (visto 24/10) |
| custo | não — não descrito nas fontes vistas | `arize.com/docs/phoenix` (visto 24/10) |
| filas e workers | não — não descrito | `arize.com/docs/phoenix` (visto 24/10) |
| rastro/replay de sessão | sim — *Span Replay* reproduz/inspeciona um passo do trace; rastreio completo | `arize.com/docs/phoenix` (visto 24/10) |
| alertas | não — não descrito nas fontes vistas | `arize.com/docs/phoenix` (visto 24/10) |

### INTERCOMUNICAÇÃO

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| mensagem entre agentes | não — não descrito | `arize.com/docs/phoenix` (visto 24/10) |
| protocolos (A2A; MCP) | não — nem A2A nem MCP citados nesta fonte | `arize.com/docs/phoenix` (visto 24/10) não descreve |
| caixa de entrada | não — não descrito | `arize.com/docs/phoenix` (visto 24/10) |
| roteamento por nome/ref | não — não descrito | `arize.com/docs/phoenix` (visto 24/10) |
| livro de mensagens | não — não descrito | `arize.com/docs/phoenix` (visto 24/10) |
| colisão de nomes | não — não descrito | `arize.com/docs/phoenix` (visto 24/10) |
