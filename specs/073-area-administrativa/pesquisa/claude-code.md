# Claude Code — sessões, subagentes e intercomunicação (ecossistema Claude)

- **URL**: https://code.claude.com/docs/en/overview
- **Data da visita**: 2026-10-24
- **Como foi pesquisada**: WebFetch na documentação oficial (code.claude.com/docs/en). Também é a ferramenta
  que **roda localmente** nesta sessão (o próprio Worker06 é uma sessão Claude Code) — as capacidades de
  sessão/intercomunicação abaixo foram vistas em uso real, além da doc.
- **O que foi aberto de verdade** (URL — o que a página realmente trazia):
  - `https://code.claude.com/docs/en/overview` — visão geral: superfícies (terminal, VS Code (*Visual Studio
    Code*), JetBrains, desktop, web), "Run agents in parallel and build custom agents", **agent view**
    ("background agents"), **Remote Control**, **Channels**, **Agent SDK**, **hooks**, **skills**, **MCP**
    (*Model Context Protocol*).
  - `https://code.claude.com/docs/en/sub-agents` — **subagentes**: arquivos Markdown com frontmatter
    (`name`, `description`, `tools`, `disallowedTools`, `model`, `permissionMode`, `maxTurns`, `skills`,
    `mcpServers`, `hooks`, `memory`, `background`, `effort`, `isolation`, …); tabela de escopo/prioridade
    (managed > `--agents` > `.claude/agents/` > `~/.claude/agents/` > plugin); **agent teams** (subagente
    com `name` vira "teammate" e mantém `TaskCreate/TaskGet/TaskList/TaskUpdate`, `CronCreate/…`);
    *"Resume via `SendMessage` with agent ID/name"*; profundidade de spawn 3
    (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`) e limite de 20 concorrentes
    (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`).
  - `https://code.claude.com/docs/en/agent-view` — **agent view** (`claude agents`): *"one screen for all
    your background sessions: what's running, what needs your input, and what's done"*, agrupadas por
    estado (`Pinned`, `Ready for review`, `Needs input`, `Working`, `Completed`); estados `Working`,
    `Needs input`, `Idle`, `Completed`, `Failed`, `Stopped`; `claude agents --json` expõe `state`,
    `status`, `waitingFor`; comandos `claude attach`, `claude logs`, `claude stop`, `claude respawn`,
    `claude rm`; **research preview**.
  - `https://code.claude.com/docs/en/monitoring-usage` — **OpenTelemetry (OTel)**: métricas
    `claude_code.session.count`, `claude_code.cost.usage` (unidade `USD`), `claude_code.token.usage`;
    evento `claude_code.api_request` com `cost_usd`, tokens; contadores carregam `model`,
    `query_source` (`"main"`/`"subagent"`/`"auxiliary"`), `agent.name`, `skill.name`, `mcp_server.name`;
    eventos de auditoria (`claude_code.tool_decision`, `claude_code.subagent_completed`,
    `claude_code.api_error`); **traces beta** (`CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1`).
  - `https://code.claude.com/docs/en/settings` — arquivos de configuração e precedência
    (**managed > linha de comando > `settings.local.json` do projeto > `settings.json` compartilhado >
    `~/.claude/settings.json`**); regras `permissions.allow` / `ask` / `deny`; `permissions.defaultMode`.
  - `https://code.claude.com/docs/en/iam` (redireciona para **Authentication**) — papéis no Claude
    Console (**`Claude Code`**, **`Developer`**), *role-based permissions* do Claude for Enterprise,
    `forceLoginMethod`/`forceLoginOrgUUID`, `apiKeyHelper`, cofre de credenciais por sistema
    (`~/.claude/.credentials.json`, Keychain no macOS).
  - `https://code.claude.com/docs/en/agent-teams.md` — **busca explícita por *mailbox***
    (rodada 4, 26/10): o time de sessões tem **`Mailbox` como componente** — *"Mailbox: Messaging
    system for communication between agents"*. Cada mailbox é um **arquivo JSON** em
    `~/.claude/teams/{team-name}/inboxes/{agent-name}.json`; o envio só conta como enviado **quando
    a escrita no mailbox do destinatário tem sucesso**; entrega automática, *idle notifications*,
    *task list* compartilhada; times são **experimentais** (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`).
  - `https://code.claude.com/docs/en/cross-session-messaging.md` — **busca explícita por *inbox***: a
    sessão **vincula um *inbox socket*** (*"The session's inbox socket"* — *Unix domain socket* no
    macOS/Linux, *named pipe* no Windows), exposto em `/status` e em `CLAUDE_CODE_MESSAGING_SOCKET`;
    controle de entrada `crossSessionInbound` = **`accept` / `hold` / `refuse`** (mensagens retidas:
    até 100, com diálogo de aprovação e prazo `dialogExpiry`); `/list-agents` (alias `/peers`) lista
    as sessões alcançáveis. **Colisão de identidade**: o `SendMessage` *"checks that a name still
    refers to the same agent... refuses the send rather than delivering it to the wrong agent"* —
    recusa em vez de entregar ao agente errado (é a dor de endereço ambíguo que o mapa § 7 trata).

## Tabela fixa (spec 073)

| Grupo | Item | Resultado | Fonte (URL — o que foi visto) |
|---|---|---|---|
| CONTROLE | subir/derrubar sessão ou agente | **sim** | `agent-view` — `claude --bg "…"` sobe sessão em segundo plano; `claude stop <id>` (*"Stop a session. Also accepts `claude kill`"*) **para** a sessão; `claude rm <id>` (*"Remove a session from the list, along with a worktree Claude created for it when that's safe to delete"*) **tira da lista**, não apaga a conversa — *"The conversation transcript stays on your local machine and remains available through `claude --resume`"*; `claude respawn <id>` (*"Restart a session, running or stopped… A session that has a saved conversation resumes it"*) reinicia |
| CONTROLE | pausar | **parcial** | `agent-view` — dá para *destacar/desanexar* a sessão (`←` no prompt vazio, `Ctrl+Z`) e parar (`claude stop`), mas a página não descreve uma pausa que suspenda o processo e o retome |
| CONTROLE | retomar | **sim** | `agent-view` — `claude attach <id\|name>` (*"Attach to a session in this terminal"*; por **nome** só enquanto o processo roda — *"pass the ID instead to restart a stopped session"*); `claude --resume <id\|name>` (`claude -r`) retoma a conversa; `sub-agents` — *"Resume via `SendMessage` with agent ID/name"* |
| CONTROLE | limites de orçamento e de taxa | **parcial** | `settings` — tetos de política (`availableModels`, `maxEffortLevel`); a doc **não** descreve teto de orçamento por sessão no CLI (isso mora na assinatura/Console) |
| CONTROLE | políticas allow/deny/ask | **sim** | `settings` — blocos `permissions.allow` / `ask` / `deny` e `permissions.defaultMode`; `sub-agents` — frontmatter `permissionMode` por agente |
| CONTROLE | aprovação humana | **sim** | `settings` — prompt de permissão ("Yes, and don't ask again" grava regra `allow`); modo `plan`; `monitoring-usage` — evento `claude_code.tool_decision` |
| ADMINISTRAÇÃO | cadastro de agentes | **sim** | `sub-agents` — cada subagente é um Markdown com frontmatter em `.claude/agents/` (projeto) ou `~/.claude/agents/` (usuário), com tabela de prioridade de escopo |
| ADMINISTRAÇÃO | papéis e permissões RBAC (*Role-Based Access Control*) | **parcial** | `iam` — papéis de Console `Claude Code` e `Developer` e *role-based permissions* do Claude for Enterprise; `sub-agents` — `tools`/`disallowedTools` restringem ferramentas, mas não é RBAC por papel de negócio |
| ADMINISTRAÇÃO | cadastro de skills/ferramentas/modelos | **sim** | `overview` — *skills*, *hooks*; `sub-agents` — frontmatter `skills`, `mcpServers`, `tools`, `model`; `settings` — `availableModels`/`deniedModels` |
| ADMINISTRAÇÃO | chaves e segredos | **sim** | `iam` — `apiKeyHelper` (script que devolve chave), `ANTHROPIC_API_KEY`/`ANTHROPIC_AUTH_TOKEN`, credenciais em `~/.claude/.credentials.json` (0600) ou Keychain |
| ADMINISTRAÇÃO | configuração por projeto | **sim** | `settings` — `.claude/settings.json` (time), `.claude/settings.local.json` (pessoal), com precedência documentada |
| ADMINISTRAÇÃO | auditoria | **parcial** | `monitoring-usage` — eventos OTel (`tool_decision`, `api_request`, `subagent_completed`, `api_error`) e gating de conteúdo; **exige backend OTel próprio** — não há console de auditoria nativo |
| GERENCIAMENTO | lista de agentes vivos com estado | **sim** | `agent-view` — `claude agents` lista por estado (`Working`, `Needs input`, `Idle`, `Completed`, `Failed`, `Stopped`) e `claude agents --json` |
| GERENCIAMENTO | tarefa aberta | **sim** | `agent-view` — cada linha mostra a *current activity*; `sub-agents` — teammates mantêm `TaskList`/`TaskGet` |
| GERENCIAMENTO | última atividade | **parcial** | `agent-view` — a linha mostra "nome, atividade atual e **idade**", mas a doc não descreve um campo de última atividade por item |
| GERENCIAMENTO | consumo por agente/sessão/modelo | **sim** | `monitoring-usage` — `claude_code.token.usage` com atributos `model`, `query_source`, `agent.name`, `skill.name` |
| GERENCIAMENTO | custo | **sim** | `monitoring-usage` — `claude_code.cost.usage` (unidade `USD`) e `cost_usd` por `claude_code.api_request` |
| GERENCIAMENTO | filas e workers | **parcial** | `sub-agents` — há limites de paralelismo (20 concorrentes, spawn depth 3) e subagentes em background, mas não há fila/worker pool nomeado |
| GERENCIAMENTO | rastro/replay de sessão | **parcial** | `agent-view` — `claude logs <id>` e retomada de sessão; `monitoring-usage` — traces beta (`claude_code.interaction`); "replay" completo não é descrito |
| GERENCIAMENTO | alertas | **parcial** | `monitoring-usage` — o desenho manda exportar OTel para o **seu** backend; alerta não é nativo |
| INTERCOMUNICAÇÃO | mensagem entre agentes | **sim** | `sub-agents`/`agent-teams` — `SendMessage` para agente por ID/nome; *mailbox* por agente; *cross-session messaging* entre as suas sessões (socket/named pipe) |
| INTERCOMUNICAÇÃO | protocolos (A2A (*Agent-to-Agent*), MCP) | **parcial** | `overview` — **MCP** é suportado (servidores MCP, `mcp__…`); **A2A não consta** nas páginas lidas |
| INTERCOMUNICAÇÃO | caixa de entrada | **parcial** | `agent-view` — estado `Needs input` e o painel *peek* (responder sem sair da tela); `cross-session-messaging` — **inbox socket** por sessão (`/status`) + controle `crossSessionInbound` (`accept`/`hold`/`refuse`, retidas até 100); `agent-teams` — *mailbox* JSON por agente. Não há uma **UI de inbox nomeada** (o inbox é socket/arquivo) — por isso `parcial`, não `sim` |
| INTERCOMUNICAÇÃO | roteamento por nome/ref | **sim** | `sub-agents` — *"Resume via `SendMessage` with agent ID/name"*; refs exibidas por ListAgents |
| INTERCOMUNICAÇÃO | livro de mensagens | **—** | A doc descreve o *mailbox* (arquivo por agente, em `~/.claude/teams/…`) e mensagens retidas, mas **não** um log/livro de mensagens consultável entre sessões — busca vazia |
| INTERCOMUNICAÇÃO | colisão de nomes | **parcial** | `sub-agents` — tabela de escopo/prioridade resolve homônimos (managed > `--agents` > projeto > usuário > plugin); `cross-session-messaging` — o `SendMessage` **recusa** quando o nome passou a outro agente (*"refuses the send rather than delivering it to the wrong agent"*). Há **recusa** de colisão, não um registro de colisões |

## Observações

- **Rodou local**: sim — é a própria ferramenta desta sessão. Vi em uso: lista de sessões
  (`ListAgents`), mensagem entre sessões (`SendMessage`), subagentes em background e estados.
- **Pago vs. livre**: o CLI exige assinatura Claude ou Console; *agent view* está em **research preview**
  e pode mudar; telemetria OTel é opt-in por variável de ambiente.
- **Lacuna**: não há, na doc lida, teto de orçamento por sessão nem livro de mensagens; MCP é o único
  protocolo de intercomunicação citado (A2A ausente).
- **Correção 3 da rodada 4 (27/10)** — *`stop` × `rm` × `attach`/`--resume`, conferido na doc*
  (`agent-view`, reverificado por WebFetch em 27/10): a linha 59 dizia só que `stop` e `rm`
  "derrubam" e que `respawn` ressuscita — a **assimetria** "`stop` religável × `rm` irreversível"
  era **inferência** (ressalva do juiz 1 ao P13). A doc é explícita: `claude stop <id>` **para** a
  sessão (*"Stop a session. Also accepts `claude kill`"*; a conversa fica em disco e reata por
  `claude attach`/resposta ou `claude respawn`) e `claude rm <id>` **remove a sessão da lista** (e o
  *worktree* "when that's safe to delete") — mas **o transcript não se perde**: *"The conversation
  transcript stays on your local machine and remains available through `claude --resume`"*. Ou seja:
  o que o `rm` tira é a **linha/worktree**, não a conversa. A retomada citada pela tela
  (`claude --resume`) **está** na ficha (`:61`, junto de `claude attach <id|name>`; `claude -r`).
  A remoção pode ainda ser **recusada** por commits não publicados (escape: `--discard-unpushed`,
  `--force-remove-worktree`). *Agent view* segue **research preview**.
- **Correção da rodada 4 (26/10)** — *busca explícita por mailbox/inbox, com URL*: as páginas
  `agent-teams.md` e `cross-session-messaging.md` (acima) **documentam** o transporte real — *mailbox*
  JSON por agente (`~/.claude/teams/{team}/inboxes/{agent}.json`) e *inbox socket* por sessão —, o que
  reforça as células de *mensagem entre agentes*, *caixa de entrada* e *colisão de nomes*. Não achei,
  porém, uma **UI de inbox** nem um **livro de mensagens**; o inbox é socket/arquivo, o que mantém
  *caixa de entrada* em `parcial` e *livro de mensagens* em `—`.
