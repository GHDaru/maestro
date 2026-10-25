# Matriz consolidada: funcionalidade × plataforma (ciclo 073, rodada 1)

> **Consolidação parcial** — cobre as **12 plataformas** do escopo do Worker06 (controle de
> processos e governança). As plataformas dos escopos do Worker03 (gateways e consoles de
> *Large Language Model*, LLM) e do Worker05 (observabilidade e orquestração de agentes) ainda
> **não** estavam publicadas em `pesquisa/` quando esta matriz foi gerada; a estrutura abaixo é
> a mesma e recebe as colunas delas por acréscimo (ver "Como acrescentar uma plataforma").

- **Data**: 2026-10-24 · **Ciclo**: 073 "área administrativa do Maestro" · **Rodada**: 1 (pesquisa)
- **Fonte de cada célula**: a **ficha da coluna** — cada ficha traz a URL visitada e o que foi
  visto na página (ver `pesquisa/<slug>.md`). A matriz é o índice; a prova está na ficha.
- **Nada foi executado** para estas 12 plataformas: `docker` não existe nesta máquina, o binário
  `temporal` não está instalado e nenhuma conta externa foi criada. A `claude-code.md` é a
  exceção parcial: é a ferramenta que roda esta sessão, e algumas capacidades foram vistas em uso.
- **Fichas desta matriz**: [Temporal Web UI](temporal-web-ui.md) ·
  [Portainer CE](portainer-ce.md) · [Prefect](prefect.md) · [Dagster](dagster.md) ·
  [Copilot Studio](copilot-studio.md) · [Agent 365](agent-365.md) · [n8n](n8n.md) ·
  [Claude Code](claude-code.md) · [Maestri canvas](maestri-canvas.md) ·
  [Kiro Crew](kiro-crew.md) · [AWS Bedrock AgentCore](aws-bedrock-agentcore.md) ·
  [Windmill](windmill.md)

## Legenda

| Símbolo | Significa |
|---|---|
| **sim** | a funcionalidade existe **e** foi vista na fonte citada pela ficha |
| **parcial** | existe de forma incompleta, só em plano pago, só em nuvem, ou por analogia (a ficha diz por quê) |
| **não** | a fonte **afirma** que não existe (raro — ex.: Kiro Crew não tem pausa documentada) |
| **—** | **nenhuma fonte encontrada**. Célula vazia de prova; **não** quer dizer "sim" nem "não" |

Siglas expandidas na primeira ocorrência: **RBAC** (*Role-Based Access Control*) · **MCP**
(*Model Context Protocol*) · **A2A** (*Agent-to-Agent*) · **CE** (*Community Edition*) · **LLM**
(*Large Language Model*) · **UI** (*User Interface*).

## A matriz

| Grupo | Funcionalidade | [Temporal](temporal-web-ui.md) | [Portainer CE](portainer-ce.md) | [Prefect](prefect.md) | [Dagster](dagster.md) | [Copilot Studio](copilot-studio.md) | [Agent 365](agent-365.md) | [n8n](n8n.md) | [Claude Code](claude-code.md) | [Maestri](maestri-canvas.md) | [Kiro Crew](kiro-crew.md) | [AgentCore](aws-bedrock-agentcore.md) | [Windmill](windmill.md) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CONTROLE | subir/derrubar sessão ou agente | sim | sim | parcial | parcial | parcial | parcial | parcial | sim | parcial | parcial | sim | parcial |
| CONTROLE | pausar | sim | — | parcial | parcial | — | — | parcial | parcial | — | não | parcial | sim |
| CONTROLE | retomar | sim | — | parcial | parcial | — | — | parcial | sim | — | sim | sim | parcial |
| CONTROLE | limites de orçamento e de taxa | parcial | — | parcial | parcial | sim | — | sim | parcial | — | parcial | sim | parcial |
| CONTROLE | políticas allow/deny/ask | — | parcial | parcial | parcial | sim | sim | parcial | sim | — | sim | sim | parcial |
| CONTROLE | aprovação humana | — | — | parcial | — | parcial | sim | sim | sim | — | sim | parcial | sim |
| ADMINISTRAÇÃO | cadastro de agentes | — | sim | parcial | parcial | sim | sim | — | sim | sim | sim | sim | parcial |
| ADMINISTRAÇÃO | papéis e permissões RBAC | parcial | sim | sim | sim | sim | sim | sim | parcial | parcial | parcial | sim | sim |
| ADMINISTRAÇÃO | cadastro de skills/ferramentas/modelos | — | sim | — | — | sim | parcial | sim | sim | parcial | sim | sim | sim |
| ADMINISTRAÇÃO | chaves e segredos | sim | sim | sim | sim | parcial | — | parcial | sim | — | sim | sim | sim |
| ADMINISTRAÇÃO | configuração por projeto | sim | sim | sim | sim | parcial | — | sim | sim | sim | sim | parcial | sim |
| ADMINISTRAÇÃO | auditoria | parcial | parcial | sim | sim | sim | sim | parcial | parcial | — | sim | sim | sim |
| GERENCIAMENTO | lista de agentes vivos com estado | sim | sim | parcial | parcial | sim | sim | — | sim | parcial | parcial | sim | parcial |
| GERENCIAMENTO | tarefa aberta | sim | — | parcial | parcial | — | parcial | parcial | sim | parcial | sim | parcial | sim |
| GERENCIAMENTO | última atividade | parcial | — | parcial | parcial | sim | parcial | sim | parcial | parcial | parcial | parcial | parcial |
| GERENCIAMENTO | consumo por agente/sessão/modelo | parcial | — | — | parcial | sim | parcial | parcial | sim | — | parcial | parcial | — |
| GERENCIAMENTO | custo | parcial | — | — | parcial | sim | — | sim | sim | — | parcial | parcial | parcial |
| GERENCIAMENTO | filas e workers | sim | — | sim | parcial | — | — | sim | parcial | — | — | parcial | sim |
| GERENCIAMENTO | rastro/replay de sessão | sim | parcial | parcial | parcial | sim | parcial | sim | parcial | parcial | parcial | sim | parcial |
| GERENCIAMENTO | alertas | parcial | — | sim | sim | parcial | parcial | parcial | parcial | — | parcial | parcial | sim |
| INTERCOMUNICAÇÃO | mensagem entre agentes | sim | — | — | — | sim | parcial | parcial | sim | sim | parcial | sim | parcial |
| INTERCOMUNICAÇÃO | protocolos (A2A, MCP) | parcial | — | parcial | parcial | sim | sim | parcial | parcial | — | parcial | sim | parcial |
| INTERCOMUNICAÇÃO | caixa de entrada | — | — | — | — | — | — | — | parcial | parcial | não | — | — |
| INTERCOMUNICAÇÃO | roteamento por nome/ref | sim | — | parcial | — | sim | parcial | parcial | sim | parcial | sim | sim | sim |
| INTERCOMUNICAÇÃO | livro de mensagens | — | — | — | — | — | — | — | — | parcial | — | parcial | parcial |
| INTERCOMUNICAÇÃO | colisão de nomes | parcial | — | — | — | — | — | — | parcial | — | sim | — | sim |

