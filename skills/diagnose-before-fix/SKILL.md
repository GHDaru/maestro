---
name: diagnose-before-fix
description: Root-cause discipline — investigate before fixing. Use it when you find any bug, failing test or unexpected behaviour, BEFORE proposing or applying any fix. Fixing a symptom without the cause is failure, not progress.
---

# Diagnose before you fix

## Iron Law

```
NO FIX WITHOUT A ROOT-CAUSE INVESTIGATION FIRST
```

**Violating the letter of this rule violates its spirit.** This is NOT an excuse:
- "it is obvious what is wrong" — if it were, why does the bug exist? Prove it with evidence.
- "the fix is small, I will test later" — a fix without a confirmed cause is a bet, not
  engineering.
- "I have seen this error before" — a similar pattern is not the same cause; the check costs
  minutes.

## The phases (in order, no skipping)

1. **Actually read the error** — the whole message, the full stack, the surrounding log.
   Most "mysteries" are written in the error nobody read.
2. **Reproduce** — if you cannot reproduce it, you do not know what you are fixing. A bug
   requires a **test that reproduces it** (red) before the fix.
3. **Isolate** — narrow down to the smallest condition that triggers it (bisect the commit,
   the data or the configuration; add logs along the suspect path; one factor at a time).
4. **A single explicit hypothesis** — "the cause is X, because of evidence Y". If there are
   two hypotheses, there is more investigation to do — not two fixes to try.
5. **Prove it** — the test from phase 2 fails exactly because of cause X, not by accident.
6. **Only then fix** — the fix attacks X; the test turns green; run the whole suite (green
   locally ≠ right globally).

## Signs that you skipped a phase (stop and go back)

- You are on the second "try this" in a row (anti-pattern 5, blind retry).
- The fix "worked" but you cannot explain why.
- The correction widened the scope ("while I was there…") — anti-pattern 10.

**Consumed by:** `dev-implementer`, `qa`. **Handoff:** fix + test → `review`.
**Sources:** systematic debugging (Superpowers, adapted); retrospectives; anti-patterns
5, 7 and 10.
