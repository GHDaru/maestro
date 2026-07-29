# QA-report 005 — Skills V0

- **Data**: 2026-07-29 · **Raia**: Plena · **Veredito**: ✅ CONFORME

## Fitness functions (DoD)

| Check | Esperado | Resultado |
|---|---|---|
| `ls skills/*/SKILL.md \| wc -l` | 3 | **3** ✅ |
| `grep -L "^name:" skills/*/SKILL.md` | vazio | vazio ✅ |
| `grep -L "^description:" skills/*/SKILL.md` | vazio | vazio ✅ |
| `grep -il "use quando" ... \| wc -l` (gatilho) | 3 | 3 ✅ |
| `grep -l "/dod" dod-verificavel` (complementaridade) | não-vazio | ok ✅ |

## Cobertura dos requisitos

- **FR1–FR3** (3 skills de dor comprovada): ✅ T1–T3.
- **FR4** (frontmatter + gatilho + exemplo): ✅.
- **FR5** (`skills/README.md`): ✅ T4.
- **Não-duplicação com `/dod`**: skill = design-time (escrever); comando = run-time (rodar);
  a skill referencia o comando. ✅

## Estado da Fase 2

3 skills no ar (constitution-check, dod-verificavel, combater-amontoado), cada uma ligada ao
agente/comando que a consome. Próximas skills só por retro (YAGNI).
Próximo no roadmap: Fase 3 — Workflows/Scripts (incl. `promote-main.sh`).

## Pendência de gate

- **T5**: promoção `dev → main` aguarda aprovação humana (indelegável).
