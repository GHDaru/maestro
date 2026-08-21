#!/usr/bin/env python3
"""PreToolUse guard: refuse to REWRITE what the method declares unrewritable.

Why this exists. The method declares artifacts that must never be rewritten — the body of a
committed ADR, past lines of the decision index, the dated idea cards of the ecosystem
catalogue. Measured in cycle 056: NOTHING enforced any of them. Every `check-*.sh` touching
those paths checks shape or index, never immutability. The rule lived in prose an agent had
to have read and remembered — the defect this repository has chased since cycle 042, sitting
in the middle of its own governance. A gate audits after the damage; this refuses before it.

What "immutable" means here, precisely: **once it is in git history**. Authoring an ADR takes
several tool calls — write the skeleton, fill in Consequences, fix a typo — and refusing the
second call would block the very thing the method asks for. So a file that git does not track
yet is being WRITTEN, and a file git tracks is being REWRITTEN. That line is a fact on disk,
not a guess. (The first version treated "the file exists" as immutable and blocked ADR
authoring from the second call on — found by the independent review of this cycle.)

Declared limits, so nobody mistakes this for total coverage:
  * `Bash` is not guarded. For `docs/records/decisoes.jsonl` there is a positive reason — the
    sanctioned route IS a Bash command (`scripts/record-decision.sh`), so guarding Bash would
    block what every refusal here points at. For ADR bodies and idea cards there is no such
    reason: `sed -i` reaches them and this guard does not. Stated, not excused.
  * `docs/ecosystem/estado.jsonl` is declared append-only by the method and is NOT guarded:
    unlike the decision index it has no append script, so refusing writes would leave no way
    to record a verdict at all. Recorded as a finding in cycle 056 rather than half-fixed.
  * Paths outside this repository are never judged. The rules are confined to the project
    root, so a nested checkout or another repo's `docs/adr/` is somebody else's business.

Contract: specs/056-instalar-o-harness/contracts/hook-io.md
"""
import json
import os
import re
import subprocess
import sys

WRITE_TOOLS = {"Edit", "Write", "NotebookEdit", "MultiEdit"}

# (matcher, tracked-by-git means immutable?, reason naming the CORRECT ROUTE)
# `IGNORECASE` because macOS and Windows filesystems are case-insensitive: `DOCS/adr/x.md`
# reaches the same inode, and a case-sensitive rule would be a live bypass there.
RULES = (
    (
        re.compile(r"(^|/)docs/records/decisoes\.jsonl$", re.IGNORECASE),
        False,  # never editable, tracked or not: the route is a script, not an editor
        "docs/records/decisoes.jsonl is append-only: a past line is never edited. "
        "Append instead: scripts/record-decision.sh '<one-line json>' — a correction is a "
        "NEW line whose status supersedes the old one.",
    ),
    (
        re.compile(r"(^|/)docs/adr/\d{4}-[^/]+\.md$", re.IGNORECASE),
        True,
        "the body of a committed ADR is immutable: a reversal is a NEW ADR that supersedes "
        "it, and the old one is left standing. Create docs/adr/<next>-<slug>.md and mark the "
        "old row superseded in the ADR index. (An ADR you are still authoring — not yet "
        "committed — is not blocked.)",
    ),
    (
        re.compile(r"(^|/)docs/ecosystem/ideias/\d{3}-[^/]+\.md$", re.IGNORECASE),
        True,
        "an idea card is a DATED OBSERVATION and is immutable once committed: rewriting it "
        "erases what was seen and when. Today's verdict goes in a new line of "
        "docs/ecosystem/estado.jsonl; the card keeps the verdict of its own date.",
    ),
)


def target_path(tool_input):
    """The file a write tool aims at, whatever it calls the field."""
    for key in ("file_path", "notebook_path", "path"):
        value = tool_input.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return None


def tracked_by_git(root, absolute):
    """Is this path in git history? That, not mere existence, is what makes it immutable."""
    try:
        result = subprocess.run(
            ["git", "ls-files", "--error-unmatch", "--", absolute],
            cwd=root,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=5,
        )
        return result.returncode == 0
    except Exception:
        # No git, or git is slow: fall back to "it exists". Conservative in the direction
        # that protects, and the ADR-authoring case is the one that suffers — rare enough
        # to prefer over leaving history rewritable.
        return os.path.isfile(absolute)


def decide(event):
    if event.get("hook_event_name") != "PreToolUse":
        return None
    if event.get("tool_name") not in WRITE_TOOLS:
        return None

    tool_input = event.get("tool_input")
    if not isinstance(tool_input, dict):
        return None
    raw = target_path(tool_input)
    if not raw:
        return None

    root = os.path.realpath(event.get("cwd") or os.getcwd())
    absolute = raw if os.path.isabs(raw) else os.path.join(root, raw)
    # realpath, never normpath: a symlink pointing at docs/adr/0001-x.md is a write to that
    # file, and Edit/Write follow it. Lexical normalisation was a live bypass in three
    # variants (independent review of cycle 056; the installer had learned the same lesson
    # in cycle 052 and the guard had not).
    resolved = os.path.realpath(absolute)

    # Confined to this project: another repository's docs/adr/ is not ours to police.
    try:
        relative = os.path.relpath(resolved, root)
    except ValueError:
        return None
    if relative.startswith(".."):
        return None
    relative = relative.replace(os.sep, "/")

    for matcher, immutable_when_tracked, reason in RULES:
        if not matcher.search(relative):
            continue
        if immutable_when_tracked and not tracked_by_git(root, resolved):
            return None  # still being authored — exactly what the method wants
        return reason
    return None


def main():
    try:
        event = json.load(sys.stdin)
        reason = decide(event)
    except Exception as exc:  # fail OPEN, and loudly — see the module docstring
        print(f"maestro guard: not evaluated ({exc.__class__.__name__}: {exc})", file=sys.stderr)
        return 0

    if reason is None:
        return 0

    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": f"Maestro: {reason}",
            }
        },
        sys.stdout,
    )
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
