# Tasks NNN — [TÍTULO]

<!--
  Regras (modelo operacional + ciclos provados):
  - VERIFICAÇÃO PRIMEIRO: T0 define os checks executáveis do DoD antes de implementar.
  - Uma task por vez, diff pequeno e focado (sem refatoração oportunista — anti-padrão 10).
  - Ordene por dependência; corte por fronteira permite paralelizar com segurança.
  - Bug exige teste que o reproduz ANTES do fix (red → green).
  - Task de doc viva entra AQUI (mesmo PR), não "depois".
-->

## Verificação primeiro

- [ ] **T0** — Definir os checks executáveis do DoD (ver `plan.md § Verificação`).

## Implementação

- [ ] **T1** — [... (FRn)]
- [ ] **T2** — [... (FRn)]

## Documentação viva (mesmo PR)

- [ ] **Tn** — [journey/ADR/CHANGELOG/glossário afetados]

## Gate

- [ ] **Tz** — DoD verde → veredito do Guardião → **gate de merge humano (indelegável)**;
  promoção via `scripts/promover-main.sh` (registra `gate-main-<sha>` automaticamente,
  ADR 0009).
