# Plan 011 — Absorções do Superpowers

- **Spec**: `spec.md` · **Raia**: Plena · **Data**: 2026-07-31

## Constitution Check (principios-maestro.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven | ✅ nasce da spec 011; vereditos aprovados em gate registrado |
| II. Orquestração humano-governada | ✅ Iron Laws endurecem execução, não decisão — gates humanos intactos |
| III. Reversibilidade / gates de risco | ✅ mudanças textuais em skills/templates — reversíveis por git |
| IV. Test-First / DoD verificável | ✅ **é o tema do ciclo**: skills testadas (baseline) + DoD por grep |
| V. Economia de contexto / fronteira | ✅ task autossuficiente = subagente sem herança de contexto |
| VI. Artefatos vivos | ✅ Apêndice B anotado como incorporado; CHANGELOG |
| VII. Governança leve / YAGNI | ✅ 5 absorções aprovadas, nada além; worktrees segue observar |

**Sem violações.**

## Como

- **FR1**: bloco `## Iron Law` no topo de cada skill (após frontmatter/título), com a
  lei em código + a fórmula "violar a letra é violar o espírito" + 2–3 brechas fechadas
  ("isso NÃO é desculpa: ..."). Leis curtas, memoráveis.
- **FR2**: seção "Protocolo (TDD para skills)" no `skill-author.md`; `skills/README.md`
  ganha a regra: skill original nova só publica com baseline RED registrado.
- **FR3**: skill `diagnostico-antes-do-fix` no padrão da casa + Iron Law; fases:
  ler erro de verdade → reproduzir → isolar (bissecção/logs) → hipótese única →
  teste que prova → só então fix. Consumida por `dev-implementador` e `qa`.
- **FR4**: `comunicacao.md` — mensagem de checkpoint por task (o que fecha, evidência,
  próximo); `dev-implementador.md` — "em ciclo >3 tasks, pare no checkpoint".
- **FR5/FR6**: 1 linha no tasks-template; parágrafo "Skills primeiro" no CLAUDE.md.

## Verificação (DoD)

- `grep -L "Iron Law" skills/*/SKILL.md` → vazio · `ls skills/*/SKILL.md | wc -l` = 5.
- greps: `baseline` no skill-author · `checkpoint` em comunicacao+dev · `zero contexto`
  no tasks-template · enforcement no CLAUDE.md.
