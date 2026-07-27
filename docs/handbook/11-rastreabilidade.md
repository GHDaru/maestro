# Capítulo 11 — Rastreabilidade spec↔PR↔testes↔journey (elemento `[11]`)

> Não é burocracia: é a **memória de longo prazo** do projeto — o porquê e o quê, sem
> re-derivar — e **emerge** do workflow, sem ferramenta pesada.

## 1. Pergunta central

Daqui a 3 meses um teste quebra e o **agente tem memória zero**. **O que a rastreabilidade
te dá nesse momento — e como tê-la sem uma matriz de compliance que ninguém lê?**

## 2. Fundamentação teórica

Rastreabilidade devolve **o quê** (o que foi construído, o que o verifica) e **o porquê**
(a decisão e o racional) **sem re-derivar**.

**Por que é load-bearing em solo+IA:** o agente **reseta** o contexto (`[3]`). Os artefatos
ligados são a **única memória durável** — a rastreabilidade é o que reconstrói intenção +
verificação depois do reset.

**Dois sentidos:**
- **para frente**: spec → foi construída? está verificada? (cobertura de intenção);
- **para trás**: sintoma → qual código → qual spec → por quê — que é **recuperação rápida**
  (a métrica de estabilidade do `[10]`).

**Emergente, não um sistema.** Você não constrói uma ferramenta de rastreabilidade; o elo
**emerge** de cada artefato referenciar o próximo — spec `NNN` → PR cita a spec → teste
nomeia o requisito → journey no mesmo PR → ADR para a decisão. A **DoD (`[8]`) força o
elo**. É subproduto do workflow, não atividade separada.

## 3. Frameworks / abordagens avaliados

| Abordagem | O que oferece | Veredito |
|---|---|---|
| **Matriz de rastreabilidade de requisitos** | Rastreio formal req↔teste | **Rejeitado** — ferramenta pesada; matriz que ninguém mantém |
| **Linking nativo issue↔commit↔PR** (GitHub) | Elo barato no fluxo | **Adotado** — spec NNN e PR se referenciam |
| **ADR ligado a componentes/C4** | Decisão → sistema | **Parcial** — ADR sim; C4 é Fase 2 |
| **docs-as-code (cross-refs)** | Links versionados | **Adotado** — journey/ADR/spec se citam |

## 4. Recomendação de utilização (1 humano + N agentes)

- **Elo obrigatório na DoD**: `spec NNN ↔ PR ↔ testes ↔ journey` explícito.
- **Convenção de referência** (a spec numera; o PR cita; o teste nomeia o requisito; o
  ADR registra a decisão) — sem matriz, sem ferramenta.
- Otimizar o **sentido para trás** (sintoma → causa) — é o que acelera a recuperação.

## 5. Conexões

- **`[3]`** — os artefatos ligados são a memória que sobrevive ao reset de contexto.
- **`[8]`** — a DoD carrega e força o elo de rastreabilidade.
- **`[10]`** — o sentido "para trás" é a recuperação rápida (estabilidade).
- **`[7]` / `[12]`** — artefatos consumidos + ADR imutável = a trilha de decisões.

## 6. Insight da jornada e impacto no modelo

Insight do aprendiz: a rastreabilidade dá **"o porquê e o quê"** sem re-derivar; em solo+IA
os artefatos ligados **são a memória** do projeto. Fundamenta o §8 (rastreabilidade) e a
DoD (§7) do `modelo-operacional.md`. Diário: `[11]`.

## 7. Fontes

- DORA — *four keys* (recuperação = trilha do sintoma à causa): https://dora.dev/guides/dora-metrics-four-keys/
- L. Mezzalira — *Documenting software architecture* (docs-as-code, cross-refs): https://lucamezzalira.medium.com/how-to-document-software-architecture-techniques-and-best-practices-2556b1915850
- `docs/governance/modelo-operacional.md` §8–§9.
