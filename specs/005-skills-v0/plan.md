# Plan 005 — Skills V0

- **Spec**: `spec.md` · **Raia**: Plena · **Data**: 2026-07-29

## Constitution Check (principios-maestro.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven | ✅ nasce da spec 005 |
| II. Orquestração humano-governada | ✅ skill padroniza execução; humano ainda decide/aprova |
| III. Reversibilidade / gates de risco | ✅ skills são guias em texto — reversíveis; não executam sozinhas |
| IV. Test-First / DoD verificável | ✅ DoD por grep (frontmatter/gatilho/referência) |
| V. Economia de contexto / fronteira | ✅ cada skill é estreita, dispara só no seu contexto |
| VI. Artefatos vivos | ✅ `skills/README.md` liga skill ↔ agente/comando |
| VII. Governança leve / YAGNI | ✅ só as 3 de dor comprovada; nada especulativo |

**Sem violações.**

## Como

- Padrão agentskills.io: `skills/<slug>/SKILL.md`, frontmatter `name` + `description`
  (com gatilho "Use quando…"), corpo em passos + 1 exemplo concreto.
- 3 slugs: `constitution-check`, `dod-verificavel`, `combater-amontoado`.
- **Não duplicar `/dod`**: a skill `dod-verificavel` é *design-time* (escrever os checks);
  o comando `/dod` é *run-time* (executar). A skill referencia o comando.
- Cada skill aponta para o agente que a consome (constitution-check → plan-arquiteto/guardião;
  dod-verificavel → spec-agent/qa; combater-amontoado → didatica-editor/tech-writer).
- Índice `skills/README.md`.

## Verificação (DoD)

- `ls skills/*/SKILL.md | wc -l` = 3.
- `grep -L "^name:" skills/*/SKILL.md` vazio; idem `^description:`.
- `grep -il "use quando" skills/*/SKILL.md` = 3 (todo description tem gatilho).
- `grep -l "/dod" skills/dod-verificavel/SKILL.md` não-vazio.
