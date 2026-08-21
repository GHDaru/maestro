#!/usr/bin/env python3
"""Decide what to do with a third party's .claude/settings.json — never overwrite it.

Somebody else's configuration is not ours. The verdict is the first word on stdout so the
shell can branch without parsing JSON:

    WRITE     no settings.json at the target — the caller may copy ours
    CURRENT   it already carries exactly our hooks — nothing to do, and NOT a conflict
    MERGED    no hooks configured (absent, null, {} or []) — the merged document follows
    CONFLICT  it configures DIFFERENT hooks — the caller refuses; `--snippet` prints what to add
    ERROR     unreadable, or not a JSON object — the caller refuses and changes nothing

`CURRENT` exists because without it the installer conflicted with **itself**: the settings
file is written by `cp`, so it never enters the manifest, and every re-run saw our own hooks
and refused to upgrade them (independent review of cycle 056).

Note on fidelity: the merged document is re-serialised with `indent=2`. Keys and values are
preserved exactly; whitespace and inline formatting are not. Said plainly because the first
version of the contract claimed "byte for byte", which was false.

Usage: merge-settings.py <target-settings.json> <source-settings.json> [--snippet]
"""
import json
import sys


def load(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    snippet = "--snippet" in argv[1:]
    if len(args) != 2:
        print("ERROR usage: merge-settings.py <target> <source> [--snippet]")
        return 0
    target, source = args

    try:
        ours = load(source)
    except Exception as exc:
        print(f"ERROR cannot read our own settings ({exc})")
        return 0

    if snippet:
        # Only the `hooks` object, valid on its own. Printing from `/"hooks"/,$p` dragged the
        # document's closing brace along and produced unbalanced JSON — a "snippet to paste"
        # that broke whatever it was pasted into (independent review of cycle 056).
        print(json.dumps({"hooks": ours.get("hooks", {})}, indent=2, ensure_ascii=False))
        return 0

    try:
        theirs = load(target)
    except FileNotFoundError:
        print("WRITE")
        return 0
    except Exception as exc:
        print(f"ERROR {exc}")
        return 0

    if not isinstance(theirs, dict):
        print("ERROR the existing settings.json is not a JSON object")
        return 0

    existing = theirs.get("hooks")
    if existing == ours.get("hooks"):
        print("CURRENT")
        return 0
    if existing in (None, {}, []):
        # Present-but-empty counts as "nothing configured": merging adds, it displaces nothing.
        theirs["hooks"] = ours.get("hooks", {})
        print("MERGED")
        print(json.dumps(theirs, indent=2, ensure_ascii=False))
        return 0

    print("CONFLICT")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
