---
name: verifiable-dod
description: Turns vague acceptance criteria into executable fitness functions (grep, ls, tests) that a machine can verify without human judgement. Use it when writing the acceptance criteria (Definition of Done) of a spec.md or plan.md, or when a criterion is subjective ("works well", "is clear") and must become an objective check. Complements the /dod command, which runs the checks — this skill helps write them.
---

# Verifiable Definition of Done (design time)

## Iron Law

```
NO ACCEPTANCE CRITERION WITHOUT THE COMMAND THAT PROVES IT
```

**Violating the letter of this rule violates its spirit.** This is NOT an excuse:
- "it is hard to automate" — then mark it explicitly as a human gate; vague is not allowed.
- "everybody understands what it means" — with no command, everybody understands a different
  thing.

## Second law: prove the check by watching it fail

```
A CHECK YOU HAVE NEVER SEEN COMPLAIN IS NOT A CHECK — IT IS A HOPE
```

Before trusting a new check, **break the world on purpose** and watch it fail: inject the
collision, remove the file, leave the date stale. It is red-before-green applied to
verification. Without it you do not know whether the check measures the **fact** or merely a
**proxy** of it (anti-pattern 13) — the cases that motivated this law all passed happily
while measuring the wrong thing.

Principle IV demands a Definition of Done (DoD) that is **autonomously verifiable**: an agent
confirms it without opining. This skill turns a vague criterion into an executable check.

> **Division of labour:** this skill is *design time* (writing the checks, while drafting the
> spec or plan). The **`/dod`** command is *run time* (executing the checks before calling it
> done). One writes, the other runs — they do not overlap.

## When to fire

Writing acceptance criteria in `spec.md` or `plan.md`; a criterion is subjective and must
become objective.

## Step by step

1. Take each criterion and ask: **"which command proves this, with empty/non-empty output or
   an exit code?"** If you cannot answer, the criterion is still vague — rewrite it.
2. Prefer, in this order: **automated test** > `grep`/`ls`/counting > manual inspection (last
   resort, and mark it explicitly as a human gate).
3. Write the **(command, expected) pair** — for example `expected empty`, `= 12`, `exit 0`.
4. Cover the **happy path and the failure path** per use case.
5. A security or architecture invariant becomes a **negative check** (something that must NOT
   exist): `grep -l <forbidden> ...` must return **empty**.

## Recommended syntax: EARS

For **behavioural** criteria, write in EARS form (Easy Approach to Requirements Syntax):
`WHEN <condition> THE SYSTEM SHALL <observable behaviour>`. The criterion becomes a test
almost one to one — the condition is the arrange/act, the behaviour is the assert.

- ✅ "WHEN the push fails because of the network, THE SYSTEM SHALL retry up to four times
  with exponential backoff" → test: simulate the failure, count the attempts.
- ✅ "WHEN the working tree is dirty, THE SYSTEM SHALL abort without changing `main`" →
  test: dirty the tree, run it, check exit ≠ 0 and the hash intact.
- For **structural** criteria (a file exists, an invariant holds), the (command, expected)
  pair from step 3 remains the form.

## Anti-patterns (rewrite these)

- ❌ "the documentation is clear" → ✅ `grep -L "^description:" skills/*/SKILL.md` empty
  (it exists) plus an editorial review (an explicit human gate for "clear").
- ❌ "the read-only agents are safe" → ✅ `grep -lE "tools:.*(Write|Edit)" review security …`
  **empty** (a negative check).
- ❌ "good coverage" (gameable numeric target) → ✅ one happy plus one failure test per use
  case.

**Consumed by:** `spec-agent` and `plan-architect` (write them), `qa` (runs them), the `/dod`
command.
