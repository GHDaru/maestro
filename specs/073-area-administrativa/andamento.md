# Andamento 073 — Área administrativa do Maestro

> Página de progresso viva (atualizada a cada DONE). Ciclo de pesquisa: **nenhum software** é
> construído aqui. Quatro rodadas: 1 pesquisa · 2 confronto e decisão · 3 wireframes (DDD, linguagem
> ubíqua) · 4 bar (três críticos, nota 0–10, passa com os três ≥ 9).

- **Data**: 2026-10-24 (pesquisa) · 2026-10-25 (consolidação, revisão, fechamento e preâmbulo da
  rodada 2) · **Lane**: plena · **Status**: rodada 1 **fechada e revisada** — 25 plataformas,
  matriz conferida por script; **preâmbulo da rodada 2 entregue** (normalização `não`/`—`, correções
  da amostragem; 25 × 26 = 650 células com um só símbolo por veredito)
- **Spec**: `spec.md` (rascunho aberto pelo Gerente a partir do despacho do regente)

## Rodada 1 — pesquisa de plataformas

| Task | Worker | Escopo | Estado |
|---|---|---|---|
| 073-T1-W03 | Worker03 | Gateways e consoles de LLM: LiteLLM Proxy Admin UI, Portkey, OpenAI Platform, Helicone | **entregue** — `pesquisa/litellm.md`, `pesquisa/portkey.md`, `pesquisa/openai-platform.md`, `pesquisa/helicone.md` + capturas do LiteLLM local em `pesquisa/img/` |
| 073-T1-W05 | Worker05 | Observabilidade e orquestração de agentes: AgentOps, Langfuse, LangSmith/LangGraph, CrewAI Enterprise (AMP), AutoGen Studio, Dify, Flowise | **entregue** — 9 arquivos (7 do despacho + 2 extras do mesmo nicho: Arize Phoenix, Comet Opik) |
| 073-T1-W06 | Worker06 | Controle de processos e governança: Temporal Web UI, Portainer CE, Prefect/Dagster, Copilot Studio/Agent 365, n8n, ecossistema Claude (Claude Code, Maestri canvas, Kiro Crew) | **entregue 24/10** — 12 fichas (as do despacho + AWS Bedrock AgentCore e Windmill, na mesma raia); pausou para a reverificação R1/R2 do 072 e retomou |
| consolidação | Worker06 | `pesquisa/plataformas.md` — matriz funcionalidade × plataforma | **entregue 25/10** — **25 plataformas × 26 funcionalidades = 650 células** (13 colunas acrescentadas por acréscimo: 4 do W03 + 9 do W05) |

- Critérios de aceite da rodada 1: ver `spec.md` §Acceptance criteria (arquivo por plataforma com
  fonte, matriz consolidada, nenhuma célula sem fonte, andamento atualizado a cada DONE).
- Orçamento: MAESTRO em 19% do consumo semanal, teto 40%; workers no gateway, tokens reportados por
  DONE.

## Rodada 2 — confronto (passo 1: inventário do Maestro)

| Task | Worker | Escopo | Estado |
|---|---|---|---|
| 073-T2-inventario | Worker05 | `confronto/inventario-maestro.md` — o que o Maestro já faz hoje para cada uma das 26 funcionalidades, com `arquivo:linha` | **entregue** — **tem 8 · parcial 16 · não tem 2** (de 26); só `pausar` e `retomar` faltam por inteiro |

- Alimenta a coluna **"estado no Maestro"** que o W03 confronta com a matriz. `não tem` traz a força
  declarada (afirmado × não encontrado), espelhando a normalização de notação da matriz.

## Histórico

- 2026-10-24 — **073-T1-W03 entregue (Worker03)**: quatro plataformas do nicho "gateways e
  consoles de LLM" com arquivo próprio e tabela fixa preenchida
  (`pesquisa/litellm.md`, `pesquisa/portkey.md`, `pesquisa/openai-platform.md`,
  `pesquisa/helicone.md`); capturas do LiteLLM rodando local em `pesquisa/img/`.
  Pendência declarada: a Admin UI autenticada do LiteLLM exige banco (sem Docker aqui).
- 2026-10-24 — ciclo aberto (`scripts/new-cycle.sh 073 area-administrativa`); spec da rodada 1
  escrita; três workers despachados (W03, W05, W06).
- 2026-10-24 — **W05 entregou** (073-T1-W05): 9 arquivos em `pesquisa/` —
  `agentops.md`, `langfuse.md`, `langsmith-langgraph.md`, `crewai-amp.md`, `autogen-studio.md`,
  `dify.md`, `flowise.md`, `arize-phoenix.md`, `comet-opik.md` — cada um com URL, data da visita
  (24/10), o que foi aberto de verdade (docs/repositório; demo do Langfuse não aberta por exigir
  conta) e a tabela fixa (26 itens) com fonte por célula. Nada rodou local; sem capturas.
