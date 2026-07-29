# Spec 003 — Perfis de agentes executáveis (`.claude/agents/`)

- **Status**: Em revisão (clarify) · **Raia**: Plena · **Data**: 2026-07-29
- **Origem**: Fase 1 do roadmap. Hoje os perfis são um rascunho descritivo
  (`docs/agents/perfis.md`); falta a forma **executável** (subagentes do Claude Code).

## O quê e por quê

Para o Maestro **rodar** (não só descrever) o fluxo humano+N-agentes, cada especialista de
IA precisa existir como **subagente estreito** — `.claude/agents/<slug>.md` com frontmatter
(`name`, `description`, `tools`, `model`) + system prompt. Estreito por causa da **janela de
contexto**: cada agente carrega só o seu papel + a spec como norte.

**Valor**: o Orquestrador (humano) passa a poder **delegar** a agentes reais com escopo e
acesso definidos, em vez de um agente genérico. É o que torna a metodologia operável.

## Requisitos funcionais

- **FR1**: um arquivo `.claude/agents/<slug>.md` por **agente de IA** (os 12 do
  `perfis.md`: 8 núcleo + 4 toolkit), com frontmatter válido e system prompt derivado do
  perfil (escopo/faz-não-faz, produz/consome, handoff).
- **FR2**: **tools allowlist estreita** por papel — ex.: Review/Security/Guardião =
  read-only (`Read, Grep, Glob, Bash` p/ rodar checks; **sem** Write/Edit); Dev = `Read,
  Write, Edit, Bash`; Curador = `+WebSearch, WebFetch`. Nenhum agente read-only com Write.
- **FR3**: `docs/agents/README.md` — índice ligando cada perfil ao seu subagente.
- **FR4**: `docs/agents/perfis.md` aponta para os subagentes (perfil = fonte humana;
  `.claude/agents/*` = executável derivado; manter em sincronia).

## Fora de escopo

- **Humanos** (Steward, Orquestrador) — não são subagentes; são o operador. (O Orquestrador
  pode ganhar um guia à parte, não um `.claude/agents/`.)
- **Agentes de domínio** (frontend/backend/UX/dados) — entram por projeto, não aqui.
- Skills/workflows (Fases 2–3).

## Critérios de aceite (DoD)

- [ ] 12 arquivos `.claude/agents/*.md` com frontmatter parseável (name/description/tools).
- [ ] Nenhum agente read-only (review/security/guardião) com `Write`/`Edit` nas tools.
- [ ] `docs/agents/README.md` lista os 12 com link.
- [ ] `perfis.md` linka os executáveis.

## Clarify (resolvido — defaults, 2026-07-29)

1. **Lote**: **núcleo (8)** neste ciclo (o fluxo spec-driven); toolkit (4) no ciclo seguinte.
2. **Rigidez de tools**: **allowlist estreita** por papel desde já.

Reduz o FR1 a **8 arquivos** neste ciclo (os toolkit viram spec 004 ou continuação).
