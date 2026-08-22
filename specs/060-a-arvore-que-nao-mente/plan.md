# Plan 060 — A árvore que não mente

- **Spec**: `spec.md` · **Lane**: plena · **Date**: 2026-08-17

## Constitution Check (governance/principles.md)

| Principle | Compliance |
|---|---|
| I. Spec-driven | ✅ Quatro FRs; o FR3 é o mecanizável e é o que a mutação exercita, nos dois sentidos. |
| II. Human-governed orchestration | ✅ O ciclo nasce de uma pergunta do Steward que nenhum portão fazia — e o remédio é justamente transformá-la em portão. |
| III. Reversibility / risk gates | ✅ Documentação e uma asserção. Nada muda no que é escrito em disco de terceiro. |
| IV. Test-first / verifiable DoD | ✅ As duas listas comparadas são **derivadas**: uma lida da página, outra de uma instalação feita na hora. Lista escrita à mão só moveria o problema um nível acima. |
| V. Context economy / boundary | ✅ Nenhum caminho novo; a asserção entra no portão que já instala num temporário. |
| VI. Living artifacts | ✅ É o ciclo inteiro: a árvore passa a ter **uma** fonte, e o README aponta em vez de repetir. |
| VII. Light governance / YAGNI | ✅ Sem 18º portão: reusa a instalação que o `check-installed.sh` já faz. |
| VIII. Intelligible communication | ✅ O livro passa a dizer que existe instrução para IA e **onde** — sem movê-la para longe de quem a consome. |

## Artifacts of this cycle (declare all five — silence is not a decision)

<!-- Read by scripts/check-conformance.sh. Declaring =yes means the file MUST exist here.
     What each one is for: docs/governance/artifacts.md -->

| Artifact | Declaration | Why |
|---|---|---|
| `research.md` | `ART:research=no` | Os quatro fatos que motivam o ciclo foram medidos por `grep` e estão na spec. |
| `data-model.md` | `ART:data-model=no` | Nenhuma entidade. |
| `contracts/` | `ART:contracts=no` | Nenhuma interface entre partes. |
| `checklist.md` | `ART:checklist=no` | Cinco critérios, três provados por mutação. |
| `ux-design.md` | `ART:ux-design=no` | Não toca tela. |

## How

**A árvore muda de casa.** Sai do `README.md` e entra na receita — que **está no livro** —, sob
um título **sem acento** (`## O que fica no seu projeto depois`), porque o GitHub mantém acento
na âncora e o site remove: um título ASCII faz as duas concordarem em vez de quebrar uma.
O README passa a apontar, com a frase que resume o essencial.

**O bloco para IA fica onde está**, e o livro **aponta** para ele dizendo por quê: um agente
abre o `README.md`, não o site.

**A asserção** entra no `check-installed.sh`, que já instala num `mktemp`. Lê os diretórios de
**primeiro nível** da árvore publicada (as linhas que abrem com `├──`/`└──`) e compara com o
que a instalação criou. Reprova nos dois sentidos, e reprova também quando a árvore **some**.

## Verification (DoD)

| Comando | Esperado |
|---|---|
| link do README para a receita | resolve no GitHub **e** no site (título ASCII) |
| `node publicar/build.mjs` | a árvore aparece no livro |
| **mutação 1**: receita documenta diretório inexistente | reprova |
| **mutação 2**: instalação cria diretório fora da receita | reprova |
| **mutação 3**: a árvore some da receita | reprova — "documenta nada" |
| os 14 portões bloqueantes · plugin · build | verdes |
