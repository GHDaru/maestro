# QA report 073 — Área administrativa do Maestro (rodada 1: pesquisa de plataformas)

- **Date**: 2026-10-24 (fichas) · 2026-10-25 (consolidação, revisão e fechamento) · **Lane**:
  plena · **Verdict**: approved (rodada 1) — 7/7 células conferem, contagens estruturais
  conferem, 1 achado bloqueante (subnotificação de 4 `sim` nas tabelas de leitura) corrigido e
  reconferido por script; segurança limpa

## Fitness functions (DoD)
| Check | Expected | Result |
|---|---|---|
| `scripts/check-cycle.sh 073` | lane justificada | **ok** — "lane 'full' with rationale" (justificativa dos três fatores no spec, commit `b186214`) |
| Colunas da matriz (`pesquisa/plataformas.md`) | 2 + 25 = 27 | **27** (medido por script sobre o arquivo, Worker06) |
| Linhas de funcionalidade | 26 | **26**, na ordem da tabela fixa da spec |
| Linhas com contagem de células ≠ 27 | 0 | **0** |
| Células da matriz | 25 × 26 = 650 | **650** |
| Fichas com tabela fixa completa | 25 × 26 = 650 | **650** — 629 com veredito explícito + 21 células em branco (convertidas em `—` na matriz) |
| Tabelas de leitura × matriz (script fora do repo, pós-correção) | todo número confere | **PASS** — sim 174 · parcial 221 · não 156 · — 99; grupos CONTROLE 30 · ADMINISTRAÇÃO 76 · GERENCIAMENTO 47 · INTERCOMUNICAÇÃO 21 |
| `scripts/check-conformance.sh 073` | verde nos dois modos | (preenchido no fechamento da rodada) |

## Closing tail — the evidence
<!-- One entry per non-n/a TAIL token. What was OBSERVED, never the intention restated. -->
- TAIL:review — Worker03, contexto fresco (não consolidou; amostragem escolhida pelo Gerente):
  7/7 células conferem contra as fichas com caminho:linha; contagens estruturais conferem
  (27/26/0/650); **1 achado bloqueante** — as tabelas de leitura subnotificavam o `sim` em 4
  (alertas 6→8, mensagem entre agentes 7→8, consumo por agente 2→3; total 170→174; grupos
  GERENCIAMENTO 44→47 e INTERCOMUNICAÇÃO 20→21) — **corrigido pelo Gerente** (commit próprio) e
  **reconferido por script**: todo número das tabelas de leitura agora bate com a matriz
  (PASS — sim 174 · parcial 221 · não 156 · — 99); dois secundários corrigidos na mesma família
  (parêntese da LiteLLM em `:120`; nota de divergência estendida à Helicone). Evidência completa
  na seção "Reverificação em contexto fresco", abaixo.
- TAIL:security — Worker03, varredura sobre `pesquisa/` (28 arquivos, 14 padrões, PNG lidos como
  bytes e **olhados**): **0 achados fora da lista declarada**; 1 casamento —
  `sk-local-demo-073-nao-e-segredo` em `litellm.md:18` — é placeholder local declarado na própria
  ficha; capturas só mostram tela de login vazia; nenhuma conta externa criada; a única execução
  real é a LiteLLM local com chave descartável. **Limpo.**
- TAIL:mutation — n/a: rodada documental — nenhum gate executável foi criado ou alterado neste ciclo (não há código); o veredito verificável da rodada é a contagem e a amostragem contra as fichas, cobertas no TAIL:review
- TAIL:gate — o gate humano da rodada 1 é o **"segue" do regente para a rodada 2** (confronto
  com o Maestro e decisão do que entra); sem ele, nada avança. A rodada 1 não promove nada —
  sem push, sem merge em dev/main, sem promote-main — e o DONE com a matriz foi entregue ao
  regente (por SendMessage, ou commitado como fallback se a sessão MAESTRO seguir fora de
  alcance).

