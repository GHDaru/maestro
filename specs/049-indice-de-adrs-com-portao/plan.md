# Plan 049 — O índice de decisões com portão

- **Spec**: `spec.md` · **Lane**: plena · **Date**: 2026-08-11

## Constitution Check (governance/principles.md)

| Principle | Compliance |
|---|---|
| I. Spec-driven | ✅ `spec.md` antes deste plano; FR1–FR4 em EARS, os quatro com mutação que os prova. |
| II. Human-governed orchestration | ✅ O portão mede coerência; o mérito de cada decisão segue humano, e a promoção também. |
| III. Reversibility / risk gates | ✅ Um script novo e uma linha na CI. Nada é apagado, nada muda de lugar. |
| IV. Test-first / verifiable DoD | ✅ O portão foi escrito antes e **visto acusar o defeito histórico real** do ciclo 046, reconstruído por mutação. |
| V. Context economy / boundary | ✅ `scripts/` já é `toolkit`; nada muda de domínio e nada entra na superfície instalável. |
| VI. Living artifacts | ✅ É o ponto do ciclo: o índice não pode mais divergir dos arquivos em silêncio. |
| VII. Light governance / YAGNI | ✅ Portão em vez de gerador: mede o mesmo fato por menos, e o gerador fica com gatilho escrito (segunda divergência). |
| VIII. Intelligible communication | ✅ Cada falha nomeia o ADR e diz por que aquilo importa — a pior linha da tabela é a decisão revertida lida como corrente. |

## Artifacts of this cycle (declare all five — silence is not a decision)

<!-- Read by scripts/check-conformance.sh. Declaring =yes means the file MUST exist here.
     What each one is for: docs/governance/artifacts.md -->

| Artifact | Declaration | Why |
|---|---|---|
| `research.md` | `ART:research=no` | Nenhuma incógnita: o defeito foi observado no ciclo 046 e está descrito no achado. |
| `data-model.md` | `ART:data-model=no` | Nenhuma entidade nova. O portão lê arquivos que já existem e uma tabela que já existe. |
| `contracts/` | `ART:contracts=no` | Nenhuma interface. O contrato que o portão lê — `- **Status**:` no ADR e o link no índice — já é a convenção dos arquivos, e está descrito na spec. |
| `checklist.md` | `ART:checklist=no` | Os critérios de aceite são a lista, e cada um é uma mutação. |
| `ux-design.md` | `ART:ux-design=no` | Não toca tela. A superfície é a saída do portão no terminal. |

## How

`scripts/check-adr.sh`, três invariantes sobre `docs/adr/`:

1. **Todo ADR no disco está no índice** — por link ao próprio arquivo, não por nome em prosa.
2. **Todo link do índice aponta para arquivo existente.**
3. **O status concorda nos dois sentidos**: se o ADR diz que foi superado, o índice tem de
   dizer; se o índice diz, o ADR tem de dizer. Um ADR sem linha de status falha, porque não
   há com o que concordar.

O status é lido por `grep -m1 '^- \*\*Status\*\*:'`, **nunca por número de linha**: os ADRs
0005 e 0008 receberam no ciclo 047 uma nota de migração acima do cabeçalho, e uma leitura
por linha fixa leria a nota em vez do status.

Entrada ausente (diretório ou índice) é falha declarada, não silêncio — a lição que os
ciclos 046, 047 e 048 pagaram três vezes.

## Verification (DoD)

| Comando | Esperado |
|---|---|
| `scripts/check-adr.sh` | verde no repositório íntegro |
| mutação reconstruindo o defeito de 046 | vermelho, nomeando 0017, 0018 e 0019 |
| mutações FR1–FR4 + índice ausente | todas acusadas |
| bateria completa + `check-installed` + plugin + build | verdes |
