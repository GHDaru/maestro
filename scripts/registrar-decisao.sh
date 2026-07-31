#!/usr/bin/env bash
# registrar-decisao.sh — anexa uma decisão ao índice consultável (append-only).
# A prosa mora no ADR/qa-report; aqui vai só o índice de máquina (1 JSON por linha).
# Nunca edita linha passada: correção = nova linha com status "superada por <id>".
#
# Uso: scripts/registrar-decisao.sh '{"id":"adr-0009","data":"2026-08-01","titulo":"...","status":"aceita","registro":"docs/adr/0009-....md"}'
set -euo pipefail

JSONL="docs/registro/decisoes.jsonl"
LINE="${1:-}"
[[ -n "$LINE" ]] || { echo "uso: registrar-decisao.sh '<json de uma linha>'" >&2; exit 2; }

# 1. JSON válido e de uma linha só.
echo "$LINE" | python3 -m json.tool >/dev/null 2>&1 || { echo "erro: JSON inválido." >&2; exit 1; }
[[ "$LINE" != *$'\n'* ]] || { echo "erro: uma linha só (JSONL)." >&2; exit 1; }

# 2. Campos obrigatórios.
for campo in id data titulo status registro; do
  echo "$LINE" | python3 -c "import json,sys; d=json.load(sys.stdin); sys.exit(0 if '$campo' in d and d['$campo'] else 1)" \
    || { echo "erro: campo obrigatório ausente: $campo" >&2; exit 1; }
done

# 3. id único (append-only: não sobrescreve, não repete).
ID=$(echo "$LINE" | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])")
if grep -q "\"id\": *\"$ID\"\|\"id\":\"$ID\"" "$JSONL" 2>/dev/null; then
  echo "erro: id '$ID' já registrado — use um id novo (ou status 'superada por $ID' em nova linha)." >&2
  exit 1
fi

# 4. Anexar.
echo "$LINE" >> "$JSONL"
echo "ok: decisão '$ID' registrada em $JSONL ($(wc -l < "$JSONL" | tr -d ' ') decisões)."
