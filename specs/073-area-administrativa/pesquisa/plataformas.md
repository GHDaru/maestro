# Matriz consolidada: funcionalidade × plataforma (ciclo 073, rodada 1)

> **Consolidação completa** — as **25 plataformas** das três fatias da rodada 1 (controle de
> processos e governança · gateways e consoles de *Large Language Model*, LLM · observabilidade e
> orquestração de agentes), 26 funcionalidades cada: **650 células**. Fechada por acréscimo, como a
> seção "Como acrescentar uma plataforma" previu.

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
| **não** | a ficha registra ausência |
| **—** | **nenhuma fonte encontrada**. Célula vazia de prova; **não** quer dizer "sim" nem "não" |

Siglas expandidas na primeira ocorrência: **RBAC** (*Role-Based Access Control*) · **MCP**
(*Model Context Protocol*) · **A2A** (*Agent-to-Agent*) · **CE** (*Community Edition*) · **LLM**
(*Large Language Model*) · **UI** (*User Interface*) · **OSS** (*Open Source Software*) · **SSO**
(*Single Sign-On*) · **PTY** (*Pseudo-Terminal*).

> **Divergência de notação entre as duas gerações de ficha** (declarada; normalização deferida ao
> preâmbulo da rodada 2 pelo Gerente). As 12 fichas do Worker06 marcam "sem fonte" com `—` e
> reservam `não` para a ausência **afirmada** pela fonte. As 13 fichas do Worker03/Worker05 **não
> usam `—`**: o Worker03 deixa a célula **em branco** (21 células — e na Helicone escreve `não`
> para "nada achei" em ao menos duas: auditoria e caixa de entrada) e o Worker05 escreve
> **`não`** para "nada achei". Nesta matriz, célula em branco virou `—` (é o que a legenda manda)
> e `não` foi transcrito como a ficha escreveu. Efeito a lembrar na leitura: nas colunas do
> Worker05 — e nas duas células citadas da Helicone —, um `não` costuma significar
> **"não encontrei"**, não "a fonte afirma que não existe". As duas leituras são conformes ao FR3
> (nenhuma célula sem fonte vira "sim"); o que muda é a força do veredito.

## A matriz

