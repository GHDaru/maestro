#!/usr/bin/env python3
"""Stop hook: the method checks itself at the moment work would be handed over.

Why this exists. "Am I following the method?" must never be answered from memory (C13), and
SessionStart only loads the measured state ONCE, at the start. Hours later, when the agent says
"done", nothing measured anything. This hook measures then — without anybody asking.

What it measures: `scripts/check-conformance.sh --ticked-only NNN`, where NNN is the NEWEST
cycle only — the one being written, discovered the same way session-state.sh does. This is the
half of the conformance gate that is never red on work in progress (cycle 061): a TAIL box
ticked with no evidence under it. An open cycle with nothing ticked passes.

Why only the newest cycle. Without NNN the gate walks every cycle from its floor, and the
old ones are closed history: ticking nothing is not an option for them, and the plugin check
(`TAIL:gate`, which runs `package-plugin.sh --verify`) turns red the moment a skill is edited
and not yet repackaged — ordinary work in progress. Measuring them blocked the agent for
things it cannot and must not fix. With NNN the plugin check still runs, but only when the
newest cycle itself ticked TAIL:gate — a claim THIS cycle made and can make true.

What it does when the measure is red:
  * first time → `{"decision": "block", "reason": ...}`: Claude Code does not let the agent
    stop; the agent reads the failing lines and keeps working. The reason is made of the
    gate's own ✗ lines and nothing else: no canned remedy, because the right one depends on
    the line, and "untick the box" would rewrite a closed cycle's history.
  * the agent already continued once because of this hook (`stop_hook_active`) → it does NOT
    block again (an agent that cannot fix it would loop forever and burn tokens). It lets the
    stop happen and tells the HUMAN through `systemMessage`. The gate escalates, it never loops.

Declared limits, so nobody mistakes this for total coverage:
  * It measures artifacts, not quality — the same limit as the script it calls.
  * It fails OPEN, loudly: a crash or a timeout never blocks the agent; it prints why to stderr.
  * A repository without `scripts/check-conformance.sh` is not judged: the method is not here.
  * The root is $CLAUDE_PROJECT_DIR (Claude Code sets it for hooks). The event's `cwd` is only
    a reserve for when it is unset: `cwd` moves with the agent (a subdirectory, another
    repository), and running `scripts/check-conformance.sh` from wherever it points would
    execute somebody else's script. When the variable exists, nothing outside it is run.

Contract: stdin = Claude Code's Stop hook JSON; stdout = nothing, or one JSON object; exit 0.
"""
import json
import os
import re
import subprocess
import sys

CHECK = os.path.join("scripts", "check-conformance.sh")
TIMEOUT_S = 90
MAX_LINES = 6


def failing_lines(output):
    """The actionable lines: what the gate marked as failing, nothing else."""
    lines = [line.strip() for line in output.splitlines() if "✗" in line]
    return lines[:MAX_LINES]


def project_root(event):
    """$CLAUDE_PROJECT_DIR when Claude Code gave it; the event's cwd only as a reserve."""
    declared = os.environ.get("CLAUDE_PROJECT_DIR")
    if declared and os.path.isdir(declared):
        return os.path.realpath(declared)
    return os.path.realpath(event.get("cwd") or os.getcwd())


def newest_cycle(root):
    """NNN of the highest specs/NNN-*/ directory, or None — the cycle being written."""
    specs = os.path.join(root, "specs")
    if not os.path.isdir(specs):
        return None
    names = sorted(
        name for name in os.listdir(specs)
        if re.match(r"^\d{3}-", name) and os.path.isdir(os.path.join(specs, name))
    )
    return names[-1][:3] if names else None


def decide(event):
    if event.get("hook_event_name") != "Stop":
        return None
    root = project_root(event)
    if not os.path.isfile(os.path.join(root, CHECK)):
        return None  # the method is not installed here; say nothing
    cycle = newest_cycle(root)
    if cycle is None:
        return None  # method installed, no cycle opened yet: nothing to be non-conformant about

    result = subprocess.run(
        ["bash", CHECK, "--ticked-only", cycle],
        cwd=root,
        capture_output=True,
        # errors="replace": the gate truncates its evidence lines by BYTES, so a line can end
        # in half of an accented character. Strict decoding raised, the hook failed open, and
        # the check silently never ran — found by this hook's own first test run.
        encoding="utf-8",
        errors="replace",
        timeout=TIMEOUT_S,
    )
    if result.returncode == 0:
        return None

    lines = failing_lines(result.stdout + "\n" + result.stderr) or [
        f"check-conformance.sh --ticked-only {cycle} exited {result.returncode} (no ✗ line printed)"
    ]
    detail = "\n".join(f"  {line}" for line in lines)

    if event.get("stop_hook_active"):
        return {
            "systemMessage": "Maestro: conformance is still RED after one attempt to fix it. "
            "The agent was allowed to stop so it does not loop; a human decides now.\n" + detail
        }
    return {
        "decision": "block",
        "reason": f"Maestro self-check (Stop hook): the conformance gate is red for cycle {cycle}. "
        "Do not hand the work over yet. Fix what these lines say, then run "
        f"`scripts/check-conformance.sh --ticked-only {cycle}` and show its output.\n"
        + detail,
    }


def main():
    try:
        event = json.load(sys.stdin)
        verdict = decide(event)
    except Exception as exc:  # fail OPEN, and loudly
        print(f"maestro stop-check: not evaluated ({exc.__class__.__name__}: {exc})", file=sys.stderr)
        return 0
    if verdict is not None:
        json.dump(verdict, sys.stdout, ensure_ascii=False)
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
