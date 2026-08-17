# Tasks NNN — [TITLE]

<!--
  Rules (operating model plus proven cycles):
  - VERIFICATION FIRST: T0 defines the executable DoD checks before implementing.
  - ZERO CONTEXT: write each task for someone with zero context of the repository —
    everything it needs is in it or linked (file, command, criterion). 2–15 minutes per task.
  - Cycle with more than 3 tasks: a light checkpoint when each one closes
    (✔ what · evidence · next).
  - One task at a time, small focused diff (no opportunistic refactor — anti-pattern 10).
  - Order by dependency; cutting by boundary is what makes parallel work safe.
  - A bug requires a test that reproduces it BEFORE the fix (red → green).
  - Living-doc tasks belong HERE (same pull request), not "later".
-->

## Verification first

- [ ] **T0** — Define the executable DoD checks (see `plan.md § Verification`).

## Implementation

- [ ] **T1** — [... (FRn)]
- [ ] **T2** — [... (FRn)]

## Living documentation (same pull request)

- [ ] **Tn** — [journey / ADR / changelog / glossary affected]

## Closing tail — MANDATORY, one line each, never delete

<!--
  This block is why cycle 042 exists. On a companion repository, a plan listed the
  implementation steps and stopped at "docs and fitness green": the closing tail lived in the
  spec and in the agent's working memory, never in the checklist the executor follows.
  Context compaction then promoted the truncated version to source of truth, and the agent
  drove faithfully to a pull request with no independent review and no security pass.
  Faithful obedience to a lossy source (corollary C12, anti-pattern 22).

  TICK THESE ONLY WHILE WRITING THE EVIDENCE, never before. Ticking a tail box in advance —
  "I am about to do this" — is how cycles 042 and 043 both reached review with `[x]` beside
  a qa-report.md that was still an empty skeleton. The box records what happened; it is not
  a plan (anti-pattern 22).

  Do NOT delete a line to say it does not apply — write `n/a: <reason>` on it instead. An
  absent step is invisible; a declared exception is auditable. `scripts/check-conformance.sh`
  reads these tokens, and for every step that is not `n/a` it requires the evidence to be in
  `qa-report.md`. A ticked box is not a witness.
-->

- [ ] **TAIL:review** — independent review in **fresh context**, by whoever did not execute
  (Theorem 2). Evidence: the verdict, in `qa-report.md`.
- [ ] **TAIL:security** — security pass proportional to the risk class. When the change has
  no risk surface, replace this line's tail with `n/a:` followed by the actual reason — a
  placeholder is rejected by the gate.
- [ ] **TAIL:mutation** — every gate this cycle created or changed was **broken on purpose
  and seen refusing**. Evidence: the mutation and its output, in `qa-report.md`. When the
  cycle touched no gate, write `n/a:` with the reason — but the gate reads the diff, not the
  sentence, and refuses `n/a` from a cycle that did change one. In six of the nine cycles
  046-054 — 046, 047, 048, 049, 050 and 054 — an independent review found a gate that had
  shipped vacuous; what separated the ones caught early was that somebody broke them and
  looked.
- [ ] **TAIL:gate** — DoD green → guardian verdict → **human merge gate (not delegable)**;
  promotion via `scripts/promote-main.sh` (records `gate-main-<sha>` automatically, ADR 0009).
