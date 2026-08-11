# Plan 052 — Symlink não é porta de saída

- **Spec**: `spec.md` · **Lane**: leve · **Date**: 2026-08-11

## Constitution Check (governance/principles.md)

| Principle | Compliance |
|---|---|
| I. Spec-driven | ✅ spec curta, três FRs, cada um com asserção no portão. |
| II. Human-governed orchestration | ✅ Recusar é a escolha conservadora: o instalador não decide atravessar um link no lugar de ninguém. |
| III. Reversibility / risk gates | ✅ A mudança **reduz** o alcance do script: ele passa a fazer menos. |
| IV. Test-first / verifiable DoD | ✅ O ataque foi reproduzido antes (escreveu em `/fora`) e é asserção do portão depois. |
| V. Context economy / boundary | ✅ Nada muda de domínio. |
| VI. Living artifacts | ✅ O portão guarda o comportamento; a recusa não pode voltar a ser silenciosa. |
| VII. Light governance / YAGNI | ✅ Raia leve, uma função de dez linhas e duas asserções. Sem manifesto novo, sem flag. |
| VIII. Intelligible communication | ✅ A recusa **nomeia o caminho** e entra no resumo, em vez de sumir. |

## Artifacts of this cycle (declare all five — silence is not a decision)

<!-- Read by scripts/check-conformance.sh. Declaring =yes means the file MUST exist here.
     What each one is for: docs/governance/artifacts.md -->

| Artifact | Declaration | Why |
|---|---|---|
| `research.md` | `ART:research=no` | Nenhuma incógnita: o achado já descrevia o mecanismo, e o ataque foi reproduzido em dois comandos. |
| `data-model.md` | `ART:data-model=no` | Nenhuma entidade. |
| `contracts/` | `ART:contracts=no` | Nenhuma interface. |
| `checklist.md` | `ART:checklist=no` | Três critérios de aceite, dois deles asserção de portão. |
| `ux-design.md` | `ART:ux-design=no` | Não toca tela. |

## How

`escapes_via_symlink <rel>` caminha componente a componente sob o alvo e responde se o
destino **ou qualquer diretório acima dele** é um link. Consultada nos dois pontos onde o
script toca o disco: antes de escrever e antes de remover. Recusa é contada no resumo.

## Verification (DoD)

| Comando | Esperado |
|---|---|
| `ln -s /fora <alvo>/skills` + instalar | nada escrito em `/fora`, recusa nomeada |
| `scripts/check-installed.sh` | doze asserções verdes, duas delas novas |
| bateria completa | verde |
