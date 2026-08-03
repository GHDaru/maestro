# Constituição — Maestro (para o Spec Kit)

> A constituição **completa** da metodologia vive em
> [`docs/governance/principles.md`](../../docs/governance/principles.md)
> (fonte de verdade, humana). Este arquivo é o ponto de entrada que o Spec Kit lê no
> **Constitution Check** de cada `plan.md`. Mantê-los em sincronia; emendas via
> `/speckit.constitution` + ADR + bump de versão.
>
> **Version**: 1.0.0 · **Ratified**: 2026-07-22 · **Last Amended**: 2026-07-22

## Princípios (resumo — texto completo em principles.md)

- **I. Spec-Driven** — a spec é a fonte de verdade (input que gera código, não descrição).
- **II. Orquestração humano-governada (1 rege N)** — RACI; Accountable humano pela política.
- **III. Reversibilidade e gates proporcionais ao risco (NON-NEGOTIABLE)** — gate ∝
  irreversibilidade × impacto; reversibilidade rebaixa a classe.
- **IV. Test-First e DoD verificável** — "prove, não declare"; converter julgamento em check.
- **V. Economia de contexto e corte por fronteira** — preservar a spec; paralelizar por
  bounded context; menor autonomia que resolve.
- **VI. Artefatos vivos e rastreabilidade** — input consumido com forcing function (ou
  imutável); spec ↔ PR ↔ testes ↔ journey.
- **VII. Governança leve (YAGNI)** — aprende sem inchar; retro → regra; poda o que não paga.

## Constitution Check (usar no plan.md)

Todo `plan.md` declara conformidade com I–VII. Violação → justificada por escrito na seção
Complexity Tracking, ou o plano é reformulado. Complexidade além do necessário é removida.
