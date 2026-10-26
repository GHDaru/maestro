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
| pausar | — | `arize.com/docs/phoenix` (visto 24/10): não descrito |
| retomar | — | `arize.com/docs/phoenix` (visto 24/10): não descrito |
| limites de orçamento e de taxa | — | `arize.com/docs/phoenix` (visto 24/10): não descrito |
| políticas allow/deny/ask | — | `arize.com/docs/phoenix` (visto 24/10): não descrito |
| aprovação humana | — | `arize.com/docs/phoenix` (visto 24/10) não descreve aprovação: há anotação humana (rotulagem), não portão de aprovação |

### ADMINISTRAÇÃO

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| cadastro de agentes | não — não há catálogo de agentes | `arize.com/docs/phoenix` (visto 24/10) |
| papéis e permissões RBAC | — | `arize.com/docs/phoenix` (visto 24/10): não descrito nas fontes vistas |
| cadastro de skills/ferramentas/modelos | parcial — *prompt management* e avaliadores; sem registro de ferramentas/modelos | `arize.com/docs/phoenix` (visto 24/10) |
| chaves e segredos | — | `arize.com/docs/phoenix` (visto 24/10): não descrito nas fontes vistas |
| configuração por projeto | — | `arize.com/docs/phoenix` (visto 24/10): não descrito nas fontes vistas |
| auditoria | — | `arize.com/docs/phoenix` (visto 24/10): não descrito nas fontes vistas |

### GERENCIAMENTO

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| lista de agentes vivos com estado | não — mostra traces/spans, não agentes vivos | `arize.com/docs/phoenix` (visto 24/10) |
| tarefa aberta | — | `arize.com/docs/phoenix` (visto 24/10): não descrito |
| última atividade | parcial — traces com carimbos de tempo | `arize.com/docs/phoenix` (visto 24/10) |
| consumo por agente/sessão/modelo | — | `arize.com/docs/phoenix` (visto 24/10): não descrito nas fontes vistas |
| custo | — | `arize.com/docs/phoenix` (visto 24/10): não descrito nas fontes vistas |
| filas e workers | — | `arize.com/docs/phoenix` (visto 24/10): não descrito |
| rastro/replay de sessão | sim — *Span Replay* reproduz/inspeciona um passo do trace; rastreio completo | `arize.com/docs/phoenix` (visto 24/10) |
| alertas | — | `arize.com/docs/phoenix` (visto 24/10): não descrito nas fontes vistas |

### INTERCOMUNICAÇÃO

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| mensagem entre agentes | — | `arize.com/docs/phoenix` (visto 24/10): não descrito |
| protocolos (A2A; MCP) | — | `arize.com/docs/phoenix` (visto 24/10) não descreve: nem A2A nem MCP citados nesta fonte |
| caixa de entrada | — | `arize.com/docs/phoenix` (visto 24/10): não descrito |
| roteamento por nome/ref | — | `arize.com/docs/phoenix` (visto 24/10): não descrito |
| livro de mensagens | — | `arize.com/docs/phoenix` (visto 24/10): não descrito |
| colisão de nomes | — | `arize.com/docs/phoenix` (visto 24/10): não descrito |

**Correção da rodada 4 (26/10, fatia do Worker06).** Fontes: 3 URLs (produto, `/docs/phoenix`, GitHub). Célula `sim` revisada contra a regra "só marketing/README → `parcial`": **nenhuma rebaixada** — *rastro/replay de sessão* (*Span Replay*) apoia-se na página de documentação, que descreve o mecanismo.
