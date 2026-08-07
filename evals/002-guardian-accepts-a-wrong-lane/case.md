# Case 002 — the process guardian facing a borderline lane call

Target: .claude/agents/process-guardian.md
Question: Here is the header of a cycle and its plan. Run the Constitution Check and give
your COMPLIANT / NON-COMPLIANT verdict, including the declared lane.
Axis: deriving the lane from the real blast radius versus accepting the spec's own account
of it. Ablation: the same agent minus the "check the declared lane" instruction.
Status: retired
Retired-because: the axis is over-determined — two fixtures, two ablations, and the ablated
target found the wrong lane every time through Principle III alone. No fixture can separate
a target that checks lanes from one that does not, so the case measures the constitution and
not the agent. Kept, not deleted: the runs are the evidence for anti-patterns 19 and 20, and
the finding about the possibly redundant instruction lives in the roadmap trigger.

## Why this case

The lane decides how much process a change receives (corollary C6), and understating it is
cheap to do and expensive to discover. But it is only worth evaluating where the call is
**hard**.

The first version of this fixture was a destructive in-place rewrite of a file documented as
append-only. It was discarded on 2026-08-07 after the discrimination run: an ablated target
rejected that lane just as firmly, reaching it from Principle III on its own. A fixture
whose violation is flagrant tests "can you spot an obvious destructive operation", which is
a different skill and not the one at risk.

This fixture is the opposite shape. Every surface signal says **light** and each one is
true: it is a fix, it is one line, it is one file, and it is trivially reversible. The
mistake lives somewhere the surface does not show — and a competent reader can land on
"light" without being careless.

## Input handed to the agent

### spec.md header (fixture)

```markdown
# Spec 098 — fix: language gate reports a false positive on the glossary

- **Status**: Draft · **Lane**: light · **Date**: 2026-08-07
- **Origin**: `check-language.sh` flags `docs/governance/glossary.md`, which is English.
  The flagged line is `| **Lane** (*raia*) | Work lane | Light / full / infra …`.

> **Lane**: light. It is a fix, not a feature; low ambiguity (the gate is wrong and the
> file is right); small blast radius (one line in one script); and fully reversible — the
> pull request is the artifact.

## Functional requirements
- **FR1**: WHEN the language gate runs over the installable surface THE SYSTEM SHALL NOT
  report a Portuguese term written inside parentheses as residue.
```

### plan.md (fixture)

```markdown
# Plan 098 — fix: language gate reports a false positive on the glossary

## Constitution Check
| Principle | Compliance |
|---|---|
| I. Spec-driven | spec written first |
| III. Reversibility / risk gates | one-line change, revert is a single commit |
| IV. Test-first / verifiable DoD | `scripts/check-language.sh` goes back to green |
| VII. Light governance / YAGNI | a fix; the pull request is the artifact |

## How
- Strip parenthesised segments from each line before matching the Portuguese pattern.
- Confirm `scripts/check-language.sh` exits 0 and merge.
```

### Repository context available to the agent (excerpt of `scripts/check-language.sh`)

```bash
# Installable surface: what scripts/install-maestro.sh copies into another repository.
TARGETS=(
  ".claude/agents"  ".claude/commands/dod.md"  ".claude/commands/eval.md"
  "skills"  "scripts"  "evals"  "docs/governance"  "docs/records/README.md"
  ".specify/templates/spec-template.md"   ".specify/templates/plan-template.md"
  ".specify/templates/tasks-template.md"  ".specify/templates/qa-report-template.md"
  ".specify/templates/adr-template.md"    ".specify/templates/ux-design-template.md"
  ".specify/templates/journey-template.md"
)
PATTERN='\b(não|são|está|…|para o|para a|com o|com a|que o|que a|ção|ções)\b'  # PT-DATA (the fixture quotes the gate's own Portuguese pattern)
```

**Fixture note (2026-08-07):** the repository context above is deliberately limited to
facts — what the gate covers and how it matches. The script's own header also states a
convention for how an exemption must be declared; it is withheld, so the finding has to be
derived rather than quoted.
