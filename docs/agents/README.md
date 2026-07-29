# Agentes do Maestro — perfil ↔ executável

Cada especialista de IA existe em **duas formas**, mantidas em sincronia:

- **Perfil** (fonte humana, legível): [`perfis.md`](./perfis.md) — o quê faz / não faz,
  produz, consome, handoff. É onde se **discute** o papel.
- **Executável** (subagente do Claude Code): `.claude/agents/<slug>.md` — frontmatter
  (`name`, `description`, `tools`) + system prompt estreito. É o que o Orquestrador **invoca**.

O padrão de mensagens entre eles está em [`comunicacao.md`](./comunicacao.md).

## Núcleo (fluxo spec-driven) — executáveis nesta fase

| Papel | Perfil | Subagente | Tools | Read-only? |
|---|---|---|---|---|
| Guardião de Processo | `perfis.md` | [`guardiao-processo`](../../.claude/agents/guardiao-processo.md) | Read, Grep, Glob | ✅ |
| Spec-agent | `perfis.md` | [`spec-agent`](../../.claude/agents/spec-agent.md) | Read, Write, Grep, Glob | — |
| Plan / Arquiteto | `perfis.md` | [`plan-arquiteto`](../../.claude/agents/plan-arquiteto.md) | Read, Write, Grep, Glob, WebFetch | — |
| Dev / Implementador | `perfis.md` | [`dev-implementador`](../../.claude/agents/dev-implementador.md) | Read, Write, Edit, Bash | — |
| Review (independente) | `perfis.md` | [`review`](../../.claude/agents/review.md) | Read, Grep, Glob, Bash | ✅ |
| Security | `perfis.md` | [`security`](../../.claude/agents/security.md) | Read, Grep, Glob, Bash | ✅ |
| QA / Living-docs | `perfis.md` | [`qa`](../../.claude/agents/qa.md) | Read, Write, Bash | — |
| Tech-Writer | `perfis.md` | [`tech-writer`](../../.claude/agents/tech-writer.md) | Read, Write, Edit, Grep | — |

**Invariante de segurança:** nenhum agente read-only (Guardião, Review, Security) tem
`Write`/`Edit` — julgar não é consertar (menor superfície de risco por agente, Princípio III).

## Toolkit (construir o próprio Maestro) — executáveis (spec 004)

Os meta-agentes que evoluem o próprio método, com governança:

| Papel | Subagente | Tools |
|---|---|---|
| Agent-Designer (meta) | [`agent-designer`](../../.claude/agents/agent-designer.md) | Read, Write, Edit, Grep |
| Skill-Author | [`skill-author`](../../.claude/agents/skill-author.md) | Read, Write, WebFetch |
| Curador / Pesquisa | [`curador-pesquisa`](../../.claude/agents/curador-pesquisa.md) | Read, Write, WebSearch, WebFetch |
| Didática / Editor | [`didatica-editor`](../../.claude/agents/didatica-editor.md) | Read, Write, Edit, Grep |

**V0 completa: 12 de 12 agentes executáveis** (8 núcleo + 4 toolkit).

## Humanos (indelegáveis) — não são subagentes

Steward / Product Owner e Orquestrador são o **operador** da metodologia, não
`.claude/agents/`. Ver `perfis.md` § Humanos.