- 2026-10-24 — **073-T1-W06 entregue**: 12 fichas de plataforma em `pesquisa/` (26 funcionalidades
  cada, célula sem fonte fica `—`) + `pesquisa/plataformas.md` (matriz consolidada parcial).
  Nada rodou localmente (`docker` e `temporal` ausentes; `demo.portainer.io` recusou conexão) —
  pesquisa 100% documental, nenhuma conta externa criada.
- 2026-10-24 — 072-T06 chamou no meio do 073: reverificação R1/R2 feita antes (attempt=2, commit
  `e0ff6f2`) e a pesquisa retomada depois.
- 2026-10-25 — **consolidação entregue** (073-T1-consolidacao, Worker06): `plataformas.md` fechada
  por acréscimo com as 13 colunas que faltavam (W03: litellm, portkey, openai-platform, helicone;
  W05: agentops, langfuse, langsmith-langgraph, crewai-amp, autogen-studio, dify, flowise,
  arize-phoenix, comet-opik) — **25 × 26 = 650 células**. Contagem conferida por script (27 colunas,
  26 linhas, 0 linhas com contagem de células errada) e 4 células sorteadas conferidas contra as
  fichas com caminho:linha. Achado declarado: as 13 fichas novas **não usam `—`** (W03 deixa em
  branco, W05 escreve `não` para "nada achei") — normalizar é decisão do dono da rodada.
- 2026-10-25 — **Gerente**: notação do consolidador **ratificada** (branco → `—`, `não`
  transcrito, divergência declarada na legenda; FR3 preservado); **normalização deferida ao
  preâmbulo da rodada 2**, onde a força do veredito passa a decidir no confronto. `plan.md`
  preenchido (Constitution Check 8/8, artefatos declarados com razão, modelo de domínio
  declarado) e `qa-report.md` estruturado. Revisão em contexto fresco despachada ao Worker03
  (073-T1-revisao: 7 células dirigidas + recontagem independente + passagem de segurança).
- 2026-10-25 — **073-T1-revisao entregue (Worker03, contexto fresco)**: 7/7 células conferem;
  contagens estruturais conferem; **1 achado bloqueante** — as tabelas de leitura da matriz
  subnotificavam o `sim` em 4 (alertas 6→8, mensagem entre agentes 7→8, consumo por agente 2→3;
  grupos GERENCIAMENTO 44→47, INTERCOMUNICAÇÃO 20→21) — e dois secundários (parêntese da LiteLLM,
  nota de divergência sem a Helicone). **Corrigido pelo Gerente** e reconferido por script fora do
  repo: todo número das tabelas de leitura agora bate com a matriz (PASS). Segurança: varredura
  limpa (0 achados não-declarados; o único casamento é o placeholder declarado do LiteLLM).
  Rabo do ciclo: review e security marcados com evidência; mutation n/a (rodada documental);
  gate do regente. **Rodada 1 fechada** — DONE ao regente com a matriz; rodada 2 só depois do
  "segue".
- 2026-10-25 — **preâmbulo da rodada 2 entregue** (073-T2-preambulo, Worker06): normalização da
  força do veredito, célula a célula, relendo as 13 fichas do W03/W05 — **143 `não → —`**, **13
  `não` mantidos** (a fonte afirma a ausência), **nenhum `—` → `sim`**; a regra foi gravada na
  legenda da matriz e a divergência dada por **resolvida**. Correções da amostragem do crítico em
  contexto fresco: Temporal *lista de vivos* e *tarefa aberta* `sim → parcial`, Maestri 6 → 5
  células `—` em CONTROLE, INTERCOMUNICAÇÃO 13% → 14%. **Distribuição medida por script:** `sim` 172
  · `parcial` 223 · `não` 13 · `—` 242 = **650**. Seção nova "Consideradas e não incluídas" (11
  plataformas). Sem push, sem merge.
- 2026-10-25 — **073-T2-inventario entregue (Worker05)** — rodada 2, passo 1: o Gerente despachou o
  **inventário do Maestro** (o que o método já faz hoje para cada uma das 26 funcionalidades). Feito
  por cinco varreduras dirigidas (`docs/governance/`, `docs/adr/`, `docs/records/`, `docs/agents/`,
  `docs/handbook/`, `scripts/`, `.claude/agents/`, `.claude/commands/`, `skills/`, `painel/`,
  `.github/`, `mods/`), com evidência `arquivo:linha` em cada linha `tem`/`parcial`. Resultado:
  `confronto/inventario-maestro.md` — **tem 8 · parcial 16 · não tem 2**; o que falta por inteiro é o
  ciclo de vida (CONTROLE: `pausar`, `retomar`), e o Maestro é mais forte justamente onde a matriz é
  vazia (INTERCOMUNICAÇÃO).
