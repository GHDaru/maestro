# Tarefas 043 — Os portões entram na integração contínua

## Verificação primeiro
- [x] T0 — simular o job localmente, comando a comando, **antes** de escrever o YAML
- [x] T1 — descobrir na simulação os dois fatos que só aparecem em CI: o build precisa de
      `npm ci --prefix publicar`, e numa branch de PR não existe `main` local

## Implementação
- [x] T2 — job `gates` com os nove portões estruturais + `package-plugin --verify` + build
- [x] T3 — `check-cycle` e `check-retro` como consultivos (`::warning::`, nunca bloqueiam)
- [x] T4 — `permissions: contents: read` no topo, valendo para todo job
- [x] T5 — `MAESTRO_TRACE_BASE=origin/main` com o `git fetch` correspondente
- [x] T6 — endurecer o `grep -q` no fim de pipe do job de `CHANGELOG` (anti-padrão 21)
- [x] T7 — `CHANGELOG.md`, `docs/roadmap.md`, índice de decisões (fechar o achado 042)

## Closing tail — obrigatória, uma linha cada, nunca apagar
- [x] **TAIL:review** — revisão independente em contexto fresco, por quem não executou
  (teorema T2). Evidência: o veredito, no `qa-report.md`.
- [x] **TAIL:security** — passagem de segurança **executada**, não dispensada: um workflow
  de CI é superfície de risco real (permissões do token, *actions* de terceiros, instalação
  de dependências). Evidência e ressalvas no `qa-report.md`.
- [ ] **TAIL:gate** — DoD verde → veredito do guardião → gate humano de merge (indelegável);
  promoção via `scripts/promote-main.sh`.
