# Capítulo 03 — Desenvolvimento dirigido por especificação (elemento `[2]`)

> A keystone da mecânica: **a spec é a fonte de verdade, não o código nem o prompt.**

## 1. Pergunta central

No mundo tradicional, a fonte de verdade é o código — a spec e a doc *apodrecem*. O
Spec-Driven inverte isso. **O que muda, quando é o agente que escreve, que faz a spec
parar de apodrecer e passar a ser mais confiável que o código?**

## 2. Fundamentação teórica

**Inversão de dependência.** Em desenvolvimento tradicional a doc *descreve* o código
(está a jusante → apodrece). No Spec-Driven a spec é o **input que gera** o código: se
você quer código novo, precisa mudar a spec primeiro. A obsolescência deixa de ser
opcional e passa a quebrar a geração — a spec vira "verdade executável".

Fluxo: `specify → clarify → plan → tasks → implement`. A spec descreve **o quê e por
quê** (valor, critérios de aceite testáveis); o plan descreve **como**. Prompt vago
"força o modelo a adivinhar milhares de requisitos não ditos".

**Nem toda mudança merece uma spec.** O valor de uma spec escala com
**ambiguidade × raio de impacto × irreversibilidade**. Quando os três são baixos, a spec
é cerimônia de papel (YAGNI). Daí as **raias** (`modelo-operacional.md` §3).

## 3. Frameworks / abordagens avaliados

| Ferramenta | Modelo | Veredito |
|---|---|---|
| **GitHub Spec Kit** | 1 spec/feature; fases com gate; cross-feature forte | **Adotado** — base do fluxo; casa com constituição + specs numeradas |
| **OpenSpec** (Fission-AI) | *Delta* (`Propose→Apply→Archive`); leve; sem Python | **Descartado como 2ª ferramenta** — a ideia do delta foi absorvida como raia leve |
| **Kiro / Tessl / "specs as source of truth"** | Variações de SDD assistido | **Observados** — mesmo princípio; sem adoção |
| **Prompt ad-hoc** | Sem spec | **Rejeitado** — produz código que compila e erra a intenção |

## 4. Recomendação de utilização (1 humano + N agentes)

- **Uma ferramenta SDD só (Spec Kit).** A raia leve (modelo delta) mora dentro dela.
- **Três raias**: leve (bug/typo — o PR é o artefato, bug exige teste que reproduz),
  plena (feature/contrato — Spec Kit completo), infra (sempre plena + gates de
  reversibilidade).
- Regra de desempate: **na dúvida, é plena; infra/migração nunca são leves.**

## 5. Conexões

- **`[3]`/`[4]`** — a spec é o **contexto integrador** que sobrevive ao `/clear` e cruza
  toda fronteira de subagente (antídoto ao ótimo local).
- **DDD/hexagonal** — dá as fronteiras (bounded contexts) onde a spec corta o trabalho.
- **`[8]` DoR** — "spec pronta" é a Definition of Ready.

## 6. Insight da jornada e impacto no modelo

"Documentação atualizada" era o *sintoma*; a causa é a **inversão de dependência**.
A crítica "bug dá pra simplificar" + a avaliação do OpenSpec **produziram mudança
normativa real**: `modelo-operacional.md` **v1.1.0** (§3 raias; spec de infra com gates)
+ **ADR 0005**. Diário: `[2]`.

## 7. Fontes

- GitHub Blog — *Spec-driven development with AI* (2025-09): https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/
- GitHub Spec Kit: https://github.com/github/spec-kit
- OpenSpec (Fission-AI): https://github.com/Fission-AI/OpenSpec
- Spec Kit vs OpenSpec: https://intent-driven.dev/knowledge/spec-kit-vs-openspec/
