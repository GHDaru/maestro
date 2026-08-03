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

## Gate

- [ ] **Tz** — DoD green → guardian verdict → **human merge gate (not delegable)**;
  promotion via `scripts/promote-main.sh` (records `gate-main-<sha>` automatically, ADR 0009).
