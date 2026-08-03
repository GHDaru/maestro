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

echo ""
if [[ "$fail" -ne 0 ]]; then
  echo "✗ $fail divergence(s) between what the model prescribes and what the toolkit delivers." >&2
  exit 1
fi
echo "✓ every prescribed role has an executable; every essential artifact has a template."