| Grupo | Funcionalidade | [Temporal](temporal-web-ui.md) | [Portainer CE](portainer-ce.md) | [Prefect](prefect.md) | [Dagster](dagster.md) | [Copilot Studio](copilot-studio.md) | [Agent 365](agent-365.md) | [n8n](n8n.md) | [Claude Code](claude-code.md) | [Maestri](maestri-canvas.md) | [Kiro Crew](kiro-crew.md) | [AgentCore](aws-bedrock-agentcore.md) | [Windmill](windmill.md) | [LiteLLM](litellm.md) | [Portkey](portkey.md) | [OpenAI Platform](openai-platform.md) | [Helicone](helicone.md) | [AgentOps](agentops.md) | [Langfuse](langfuse.md) | [LangSmith/LG](langsmith-langgraph.md) | [CrewAI AMP](crewai-amp.md) | [AutoGen Studio](autogen-studio.md) | [Dify](dify.md) | [Flowise](flowise.md) | [Arize Phoenix](arize-phoenix.md) | [Comet Opik](comet-opik.md) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CONTROLE | subir/derrubar sessão ou agente | sim | sim | parcial | parcial | parcial | parcial | parcial | sim | parcial | parcial | sim | parcial | parcial | parcial | parcial | não | parcial | não | parcial | parcial | parcial | não | não | não | não |
| CONTROLE | pausar | sim | — | parcial | parcial | — | — | parcial | parcial | — | não | parcial | sim | não | não | não | — | não | não | não | não | sim | não | não | não | não |
| CONTROLE | retomar | sim | — | parcial | parcial | — | — | parcial | sim | — | sim | sim | parcial | não | — | — | — | não | não | parcial | parcial | parcial | não | não | não | não |
| CONTROLE | limites de orçamento e de taxa | parcial | — | parcial | parcial | sim | — | sim | parcial | — | parcial | sim | parcial | sim | sim | sim | parcial | parcial | não | parcial | não | não | não | parcial | não | não |
| CONTROLE | políticas allow/deny/ask | — | parcial | parcial | parcial | sim | sim | parcial | sim | — | sim | sim | parcial | parcial | parcial | parcial | parcial | não | não | não | não | não | não | parcial | não | não |
| CONTROLE | aprovação humana | — | — | parcial | — | parcial | sim | sim | sim | — | sim | parcial | sim | não | parcial | parcial | — | não | parcial | sim | sim | parcial | não | sim | não | não |
| ADMINISTRAÇÃO | cadastro de agentes | — | sim | parcial | parcial | sim | sim | — | sim | sim | sim | sim | parcial | sim | sim | parcial | não | parcial | não | parcial | parcial | sim | parcial | sim | não | não |
| ADMINISTRAÇÃO | papéis e permissões RBAC | parcial | sim | sim | sim | sim | sim | sim | parcial | parcial | parcial | sim | sim | sim | sim | sim | não | não | sim | não | não | não | parcial | sim | não | não |
| ADMINISTRAÇÃO | cadastro de skills/ferramentas/modelos | — | sim | — | — | sim | parcial | sim | sim | parcial | sim | sim | sim | sim | sim | parcial | parcial | parcial | parcial | parcial | sim | sim | sim | sim | parcial | parcial |
| ADMINISTRAÇÃO | chaves e segredos | sim | sim | sim | sim | parcial | — | parcial | sim | — | sim | sim | sim | sim | sim | sim | parcial | parcial | sim | parcial | não | parcial | parcial | sim | não | parcial |
| ADMINISTRAÇÃO | configuração por projeto | sim | sim | sim | sim | parcial | — | sim | sim | sim | sim | parcial | sim | sim | sim | sim | — | não | sim | não | parcial | parcial | sim | sim | não | parcial |
| ADMINISTRAÇÃO | auditoria | parcial | parcial | sim | sim | sim | sim | parcial | parcial | — | sim | sim | sim | sim | sim | sim | não | não | sim | não | parcial | não | não | parcial | não | não |
| GERENCIAMENTO | lista de agentes vivos com estado | sim | sim | parcial | parcial | sim | sim | — | sim | parcial | parcial | sim | parcial | parcial | não | não | não | parcial | não | não | não | parcial | não | não | não | não |
| GERENCIAMENTO | tarefa aberta | sim | — | parcial | parcial | — | parcial | parcial | sim | parcial | sim | parcial | sim | — | — | — | — | não | não | não | não | parcial | não | não | não | não |
| GERENCIAMENTO | última atividade | parcial | — | parcial | parcial | sim | parcial | sim | parcial | parcial | parcial | parcial | parcial | parcial | parcial | parcial | sim | parcial | parcial | parcial | parcial | parcial | sim | parcial | parcial | sim |
| GERENCIAMENTO | consumo por agente/sessão/modelo | parcial | — | — | parcial | sim | parcial | parcial | sim | — | parcial | parcial | — | sim | parcial | parcial | parcial | parcial | parcial | não | não | não | parcial | não | não | parcial |
| GERENCIAMENTO | custo | parcial | — | — | parcial | sim | — | sim | sim | — | parcial | parcial | parcial | sim | sim | sim | sim | sim | sim | parcial | não | não | parcial | não | não | parcial |
| GERENCIAMENTO | filas e workers | sim | — | sim | parcial | — | — | sim | parcial | — | — | parcial | sim | não | — | parcial | — | não | não | não | não | não | não | não | não | não |
| GERENCIAMENTO | rastro/replay de sessão | sim | parcial | parcial | parcial | sim | parcial | sim | parcial | parcial | parcial | sim | parcial | parcial | parcial | parcial | parcial | sim | parcial | sim | parcial | parcial | parcial | parcial | sim | sim |
| GERENCIAMENTO | alertas | parcial | — | sim | sim | parcial | parcial | parcial | parcial | — | parcial | parcial | sim | sim | parcial | sim | sim | parcial | sim | sim | não | não | não | não | não | parcial |
| INTERCOMUNICAÇÃO | mensagem entre agentes | sim | — | — | — | sim | parcial | parcial | sim | sim | parcial | sim | parcial | sim | não | parcial | não | não | não | não | sim | sim | não | parcial | não | não |
| INTERCOMUNICAÇÃO | protocolos (A2A, MCP) | parcial | — | parcial | parcial | sim | sim | parcial | parcial | — | parcial | sim | parcial | sim | parcial | parcial | parcial | parcial | parcial | parcial | sim | não | parcial | parcial | não | parcial |
| INTERCOMUNICAÇÃO | caixa de entrada | — | — | — | — | — | — | — | parcial | parcial | não | — | — | não | — | — | não | não | não | não | não | não | não | não | não | não |
| INTERCOMUNICAÇÃO | roteamento por nome/ref | sim | — | parcial | — | sim | parcial | parcial | sim | parcial | sim | sim | sim | parcial | parcial | não | — | não | não | não | parcial | parcial | não | não | não | não |
| INTERCOMUNICAÇÃO | livro de mensagens | — | — | — | — | — | — | — | — | parcial | — | parcial | parcial | parcial | — | parcial | — | não | não | não | não | parcial | não | não | não | não |
| INTERCOMUNICAÇÃO | colisão de nomes | parcial | — | — | — | — | — | — | parcial | — | sim | — | sim | — | — | — | — | não | não | não | não | não | não | não | não | não |

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

