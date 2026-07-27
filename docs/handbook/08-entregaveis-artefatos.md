# Capítulo 08 — Entregáveis e artefatos (elemento `[7]`)

> Um artefato custa **duas vezes** (escrever + manter). Só vale o custo se for um **input
> consumido com forcing function** — ou imutável.

## 1. Pergunta central

A lista clássica é enorme (PRD, spec, plan, ADR, RFC, design doc, journey, runbook,
changelog, C4...). **O que faz um artefato valer seu custo duplo — e o que o distingue de
"cerimônia de papel" que apodrece?**

## 2. Fundamentação teórica

Todo artefato custa para **escrever** e para **manter atualizado**. O que "dá contexto e
direção" é necessário, mas **não** distingue — um design doc também dá direção e apodrece.
O que distingue é **mecânico**:

> **Um artefato sobrevive quando é um INPUT que algo downstream consome, com uma
> *forcing function* que falha barulhento quando ele está velho** — ou quando é
> **imutável** (registra um ponto no tempo e nunca muda, como o ADR).

- A **spec** vive porque o agente **gera código dela**: velha → código errado → quebra
  visível (`[2]`).
- O **teste** vive porque a **CI** o consome: velho → vermelho.
- O **ADR** vive por **imutabilidade**: nunca precisa de update.
- O **journey** é **vivo por gate**: a Constituição (Princípio VII) regenera as capturas
  do build real e revisa a heurística **no mesmo PR** — sem esse gate, apodrece. É o caso
  canônico de *living documentation / docs-as-code*: doc desconectado do fluxo não tem
  forcing function.

**Segunda metade da regra: não duplique função já servida por um artefato vivo.** Um
**PRD** avulso duplica a função da **spec**; um **design doc/RFC** avulso duplica **plan +
ADR**. Sem consumidor próprio, apodrecem → cerimônia de papel (YAGNI).

## 3. Frameworks / abordagens avaliados

| Artefato | Consumidor | Forcing function | Veredito |
|---|---|---|---|
| **Spec** (`spec.md`) | agente (gera código) | código errado se velha | **Essencial** |
| **Plan** (`plan.md`) | dev-agent / Constitution Check | divergência da impl | **Essencial** |
| **Tasks** (`tasks.md`) | dev-agent | efêmero (descarta pós-uso) | **Essencial (efêmero)** |
| **Código + testes** | CI | vermelho | **Essencial** |
| **ADR** | decisões futuras / onboarding | **imutável** | **Essencial** |
| **Journey doc** | gate de PR (capturas + heurística) | PR falha se não regenerar (P. VII) | **Essencial (por gate)** |
| **Runbook** | incidente / deploy | uso real / drills (fraco) | **Essencial (disciplina)** |
| **Changelog** | release | PR de release | **Essencial (se gated)** |
| **DoR/DoD** | agente / Stop-hook | gate de merge | **Essencial** |
| **PR** | revisão / merge | — | **Essencial** (na raia leve, *é* o artefato) |
| PRD avulso | (duplica a spec) | nenhuma | **YAGNI** |
| Design doc / RFC avulso | (duplica plan + ADR) | nenhuma | **YAGNI** |
| C4 diagrams | humano (leitura) | nenhuma | **Fase 2 / YAGNI** |
| Painel de métricas DORA | — | — | **YAGNI** |

## 4. Recomendação de utilização (1 humano + N agentes)

- **Manter** apenas artefatos com consumidor + forcing function (ou imutáveis).
- **Não criar** artefato cuja função já é servida por um vivo (PRD→spec; design doc→plan+ADR).
- **Journey exige o gate** do Princípio VII para não apodrecer (não é "doc solto").
- Formalizar o **changelog** com forcing function no PR de release (pendência do modelo).

## 5. Conexões

- **`[2]`** — a spec é o arquétipo do "input consumido que não apodrece".
- **`[8]` DoR/DoD** — são artefatos-checklist verificáveis (habilitam o gate barato).
- **`[11]`** — a rastreabilidade liga os artefatos (spec↔PR↔testes↔journey).
- **`[12]`** — ADR é o artefato imutável de governança.

## 6. Insight da jornada e impacto no modelo

O que faz um artefato valer não é o **conteúdo** ("dá contexto") e sim o **mecanismo**:
**consumidor + forcing function**, ou **imutabilidade** (ADR). E **não duplicar função já
servida** (PRD/design doc avulsos = YAGNI). Fundamenta o catálogo do `modelo-operacional.md`
§6. Diário: `[7]`.

## 7. Fontes

- M. Nygard — *Documenting Architecture Decisions* (ADR): https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- Simon Brown — *C4 model*: https://c4model.com/
- L. Mezzalira — *Documenting software architecture* (docs-as-code / living documentation): https://lucamezzalira.medium.com/how-to-document-software-architecture-techniques-and-best-practices-2556b1915850
- `docs/governance/modelo-operacional.md` §6; Constituição (Princípio VII, jornadas vivas).
