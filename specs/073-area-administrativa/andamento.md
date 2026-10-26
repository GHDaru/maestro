# Andamento 073 — Área administrativa do Maestro

> Página de progresso viva (atualizada a cada DONE). Ciclo de pesquisa: **nenhum software** é
> construído aqui. Quatro rodadas: 1 pesquisa · 2 confronto e decisão · 3 wireframes (DDD, linguagem
> ubíqua) · 4 bar (três críticos, nota 0–10, passa com os três ≥ 9).

- **Data**: 2026-10-24 (pesquisa) · 2026-10-25 (consolidação, revisão, fechamento e rodada 2
  inteira) · 2026-10-26 (rodada 3 inteira) · **Lane**: plena · **Status**: **rodada 3 fechada** —
  glossário (+12 termos ratificados, colisões resolvidas por `arquivo:linha`), **11 wireframes
  estáticos das 13 ENTRA** (4 Mensageria + 3 Administração + 4 Workflow) no contrato de marcação,
  README do protótipo (13 ENTRA em 11 telas, navegação proposta marcada rodada 4), **fitness
  function `verifica-prototipo.py`** (4 regras; verde: 11 telas, 0 achados, exit 0), revisão em
  contexto fresco (9 achados de disciplina de nome/citação, nenhum estrutural) + **mutação do
  gate** (regras 3 e 4 cegas, achados que sumiram copiados da saída, script restaurado byte a
  byte), segurança documental (0 achados) e conformance 073 verde nos dois modos; **rodada de
  correção fechada** (R1–R9 por dono de tela; regra 4 ampliada ao texto visível); **rodada 4
  aberta** — preâmbulo integrado (R8 rename `741b130`, R9 base de citação `6a32e24`), três juízes
  em contexto fresco: **barra não atingida** (nenhuma peça em 9), **correção 1 (de máx. 2)
  despachada por dono** (`rodada-4/correcao-1.md`)
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

## Rodada 2 — confronto (passos 1–2)

| Task | Worker | Escopo | Estado |
|---|---|---|---|
| 073-T2-inventario | Worker05 | `confronto/inventario-maestro.md` — o que o Maestro já faz hoje para cada uma das 26 funcionalidades, com `arquivo:linha` | **entregue** — **tem 8 · parcial 16 · não tem 2** (de 26); só `pausar` e `retomar` faltam por inteiro |
| 073-T2-confronto | Worker03 | `confronto/confronto-decisao.md` — matriz 26 × {melhor referência, estado no Maestro, lacuna, decisão} | **entregue** — **ENTRA 13 · NÃO PRECISA 8 · DEPOIS 5**; INTERCOMUNICAÇÃO decidiu primeiro (6 `ENTRA` de 6) |

- Alimenta a coluna **"estado no Maestro"** que o W03 confronta com a matriz. `não tem` traz a força
  declarada (afirmado × não encontrado), espelhando a normalização de notação da matriz.
- A decisão do que entra (passo 2) cruza a matriz com esta coluna: `ENTRA` exige **fonte citada**
  (plataforma com ficha **ou** requisito do método) e nunca se apoia em célula `—`; `NÃO PRECISA`
  cobre o que o método já tem por inteiro e o que contraria o método; `DEPOIS` guarda a lacuna real
  com o gatilho declarado.

## Rodada 3 — wireframes das 13 ENTRA (DDD, linguagem ubíqua)

