#!/usr/bin/env bash
# retro.sh — pré-computa o material da retro a partir dos artefatos do repo.
# (Absorção do /reflect do maestro-02 — Apêndice A, spec 008.)
# Read-only: nunca escreve nada. A retro em si continua sendo cerimônia humana;
# este script só elimina o "recarregar contexto de cabeça".
set -euo pipefail

echo "══════════════════════════════════════════════"
echo "  RETRO — material pré-computado"
echo "══════════════════════════════════════════════"

# 1. Ciclos e vereditos.
echo ""
echo "── Ciclos (specs/) e veredito do QA ──"
for d in specs/[0-9][0-9][0-9]-*/; do
  [[ -d "$d" ]] || continue
  nome=$(basename "$d")
  veredito=$(grep -m1 -o "Veredito[^|]*" "$d/qa-report.md" 2>/dev/null | sed 's/Veredito..: *//' | tr -d '*' || true)
  echo "  $nome — ${veredito:-sem qa-report}"
done

# 2. Gates: pendências dos qa-reports cruzadas com o registro (ADR 0009 —
#    o índice docs/registro/decisoes.jsonl é a fonte do estado do gate).
echo ""
echo "── Gates (qa-report × registro) ──"
achou=0
for f in $(grep -rl "Pendência de gate" specs/*/qa-report.md 2>/dev/null); do
  ciclo=$(dirname "$f" | xargs basename | cut -d- -f1)
  pend=$(sed -n '/Pendência de gate/,$p' "$f" | grep -m1 "^- " | sed 's/^- //' || true)
  [[ -n "$pend" ]] || continue
  if grep -q "\"gate-$ciclo" docs/registro/decisoes.jsonl 2>/dev/null; then
    echo "  $(dirname "$f" | xargs basename): ✅ fechado no registro (gate-$ciclo-*)"
  else
    echo "  $(dirname "$f" | xargs basename): ⏳ PENDENTE — $pend"
    achou=1
  fi
done
[[ "$achou" -eq 0 ]] && echo "  (nenhum gate pendente)"

# 3. Últimas decisões registradas.
echo ""
echo "── Últimas 5 decisões (docs/registro/decisoes.jsonl) ──"
if [[ -f docs/registro/decisoes.jsonl ]]; then
  tail -5 docs/registro/decisoes.jsonl | python3 -c "
import json,sys
for line in sys.stdin:
    d=json.loads(line)
    print(f\"  {d['data']}  [{d['status']}]  {d['id']}: {d['titulo']}\")"
else
  echo "  (sem registro — ver docs/registro/README.md)"
fi

# 4. Inventário do toolkit.
echo ""
echo "── Inventário ──"
echo "  agentes:  $(find .claude/agents -name '*.md' 2>/dev/null | wc -l | tr -d ' ')"
echo "  skills:   $(find skills -name 'SKILL.md' 2>/dev/null | wc -l | tr -d ' ')"
echo "  scripts:  $(find scripts -name '*.sh' 2>/dev/null | wc -l | tr -d ' ')"
echo "  ADRs:     $(find docs/adr -name '0*.md' 2>/dev/null | wc -l | tr -d ' ')"

# 5. As perguntas da retro (a parte humana).
echo ""
echo "── Perguntas da retro (responda e converta em regra) ──"
echo "  1. Que erro/correção se REPETIU neste(s) ciclo(s)?  → vira regra versionada"
echo "     (CLAUDE.md, skill, princípio) — nunca corrigir a mesma coisa duas vezes."
echo "  2. Que regra existente NÃO pagou seu custo?  → podar (YAGNI)."
echo "  3. Que passo manual se repetiu idêntico?  → candidato a script/skill."
echo ""
echo "Feito. Este material é insumo; a retro é sua."
