# Tasks 006 — Scripts do ritual

> Raia plena · DoD por exit code + efeito no filesystem (testável a seco).

## Verificação primeiro
- [x] **T0** — Definir checks: sintaxe, +x, aborts, create/no-overwrite, exit 0.

## Implementação (3 scripts — FR1–FR3)
- [x] **T1** — `scripts/promover-main.sh` (confirmação + retry + aborta sujo/sem-avanço)
- [x] **T2** — `scripts/novo-ciclo.sh` (scaffold 4 artefatos, não sobrescreve)
- [x] **T3** — `scripts/verificar-agentes.sh` (invariantes dos agentes, exit 1 se quebra)

## Documentação viva (FR4)
- [x] **T4** — `scripts/README.md` + roadmap atualizado (F1/F2 ✅, F3 🔜)

## Verificação executada
- [x] **T5** — `bash -n` ok · `+x` ok · `verificar-agentes` exit 0 · `novo-ciclo` cria/não
  sobrescreve · `promover-main` aborta com árvore suja (main intacto)

## Gate
- [ ] **T6** — Gate humano de merge → promover via o próprio `promover-main.sh` (dogfood).