## Requirement coverage
- FR1: **presente** — 25 fichas em `pesquisa/`, cada uma com URL, data da visita, o que foi aberto
  de verdade (docs, repositório, demo, execução local) e a tabela fixa de 26 funcionalidades.
- FR2: **presente** — `pesquisa/plataformas.md` consolida as 25 plataformas (27 colunas de
  cabeçalho, 26 linhas de dados, 650 células), fechada por acréscimo.
- FR3: **presente** — toda célula se apoia na ficha da coluna; célula sem fonte ficou `—` (as 21
  em branco do Worker03 foram convertidas na matriz); nenhuma célula sem fonte virou "sim"
  (amostragem dirigida no fechamento).
- FR4: **presente** — `andamento.md` atualizado a cada DONE (quatro linhas da rodada 1 em
  **entregue** + histórico datado).

## Pending gate
- dev -> main promotion awaits human approval.

## Evidência da consolidação (073-T1-consolidacao, 25/10)

Worker06, contexto próprio. `pesquisa/plataformas.md` foi fechada **por acréscimo**, como a seção
"Como acrescentar uma plataforma" previu: as 13 colunas que faltavam (4 do Worker03 + 9 do
Worker05) entraram depois das 12 do Worker06. Nenhuma linha das fichas alheias foi reescrita.

### Contagem conferida

| O que | Esperado | Medido | Como foi medido |
|---|---|---|---|
| Colunas da matriz | 2 + 25 = 27 | **27** | cabeçalho da tabela, contado por script sobre o arquivo |
| Linhas de funcionalidade | 26 | **26** | 26 linhas de dados; **0** com contagem de células diferente de 27 |
| Células da matriz | 25 × 26 = 650 | **650** | 26 linhas × 25 colunas de plataforma |
| Linhas das 13 fichas novas | 13 × 26 = 338 | **338** | contagem própria por arquivo: **317 com veredito explícito + 21 células em branco** |
| Fichas consolidadas | 25 | **25** | 12 + 4 + 9, todas com 26 linhas |

Medição própria das 13 fichas novas (uma linha por arquivo): `helicone.md` **17**,
`openai-platform.md` **22**, `portkey.md` **20**, `litellm.md` **24** — as quatro do Worker03 somam
83 = 4×26 − 21 células em branco — e **26** para cada uma das nove do Worker05. Total com veredito:
**317**; 317 + 21 = **338** = 13 × 26.

### Células sorteadas e conferidas contra a ficha

| Célula na matriz | Ficha (caminho:linha) | O que a ficha diz |
|---|---|---|
| Langfuse × auditoria = `sim` | `pesquisa/langfuse.md:47` | "auditoria → sim — *audit logs* listados entre os controles" |
| Portkey × mensagem entre agentes = `não` | `pesquisa/portkey.md:68` | "mensagem entre agentes → não — nada sobre mensagem entre agentes (nem o termo A2A aparece)" |
| LiteLLM × colisão de nomes = `—` | `pesquisa/litellm.md:119` | célula **em branco**: "colisão de nomes → (vazio) — `a2a_agent_permissions` fixa o roteamento por `agent_id`, mas nenhuma página aberta trata colisão" |
| LiteLLM × protocolos (A2A; MCP) = `sim` | `pesquisa/litellm.md:115` | "Protocolos (A2A; MCP) → sim — `agent-card.json`, `protocolVersion` 0.3/1.0, e MCP" |

As quatro conferem — inclusive a única conversão deliberada: célula **em branco** na ficha virou
`—` na matriz, porque é o que a legenda manda e porque branco não é "sim" (FR3).

### Achado declarado (não corrigido por conta própria)

As 13 fichas novas **não usam `—`**: o Worker03 deixa a célula em branco (21 células) e o Worker05
escreve `não` para "nada achei". Nas colunas do Worker05, `não` significa amiúde **"não
encontrei"**, não "a fonte afirma que não existe" — é mais fraco que o `não` da legenda. O FR3 não
é violado (nenhuma célula sem fonte virou "sim"), mas a **força** do veredito difere entre as duas
gerações de ficha. Normalizar é decisão do dono da rodada; a nota está repetida em
`plataformas.md`, para quem ler a matriz sem ler este relatório.

