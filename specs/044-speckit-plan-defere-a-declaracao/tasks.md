# Tarefas 044 — O `/speckit.plan` defere à tabela de declaração

## Verificação primeiro
- [x] T0 — ler a regra de proveniência antes de tocar em peça vendorizada
- [x] T1 — localizar os três pontos exatos do comando que mandam gerar

## Implementação — correções da revisão
- [x] R1 — reconstruir o `plugin/maestro/` (o contraditório sobrevivia no build commitado)
- [x] R2 — o portão bloqueante do plugin entra na DoD do plano
- [x] R3 — G2: o item 3 (contexto do agente) não é engolido pelo portão dos tokens
- [x] R4 — G3: a linha "skip if purely internal" deixa de competir com a tabela
- [x] R5 — G4: o portão da fase 0 sobe para antes dos passos
- [x] R6 — `new-cycle.sh` cita a regra 4 após a renumeração do `UPSTREAM.md`

## Implementação
- [x] T2 — passo 3: preencher a tabela de declaração **antes** das fases
- [x] T3 — fase 0 defere a `ART:research=yes`
- [x] T4 — fase 1 defere aos tokens; `quickstart.md` declarado fora, com a razão
- [x] T5 — `UPSTREAM.md`: `speckit.plan.md` de *Verbatim* para **Adaptado**
- [x] T6 — `UPSTREAM.md`: regra "divergência declarada, nunca silenciosa" + `quickstart`
- [x] T7 — `CHANGELOG.md`, `docs/roadmap.md`, índice (achado 042 fechado)

## Closing tail — obrigatória, uma linha cada, nunca apagar
<!-- Marcar apenas enquanto escrevo a evidência. Terceira ocorrência do contrário no 043. -->
- [x] **TAIL:review** — revisão independente em contexto fresco, por quem não executou.
  Evidência: o veredito ("do not merge as-is", seis lacunas), no `qa-report.md`.
- [x] **TAIL:security** — passagem executada: texto que instrui agente é código. Evidência
  e escopo no `qa-report.md`.
- [ ] **TAIL:gate** — DoD verde → veredito do guardião → gate humano de merge (indelegável).