## Como acrescentar uma plataforma

1. Escreva a ficha `pesquisa/<slug>.md` com URL, data da visita, o que foi **aberto de verdade**
   e a tabela fixa de 26 linhas (a mesma ordem desta matriz).
2. Acrescente **uma coluna** à matriz, no fim ou junto do bloco temático, com o rótulo linkando a
   ficha; transfira as 26 células na ordem.
3. Nenhuma célula entra sem prova: sem fonte na ficha, fica `—`.

## Leitura da matriz (o que os números dizem)

**Por plataforma** — uma linha cada, do que a plataforma é boa:

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
  propriamente dito) e uma das três com **A2A**; sem filas/workers.
- **Agent 365** — o **plano de controle** do lado Microsoft: políticas `allow/deny/ask`,
  aprovação humana, cadastro e **auditoria** de agentes; consumo/custo só parciais.
- **n8n** — a mais **larga em controle de execução** (pausar/retomar/limites/aprovação humana) e
  a única com **custo** e **alertas** simultaneamente fortes; mensageria entre agentes só parcial.
- **Claude Code** — a única que cobre **sessão de agente de ponta a ponta**: subir, retomar,
  listar por estado, consumo por agente (`agent.name`), custo em dólar e mensagem entre sessões.
  É a plataforma que **roda nesta sessão**.
- **Maestri canvas** — a mais **fraca em controle** (6 células `—` no grupo CONTROLE) e a única
  cuja intercomunicação é por **PTY** (*pseudo-terminal*), com caixa de entrada e livro de
  mensagens parciais.
- **Kiro Crew** — a mais **completa em administração** (só RBAC é parcial) e a única que
  **documenta a ausência** de pausa e de caixa de entrada; forte em **colisão de nomes**.
- **AWS Bedrock AgentCore** — a **mais completa no total** (só 2 células `—`): sessão, limites,
  políticas, cadastro, auditoria, rastro e mensageria com **A2A**.
- **Windmill** — a mais forte em **filas e workers** e **pausa**, com auditoria e segredos
  robustos; fraca exatamente onde o Maestro é forte (consumo por agente, caixa de entrada).

**Por funcionalidade** — onde o campo está vazio (contagem de `sim` entre as 12):

| Funcionalidade | `sim` | Leitura |
|---|---|---|
| caixa de entrada | **0** | **ninguém** entrega; o mais próximo é estado `Needs input` (Claude Code) e a caixa por PTY (Maestri) — ambas **parciais** |
| livro de mensagens | **0** | **ninguém** entrega; só históricos de conversa parciais (Maestri, AgentCore, Windmill) |
| pausar | 2 | só Temporal e Windmill |
| colisão de nomes | 2 | só Kiro Crew e Windmill |
| última atividade · consumo por agente/sessão/modelo | 2 cada | consumo por agente só em Copilot Studio e Claude Code |
| limites de orçamento e de taxa · custo · protocolos (A2A, MCP) · alertas | 3 cada | **A2A** documentado em apenas três fichas (Copilot Studio, Agent 365, AgentCore); nas demais o protocolo é só **MCP** |

Duas leituras para a rodada 2 (confronto e decisão):

1. **A caixa de entrada e o livro de mensagens não existem em nenhuma das 12.** O que o Maestro já
   faz — mensagem endereçada por nome entre sessões, com registro — não tem equivalente pronto para
   copiar; é lacuna de mercado, não falta de pesquisa.
2. **A intercomunicação é quase toda MCP; A2A aparece em três fichas.** Quem quiser A2A de verdade
   precisa escolher a plataforma por causa disso, não pelo painel.

## Lacunas declaradas

- A matriz **não** cobre as plataformas do Worker03 e do Worker05 (ainda não publicadas).
- Quatro fichas têm itens `—` por **404** ou ausência de página, registrados como tentativa-e-falha
  em cada ficha (ex.: `docs.temporal.io/batch-operations` → HTTP 404).
- Nenhuma demo pública respondeu: `demo.portainer.io` recusou conexão
  (`connect ECONNREFUSED 114.23.206.2:443`, registrado na ficha do Portainer CE). Por isso
  **nenhuma** célula se apoia em demo — só em documentação oficial.
