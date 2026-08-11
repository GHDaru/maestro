# Tasks 052 — Symlink não é porta de saída

## Verification first
- [x] T0 — reproduzir o ataque: `ln -s /fora <alvo>/skills` e ver o instalador escrever lá.

## Implementation
- [x] T1 — `escapes_via_symlink()` consultada antes de escrever e antes de remover.
- [x] T2 — recusa nomeada e contada no resumo.
- [x] T3 — duas asserções no `check-installed.sh`.
- [x] T4 — registrar e fechar o achado 051.

## Closing tail — MANDATORY, one line each, never delete
<!-- TICK ONLY WHILE WRITING THE EVIDENCE, never in advance: the box records what happened.
     Do not delete a line to say it does not apply: write `n/a: <reason>` on it.
     check-conformance.sh requires the evidence of every non-n/a step in qa-report.md. -->
- [x] TAIL:review — independent review in fresh context, by whoever did not execute
- [x] TAIL:security — security pass proportional to the risk class
- [x] TAIL:gate — DoD green -> guardian verdict -> human merge gate (not delegable)
