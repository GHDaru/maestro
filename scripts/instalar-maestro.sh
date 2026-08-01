#!/usr/bin/env bash
# instalar-maestro.sh — instala o Maestro (agentes + skills + scripts + templates)
# em outro repositório, para a IA seguir o método lá.
#
# Uso (de dentro do repo do Maestro):
#   scripts/instalar-maestro.sh /caminho/do/projeto           # instala
#   scripts/instalar-maestro.sh /caminho/do/projeto --dry-run # só mostra o que faria
#
# NÃO sobrescreve arquivos existentes sem --forcar (reversibilidade, Princípio III).
set -euo pipefail

DESTINO="${1:-}"
MODO="${2:-}"
ORIGEM="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

[[ -n "$DESTINO" ]] || { echo "uso: scripts/instalar-maestro.sh <destino> [--dry-run|--forcar]" >&2; exit 2; }
[[ -d "$DESTINO" ]] || { echo "erro: destino '$DESTINO' não existe." >&2; exit 1; }
DRY=0; FORCAR=0
[[ "$MODO" == "--dry-run" ]] && DRY=1
[[ "$MODO" == "--forcar" ]] && FORCAR=1

echo "Maestro: $ORIGEM  →  $DESTINO"
[[ "$DRY" -eq 1 ]] && echo "(dry-run: nada será escrito)"
echo

copiar() {  # $1 = caminho relativo (arquivo ou diretório)
  local rel="$1" src="$ORIGEM/$1" dst="$DESTINO/$1"
  [[ -e "$src" ]] || { echo "  ⚠ ausente na origem: $rel"; return; }
  if [[ -e "$dst" && "$FORCAR" -ne 1 ]]; then
    echo "  = existe (mantido): $rel"
    return
  fi
  if [[ "$DRY" -eq 1 ]]; then
    echo "  + copiaria: $rel"
  else
    mkdir -p "$(dirname "$dst")"
    cp -r "$src" "$dst"
    echo "  + instalado: $rel"
  fi
}

echo "── Agentes (quem faz) ──"
copiar ".claude/agents"

echo "── Skills (como fazer) ──"
copiar "skills"

echo "── Scripts (o ritual) ──"
for s in novo-ciclo.sh promover-main.sh retro.sh registrar-decisao.sh verificar-agentes.sh; do
  copiar "scripts/$s"
done
copiar "scripts/README.md"

echo "── Comandos e templates (o motor spec-driven) ──"
copiar ".claude/commands"
copiar ".specify/templates"
copiar ".specify/UPSTREAM.md"

echo "── Governança (a fonte de verdade) ──"
copiar "docs/governance/principios-maestro.md"
copiar "docs/governance/modelo-operacional.md"
copiar "docs/governance/glossario.md"
copiar "docs/registro/README.md"

if [[ "$DRY" -eq 0 ]]; then
  chmod +x "$DESTINO"/scripts/*.sh 2>/dev/null || true
  # índice de decisões começa vazio no projeto novo (histórico é de cada projeto)
  [[ -f "$DESTINO/docs/registro/decisoes.jsonl" ]] || { mkdir -p "$DESTINO/docs/registro"; : > "$DESTINO/docs/registro/decisoes.jsonl"; }
fi

cat <<'FIM'

── Próximos passos (no projeto de destino) ──
  1. Adicione ao CLAUDE.md (ou AGENTS.md) do projeto:

     ## Método: Maestro
     - Leia `docs/governance/principios-maestro.md` (constituição) e
       `docs/governance/modelo-operacional.md` antes de qualquer trabalho.
     - **Skills primeiro**: antes de agir, verifique se uma skill de `skills/` se aplica;
       se houver chance razoável, siga-a (cada uma tem sua Iron Law).
     - Fluxo: `spec → plan (Constitution Check) → tasks → implement → DoD → review em
       contexto fresco → gate humano → merge`.
     - Raias: leve (o PR é o artefato) · plena (spec completa) · infra (plena + reversibilidade).

  2. Abra o primeiro ciclo:   scripts/novo-ciclo.sh 001 <slug>
  3. Ao promover:             scripts/promover-main.sh
  4. Na retro:                scripts/retro.sh

FIM
echo "pronto."
