# Tasks 003 — Perfis de agentes executáveis

> Raia plena · TDD pragmático: o DoD é verificável por `grep`/`ls` (as "fitness
> functions" deste ciclo). Cada task fecha contra um critério de aceite da `spec.md`.

## Verificação primeiro (o teste que precisa passar)

- [x] **T0** — Definir os checks executáveis do DoD (ver `plan.md § Verificação`):
  - `ls .claude/agents/*.md | wc -l` = 8
  - `grep -L "^name:" .claude/agents/*.md` → vazio (todo agente tem frontmatter)
  - `grep -lE "tools:.*(Write|Edit)" .claude/agents/{review,security,guardiao-processo}.md` → vazio

## Implementação (8 subagentes-núcleo — FR1/FR2)

- [x] **T1** — `guardiao-processo.md` (read-only: Read, Grep, Glob)
- [x] **T2** — `spec-agent.md` (Read, Write, Grep, Glob)
- [x] **T3** — `plan-arquiteto.md` (Read, Write, Grep, Glob, WebFetch)
- [x] **T4** — `dev-implementador.md` (Read, Write, Edit, Bash)
- [x] **T5** — `review.md` (read-only: Read, Grep, Glob, Bash)
- [x] **T6** — `security.md` (read-only: Read, Grep, Glob, Bash)
- [x] **T7** — `qa.md` (Read, Write, Bash)
- [x] **T8** — `tech-writer.md` (Read, Write, Edit, Grep)

## Documentação viva (FR3/FR4 — mesmo PR)

- [x] **T9** — `docs/agents/README.md` (índice perfil ↔ subagente + invariante de segurança)
- [x] **T10** — `docs/agents/perfis.md` aponta para os executáveis + regra de sincronia

## Gate

- [ ] **T11** — Verde nos checks do DoD → veredito do Guardião → **gate de merge humano**
  (indelegável): promover `dev` → `main` só após aprovação do Steward.
