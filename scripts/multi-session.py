"""Multi-session launcher: opens the builder sessions of a cycle in Windows Terminal.

Adapted from the Hindiana project's launcher (hindiana/scripts/multi-session.py, 24/09/2026)
for cycle 066. Three things changed, each from a recorded decision
(decisao-066-sessoes-via-gateway, decisao-066-daru-20-10):

  * one `--model` per session: the Gerente runs on one model, the Workers on another
    (`claude --model` beats settings.local.json and ANTHROPIC_MODEL for that session);
  * one git worktree per Worker (`.claude/worktrees/<name>`), so a Worker's edits and
    commits cannot touch another Worker's files — six sessions in one checkout had no
    isolation (security review, finding 2);
  * no secret here and none in the repository: ANTHROPIC_AUTH_TOKEN lives in the user's
    ~/.claude/settings.json; this script only passes the model.

Usage:
  python scripts/multi-session.py . --dry-run                    # print what would open
  python scripts/multi-session.py . --resume                     # Gerente + 6 Workers
  python scripts/multi-session.py . --count 3 --resume           # Gerente + 2 Workers
  python scripts/multi-session.py . --gerente-model glm-5.3 --worker-model deepseek-v4.1-flash --resume
"""
from __future__ import annotations

import argparse
import base64
import os
import shutil
import subprocess
import sys
import time

CLAUDE_EXE = os.path.expanduser(r"~\.local\bin\claude.exe")
NAMES = ["Gerente", "Worker01", "Worker02", "Worker03", "Worker04", "Worker05", "Worker06"]
COLORS = ["DarkRed", "DarkCyan", "DarkGreen", "DarkYellow", "DarkMagenta", "DarkBlue", "Cyan"]


def _encode_ps(script: str) -> str:
    return base64.b64encode(script.encode("utf-16-le")).decode("ascii")


def worktree_for(root: str, name: str, base: str, dry: bool) -> str:
    """One worktree per Worker under .claude/worktrees/<name>, branched from `base`."""
    path = os.path.join(root, ".claude", "worktrees", name.lower())
    if os.path.isdir(path):
        return path
    cmd = ["git", "-C", root, "worktree", "add", "-b", f"w/{name.lower()}", path, base]
    if dry:
        print("  would run:", " ".join(cmd))
        return path
    subprocess.run(cmd, check=True)
    return path


def ps_for(name: str, role: str, color: str, cwd: str, model: str) -> str:
    claude = f"& '{CLAUDE_EXE}' --name '{name}' --model '{model}'"
    return (
        "Remove-Item Env:CLAUDE_CODE_CHILD_SESSION -ErrorAction SilentlyContinue; "
        "$env:CLAUDE_CODE_FORCE_SESSION_PERSISTENCE = '1'; "
        f"Set-Location '{cwd}'; "
        f"$Host.UI.RawUI.WindowTitle = '{name} - {role} - {model}'; "
        f"Write-Host '=== {name} ({role}, {model}) ===' -ForegroundColor {color}; "
        f"Write-Host 'Folder: {cwd}' -ForegroundColor Gray; "
        f"{claude}"
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project_path")
    ap.add_argument("--count", type=int, default=7, help="sessions to open, Gerente first (1-7)")
    ap.add_argument("--gerente-model", default="glm-5.3")
    ap.add_argument("--worker-model", default="deepseek-v4.1-flash")
    ap.add_argument("--base", default="HEAD", help="branch/commit the Worker worktrees start from")
    ap.add_argument("--resume", action="store_true", help="actually open Windows Terminal")
    ap.add_argument("--dry-run", action="store_true", help="print the plan, open nothing")
    a = ap.parse_args()

    root = os.path.abspath(a.project_path)
    count = max(1, min(a.count, len(NAMES)))
    dry = a.dry_run or not a.resume

    sessions = []
    for i in range(count):
        name = NAMES[i]
        role = "Gerente" if i == 0 else f"Worker {i:02d}"
        model = a.gerente_model if i == 0 else a.worker_model
        cwd = root if i == 0 else worktree_for(root, name, a.base, dry)
        sessions.append((name, role, COLORS[i], cwd, model))

    print(f"\n=== Multi-session ({count}) in {root} ===")
    for name, role, _, cwd, model in sessions:
        print(f"  {name:9} {role:10} {model:22} {cwd}")

    if dry:
        print("\n[dry-run] nothing opened. Use --resume to open.")
        return 0

    wt = shutil.which("wt.exe") or os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WindowsApps\wt.exe")
    if not os.path.isfile(wt):
        print("error: wt.exe (Windows Terminal) not found.", file=sys.stderr)
        return 1

    def pane(s):
        return f"powershell -NoExit -EncodedCommand {_encode_ps(ps_for(*s))}"

    def run(cmd, delay=0.6):
        os.system(cmd)
        time.sleep(delay)

    gerente, workers = sessions[0], sessions[1:]
    run(f"wt {pane(gerente)}", 1.0)
    n = len(workers)
    if n >= 3:
        run(f"wt -w 0 split-pane -H -s 0.5 {pane(workers[2])}")
        for i in range(3, n):
            j = n - i
            run(f"wt -w 0 split-pane -V -s {j / (j + 1):.3f} {pane(workers[i])}")
        run("wt -w 0 move-focus up", 0.3)
    for w in workers[:2]:
        run(f"wt -w 0 split-pane -V -s 0.5 {pane(w)}")
    print(f"\n[OK] {count} session(s) opened.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