**Por grupo** — `sim` sobre o total de células do grupo, nas 25 plataformas:

| Grupo | `sim` | Células | Aproveitamento | Leitura |
|---|---|---|---|---|
| ADMINISTRAÇÃO | 76 | 150 | **51%** | o que o mercado sabe fazer: cadastro, RBAC, segredos, por projeto, auditoria |
| GERENCIAMENTO | 47 | 200 | **23,5%** | metade é observabilidade; "agentes vivos" e consumo por agente quase não existem |
| CONTROLE | 30 | 150 | **20%** | ciclo de vida é o buraco: pausar tem 3 `sim` em 25 |
| INTERCOMUNICAÇÃO | 21 | 150 | **14%** | **o grupo mais fraco** — e é exatamente o que o Maestro já opera a mão |

**Por funcionalidade** — contagem de `sim` nas 25 plataformas, do mais coberto ao menos:

| Funcionalidade | `sim` | Leitura |
|---|---|---|
| configuração por projeto | 15 | o mais maduro do conjunto |
| papéis e permissões RBAC · cadastro de skills/ferramentas/modelos · chaves e segredos | 13 cada | a base de administração é commodity |
| cadastro de agentes · auditoria | 11 cada | o "cadastro de agentes" é **registro**, quase nunca processo vivo |
| custo | 9 | custo de *token* é comum; custo de operação de agente, não |
| aprovação humana · rastro/replay de sessão · alertas · mensagem entre agentes | 8 cada | human-in-the-loop existe onde há grafo de execução; e a mensagem entre agentes é quase toda delegação dentro do processo, não mensagem entre pares |
| limites de orçamento e de taxa · lista de agentes vivos com estado · roteamento por nome/ref | 6 cada | orçamento por chave/projeto, raramente por agente |
| políticas allow/deny/ask · protocolos (A2A, MCP) · última atividade | 5 cada | |
| subir/derrubar sessão ou agente · retomar · tarefa aberta · filas e workers | 4 cada | |
| pausar · consumo por agente/sessão/modelo | 3 cada | consumo por agente em **Copilot Studio**, **Claude Code** e **LiteLLM** |
| colisão de nomes | 2 | |
| **caixa de entrada** · **livro de mensagens** | **0 cada** | **nenhuma** das 25 entrega |

**Por plataforma** — uma linha cada (as 12 primeiras são da fatia do Worker06):

- **Temporal Web UI** — a melhor em **rastro/replay** (History em 4 formatos, *download* do
  histórico, Reset) e em **filas e workers** (Workers por Task Queue, Pending Activities). Tudo
  de administração (RBAC, auditoria, chaves, limites) é **exclusivo do Temporal Cloud**.
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
- **Maestri canvas** — a mais **fraca em controle** (6 células `—` no grupo CONTROLE) e a única
  cuja intercomunicação é por **PTY** (*Pseudo-Terminal*), com caixa de entrada e livro de
  mensagens parciais.
