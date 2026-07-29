# Plan 003 — Perfis de agentes executáveis

- **Spec**: `spec.md` · **Raia**: Plena · **Data**: 2026-07-29

## Constitution Check (principios-maestro.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven | ✅ nasce da spec 003 |
| II. Orquestração humano-governada | ✅ define os agentes que o humano orquestra; A humano preservado |
| III. Reversibilidade / gates de risco | ✅ **tools estreitas** = menor superfície de risco por agente (read-only onde cabe) |
| IV. Test-First / DoD verificável | ✅ DoD verificável por grep (frontmatter, tools proibidas) |
| V. Economia de contexto / fronteira | ✅ **é o princípio-motor**: cada agente estreito, carrega só seu papel |
| VI. Artefatos vivos | ✅ perfis (fonte humana) ↔ `.claude/agents` (executável), com índice |
| VII. Governança leve / YAGNI | ✅ 8 agora (núcleo); toolkit depois |

**Sem violações.**

## Como

- Formato Claude Code: `.claude/agents/<slug>.md` com frontmatter `name`, `description`
  (quando usar), `tools` (allowlist estreita), e system prompt derivado do perfil
  (escopo · faz/não faz · produz/consome · handoff · orçamento de contexto).
- 8 agentes-núcleo: `guardiao-processo`, `spec-agent`, `plan-arquiteto`,
  `dev-implementador`, `review`, `security`, `qa`, `tech-writer`.
- **Regra de tools**: read-only (guardião, review, security) = `Read, Grep, Glob, Bash`
  (sem Write/Edit); autores (spec, plan, dev, qa, tech-writer) = + Write/Edit; nenhum extra.
- Índice `docs/agents/README.md`; `perfis.md` linka os executáveis.

## Verificação (DoD)

- `ls .claude/agents/*.md | wc -l` = 8 (+ o `dod.md` já existente é comando, não agente).
- `grep -L "^name:" .claude/agents/*.md` vazio (todo agente tem frontmatter).
- `grep -lE "tools:.*(Write|Edit)" .claude/agents/{review,security,guardiao-processo}.md` vazio.
