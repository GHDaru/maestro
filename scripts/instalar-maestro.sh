#!/usr/bin/env bash
# instalar-maestro.sh — instala o Maestro (agentes + skills + scripts + templates)
# em outro repositório, para a IA seguir o método lá.
#
# Uso (de dentro do repo do Maestro):
#   scripts/instalar-maestro.sh /caminho/do/projeto           # instala
#   scripts/instalar-maestro.sh /caminho/do/projeto --dry-run # só mostra o que faria
#   scripts/instalar-maestro.sh --bloco                       # imprime a instrução p/ CLAUDE.md
#
# NÃO sobrescreve arquivos existentes sem --forcar (reversibilidade, Princípio III).
set -euo pipefail

DESTINO="${1:-}"
MODO="${2:-}"
ORIGEM="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# O bloco de instrução é GERADO das skills que existem no disco — lista escrita à mão
# envelhece calada (era o modo de falha do próprio repo do Maestro, ciclo 021).
bloco_metodo() {
  echo '## Método: Maestro'
  echo '- Leia `docs/governance/principios-maestro.md` (constituição) e'
  echo '  `docs/governance/modelo-operacional.md` antes de qualquer trabalho.'
  echo '- **Skills primeiro**: antes de agir, verifique se uma skill abaixo se aplica; se'
  echo '  houver chance razoável, siga-a (cada uma tem sua Iron Law):'
  for d in "$ORIGEM"/skills/*/; do
    nome="$(basename "$d")"
    # primeira frase da description, sem cortar palavra no meio
    desc="$(sed -n 's/^description: *//p' "$d/SKILL.md" 2>/dev/null | head -1 | sed 's/\([.:] \).*/\1/' | sed 's/ *$//')"
    echo "  - \`$nome\`${desc:+ — $desc}"
  done
  echo '- Fluxo: `spec → plan (Constitution Check) → tasks → implement → DoD → review em'
  echo '  contexto fresco → gate humano → merge`.'
  echo '- Raias: leve (o PR é o artefato) · plena (spec completa) · infra (plena + reversibilidade).'
}

# --bloco: imprime só a instrução para a IA (para redirecionar ao CLAUDE.md do projeto)
if [[ "$DESTINO" == "--bloco" || "$MODO" == "--bloco" ]]; then bloco_metodo; exit 0; fi

[[ -n "$DESTINO" ]] || { echo "uso: scripts/instalar-maestro.sh <destino> [--dry-run|--forcar|--bloco]" >&2; exit 2; }
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
for s in novo-ciclo.sh promover-main.sh retro.sh registrar-decisao.sh verificar-agentes.sh verificar-papeis.sh verificar-instalacao.sh; do
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

echo
echo "── Próximos passos (no projeto de destino) ──"
echo "  1. Adicione ao CLAUDE.md (ou AGENTS.md) do projeto o bloco abaixo"
echo "     (para colar direto:  scripts/instalar-maestro.sh <destino> --bloco >> CLAUDE.md):"
echo
bloco_metodo | sed 's/^/     /'
cat <<'FIM'

     (dica: mantenha UMA fonte — `ln -s CLAUDE.md AGENTS.md` — para as duas
     instruções não divergirem.)

  2. Prove que está instalado:  scripts/verificar-instalacao.sh
     (falha enquanto o CLAUDE.md/AGENTS.md não apontar para o método: copiar arquivos
     não é instalar — instalado é quando a IA sabe que deve segui-los.)
  3. Abra o primeiro ciclo:     scripts/novo-ciclo.sh 001 <slug>
  4. Ao promover:               scripts/promover-main.sh
  5. Na retro:                  scripts/retro.sh

FIM
echo "pronto."
