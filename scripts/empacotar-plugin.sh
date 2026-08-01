#!/usr/bin/env bash
# empacotar-plugin.sh — gera o plugin do Claude Code a partir das fontes canônicas.
#
# O Claude Code espera `agents/`, `commands/` e `skills/` na RAIZ do plugin; nossas
# fontes canônicas vivem em `.claude/agents`, `.claude/commands` e `skills/` (que é
# onde o repositório as usa para si mesmo e onde o padrão `npx skills add` as procura).
# Este script reconcilia os dois layouts — e `--verificar` prova que estão sincronizados.
#
# Uso:  scripts/empacotar-plugin.sh              # (re)gera plugin/maestro/
#       scripts/empacotar-plugin.sh --verificar  # falha se o pacote está desatualizado
set -euo pipefail

DESTINO="plugin/maestro"
MODO="${1:-}"

gerar() {  # $1 = diretório de saída
  local out="$1"
  rm -rf "$out"
  mkdir -p "$out/.claude-plugin"
  cp -r .claude/agents "$out/agents"
  cp -r .claude/commands "$out/commands"
  cp -r skills "$out/skills"
  rm -f "$out/skills/README.md"   # índice do catálogo não é uma skill
  local versao
  versao=$(grep -m1 '^\*\*Versão\*\*\|Versão\*\*:' docs/governance/principios-maestro.md 2>/dev/null | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+' | head -1)
  cat > "$out/.claude-plugin/plugin.json" <<JSON
{
  "name": "maestro",
  "description": "Metodologia de um humano regendo N agentes de IA: spec como fonte de verdade, gates proporcionais ao risco e reversibilidade que compra velocidade. Traz os subagentes do fluxo spec-driven, as skills com suas leis e os comandos do ciclo.",
  "version": "${versao:-1.0.0}",
  "author": { "name": "GHDaru" },
  "homepage": "https://ghdaru.github.io/maestro/",
  "repository": "https://github.com/GHDaru/maestro",
  "license": "MIT"
}
JSON
  cp README.md "$out/README.md" 2>/dev/null || true
}

if [[ "$MODO" == "--verificar" ]]; then
  TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
  gerar "$TMP/maestro"
  if [[ ! -d "$DESTINO" ]]; then
    echo "✗ pacote ausente — rode: scripts/empacotar-plugin.sh" >&2
    exit 1
  fi
  if ! diff -rq "$TMP/maestro" "$DESTINO" >/dev/null 2>&1; then
    echo "✗ plugin desatualizado em relação às fontes. Diferenças:" >&2
    diff -rq "$TMP/maestro" "$DESTINO" 2>&1 | sed 's/^/   /' >&2
    echo "   → rode: scripts/empacotar-plugin.sh" >&2
    exit 1
  fi
  echo "✓ plugin sincronizado com as fontes ($(find "$DESTINO" -name '*.md' | wc -l | tr -d ' ') arquivos)."
  exit 0
fi

gerar "$DESTINO"
echo "✓ plugin gerado em $DESTINO/"
echo "   agentes: $(find "$DESTINO/agents" -name '*.md' | wc -l | tr -d ' ') · skills: $(find "$DESTINO/skills" -name 'SKILL.md' | wc -l | tr -d ' ') · comandos: $(find "$DESTINO/commands" -name '*.md' | wc -l | tr -d ' ')"
echo "   teste local:  claude --plugin-dir ./$DESTINO"
