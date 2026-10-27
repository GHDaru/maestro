# Matriz consolidada: funcionalidade × plataforma (ciclo 073, rodada 1)

> **Consolidação completa** — as **25 plataformas** das três fatias da rodada 1 (controle de
> processos e governança · gateways e consoles de *Large Language Model*, LLM · observabilidade e
> orquestração de agentes), 26 funcionalidades cada: **650 células**. Fechada por acréscimo, como a
> seção "Como acrescentar uma plataforma" previu.
>
> **Onze plataformas foram consideradas e não entraram** — com o motivo, na seção "Consideradas e
> não incluídas", ao fim.

- **Data**: 2026-10-24 (fichas) · fechada em 2026-10-25 · **Ciclo**: 073 "área administrativa do
  Maestro" · **Rodada**: 1 (pesquisa)
- **Fonte de cada célula**: a **ficha da coluna** — cada ficha traz a URL visitada e o que foi
  visto na página (ver `pesquisa/<slug>.md`). A matriz é o índice; a prova está na ficha.
- **Nada foi executado** para 23 das 25 plataformas: `docker` não existe nesta máquina, o binário
  `temporal` não está instalado e nenhuma conta externa foi criada. Duas exceções registradas nas
  próprias fichas: o **LiteLLM** (Worker03 subiu o proxy e a Admin UI localmente; capturas em
  `pesquisa/img/litellm-*.png`) e o **Claude Code** (a ferramenta que roda esta sessão).

## As 25 fichas, na ordem das colunas

- **Controle de processos e governança** (Worker06): [Temporal Web UI](temporal-web-ui.md) ·
  [Portainer CE](portainer-ce.md) · [Prefect](prefect.md) · [Dagster](dagster.md) ·
  [Copilot Studio](copilot-studio.md) · [Agent 365](agent-365.md) · [n8n](n8n.md) ·
  [Claude Code](claude-code.md) · [Maestri canvas](maestri-canvas.md) ·
  [Kiro Crew](kiro-crew.md) · [AWS Bedrock AgentCore](aws-bedrock-agentcore.md) ·
  [Windmill](windmill.md)
- **Gateways e consoles de LLM** (Worker03): [LiteLLM](litellm.md) · [Portkey](portkey.md) ·
  [OpenAI Platform](openai-platform.md) · [Helicone](helicone.md)
- **Observabilidade e orquestração de agentes** (Worker05): [AgentOps](agentops.md) ·
  [Langfuse](langfuse.md) · [LangSmith/LangGraph](langsmith-langgraph.md) ·
  [CrewAI AMP](crewai-amp.md) · [AutoGen Studio](autogen-studio.md) · [Dify](dify.md) ·
  [Flowise](flowise.md) · [Arize Phoenix](arize-phoenix.md) · [Comet Opik](comet-opik.md)

## Legenda

| Símbolo | Significa |
|---|---|
| **sim** | a funcionalidade existe **e** foi vista na fonte citada pela ficha |
| **parcial** | existe de forma incompleta, só em plano pago, só em nuvem, ou por analogia (a ficha diz por quê) |
| **não** | a **fonte afirma a ausência** — a ficha descreve o objeto e declara que a função não existe ali. Não é "não encontrei" |
| **—** | **nenhuma fonte encontrada**: busca vazia ("nada sobre / não aparece / não descrito / *not documented*") **ou** célula vazia de prova. **Nunca** quer dizer "sim" |

Siglas expandidas na primeira ocorrência: **RBAC** (*Role-Based Access Control*) · **MCP**
(*Model Context Protocol*) · **A2A** (*Agent-to-Agent*) · **CE** (*Community Edition*) · **LLM**
(*Large Language Model*) · **UI** (*User Interface*) · **OSS** (*Open Source Software*) · **SSO**
(*Single Sign-On*) · **PTY** (*Pseudo-Terminal*).

