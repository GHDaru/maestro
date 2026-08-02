#!/usr/bin/env bash
# verificar-instalacao.sh — o método está instalado NESTE repositório e a instrução
# que a IA lê continua batendo com o que existe no disco?
#
# Instalar é copiar arquivos; *estar instalado* é a IA saber que deve segui-los. Esta
# fitness function verifica as duas metades — e a coerência entre elas, que é a que
# apodrece em silêncio (skill nova em skills/ e ausente do CLAUDE.md = skill invisível).
#
# Uso:  scripts/verificar-instalacao.sh [diretório]   (padrão: diretório atual)
set -euo pipefail

RAIZ="${1:-.}"
cd "$RAIZ"
falhas=0
alerta() { echo "  ✗ $1" >&2; falhas=$((falhas + 1)); }

echo "── Camadas do método (o que foi copiado) ──"
for par in ".claude/agents:subagentes" \
           "skills:skills" \
           "scripts/novo-ciclo.sh:script de ciclo" \
           "scripts/promover-main.sh:script de promoção" \
           ".specify/templates:templates spec-driven" \
           "docs/governance/principios-maestro.md:constituição" \
           "docs/governance/modelo-operacional.md:modelo operacional"; do
  alvo="${par%%:*}"; nome="${par##*:}"
  if [[ -e "$alvo" ]]; then echo "  ok: $nome ($alvo)"; else alerta "$nome ausente: $alvo"; fi
done

# A instrução que a IA lê. Um dos dois basta existir, mas o que existir precisa apontar
# para o método — arquivo presente e mudo é pior que ausente: parece instalado.
echo ""
echo "── Instrução para a IA (o que faz a IA seguir) ──"
INSTRUCOES=()
for f in CLAUDE.md AGENTS.md; do [[ -f "$f" ]] && INSTRUCOES+=("$f"); done
if [[ ${#INSTRUCOES[@]} -eq 0 ]]; then
  alerta "nem CLAUDE.md nem AGENTS.md — a IA não tem por onde saber do método"
else
  for f in "${INSTRUCOES[@]}"; do
    grep -q "principios-maestro" "$f" || alerta "$f não aponta para docs/governance/principios-maestro.md"
    grep -qi "skills" "$f"            || alerta "$f não manda consultar as skills antes de agir"
    grep -qi "spec.*plan.*tasks"      "$f" || alerta "$f não descreve o fluxo spec → plan → tasks → …"
    grep -qi "raia"                   "$f" || alerta "$f não cita as raias (leve/plena/infra)"
    echo "  verificado: $f"
  done
fi

# Coerência: se o documento enumera skills, precisa enumerar TODAS. Lista parcial é o
# modo de falha real — a skill nova entra no disco e some da instrução (ciclo 021).
echo ""
echo "── Coerência: skills no disco × skills citadas ──"
if [[ -d skills ]]; then
  for d in skills/*/; do
    nome="$(basename "$d")"
    [[ -f "$d/SKILL.md" ]] || { alerta "skills/$nome não tem SKILL.md"; continue; }
    citada=0
    for f in "${INSTRUCOES[@]:-}"; do
      [[ -n "$f" && -f "$f" ]] && grep -q "$nome" "$f" && citada=1
    done
    if [[ "$citada" -eq 1 ]]; then echo "  ok: $nome"; else alerta "skill '$nome' existe mas não é citada em CLAUDE.md/AGENTS.md"; fi
  done
fi

echo ""
if [[ "$falhas" -ne 0 ]]; then
  echo "✗ $falhas problema(s): o método está no disco, mas não está instalado de fato." >&2
  exit 1
fi
echo "✓ método instalado e coerente: camadas presentes, IA instruída, skills todas visíveis."
