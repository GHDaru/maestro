# Plan 004 — Agentes de toolkit executáveis

- **Spec**: `spec.md` · **Raia**: Plena · **Data**: 2026-07-29

## Constitution Check (principios-maestro.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven | ✅ nasce da spec 004 (continuação da 003) |
| II. Orquestração humano-governada | ✅ meta-agentes propõem; A humano decide adotar |
| III. Reversibilidade / gates de risco | ✅ tools estreitas; nenhum meta-agente altera main sozinho |
| IV. Test-First / DoD verificável | ✅ DoD por grep/ls (frontmatter, tools, contagem) |
| V. Economia de contexto / fronteira | ✅ cada meta-agente carrega só seu papel |
| VI. Artefatos vivos | ✅ README fecha 12/12; perfis já linkam |
| VII. Governança leve / YAGNI | ✅ fecha exatamente os 4 restantes; nada além |

**Sem violações.**

## Como

- Mesmo formato Claude Code da 003. 4 slugs: `agent-designer`, `skill-author`,
  `curador-pesquisa`, `didatica-editor`.
- **Tools por papel**:
  - `agent-designer`: Read, Write, Edit, Grep (autor local de perfis/subagentes).
  - `skill-author`: Read, Write, WebFetch (padrão agentskills.io + escrever SKILL.md).
  - `curador-pesquisa`: Read, Write, WebSearch, WebFetch (pesquisa citada).
  - `didatica-editor`: Read, Write, Edit, Grep (clareza/storytelling, sem web).
- `docs/agents/README.md`: mover os 4 da seção "próxima fase" para a tabela de executáveis.

## Verificação (DoD)

- `ls .claude/agents/*.md | wc -l` = 12.
- `grep -L "^name:" .claude/agents/{agent-designer,skill-author,curador-pesquisa,didatica-editor}.md` vazio.
- `grep -l "WebSearch" .claude/agents/curador-pesquisa.md` e `grep -l "WebFetch" .claude/agents/skill-author.md` não-vazios.
