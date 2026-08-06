# Tarefas 037 — Evals: linha de base para saída não-determinística

## Verificação primeiro
- [x] T0 — escrever `scripts/check-evals.sh` **antes** dos casos, cobrindo FR2, FR3 e FR4
- [x] T1 — vê-lo acusar nas três condições (estrutura ausente, asserção fraca, alvo mudou)

## Implementação
- [x] T2 — T7 + corolário C11 em `docs/governance/axioms.md` (versão 1.1.0)
- [x] T3 — ADR 0016 registrando a emenda, a anatomia do caso e o limite assumido
- [x] T4 — `evals/README.md` (anatomia, como rodar, o que NÃO é um eval)
- [x] T5 — caso `001-review-drops-a-requirement` (alvo `.claude/agents/review.md`)
- [x] T6 — caso `002-guardian-accepts-a-wrong-lane` (alvo `.claude/agents/process-guardian.md`)
- [x] T7 — `.claude/commands/eval.md` (execução em contexto fresco, grava a linha de base)
- [x] T8 — `evals/` nos alvos do `check-language.sh`
- [x] T9 — *eval* no glossário; `check-evals.sh` na lista de fitness functions do `CLAUDE.md`
- [x] T10 — `CHANGELOG.md`, `docs/roadmap.md` e linha no índice de decisões (incluindo o
      achado aberto das duas linhas de base pendentes)

## Gate
- [x] T11 — DoD verde (exceto o vermelho declarado do `check-evals.sh`) → `qa-report.md`
- [ ] T12 — gate humano de merge `dev` → `main`
