# Plan 064 — Portão de slop: o julgamento editorial vira checagem

- **Spec**: `spec.md` · **Raia**: plena · **Data**: 2026-08-13

## Constitution Check (governance/principles.md)

| Principle | Compliance |
|---|---|
| I. Spec-driven | ✅ spec antes do código; as três regras descartadas viraram ADR 0021 antes de virarem ausência silenciosa. |
| II. Human-governed orchestration | ⚠️ **dívida declarada**: quem executou foi o agente, e `TAIL:review` (revisão independente em contexto fresco) segue **em aberto**. O gate de merge é humano e não delegável. |
| III. Reversibility / risk gates | ✅ arquivo novo + uma linha no `package.json` + um passo na CI. Reverter é apagar. Nenhuma ação irreversível. |
| IV. Test-first / verifiable DoD | ✅ é o princípio que motiva o ciclo. O portão tem autoteste próprio (16 canários, cada um também dobrado em duas linhas) e foi visto recusando slop plantado — `TAIL:mutation`. |
| V. Context economy / boundary | ✅ corte por fronteira: o portão vive em `publicar/` (o livro), não em `scripts/` (o método que viaja). Escopo explícito, com três diretórios fora por motivo escrito. |
| VI. Living artifacts | ✅ ADR 0021 + linha em `decisoes.jsonl` + CHANGELOG + `CLAUDE.md` no mesmo PR. O portão é consumido por uma forcing function (o build), não é documento parado. |
| VII. Light governance / YAGNI | ✅ três regras do guia foram **removidas** por medição, não adicionadas por precaução. Zero dependência nova. |
| VIII. Intelligible communication | ✅ cada achado cita a seção do guia de origem; o cabeçalho do arquivo explica por extenso o que o portão não mede e por quê. |

## Artifacts of this cycle (declare all five — silence is not a decision)

<!-- Read by scripts/check-conformance.sh. Declaring =yes means the file MUST exist here.
     What each one is for: docs/governance/artifacts.md -->

| Artifact | Declaration | Why |
|---|---|---|
| `research.md` | `ART:research=no` | a lista de padrões é o guia "Signs of AI writing"; não há incógnita técnica a resolver antes. |
| `data-model.md` | `ART:data-model=no` | não há entidade nem persistência: o portão lê arquivo e sai 0 ou 1. |
| `contracts/` | `ART:contracts=no` | a única interface é o código de saída e o formato da linha de achado, ambos na spec. |
| `checklist.md` | `ART:checklist=no` | os critérios da DoD já são executáveis; um checklist paralelo seria a mesma coisa duas vezes (VI). |
| `ux-design.md` | `ART:ux-design=no` | não toca tela: a saída é terminal, e o site publicado não muda. |

## How
<...>

## Verification (DoD)
<commands and expected output>
