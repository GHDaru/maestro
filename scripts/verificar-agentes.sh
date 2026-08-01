#!/usr/bin/env bash
# verificar-agentes.sh — fitness functions estruturais dos subagentes.
# Roda os invariantes que foram checados à mão nos ciclos 003/004.
# Exit 0 se tudo passa; exit 1 se qualquer invariante quebra.
set -euo pipefail

AGENTS_DIR=".claude/agents"
EXPECTED_COUNT="${MAESTRO_AGENTS_EXPECTED:-13}"
READONLY_AGENTS=(review security guardiao-processo)
fail=0

# 1. Contagem esperada.
count=$(find "$AGENTS_DIR" -maxdepth 1 -name '*.md' | wc -l | tr -d ' ')
if [[ "$count" -ne "$EXPECTED_COUNT" ]]; then
  echo "FALHA: esperado $EXPECTED_COUNT agentes, encontrei $count." >&2
  fail=1
else
  echo "ok: $count agentes."
fi

# 2. Todo agente tem frontmatter 'name:'.
missing_name=$(grep -L "^name:" "$AGENTS_DIR"/*.md || true)
if [[ -n "$missing_name" ]]; then
  echo "FALHA: sem 'name:' no frontmatter:" >&2
  echo "$missing_name" >&2
  fail=1
else
  echo "ok: todos com frontmatter 'name:'."
fi

# 3. Invariante de segurança: agente read-only NÃO pode ter Write/Edit.
for a in "${READONLY_AGENTS[@]}"; do
  f="$AGENTS_DIR/$a.md"
  [[ -e "$f" ]] || { echo "FALHA: falta $f." >&2; fail=1; continue; }
  if grep -qE "tools:.*(Write|Edit)" "$f"; then
    echo "FALHA: agente read-only '$a' tem Write/Edit nas tools." >&2
    fail=1
  fi
done
[[ "$fail" -eq 0 ]] && echo "ok: nenhum read-only com Write/Edit."

if [[ "$fail" -ne 0 ]]; then
  echo "invariantes de agentes QUEBRADOS." >&2
  exit 1
fi
echo "todos os invariantes de agentes OK."
