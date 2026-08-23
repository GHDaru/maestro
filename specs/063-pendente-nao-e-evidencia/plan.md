# Plan 063 — "Pendente" não é evidência

- **Spec**: `spec.md` · **Lane**: plena · **Date**: 2026-08-23

## Constitution Check (governance/principles.md)

| Principle | Compliance |
|---|---|
| I. Spec-driven | ✅ Cinco FRs; o FR5 absorve os 18 achados da revisão independente, cada um aplicado ou registrado com motivo. |
| II. Human-governed orchestration | ✅ O Steward autorizou a revisão e concedeu o portão do 062 com a ausência dela dita **antes** da decisão. |
| III. Reversibility / risk gates | ✅ Portões e texto. O único artefato público — a tag `v0.3.0` — foi **removida** localmente e será recriada sobre a nota corrigida. |
| IV. Test-first / verifiable DoD | ✅ Cada portão alterado tem mutação **e** contraprova; o FR2 e o FR3 existem porque a correção ingênua quebra evidência boa e ciclo antigo. |
| V. Context economy / boundary | ✅ Nenhum portão novo: tudo entra nos quatro que já existem. |
| VI. Living artifacts | ✅ Os `qa-report` de 061 e 062 recebem a evidência da revisão que chegou depois, e a linha falsa de fechamento do `achado-055` é corrigida por linha nova, não reescrita. |
| VII. Light governance / YAGNI | ✅ O vocabulário de ausência é fechado e curto; lista aberta seria adivinhação. |
| VIII. Intelligible communication | ✅ O índice de scripts volta a nomear todos, e o portão de capítulos deixa de calar sobre o que não conseguiu comparar. |

## Artifacts of this cycle (declare all five — silence is not a decision)

<!-- Read by scripts/check-conformance.sh. Declaring =yes means the file MUST exist here.
     What each one is for: docs/governance/artifacts.md -->

| Artifact | Declaration | Why |
|---|---|---|
| `research.md` | `ART:research=no` | Os fatos foram medidos e estão na spec e no `qa-report`. |
| `data-model.md` | `ART:data-model=no` | Nenhuma entidade. |
| `contracts/` | `ART:contracts=no` | Nenhuma interface entre partes. |
| `checklist.md` | `ART:checklist=no` | Quatro critérios de aceite, todos provados por mutação e contraprova. |
| `ux-design.md` | `ART:ux-design=no` | Não toca tela. |

## How

**Primeiro o que estava quebrando `main`.** O achado 1 da revisão não é sobre `pendente`: o
corte da v0.3.0 ativou uma corrida latente havia onze ciclos no `install-maestro.sh`, e ela
deixava um portão **bloqueante** vermelho ao acaso. Isso foi corrigido antes de tudo, com a
leitura passando de `sed | grep -m1 | tr` para um `awk` que abre o arquivo — sem pipe, sem
SIGPIPE — e com o resultado **validado** por forma.

**Depois o `is_placeholder`.** Ganha um vocabulário **fechado** de ausência declarada, lido do
**início** da evidência, com **piso** em 061 e as duas proteções de botão (piso acima do ciclo
mais novo reprova; piso não-numérico recusa rodar).

**Os buracos do `--ticked-only`.** A exigência dos quatro artefatos vira `soft` (um ciclo com
só `spec.md` é trabalho em curso, não violação), e a **ausência da linha `TAIL:`** vira `bad`
(apagar a pergunta não é o mesmo que deixá-la sem resposta). A checagem do plugin deixa de
depender do ciclo mais novo, e diz quando **não** pôde olhar.

**O vocabulário divergente.** `cycle_touched_a_gate` e o `check-cycle.sh` passam a aceitar
`spec NNN` **e** `ciclo NNN` — a dispensa estava comprável porque os dois lados usavam palavras
diferentes para a mesma coisa. De quebra, o `echo | grep -q` do `check-cycle.sh` vira
here-string: anti-padrão 21, sexta ocorrência.

**O portão de contagens** é reescrito: extração em python (acento e caixa), substantivo
desconhecido **reprova** em vez de pular, camada vazia é comparada, camada ausente não aborta a
página, e **zero contagens lidas é falha**.

**O portão do CHANGELOG** passa a cobrir `[Unreleased]` **e a versão recém-lançada** — só
`[Unreleased]` ficava vacuoso a cada corte — com vocabulário fechado de tipo.

**Duas portas novas ganham guarda**: o `check-flags.sh` passa a cobrir os `check-*.sh` que
têm parser, e a comparar `scripts/README.md` com os scripts que existem.

## Verification (DoD)

| Comando | Esperado |
|---|---|
| **20 instalações seguidas** | `maestro_version` = `0.3.0` nas vinte |
| **mutação**: `TAIL:review` marcado com "não executada" | reprova |
| **contraprova**: evidência legítima que contém a palavra no meio (ciclo 060) | passa |
| **contraprova**: ciclo 042, ausência declarada abaixo do piso | passa |
| **mutação**: piso acima do ciclo mais novo · piso não-numérico | reprova · recusa rodar |
| **mutação**: 061 escreve `TAIL:mutation — n/a` | reprova |
| **mutação**: números por extenso nas duas páginas | reprova (era `✓`) |
| **mutação**: `8 portoes` sem acento | reprova |
| **mutação**: tipo repetido na versão recém-lançada · tipo renomeado | reprovam |
| **mutação**: abrir ciclo novo com `TAIL:gate` marcado atrás | continua cobrando |
| **mutação**: flag no parser sem `# Usage` · script fora do índice | reprovam |
| os 14 portões bloqueantes · `--ticked-only` · plugin · build | verdes |
