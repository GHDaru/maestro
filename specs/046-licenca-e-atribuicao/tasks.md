# Tasks 046 — Licença e atribuição do que é redistribuído

## Verification first
- [x] T0 — escrever `scripts/check-licensing.sh` **antes** de qualquer correção e vê-lo
  acusar: sem `LICENSE`, manifesto divergente, instalador que não leva os avisos.

## Implementation
- [x] T1 — `LICENSE` na raiz: texto MIT, `Copyright (c) 2026 GHDaru` (FR1).
- [x] T2 — `THIRD-PARTY-NOTICES.md`: `github/spec-kit` com versão, commit do fork, licença e
  linha de copyright do titular; verbatim separado de modificado (FR2).
- [x] T3 — `install-maestro.sh`: `copy_as()` levando os dois arquivos renomeados para
  `docs/governance/` no destino (FR3).
- [x] T4 — portão cobrindo manifesto × licença (FR4) e upstream × atribuição (FR5).
- [x] T5 — glossário: EARS, BMAD, SBOM.
- [x] T6 — classificar os arquivos novos no `boundary.json`.
- [x] T7 — ADR 0020 (a escolha e o que ela custa: MIT sem concessão de patente).
- [x] T8 — `check-licensing` entra na CI como bloqueante — portão que só roda quando alguém
  lembra não é *forcing function*.
- [x] T9 — corrigir o índice `docs/adr/README.md`, congelado desde o 0017 (achado do ciclo).
- [x] T10 — registrar o ciclo: CHANGELOG, roadmap, índice de decisões.

## Closing tail — MANDATORY, one line each, never delete
<!-- TICK ONLY WHILE WRITING THE EVIDENCE, never in advance: the box records what happened.
     Do not delete a line to say it does not apply: write `n/a: <reason>` on it.
     check-conformance.sh requires the evidence of every non-n/a step in qa-report.md. -->
- [x] TAIL:review — independent review in fresh context, by whoever did not execute
- [x] TAIL:security — security pass proportional to the risk class
- [x] TAIL:gate — DoD green -> guardian verdict -> human merge gate (not delegable)
