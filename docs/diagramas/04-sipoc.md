# Maestro — SIPOC

> SIPOC (Fornecedores–Entradas–Processo–Saídas–Clientes) do ciclo de entrega. Fonte visual:
> [`fontes/04-sipoc.html`](fontes/04-sipoc.html) · PDF: [`pdf/04-sipoc.pdf`](pdf/04-sipoc.pdf)

O processo central é o ciclo spec-driven; os losangos ◆ marcam os **gates humanos
indelegáveis**, os círculos verdes as **verificações mecânicas**.

## S · Suppliers (Fornecedores)

Steward/negócio (intenção, prioridade, apetite) · usuários e jornadas (necessidade, feedback)
· governança (Constituição, princípios, ADRs) · Curador/Pesquisa (evidência, boas práticas) ·
base de código e sistema existente · catálogo de agentes, skills, templates.

## I · Inputs (Entradas)

Brief/intenção + apetite · critérios de negócio/jornada · Princípios I–VII (Constitution
Check) · linguagem ubíqua/contexto de domínio · specs vizinhas, ADRs e padrões anteriores ·
classe de risco da mudança (define a **raia**).

## P · Process (Processo — o ciclo)

1. **Especificar** — `spec-agent` → `spec.md`
   - ◆ **Gate DoR** — humano aprova a spec
2. **Planejar** — `plan-arquiteto` → `plan.md` + Constitution Check
   - ◆ **Gate** — humano aprova o plan
3. **Fatiar** — → `tasks.md` por fronteira
4. **Implementar** — `dev` → código + testes (diffs pequenos)
5. **Verificar** — `review` (fresco) · `security` · `qa`
   - ◆ **Gate DoD** — checks verificáveis verdes
6. **Promover** — gate de merge (humano) → `main`
7. **Retro** — erro recorrente → regra versionada

## O · Outputs (Saídas)

Código + testes em `main` · artefatos vivos (spec/plan/tasks/`qa-report`) · ADR, journey,
CHANGELOG (mesmo PR) · PR mergeado + evidência · rastreabilidade **spec ↔ PR ↔ teste ↔
journey** · regra nova (retro → CLAUDE.md/constituição).

## C · Customers (Clientes)

Usuário final (a jornada) · Steward (próxima aposta) · próximos ciclos e agentes (consomem os
artefatos) · operação (runbook, rollback) · **o próprio método** (retro alimenta a governança).

---

## Gates (portões)

**Humanos inegociáveis** ◆
- Aprovar a **spec** — DoR (raia plena)
- Aprovar o **plan** — Constitution Check
- **Gate de merge** — decisão de promover
- Autorizar **deploy/migração** — infra, dupla aprovação

**Mecânicos** ● (CI / infra)
- Hard gates de CI — testes + fitness functions + build, CHANGELOG, secret scanning
- Reversibilidade (infra) — backup, dry-run/staging, rollback

## Documentos (artefatos)

`brief/intenção` · `spec.md` · `plan.md` · `Constitution Check` · `ux-design.md` · `tasks.md`
· `código + testes` · `qa-report.md` · `ADR` · `journey` · `runbook` · `CHANGELOG` ·
`DoR / DoD` · `PR`.
