# Skills do Maestro (padrão agentskills.io)

Skill = procedimento recorrente empacotado como `skills/<slug>/SKILL.md` — frontmatter
`name` + `description` (com **gatilho** "Use quando…") + corpo em passos. Dispara sozinha no
contexto certo, padronizando a execução sem depender da memória do humano.

**Regra de nascimento (YAGNI + TDD):** uma skill só existe a partir de **dor recorrente
comprovada** (retro/ciclos), nunca especulativa — e skill original nova só publica com
**baseline testado** (cenário de pressão: agente falha SEM a skill, cumpre COM ela — ver
protocolo no `skill-author`). Toda skill carrega sua **Iron Law** (a regra inegociável,
com brechas fechadas). Autor: agente `skill-author`.

## Catálogo (V0 — spec 005)

| Skill | Para quê | Nasce da dor | Consumida por |
|---|---|---|---|
| [`constitution-check`](./constitution-check/SKILL.md) | Tabela Princípios I–VII no `plan.md` | Refeita à mão em 003/004 | `plan-arquiteto`, `guardiao-processo` |
| [`dod-verificavel`](./dod-verificavel/SKILL.md) | Critério de aceite → fitness function (grep/ls/teste) | Checks reescritos iguais a cada ciclo | `spec-agent`, `qa`, comando `/dod` |
| [`combater-amontoado`](./combater-amontoado/SKILL.md) | Revisão didática (anti-"amontoado") | Feedback do Steward sobre docs densos | `didatica-editor`, `tech-writer` |
| [`anti-padroes`](./anti-padroes/SKILL.md) | Catálogo do que NÃO fazer (contexto, orquestração, qualidade, processo) | Retros 001–008 + estudo maestro-02 (spec 008) | todos os agentes; `review`, `guardiao-processo` |
| [`diagnostico-antes-do-fix`](./diagnostico-antes-do-fix/SKILL.md) | Causa raiz antes de qualquer correção (Iron Law + 6 fases) | Estudo Superpowers (spec 011) — lacuna real de disciplina de debugging | `dev-implementador`, `qa` |
| [`jornada-viva`](./jornada-viva/SKILL.md) | Doc + capturas do build real + heurística **datada**, no mesmo PR | Lacuna do ciclo 018: o modelo prescrevia journey doc sem skill nem template | `qa`, `tech-writer`, `ux-semantica` |

## Skills vs. comandos vs. agentes

- **Skill** (`skills/*/SKILL.md`) — *como fazer* um procedimento; dispara pelo contexto.
- **Comando** (`.claude/commands/*.md`) — invocação explícita (`/dod`, `/speckit.*`).
- **Agente** (`.claude/agents/*.md`) — *quem faz*; consome skills e comandos.

Ex.: a skill `dod-verificavel` ajuda a **escrever** os checks; o comando `/dod` os **roda**.

## Próximas (por retro, não especulação)

Candidatas quando a dor aparecer: `preparar-pr`, `abrir-ciclo`. Fase 3 traz workflows/scripts
(incl. `promote-main.sh`).
