---
description: Roda a Definition of Done verificável (testes, fitness functions, typecheck/build) e mostra a evidência antes de dar uma feature por pronta.
---

Execute a **Definition of Done verificável** (modelo operacional §7) e **mostre a
evidência** de cada check — nunca afirme sucesso sem output ("prove, não declare").

Rode e reporte o resultado de cada item:

1. **Web** (em `apps/web`): `pnpm test` (inclui as fitness functions `architecture.test.ts`) e `pnpm build` (typecheck + build).
2. **API** (em `apps/api`): `uv run pytest` e `uv run lint-imports` (contratos de arquitetura).
3. **Segredos**: verifique que nenhum segredo/token foi commitado no diff.
4. **Rastreabilidade** (§9): confirme o elo `spec NNN ↔ PR ↔ testes ↔ journey`.
5. **CHANGELOG**: confirme uma entrada em `[Unreleased]` no `CHANGELOG.md` (ou raia leve com label `skip-changelog`).
6. **Docs vivas**: journey atualizada (se tocou jornada) e ADR se houve decisão.

Para cada item que **passa**, mostre o comando e o resultado. Para cada item que
**falha**, mostre o output e o que corrigir.

**Lembrete (§8):** verde local ≠ certo global. Sinalize explicitamente se a jornada ou o
conjunto maior pode ter sido comprometido — essa avaliação e o "é a coisa certa" ficam
com o humano (o Accountable, §4).
