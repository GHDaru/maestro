# Capítulo 12 — Governança leve (elemento `[12]`)

> Como o próprio sistema evolui e se mantém coerente — **aprendendo sem inchar**.
> A camada meta que fecha a jornada.

## 1. Pergunta central

Você tem um sistema de regras que **cresce** (constituição, ADRs, modelo versionado).
**Qual é o modo de falha de um sistema de regras que cresce — e que força o combate?**

## 2. Fundamentação teórica

**Modo de falha: bloat / ossificação.** Regras acumulam, ninguém poda, e o conjunto vira
o **processo pesado que a gente cortou** lá no começo.

**A força contrária: YAGNI + poda + flexibilidade.** A governança precisa de duas forças
opostas equilibradas:
- **aprender** (adicionar regra) — via retro → ADR → nova versão;
- **ficar lean** (remover/não adicionar) — via YAGNI e poda do que não paga.

A Constituição já carrega essa poda: *"complexidade além do necessário DEVE ser
justificada por escrito ou removida (YAGNI)."*

**A arquitetura que dá flexibilidade: camadas com velocidades diferentes.**
- **Núcleo firme** — a **Constituição** (princípios) muda devagar, por emenda versionada
  com Sync Impact Report;
- **Periferia evoluível** — **modelo operacional + handbook**, com **versão própria**,
  mudam rápido (por isso ancorados como *extensão subordinada* — Constituição v1.4.0);
- **Memória append-only** — **ADRs** imutáveis (`[7]`): o log de decisões que não apodrece;
- **Loop de aprendizado** — retro → regra versionada (`[6]`).

**Governança aplica os próprios princípios a si mesma:** é versionada, emendada sob gate
humano (`[9]`), registrada em ADR (`[7]`) e podada por YAGNI. E os ADRs, sendo imutáveis
mas **substituíveis** (um novo ADR pode superar outro), dão à decisão a mesma
**reversibilidade** do `[1]`: nada fica preso, tudo é rastreável.

## 3. Frameworks / abordagens avaliados

| Abordagem | O que oferece | Veredito |
|---|---|---|
| **Constituição versionada** (spec-kit) | Fonte de verdade + emenda disciplinada | **Adotado** — núcleo firme |
| **ADR** (Nygard) | Log imutável de decisões + racional | **Adotado** — memória de governança |
| **Working agreements / handbook** | Convenções evoluíveis | **Adotado** — periferia rápida (este handbook) |
| **RFC process pesado** | Revisão formal ampla | **Rejeitado** — ADR cobre; YAGNI |
| **Governança "adicionar sempre"** | Mais regras = mais controle | **Rejeitado** — leva a bloat/ossificação |

## 4. Recomendação de utilização (1 humano + N agentes)

- **Constituição firme em princípios**; modelo/handbook **evoluíveis e subordinados**.
- **ADR para toda decisão** que muda o sistema (imutável; superável por outro ADR).
- **Emenda via retro** (erro recorrente → regra); **poda via YAGNI** (regra que não paga
  sai).
- **Revisão obrigatória ao fim de cada fase** do projeto.

## 5. Conexões

- É a **meta-camada** de todos os elementos.
- **`[6]`** — a retro é o motor de emenda; **`[7]`** — ADR é a memória imutável;
  **`[9]`** — emenda é human-gated; **`[1]`** — ADR superável = reversibilidade da decisão.

## 6. Insight da jornada e impacto no modelo

Insights do aprendiz: **bloat/ossificação** é o risco; **YAGNI + poda + flexibilidade** é a
força; governança precisa ser flexível para evoluir. **Meta**: esta própria jornada de
aprendizado foi o `[12]` em ação — crítica → refino do modelo → ADR 0005 → versão v1.1.0 →
ancoragem na Constituição v1.4.0. Diário: `[12]`.

## 7. Fontes

- M. Nygard — *Documenting Architecture Decisions*: https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- GitHub Spec Kit (constituição versionada): https://github.com/github/spec-kit
- `.specify/memory/constitution.md` (Governance); `docs/adr/`; `docs/governance/modelo-operacional.md` §10–§11.
