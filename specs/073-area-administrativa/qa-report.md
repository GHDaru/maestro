# QA report 073 — Área administrativa do Maestro (rodadas 1–2)

- **Date**: 2026-10-24 (fichas) · 2026-10-25 (consolidação, revisão, fechamento e rodada 2
  inteira) · **Lane**: plena · **Verdict**: approved (rodada 1) — 7/7 células conferem, contagens
  estruturais conferem, 1 achado bloqueante corrigido e reconferido por script; segurança limpa ·
  **rodada 2 fechada** — preâmbulo verificado por script (PASS), inventário com 6 citações
  amostradas conferindo, confronto com contagem machine-checkada (13/8/5) e revisão fresca 6/6
  com o bloqueante de Princípio VIII corrigido e verificado por script (PASS); mapa de contextos
  entregue

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
| Matriz pós-preâmbulo × tabelas de leitura (script fora do repo) | todo número confere | **PASS** — sim 172 · parcial 223 · não 13 · — 242; grupos CONTROLE 30 · ADMINISTRAÇÃO 76 · GERENCIAMENTO 45 · INTERCOMUNICAÇÃO 21 (rodada 2) |
| Decisões do confronto (script fora do repo) | 26 linhas; ENTRA 13 · NÃO PRECISA 8 · DEPOIS 5 | **PASS** — 26 linhas, contagem exata; por grupo confere com §Totais (rodada 2) |
| Siglas na 1ª ocorrência no confronto (script fora do repo) | toda 1ª ocorrência expandida | **PASS** — RBAC/RACI/A2A/MCP/ADR/YAGNI/OPA/DDD/ABAC (pós-correção; o script achou o ABAC que a revisão não viu) |
| `scripts/check-conformance.sh 073` | verde nos dois modos | **verde, exit 0** — normal e `TICKED_ONLY=1` (fechamento da rodada 2, 25/10: Constitution Check 8/8, 5 artefatos com razão, domínio declarado, TAIL com evidência; TAIL:gate segue sendo o "segue" do regente para a rodada 3) |

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

## Rodada 3 (073-T3-seguranca, 26/10) — segurança documental e conformance 073

Worker06, contexto próprio. Objeto: `specs/073-area-administrativa/` — foco em `prototipo/`
(11 telas + 2 fixtures + o verificador) e `confronto/` (3 arquivos). **Por acréscimo**: nada da
evidência das rodadas 1/2 foi reescrito.

### 1. Varredura — nenhum achado

| Classe | Padrões procurados | Resultado |
|---|---|---|
| Segredo | chave `sk-*`/`sk_live`/`sk_test`, `api_key`, `secret`, `senha`, `password`, `bearer`, *connection string*, `AKIA…`, `ghp_…`, bloco de chave privada, JWT (*JSON Web Token*, `eyJ…`) | **0** — os únicos casamentos são **falsos positivos**: `sk-l` dentro de "ta**sk-l**edger" (o `task-ledger.md` citado nas telas) e `senha` dentro de "de**senha**dos" (`prototipo/README.md:4`). Confirmado por `grep -o`: o texto casado é literalmente `sk-l`/`senha`, não um segredo. |
| Dado pessoal | e-mail, telefone `+55`, CPF, CNPJ, caminho de usuário | **0** e-mails, 0 telefone, 0 CPF/CNPJ. O único caminho de usuário é o **namespace público do repositório** `GHDaru/maestro` (`confronto/inventario-maestro.md:9`) — não é dado de terceiro. |
| Nome real de sessão/agente | `Worker0*`, `Gerente`, `Regente`, `Office`, nomes próprios | **0 sem marcador** — todo valor que parece real carrega `(exemplo)` **e** `data-exemplo="true"` (verificado tela a tela). Nomes de **papel** do método (Worker01–05, Gerente) não são pessoas. |
| URL externa | `http(s)://…`, com e sem *query string* | **só documentação/produto público** — `docs.litellm.ai`, `code.claude.com/docs`, `docs.temporal.io`, `windmill.dev`, `kiro.dev`, `themaestri.app`, `learn.microsoft.com`, `arize.com`… A única com *query string* é o endpoint público de consulta da doc do n8n (`pesquisa/n8n.md:5`), sem token nem credencial. Nada vaza acesso privado. |

