# QA report 066 — Painel de regência: ciclo guarda-chuva da integração da linha paralela

- **Date**: 2026-10-24 · **Lane**: light (coordination; the code lives in the child cycles) · **Verdict**: artifacts present and honest; the four TAIL steps are n/a with the reasons mirrored from `tasks.md`; nothing of its own to promote

> This folder coordinated the integration of the parallel line (cycles 066 v0, 067, 068, 069,
> 070) and the opening of the regency panel (072). Its deliverables are documents, decisions and
> the multi-session launcher. Every child cycle carries its own review, security pass, mutation
> record and gate. Measured on this Windows machine on 24/10/2026, main checkout, branch
> `066-painel-de-regencia`.

## Fitness functions (DoD)

| Check | Expected | Result |
|---|---|---|
| `ls specs/066-painel-de-regencia/` | 11 files (andamento, handoff, plano de integração, ux-design, pareceres, 2 insumos, spec, plan, tasks, qa-report) | 11 ✅ |
| `python scripts/multi-session.py . --dry-run` | 7 sessions listed, nothing opened | `Gerente glm-5.3`, `Worker01..06 deepseek-v4.1-flash`, `[dry-run] nothing opened` (22/10) ✅ |
| real launch (24/10) | 7 sessions registered, gateway answering | `ListAgents` shows Gerente and Worker01–06; Gerente answered "glm-5.3, HEAD a51c5f6, pronto"; Worker01 committed the 072 spec (`48da92d`) ✅ |
| `git log --oneline -- scripts/check-*.sh` filtered by this folder's commits | no gate script touched by this cycle | none ✅ |
| `scripts/check-conformance.sh 066` | green for both 066 folders | recorded in `andamento.md`, entry of 24/10, after this file |

## Closing tail — the evidence

- **TAIL:review** — n/a: coordination cycle without product code of its own; the independent reviews in fresh context happened per child cycle (066 v0, 067, 068, 069: 20/10; 070: 22/10, REQUEST_CHANGES then fixed) and are recorded in each `qa-report.md`. The launcher has no test yet (debt 1 of `tasks.md`) and will get its review with the test.
- **TAIL:security** — n/a: the only surface of this folder is `scripts/multi-session.py`; its risk was assessed by three opinions in fresh context (`pareceres-sessoes-via-gateway.md`: no secret in the repository, the token only in the user scope, one worktree per Worker, deny list for the builders) and the 401 incident of 22/10 was diagnosed before being fixed (inherited base URL, not the token). The child cycles carry their own passes.
- **TAIL:mutation** — the gate charges the cycle number, and commits labelled "ciclo 066" touched two gates: the shape-based exemption for imported evidence in `scripts/check-conformance.sh` (decision B1 of 21/10, `3f590ab`) and `boundary.json` (cycle 066 v0). Both were broken on purpose and seen refusing, and the observations are mirrored here from the files that first recorded them: (a) exemption — an empty `tasks.md` added to `specs/070-conferidor-ordem-veredito/` made `check-conformance.sh 070` print `✗ missing plan.md` and `✗ missing qa-report.md` (the folder charged as a cycle again); removing it returned the folder to the exempt listing with `0` changes (cycle 069 `qa-report.md` § Findings); a first version of the exemption made the single-cycle run say "checked nothing" and was fixed by counting the exempt folder as inspected; (b) `boundary.json` — the `painel/` ownership line removed made `check-boundary.sh` refuse with the undeclared-domain error, restored byte for byte afterwards (cycle 066 v0 `qa-report.md` § TAIL:mutation). No new gate was created by this folder's own commits of 24/10 (`8245a36`): plan, tasks and this file only.
- **TAIL:gate** — n/a: this folder promotes nothing by itself. The gates of the work it coordinated are recorded as `gate-dev-integra-066-069`, `gate-main-3f590ab` (CI green, 21/10) and `gate-070-delegado` (24/10, ADR 0026). The next promotion of `dev` to `main` happens when rodada 1 of cycle 072 closes, because `promote-main.sh` runs the full conformance and a spec-only 072 is red by design until then (aborted run of 24/10 recorded in `andamento.md`).

## Requirement coverage

- The intention in `spec.md` (a regency panel: queue of decisions, sessions, chamados by gate, evidence journey) is served by `ux-design.md` (roles) and by the spec of cycle 072 (21 FR), not by code in this folder.

## Findings inside the cycle

- **The builder sessions failed once by environment, not by credentials.** The launcher inherited `ANTHROPIC_BASE_URL=https://api.anthropic.com` from the session that ran it; the gateway answered 200 with the same token. Fixed in `18d7223`.
- **Name collision across projects.** "Gerente" exists in the Hindiana and in the Maestro; on 24/10 messages crossed both ways and the chain stalled 16 h. Rule adopted: address sessions by their ListAgents ref; launcher to prefix names (debt 2).
- **The skeleton of this folder stayed a skeleton for five days** and turned the full conformance red at promotion time. It now says what the cycle was. Lesson for `new-cycle.sh` users: an umbrella folder must declare itself as such on day one.