### Decisão do Gerente (25/10) — notação ratificada, normalização deferida

O tratamento do consolidador está **ratificado**: célula em branco vira `—` (é o que a legenda
manda), `não` é transcrito como a ficha escreveu, e a divergência fica declarada na legenda da
matriz. O FR3 está preservado — nenhuma célula sem fonte virou "sim" — e a nota avisa o leitor
sobre a força do veredito. **Normalizar** (reclassificar o `não` do Worker05 entre "ausência
afirmada pela fonte" e "não encontrei", célula a célula, relendo as 9 fichas) fica como
**tarefa de preâmbulo da rodada 2**: é no confronto com o Maestro que a força do veredito passa
a decidir, e reclassificar agora seria gastar ficha antes de saber se a rodada 2 precisa da
distinção.

## Reverificação em contexto fresco (073-T1-revisao, 25/10)

Worker03, contexto próprio — a consolidação foi do Worker06, então quem verifica não é quem
consolidou (Teorema 2). Objeto: `pesquisa/plataformas.md` na revisão `397f302`. **Nada foi
corrigido**: o achado bloqueante abaixo está **reportado**, não alterado — corrigir é decisão do
dono da rodada. A amostragem das 7 células foi escolhida pelo Gerente (não por quem revisa), para
não ser auto-selecionada.

### 1. Amostragem dirigida — 7 células contra a ficha da coluna

| Célula na matriz (linha) | Veredito | Ficha (caminho:linha) | O que a ficha diz | Confere? |
|---|---|---|---|---|
| Dify × políticas allow/deny/ask (`plataformas.md:63`, 22ª célula) | `não` | `dify.md:32` | "políticas allow/deny/ask → não — não descrito nas fontes vistas" | **confere** |
| CrewAI AMP × protocolos (A2A, MCP) (`:80`, 20ª) | `sim` | `crewai-amp.md:64` | "sim — suporte a MCP e A2A listado na página do repositório" | **confere** |
| LangSmith/LG × aprovação humana (`:64`, 19ª) | `sim` | `langsmith-langgraph.md:32` | "sim — human-in-the-loop: inspecionar e modificar o estado (interrupts)" | **confere** |
| n8n × pausar (`:60`, 7ª) | `parcial` | `n8n.md:28` | "parcial — 'Unpublishing removes the workflow from production'; não há 'pausa' com retomada de estado" | **confere** (inclusive o motivo) |
| Windmill × filas e workers (`:76`, 12ª) | `sim` | `windmill.md:43` | "sim — 'Workers pull jobs from the queue'; priority 1–100; 'Queues are named via tags'" | **confere** |
| Temporal Web UI × caixa de entrada (`:81`, 1ª) | `—` | `temporal-web-ui.md:105` | "caixa de entrada → —" (sem fonte) | **confere** |
| Helicone × auditoria (`:70`, 16ª) | `não` | `helicone.md:51` | "não — nenhuma página de auditoria em 147 de docs (o termo não aparece no índice)" | **confere** (checagem inversa: a ficha é do Worker03; confirma a transcrição do Worker06) |

As 7 conferem — transcrição fiel, nenhuma célula "inventada". Duas ressalvas de **força** (não de
fidelidade), que a ficha já declara sozinha:

- **Dify × políticas = `não`** e **Helicone × auditoria = `não`** são `não` de *"não achei"*, não de
  *"a fonte afirma que não existe"* — exatamente a divergência de notação já declarada em
  `plataformas.md:46–53`. Mais fraco que o `não` da legenda, mas declarado (não é célula nua).
- **CrewAI AMP × protocolos = `sim`** apoia-se na **página do repositório** (o elo mais fraco das
  sete fontes), não em documentação de produto. Reverifiquei a página hoje (`github.com/crewAIInc/crewAI`):
  "Key Features" traz "MCP/A2A support" (texto literal); o resto da página menciona MCP, mas **não
  expande A2A nem MCP**. O `sim` se sustenta, com essa ressalva de qualidade de fonte.

### 2. Recontagem independente (script próprio, fora do repositório)

Contagem própria sobre o arquivo (parse da tabela **só no bloco da matriz**, entre o cabeçalho
`| Grupo |` e a próxima seção `## ` — sem isto, a tabela-resumo "Por grupo" entra como linha de
dados e infla tudo):

| O que | Declarado | Medido | Resultado |
|---|---|---|---|
| Colunas do cabeçalho | 2 + 25 = 27 | **27** | ✅ |
| Linhas de dados (funcionalidades) | 26 | **26** | ✅ |
| Linhas com contagem de células ≠ 27 | 0 | **0** | ✅ |
| Células de dados | 25 × 26 = 650 | **650** | ✅ |
| `sim` por grupo | CONTROLE 30 · ADMINISTRAÇÃO 76 · GERENCIAMENTO 44 · INTERCOMUNICAÇÃO 20 | **30 · 76 · 47 · 21** | ⚠️ **2 de 4 não conferem** |

Distribuição medida dos 650 símbolos: `sim` 174 · `parcial` 221 · `não` 156 · `—` 99.

### 3. Achado bloqueante — as tabelas de leitura **subnotificam** o `sim`

O veredito por célula está fiel (as 7 amostras conferem), mas as duas **tabelas de leitura** da
matriz contam a menos. Medido por funcionalidade contra a tabela "Por funcionalidade":

| Funcionalidade | Declarado (linha) | Medido | Onde o `sim` está na matriz |
|---|---|---|---|
| alertas | 6 (`plataformas.md:116`) | **8** | `plataformas.md:78` (Prefect, Dagster, Windmill, LiteLLM, OpenAI Platform, Helicone, Langfuse, LangSmith/LG) |
| mensagem entre agentes | 7 (`:114`) | **8** | `plataformas.md:79` (Temporal, Copilot Studio, Claude Code, Maestri, AgentCore, LiteLLM, CrewAI AMP, AutoGen Studio) |
| consumo por agente/sessão/modelo | 2 (`:120`) | **3** | `plataformas.md:74` (Copilot Studio, Claude Code, **LiteLLM**) |
| **total das 26 linhas** | **170** | **174** | as outras 23 linhas conferem |

Consequência nos totais por grupo (`plataformas.md:100–103`): **GERENCIAMENTO 44 → 47** (`sim`
real sobre 200 = 23,5%, não 22%) e **INTERCOMUNICAÇÃO 20 → 21** (14% de 150, não 13%). CONTROLE
(30) e ADMINISTRAÇÃO (76) **conferem**. O texto da leitura — "GERENCIAMENTO: metade é
observabilidade", "INTERCOMUNICAÇÃO: o grupo mais fraco" — continua **verdadeiro**; o número é que
está subestimado.

Achados secundários, na mesma família (declarados, não corrigidos):

- **`plataformas.md:120`** — o parêntese "consumo por agente só em **Copilot Studio** e **Claude
  Code**" **contradiz a própria matriz**: a célula da LiteLLM em `plataformas.md:74` é `sim`.
  Ou o parêntese esqueceu a LiteLLM, ou a linha da LiteLLM está `sim` indevidamente — a decisão é
  do dono da rodada.
- **`plataformas.md:47–49`** — a nota de divergência diz que só as colunas do Worker05 escrevem
  `não` para "nada achei". Não é só o Worker05: a coluna do **próprio Worker03** (`helicone.md`)
  também usa esse `não` — p.ex. auditoria (`helicone.md:51`) e caixa de entrada têm fonte
  "nenhuma página aberta". A ressalva "`não` = não encontrei" vale para **≥ 2 células** da coluna
  do Worker03 também.

### 4. Passagem de segurança (TAIL:security da rodada)

Varredura própria sobre `specs/073-area-administrativa/pesquisa/` — **28 arquivos** (26 `.md` + 2
PNG), 14 padrões (chaves `sk-*`/`sk-proj`/`sk-live`/`sk_test`, tokens GitHub/Google/AWS/Slack,
bloco de chave privada, JWT, `bearer` literal, `password|senha|secret|api_key|token: valor`,
e-mail, CPF, CNPJ, telefone `+55`), com os PNG lidos também como bytes:

- **0 achados fora da lista declarada.** Houve **1** casamento de padrão — `sk-local-demo-073-nao-e-segredo`
  em `litellm.md:18` — e está **declarado na própria ficha como placeholder local descartável, não-segredo**.
  É o único; nenhum outro segredo, token, e-mail, CPF/CNPJ, JWT ou telefone em nenhuma ficha.
- **Capturas da LiteLLM** (`img/litellm-01-ui-login.png`, `img/litellm-02-ui-login-sem-banco.png`):
  abertas e **olhadas**, não só varridas — mostram apenas a tela de login do Admin UI (campos
  vazios) e a recusa de login sem banco. **Não expõem** usuário, senha, token nem dado pessoal; a
  varredura de bytes também não acha padrão algum nelas.
- **Conta externa**: nenhuma criada. As 9 fichas do Worker05 trazem "Conta criada? **não**"
  explícito; as do Worker03/Worker06 declaram em prosa ("Não rodou local", "nada foi executado").
  A **única** execução real da rodada é a da LiteLLM (proxy + Admin UI **local**, chave descartável,
  sem conta externa) — declarada na ficha, não presumida.

**Veredito da varredura: limpo** — 0 achados não-declarados, e o único casamento é um placeholder
que a ficha nomeia como tal.

### 5. Resumo da revisão

- **7/7 células conferem** na transcrição (1 delas reverificada contra a fonte na web hoje).
- **Contagens estruturais conferem** (27 colunas, 26 linhas, 0 linhas malformadas, 650 células).
- **1 achado bloqueante**: as tabelas de leitura subnotificam o `sim` em 4 (3 linhas + o total);
  `plataformas.md:120` contradiz a matriz sobre a LiteLLM. **Reportado, não corrigido.**
- **TAIL:security**: limpo (0 achados não-declarados).
- Scripts de medição **fora do repositório** (`%TEMP%\rev073.py`, `%TEMP%\rev073b.py`) — nada de
  ferramenta nova entra no projeto por causa desta revisão.

## Preâmbulo da rodada 2 (073-T2-preambulo, 25/10) — normalização e correções da amostragem

Worker06, contexto próprio. Duas operações, ambas **na ficha e na coluna da matriz** (a ficha é a
fonte de verdade; a matriz é a projeção).

**1. Normalização da força do veredito (`não` × `—`).** As 13 fichas do Worker03/Worker05 usavam
`não` com dois sentidos. Reclassificação **célula a célula, relendo cada ficha**: `não` de "não
achei / nada sobre / não aparece / não descrito / *not documented*" → `—`; `não` **afirmado** pela
fonte ficou `não`. Resultado: **143 células** `não → —` (conferidas por script) e **13 `não`
mantidos** — Helicone 3 (subir, lista de vivos, mensagem) · Dify 1 · Flowise 1 · Arize Phoenix 3 ·
Comet Opik 3 · Kiro Crew 2 —, todas com a ausência **afirmada** pela fonte. As 21 células em branco
do Worker03 já eram `—` na matriz e continuam. **Nenhuma célula mudou de `—` para `sim`** (FR3
intocado). A regra entrou na legenda da matriz; a nota de divergência passou a "resolvida em 25/10,
rodada 2".

**2. Correções da amostragem** (crítico em contexto fresco, veredito `SOUND_WITH_FIXES`): duas
células da coluna **Temporal Web UI** desceram de `sim` para `parcial` — *lista de agentes vivos com
estado* e *tarefa aberta* (a aba Workers lista *workers* em *polling*, não agentes; a tabela
Workflows lista execuções, não a tarefa aberta de um agente) —, com a justificativa gravada na
própria ficha (`pesquisa/temporal-web-ui.md`). Textos corrigidos na leitura: Maestri **6 → 5**
células `—` em CONTROLE; INTERCOMUNICAÇÃO **13% → 14%** (21/150); tabelas de leitura recontadas.

**Distribuição pós-normalização (medida por script sobre a matriz, 25/10):** `sim` **172** ·
`parcial` **223** · `não` **13** · `—` **242** = **650**. Por grupo (`sim`): CONTROLE **30**/150 ·
ADMINISTRAÇÃO **76**/150 · GERENCIAMENTO **45**/200 (22,5%) · INTERCOMUNICAÇÃO **21**/150 (14%).

**Conferência texto × matriz (PASS):** 27 colunas de cabeçalho, 26 linhas de dados, **0** linhas com
contagem de células ≠ 27, 650 células; toda contagem das tabelas de leitura bate com a matriz.
Script de medição fora do repositório (`%TEMP%\wf073_check.py`). Nada da evidência da rodada 1 foi
reescrito — normalização e correções entraram **por acréscimo**.

## Revisão em contexto fresco do confronto (073-T2-revisao-confronto, 25/10)

Worker05, contexto próprio — **não escrevi o confronto** (foi o Worker03). Declaro, por
transparência, que sou **autor de um dos insumos** (o inventário): a amostragem abaixo confere o
confronto contra a **matriz** e contra **fontes externas** (o incidente do 066), não contra juízo
próprio. Objeto: `confronto/confronto-decisao.md` (commit `eb40d89`), contra
`pesquisa/plataformas.md` (pós-preâmbulo, normalizada) e `confronto/inventario-maestro.md`.
Amostragem dirigida pelo Gerente (não auto-selecionada). **Nada foi corrigido** — os achados estão
**reportados**; corrigir é decisão do dono da rodada.

### 1. Amostragem dirigida — 6 linhas

| # | Linha (decisão) | Verificação pedida | Confere? |
|---|---|---|---|
| 1 | caixa de entrada = **ENTRA** | fonte = requisito do método (`fila_outbox.py:140`); melhor referência citada = Maestri canvas `parcial`; nenhuma das 25 colunas `sim` | **confere** — `plataformas.md:88` não tem `sim`; ressalva: a Maestri **empata** com o Claude Code (ambas `parcial`) — ver Achado 2 |
| 2 | colisão de nomes = **ENTRA** | incidente cita `specs/066-painel-de-regencia/qa-report.md:35`; Kiro Crew e Windmill `sim` | **confere** — `:35` diz exatamente o afirmado ("'Gerente' … 24/10 … 16 h … endereçar por ref … debt 2"); `plataformas.md:91` Kiro Crew = `sim`, Windmill = `sim` |
| 3 | pausar = **DEPOIS** | respeita a força do veredito (`não encontrado`, piso); gatilho coerente com o ENTRA de limite de orçamento | **confere** — o inventário marca `pausar` como `não tem (não encontrado)`; limites é ENTRA com lacuna "limite executável", e o gatilho de pausar é esse teto |
| 4 | RBAC = **NÃO PRECISA** (fora do método) | justificativa (autorização fora do modelo, Princípio III) contra `principles.md:37` e o glossário | **confere** — `principles.md:37` "Declarative policy `allow / deny / ask`; authorization lives outside the model."; `glossary.md:12` ABAC / `:13` RBAC |
| 5 | consumo por agente = **ENTRA** | Copilot Studio `sim` na linha; estado `parcial` confere com o inventário | **confere** — `plataformas.md:81` Copilot Studio = `sim`; o inventário marca `parcial` (por sessão sim, por agente não) |
| 6 | subir/derrubar = **ENTRA** | fonte dupla (método + plataforma), sem célula `—` | **confere** — `specs/072-…/spec.md:229` "Controle de PID — subir/derrubar sessão (risco alto; spec própria)"; `multi-session.py:140` (o "subir"); `plataformas.md:66` Claude Code = `sim` |

**6/6 conferem** (a 1ª com a ressalva de empate, Achado 2).

### 2. Recontagem das 26 decisões, por grupo (× §Totais)

| Grupo | ENTRA | NÃO PRECISA | DEPOIS | Declarado no arquivo | Confere? |
|---|---|---|---|---|---|
| CONTROLE (6) | 3 | 1 | 2 | "3 ENTRA · 1 NÃO PRECISA · 2 DEPOIS" | ✅ |
| ADMINISTRAÇÃO (6) | 1 | 4 | 1 | "1 ENTRA de 6" | ✅ |
| GERENCIAMENTO (8) | 3 | 3 | 2 | "3 ENTRA de 8" | ✅ |
| INTERCOMUNICAÇÃO (6) | 6 | 0 | 0 | "6 ENTRA de 6" | ✅ |
| **Total (26)** | **13** | **8** | **5** | **13 · 8 · 5** | ✅ |

Os nomes listados na tabela §Totais batem, um a um, com a decisão de cada linha da matriz de decisão.

### 3. Regra 2 — nenhum `ENTRA` se apoia em célula `—`

Conferência dos 13 `ENTRA` contra a coluna citada: subir→Claude Code `sim` (`:66`) · limites→OpenAI
Platform `sim` (`:69`) · políticas→Agent 365 `sim` (`:70`) · skills→LiteLLM `sim` (`:74`) · lista de
vivos→Claude Code `sim` (`:78`) · tarefa aberta→Claude Code `sim` (`:79`) · consumo→Copilot Studio
`sim` (`:81`) · mensagem→CrewAI AMP `sim` (`:86`) · protocolos→LiteLLM `sim` (`:87`) · caixa de
entrada→método + Maestri `parcial` (`:88`) · roteamento→Windmill `sim` (`:89`) · livro→método +
Maestri `parcial` (`:90`) · colisão→Kiro Crew `sim` (`:91`). **Nenhum `—`.** **PASS.**

### 4. Achado — Princípio VIII (Iron Law): quatro siglas com a 1ª ocorrência nua

**RBAC** (`:49`), **RACI** (`:49`), **A2A** (`:63`) e **MCP** (`:73`) aparecem **sem expansão** na
primeira ocorrência do documento; a expansão só existe na lista final de siglas (`:172-174`). A
Iron Law do Princípio VIII exige a expansão **na primeira ocorrência**, e a contagem reinicia a cada
documento — a lista final não sana a primeira. **Violação.** Correção editorial trivial (antecipar a
expansão para `:49`/`:63`/`:73`). **Reportado, não corrigido.** (ADR `:15`, YAGNI `:21` e OPA `:89`
estão corretos — expandidos na 1ª ocorrência.)

### 5. Achado (secundário) — "melhor referência" não é única pela matriz

Nas linhas **caixa de entrada** (`:74`) e **livro de mensagens** (`:76`), o rótulo "melhor" (Maestri
canvas) **não se lê da matriz**: caixa de entrada é **empate** Maestri × Claude Code (ambas `parcial`,
`plataformas.md:88`); livro de mensagens é **empate de seis** (`Maestri, AgentCore, Windmill, LiteLLM,
OpenAI Platform, AutoGen Studio`, todas `parcial`, `:90`). A escolha da Maestri canvas é **defensável**
pela nota da própria plataforma — a única cuja intercomunicação é por PTY, "com caixa de entrada e
livro de mensagens parciais" (`plataformas.md:164-166`) —, mas o rótulo deveria ser "empatada (melhor
por juízo)", não fato da matriz. **Não bloqueante**: a base do `ENTRA` é o requisito do método e a
célula citada **não** é `—` (a Regra 2 segue satisfeita).

### 6. Resumo da revisão

- **6/6** amostras conferem (a 1ª com a ressalva do empate).
- Recontagem **13/8/5** confere; por grupo, confere; §Totais bate com as linhas.
- **Regra 2: PASS** — nenhum `ENTRA` sobre célula `—`.
- **1 achado bloqueante (Princípio VIII)**: RBAC/RACI/A2A/MCP nuas na 1ª ocorrência; e **1
  secundário** (rótulo "melhor"). Ambos **reportados, não corrigidos**.
- **Limites**: revisão read-only; nada construído; nada de ferramenta nova entrou no repositório.
