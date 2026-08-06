#!/usr/bin/env bash
# check-boundary.sh — the split between the two repositories is machine-checkable
# BEFORE anything moves (ADR 0017).
#
# What this actually measures (anti-pattern 13): it does not verify that the split
# happened. It verifies that the split is **decidable** — that every tracked file has
# exactly one owner, that the mirror has a direction, and that no published page depends
# on a path nobody claimed. Those are the three ways a repository split goes wrong
# silently, and all three are checkable while the files are still in one place.
#
# Invariants:
#   1. every tracked file belongs to exactly one repository (no orphan, no double claim)
#   2. every mirrored path is owned by the toolkit (a mirror without a source is a fork)
#   3. every page in publicar/sumario.json comes from a guide path or a mirrored one
#
# Source of truth: boundary.json. Exit 0 only when all three hold.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

[[ -f boundary.json ]] || { echo "✗ boundary.json missing — the split has no source of truth." >&2; exit 1; }

python3 - <<'PY'
import json, subprocess, sys

b = json.load(open("boundary.json"))
repos = b["repos"]
mirrored = [p for p in b["mirrored"]["paths"]]
allowed = b.get("unclassified_allowed", [])

def owner(path):
    """The repository that claims this path, or None. Longest prefix wins."""
    hits = []
    for key, repo in repos.items():
        for own in repo["owns"]:
            if path == own or path.startswith(own):
                hits.append((len(own), key))
    if not hits:
        return None
    hits.sort(reverse=True)
    best = hits[0][0]
    winners = {k for ln, k in hits if ln == best}
    return "AMBIGUOUS" if len(winners) > 1 else hits[0][1]

files = subprocess.run(["git", "ls-files"], capture_output=True, text=True).stdout.split()
fail = 0
orphans, ambiguous = [], []
count = {k: 0 for k in repos}

for f in files:
    if any(f.startswith(a) for a in allowed):
        continue
    o = owner(f)
    if o is None:
        orphans.append(f)
    elif o == "AMBIGUOUS":
        ambiguous.append(f)
    else:
        count[o] += 1

print("── 1. Every tracked file has exactly one owner ──")
for k, v in count.items():
    print(f"  {k:8s} {v:4d} files  ({repos[k]['name']}, read by {repos[k]['reader']}s)")
if orphans:
    fail = 1
    print(f"  ✗ {len(orphans)} file(s) claimed by nobody — the split cannot be executed:")
    for f in orphans[:10]:
        print(f"      {f}")
    if len(orphans) > 10:
        print(f"      … and {len(orphans)-10} more")
if ambiguous:
    fail = 1
    print(f"  ✗ {len(ambiguous)} file(s) claimed by both repositories:")
    for f in ambiguous[:10]:
        print(f"      {f}")
if not orphans and not ambiguous:
    print("  ✓ no orphan, no double claim")

print("── 2. Every mirrored path is owned by the toolkit ──")
bad_mirror = [p for p in mirrored if owner(p.rstrip("/") if "." in p.split("/")[-1] else p) != "toolkit"]
# a directory prefix resolves through the same owner() rule
bad_mirror = [p for p in mirrored if owner(p) != "toolkit"]
if bad_mirror:
    fail = 1
    for p in bad_mirror:
        print(f"  ✗ mirrored but not owned by the toolkit: {p} (owner: {owner(p)})")
else:
    print(f"  ✓ {len(mirrored)} mirrored path(s), all sourced from the toolkit")

print("── 3. Every published page has a claimed source ──")
try:
    sumario = json.load(open("publicar/sumario.json"))
except FileNotFoundError:
    print("  ✗ publicar/sumario.json missing")
    sys.exit(1)

pages = [i["arquivo"] for p in sumario["partes"] for i in p["itens"]]
homeless = []
for page in pages:
    o = owner(page)
    is_mirror = any(page == m or page.startswith(m) for m in mirrored)
    if o == "guide" or is_mirror:
        continue
    homeless.append((page, o))

if homeless:
    fail = 1
    print(f"  ✗ {len(homeless)} published page(s) come from the toolkit and are NOT mirrored —")
    print("     the guide's site would lose them on the day of the split:")
    for page, o in homeless:
        print(f"      {page}  (owner: {o})")
else:
    guide_pages = sum(1 for p in pages if owner(p) == "guide")
    print(f"  ✓ {len(pages)} pages: {guide_pages} owned by the guide, {len(pages)-guide_pages} mirrored from the toolkit")

print("──")
if fail:
    print("✗ the boundary is not decidable yet — fix boundary.json before moving any file.")
    sys.exit(1)
print("✓ boundary decidable: the split can be executed mechanically.")
PY