| Task | Worker | Escopo | Estado |
|---|---|---|---|
| 073-T3-glossario | Worker01 | os 12 termos ratificados em `docs/governance/glossary.md`, resolvendo as cinco colisões | **entregue** — `ebe7eb9`; acréscimo puro (+12/−0), colisões com `arquivo:linha` do mapa §7 |
| 073-T3-telas-mensageria | Worker03 | caixa de entrada, livro de mensagens, roteamento com colisão visível, protocolo de intercomunicação | **entregue** — `5f6dcf8` + correção do gate `ccf574c` (só atributos) |
| 073-T3-telas-administracao | Worker04 | catálogo de skills/ferramentas/modelos, políticas allow/deny/ask, limites de orçamento | **entregue** — `5ce4a5f` + correção do gate `7147f50` (só atributos) |
| 073-T3-telas-workflow | Worker05 | sessão de agente (subir/derrubar), estado do agente vivo, tarefa aberta, consumo por agente | **entregue** — `365f59d`+`fc183ce` (attempt=2 por redespacho; renomeadas `workflow-01..04` pela regente em `af81499`) + correção R4/R7/R9 `09c02f0` |
| 073-T3-readme-navegacao | Worker01 | `prototipo/README.md` (telas × ENTRA × contexto × juízes) e lugar na navegação | **entregue** — `e40f4bf`+`ff83e38` + complemento `e756232` (nomes reais, 11 telas, medição datada) |
| 073-T3-fitness | Gerente | `prototipo/verifica-prototipo.py` — gate executável dos wireframes | **entregue** — `fa4ee3e`→v3 `da85def`; 4 regras; verde sobre as 11 telas |
| 073-T3-revisao | Worker02 | revisão em contexto fresco das 11 telas + mutação do gate | **entregue** — `d1e9cc7`; 9 achados (nenhum estrutural), mutação 5→4 com o achado que sumiu |
| 073-T3-seguranca | Worker06 | segurança documental + conformance 073 nos dois modos | **entregue** — `bc36487`; 0 achados, conformance verde nos dois modos |
| 073-T3-regra4 | Worker02 | regra 4 do gate ampliada ao texto visível e a atributos | **entregue** — `9cf0118`+`1264194`; isenção declarada para tabela de colisão de nomes; mutação re-rodada 10→4 |
| correções R1–R9 | W03/W04/W05 | por dono de tela, mandato da regente | **entregues** — W03 `938d38b`, W04 `9fbbad3`, W05 `09c02f0`; R8/R9-mensageria declarados dívida da rodada 4 |
| 073-T3-fechamento | Gerente | gate final, conformance, andamento, DONE ao regente | **entregue** — ver qa-report § fechamento; **rodada 4 só com o "segue"** |

## Rodada 4 — o bar dos três juízes (26/10)

Pareceres dos três juízes (controle; administração e gerenciamento; intercomunicabilidade) sobre
`83c386e`: **barra não atingida** — os 13 ENTRA têm tela, as 25 plataformas têm ficha, o que falta
é teor. Pareceres e consolidação da regente em `rodada-4/` (commit `bce269b`). Correção 1 (de
máx. 2), despachada por dono a partir de `6a32e24`:

| Fatia | Dono | Estado |
|---|---|---|
| preâmbulo R8 (rename das 3 telas da Administração) | Worker04 | **integrado** — `9bb5917` → `741b130` |
| preâmbulo R9 (base de citação única + § Convenções + mapa §7 "fila outbox") | Worker02 | **integrado** — `46d254c` → `6a32e24` (conflitos do nav: hrefs do R8 + base nova) |
| correção 1 — Mensageria (4 telas) | Worker03 | **integrado** — `edbb32f`+`80a4c6d` → `d83920e`; gate 11 telas, 0 achados |
| correção 1 — Administração (3 telas) | Worker04 | **integrado** — `5be4a31` → `bfe1da5`; gate 11 telas, 0 achados |
| correção 1 — Workflow (4 telas) + inventário | Worker05 | **integrado** — `952ce53` (derrubar por confirmação com regente protegido, reiniciar no lugar de subir, ações por estado, travada com limiar, custo estimado em US$ com teto da Administração; inventário com SendMessage/ListAgents de primeira classe); gate 11/0 |
| correção 1 — confronto + mapa + regra 5 do verificador (identidade `nome · ref · projeto`, com mutação e fixture) | Worker02 | **integrado** — `11efa79` → `eb638b2` (ENTRA 15 · NÃO PRECISA 6 · DEPOIS 11; mapa com o orçamento na Administração, invariante de endereço ambíguo e § 7.1; regra 5 v4 com mutação 36→6 e fixtures) |
| fechamento da regra 5 nas telas (identidade `nome · ref · projeto` adjacente) | W03 + W05 | **integrado** — W05 `fb599bb` (4: ref logo depois do nome) + W03 `a04b6d0` (34: ref embutido no mesmo nó de texto; a causa era o `<span class="mono">` separando nome e ref em nós diferentes); **gate 11 telas, 0 achados com a regra 5 viva** |
| correção 1 — matriz (`plataformas.md`) | Worker06 | despachada |
| correção 1 — README + glossário | Worker01 | **integrado** — `0deccf4` (tabela de identidade, colisões termo × endereço, ENTRA 12 e 17, prosa obsoleta reescrita; glossário +2 termos); gate 11/0, check-language ✓ |

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
- 2026-10-25 — **073-T2-confronto entregue (Worker03)** — rodada 2, passo 2: o **confronto e a
  decisão do que entra**. `confronto/confronto-decisao.md` cruza as 26 funcionalidades com a melhor
  referência entre as 25 (com a ficha), o estado no Maestro (herdado do inventário) e a decisão:
  **ENTRA 13 · NÃO PRECISA 8 · DEPOIS 5**. Intercomunicação decidiu primeiro — **6 `ENTRA` de 6**
  (onde o mercado é vazio e o método opera à mão). Cada `ENTRA` traz nome na linguagem ubíqua,
  juízes da rodada 4 e fonte citada (plataforma com ficha **ou** requisito do método); **nenhum
  `ENTRA` se apoia em célula `—`**. Fecha com os totais e a **lista de 12 termos propostos** para o
  glossário. Sem push, sem merge.
