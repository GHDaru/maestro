---
description: Execute the implementation planning workflow using the plan template to generate design artifacts.
handoffs: 
  - label: Create Tasks
    agent: speckit.tasks
    prompt: Break the plan into tasks
    send: true
  - label: Create Checklist
    agent: speckit.checklist
    prompt: Create a checklist for the following domain...
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before planning)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_plan` key
- If the YAML cannot be parsed or is invalid, skip hook checking silently and continue normally
- Filter out hooks where `enabled` is explicitly `false`. Treat hooks without an `enabled` field as enabled by default.
- For each remaining hook, do **not** attempt to interpret or evaluate hook `condition` expressions:
  - If the hook has no `condition` field, or it is null/empty, treat the hook as executable
  - If the hook defines a non-empty `condition`, skip the hook and leave condition evaluation to the HookExecutor implementation
- For each executable hook, output the following based on its `optional` flag:
  - **Optional hook** (`optional: true`):
    ```
    ## Extension Hooks

    **Optional Pre-Hook**: {extension}
    Command: `/{command}`
    Description: {description}

    Prompt: {prompt}
    To execute: `/{command}`
    ```
  - **Mandatory hook** (`optional: false`):
    ```
    ## Extension Hooks

    **Automatic Pre-Hook**: {extension}
    Executing: `/{command}`
    EXECUTE_COMMAND: {command}

    Wait for the result of the hook command before proceeding to the Outline.
    ```
- If no hooks are registered or `.specify/extensions.yml` does not exist, skip silently

## Outline

1. **Setup**: Run `.specify/scripts/bash/setup-plan.sh --json` from repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read FEATURE_SPEC and `docs/governance/principles.md`. Load IMPL_PLAN template (already copied).

3. **Execute plan workflow**: Follow the structure in IMPL_PLAN template to:
   - Fill Technical Context (mark unknowns as "NEEDS CLARIFICATION")
   - Fill Constitution Check section from constitution
   - Evaluate gates (ERROR if violations unjustified)
   - **Fill the "Artifacts of this cycle" table** — one `ART:<name>=yes|no` per conditional
     artifact, each with its reason. **This table decides what the phases below produce.**
     Declaring `=no` is a decision and is expected for documentation, method and tooling
     work; declaring `=yes` obligates the file to exist. Catalogue and criteria:
     `docs/governance/artifacts.md`. Verified by `scripts/check-conformance.sh`.
   - Phase 0: generate `research.md` **only if `ART:research=yes`**
   - Phase 1: generate `data-model.md` and `contracts/` **only for those declared `=yes`**
   - Phase 1: Update agent context by running the agent script
   - Re-evaluate Constitution Check post-design

4. **Stop and report**: the command ends after planning — there is no Phase 2 in this file
   (upstream residue, kept visible rather than silently renumbered). Report branch, IMPL_PLAN path, and generated artifacts.

5. **Check for extension hooks**: After reporting, check if `.specify/extensions.yml` exists in the project root.
   - If it exists, read it and look for entries under the `hooks.after_plan` key
   - If the YAML cannot be parsed or is invalid, skip hook checking silently and continue normally
   - Filter out hooks where `enabled` is explicitly `false`. Treat hooks without an `enabled` field as enabled by default.
   - For each remaining hook, do **not** attempt to interpret or evaluate hook `condition` expressions:
     - If the hook has no `condition` field, or it is null/empty, treat the hook as executable
     - If the hook defines a non-empty `condition`, skip the hook and leave condition evaluation to the HookExecutor implementation
   - For each executable hook, output the following based on its `optional` flag:
     - **Optional hook** (`optional: true`):
       ```
       ## Extension Hooks

       **Optional Hook**: {extension}
       Command: `/{command}`
       Description: {description}

       Prompt: {prompt}
       To execute: `/{command}`
       ```
     - **Mandatory hook** (`optional: false`):
       ```
       ## Extension Hooks

       **Automatic Hook**: {extension}
       Executing: `/{command}`
       EXECUTE_COMMAND: {command}
       ```
   - If no hooks are registered or `.specify/extensions.yml` does not exist, skip silently

## Phases

### Phase 0: Outline & Research

**This whole phase runs only if the plan declares `ART:research=yes`.** When it is `=no`,
stop here: the reason written in the declaration table is the record of that decision. The
gate is stated before the steps on purpose — an order issued first and qualified afterwards
is followed first and qualified never.

1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:

   ```text
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved — **produced only when the
plan declares `ART:research=yes`**. When it is `=no`, this phase is skipped and the reason
recorded in the declaration table is the record of that decision.

### Phase 1: Design & Contracts

**Prerequisites:** the declaration table is filled; `research.md` complete when it was
declared `=yes`.

**Items 1 and 2 below run only if the matching `ART:` token is `yes`.** An artifact that the
plan declared `=no` is not produced here, and the declaration is what stands as the decision
— silence would not (anti-pattern 22). **Item 3 has no token and always runs**: it updates
the agent context file, which is not a cycle artifact.

1. **Extract entities from feature spec** → `data-model.md` (`ART:data-model=yes`):
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Define interface contracts** → `/contracts/` (`ART:contracts=yes`):
   - Identify what interfaces the project exposes to users or other systems
   - Document the contract format appropriate for the project type
   - Examples: public APIs for libraries, command schemas for CLI tools, endpoints for web services, grammars for parsers, UI contracts for applications
   - A purely internal change (build scripts, one-off tooling) is the case for declaring
     `ART:contracts=no` **in the table**. Do not skip here after declaring `=yes`: the
     declaration is the only decider, and `scripts/check-conformance.sh` fails a `=yes`
     with no file.

3. **Agent context update**:
   - Run `.specify/scripts/bash/update-agent-context.sh claude`
   - These scripts detect which AI agent is in use
   - Update the appropriate agent-specific context file
   - Add only new technology from current plan
   - Preserve manual additions between markers

**Output**: the artifacts declared `=yes` in the table, plus the agent-specific file.

**`quickstart.md` is not produced in Maestro.** Its function — how someone tries the thing —
is served by the journey document (`.specify/templates/journey-template.md`) and by the
recipes, and Principle VI forbids duplicating a function already served. Divergence from
upstream recorded in `.specify/UPSTREAM.md`.

## Key rules

- Use absolute paths
- ERROR on gate failures or unresolved clarifications
