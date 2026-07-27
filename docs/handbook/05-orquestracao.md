# Capítulo 05 — Padrões de orquestração de agentes (elemento `[4]`)

> Como coordenar subagentes sem cair em ótimo local: **map-reduce cognitivo** ao longo
> do espectro **workflow ↔ agent**.

## 1. Pergunta central

Cinco subagentes devolvem cinco fatias, cada um com a spec em mãos. Elas não se encaixam
sozinhas. **O que precisa acontecer depois — e quem, estruturalmente, faz isso?**

## 2. Fundamentação teórica

A peça que falta depois do *map* (workers em paralelo) é o **reduce cognitivo**:
reconciliar as fatias (contratos, coerência com a spec). Não é `cat fatia1 fatia2` — é
*julgamento*, e só pode ser feito por quem tem o **contexto global**: o **orquestrador**.
Padrão: **orchestrator-workers**.

**O corte é mais traiçoeiro que o reduce.** O map-reduce clássico assume splits
independentes; em código quase nunca são (porta e adaptador dividem um contrato). Se você
corta nas **costuras erradas**, nenhum reduce salva. As costuras certas são os **bounded
contexts** (DDD) — cortar ao longo das fronteiras arquiteturais é o que torna a
paralelização segura.

**Espectro workflow ↔ agent.** *Workflow* = você fixa o caminho (previsível, foco,
sinergia). *Agent* = o LLM decide o corte na hora (flexível, mas pode errar o corte —
ótimo local — e varia). Regra de ouro: **use a menor autonomia que resolve** ("comece
simples; adicione autonomia só quando o simples comprovadamente falha").

## 3. Frameworks / abordagens avaliados

| Padrão | O que é | Tipo | Onde vive no modelo |
|---|---|---|---|
| **Prompt chaining** | passos fixos em sequência | workflow | fluxo Spec Kit `specify→…→implement` |
| **Routing** | classifica a entrada → handler certo | workflow | as **raias** (§3) |
| **Parallelization** | fatias independentes / N tentativas (voting) | workflow | subagentes por bounded context |
| **Orchestrator-workers** | corte dinâmico + reduce | agent | papel **Orquestrador** (§4) |
| **Evaluator-optimizer** | gera → crítica → refina | workflow c/ loop | Writer/Reviewer + `/code-review` |
| **Autonomous** | LLM aberto + guarda-corpos | agent | **evitado** (YAGNI; exige guardrails pesados) |

## 4. Recomendação de utilização (1 humano + N agentes)

- **Default é workflow** (chaining/routing/parallel) — barato, previsível, depurável.
- **Parallelize por bounded context**; o **Orquestrador (humano)** faz o reduce.
- Suba para orchestrator-workers/autonomous **só** quando o corte genuinamente não pode
  ser predefinido.
- **Melhor arquitetura → mais tempo no lado barato do espectro.** Boas fronteiras compram
  previsibilidade.

## 5. Conexões

- **`[3]`** — resolve o *ótimo local* deixado em aberto pelo fluxo agentic.
- **`[2]` / DDD** — as fronteiras onde se corta; a spec como norte de cada worker.
- **`[1]`** — evaluator-optimizer é o revisor independente institucionalizado.

## 6. Insight da jornada e impacto no modelo

Analogia do aprendiz: **"map-reduce, mas cognitivo"**; e o insight de que **fixar o
corte** reduz escopo e ganha sinergia (workflow > agent quando o corte é conhecido). Sem
impacto normativo direto; mapeia os padrões sobre papéis/raias já existentes. Diário: `[4]`.

## 7. Fontes

- Anthropic — *Building effective agents* (workflow×agent; 6 padrões; menor autonomia): https://www.anthropic.com/engineering/building-effective-agents
- Claude Code — *Best practices* (subagentes, fan-out, Writer/Reviewer): https://code.claude.com/docs/en/best-practices
