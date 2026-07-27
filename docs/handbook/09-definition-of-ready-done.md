# Capítulo 09 — Definition of Ready / Done (elemento `[8]`)

> A DoD **é** o gate. Um gate barato é **verificável autonomamente** — mas verde ≠ certo.

## 1. Pergunta central

Baratear os gates é como se escapa do gargalo humano (`[6]`). **Que propriedade um critério
de "done" precisa ter para um agente satisfazê-lo e um hook conferi-lo sem depender de
você — e o que ele, mesmo verde, ainda não garante?**

## 2. Fundamentação teórica

**A propriedade: verificável autonomamente.** Um critério de "done" precisa produzir um
**pass/fail objetivo** que o agente gera e um hook confere — "prove, não declare" (`[1]`)
virado em máquina. *"Código limpo"* não é DoD (subjetivo); *"testes verdes + lint + revisão
sem lacunas de correção"* é.

**O trabalho é converter julgamento em check** (harness design — ADR 0001):
- "código limpo" → lint + fitness functions + limite de complexidade;
- "boa UX" → tokens do design system + checklist heurístico;
- "seguro" → secret scanning + revisão de injeção/autorização.

**DoR** é a mesma ideia a montante: "pronto para começar" = a spec/plan é completa o
bastante para o agente executar **sem adivinhar** (critérios testáveis, ambiguidades
resolvidas, Constitution Check, apetite definido).

**Necessária, não suficiente.** Uma DoD verde garante a **peça local** — não garante:
- **(a) coerência global**: a jornada/todo ainda funciona e não regrediu (o **ótimo local**
  do `[4]` no nível da qualidade);
- **(b) a coisa certa**: verde não conserta requisito/spec errado.
O modelo trata (a) puxando o global para dentro da DoD (journey, e2e, rastreabilidade
`[11]`) + checkpoint humano; (b) fica com o **humano (o A do `[5]`)**.

## 3. Frameworks / abordagens avaliados

| Abordagem | O que oferece | Veredito |
|---|---|---|
| **DoR / DoD** (Scrum/Kanban) | Portões de entrada/saída | **Adotado** — como **checklists verificáveis** (§7 do modelo) |
| **Testing trophy** (mais integração) vs **test pyramid** (mais unitário) | Onde investir teste | **Trophy-leaning** — integração por rota + contrato por porta pegam o "todo" melhor que só unitário |
| **TDD / BDD** | Teste antes; critério em linguagem de negócio | **Adotado** — bug exige teste que reproduz; caso de uso tem feliz + falha |
| **Quality gates no CI + DevSecOps leve** | Bloqueio automático | **Adotado** — fitness functions, lint/typecheck, secret scanning |
| **Cobertura como meta numérica** | % de linhas | **Rejeitado** — gaméavel; usamos "feliz + falha por caso de uso" |

## 4. Recomendação de utilização (1 humano + N agentes)

- **DoR e DoD como checklists verificáveis** (`modelo-operacional.md` §7), fecháveis por
  Stop-hook/`/goal`.
- **DoD reduzida na raia leve**; **bloco de reversibilidade** na raia infra.
- **Puxar o global para a DoD**: journey atualizada + e2e + rastreabilidade spec↔journey.
- **O humano guarda o irredutível**: coerência global no checkpoint e "é a coisa certa".

## 5. Conexões

- **`[1]`** — "prove, não declare" é a raiz da DoD verificável.
- **`[5]`** — o humano é Accountable pelos **critérios**; a DoD é onde eles viram check.
- **`[6]`** — DoD verificável = gate barato = fuga do gargalo humano.
- **`[4]` / `[11]`** — verde local ≠ todo correto; rastreabilidade/journey puxam o global.

## 6. Insight da jornada e impacto no modelo

Insights do aprendiz: **"verificável autonomamente"** e **"a peça é local — ainda é preciso
ver se atendeu o requisito da jornada / não comprometeu o conjunto maior"** (o ótimo local
reaparecendo). Fundamenta a DoR/DoD do `modelo-operacional.md` §7. Diário: `[8]`.

## 7. Fontes

- Claude Code — *Best practices* (dê ao agente um check que ele rode; verificação como gate): https://code.claude.com/docs/en/best-practices
- DORA — *four keys* (testes/CI como capacidades): https://dora.dev/guides/dora-metrics-four-keys/
- Kent C. Dodds — *The Testing Trophy* (conceito; ênfase em integração).
- `docs/governance/modelo-operacional.md` §7; ADR 0001 (harness design).
