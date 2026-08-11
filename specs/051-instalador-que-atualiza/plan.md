# Plan 051 — O instalador que atualiza

- **Spec**: `spec.md` · **Lane**: plena · **Date**: 2026-08-11

## Constitution Check (governance/principles.md)

| Principle | Compliance |
|---|---|
| I. Spec-driven | ✅ `spec.md` antes deste plano; FR1–FR6 em EARS, cinco deles cobertos por cenário no portão. |
| II. Human-governed orchestration | ✅ O instalador nunca decide por ninguém: arquivo modificado pelo projeto é mantido, e a versão nova fica ao lado para o humano conciliar. |
| III. Reversibility / risk gates | ⚠️ Parcial e declarado: este ciclo faz o instalador **apagar** arquivos no repositório de terceiro. Mitigado por três limites — só apaga o que **nós** escrevemos, só se estiver **inalterado**, e `--dry-run` mostra antes. É a razão da raia plena. |
| IV. Test-first / verifiable DoD | ✅ O cenário foi escrito **antes** e visto vermelho — mas honestamente: com o instalador antigo só a asserção do manifesto era **alcançável**, as outras ficavam dentro do `else`. As cinco foram provadas por **mutação do instalador corrigido**, uma por invariante, cada mutante matando exatamente a asserção certa. |
| V. Context economy / boundary | ✅ Nada muda de domínio. O manifesto vive no destino, não aqui. |
| VI. Living artifacts | ✅ É o ponto do ciclo: a instalação deixa de congelar na versão em que nasceu. |
| VII. Light governance / YAGNI | ✅ Sem migração de conteúdo, sem versionar a instalação, sem formato novo além de `hash⇥caminho`. |
| VIII. Intelligible communication | ✅ O resumo diz em números o que aconteceu, e o caminho sem manifesto **explica por que não sobrescreveu**, em vez de parecer que não fez nada. |

## Artifacts of this cycle (declare all five — silence is not a decision)

<!-- Read by scripts/check-conformance.sh. Declaring =yes means the file MUST exist here.
     What each one is for: docs/governance/artifacts.md -->

| Artifact | Declaration | Why |
|---|---|---|
| `research.md` | `ART:research=no` | Nenhuma incógnita: o defeito foi reproduzido em dois comandos antes de escrever qualquer coisa. |
| `data-model.md` | `ART:data-model=no` | O manifesto é uma linha `hash⇥caminho`; descrevê-lo custa uma frase, e ela está na spec. Um documento para isso seria a cerimônia que o Princípio VII recusa. |
| `contracts/` | `ART:contracts=no` | Nenhuma interface de rede. O formato do manifesto é lido só pelo próprio instalador. |
| `checklist.md` | `ART:checklist=no` | Os critérios de aceite são a lista, e cada um é um cenário do portão. |
| `ux-design.md` | `ART:ux-design=no` | Não toca tela. A superfície é a saída do instalador no terminal, coberta pelo Princípio VIII acima. |

## How

**O manifesto é o fato que faltava.** `.maestro/manifest.tsv` no destino, `hash⇥caminho` por
arquivo escrito. Com ele, três estados passam a ser distinguíveis, e só o do meio é nosso:

| Estado | O que o instalador faz |
|---|---|
| igual à origem | nada (`already current`) |
| difere da origem **e** bate com o manifesto | **atualiza** — é versão velha |
| difere dos dois | **mantém**, e escreve `<arquivo>.maestro-new` ao lado |
| estava no manifesto e não é mais enviado | **remove**, se inalterado; mantém, se modificado |

`copy()` passa a **caminhar arquivo a arquivo** (`find -type f`), o que elimina o
aninhamento: nunca mais `cp -r` sobre diretório existente.

**Sem manifesto** (instalação da v0.2.0 ou anterior): nada é sobrescrito, tudo que difere vira
`.maestro-new`, e a saída explica que a partir daí passa a ser possível distinguir.

## Verification (DoD)

| Comando | Esperado |
|---|---|
| `scripts/check-installed.sh` | cenário de upgrade verde nos cinco invariantes |
| reinstalar sem mudança | `already current` para tudo, nada escrito |
| `--force` | sobrescreve em lugar, sem aninhar |
| bateria completa + plugin + build | verdes |
