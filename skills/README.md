# Maestro skills (community `SKILL.md` standard)

A skill is a recurring procedure packaged as `skills/<slug>/SKILL.md` — front matter with
`name` and `description` (carrying the **trigger**: "Use it when…") plus a body of steps. It
fires on its own in the right context, standardising execution without depending on the
human's memory.

**Birth rule (YAGNI plus test-first):** a skill only exists from **proven recurring pain**
(retrospectives and cycles), never speculation — and a new original skill ships only with a
**tested baseline** (pressure scenario: the agent fails WITHOUT the skill, complies WITH it —
see the protocol in `skill-author`). Every skill carries its **Iron Law** (the non-negotiable
rule, with the loopholes closed). Author: the `skill-author` agent.

## Catalogue

| Skill | What for | Born from | Consumed by |
|---|---|---|---|
| [`constitution-check`](./constitution-check/SKILL.md) | The Principles I–VIII table in `plan.md` | Rewritten by hand in cycles 003 and 004 | `plan-architect`, `process-guardian` |
| [`verifiable-dod`](./verifiable-dod/SKILL.md) | Acceptance criterion → fitness function (grep, ls, test) | Checks rewritten identically every cycle | `spec-agent`, `qa`, the `/dod` command |
| [`fight-the-pile-up`](./fight-the-pile-up/SKILL.md) | Editorial review against the "pile-up" | Steward feedback on dense documents | `didactics-editor`, `tech-writer` |
| [`anti-patterns`](./anti-patterns/SKILL.md) | Catalogue of what NOT to do (context, orchestration, quality, process, verification) | Retrospectives of cycles 001–008 and 017–020 | every agent; `review`, `process-guardian` |
| [`diagnose-before-fix`](./diagnose-before-fix/SKILL.md) | Root cause before any fix (Iron Law plus six phases) | A real gap in debugging discipline (cycle 011) | `dev-implementer`, `qa` |
| [`living-journey`](./living-journey/SKILL.md) | Document plus screenshots from the real build plus a **dated** heuristic, in the same pull request | Cycle 018 gap: the model prescribed a journey document with no skill and no template | `qa`, `tech-writer`, `ux-semantics` |

## Skills versus commands versus agents

- **Skill** (`skills/*/SKILL.md`) — *how to do* a procedure; fires from context.
- **Command** (`.claude/commands/*.md`) — explicit invocation (`/dod`, `/speckit.*`).
- **Agent** (`.claude/agents/*.md`) — *who does it*; consumes skills and commands.

For example: the `verifiable-dod` skill helps you **write** the checks; the `/dod` command
**runs** them.

## Next ones (from retrospectives, not speculation)

Candidates when the pain shows up: preparing a pull request, opening a cycle.
