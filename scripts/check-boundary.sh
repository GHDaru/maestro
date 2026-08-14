#!/usr/bin/env bash
# check-boundary.sh — the two domains inside this repository stay decidable (ADR 0018).
#
# Maestro serves two readers: agents, which read the installable method to execute it, and
# people, which read the book to understand it. The split into two REPOSITORIES was measured
# and rejected (ADR 0018 supersedes ADR 0017) — only 20% of commits couple the two halves
# substantively, and separating would cost atomic commits, link coverage and the book's
# evidence. What survived is the boundary itself, enforced here.
#
# What this actually measures (anti-pattern 13): not that files are in pretty folders. It
# measures that the boundary is DECIDABLE — every file has exactly one domain, every shared
# path has an owner, and nothing reaches the published site from a path nobody declared.
# Those are the three ways a boundary rots without anyone noticing.
#
# Invariants:
#   1. every tracked file belongs to exactly one domain (no orphan, no double claim)
#   2. every shared path is owned by the toolkit (shared without an owner is a fork)
#   3. every page in publicar/sumario.json comes from the guide or from a declared shared path
#
# Invariant 3 changed its REASON when the split was dropped, not its value: it no longer
# guards against losing pages on moving day — it guards against the site quietly publishing
# a machine-facing document nobody meant to make public.
#
# Source of truth: boundary.json. Exit 0 only when all three hold.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

[[ -f boundary.json ]] || { echo "✗ boundary.json missing — the boundary has no source of truth." >&2; exit 1; }

python3 - <<'PY'
import json, subprocess, sys

b = json.load(open("boundary.json"))
domains = b["domains"]
shared = b["shared"]["paths"]
allowed = b.get("unclassified_allowed", [])

def owner(path):
    """The domain that claims this path, or None. Longest prefix wins."""
    hits = []
    for key, dom in domains.items():
        for own in dom["owns"]:
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
count = {k: 0 for k in domains}

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

print("── 1. Every tracked file has exactly one domain ──")
for k, v in count.items():
    print(f"  {k:8s} {v:4d} files  ({domains[k]['label']}, read by {domains[k]['reader']}s)")
if orphans:
    fail = 1
    print(f"  ✗ {len(orphans)} file(s) claimed by no domain — it will drift into the wrong half:")
    for f in orphans[:10]:
        print(f"      {f}")
    if len(orphans) > 10:
        print(f"      … and {len(orphans)-10} more")
if ambiguous:
    fail = 1
    print(f"  ✗ {len(ambiguous)} file(s) claimed by both domains:")
    for f in ambiguous[:10]:
        print(f"      {f}")
if not orphans and not ambiguous:
    print("  ✓ no orphan, no double claim")

print("── 2. Every shared path is owned by the toolkit ──")
bad = [p for p in shared if owner(p) != "toolkit"]
if bad:
    fail = 1
    for p in bad:
        print(f"  ✗ declared shared but not owned by the toolkit: {p} (owner: {owner(p)})")
else:
    print(f"  ✓ {len(shared)} shared path(s), all owned by the toolkit")

print("── 3. Every published page has a declared source ──")
try:
    sumario = json.load(open("publicar/sumario.json"))
except FileNotFoundError:
    print("  ✗ publicar/sumario.json missing")
    sys.exit(1)

# `materiais` (cycle 054) is a SECOND publication channel into the reader-facing site.
# It was invisible to this gate for exactly one cycle, and in that window a toolkit-owned
# file declared as material was published while this script reported all clear — the very
# failure it exists to prevent, arriving through the door it was not watching. A gate that
# reads one of two channels cannot tell "nothing leaked" from "I did not look".
pages = [i["arquivo"] for p in sumario["partes"] for i in p["itens"]] \
      + [m["arquivo"] for m in sumario.get("materiais", [])]
homeless = []
for page in pages:
    o = owner(page)
    if o == "guide" or any(page == s or page.startswith(s) for s in shared):
        continue
    homeless.append((page, o))

if homeless:
    fail = 1
    print(f"  ✗ {len(homeless)} page(s) published from the toolkit without being declared shared —")
    print("     a machine-facing document is going out to readers unannounced:")
    for page, o in homeless:
        print(f"      {page}  (owner: {o})")
else:
    guide_pages = sum(1 for p in pages if owner(p) == "guide")
    print(f"  ✓ {len(pages)} pages: {guide_pages} owned by the guide, {len(pages)-guide_pages} declared shared")

print("──")
if fail:
    print("✗ the boundary is no longer decidable — fix boundary.json.")
    sys.exit(1)
print("✓ boundary decidable: every file has a domain, every published page has a source.")
PY
