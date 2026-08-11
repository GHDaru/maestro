---
description: Runs the verifiable Definition of Done (tests, fitness functions, type check and build) and shows the evidence before calling a feature done.
---

Run the **verifiable Definition of Done** (operating model §7) and **show the evidence**
for every check — never claim success without output ("prove it, don't claim it").

Run and report the result of each item:

1. **Tests and build** of the project at hand, including the fitness functions.
2. **Method fitness functions**: `scripts/check-agents.sh`, `scripts/check-roles.sh`,
   `scripts/check-install.sh` — and every other `scripts/check-*.sh` this repository has.
3. **Secrets**: confirm that no secret or token was committed in the diff.
4. **Traceability** (§9): confirm the link `spec NNN ↔ pull request ↔ tests ↔ journey`.
5. **Changelog**: confirm an entry under `[Unreleased]` in `CHANGELOG.md` (or a light-lane
   change carrying the `skip-changelog` label).
6. **Living docs**: journey updated (if a journey was touched) and an ADR if a decision was
   made.

For every item that **passes**, show the command and its result. For every item that
**fails**, show the output and what to fix.

**Reminder (§8):** green locally ≠ right globally. Flag explicitly when the journey or the
larger whole may have been compromised — that judgement, and "is this the right thing", stay
with the human (the Accountable, §4).
