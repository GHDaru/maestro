# Tarefas 039 — Fronteira interna e portão para os perfis de agente

## Verificação primeiro
- [x] T0 — auditar a organização medindo (duplicação por hash, consumidores por diretório,
      portões que citam cada caminho) em vez de opinar
- [x] T1 — estender `check-roles.sh` **antes** de tocar em `docs/agents/`
- [x] T2 — vê-lo acusar nas quatro condições (ausente, fantasma, tool nova, total velho)

## Implementação — parte A (a reversão)
- [x] T3 — ADR 0018 superseding o 0017, com a medição que mudou a decisão
- [x] T4 — status de superado no 0017, corpo intacto (ADR é imutável)
- [x] T5 — `boundary.json`: `repos`→`domains`, `mirrored`→`shared`, rótulos de domínio
- [x] T6 — `check-boundary.sh` acompanha, incluindo as mensagens e a razão da invariante 3
- [x] T7 — re-provar `check-boundary.sh` acusando depois da reescrita

## Implementação — parte B (registro e artefatos vivos)
- [x] T8 — índice de decisões: ADR 0018 + linha de superação do 0017
- [x] T9 — corrigir por linha nova os dois registros errados: o `fecha` auto-referente e o
      `achado-038`, que descrevia um cenário que a reversão eliminou
- [x] T10 — `CHANGELOG.md`, `docs/roadmap.md` (F14b sai; gatilhos de reabertura entram),
      `CLAUDE.md`

## Gate
- [x] T11 — DoD verde → `qa-report.md`
- [ ] T12 — gate humano de merge `dev` → `main`
