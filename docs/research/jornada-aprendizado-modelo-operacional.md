# Jornada de aprendizado — Modelo Operacional (por elemento)

> Registro dos insights construídos ao avaliar criticamente cada elemento do modelo
> operacional (`docs/governance/modelo-operacional.md`), no formato de tutoria
> (perguntar → criticar → refinar), não de exposição. Documento **vivo**: cresce à
> medida que a jornada avança pelos elementos.
>
> **Iniciado**: 2026-07-22 · **Contexto**: 1 humano orquestrando N agentes de IA ·
> **Insights em negrito foram trazidos pelo aprendiz ao criticar cada peça.**

## Mapa dos elementos

```
FUNDAMENTO   [1] Princípio central ← [10] DORA/SPACE (evidência)
MECÂNICA     [2] Spec-Driven · [3] Fluxo agentic · [4] Orquestração
ESTRUTURA    [5] Papéis+RACI · [6] Cerimônias (Shape Up+Kanban)
QUALIDADE    [7] Artefatos · [8] DoR/DoD · [9] Gates+risco · [11] Rastreabilidade
META         [12] Governança leve (constituição · ADRs · YAGNI)
```

Status: ✅ **JORNADA COMPLETA** — `[1]` `[2]` `[3]` `[4]` `[5]` `[6]` `[7]` `[8]` `[9]` `[10]` `[11]` `[12]` (12/12)

---

## `[1]` Princípio central — *IA escreve · humano decide/aprova · verificação independente valida*

- Ataque ao "humano decide": **toda decisão pode ser automatizada se houver um registro
  auditável (alternativas + racional), seja quem/o que a tome.** → é o **ADR**, e separa
  a *qualidade* da decisão da *identidade* de quem decide.
- Refino 1: **o humano delega, e a delegação vai pro registro** → política declarativa
  `allow/deny/ask` (Princípio IV); a responsabilidade sobe um nível (responde pela
  *política*, não por cada instância).
- Refino 2: registro é **ex-post**; gate é **ex-ante**. Para ação irreversível, auditar
  não impede o dano.
- **Insight-chave: o que torna o irreversível seguro de delegar é a REVERSIBILIDADE
  engenheirada** (backup / dry-run / staging / soft-delete = "permite desfazer"). O gate
  humano sempre foi um *proxy* de "torne reversível ou olhe antes". Engenheirar
  reversibilidade → menos coisas precisam do gate forte.
- Fios: liga ao checkpoint/rewind/git (`[3]`) e ao DORA "recuperável > cauteloso" (`[10]`).

## `[2]` Spec-Driven — *a spec é a fonte de verdade*

- Por que a spec não apodrece: virou o **input que gera o código**, não uma descrição
  dele (inversão de dependência). "Documentação atualizada" era o *sintoma*; a causa é a
  inversão.
- Crítica: nem toda mudança merece spec (senão vira burocracia). **Bug → simplifica.**
- Regra derivada: **valor da spec = ambiguidade × raio de impacto × irreversibilidade.**
  O "spec" de um bug é um **teste que o reproduz**.
- OpenSpec avaliado → **descartado** (uma ferramenta só); a ideia do *delta* virou a
  **raia leve**.
- Infra: **decisão de que infra tem specs exclusivas** → infra deve ser *mais* estrita
  (zona de alta irreversibilidade).
- **Produziu mudança real**: `modelo-operacional.md` v1.1.0 (§3 Raias de trabalho;
  spec de infra com gates de reversibilidade) + ADR 0005.

## `[3]` Fluxo agentic — *explore→plan→code→commit + subagentes + /clear + revisor fresco*

- Restrição única por trás das 4 peças: **a janela de contexto é finita e degrada ao
  encher** — o inimigo é o *acúmulo*, não a falta. Aterrissagem: **"foco / resetar"**.
- As 4 peças = **economia de contexto** (manter o sinal alto): o *plan* comprime a
  exploração; subagentes descarregam a leitura; `/clear` despeja ruído; revisor fresco =
  não contaminado pelos becos sem saída.
- Crítica dos limites: **resetar demais → esquece o básico; delegar demais → subagente
  cai em ÓTIMO LOCAL** (não recebeu o contexto integrador).
- Resolução: **preserve o contexto que sustenta, descarte só o ruído.** O "contexto
  integrador" **é a spec/plan** → **`[2]` e `[3]` são a mesma espinha**: a spec é o que
  sobrevive ao reset e cruza toda fronteira.

## `[4]` Padrões de orquestração — *map-reduce cognitivo + espectro workflow↔agent*

- A peça que falta depois do *map* (workers em paralelo) é o **reduce cognitivo**:
  reconciliar as fatias (contratos, coerência com a spec) — feito por quem tem o
  **contexto global**, o **Orquestrador**. Padrão: **orchestrator-workers**. Analogia
  do aprendiz: **"map-reduce, mas para a questão cognitiva"**.