> **Notação — divergência entre gerações de ficha, resolvida na rodada 2 (25/10).** As duas
> gerações usavam o `não` com força diferente: as 12 fichas do Worker06 marcam "sem fonte" com `—` e
> reservam `não` para a ausência **afirmada**; as 13 fichas do Worker03/Worker05 **não usavam `—`**
> (o Worker03 deixava a célula **em branco** — 21 células — e o Worker05 escrevia `não` para "nada
> achei"). O preâmbulo da rodada 2 **reclassificou célula a célula, relendo cada ficha**: o `não` de
> "não achei / nada sobre / não aparece / não descrito / *not documented*" virou `—`; o `não` que a
> fonte **afirma** permaneceu `não`. Resultado: **144 células** `não → —` (143 na rodada 2 + 1 na
> correção da rodada 4, a *caixa de entrada* do Kiro Crew) e **12** `não` mantidos — 3 na Helicone
> (subir, lista de vivos, mensagem), 8 nas nove fichas de observabilidade/orquestração (subir,
> cadastro e lista de vivos: "não sobe nem derruba agente", "não há catálogo de agentes", "mostra
> traces, não agentes vivos") e 1 no Kiro Crew (pausar). **Nenhuma célula mudou de `—` para `sim`** (FR3 intocado). Hoje vale
> **um só símbolo, uma só força**: `não` = a fonte afirma a ausência; `—` = nenhuma fonte encontrada.

## A matriz

| Grupo | Funcionalidade | [Temporal](temporal-web-ui.md) | [Portainer CE](portainer-ce.md) | [Prefect](prefect.md) | [Dagster](dagster.md) | [Copilot Studio](copilot-studio.md) | [Agent 365](agent-365.md) | [n8n](n8n.md) | [Claude Code](claude-code.md) | [Maestri](maestri-canvas.md) | [Kiro Crew](kiro-crew.md) | [AgentCore](aws-bedrock-agentcore.md) | [Windmill](windmill.md) | [LiteLLM](litellm.md) | [Portkey](portkey.md) | [OpenAI Platform](openai-platform.md) | [Helicone](helicone.md) | [AgentOps](agentops.md) | [Langfuse](langfuse.md) | [LangSmith/LG](langsmith-langgraph.md) | [CrewAI AMP](crewai-amp.md) | [AutoGen Studio](autogen-studio.md) | [Dify](dify.md) | [Flowise](flowise.md) | [Arize Phoenix](arize-phoenix.md) | [Comet Opik](comet-opik.md) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CONTROLE | subir/derrubar sessão ou agente | sim | sim | parcial | parcial | parcial | parcial | parcial | sim | parcial | parcial | sim | parcial | parcial | parcial | parcial | não | parcial | — | parcial | parcial | parcial | não | não | não | não |
| CONTROLE | pausar | sim | — | parcial | parcial | — | — | parcial | parcial | — | não | parcial | sim | — | — | — | — | — | — | — | — | sim | — | — | — | — |
| CONTROLE | retomar | sim | — | parcial | parcial | — | — | parcial | sim | — | sim | sim | parcial | — | — | — | — | — | — | parcial | parcial | parcial | — | — | — | — |
| CONTROLE | limites de orçamento e de taxa | parcial | — | parcial | parcial | sim | — | sim | parcial | — | parcial | sim | parcial | sim | sim | sim | parcial | parcial | — | parcial | — | — | — | parcial | — | — |
| CONTROLE | políticas allow/deny/ask | — | parcial | parcial | parcial | sim | sim | parcial | sim | — | sim | sim | parcial | parcial | parcial | parcial | parcial | — | — | — | — | — | — | parcial | — | — |
| CONTROLE | aprovação humana | — | — | parcial | — | parcial | sim | sim | sim | — | sim | parcial | sim | — | parcial | parcial | — | — | parcial | sim | sim | parcial | — | sim | — | — |
| ADMINISTRAÇÃO | cadastro de agentes | — | sim | parcial | parcial | sim | sim | — | sim | sim | sim | sim | parcial | sim | sim | parcial | — | parcial | — | parcial | parcial | sim | parcial | sim | não | não |
| ADMINISTRAÇÃO | papéis e permissões RBAC | parcial | sim | sim | sim | sim | sim | sim | parcial | parcial | parcial | sim | sim | sim | sim | sim | — | — | sim | — | — | — | parcial | sim | — | — |
| ADMINISTRAÇÃO | cadastro de skills/ferramentas/modelos | — | sim | — | — | sim | parcial | sim | sim | parcial | sim | sim | sim | sim | sim | parcial | parcial | parcial | parcial | parcial | sim | sim | sim | sim | parcial | parcial |
| ADMINISTRAÇÃO | chaves e segredos | sim | sim | sim | sim | parcial | — | parcial | sim | — | sim | sim | sim | sim | sim | sim | parcial | parcial | sim | parcial | — | parcial | parcial | sim | — | parcial |
| ADMINISTRAÇÃO | configuração por projeto | sim | sim | sim | sim | parcial | — | sim | sim | sim | sim | parcial | sim | sim | sim | sim | — | — | sim | — | parcial | parcial | sim | sim | — | parcial |
| ADMINISTRAÇÃO | auditoria | parcial | parcial | sim | sim | sim | sim | parcial | parcial | — | sim | sim | sim | sim | sim | sim | — | — | parcial | — | parcial | — | — | parcial | — | — |
| GERENCIAMENTO | lista de agentes vivos com estado | parcial | sim | parcial | parcial | sim | sim | — | sim | parcial | parcial | sim | parcial | parcial | — | — | não | parcial | — | — | — | parcial | — | — | não | não |
| GERENCIAMENTO | tarefa aberta | parcial | — | parcial | parcial | — | parcial | parcial | sim | parcial | sim | parcial | sim | — | — | — | — | — | — | — | — | parcial | — | — | — | — |
| GERENCIAMENTO | última atividade | parcial | — | parcial | parcial | sim | parcial | sim | parcial | parcial | parcial | parcial | parcial | parcial | parcial | parcial | sim | parcial | parcial | parcial | parcial | parcial | sim | parcial | parcial | sim |
| GERENCIAMENTO | consumo por agente/sessão/modelo | parcial | — | — | parcial | sim | parcial | parcial | sim | — | parcial | parcial | — | sim | parcial | parcial | parcial | parcial | parcial | — | — | — | parcial | — | — | parcial |
| GERENCIAMENTO | custo | parcial | — | — | parcial | sim | — | sim | sim | — | parcial | sim | sim | sim | sim | parcial | parcial | parcial | parcial | — | — | parcial | — | — | — | parcial |
| GERENCIAMENTO | filas e workers | sim | — | sim | parcial | — | — | sim | parcial | — | — | parcial | sim | — | — | parcial | — | — | — | — | — | — | — | — | — | — |
| GERENCIAMENTO | rastro/replay de sessão | sim | parcial | parcial | parcial | sim | parcial | sim | parcial | parcial | parcial | sim | parcial | parcial | parcial | parcial | parcial | parcial | parcial | sim | parcial | parcial | parcial | parcial | sim | sim |
| GERENCIAMENTO | alertas | parcial | — | sim | sim | parcial | parcial | parcial | parcial | — | parcial | parcial | sim | sim | parcial | sim | sim | parcial | sim | sim | — | — | — | — | — | parcial |
| INTERCOMUNICAÇÃO | mensagem entre agentes | sim | — | — | — | sim | parcial | parcial | sim | sim | parcial | sim | parcial | sim | — | parcial | não | — | — | — | sim | sim | — | parcial | — | — |
| INTERCOMUNICAÇÃO | protocolos (A2A, MCP) | parcial | — | parcial | parcial | sim | sim | parcial | parcial | — | parcial | sim | parcial | sim | parcial | parcial | parcial | parcial | parcial | parcial | sim | — | parcial | parcial | — | parcial |
| INTERCOMUNICAÇÃO | caixa de entrada | — | — | — | — | — | — | — | parcial | parcial | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| INTERCOMUNICAÇÃO | roteamento por nome/ref | sim | — | parcial | — | sim | parcial | parcial | sim | parcial | sim | sim | sim | parcial | parcial | — | — | — | — | — | parcial | parcial | — | — | — | — |
| INTERCOMUNICAÇÃO | livro de mensagens | — | — | — | — | — | — | — | — | parcial | — | parcial | parcial | parcial | — | parcial | — | — | — | — | — | parcial | — | — | — | — |
| INTERCOMUNICAÇÃO | colisão de nomes | parcial | — | — | — | — | — | — | parcial | — | sim | — | sim | — | — | — | — | — | — | — | — | — | — | — | — | — |

> **Nota de coluna — "corta × avisa"** (decisão da rodada 4). Duas linhas parecem a mesma coisa e não
> são: **limites de orçamento e de taxa** (grupo CONTROLE) é o **limite que corta** — estourou, a
> chamada é recusada (a OpenAI Platform devolve 429 acima do teto de gasto); **alertas** (grupo
> GERENCIAMENTO) é o **aviso que só notifica**, sem bloquear nada (a própria doc do Portkey declara os
> alertas "work in progress and not sent today"). Um `sim` na linha de alertas diz que a plataforma
> **avisa** — não que ela **corta**.

## Como acrescentar uma plataforma

1. Escreva a ficha `pesquisa/<slug>.md` com URL, data da visita, o que foi **aberto de verdade**
   e a tabela fixa de 26 funcionalidades (a mesma ordem desta matriz).
2. Acrescente **uma coluna** à matriz, no fim ou junto do bloco temático, com o rótulo linkando a
   ficha; transfira as 26 células na ordem.
3. Nenhuma célula entra sem prova: sem fonte na ficha, fica `—`.

## Leitura da matriz (o que os números dizem)

> **Corrigido em 25/10** após a reverificação em contexto fresco (Worker03, ver qa-report §
> "Reverificação em contexto fresco"): as tabelas de leitura subnotificavam o `sim` em 4 (alertas
> 6→8, mensagem entre agentes 7→8, consumo por agente 2→3; total 170→174). As células da matriz
> estavam certas — o erro era só das contagens desta seção. Números atuais conferidos por script
> contra a matriz.
>
> **Corrigido em 25/10 (2ª passagem — correções da amostragem do crítico).** Duas células desceram
> de `sim` para `parcial` na coluna do **Temporal Web UI**: *lista de agentes vivos com estado* e
> *tarefa aberta* — a aba **Workers** mostra *workers* em *polling*, não agentes, e a tabela
> *Workflows* lista execuções, não a tarefa aberta de um agente (fonte em `temporal-web-ui.md`).
> Efeito nos totais: **`sim` 174 → 172**, **`parcial` 221 → 223**, **GERENCIAMENTO 47 → 45** (22,5%).
> Toda contagem desta seção foi reconferida por script contra a matriz (PASS), já sobre a
> distribuição normalizada (`não` 156 → 13 · `—` 99 → 242).
>
> **Corrigido em 26/10 (correção 1 da rodada 4).** Seis células mudaram nesta fatia: **Kiro Crew**
> *caixa de entrada* `não` → `—` (a fonte não afirma a ausência); **AgentOps** *custo* e
> *rastro/replay de sessão* e **Langfuse** *custo* `sim` → `parcial` (apoio só no README/marketing);
> **Claude Code** *caixa de entrada* e *colisão de nomes* `—` → `parcial` (busca explícita por
> mailbox/*agent teams* achou fonte, ver `claude-code.md`). Totais reconferidos por script contra a
> matriz, **valendo sobre os números acima**: **`sim` 169 · `parcial` 225 · `não` 12 · `—` 244**
> (650 células = 26 funcionalidades × 25 plataformas); **GERENCIAMENTO 42/200 = 21%**.
>
> **Corrigido em 26/10 (correção 2 da rodada 4).** Uma célula mudou: **Langfuse** *auditoria*
> `sim` → `parcial` — o `sim` apoiava-se em "*audit logs* listados entre os controles"
> (`langfuse.md:47`), lista de itens da página de segurança, o **mesmo tipo de apoio** que já
> rebaixara o *custo* (`langfuse.md:57`) e que o juiz 2 (P1) nomeou. Totais reconferidos por script
> contra a matriz, **valendo sobre os números acima**: **`sim` 168 · `parcial` 226 · `não` 12 ·
> `—` 244** (650 células); **ADMINISTRAÇÃO 75/150 = 50%**; **GERENCIAMENTO 42/200 = 21%**
> (inalterado). Nenhuma célula `—` → `sim` (FR3 intocado).

**Por grupo** — `sim` sobre o total de células do grupo, nas 25 plataformas:

| Grupo | `sim` | Células | Aproveitamento | Leitura |
|---|---|---|---|---|
| ADMINISTRAÇÃO | 75 | 150 | **50%** | o que o mercado sabe fazer: cadastro, RBAC, segredos, por projeto, auditoria |
| GERENCIAMENTO | 42 | 200 | **21%** | metade é observabilidade; "agentes vivos" e consumo por agente quase não existem |
| CONTROLE | 30 | 150 | **20%** | ciclo de vida é o buraco: pausar tem 3 `sim` em 25 |
| INTERCOMUNICAÇÃO | 21 | 150 | **14%** | **o grupo mais fraco** — e é exatamente o que o Maestro já opera a mão |

**Por funcionalidade** — contagem de `sim` nas 25 plataformas, do mais coberto ao menos:

| Funcionalidade | `sim` | Leitura |
|---|---|---|
| configuração por projeto | 15 | o mais maduro do conjunto |
| papéis e permissões RBAC · cadastro de skills/ferramentas/modelos · chaves e segredos | 13 cada | a base de administração é commodity |
| cadastro de agentes | 11 | o "cadastro de agentes" é **registro**, quase nunca processo vivo |
| auditoria | 10 | desceu na correção 2 com o rebaixamento do Langfuse (apoio só na página de segurança) |
| aprovação humana · alertas · mensagem entre agentes | 8 cada | human-in-the-loop existe onde há grafo de execução; e a mensagem entre agentes é quase toda delegação dentro do processo, não mensagem entre pares |
| custo · rastro/replay de sessão | 7 cada | custo de *token* é comum, custo de operação de agente não; e o rastro desceu com os rebaixamentos por apoio só em marketing/README |
| limites de orçamento e de taxa · roteamento por nome/ref | 6 cada | orçamento por chave/projeto, raramente por agente |
| políticas allow/deny/ask · protocolos (A2A, MCP) · última atividade · lista de agentes vivos com estado | 5 cada | |
| subir/derrubar sessão ou agente · retomar · filas e workers | 4 cada | |
| pausar · tarefa aberta · consumo por agente/sessão/modelo | 3 cada | consumo por agente em **Copilot Studio**, **Claude Code** e **LiteLLM** |
| colisão de nomes | 2 | |
| **caixa de entrada** · **livro de mensagens** | **0 cada** | nenhuma das 25 tem `sim` — no máximo `parcial` (Claude Code e Maestri na *caixa de entrada*; nenhuma no *livro de mensagens*): **não encontrado na documentação lida** |

**Por plataforma** — uma linha cada (as 12 primeiras são da fatia do Worker06):

- **Temporal Web UI** — a melhor em **rastro/replay** (History em 4 formatos, *download* do
  histórico, Reset) e em **filas e workers** (Workers por Task Queue, Pending Activities). Tudo
  de administração (RBAC, auditoria, chaves, limites) é **exclusivo do Temporal Cloud**. A aba
  **Workers** lista *workers* em *polling*, não agentes — por isso *lista de vivos* e *tarefa
  aberta* ficam `parcial`.
- **Portainer CE** — a melhor em **administração de recursos** (cadastro, RBAC, *secrets*,
  configuração por projeto) e a única que **não** tem nada de agente: é gestão de contêineres.
- **Prefect** — forte em **execução** (filas/workers, alertas, auditoria) e **RBAC**; mensageria
  entre agentes ausente.
- **Dagster** — parecido com o Prefect, mais forte em **alertas** e **auditoria**; intercomunicação
  quase toda `—`.
- **Copilot Studio** — a mais **completa em consumo e custo** (por agente/sessão/modelo e custo
  propriamente dito) e uma das cinco com **A2A**; sem filas/workers.
- **Agent 365** — o **plano de controle** do lado Microsoft: políticas `allow/deny/ask`,
  aprovação humana, cadastro e **auditoria** de agentes; consumo/custo só parciais.
- **n8n** — a mais **larga em controle de execução** (pausar/retomar/limites/aprovação humana) e
  a única com **custo** e **alertas** simultaneamente fortes; mensageria entre agentes só parcial.
- **Claude Code** — a única que cobre **sessão de agente de ponta a ponta**: subir, retomar,
  listar por estado, consumo por agente (`agent.name`), custo em dólar e mensagem entre sessões.
  É a plataforma que **roda nesta sessão**.
- **Maestri canvas** — a mais **fraca em controle** (5 células `—` no grupo CONTROLE: só *subir/derrubar* é `parcial`) e a única
  cuja intercomunicação é por **PTY** (*Pseudo-Terminal*), com caixa de entrada e livro de
  mensagens parciais.
- **Kiro Crew** — a mais **completa em administração** (só RBAC é parcial) e a única que
  **documenta a ausência** de pausa (a *caixa de entrada* deixou de ser `não` na correção da rodada
  4: a página não a descreve, mas também não afirma que inexiste — ver `kiro-crew.md:55`); forte em
  **colisão de nomes**.
- **AWS Bedrock AgentCore** — a **mais completa no total** (só 2 células `—`): sessão, limites,
  políticas, cadastro, auditoria, rastro e mensageria com **A2A**.
- **Windmill** — a mais forte em **filas e workers** e **pausa**, com auditoria e segredos
  robustos; fraca exatamente onde o Maestro é forte (consumo por agente, caixa de entrada).
- **LiteLLM** — **a mais completa das 25 em administração e consumo** (RBAC com 5 papéis, *Skills
  Registry*, orçamento por projeto/usuário/time, custo por agente A2A) e a segunda com **A2A de
  verdade** (`POST /a2a/{agent_id}/message/send`). **Rodou local de verdade** (proxy + Admin UI,
  capturas em `img/`). Fraqueza declarada: ciclo de vida — só *kill switch*, nada de subir.
  *Paywall*: auditoria, gestão de projeto e o *kill switch* exigem licença Enterprise.
- **Portkey** — gateway com **A2A ausente** (só MCP) e *alertas incompletos* declarados pela
  própria doc ("work in progress and not sent today"). O Agent Registry **cadastra** mas não lista
  saúde/versão.
- **OpenAI Platform** — forte em **limites de orçamento e custo** (limite de gasto devolve 429;
  alerta avisa mas não corta). **Alerta de vida**: a própria doc diz que **Agent Builder e Evals
  serão descontinuados — indisponíveis depois de 30/11/2026**; nada que dependa deles deve ser
  aposta da rodada 2.
- **Helicone** — é **observabilidade, não administração**: 13 células `—` (três `não` afirmados
  pela fonte: subir, lista de vivos, mensagem), nenhuma entidade de agente, nenhum papel/auditoria.
  O que salva é **custo por dimensão** e sessão como árvore de chamadas; o MCP é o dela mesma
  (consultar dados), não um gateway.
- **AgentOps** — quase todo `—`/`parcial`; nem um `sim`: custo e rastro/replay apoiavam-se só no
  README (não na UI) e desceram para `parcial` na correção da rodada 4 (ver `agentops.md`).
- **Langfuse** — o **melhor bloco de administração entre as 9 do Worker05** (RBAC, chaves e por
  projeto = `sim`; *auditoria* e *custo* `parcial` após as correções 1 e 2 — apoio só em lista de
  itens da página de segurança e em página de visão, não em página que documente o mecanismo); o
  ciclo de vida (subir/pausar/retomar) fica todo `—`.
- **LangSmith/LangGraph** — o único do bloco com **aprovação humana** forte
  (*human-in-the-loop*/*interrupts*), rastro/replay e alertas; RBAC e auditoria não aparecem.
- **CrewAI AMP** — um dos dois do bloco com **A2A** e o único com **mensagem entre agentes** além
  do AutoGen; limites, RBAC, custo e alertas todos `—`.
- **AutoGen Studio** — o único com **pausar = `sim`** fora do Temporal/Windmill; forte em cadastro
  (Team Builder, *Gallery*); **nem MCP nem A2A** são citados.
- **Dify** — o bloco CONTROLE inteiro `—`, exceto *subir/derrubar*, cuja ausência a fonte afirma
  (`não`); salva-se por **cadastro de skills** e **workspace por projeto**; RBAC só na Enterprise.
- **Flowise** — bom em administração (RBAC, SSO, *secret managers*, times/workspaces), mas a ficha
  registra um **alerta grave**: o repositório no GitHub está **arquivado/descontinuado pelo autor**.
- **Arize Phoenix** — a **mais vazia do conjunto**: um único `sim` (rastro/replay, *Span Replay*) e
  20 células `—`.
- **Comet Opik** — também quase só observabilidade (última atividade e rastro/replay); a doc
  oficial deu **404** e a fonte foi o README do GitHub.

Três leituras para a rodada 2 (confronto e decisão):

1. **A caixa de entrada e o livro de mensagens: `sim` em nenhuma das 25 — não encontrado na
   documentação lida.** O que o Maestro já faz — mensagem endereçada por nome entre sessões, com
   registro — não tem equivalente pronto para copiar nas fontes lidas. E o grupo INTERCOMUNICAÇÃO
   é o mais fraco (14%) — converge com o achado do Worker05.
2. **Intercomunicação com A2A é minoria: 5 fichas** (LiteLLM, CrewAI AMP, Copilot Studio, Agent 365,
   AgentCore). Nas demais o protocolo é só **MCP** — e em duas (AutoGen Studio, Arize Phoenix)
   nenhum dos dois aparece. Quem quiser A2A escolhe a plataforma por isso, não pelo painel.
3. **Duas plataformas desaconselhadas por escrito**: **Flowise** (repositório arquivado) e
   **OpenAI Agent Builder/Evals** (descontinuados após 30/11/2026). E a administração que parece
   mais madura é frequentemente **Enterprise** (LiteLLM, Portkey, Langfuse, Dify) — o "51% de
   ADMINISTRAÇÃO" não é 51% de graça.

## Lacunas declaradas

- **Notação**: `não` = a fonte **afirma** a ausência; `—` = **nenhuma fonte encontrada** (busca vazia
  ou célula vazia de prova). A divergência entre as duas gerações de ficha foi **resolvida na rodada
  2** (nota da legenda): 144 células `não → —`, 12 `não` mantidos. Hoje há **um só símbolo, uma só
  força** nas 25 colunas.
- **Apoio em marketing não vira `sim`** (correção da rodada 4): `sim` exige fonte que **descreva o
  mecanismo** (documentação ou README técnico), não *bullet* de marketing. Onde só havia marketing, a
  célula desceu para `parcial` (AgentOps *custo* e *rastro/replay*; Langfuse *custo*). Onde a fonte é
  o README técnico do repositório, a célula foi **mantida e declarada** para o juiz reavaliar.
- **Leitura**: onde **nenhuma** fonte foi encontrada, a leitura é "**não encontrado na documentação
  lida**" — nunca "lacuna de mercado": ausência de fonte não é prova de ausência no mercado.
- **Nada rodou local** exceto o LiteLLM (capturas em `pesquisa/img/`) e a própria sessão Claude Code.
- **Demo pública não abriu** onde foi tentada: `demo.portainer.io` recusou conexão
  (`connect ECONNREFUSED 114.23.206.2:443`), e as demos do Langfuse e da Helicone foram recusadas
  por exigirem conta. Por isso nenhuma célula se apoia em demo — só em documentação oficial.
- **Fontes que falharam**: `docs.temporal.io/batch-operations` e `visibility/batch-operations`
  deram HTTP 404; a doc oficial do Comet Opik (`www.comet.com/docs/opik/`) deu 404 e a fonte
  efetiva foi o README do GitHub.
- **Capturas**: só do LiteLLM, porque só ele rodou nesta máquina. As outras 24 são 100% documentais.

## Consideradas e não incluídas

Plataformas que a rodada 1 **não pesquisou**, com o motivo — para a rodada 2 não as tratar como
lacuna. Nenhuma entra na matriz (a matriz tem as 25 fichas com fonte); se alguma voltar, entra pelo
caminho da seção "Como acrescentar uma plataforma".

- **Cloudflare AI Gateway** — nicho de *gateway* de LLM; **deferida ao regente** (a fatia de
  gateway já cobre LiteLLM, Portkey, OpenAI Platform e Helicone).
- **Kong AI Gateway** — idem: *gateway*; **deferida ao regente**.
- **Bifrost** — idem: *gateway*; **deferida ao regente**.
- **Relevance AI** — estava no **despacho original** e **não foi pesquisada** (declarado).
- **Lindy** — estava no **despacho original** e **não foi pesquisada** (declarado).
- **Azure AI Foundry** — **não pesquisada**, por decisão de escopo da rodada.
- **Vertex AI Agent Builder** — **não pesquisada**, por decisão de escopo.
- **Salesforce Agentforce** — **não pesquisada**, por decisão de escopo.
- **Braintrust** — **não pesquisada**, por decisão de escopo.
- **W&B Weave** — **não pesquisada**, por decisão de escopo.
- **Letta** — **não pesquisada**, por decisão de escopo.
