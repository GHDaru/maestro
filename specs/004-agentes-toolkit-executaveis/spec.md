# Spec 004 — Agentes de toolkit executáveis (`.claude/agents/`)

- **Status**: Aprovada (defaults) · **Raia**: Plena · **Data**: 2026-07-29
- **Origem**: continuação da spec 003. Fecha a **V0 de todos os agentes**: os 8
  núcleo já são executáveis; faltam os **4 de toolkit** — os que constroem o
  próprio Maestro (meta-agentes).

## O quê e por quê

Os 4 agentes de toolkit hoje só existem como perfil descritivo (`perfis.md § toolkit`).
Para o Maestro **evoluir a si mesmo** com governança (não ad-hoc), cada um precisa da
forma executável — `.claude/agents/<slug>.md`, estreito, com tools por papel.

**Valor**: transformar melhoria do próprio método (novo agente, nova skill, pesquisa
citada, clareza didática) em trabalho **delegável e auditável**, não improviso.

## Requisitos funcionais

- **FR1**: um `.claude/agents/<slug>.md` por agente de toolkit (4): `agent-designer`,
  `skill-author`, `curador-pesquisa`, `didatica-editor` — frontmatter + system prompt
  derivado do perfil (escopo/faz-não-faz, produz/consome, handoff).
- **FR2**: tools allowlist estreita por papel — Curador/Pesquisa ganha `WebSearch,
  WebFetch`; Skill-Author ganha `WebFetch` (padrão agentskills.io); Agent-Designer e
  Didática/Editor são autores locais (sem web).
- **FR3**: `docs/agents/README.md` promove os 4 de "próxima fase" para **executáveis**,
  com tabela e links (fecha a V0: 12 de 12).

## Fora de escopo

- Skills e workflows em si (Fases 2–3) — aqui só o **agente** que os cria.
- Agentes de domínio (por projeto).

## Critérios de aceite (DoD)

- [ ] `ls .claude/agents/*.md | wc -l` = 12.
- [ ] Os 4 novos têm frontmatter parseável (`^name:`).
- [ ] `curador-pesquisa` tem `WebSearch`; `skill-author` tem `WebFetch`.
- [ ] `README.md` lista os 12 como executáveis (nenhum "próxima fase" restante).

## Clarify (resolvido — defaults, 2026-07-29)

1. **Lote**: os 4 restantes agora → fecha a V0 (pedido explícito: "não pare até
   terminar a V0 de todos os agentes").
2. **Tools**: allowlist estreita por papel (mesma regra da 003).