- Camada crítica: o **corte** é mais traiçoeiro que o reduce. Cortar nas costuras
  erradas → nenhum reduce salva. **Costuras certas = bounded contexts (DDD)**; cortar
  ao longo das fronteiras arquiteturais é o que torna a paralelização segura (`[4]`↔`[2]`).
- **Insight organizador (seu):** fixar o caminho (*workflow*) → previsível, escopo
  reduzido, foco, sinergia; deixar o LLM cortar (*agent*) → flexível, mas pode errar o
  corte (ótimo local) e varia a cada execução. Regra: **use a menor autonomia que
  resolve** ("comece simples").
- Os 6 padrões já vivem no modelo: **chaining** = fluxo Spec Kit; **routing** = as raias
  (§3); **parallelization** = subagentes por bounded context; **orchestrator-workers** =
  papel Orquestrador (§4); **evaluator-optimizer** = Writer/Reviewer + `/code-review`;
  **autonomous** = evitado (YAGNI, exige guardrails pesados).
- Fechamento: **melhor arquitetura → mais tempo no lado barato/previsível do espectro.**
  Boas fronteiras compram previsibilidade.

## `[10]` DORA/SPACE — *velocidade e estabilidade não são trade-off*

- Achado contraintuitivo: os **mesmos** times de elite são rápidos **e** estáveis. As 4
  métricas são *outcomes* de capacidades (CI, trunk-based, testes, revisão, deploys
  pequenos).
- **Alavanca única: lote pequeno** — move as 4 métricas juntas (frequência↑, lead time↓,
  falha↓, recuperação↑).
- **Analogia (sua): linha de produção cognitiva** — padronização reduz fricção/variação
  (Ford). Complemento: a linha do Ford não tinha *undo barato*; a cognitiva tem →
  **rápido E estável = lote pequeno + reversibilidade (`[1]`)**.
- Confirma que a DoD e as raias do modelo não são burocracia: são as capacidades de elite.

## `[5]` Papéis e responsabilidades — *RACI em solo+IA*

- Num time, decide/executa/verifica = 3 pessoas (o contrapeso). Solo+IA: preservar sem
  colapsar tudo numa cabeça.
- **Insight (seu): delega-se tudo menos o A.** R→agente, C→agente independente (contexto
  fresco), I→logs, **A→humano** — porque accountability é responder pelas consequências
  (`[1]`).
- Armadilha do funil: A + verificar cada item à mão = fazer tudo sozinho. **Insight
  (seu): o humano é Accountable pela política, gates e critérios — não por cada item.**
  Projeta os trilhos; agentes operam dentro.
- Contrapeso preservado: **decide (humano) ≠ executa (dev-agent) ≠ verifica (review-agent
  fresco)**.

## `[6]` Cerimônias e cadência — *cerimônia = função; WIP = atenção humana*

- **Cerimônia é a função que entrega, não a reunião.** Corta-se pela função: a da daily
  (sincronizar entre pessoas) some em solo+IA → cortada.
- **Insight (seu): retro é a que fica MAIS valiosa com agentes** — a melhoria vira
  instrução versionada (durável/executável), não hábito mole.
- Tensão do WIP: **dependência entre tasks** limita o paralelo **dentro** da feature;
  mas **o humano (atenção/decisão) é o gargalo** através de features (`[5]`).
- **Insight (seu): o gargalo é o humano; muitos gates sobrecarregam.** Corolário:
  paralelizar DENTRO da feature; escalar = **baratear os gates** (`[8]`/`[1]`), não abrir
  frentes.

## `[7]` Entregáveis e artefatos — *consumidor + forcing function, não conteúdo*

- Artefato custa **duas vezes** (escrever + manter). "Dar contexto/direção" é necessário
  mas não distingue — design doc também dá e apodrece.
- **Insight-chave:** artefato vive se é **input consumido com forcing function** (spec →
  agente gera; teste → CI vermelho) **ou imutável** (ADR). Journey = **vivo por gate**
  (Princípio VII: capturas + heurística no mesmo PR).
- **2ª metade da regra (seu fio "o que/por que" → ADR):** não duplicar função já servida —
  PRD avulso duplica a spec; design doc/RFC avulso duplica plan+ADR → **YAGNI**.
- Refresh: **YAGNI** = "You Aren't Gonna Need It" — não construir o especulativo.

## `[8]` Definition of Ready / Done — *verificável autonomamente; verde ≠ certo*

- **Insight (seu): a propriedade é "verificável autonomamente"** — pass/fail objetivo que
  o agente gera e o hook confere. É "prove, não declare" (`[1]`) em máquina; barateia o
  gate (`[6]`).
- O trabalho é **converter julgamento em check** (harness design): "código limpo" → lint +
  fitness functions; "boa UX" → tokens + heurística.
