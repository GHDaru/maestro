# Contracts 056 — the two interfaces the harness sits on

Verified against the public reference (`code.claude.com/docs/en/hooks-reference`) before a
line was written. Field names below are **exact**; guessing them is how a hook becomes a file
that runs and decides nothing.

## 1. `PreToolUse` — what the guard receives and what it must answer

**In (stdin, JSON).** The fields the guard reads are marked ✅; the rest arrive and are ignored.

| Field | Used | Content |
|---|---|---|
| `hook_event_name` | ✅ | `"PreToolUse"` — the guard answers nothing for any other event |
| `tool_name` | ✅ | `"Edit"`, `"Write"`, `"Bash"`… the matcher already filters, and the guard re-checks |
| `tool_input` | ✅ | tool-shaped; the guard reads `file_path`, and also `notebook_path` and `path`, because the write tools do not all use the same name |
| `cwd` | ✅ | the project root a relative `file_path` resolves against |
| `session_id`, `prompt_id`, `transcript_path`, `permission_mode`, `tool_use_id` | — | present, unused |

**Out (stdout, JSON).** To refuse:

```json
{"hookSpecificOutput": {
   "hookEventName": "PreToolUse",
   "permissionDecision": "deny",
   "permissionDecisionReason": "why, and the correct route"}}
```

`permissionDecision` accepts `"allow"`, `"deny"` or `"ask"` — this guard only ever uses
`"deny"`. Exit **0** is enough — refusal is carried
by the field, not by the exit code. Exit **2** would block regardless of the JSON, and the
guard deliberately never uses it: a refusal without a stated reason is a wall, not a gate.

To allow: print nothing, exit 0.

**Failure mode, declared.** Any internal error → the guard prints the cause on `stderr` and
**allows**. A broken guard must not freeze somebody else's repository. What stops a broken
guard from passing unnoticed is not the guard: it is the assertion in `check-installed.sh`
that runs it and requires a refusal (FR6).

## 2. `SessionStart` — what the state hook may return

**In (stdin, JSON)**: `session_id`, `hook_event_name`, `cwd`, `permission_mode`,
`transcript_path`, and — the one that matters — **`source`**, which carries which of
`startup` · `resume` · `clear` · `compact` · `fork` fired. The first version of this table
omitted `source` and listed the values as if they were the input itself.

`.claude/settings.json` wires four of the five and **drops `fork`** on purpose: a forked
session inherits the parent's context, so re-printing the state would duplicate it.

**Out**: unique among the events — **plain stdout is added to the context Claude sees**
(`additionalContext` in JSON does the same). It cannot block; a non-zero exit only shows
stderr to the user.

That is why the state hook writes plain text: the measured facts enter the session as
context, so the method's state is **loaded** instead of remembered (corollary C13).

## 3. Merging into a third party's `.claude/settings.json`

The installer never `cp`s over this file. Three states, three behaviours:

| Target state | Behaviour |
|---|---|
| no `settings.json` | write ours |
| exists, `hooks` absent **or empty** (`null`, `{}`, `[]`) | add `hooks`; every key and value preserved — but the document is re-serialised with `indent=2`, so whitespace and inline formatting are **not** preserved. (The first version of this line claimed "byte for byte", which was false.) |
| exists, `hooks` **identical to ours** | `CURRENT` — nothing to do, and **not** a conflict. Without this state the installer conflicted with itself on every re-run and the harness could never be upgraded. |
| exists with **different** `hooks` | **refuse**, print the snippet (`--snippet`, valid JSON on its own), change nothing |

The third case is a refusal and not a merge on purpose: two hook configurations for the same
event are a behaviour question only the repository's owner can answer, and this installer
already learned in cycles 051 and 052 what it costs to decide for somebody else.
