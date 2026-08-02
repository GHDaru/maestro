#!/usr/bin/env bash
# verificar-capitulos.sh — a Iron Law editorial vira executável.
#
#   NENHUM CAPÍTULO PUBLICA SEM OBJETIVOS, EXEMPLO REAL E VERIFICAÇÃO
#
# O capítulo 01 foi migrado no ciclo 016 e as nove seções foram contadas À MÃO no
# qa-report. Contar à mão funciona uma vez; sobram onze capítulos. Este script cobra o
# esqueleto de todo capítulo JÁ migrado (cabeçalho "migrado ao padrão v2") e lista os que
# ainda faltam — para o número de pendentes ser fato, não lembrança.
set -euo pipefail

DIR="${1:-docs/handbook}"
falhas=0
migrados=0; pendentes=()

# as nove seções do guia editorial (docs/livro/guia-editorial.md §2), na ordem
SECOES=("Objetivos" "O problema" "A ideia central" "A regra vigente" "Fundamentos" \
        "Na prática" "Erros e anti-padrões" "Verificação" "O que roubar")

for f in "$DIR"/[0-9][0-9]-*.md; do
  [[ -e "$f" ]] || continue
  nome="$(basename "$f")"
  # "migrado" se tem a ESTRUTURA v2, não se tem a frase "migrado ao padrão v2": com o
  # marcador textual, apagar a linha do cabeçalho tirava o capítulo do check em silêncio
  # (visto ao provar este script falhando — anti-padrão 13).
  if ! grep -q '^## 1\. Objetivos' "$f"; then pendentes+=("$nome"); continue; fi
  migrados=$((migrados + 1))

  # datação obrigatória (guia §4): capturado em + revisão + ciclo
  grep -qE '^> \*\*Capturado em\*\* [0-9]{4}-[0-9]{2} · última revisão [0-9]{4}-[0-9]{2}-[0-9]{2} · ciclo [0-9]{3}' "$f" \
    || { echo "  ✗ $nome: cabeçalho de datação fora do padrão (capturado · revisão · ciclo)" >&2; falhas=$((falhas + 1)); }

  # as nove seções, na ordem
  ordem_lida="$(grep -oE '^## [0-9]+\. .*' "$f" | sed 's/^## [0-9]*\. //; s/⭐ //; s/ —.*//')"
  i=0
  while IFS= read -r titulo; do
    esperado="${SECOES[$i]:-}"
    [[ "$titulo" == "$esperado"* ]] || { echo "  ✗ $nome: seção $((i+1)) é '$titulo', esperada '$esperado'" >&2; falhas=$((falhas + 1)); }
    i=$((i + 1))
  done <<< "$ordem_lida"
  [[ "$i" -eq 9 ]] || { echo "  ✗ $nome: $i seções numeradas (o esqueleto tem 9)" >&2; falhas=$((falhas + 1)); }

  # o exemplo real é a nossa marca: seção 6 marcada e com evidência de ciclo
  grep -q '^## 6\. ⭐ Na prática' "$f" || { echo "  ✗ $nome: falta a seção 6 marcada '⭐ Na prática'" >&2; falhas=$((falhas + 1)); }
  grep -qE 'ciclo [0-9]{3}|spec [0-9]{3}|gate-main|\$ ' "$f" \
    || { echo "  ✗ $nome: seção 'Na prática' sem evidência real (ciclo, spec, gate ou saída de comando)" >&2; falhas=$((falhas + 1)); }

  [[ "$falhas" -eq 0 ]] && echo "  ok: $nome"
done

echo ""
echo "migrados ao padrão v2: $migrados · pendentes: ${#pendentes[@]} (${pendentes[*]:-nenhum})"
if [[ "$falhas" -ne 0 ]]; then
  echo "✗ $falhas violação(ões) da Iron Law editorial." >&2
  exit 1
fi
echo "✓ todo capítulo migrado cumpre o esqueleto de nove seções, com datação e exemplo real."
