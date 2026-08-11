#!/usr/bin/env bash
# check-roles.sh — the operating model prescribes roles; the toolkit must deliver
# them. This fitness function compares the two and fails when they diverge.
#
# It was born from a real gap (cycle 018): the model had been naming a UX role and a
# journey document for fourteen cycles with no agent and no skill behind them. A norm
# with no executable is a norm with no effect.
set -euo pipefail

MODEL="docs/governance/operating-model.md"
fail=0

# role prescribed in the model -> file that delivers it
declare -A EXPECTED=(
  ["Spec-agent"]=".claude/agents/spec-agent.md"
  ["Plan-agent"]=".claude/agents/plan-architect.md"
  ["UX-agent"]=".claude/agents/ux-semantics.md"
  ["Dev-agent"]=".claude/agents/dev-implementer.md"
  ["QA/SDET-agent"]=".claude/agents/qa.md"
  ["Review-agent"]=".claude/agents/review.md"
  ["Security-agent"]=".claude/agents/security.md"
  ["Tech Writer-agent"]=".claude/agents/tech-writer.md"
)

echo "── Roles in the operating model × executable agents ──"
for role in "${!EXPECTED[@]}"; do
  file="${EXPECTED[$role]}"
  if ! grep -q "$role" "$MODEL" 2>/dev/null; then
    echo "  ⚠ '$role' no longer appears in the model — remove it from the map or from the toolkit." >&2
    fail=$((fail + 1))
  elif [[ ! -f "$file" ]]; then
    echo "  ✗ '$role' is prescribed by the model but has NO agent: $file" >&2
    fail=$((fail + 1))
  else
    echo "  ok: $role → $(basename "$file")"
  fi
done

# artifacts prescribed as essential need a template
echo ""
echo "── Essential artifacts × templates ──"
for pair in "ux-design.md:.specify/templates/ux-design-template.md" \
            "Journey doc:.specify/templates/journey-template.md"; do
  name="${pair%%:*}"; tpl="${pair##*:}"
  if grep -q "$name" "$MODEL" 2>/dev/null && [[ ! -f "$tpl" ]]; then
    echo "  ✗ '$name' is essential in the model but has no template: $tpl" >&2
    fail=$((fail + 1))
  else
    echo "  ok: $name → $(basename "$tpl")"
  fi
done

# The constitution grows; the Constitution Check must grow with it. Principle VIII
# arrived in cycle 013 and the template stayed at I–VII until cycle 020 — eight cycles
# of plans with nowhere to record it. Counting both sides is what stops a new norm
# from being born invisible.
echo ""
echo "── Constitution principles × Constitution Check rows ──"
CONST="docs/governance/principles.md"
TPL=".specify/templates/plan-template.md"
n_principles=$(grep -cE '^### [IVX]+\. ' "$CONST" || true)
n_rows=$(grep -cE '^\| [IVX]+\. ' "$TPL" || true)
if [[ "$n_principles" -ne "$n_rows" ]]; then
  echo "  ✗ the constitution has $n_principles principles; the plan template checks $n_rows." >&2
  fail=$((fail + 1))
else
  echo "  ok: $n_principles principles → $n_rows rows in the template"
fi

# The profile index (docs/agents/README.md) is a hand-written table describing every
# agent: which file delivers it and which tools it holds. Nothing compared it to disk.
# That is the failure family this repository knows best — cycle 021 found three drifts at
# once, all from hand-written lists never checked against the disk. The list matching today
# is exactly why it is dangerous: it looks healthy, and the health depends on memory.
#
# The link is structural (a markdown link to the file), never the role's prose label — a
# label read as prose would be a check measuring the words instead of the fact.
echo ""
echo "── Agent profile index (docs/agents/README.md) × agents on disk ──"
INDEX="docs/agents/README.md"
if [[ ! -f "$INDEX" ]]; then
  # A project that installed Maestro received the agents but NOT this index: it is the
  # book's, written in Portuguese, and the installable surface is English (ADR 0014). Absent
  # is therefore legitimate THERE — and said out loud, never in silence.
  #
  # …but not HERE. A repository that declares the index in boundary.json owns one, and its
  # deletion is a defect, not a fresh start. Same guard, same reason, same words as
  # check-ecosystem.sh: the escape hatch for new projects must not become an escape hatch
  # for everyone (cycle 047's lesson, re-applied after the review of 048 found it undone).
  if [[ -f boundary.json ]] && grep -qF '"docs/agents/"' boundary.json; then
    echo "  ✗ $INDEX is declared in boundary.json and does not exist — this repository owns a" >&2
    echo "    profile index; deleting it is not the same as never having had one." >&2
    fail=$((fail + 1))
  else
    echo "  · no profile index at $INDEX — the agents are installed; the catalogue of them is"
    echo "    the book's, and does not travel. Nothing to compare."
  fi
else
  # every agent linked from the index, as a bare slug
  documented=$(grep -oE '\.\./\.\./\.claude/agents/[a-z-]+\.md' "$INDEX" | sed 's|.*/||; s|\.md$||' | sort -u)
  on_disk=$(ls .claude/agents/*.md 2>/dev/null | sed 's|.*/||; s|\.md$||' | sort -u)

  # 1. an agent on disk that the index never mentions is an invisible agent
  while read -r slug; do
    [[ -z "$slug" ]] && continue
    if ! grep -qx "$slug" <<<"$documented"; then
      echo "  ✗ agent on disk and ABSENT from the index: $slug" >&2
      fail=$((fail + 1))
    fi
  done <<<"$on_disk"

  # 2. an index row pointing at nothing is a profile for an agent that does not exist
  while read -r slug; do
    [[ -z "$slug" ]] && continue
    if [[ ! -f ".claude/agents/${slug}.md" ]]; then
      echo "  ✗ index documents an agent that does not exist: $slug" >&2
      fail=$((fail + 1))
    fi
  done <<<"$documented"

  # 3. the tools column is a promise about permissions — the place where a silent drift
  #    would be most expensive (Principle III: the judging role gets no write access).
  while read -r slug; do
    [[ -z "$slug" ]] && continue
    [[ -f ".claude/agents/${slug}.md" ]] || continue
    real=$(grep -m1 '^tools:' ".claude/agents/${slug}.md" | sed 's/^tools:[[:space:]]*//' | tr -d ' ')
    row=$(grep -m1 "agents/${slug}\.md" "$INDEX")
    for tool in ${real//,/ }; do
      grep -q "$tool" <<<"$row" || {
        echo "  ✗ $slug holds '$tool' on disk and the index row does not list it" >&2
        fail=$((fail + 1))
      }
    done
  done <<<"$documented"

  n_doc=$(grep -c . <<<"$documented"); n_disk=$(grep -c . <<<"$on_disk")
  # 4. the index states a total in prose; a stale number is how a reader learns the wrong size
  stated=$(grep -oE '\*\*[0-9]+ agentes executáveis\*\*' "$INDEX" | grep -oE '[0-9]+' || true)  # PT-DATA (Portuguese index)
  if [[ -n "$stated" && "$stated" -ne "$n_disk" ]]; then
    echo "  ✗ the index claims $stated executable agents; there are $n_disk on disk" >&2
    fail=$((fail + 1))
  fi
  echo "  checked: $n_doc documented / $n_disk on disk / stated ${stated:-–}"
fi

echo ""
if [[ "$fail" -ne 0 ]]; then
  echo "✗ $fail divergence(s) between what the model prescribes and what the toolkit delivers." >&2
  exit 1
fi
echo "✓ every prescribed role has an executable; every agent is documented with its real tools."
