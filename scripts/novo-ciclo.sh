#!/usr/bin/env bash
# novo-ciclo.sh — cria o esqueleto de um ciclo (spec) do Maestro.
# Padroniza a estrutura specs/NNN-slug/ com os 4 artefatos obrigatórios,
# já com cabeçalhos preenchidos e Constitution Check em branco para preencher.
# Não sobrescreve um ciclo existente.
# Este esqueleto é o ATALHO MÍNIMO; a referência completa (com guidance) são os
# templates vendorizados em .specify/templates/ — se divergirem, eles mandam
# (.specify/UPSTREAM.md, regra 2).
#
# Uso:  scripts/novo-ciclo.sh <NNN> <slug>
#       scripts/novo-ciclo.sh 007 vendorizar-spec-kit
set -euo pipefail

NNN="${1:-}"; SLUG="${2:-}"
if [[ -z "$NNN" || -z "$SLUG" ]]; then
  echo "uso: scripts/novo-ciclo.sh <NNN> <slug>" >&2
  exit 2
fi
[[ "$NNN" =~ ^[0-9]{3}$ ]] || { echo "erro: NNN deve ter 3 dígitos (ex.: 007)." >&2; exit 2; }
[[ "$SLUG" =~ ^[a-z0-9-]+$ ]] || { echo "erro: slug em kebab-case (a-z 0-9 -)." >&2; exit 2; }

DIR="specs/${NNN}-${SLUG}"
DATE="$(date +%Y-%m-%d)"
mkdir -p "$DIR"

write_if_absent() {  # $1 = arquivo, stdin = conteúdo
  if [[ -e "$1" ]]; then
    echo "existe (mantido): $1"
  else
    cat > "$1"
    echo "criado: $1"
  fi
}

write_if_absent "$DIR/spec.md" <<EOF
# Spec ${NNN} — <título>

- **Status**: Rascunho · **Raia**: <leve|plena|infra> · **Data**: ${DATE}
- **Origem**: <de onde vem esta demanda>

## O quê e por quê
<valor de negócio; o problema>

## Requisitos funcionais
- **FR1**: <...>

## Fora de escopo
- <...>

## Critérios de aceite (DoD)
- [ ] <check verificável — ver skill dod-verificavel>

## Clarify
1. <ambiguidade a resolver antes do plan>
EOF

write_if_absent "$DIR/plan.md" <<EOF
# Plan ${NNN} — <título>

- **Spec**: \`spec.md\` · **Raia**: <...> · **Data**: ${DATE}

## Constitution Check (principios-maestro.md)
<preencher I–VII — ver skill constitution-check>

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven |  |
| II. Orquestração humano-governada |  |
| III. Reversibilidade / gates de risco |  |
| IV. Test-First / DoD verificável |  |
| V. Economia de contexto / fronteira |  |
| VI. Artefatos vivos |  |
| VII. Governança leve / YAGNI |  |

## Como
<...>

## Verificação (DoD)
<comandos e esperado>
EOF

write_if_absent "$DIR/tasks.md" <<EOF
# Tasks ${NNN} — <título>

## Verificação primeiro
- [ ] T0 — definir os checks do DoD

## Implementação
- [ ] T1 — <...>

## Gate
- [ ] Tn — DoD verde -> veredito Guardião -> gate de merge humano
EOF

write_if_absent "$DIR/qa-report.md" <<EOF
# QA-report ${NNN} — <título>

- **Data**: ${DATE} · **Raia**: <...> · **Veredito**: <pendente>

## Fitness functions (DoD)
| Check | Esperado | Resultado |
|---|---|---|
|  |  |  |

## Cobertura dos requisitos
- FR1: <...>

## Pendência de gate
- promoção dev -> main aguarda aprovação humana.
EOF

echo "ciclo ${NNN}-${SLUG} pronto em $DIR/"
