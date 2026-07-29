# Skills do Maestro (padrão agentskills.io)

Skill = procedimento recorrente empacotado como `skills/<slug>/SKILL.md` — frontmatter
`name` + `description` (com **gatilho** "Use quando…") + corpo em passos. Dispara sozinha no
contexto certo, padronizando a execução sem depender da memória do humano.

**Regra de nascimento (YAGNI):** uma skill só existe a partir de **dor recorrente comprovada**
(retro/ciclos), nunca especulativa. Autor: agente `skill-author`.

## Catálogo (V0 — spec 005)

| Skill | Para quê | Nasce da dor | Consumida por |
|---|---|---|---|
| [`constitution-check`](./constitution-check/SKILL.md) | Tabela Princípios I–VII no `plan.md` | Refeita à mão em 003/004 | `plan-arquiteto`, `guardiao-processo` |
| [`dod-verificavel`](./dod-verificavel/SKILL.md) | Critério de aceite → fitness function (grep/ls/teste) | Checks reescritos iguais a cada ciclo | `spec-agent`, `qa`, comando `/dod` |
| [`combater-amontoado`](./combater-amontoado/SKILL.md) | Revisão didática (anti-"amontoado") | Feedback do Steward sobre docs densos | `didatica-editor`, `tech-writer` |

## Skills vs. comandos vs. agentes

- **Skill** (`skills/*/SKILL.md`) — *como fazer* um procedimento; dispara pelo contexto.
- **Comando** (`.claude/commands/*.md`) — invocação explícita (`/dod`, `/speckit.*`).
- **Agente** (`.claude/agents/*.md`) — *quem faz*; consome skills e comandos.

Ex.: a skill `dod-verificavel` ajuda a **escrever** os checks; o comando `/dod` os **roda**.

## Próximas (por retro, não especulação)

Candidatas quando a dor aparecer: `preparar-pr`, `abrir-ciclo`. Fase 3 traz workflows/scripts
(incl. `promote-main.sh`).