- **Kiro Crew** — a mais **completa em administração** (só RBAC é parcial) e a única que
  **documenta a ausência** de pausa e de caixa de entrada; forte em **colisão de nomes**.
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
- **Helicone** — é **observabilidade, não administração**: 9 células `—`, nenhuma entidade de
  agente, nenhum papel/auditoria. O que salva é **custo por dimensão** e sessão como árvore de
  chamadas; o MCP é o dela mesma (consultar dados), não um gateway.
- **AgentOps** — quase todo `não`/`parcial`; os dois únicos `sim` (custo e rastro/replay) vêm do
  README, não da UI.
- **Langfuse** — o **melhor bloco de administração entre as 9 do Worker05** (RBAC, chaves, por
  projeto e auditoria = `sim`); controle de sessão inteiro `não`.
- **LangSmith/LangGraph** — o único do bloco com **aprovação humana** forte
  (*human-in-the-loop*/*interrupts*), rastro/replay e alertas; RBAC e auditoria não aparecem.
- **CrewAI AMP** — um dos dois do bloco com **A2A** e o único com **mensagem entre agentes** além
  do AutoGen; limites, RBAC, custo e alertas todos `não`.
- **AutoGen Studio** — o único com **pausar = `sim`** fora do Temporal/Windmill; forte em cadastro
  (Team Builder, *Gallery*); **nem MCP nem A2A** são citados.
- **Dify** — o bloco CONTROLE inteiro `não`; salva-se por **cadastro de skills** e **workspace por
  projeto**; RBAC só na Enterprise.
- **Flowise** — bom em administração (RBAC, SSO, *secret managers*, times/workspaces), mas a ficha
  registra um **alerta grave**: o repositório no GitHub está **arquivado/descontinuado pelo autor**.
- **Arize Phoenix** — a **mais vazia do conjunto**: um único `sim` (rastro/replay, *Span Replay*).
- **Comet Opik** — também quase só observabilidade (última atividade e rastro/replay); a doc
  oficial deu **404** e a fonte foi o README do GitHub.

Três leituras para a rodada 2 (confronto e decisão):

1. **A caixa de entrada e o livro de mensagens não existem em nenhuma das 25.** O que o Maestro já
   faz — mensagem endereçada por nome entre sessões, com registro — não tem equivalente pronto para
   copiar; é lacuna de mercado, não falta de pesquisa. E o grupo INTERCOMUNICAÇÃO é o mais fraco
   (13%) — converge com o achado do Worker05.
2. **Intercomunicação com A2A é minoria: 5 fichas** (LiteLLM, CrewAI AMP, Copilot Studio, Agent 365,
   AgentCore). Nas demais o protocolo é só **MCP** — e em duas (AutoGen Studio, Arize Phoenix)
   nenhum dos dois aparece. Quem quiser A2A escolhe a plataforma por isso, não pelo painel.
3. **Duas plataformas desaconselhadas por escrito**: **Flowise** (repositório arquivado) e
   **OpenAI Agent Builder/Evals** (descontinuados após 30/11/2026). E a administração que parece
   mais madura é frequentemente **Enterprise** (LiteLLM, Portkey, Langfuse, Dify) — o "51% de
   ADMINISTRAÇÃO" não é 51% de graça.

## Lacunas declaradas

- **Notação**: ver a nota da divergência entre gerações de ficha, acima. Nas colunas do Worker05,
  `não` geralmente é "não encontrei".
- **Nada rodou local** exceto o LiteLLM (capturas em `pesquisa/img/`) e a própria sessão Claude Code.
- **Demo pública não abriu** onde foi tentada: `demo.portainer.io` recusou conexão
  (`connect ECONNREFUSED 114.23.206.2:443`), e as demos do Langfuse e da Helicone foram recusadas
  por exigirem conta. Por isso nenhuma célula se apoia em demo — só em documentação oficial.
- **Fontes que falharam**: `docs.temporal.io/batch-operations` e `visibility/batch-operations`
  deram HTTP 404; a doc oficial do Comet Opik (`www.comet.com/docs/opik/`) deu 404 e a fonte
  efetiva foi o README do GitHub.
- **Capturas**: só do LiteLLM, porque só ele rodou nesta máquina. As outras 24 são 100% documentais.
