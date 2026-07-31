# Capítulo 04 — Fluxo agentic e economia de contexto (elemento `[3]`)

> Como o trabalho roda: **explore → plan → code → commit**, subagentes, `/clear` e
> revisor em contexto fresco — quatro peças, uma restrição.

## 1. Pergunta central

O fluxo agentic tem quatro peças que *parecem* boas práticas soltas. **Qual restrição
física única elas estão todas contornando?**

## 2. Fundamentação teórica

A janela de contexto do agente é **finita**, e a performance **degrada à medida que ela
enche** — o agente "esquece" instruções antigas e erra mais. O inimigo não é a *falta*
de contexto; é o **acúmulo** (becos sem saída, arquivos irrelevantes) que afoga o sinal.

As quatro peças são, todas, **economia de contexto**:

| Peça | O que faz com o contexto |
|---|---|
| explore→**plan**→code | o *plan* **comprime** a exploração no essencial |
| **subagentes** | leem em janela separada; só volta o resumo — o principal fica magro |
| **`/clear`** | despeja ruído entre tarefas não relacionadas |
| **revisor fresco** | não contaminado pelos becos sem saída; vê só diff + critério |

**Limite (não exagerar):** resetar demais esquece o básico; delegar demais leva o
subagente ao **ótimo local** (otimiza a fatia, quebra o todo). Disciplina madura:
**preserve o contexto que sustenta (load-bearing), descarte só o ruído.** O contexto
integrador é a **spec/plan** (`[2]`).

## 3. Frameworks / abordagens avaliados

| Padrão/prática | O que oferece | Veredito |
|---|---|---|
| **explore-plan-code-commit** (Claude Code) | Separa pesquisa de execução → não resolve o problema errado | **Adotado** (raia plena) |
| **Writer/Reviewer** (contexto fresco) | Revisor sem viés de quem escreveu | **Adotado** — é a revisão independente da DoD |
| **Subagentes** | Investigação/verificação em janela isolada | **Adotado** — cortados por bounded context |
| **Revisão adversarial do diff** | Modelo fresco tenta refutar antes do "pronto" | **Adotado** — `/code-review` como gate |
| **`/clear` / compactação** | Reset de contexto entre tarefas | **Adotado** — higiene de contexto |

## 4. Recomendação de utilização (1 humano + N agentes)

- **Plan comprime** a exploração antes de implementar (raia plena).
- **Subagentes por bounded context**, cada um recebendo a spec (contexto integrador).
- **Revisão independente em contexto fresco** é item obrigatório da DoD (todas as raias).
- Preservar o load-bearing (objetivo, invariantes, contratos); descartar o ruído.

## 5. Conexões

- **`[2]`** — mesma espinha: a spec é o que sobrevive ao reset e cruza fronteiras.
- **`[4]`** — o ótimo local abre a necessidade de orquestração (reduce + corte por costura).
- **`[1]`** — checkpoint/rewind é a reversibilidade aplicada ao contexto.

## 6. Insight da jornada e impacto no modelo

Do "falta de contexto" ao **acúmulo/foco**; das 4 peças a **uma ideia (economia de
contexto)**; do "delegar" ao **ótimo local**. Confirmou decisões que já estavam no
modelo (`/clear` entre tarefas, revisão em contexto fresco no §4) — o aprendiz codificou
o *quê* antes de entender o *porquê*. Diário: `[3]`.

## 6b. Economia de contexto medida

"Cada agente estreito" (Princípio V) deixa de ser afirmação e vira **número**: ao fatiar
contexto para um agente/task, estime os tokens do recorte vs. do contexto integral e
reporte a economia (% poupado). Prática mínima: o orquestrador anota a estimativa ao
montar contexto grande — se a economia é consistentemente baixa, o **corte de fronteira
está errado** (sinal de revisar o plan, não de aumentar o contexto). Origem: estudo do
`maestro-02` (Apêndice A, context-slicer), incorporado na spec 008.

## 7. Fontes

- Claude Code — *Best practices* (economia de contexto, subagentes, revisão adversarial): https://code.claude.com/docs/en/best-practices
- Anthropic — *Building effective agents*: https://www.anthropic.com/engineering/building-effective-agents
