#!/usr/bin/env bash
# verificar-papeis.sh — o modelo operacional prescreve papéis; o toolkit precisa
# entregá-los. Esta fitness function compara os dois e falha quando divergem.
#
# Nasceu de uma lacuna real (ciclo 018): o modelo citava UX-agent e journey doc havia
# ciclos, sem agente nem skill correspondente. Norma sem executável é norma sem efeito.
set -euo pipefail

MODELO="docs/governance/modelo-operacional.md"
falhas=0

# papel prescrito no modelo -> arquivo que o entrega
declare -A ESPERADO=(
  ["Spec-agent"]=".claude/agents/spec-agent.md"
  ["Plan-agent"]=".claude/agents/plan-arquiteto.md"
  ["UX-agent"]=".claude/agents/ux-semantica.md"
  ["Dev-agent"]=".claude/agents/dev-implementador.md"
  ["QA/SDET-agent"]=".claude/agents/qa.md"
  ["Review-agent"]=".claude/agents/review.md"
  ["Security-agent"]=".claude/agents/security.md"
  ["Tech Writer-agent"]=".claude/agents/tech-writer.md"
)

echo "── Papéis do modelo operacional × agentes executáveis ──"
for papel in "${!ESPERADO[@]}"; do
  arquivo="${ESPERADO[$papel]}"
  if ! grep -q "$papel" "$MODELO" 2>/dev/null; then
    echo "  ⚠ '$papel' não aparece mais no modelo — remova do mapa ou do toolkit." >&2
    falhas=$((falhas + 1))
  elif [[ ! -f "$arquivo" ]]; then
    echo "  ✗ '$papel' é prescrito pelo modelo mas NÃO tem agente: $arquivo" >&2
    falhas=$((falhas + 1))
  else
    echo "  ok: $papel → $(basename "$arquivo")"
  fi
done

# artefatos prescritos como essenciais precisam de template
echo ""
echo "── Artefatos essenciais × templates ──"
for par in "ux-design.md:.specify/templates/ux-design-template.md" \
           "Journey doc:.specify/templates/journey-template.md"; do
  nome="${par%%:*}"; tpl="${par##*:}"
  if grep -q "$nome" "$MODELO" 2>/dev/null && [[ ! -f "$tpl" ]]; then
    echo "  ✗ '$nome' é essencial no modelo mas não há template: $tpl" >&2
    falhas=$((falhas + 1))
  else
    echo "  ok: $nome → $(basename "$tpl")"
  fi
done

# A constituição cresce; o Constitution Check precisa crescer junto. O princípio VIII
# entrou no ciclo 013 e o template ficou em I–VII até o 020 — oito ciclos de planos sem
# onde marcá-lo. Contar os dois lados é o que impede a norma nova de nascer invisível.
echo ""
echo "── Princípios da constituição × linhas do Constitution Check ──"
CONST="docs/governance/principios-maestro.md"
TPL=".specify/templates/plan-template.md"
n_princ=$(grep -cE '^### [IVX]+\. ' "$CONST" || true)
n_tpl=$(grep -cE '^\| [IVX]+\. ' "$TPL" || true)
if [[ "$n_princ" -ne "$n_tpl" ]]; then
  echo "  ✗ a constituição tem $n_princ princípios; o template de plano checa $n_tpl." >&2
  falhas=$((falhas + 1))
else
  echo "  ok: $n_princ princípios → $n_tpl linhas no template"
fi

echo ""
if [[ "$falhas" -ne 0 ]]; then
  echo "✗ $falhas divergência(s) entre o que o modelo manda e o que o toolkit entrega." >&2
  exit 1
fi
echo "✓ todo papel prescrito tem executável; todo artefato essencial tem template."
