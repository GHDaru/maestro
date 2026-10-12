#!/usr/bin/env python3
"""record-task.py — appends one event to the task ledger (append-only).

The ledger answers "what did each task cost, in tokens and money, and how many attempts did it
take to be approved?" with facts written at the moment they happened, never reconstructed.
It is written by the `maestro-ledger` mod; a human or another script may also call it.

One JSON object per line in docs/records/tarefas.jsonl. A past line is never edited: a
correction is a new event. Several sessions write at once, so the line is written with ONE
O_APPEND write, repeated until the whole line is out (a short write is never silent). On
POSIX the kernel positions every O_APPEND write at the end of the file atomically, so concurrent
writers do not interleave; no lock file is needed (flock is absent on macOS and on Windows' Git
Bash, where this must also run). Declared limit: on Windows, Python's O_APPEND is a seek to the
end followed by the write, which is NOT atomic across processes — there, simultaneous writers
can in theory overwrite each other, and a line that is a few KB long is the likelier victim.

Usage:  scripts/record-task.py '<one-line json>'
        MAESTRO_TASK_LEDGER=<path> overrides the ledger file (tests, central ledgers).
Exit:   0 recorded · 1 rejected (the reason is on stderr) · 2 usage
"""
import json
import os
import sys
from datetime import datetime

LEDGER = os.environ.get("MAESTRO_TASK_LEDGER", os.path.join("docs", "records", "tarefas.jsonl"))

EVENTS = {"assigned", "start", "stop", "verdict"}
KINDS = {"spec", "plan", "implement", "test", "review", "audit", "fix", "docs", "research"}
OUTCOMES = {"delivered", "blocked", "failed", "interrupted", "superseded"}
VERDICTS = {"approved", "approved_with_notes", "rejected"}


def is_text(value):
    return isinstance(value, str) and bool(value)


def is_iso8601(value):
    if not isinstance(value, str):
        return False
    try:
        datetime.fromisoformat(value[:-1] + "+00:00" if value.endswith("Z") else value)
    except ValueError:
        return False
    return True


def problems(rec):
    """Every reason the record cannot enter the ledger; empty when it can."""
    found = []
    for field in ("ts", "event", "task_id"):
        if not rec.get(field):
            found.append(f"missing required field: {field}")
    if rec.get("ts") and not is_iso8601(rec["ts"]):
        found.append("ts must be an ISO 8601 timestamp")
    if "task_id" in rec and not is_text(rec["task_id"]):
        found.append("task_id must be a non-empty string")
    if "session" in rec and not is_text(rec["session"]):
        found.append("session must be a non-empty string")
    # Vocabulary checks: a non-string never reaches a set lookup (a list would raise TypeError).
    if rec.get("event") and (not isinstance(rec["event"], str) or rec["event"] not in EVENTS):
        found.append(f"event must be one of {sorted(EVENTS)}")
    if "kind" in rec and (not isinstance(rec["kind"], str) or rec["kind"] not in KINDS):
        found.append(f"kind must be one of {sorted(KINDS)}")
    # bool is an int in Python: `true` would pass isinstance(…, int) and poison the report.
    if "attempt" in rec and not (type(rec["attempt"]) is int and rec["attempt"] >= 1):
        found.append("attempt must be an integer >= 1")
    if "outcome" in rec and (not isinstance(rec["outcome"], str) or rec["outcome"] not in OUTCOMES):
        found.append(f"outcome must be one of {sorted(OUTCOMES)}")
    if "verdict" in rec and (not isinstance(rec["verdict"], str) or rec["verdict"] not in VERDICTS):
        found.append(f"verdict must be one of {sorted(VERDICTS)}")
    if rec.get("event") == "verdict":
        if not rec.get("verdict"):
            found.append("a verdict event needs a verdict")
        if not is_text(rec.get("by")):
            found.append("a verdict event needs `by` (the id of the audit or review task)")
    return found


def main(argv):
    if len(argv) != 2:
        print("usage: record-task.py '<one-line json>'", file=sys.stderr)
        return 2
    try:
        rec = json.loads(argv[1])
    except json.JSONDecodeError as exc:
        print(f"error: invalid JSON ({exc})", file=sys.stderr)
        return 1
    if not isinstance(rec, dict):
        print("error: the record must be a JSON object", file=sys.stderr)
        return 1
    errors = problems(rec)
    if errors:
        for err in errors:
            print(f"error: {err}", file=sys.stderr)
        return 1

    line = (json.dumps(rec, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
    os.makedirs(os.path.dirname(LEDGER) or ".", exist_ok=True)
    fd = os.open(LEDGER, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
    try:
        view = memoryview(line)
        while view:  # normally one write; a short one is finished, never dropped
            written = os.write(fd, view)
            if written <= 0:
                raise OSError("write to the ledger made no progress")
            view = view[written:]
    finally:
        os.close(fd)
    print(f"ok: {rec['event']} {rec['task_id']} recorded in {LEDGER}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
