# Tasks 056 — Instalar o harness

## Verification first
- [x] T0 — medir o estado antes de escrever: o instalador não menciona hooks, o `CLAUDE.md`
      não tem `@`-import, e **nenhum** portão verifica as três imutabilidades declaradas.

## Implementation
- [x] T1 — `contracts/`: o JSON de entrada e saída do hook, e a forma da fusão do `settings.json`.
- [x] T2 — `scripts/hooks/guard-immutables.py` (PreToolUse), com a via correta em cada recusa.
- [x] T3 — `scripts/hooks/session-state.sh` (SessionStart), medindo em vez de lembrar.
- [x] T4 — `.claude/settings.json` no Maestro, ligando os dois (o método instalado nele mesmo).
- [x] T5 — instalador: copia a camada, **funde sem destruir**, `--no-hooks`, resumo declara.
- [x] T6 — `@docs/governance/principles.md` no bloco gerado, com o custo escrito na spec.
- [x] T7 — asserções no `check-installed.sh`: bloqueia o que deve, passa o que deve.

## Closing tail — MANDATORY, one line each, never delete
<!-- TICK ONLY WHILE WRITING THE EVIDENCE, never in advance: the box records what happened.
     Do not delete a line to say it does not apply: write `n/a: <reason>` on it.
     check-conformance.sh requires the evidence of every non-n/a step in qa-report.md. -->
- [x] TAIL:review — independent review in fresh context, by whoever did not execute
- [x] TAIL:security — security pass proportional to the risk class
- [x] TAIL:mutation — every gate created or changed here, broken on purpose and seen refusing
- [x] TAIL:gate — DoD green -> guardian verdict -> human merge gate (not delegable)

## Após o parecer — 24 achados, 9 bloqueantes
- [x] T8 — o guarda: `realpath` (bypass por symlink), `IGNORECASE` (bypass em FS
      insensível), confinamento ao repositório, e **rastreado pelo git** em vez de "existe" —
      autorar um ADR em duas chamadas deixou de ser bloqueado.
- [x] T9 — o instalador: escrita do `settings.json` sem redirect cru (matava a instalação e
      órfãava o manifesto), `--no-hooks` deixa de apagar hooks vivos, reinstalar deixa de
      conflitar consigo, *snippet* virou JSON válido, `--dry-run` não conta nem afirma,
      `chmod +x` também no `.py`, e o helper de merge deixou de ser enviado ao destino.
- [x] T10 — o bloco de método só afirma a proteção quando o harness está ativo.
- [x] T11 — `session-state.sh` em repositório sem commit.
- [x] T12 — o portão passa a provar a **fiação**, não só o script; e parseia em vez de casar
      espaço de `json.dump`.
- [x] T13 — contrato e spec corrigidos: campos do evento, `ask`, `source`, fidelidade do
      merge, custo do `@`-import com o método de medida, e a dívida herdada declarada.