- **Insight (seu): a peça é local — ainda é preciso ver se atendeu o requisito da jornada /
  não comprometeu o todo.** É o **ótimo local do `[4]`** no nível da qualidade. Verde ≠
  certo. O global vai para a DoD (journey/e2e/rastreabilidade) + checkpoint humano; "é a
  coisa certa" fica com o A humano (`[5]`).

## `[9]` Gates humanos e classes de risco — *gate proporcional ao risco*

- Gate uniforme falha de dois jeitos: **pesado → funil (`[6]`)**; **leve → irreversível
  escapa (`[1]`)**.
- **Insight (seu): o eixo é irreversibilidade × impacto.** Logo, gate **proporcional** —
  automatiza baixo, escala alto, **bloqueia** lote/cross-tenant/admin.
- Amarre 1: **mesmo eixo das raias (`[2]`)** — lá decide *processo* (spec), aqui decide
  *gate*. Amarre 2: **reversibilidade rebaixa a classe** (`[1]`) → menos gates pesados.

## `[11]` Rastreabilidade — *a memória de longo prazo do projeto*

- **Insight (seu): dá "o porquê e o quê"** sem re-derivar. Em solo+IA, como o agente
  reseta (`[3]`), os artefatos ligados **são a memória** durável do projeto.
- Dois sentidos: para frente (spec → construída/verificada?) e **para trás** (sintoma →
  código → spec → porquê) = recuperação rápida (`[10]`).
- **Emergente, não ferramenta**: o elo emerge de artefatos se referenciarem; a DoD (`[8]`)
  o força. Governança leve, sem matriz.

## `[12]` Governança leve — *aprender sem inchar*

- **Insight (seu): o risco é bloat/ossificação; a força é YAGNI + poda + flexibilidade.**
- Arquitetura da flexibilidade: **núcleo firme** (constituição, muda devagar) + **periferia
  evoluível** (modelo/handbook, versão própria) + **memória append-only** (ADRs) + **loop
  de aprendizado** (retro → regra).
- **Meta**: esta jornada FOI o `[12]` em ação — crítica → refino → ADR 0005 → modelo v1.1.0
  → Constituição v1.4.0.

---

## Síntese final — os fios que amarram os 12 elementos num só sistema

A jornada não é uma lista; é **um sistema** costurado por poucos fios recorrentes:

1. **Reversibilidade** é a alavanca-mestra: torna o irreversível seguro de delegar (`[1]`),
   rebaixa a classe de risco (`[9]`), é a recuperação do DORA (`[10]`) e o rewind do fluxo
   agentic (`[3]`).
2. **Um mesmo eixo** — `ambiguidade × raio × irreversibilidade` — decide quanto **processo**
   (raias, `[2]`) e quanto **gate** (`[9]`).
3. **Economia de contexto** (`[3]`/`[4]`): contexto finito; a **spec é a memória
   integradora** que sobrevive ao reset (`[2]`/`[11]`).
4. **Ótimo local** reaparece: no reduce da orquestração (`[4]`) e no "verde local ≠ certo
   global" da DoD (`[8]`).
5. **O humano é Accountable pela política, não pelo item** (`[5]`) — foge do funil e escala.
6. **Gate barato = verificável autonomamente** (`[8]`) — a fuga do gargalo humano (`[6]`).
7. **O loop de aprendizado** (retro → regra versionada, `[6]`/`[12]`) — que esta própria
   jornada executou.
8. **YAGNI** — a poda que mantém tudo leve, do processo aos artefatos à governança.

---

## Meta-insights (transversais)

- **A própria jornada é a retro (`[5]/[6]`) em ação**: criticar um elemento gera regra
  versionada. Prova viva: rendeu o modelo v1.1.0 + ADR 0005.
- **FlowBuilder**: disciplina de branch **descartada** (específica do repo); specs de
  infra **adotadas** como raia própria.
- **Padrão recorrente da tutoria**: o aprendiz codificou o *quê* (ex.: "/clear entre
  tarefas", "revisão em contexto fresco") no modelo antes de entender o *porquê*; a
  jornada preenche o porquê e conecta os elementos.

## Artefatos produzidos (branch `docs/praticas-e-modelo-operacional`)

- `dcb6a64` — pesquisa citada (`docs/research/…-praticas-desenvolvimento-…`)
- `5fec5a7` — modelo operacional v1.0.0 + ADR 0004
- `6dcaa2d` — modelo v1.1.0 (raias + gates de infra) + ADR 0005

## Próximo

**Jornada concluída (12/12).** Handbook completo em `docs/handbook/` (capítulos 01–12).

Enforcement implementado (ADR 0006, modelo v1.2.0 §12): PR template com a DoD, gate de
CHANGELOG na CI, comando `/dod`, `CHANGELOG.md`. Ver `docs/governance/modelo-operacional.md`
§12 (mapa item → mecanismo).

Próximo passo restante: **aplicar o modelo numa feature real** via spec-kit (o teste de
campo); follow-ups: habilitar secret scanning nativo, avaliar lint (ruff/eslint).
