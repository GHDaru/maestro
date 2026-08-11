---
description: Create or update the project constitution from interactive or provided principle inputs, ensuring all dependent templates stay in sync.
handoffs: 
  - label: Build Specification
    agent: speckit.specify
    prompt: Implement the feature specification based on the updated constitution. I want to build...
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

You are amending the project constitution at `docs/governance/principles.md`. **This file is the RATIFIED constitution, not a template**: it is written, versioned, installed into other repositories and packaged in the plugin. **Amend it in place — never regenerate it, never overwrite it.** Your job is to (a) collect/derive the values the amendment needs, (b) apply the smallest edit that expresses it, and (c) propagate the amendment across dependent artifacts.

> The upstream version of this command assumed a freshly scaffolded template full of `[TOKENS]` and told you to overwrite it. Pointing that at a real constitution is how a method loses its source of truth in one command — found by the independent review of cycle 048, in this very file.

**Note (Maestro divergence — declared in `.specify/UPSTREAM.md`)**: upstream keeps the constitution under its own memory directory, a path the Maestro installation never creates. Maestro has exactly ONE constitution, `docs/governance/principles.md`, which the installer ships. A second constitution file would be a lossy copy of the first (anti-pattern 22), and the installation never created that path anyway — which is the defect cycle 048 fixed.

Follow this execution flow:

1. Load the existing constitution at `docs/governance/principles.md`.
   - Read it whole. If it is already written (it is, in Maestro), there are no placeholder tokens to fill:
     identify instead the **specific principles the amendment touches**.
   - Only a constitution that is still a fresh scaffold has `[ALL_CAPS_IDENTIFIER]` tokens; filling those is
     the exception, not the flow.
   **IMPORTANT**: the number of principles is the project's decision, and changing it is an amendment like any
   other — argued, versioned and recorded, never a side effect of running this command.

2. Collect/derive values for placeholders:
   - If user input (conversation) supplies a value, use it.
   - Otherwise infer from existing repo context (README, docs, prior constitution versions if embedded).
   - For governance dates: `RATIFICATION_DATE` is the original adoption date (if unknown ask or mark TODO), `LAST_AMENDED_DATE` is today if changes are made, otherwise keep previous.
   - `CONSTITUTION_VERSION` must increment according to semantic versioning rules:
     - MAJOR: Backward incompatible governance/principle removals or redefinitions.
     - MINOR: New principle/section added or materially expanded guidance.
     - PATCH: Clarifications, wording, typo fixes, non-semantic refinements.
   - If version bump type ambiguous, propose reasoning before finalizing.

3. Draft the updated constitution content:
   - Replace every placeholder with concrete text (no bracketed tokens left except intentionally retained template slots that the project has chosen not to define yet—explicitly justify any left).
   - Preserve heading hierarchy and comments can be removed once replaced unless they still add clarifying guidance.
   - Ensure each Principle section: succinct name line, paragraph (or bullet list) capturing non‑negotiable rules, explicit rationale if not obvious.
   - Ensure Governance section lists amendment procedure, versioning policy, and compliance review expectations.

4. Consistency propagation checklist (convert prior checklist into active validations):
   - Read `.specify/templates/plan-template.md` and ensure any "Constitution Check" or rules align with updated principles.
   - Read `.specify/templates/spec-template.md` for scope/requirements alignment—update if constitution adds/removes mandatory sections or constraints.
   - Read `.specify/templates/tasks-template.md` and ensure task categorization reflects new or removed principle-driven task types (e.g., observability, versioning, testing discipline).
   - Read each command file in `.specify/templates/commands/*.md` (including this one) to verify no outdated references (agent-specific names like CLAUDE only) remain when generic guidance is required.
   - Read any runtime guidance docs (e.g., `README.md`, `CLAUDE.md`, or agent-specific guidance files if present). Update references to principles changed.
     (Maestro produces no quickstart: that function is served by the journey document and the recipes — `.specify/UPSTREAM.md`, rule 3.)

5. Produce a Sync Impact Report (prepend as an HTML comment at top of the constitution file after update):
   - Version change: old → new
   - List of modified principles (old title → new title if renamed)
   - Added sections
   - Removed sections
   - Templates requiring updates (✅ updated / ⚠ pending) with file paths
   - Follow-up TODOs if any placeholders intentionally deferred.

6. Validation before final output:
   - No remaining unexplained bracket tokens.
   - Version line matches report.
   - Dates ISO format YYYY-MM-DD.
   - Principles are declarative, testable, and free of vague language ("should" → replace with MUST/SHOULD rationale where appropriate).

7. Apply the amendment **in place** in `docs/governance/principles.md` — edit the lines that change and
   leave the rest byte-for-byte. Never rewrite the file from a template, and never regenerate it: the
   diff of this command must be readable as an amendment, not as a replacement.

8. Output a final summary to the user with:
   - New version and bump rationale.
   - Any files flagged for manual follow-up.
   - Suggested commit message (e.g., `docs: amend constitution to vX.Y.Z (principle additions + governance update)`).

Formatting & Style Requirements:

- Use Markdown headings exactly as in the template (do not demote/promote levels).
- Wrap long rationale lines to keep readability (<100 chars ideally) but do not hard enforce with awkward breaks.
- Keep a single blank line between sections.
- Avoid trailing whitespace.

If the user supplies partial updates (e.g., only one principle revision), still perform validation and version decision steps.

If critical info missing (e.g., ratification date truly unknown), insert `TODO(<FIELD_NAME>): explanation` and include in the Sync Impact Report under deferred items.

Do not create a new template; always operate on the existing `docs/governance/principles.md` file.
