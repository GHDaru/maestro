# Tarefas 045 — A quarta ocorrência vira forma, e a v0.1.0 é fechada

## Verificação primeiro
- [x] T0 — escrever a condição do portão **antes** de mudar o template
- [x] T1 — vê-lo falhar numa spec com caixa nos critérios

## Implementação — correções da revisão
- [x] R1 — o portão cobre a família inteira de caixas e falha quando não acha a seção
- [x] R2 — `sed -nE` (o `\|` em BRE é extensão GNU: verde silencioso em BSD)
- [x] R3 — `record-decision.sh` recusa linha que cite arquivo-placeholder (quinta ocorrência)
- [x] R4 — nota de release: onze/oito em vez de doze/nove, tempo verbal, data 2026-08-09
- [x] R5 — entrada do próprio ciclo 045 no `[0.1.0]`

## Implementação
- [x] T2 — `spec-template.md`: critérios sem caixa, com a razão escrita
- [x] T3 — `new-cycle.sh`: esqueleto idem (é ele que se roda de fato)
- [x] T4 — `check-conformance.sh`: reprova caixa nos critérios, piso em 045
- [x] T5 — `CHANGELOG.md`: `[0.1.0]` datada com nota de release + `[Unreleased]` vazio
- [x] T6 — índice: fechar `achado-044`; abrir o das subseções repetidas
- [x] T7 — `docs/roadmap.md` e `README.md` citam a versão

## Closing tail — obrigatória, uma linha cada, nunca apagar
<!-- Marcar apenas enquanto escrevo a evidência. -->
- [x] **TAIL:review** — revisão independente em contexto fresco. Veredito "do not promote
  as-is", quatro bloqueantes; evidência e correções no `qa-report.md`.
- [x] **TAIL:security** — n/a: o ciclo mexe em texto de template, condição de portão
  somente-leitura e changelog; nenhum segredo, rede, credencial ou permissão entra.
- [ ] **TAIL:gate** — gate humano de merge (indelegável), depois a tag.
