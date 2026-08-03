---
description: Compara o estado real do repositório com a spec/plan/tasks do ciclo ativo e ANEXA o trabalho faltante como tasks novas — para o implement poder terminar.
---

<!-- Vendorizado do fork GHDaru/spec-kit@0117a7b (templates/commands/converge.md),
     adaptado ao Maestro: sem extension hooks (YAGNI), formato de tasks da casa. -->

Entrada do usuário (opcional — pode indicar o ciclo `NNN` ou uma área de foco):

```text
$ARGUMENTS
```

## O que fazer

1. **Localize o ciclo ativo**: o maior `specs/NNN-*/` com `tasks.md` (ou o indicado no
   argumento). Leia `spec.md`, `plan.md` e `tasks.md`.
2. **Inspecione o estado real** dos artefatos que a spec promete (arquivos, testes,
   docs, scripts) — rode os checks do `plan.md § Verificação` quando existirem e
   **mostre a evidência** de cada um (prove, não declare).
3. **Compare**: para cada FR e critério do DoD, classifique — ✅ feito e verificado ·
   ⚠️ feito mas sem verificação · ❌ não feito.
4. **Convirja**: para cada ⚠️/❌, **anexe** uma task nova ao `tasks.md` (seção
   `## Convergência (adicionadas em [data])`), numerada em sequência, com o check que a
   prova. **Nunca** reescreva ou desmarque tasks existentes (histórico é histórico).
5. **Reporte**: tabela FR → estado → task criada (se houver). Se tudo ✅, diga
   explicitamente que o ciclo está convergido e pronto para o gate.

## Regras

- Escopo é o da spec — trabalho novo descoberto que **não** está na spec vira nota de
  clarify/registro, não task silenciosa (anti-padrão 10: mudança silenciosa de escopo).
- Raia infra: confirme também os gates de reversibilidade (backup/dry-run/rollback).
- Handoff: → `dev-implementer` (tasks novas) ou → gate humano (se convergido).
