# Pesquisa — o upstream: decompor um projeto grande em objetos executáveis

> **Migrado para o catálogo (ciclo 047).** O julgamento por **ideia** e o veredito
> **corrente** vivem agora em [`docs/ecosystem/`](../ecosystem/README.md) — fontes com licença, um card
> datado por ideia e o estado em índice append-only. Este documento fica como está: é
> a observação daquele momento, e o catálogo não reescreve história.

> **Pergunta**: existe método (e skills prontas) para ir de uma **intenção grande** até o
> conjunto de specs que o Maestro sabe executar? O que adotar, o que absorver, o que
> descartar?
>
> **Capturado em** 2026-08 · ciclo 036 · agente `research-curator`
> · Fontes primárias citadas ao final de cada seção.

## 1. O gap, medido no nosso próprio repositório

O Maestro é forte **do `spec.md` para a frente**: oito portões, treze agentes, gate humano
em cada ciclo. A montante da spec, o que existe é um documento de roadmap escrito à mão.

Três medidas do próprio repositório:

```
$ ls specs/*/spec.md | wc -l                    # 34 specs
$ # origem declarada, classificada à mão:
   14 nascem de cadência/fase do roadmap
   20 nascem de pedido pontual do Steward
$ grep -l "roadmap\|epic\|decompos" .claude/agents/*.md skills/*/SKILL.md
   (nenhum agente ou skill cobre decomposição)
```

Ou seja: **20 de 34 ciclos nasceram de uma conversa**, não de um corte planejado. Isso
funcionou porque o "projeto" era o próprio método e o Steward é o dono do escopo — mas é
exatamente o que não escala para um produto com terceiros, e é o que o ciclo 017 já tinha
mostrado quando o roadmap ficou congelado por sete ciclos (anti-padrão 15).

Não há **objeto**, **verbo** nem **portão** a montante:

| Camada | Objeto | Quem produz | Portão |
|---|---|---|---|
| Intenção grande | — | — | — |
| Corte em fatias | — | — | — |
| Ciclo | `spec.md` | `spec-agent` | ◆ humano (DoR) |
| Execução | plan/tasks/código | 13 agentes | 8 checks + ◆ merge |

## 2. O que existe lá fora

### 2.1 Frameworks agênticos com upstream próprio

**BMAD-METHOD** é o mais completo: divide o ciclo de vida em *Agentic Planning* e
*Context-Engineered Development*, com agentes dedicados (Analyst, Product Manager,
Architect, Scrum Master) e uma cadeia de artefatos versionados em Markdown:

```
brainstorm → product-brief → PRD (com épicos e rascunho de histórias)
           → UX spec → architecture → stories (Scrum Master) → dev → QA
```

O detalhe que importa: **todo agente produz artefato verificável, não resposta de chat** —
a mesma tese do nosso Princípio VI. E o `bmad-spec` "destila qualquer intenção num contrato
`SPEC.md` sucinto", com `stories.yaml` opcional. É a arquitetura mais próxima do que nos
falta.

**Agent OS (buildermethods)** resolve o mesmo problema com **três arquivos, não uma
pirâmide**: `mission.md` (visão, usuários, problemas), `roadmap.md` (fases com features
priorizadas) e `tech-stack.md`. O comando `/shape-spec` lê esses três + os padrões do
projeto e faz perguntas dirigidas antes de escrever a spec. É o oposto do BMAD em custo:
onde o BMAD tem sete papéis, o Agent OS tem três documentos e uma conversa.

**GitHub Spec Kit** — o nosso motor — **não tem nada a montante**. Verificado comando a
comando: `constitution, specify, clarify, plan, tasks, taskstoissues, implement, converge,
analyze, checklist`. Nenhum cobre decomposição de projeto em várias specs. O ponto de
entrada é "descreva o que você quer construir", e assume que alguém já cortou.