**Declarado, não achado:** `Darú` aparece em `spec.md:44` e `plan.md:18` (prosa: "a página de
progresso viva do Darú") — é o **dono do repositório**, nome já presente em todo o repo; não é dado
de terceiro nem dado de tela.

**Achados: 0.** Pela taxonomia do Princípio III (*read → … → irreversível → bloqueada*), nada a
classificar.

### 2. O protótipo passa na própria fitness function

```
$ python specs/073-area-administrativa/prototipo/verifica-prototipo.py
-- verifica-prototipo: 11 screen(s), 0 finding(s)
```

11 telas, 0 achados, exit 0 — verde **além** do retrato de 25/10, que registrava 45 achados
pendentes de `attempt=2`.

### 3. Conformance 073 — verde nos dois modos

**Modo normal** (`bash scripts/check-conformance.sh 073`) — exit 0:

```text
── Conformance: did the method survive into the artifacts? ──
   (floor: cycle 42; older cycles carry declared debt — see the roadmap)
• 070-conferidor-ordem-veredito
    · imported evidence (00-chamado.md + G*-*.md, no tasks.md): a Hindiana chamado, not a Maestro cycle — not charged (ADR 0024)
• 073-area-administrativa
    ✓ Constitution Check complete (8/8)
    ✓ acceptance criteria located and stated without checkboxes
    ✓ all 5 conditional artifacts declared with a reason
    ✓ domain model declared (aggregate, invariants, glossary, ports) with a reason
    ✓ TAIL:review evidence: Worker03, contexto fresco (não consolidou; amostragem esc
    ✓ TAIL:security evidence: Worker03, varredura sobre `pesquisa/` (28 arquivos, 14 pad
    ✓ TAIL:gate evidence: o gate humano da rodada 1 é o **"segue" do regente para a
    · TAIL:mutation not applicable — rodada documental — nenhum gate executável criado ou alte
──
cycles checked: 2
✓ every cycle checked declares its artifacts and carries the closing tail with evidence.
```

**Modo `TICKED_ONLY=1`** — saída **idêntica**, exit 0.

> Nota da máquina: nesta worktree a chamada do conformance 073 leva ~4–6 min (msys, *fork* por
> arquivo). **Não** foi preciso extrair `check-links.sh`/`check-boundary.sh` — o conformance 073
> não os invoca a ponto de pendurar; a lentidão é do próprio `check-conformance.sh` sob msys.
> Saídas coladas acima, como pedido.

### Veredito

**Limpo.** 0 achados de segurança (segredo, dado pessoal, nome não marcado, URL vazada); protótipo
verde na própria fitness function; conformance 073 verde nos dois modos. **Nada corrigido — nada
havia a corrigir.**

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

## Fechamento da rodada 2 (Gerente, 25/10)

- **Correção do bloqueante da revisão** (commit próprio, "ciclo 073: correcoes da revisao fresca do
  confronto"): RBAC, RACI, A2A e MCP expandidos na primeira ocorrência (`:49`, `:63`, `:73`) e o
  secundário rotulado (empates da "melhor referência" em caixa de entrada e livro de mensagens).
  **Verificado por script** (`%TEMP%\verifica-viii.py`, fora do repo): toda primeira ocorrência de
  sigla expandida — o script achou também um **ABAC** nu em `:107` que a revisão não viu, corrigido
  no mesmo commit. **PASS.** Recontagem das decisões re-executada pós-correção: 26 linhas,
  ENTRA 13 · NÃO PRECISA 8 · DEPOIS 5 — intacta.
- **Mapa de contextos** (Worker02, `e90e8b9`): cinco contextos com raiz e invariantes, diagrama
  Mermaid, sete relacionamentos tipados com motivo, core domain = Chamados e Gates (leitura
  alternativa declarada), linguagem ubíqua por contexto com os 12 termos propostos marcados,
  cinco colisões de nome reais. Divergências declaradas pelo autor (painel é projeção; sexto
  contexto recusado por YAGNI; evidência por arquivo+símbolo, não arquivo:linha).
- **Segurança da rodada 2**: n/a estendida — rodada documental sem navegação nova (mandato do
  regente), sem código, sem contas externas, sem dados pessoais; os insumos são arquivos do próprio
  repositório já varridos na rodada 1.

## Rodada 3 — fitness function do protótipo (Gerente, 25/10)

**`prototipo/verifica-prototipo.py`** (commit `fa4ee3e`) — o gate executável dos wireframes, com as
quatro regras do mandato:

1. **elemento interativo sem `data-fonte`** — todo `button`/`a`/`input`/`select`/`textarea` precisa
   do atributo dizendo de onde a ideia veio;
2. **rótulo fora do glossário** — allowlist extraída de `docs/governance/glossary.md` (74 termos,
   primeira coluna em negrito) **+ os 12 ratificados** embutidos no script; casa com **word
   boundary**, não substring;
3. **número sem a marca "exemplo"** — conferido em **todo nó de texto** (não só rótulos); aceita a
   marca como atributo `data-exemplo` em qualquer ancestral ou a palavra "exemplo" no próprio texto;
4. **colisão sem qualificador** (condição da ratificação) — "fila" exige `decisões`/`outbox` e
   "portão" exige `chamado`/`regente` no mesmo rótulo.

**Smoke test** (telas sintéticas, commitadas como fixtures do script em
`prototipo/fixtures/tela-bom.html` e `prototipo/fixtures/tela-ruim.html` — subdiretório não é
varrido como tela; a ruim mantém os 5 achados de propósito e é o corpus da mutação do W02): a tela
ruim acusou **5 achados** (rótulo fora do glossário, "fila"
sem qualificador, `button` sem `data-fonte`, número sem "exemplo", e o `<th>` "Fluxo de caixa
operacional"); a tela boa, **0 achados**. O smoke test **achou um falso-negativo real**: o termo
"RACI" casava como substring de "ope**raci**onal" — corrigido para word boundary antes do commit.
Sem telas reais o script **falha por design** ("no screens found", exit 1) — a rodada verde sobre as
13 telas e a saída colada aqui acontecem no **T3-fechamento**; a mutação do Worker02 quebra este
script de propósito (TAIL:mutation da rodada).

### Primeira rodada sobre telas reais (v2 `b30fd8f` → v3 `da85def`, Gerente, 25/10)

O contrato de marcação foi fechado DEPOIS da primeira rodada real (4 telas do W03): v2 validou
`data-rotulo` contra o glossário e isentou contexto de citação (`data-fonte`/`data-referencia`) e
acrônimo com dígito (A2A, F1); v3 declarou o vocabulário de **moldura** do W04 (tipo, consultar,
regra, efeito…) como stopwords — palavra de domínio NÃO entra nessa lista, leva `data-rotulo`.
Rodada v3 sobre as **7 telas integradas** (4 Mensageria `566bca5` + 3 Administração `00c1ae9`):

```text
-- verifica-prototipo: 7 screen(s), 45 finding(s)   [exit 1]
```

**45 achados, todos em duas classes** — nenhum de `data-fonte` ausente, nenhum de `data-rotulo`
fora do glossário, nenhum de colisão (fila/portão sempre qualificados nas telas):
1. **citação sem atributo** (40: W03 22 · W04 18) — dígito de referência (§, ADR, file:linha,
   "25 plataformas", "ciclo 073") em texto visível fora de `data-fonte`/`data-referencia`;
2. **rótulo de domínio sem `data-rotulo`** (5, W04) — `Teto`/`Consumo`/`Restante`/`Efeito ao
   estourar` (→ limite de orçamento / consumo por agente) e o h1 de políticas (→ **OPA**, o termo
   reusado do glossário para allow/deny/ask, `confronto-decisao.md:159-161`).

**Correções attempt=2 despachadas** ao W03 (22) e ao W04 (23) com o contrato e a lista exata;
verde esperado antes do fechamento. Com o glossário do W01 integrado (`853a1d5`): allowlist
74→86 e a rodada re-executada dá **45 = 45** (os achados são todos da classe citação/rótulo,
independentes do glossário — medido também pelo W01: 22=22 nas telas dele).

## Rodada 3 — telas da Administração (Worker04, 25/10)

**Escopo:** `T3-telas-administracao` — três wireframes estáticos em
`specs/073-area-administrativa/prototipo/`, as três `ENTRA` que o mapa §6.5 põe na Administração:

| Arquivo | ENTRA (`confronto-decisao.md`) | Nome na linguagem ubíqua | Juiz(es) da rodada 4 |
|---|---|---|---|
| `administracao-catalogo.html` | cadastro de skills/ferramentas/modelos | catálogo de skills/ferramentas/modelos | Administração/Gerenciamento |
| `administracao-politicas.html` | políticas allow/deny/ask | política declarativa (allow/deny/ask) | Controle · Administração/Gerenciamento |
| `administracao-orcamento.html` | limites de orçamento e de taxa | limite de orçamento | Controle |

Cadastro de agentes e papéis **não** é tela nova: aparece como **coluna de contexto somente-leitura**
no catálogo, com `data-fonte` em `docs/agents/README.md` + `scripts/check-agents.sh` — sem
funcionalidade nova, conforme o mandato do regente.

### Formato entregue

- um arquivo HTML **estático** por tela; zero `<script>`, zero recurso externo (`http`), sem servidor;
- CSS mínimo em cinza, "caixas e rótulos" (tokens em `:root`, ~30 linhas, repetido por arquivo);
- **todo** elemento de bloco e **todo** controle com `data-fonte`, que nomeia a plataforma (ficha em
  `pesquisa/`) ou o requisito do método (princípio, ADR, ux-design);
- **nenhum número inventado**: ilustrativo → `exemplo`; vivo → `—` com `motivo`; real → selo
  `declarado` (método) ou `referência` (plataforma) com a fonte.

### Auto-checagem (mesmas regras do `T3-fitness` do Gerente)

Script `%TEMP%\w04check\fit073.py` (fora do repositório), nove regras — R1 interativo com
`data-fonte` · R2 `.metrica` com `data-fonte` (`F1`) · R3 travessão-valor com `motivo` (`F8`) · R4
número sem marca `exemplo` · R5 rótulo fora do glossário/ratificados/moldura · R6 termo da lista
"Evitar" (`ux-design 066` §5) · R7 sigla expandida na 1ª ocorrência (Princípio VIII) · R8
script/externo · R9 link relativo quebrado.

Saída: **`RESULTADO: PASS — 3 arquivos, todas as regras verdes`** (R1–R9 `medido=0 esperado=0` nos
três arquivos). Vocabulário carregado do próprio repositório: 74 termos do glossário + 12 propostos
ratificados.

### Mutação da auto-checagem (prova de que não é vazia)

`%TEMP%\w04check\mut073.py` — quebra **uma** regra de cada vez numa cópia temporária e roda o MESMO
`fit073.py` sobre a cópia, exigindo a acusação da regra correspondente. Saída:
**`RESULTADO: PASS — 9 mutações, cada uma acusada pela sua regra`** (9/9).

Um **ponto cego** apareceu e foi corrigido antes da entrega: a primeira versão do R5 aceitava o
rótulo "Motor de custódia de credenciais" porque o termo `Mod` casava como **substring** de
"motor". O R5 passou a exigir **fronteira de palavra** (`mod` não casa dentro de `motor`), mantendo
a segunda via (rótulo curto contido num termo) só para casos legítimos como "Skill" ⊂ "catálogo de
skills/ferramentas/modelos". Re-executado: PASS nos dois scripts.

### Interpretações declaradas

1. **"plataforma e URL da ficha em `pesquisa/`"** → o `data-fonte` nomeia a plataforma e o
   **caminho da ficha** em `pesquisa/`, que traz a URL externa dentro dela; o HTML não duplica a
   ficha nem o link externo.
2. **A regra de rótulo incide sobre nomes de objeto** (`<span class="rotulo">`, `<h3>`):
   glossário + 12 ratificados + linguagem ubíqua do mapa §6.5 (Agente, Skill, ferramenta, Projeto,
   Fronteira). Palavras de moldura de interface (Controle, Escopo, Estado, Consultar, Nome, Tipo…)
   são declaradas **como moldura** no rodapé de cada tela, não como vocabulário de domínio.
3. **`F1`, `F8`, `F9`** do `ux-design` 066 valem; **`F2`–`F7` e `F10`–`F12` são n/a** neste
   protótipo (supõem servidor e API) — declarado no rodapé de cada tela, não omitido.

### Limites

Nada fora de `specs/073-area-administrativa/prototipo/` foi escrito; sem push, sem merge, sem
código de produto, sem segredo; siglas expandidas na 1ª ocorrência (verificado pelo R7).

### Correção do gate `verifica-prototipo` (attempt=2, 25/10)

A fitness function do protótipo (`prototipo/verifica-prototipo.py`, v3) acusou **23 achados nas 3
telas** — nenhum era valor inventado; todos eram de **marcação**. As duas classes e a correção:

| Classe | Achados | Correção (só atributo) |
|---|---|---|
| dígito de citação fora de contexto de citação | 18 (6 por tela: a `p.migalha` "ciclo 073, rodada 3" e os 5 blocos de rodapé com `fonte: … §4 / §7`) | `data-referencia="true"` na `p.migalha` e no `<footer class="rodape">` — ancestral isenta os descendentes |
| rótulo de domínio sem `data-rotulo` | 5 | `data-rotulo` nos `<th>` do orçamento (Teto → `limite de orçamento`; Consumo → `consumo por agente`; Restante → `limite de orçamento`; Efeito ao estourar → `limite de orçamento`) e no `<h1>` da política (→ `OPA`) |

**Nenhum texto visível foi alterado** — só atributos. Os `class="exemplo"` com "exemplo:" no texto
já passavam pela regra do número (contrato §2) e ficaram como estavam.

Verificação re-executada:

- `python specs/073-area-administrativa/prototipo/verifica-prototipo.py` → total do protótipo
  **45 → 22 achados**: as 23 minhas zeradas (**0 achado em `administracao-*.html`**); os 22
  restantes são das 4 telas da Mensageria (W03), não destas telas.
- auto-checagem própria re-rodada **só nas 3 telas** (cópia em diretório temporário): `fit073.py`
  **PASS** (R1–R9 verdes) e `mut073.py` **PASS** (9/9 mutações acusadas) — os atributos novos não
  afrouxaram nenhuma regra própria.

Sincronização: a worktree foi para `853a1d5` (`git merge --ff-only`) apenas para trazer o script do
gate, que não existia na minha linha.

### Verde intermediário do Gerente — 7 telas, 0 achados (25/10)

Com as DUAS correções integradas (W03 `ccf574c` → `1354240`; W04 `7147f50` → `01b55f6`), o gate
re-executado na árvore integrada:

```text
-- verifica-prototipo: 7 screen(s), 0 finding(s)   [exit 0]
```

As 7 telas (4 Mensageria + 3 Administração) passam nas quatro regras. Faltam as telas do Workflow
(W05) e o README/navegação (W01); a rodada final sobre as 13, com a saída colada aqui, acontece no
T3-fechamento — e a mutação do W02 quebra este script de propósito antes disso.

## Rodada 3 — telas do Workflow de sessões (Worker05, 26/10)

**Escopo:** `T3-telas-workflow` (attempt=2, redespacho) — os quatro wireframes **estáticos** das
`ENTRA` que o mapa §6.3 põe no contexto **Workflow de sessões**, em
`specs/073-area-administrativa/prototipo/` (commit `365f59d`, citando "ciclo 073"; worktree
sincronizada em `c3137e2` com `git merge --ff-only`):

| Arquivo | ENTRA (`confronto-decisao.md`) | Nome na linguagem ubíqua | Juiz(es) da rodada 4 |
|---|---|---|---|
| `workflow-01-sessao-de-agente.html` | sessão de agente, subir/derrubar | **sessão de agente** | Controle · Administração/Gerenciamento |
| `workflow-02-estado-do-agente-vivo.html` | estado do agente vivo | **estado do agente vivo** | Administração/Gerenciamento · Controle |
| `workflow-03-tarefa-aberta.html` | tarefa aberta | **tarefa aberta** | Administração/Gerenciamento |
| `workflow-04-consumo-por-agente.html` | consumo por agente | **consumo por agente** | Controle · Administração/Gerenciamento |

**Coluna existente, não funcionalidade nova.** "Última atividade" é a coluna que o painel já exibe
(`painel/server.py`); nas duas telas em que aparece (sessão de agente e estado do agente vivo) está
declarada **NÃO PRECISA** na própria tela — nenhuma capacidade nova é pedida, só a reexibição, como
o mandato exige.

### Formato entregue (contrato de marcação — `verifica-prototipo.py` § Markup contract)

- um arquivo HTML **estático** por tela; zero `<script>`, zero recurso externo (`http`), sem servidor;
- CSS mínimo em cinza (tokens em `:root`, ~25 linhas, repetido por arquivo), sem `<body>` com
  `data-fonte` — a isenção vale **por bloco**, não para a tela inteira;
- **todo** controle e todo bloco com `data-fonte` (plataforma + ficha em `pesquisa/`, ou requisito do
  método); **todo** rótulo de domínio com `data-rotulo`, cujo **valor** é termo ratificado na rodada 2
  (`sessão de agente`, `estado do agente vivo`, `tarefa aberta`, `consumo por agente`,
  `roteamento por nome/ref`, `limite de orçamento`, `catálogo de skills/ferramentas/modelos`);
- **nenhum número inventado**: ilustrativo → dentro do marcador `data-exemplo` **com** "(exemplo)";
  vivo → `—` **com** `motivo:`; citação (ciclo, §, `F1`, `file:line`) sempre dentro de
  `data-fonte`/`data-referencia`, sem dígito solto em texto visível;
- `F1`, `F7` (idade nunca digitada), `F8` (todo "—" com motivo) e `F9` (controle só-ícone com
  `aria-label`) do `ux-design` 066 valem; **`F2`–`F6` e `F10`–`F12` são *n/a*** neste protótipo
  (supõem servidor e API) — declarado no rodapé de cada tela, não omitido;
- Princípio VIII: siglas expandidas na 1ª ocorrência (`PID`, `ux-design`).

### Auto-checagem — o gate do protótipo

```text
python specs/073-area-administrativa/prototipo/verifica-prototipo.py
-- verifica-prototipo: 11 screen(s), 0 finding(s)   [exit 0]
```

**11 telas · 0 achados** (as 7 integradas + as 4 desta entrega): as quatro regras do verificador
passam em todas. A conferência foi feita **antes** de commitar, e é re-executável por qualquer um.

### Dúvida declarada (herdada, não resolvida aqui)

A convenção de nome destas telas é **`slug.html` sem prefixo de contexto e sem ordem**
(`workflow-01-sessao-de-agente.html`, `workflow-02-estado-do-agente-vivo.html`, `workflow-03-tarefa-aberta.html`,
`workflow-04-consumo-por-agente.html`) — diverge das duas já em uso
(`mensageria-NN-slug.html`, `administracao-slug.html`), como o README desta pasta já declara (o
autor da tela escolhe o nome; renomear arquivo de outro worker não é decisão de worker). Se a
rodada 4 quiser uniformidade, é decisão do regente.

### Limites

Nada fora de `specs/073-area-administrativa/prototipo/` foi escrito (só o acréscimo desta seção ao
`qa-report.md`); **sem push, sem merge, sem código de produto, sem segredo**; a rodada não julga —
entrega a peça para o bar da rodada 4. Tokens (piso, soma do `message.usage` do transcript desde a
1ª ocorrência do `[[TASK]]`): **≈2,56 M** (entrada 2.380.079 + saída 179.650, em 96 mensagens;
`cache_read` 7.840.512 à parte).

## Correções da revisão fresca (073-T3-correcao-workflow, Worker05, 26/10)

**Escopo:** as correções da revisão em contexto fresco (`revisao-073-rodada-3.md` §1) **nas quatro
telas do Workflow**. Worktree sincronizada em `dbfe3f2` (`git merge --ff-only`). A revisão é relato,
não correção: quem corrige é o autor da tela — e é o que se fez aqui.

### R4 — `tasks.jsonl` não existe (o achado mais sério) — **corrigido**

As **cinco** ocorrências em `workflow-03-tarefa-aberta.html` (`:52`, `:66`, `:71`, `:72`, `:73`)
apontavam para `tasks.jsonl`. **Conferido com `ls` antes de escrever:** não existe `tasks.jsonl` em
lugar nenhum; o livro de ponto real é **`docs/records/tarefas.jsonl`** (mapa §7, l. 294), e o
arquivo existe. Todas as cinco passaram ao caminho completo. A `:73` citava **os dois nomes no
mesmo atributo** (`tasks.jsonl (attempt=) e o histórico de despachos do tarefas.jsonl`) — ficou um
caminho só: `docs/records/tarefas.jsonl (campo attempt= e o histórico de despachos)`. A `:102`, que
já acertava o nome mas omitia o diretório, também passou ao caminho completo — citação se resolve
de fora da pasta do ciclo.

### R7 — estados ilustrativos sem marca — **corrigido** (as 6 células)

As células de **estado** das tabelas ficavam nuas enquanto as vizinhas da mesma linha traziam
`data-exemplo="true"` + "(exemplo)" — ambíguo para o leitor (dado vivo ou exemplo?). Agora as seis
carregam a mesma marca das vizinhas: `workflow-01:89`, `:99`, `:109` e `workflow-02:79`, `:85`,
`:91` → `<span data-fonte="exemplo — nenhum dado real" data-exemplo="true">trabalhando (exemplo)</span>`
(e equivalentes para "esperando" e "sem tarefa"). Só marcação: nenhum texto de estado mudou.

### R9 — duas bases de citação no mesmo rodapé — **corrigido nas minhas 4 telas**

Escolhida **uma** base: **relativa à raiz do repositório**. As citações relativas ao ciclo viraram
caminhos completos (`confronto/…` → `specs/073-area-administrativa/confronto/…`; `pesquisa/…` →
`specs/073-area-administrativa/pesquisa/…`) e o mapa deixou de aparecer como
`mapa-de-contextos.md` sem diretório (agora `specs/073-area-administrativa/confronto/mapa-de-contextos.md`).
Resultado: `docs/…`, `painel/…`, `scripts/…`, `specs/…` — uma base só, resolvível de qualquer
diretório.

**Toda citação foi conferida contra o disco** (a citação tem de apontar para arquivo que existe).
Os 11 caminhos citados nas 4 telas existem: `specs/073-area-administrativa/confronto/confronto-decisao.md`
· `…/confronto/mapa-de-contextos.md` · `docs/records/tarefas.jsonl` · `painel/server.py` ·
`scripts/multi-session.py` · `…/pesquisa/claude-code.md` · `…/pesquisa/litellm.md` ·
`specs/066-painel-de-regencia/ux-design.md` · `specs/072-painel-de-regencia/spec.md` ·
`docs/governance/principles.md` · `docs/governance/task-ledger.md`.

### Auto-checagem

```text
python specs/073-area-administrativa/prototipo/verifica-prototipo.py
-- verifica-prototipo: 11 screen(s), 0 finding(s)   [exit 0]
```

**11 telas · 0 achados** depois das correções — nenhuma regra do gate regrediu (as correções mexem
em atributo e em texto de citação, e o gate as aceita: citação já estava sob `data-fonte`).

### O que NÃO é meu — dívida declarada da rodada 4

O mandato é aplicar **o que for correção de uma linha minha** e declarar o resto. Fica declarado,
para o regente decidir:

| Achado | Onde | Dono |
|---|---|---|
| **R1 / R1b** — "fila" nua em prosa e em atributo | `mensageria-01-caixa-de-entrada.html:75`, `:78` | telas da Mensageria (W03) |
| **R2** — "portão" nu em `<td>` | `mensageria-04-protocolo.html:61` | telas da Mensageria (W03) |
| **R2b** — "portão do humano" (terceiro qualificador) | `administracao-politicas.html:105` | telas da Administração (W04) + decisão de grafia |
| **R3** — "fila outbox" × "fila (outbox)" | `mensageria-03-roteamento.html:73`, `:74`, `:100` | telas da Mensageria (W03) + decisão de grafia |
| **R5** — `hooks/…` em vez de `scripts/hooks/…` | `administracao-politicas.html:62`, `:92`, `:98`, `:110`, `:122`, `:123` | telas da Administração (W04) |
| **R6** — `data-exemplo` zero vezes (segundo dialeto) | as 3 telas `administracao-*` | telas da Administração (W04) |
| **R8** — sem prefixo numérico | as 3 telas `administracao-*` | decisão do regente (uniformidade) |
| **R9 (metade da Mensageria)** — duas bases no mesmo rodapé | as 4 telas `mensageria-*` | telas da Mensageria (W03) |

**Decisões de grafia que a correção não pode tomar sozinha** (recomendações 2, 3 e 4 da revisão):
qual grafia única de "fila (outbox)" (o mapa prescreve com parênteses; a tela escreve sem) · se
"portão do humano" sobrevive ou entra no par permitido do §7 · estender a **regra 4** do gate a
`<p>`/`<td>`/atributos (hoje ela só lê rótulos — o ponto cego que a Parte 2 da revisão mediu) · e
**pôr `fixtures/tela-ruim.html` no alcance do gate**, senão a fitness function não tem oráculo.

### Limites

Só as 4 telas do Workflow e o acréscimo desta seção ao `qa-report.md`; **sem push, sem merge, sem
código de produto, sem segredo**; nenhuma outra tela foi tocada. Tokens (piso, soma do
`message.usage` do transcript desde a 1ª ocorrência deste `[[TASK]]`): **≈0,45 M** (entrada 430.176
+ saída 22.660, em 30 mensagens; `cache_read` 2.804.992 à parte).

### Correções da revisão fresca — telas da Administração (26/10)

Achados da `revisao-073-rodada-3.md` §1 que caem nestas três telas:

| # | Onde | Correção | Estado |
|---|---|---|---|
| **R5** | `administracao-politicas.html:62, :92, :98, :110, :122, :123` | `hooks/guard-immutables.py` → **`scripts/hooks/guard-immutables.py`** (6×). Caminho conferido antes de corrigir: não existe `hooks/` na raiz; o arquivo está em `scripts/hooks/` | **corrigido** |
| **R2b** | `administracao-politicas.html:105` | "portão do humano" → **"portão do regente"** — a grafia prescrita pelo mapa §7 (`confronto/mapa-de-contextos.md:296`: o segundo portão é *sempre* qualificado, "portão do regente") | **corrigido** |
| **R6** | as 3 telas | `data-exemplo="true"` nos 18 valores ilustrativos, além do `class="exemplo"` e da palavra no texto — encerra o segundo dialeto de marcação | **corrigido** |
| **R8** | as 3 telas | prefixo numérico uniforme | **dívida da rodada 4** — renomear arquivo é decisão da regente (uniformizou o Workflow em `af81499` e deixou a Administração como está); não renomeei por conta própria |
| **R9** | as 3 telas | uma base única de citação | **dívida da rodada 4** — a revisão não listou estas telas, mas o padrão ocorre: o mesmo rodapé mistura citação relativa ao ciclo (`ux-design 066 §4`) com relativa à raiz (`specs/066-painel-de-regencia/ux-design.md §4 e §7`), e cita `tasks.md` sem diretório. Escolher a base é decisão (recomendação 5 da revisão) — não alterei em silêncio |

R1, R1b, R2, R3 e R4 **não** tocam estas telas (são de `mensageria-*` e `workflow-03`).

**Verificação**

- `python specs/073-area-administrativa/prototipo/verifica-prototipo.py` → **11 telas, 0 achados, exit 0**.
- Auto-checagem própria re-rodada **só nas 3 telas** (cópia em diretório temporário): `fit073.py`
  **PASS** (R1–R9 verdes) e `mut073.py` **PASS** (9/9) — a mutação do R4 foi reapontada para a
  marcação nova, senão mediria um texto que não existe mais.
- **Nota para a rodada 4**: a regra 4 do gate ainda não foi ampliada a `<p>`/`<td>`/atributos
  (§2.3 da revisão). Quando for, nenhuma destas 3 telas acusa termo de colisão nu — "portão" aqui
  só aparece qualificado ("portão do regente") e "fila" não aparece.

## Rodada 3 — correções da revisão fresca nas telas da Mensageria (Worker03, 26/10)

**Escopo:** `T3-correcao-mensageria` (attempt=2, mandato do Gerente) — os achados **R1, R1b, R2 e
R3** da revisão em contexto fresco (`revisao-073-rodada-3.md` §1.2) que tocam as quatro telas da
Mensageria (commit desta correção, citando "ciclo 073"; worktree sincronizada em `dbfe3f2` com
`git merge --ff-only`):

| Achado | Onde | Antes | Depois |
|---|---|---|---|
| **R1** | `mensageria-01-caixa-de-entrada.html:78` | "A **fila** é *append-only*: …" | "A **fila outbox** é *append-only*: …" |
| **R1b** | `mensageria-01-caixa-de-entrada.html:75` | `data-fonte="… ADR 0027 — a **fila** recusa DELETE …"` | `… — a **fila outbox** recusa DELETE …` |
| **R2** | `mensageria-04-protocolo.html:61` | "(o **portão** vira contrato)" | "(o **portão do chamado** vira contrato)" |
| **R3** | `mensageria-03-roteamento.html:74` | `… — “fila de decisões” × “fila outbox”` | `… — fila de decisões × fila outbox` (grafia única; `:73` e `:100` já a tinham) |

**R6–R9:** nenhum é correção de uma linha das telas da Mensageria. **R9** (parte das telas da
Mensageria — bases de citação mistas: `confronto/…` relativo ao ciclo convivendo com `docs/…`,
`painel/…`, `specs/066-…` relativos à raiz, e `mapa-de-contextos.md` sem diretório) fica **dívida
declarada da rodada 4**: unificar a base de citação é decisão de convenção **global** (vale para as
11 telas), não correção pontual desta rodada.

Verificação re-executada (antes de commitar):

```text
python specs/073-area-administrativa/prototipo/verifica-prototipo.py
-- verifica-prototipo: 11 screen(s), 0 finding(s)   [exit 0]
```

**Nota sobre R3 (registrada para o fechamento):** a §7 do mapa escreve "**fila (outbox)**" *com*
parênteses (`mapa-de-contextos.md:292`); o despacho fixou a grafia "**fila outbox**" *sem*
parênteses — foi a seguida aqui. Se o fechamento quiser uma grafia só, a §7 é o outro lado a alinhar.

### Limites

Sem push, sem merge, sem código de produto, sem segredo; só as quatro telas da Mensageria e o
acréscimo desta seção ao `qa-report.md`. Tokens (piso): declarados no `[[DONE]]`.