- 2026-10-25 — **073-T2-revisao-confronto entregue (Worker05, contexto fresco)**: 6/6 linhas da
  amostragem dirigida conferem; recontagem PASS (13/8/5 e por grupo); regra 2 PASS (nenhum ENTRA
  sobre célula `—`); **1 bloqueante** — Princípio VIII: RBAC, RACI, A2A e MCP nus na primeira
  ocorrência — e 1 secundário (empates da "melhor referência" sem rótulo). **Corrigido pelo
  Gerente** (commit próprio) e verificado por script: toda primeira ocorrência de sigla expandida
  (PASS — o script achou também um ABAC que a revisão não viu); empates rotulados. Evidência no
  qa-report § "Revisão em contexto fresco do confronto".
- 2026-10-26 — **rodada 3 fechada (Gerente)**. Os 13 `ENTRA` cabem em **11 wireframes estáticos**
  (4 Mensageria · 3 Administração · 4 Workflow de sessões) em `prototipo/`, todos no contrato de
  marcação (data-fonte por bloco, data-rotulo com termo do glossário, data-exemplo com "(exemplo)",
  `—` sempre com motivo, citação sob data-fonte/data-referencia). **Fitness function**
  `verifica-prototipo.py`: 4 regras, **11 telas, 0 achados, exit 0** — com a regra 4 ampliada ao
  texto visível pela mutação do W02 ter provado que nenhuma tela real a exercitava. **Revisão
  fresca (W02)**: 9 achados de disciplina de nome/citação (nenhum estrutural); **correção por
  dono de tela** mandatada pela regente: R1/R1b/R2/R3 (W03), R4/R7/R9 (W05), R5/R2b/R6 (W04) —
  R8 (prefixo numérico da Administração) e R9-mensageria (base única de citação) declarados
  **dívida da rodada 4**; resalva do W03 registrada: o mapa §7 escreve "fila (outbox)" com
  parênteses, as telas seguem a grafia da regente "fila outbox" — alinhar a §7 é edição de doc
  para a rodada 4. **Segurança (W06)**: 0 achados (falsos positivos `sk-l`⊂"task-ledger" e
  `senha`⊂"desenhados" confirmados); conformance 073 verde nos dois modos. **Incidente
  declarado**: um marcador de conflito órfão (`<<<<<<< HEAD`) entrou no qa-report na resolução do
  merge `00c1ae9` (Gerente, 25/10) e propagou por todos os commits até ser achado e removido na
  resolução do merge do W04 (26/10, `6f71db7`). DONE ao regente com a lista das 11 telas, a saída
  do gate e os tokens; **rodada 4 (três juízes) só com o "segue"**.
- 2026-10-25 — **073-T2-mapa entregue (Worker02)** — rodada 2, passo 3: `confronto/mapa-de-contextos.md`
  — cinco contextos delimitados (Chamados e Gates · Workflow de sessões · Regência · Administração ·
  Mensageria) com raiz e invariantes, diagrama Mermaid, sete relacionamentos tipados com motivo,
  **core domain = Chamados e Gates** (leitura alternativa — Regência — declarada), linguagem ubíqua
  por contexto (12 termos propostos marcados) e **cinco colisões de nome reais** para a rodada 3.
  Divergências declaradas: o painel é projeção (não contexto); sexto contexto (Medição) recusado
  por YAGNI. **Rodada 2 fechada** — DONE ao regente; rodada 3 só depois do "segue".