> **Fontes**: [BMAD workflow map](https://docs.bmad-method.org/reference/workflow-map/) ·
> [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) ·
> [Agent OS — product planning](https://buildermethods.com/agent-os/product-planning) ·
> [`shape-spec.md`](https://github.com/buildermethods/agent-os/blob/main/commands/agent-os/shape-spec.md) ·
> [Spec Kit](https://github.com/github/spec-kit)

### 2.2 Skills publicadas no padrão `SKILL.md`

**`deanpeters/Product-Manager-Skills`** — o achado mais direto: **70 skills** de gestão de
produto no padrão que já usamos, organizadas em três camadas (19 *workflow*, 27
*interactive*, 24 *component*). Cobrem exatamente a nossa lacuna: `problem-framing-canvas`,
`opportunity-solution-tree`, `epic-breakdown-advisor`, `roadmap-planning`,
`user-story-mapping-workshop`, `prd-development`, `prioritization-advisor`.

O `roadmap-planning` liga item de roadmap a **épico com hipótese e métrica de sucesso**, e
declara o anti-padrão que queremos evitar: roadmap de "feature factory", sem narrativa
estratégica.

⚠️ **Licença CC BY-NC-SA 4.0**: uso e adaptação com atribuição, **vedado repacote
comercial**. Consumir como fonte citada é seguro; copiar arquivo para dentro do nosso
toolkit, não — nossa distribuição é MIT.

**`decompose`** (skill comunitária): "quebra uma feature em issues do GitHub ordenadas e do
tamanho de um agente, que o *ship-loop* consome em sequência". Faz o corte **abaixo** da
spec (feature → issues), não acima. É o pedaço que o nosso `tasks.md` já cobre.

**`spec-decompose`** (relato de campo, Joshua McDonald): a peça mais próxima do que
precisamos. Três passadas sobre uma spec fechada — **superfície** (camadas
arquiteturais: dados, regra, API, frontend, infra), **jornada** (comportamentos visíveis em
sequência) e **risco** (raio de impacto: alto = migração/dependência externa; baixo =
aditivo) — produzindo *mini specs* com contrato de entrada e saída, mais dois artefatos: um
**índice de specs** (`specs/INDEX.md`, com status, dono, mini specs em voo e bloqueadas) e
um **mapa de paralelismo** (uma coluna por executor, uma linha por dia).

Duas regras de tamanho que valem ouro: **"nenhuma mini spec passa de dois dias"** e
**"mantenha a spec abaixo de quatro páginas; se passar, são duas specs"**. E o passo que
nos interessa mais: **revisão humana da decomposição antes de começar o paralelo** — porque
acoplamento escondido não é achado por análise estática.

> **Fontes**: [Product-Manager-Skills](https://github.com/deanpeters/Product-Manager-Skills) ·
> [roadmap-planning/SKILL.md](https://github.com/deanpeters/Product-Manager-Skills/blob/main/skills/roadmap-planning/SKILL.md) ·
> [skill `decompose`](https://claudskills.com/skills/decompose/) ·
> [Spec-driven development num time pequeno](https://joshmcdonald.medium.com/running-a-small-team-on-a-big-project-spec-driven-development-with-claude-code-9a1b97f58551)

### 2.3 As técnicas clássicas — onde está o conhecimento de verdade

Os frameworks acima **orquestram**; quem ensina a **cortar** é a literatura ágil, e ela é
muito mais precisa do que qualquer skill que encontrei.

**Padrões de fatiamento (Richard Lawrence / Humanizing Work)** — nove padrões, cada um um
tipo de costura: passos do fluxo · operações (criar/ler/atualizar/apagar) · variação de
regra de negócio · variação de dados · forma de entrada · esforço maior · simples/complexo ·
adiar desempenho · investigação isolada. Mais duas regras de desempate que valem sozinhas:

> **"Escolha o corte que permite despriorizar ou jogar fora uma das fatias."**
> **"Escolha o corte que produz fatias mais parecidas de tamanho."**

**SPIDR (Mike Cohn)** — cinco cortes memorizáveis: *Spike, Path, Interface, Data, Rules*.
"Cada letra é uma linha de corte, e cada corte produz fatias que entregam sozinhas, não
metades que só funcionam juntas."

**INVEST** e **fatia vertical**: a restrição que elimina metade dos cortes ruins — cortar
por camada técnica (só backend, só frontend) produz partes sem valor próprio; a fatia
precisa atravessar da interface ao dado.

**Descoberta (a montante do corte)**: *Impact Mapping* (Gojko Adzic, 2012) liga meta →
ator → impacto → entregável, forçando o elo entre estratégia e execução; *Opportunity
Solution Tree* (Teresa Torres, 2016) vai de resultado desejado → oportunidades → ideias →
experimentos; *User Story Mapping* organiza a espinha da jornada; *Event Storming* levanta
eventos e comandos do domínio (e é o que produz as **fronteiras** que a nossa economia de
contexto pede).

**E o consenso de 2026 sobre agentes**: fatia vertical não é preferência de estilo — é a
**infraestrutura da paralelização**. "Quando um agente conhece o contrato de dados na
fronteira entre camadas, ele gera código que respeita esse contrato." A recomendação
recorrente é *escrever o contrato da tarefa antes de escolher o modelo*: objetivo, critério
de aceite, artefatos exigidos, dependências e efeitos colaterais.

> **Fontes**: [Guia de fatiamento — Humanizing Work](https://www.humanizingwork.com/the-humanizing-work-guide-to-splitting-user-stories/) ·
> [SPIDR](https://blogs.itemis.com/en/spidr-five-simple-techniques-for-a-perfectly-split-user-story) ·
> [Story splitting (DPR)](https://socadk.github.io/design-practice-repository/activities/DPR-StorySplitting.html) ·
> [Opportunity Solution Trees](https://www.producttalk.org/opportunity-solution-trees/) ·
> [Impact Mapping + OST](https://busra.co/blog/combining-impact-mapping-and-opportunity-solution-tree) ·
> [Agentic coding em 2026 (Sourcegraph)](https://sourcegraph.com/blog/agentic-coding) ·
> [Vertical slicing e IA](https://www.mddionline.com/artificial-intelligence/vertical-slicing-as-a-foundation-for-samd-development-in-the-age-of-agentic-ai)

## 3. Avaliação — o que serve para 1 humano regendo N agentes

O critério é o de sempre: **artefato com consumidor e forcing function**, corte por
fronteira, menor cerimônia que resolve. Contra isso:

| Fonte | O que oferece | Veredito |
|---|---|---|
| **Padrões de fatiamento** (Lawrence, 9) + **SPIDR** | o *como* cortar, com regras de desempate | **Absorver** — é o miolo da skill que falta; conhecimento estável, não ferramenta |
| **Fatia vertical / INVEST** | a restrição que impede corte por camada | **Absorver** como lei da skill |
| **Três passadas** (superfície, jornada, risco) + regra de tamanho | o *procedimento* de decomposição e o limite de tamanho | **Absorver** — adaptado: nossa unidade é o **ciclo**, não "dois dias" |
| **Contrato declarado por fatia** | o que torna paralelismo seguro | **Absorver** — vira campo obrigatório |
| **Agent OS** (mission/roadmap/tech-stack + shape-spec) | upstream mínimo, três documentos | **Absorver o formato**, não a ferramenta: já temos roadmap; falta ligar item ↔ ciclo |
| **BMAD-METHOD** | pipeline completo com 7 papéis e PRD/épicos/histórias | **Descartar como pipeline** — é cerimônia de time para quem opera sozinho (mesmo veredito que demos ao Scrum). **Observar** o princípio "todo agente produz artefato" (já é nosso) |
| **Product-Manager-Skills** (70 skills) | catálogo enorme de discovery e priorização | **Observar e citar** — licença CC BY-NC-SA impede levar para o nosso pacote MIT; útil como fonte e como prova de que o padrão `SKILL.md` cobre esse território |
| **Impact Mapping / OST / Story Mapping / Event Storming** | descoberta e fronteiras | **Observar com gatilho**: entram quando houver produto com usuários externos; hoje o Steward *é* o usuário |
| **skill `decompose`** (feature → issues) | corte abaixo da spec | **Descartar** — nosso `tasks.md` já faz, e amarrar a issues do GitHub é acoplamento que não queremos |
| **PRD / épico / história** como camadas obrigatórias | hierarquia clássica | **Descartar a pirâmide** — três níveis novos para um operador é o anti-padrão 11. Um nível novo, no máximo |

**A conclusão desconfortável**: não falta ferramenta lá fora — falta **um objeto e um verbo
nossos**. Tudo que encontrei ou é pesado demais (BMAD), ou já temos (decompose→tasks), ou é
conhecimento que precisa virar skill (fatiamento, três passadas), ou é licenciado de forma
incompatível (PM-Skills).

## 4. Proposta (para o gate do Steward)

O mínimo que fecha o gap sem construir uma pirâmide. **Um objeto novo, um verbo novo, um
portão novo.**

### 4.1 O objeto: `outcome` (resultado), não "épico"

Um **resultado** é a mudança observável que se quer causar — com métrica e dono. Não é
feature, não é entregável. É o que o roadmap deveria ter e não tem:

```
docs/product/outcomes/NNN-<slug>.md
  - o que muda no mundo (uma frase, verbo de mudança)
  - como se mede (número, ou "não sei ainda" declarado)
  - apetite (tempo fixo)
  - fatias: tabela ciclo × contrato × ordem × estado
```

Por que "resultado" e não "épico": épico é balde de features (feature factory); resultado
carrega o *porquê* e sobrevive a mudar de solução no meio.

### 4.2 O verbo: skill `slice-outcome` (inglês, instalável)

O procedimento das três passadas, com os padrões de fatiamento embutidos e **Iron Law**:

```
NO SLICE WITHOUT ITS OWN ACCEPTANCE CRITERION AND A DECLARED CONTRACT
```

Brechas fechadas antecipadamente: *"essa fatia é só o backend"* (fatia sem valor próprio é
camada, não fatia) · *"o contrato a gente combina na hora"* (contrato combinado na hora é o
acoplamento que nenhum reduce salva) · *"depois eu escrevo o critério"* (depois é onde a
fatia vira balde).

Conteúdo: as três passadas (fronteira → jornada → risco), os nove padrões como checklist,
as duas regras de desempate de Lawrence, a regra de tamanho (**uma fatia = um ciclo; se não
cabe, corte de novo**) e a proibição do corte horizontal.

### 4.3 O portão: `check-outcomes.sh`

O que ele mede (e o que **não** mede):

- toda spec de ciclo cita o resultado que serve, **ou** declara `sem resultado` com motivo
  (manutenção, correção — o equivalente à raia leve);
- todo resultado tem pelo menos uma fatia e cada fatia tem contrato declarado;
- resultado sem ciclo há N ciclos aparece como **dívida de roadmap** (mesmo mecanismo do
  `check-retro.sh`, que já provou funcionar);
- **não** julga se o corte está certo — isso é gate humano, como a raia.

### 4.4 O gate humano: aprovar o corte

Novo gate indelegável, na altura certa: **aprovar a decomposição** antes de abrir o primeiro
ciclo da fatia. É o gate de maior alavancagem que existe, porque corte errado nenhuma
verificação salva (teorema T3 + corolário C6 dos axiomas).

### 4.5 O que **não** faremos

- Não haverá PRD, épico nem história como camadas obrigatórias.
- Não haverá agente de "Product Manager" com sete papéis; o `spec-agent` ganha, no máximo,
  um irmão estreito (`outcome-shaper`) — e só se a dor aparecer no primeiro uso real.
- Não copiaremos nenhum arquivo do `Product-Manager-Skills` (licença incompatível); ele
  entra como **fonte citada** no apêndice do livro.
- Nada de mapa de paralelismo por dia: nosso trabalho em curso é **um** (capítulo 07).

## 5. Riscos declarados

1. **Cerimônia a montante é o risco maior.** Mitigação: a decomposição só é obrigatória
   quando a intenção não cabe em um ciclo — a mesma régua das raias, aplicada acima.
2. **Resultado sem métrica vira slogan.** Mitigação: o template exige número **ou** a frase
   explícita "ainda não sei medir", que é honesta e revisitável.
3. **O nosso próprio histórico contradiz a necessidade**: 20 ciclos nasceram de conversa e
   entregaram. A pergunta legítima é se o gap é real ou se é o método pedindo processo que
   não paga. **Resposta honesta**: para *este* repositório, com o dono do escopo na sala, o
   ganho é pequeno; para o primeiro projeto com produto e usuários externos, o gap é o que
   quebra. Daí a proposta ter **gatilho**, não adoção imediata.

## 6. Recomendação

**Adotar o núcleo (4.1–4.4) num único ciclo**, com uso real imediato: decompor a próxima
intenção grande que existir de fato — não um exemplo inventado. Se não houver intenção
grande agora, **registrar como gatilho aberto** e não construir nada: skill sem dor é
exatamente o que a nossa regra de nascimento proíbe.
