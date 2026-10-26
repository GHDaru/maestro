# AutoGen Studio — prototipagem de times de agentes (073-T1-W05)

- **URL**: https://microsoft.github.io/autogen/stable/user-guide/autogenstudio-user-guide/index.html
- **Data da visita**: 2026-10-24
- **Aberto de verdade**:
  - `https://microsoft.github.io/autogen/stable/user-guide/autogenstudio-user-guide/index.html` —
    guia do usuário do AutoGen Studio: *Team Builder* (arrastar-e-soltar ou JSON declarativo),
    *Playground* (rodar sessões e ver o fluxo de mensagens em tempo real), controle de execução
    com *pause/stop*, grafo de transição de controle ("control transition graph") mostrando como a
    mensagem flui entre agentes, *Gallery* (importar componentes da comunidade), `UserProxyAgent`
    para participação humana, configuração de modelos/time de execução (visto 24/10).
- **Rodou local?**: **não** — nada instalado nem executado nesta máquina; sem capturas de tela.
- **Conta criada?**: **não**.

Acrônimos: LLM (*Large Language Model*), RBAC (*Role-Based Access Control*), MCP (*Model Context
Protocol*), A2A (*Agent-to-Agent*), API (*Application Programming Interface*), JSON (*JavaScript
Object Notation*).

## Tabela fixa (spec 073)

### CONTROLE

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| subir/derrubar sessão ou agente | parcial — rodar *times* no Playground; sem subir/derrubar agente pela UI | `.../autogenstudio-user-guide/index.html` (visto 24/10) |
| pausar | sim — "ability to pause or stop execution" no Playground | `.../autogenstudio-user-guide/index.html` (visto 24/10) |
| retomar | parcial — o controle pause/stop é descrito; retomar explicitamente, não | `.../autogenstudio-user-guide/index.html` (visto 24/10) |
| limites de orçamento e de taxa | — | `.../autogenstudio-user-guide/index.html` (visto 24/10) |
| políticas allow/deny/ask | — | `.../autogenstudio-user-guide/index.html` (visto 24/10) |
| aprovação humana | parcial — `UserProxyAgent` permite participação humana no diálogo, não um portão de aprovação | `.../autogenstudio-user-guide/index.html` (visto 24/10) |

### ADMINISTRAÇÃO

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| cadastro de agentes | sim — *Team Builder* monta agentes por arrastar-e-soltar ou JSON declarativo | `.../autogenstudio-user-guide/index.html` (visto 24/10) |
| papéis e permissões RBAC | — | `.../autogenstudio-user-guide/index.html` (visto 24/10) |
| cadastro de skills/ferramentas/modelos | sim — configuração de ferramentas e modelos no Team Builder; *Gallery* importa componentes da comunidade | `.../autogenstudio-user-guide/index.html` (visto 24/10) |
| chaves e segredos | parcial — modelos são configurados no Team Builder (implica credencial); gestão de chaves não descrita | `.../autogenstudio-user-guide/index.html` (visto 24/10) |
| configuração por projeto | parcial — o time é uma especificação declarativa (JSON) versionável; "projeto" não formalizado | `.../autogenstudio-user-guide/index.html` (visto 24/10) |
| auditoria | — | `.../autogenstudio-user-guide/index.html` (visto 24/10) |

### GERENCIAMENTO

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| lista de agentes vivos com estado | parcial — grafo de transição de controle e sessões do Playground, não agentes vivos com estado | `.../autogenstudio-user-guide/index.html` (visto 24/10) |
| tarefa aberta | parcial — tarefas aparecem na execução do time no Playground | `.../autogenstudio-user-guide/index.html` (visto 24/10) |
| última atividade | parcial — streaming de mensagens em tempo real na execução | `.../autogenstudio-user-guide/index.html` (visto 24/10) |
| consumo por agente/sessão/modelo | — | `.../autogenstudio-user-guide/index.html` (visto 24/10) |
| custo | — | `.../autogenstudio-user-guide/index.html` (visto 24/10) |
| filas e workers | — | `.../autogenstudio-user-guide/index.html` (visto 24/10) |
| rastro/replay de sessão | parcial — mensagens em tempo real; *replay* não é citado | `.../autogenstudio-user-guide/index.html` (visto 24/10) |
| alertas | — | `.../autogenstudio-user-guide/index.html` (visto 24/10) |

### INTERCOMUNICAÇÃO

| Funcionalidade | Veredito | Fonte |
|---|---|---|
| mensagem entre agentes | sim — times trocam mensagens; grafo de transição de controle mostra o fluxo; `UserProxyAgent` no diálogo | `.../autogenstudio-user-guide/index.html` (visto 24/10) |
| protocolos (A2A; MCP) | — | `.../autogenstudio-user-guide/index.html` (visto 24/10) não descreve |
| caixa de entrada | — | `.../autogenstudio-user-guide/index.html` (visto 24/10) |
| roteamento por nome/ref | parcial — o time roteia mensagens entre os agentes conforme o grafo | `.../autogenstudio-user-guide/index.html` (visto 24/10) |
| livro de mensagens | parcial — a sessão no Playground mostra as mensagens trocadas (streaming) | `.../autogenstudio-user-guide/index.html` (visto 24/10) |
| colisão de nomes | — | `.../autogenstudio-user-guide/index.html` (visto 24/10) |

**Correção da rodada 4 (26/10, fatia do Worker06).** Fonte: 1 URL (guia do usuário, página de documentação). Células `sim` revisadas contra a regra "só marketing/README → `parcial`": **nenhuma rebaixada** — *pausar*, *cadastro de agentes*, *cadastro de skills/ferramentas/modelos* e *mensagem entre agentes* apoiam-se no guia, que descreve o mecanismo.
