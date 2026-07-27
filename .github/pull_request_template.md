<!-- Espelha a Definition of Done do modelo operacional (docs/governance/modelo-operacional.md §7).
     O que é mecânico já é hard gate na CI; este checklist cobre o que exige julgamento. -->

## O que muda
<!-- Resumo do delta. Na raia leve, este PR é o próprio artefato. -->

## Raia (§3)
- [ ] Leve (bug/typo/rename) &nbsp;·&nbsp; [ ] Plena (feature/contrato) &nbsp;·&nbsp; [ ] Infra (sempre plena + gates de reversibilidade)

## Rastreabilidade (§9)
- Spec: `specs/NNN-*` &nbsp;(ou `N/A — raia leve`)
- Fecha/relaciona: #

## Definition of Done (§7)
- [ ] Testes verdes (unitário de domínio + contrato por porta + integração por rota)
- [ ] Fitness functions verdes (web `architecture.test.ts` · api `lint-imports`)
- [ ] Typecheck/build limpos
- [ ] Revisão independente (`/code-review` em contexto fresco) sem lacunas de correção abertas
- [ ] Segurança: nenhum segredo commitado; injeção/authz revisadas quando aplicável
- [ ] Docs vivas no mesmo PR: journey (capturas+heurística) / ADR se houve decisão / **entrada no `CHANGELOG.md`**
- [ ] Rastreabilidade registrada (spec ↔ PR ↔ testes ↔ journey)
- [ ] Evidência anexada (output de teste/build/screenshot) — "prove, não declare"

## Ações irreversíveis — raia infra (§7)
- [ ] N/A
- [ ] Backup/snapshot antes · dry-run + staging · estratégia de rollback no runbook · aprovação humana explícita

## Gate humano (§8)
- [ ] Classe de risco identificada; aprovação humana obtida quando exigida (alteração/exclusão/irreversível)
