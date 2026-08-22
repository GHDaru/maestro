# Plan 059 — "Clonei, e agora?"

- **Spec**: `spec.md` · **Lane**: plena · **Date**: 2026-08-17

## Constitution Check (governance/principles.md)

| Principle | Compliance |
|---|---|
| I. Spec-driven | ✅ Cinco FRs; o FR4 é o único mecanizável e é o que a mutação exercita. Os outros são de leitura e ficam com a revisão independente — dito, não disfarçado de portão. |
| II. Human-governed orchestration | ✅ O ciclo nasce de uma pessoa tropeçando na própria documentação; o remédio é escrito para quem tropeçou, não para quem já sabe. |
| III. Reversibility / risk gates | ✅ Só texto e um portão. Nada muda no que é escrito no disco de terceiro. |
| IV. Test-first / verifiable DoD | ✅ As duas formas de instalar em outra pasta são **executadas** antes de escritas, e a árvore publicada é **gerada** de uma instalação real, não desenhada. |
| V. Context economy / boundary | ✅ `README.md` já é `toolkit` e já é a capa publicada. Nenhum caminho novo. |
| VI. Living artifacts | ✅ O bloco para IA **aponta** para o `CLAUDE.md` e para a constituição em vez de repeti-los: duplicar criaria a segunda fonte que o princípio proíbe. |
| VII. Light governance / YAGNI | ✅ Um portão, que é a extensão de um que já existe (flags → subcomandos), e não um mecanismo novo. |
| VIII. Intelligible communication | ✅ É o ciclo inteiro. A medida de sucesso não é elegância: é a pessoa que perguntou não precisar perguntar de novo. |

## Artifacts of this cycle (declare all five — silence is not a decision)

<!-- Read by scripts/check-conformance.sh. Declaring =yes means the file MUST exist here.
     What each one is for: docs/governance/artifacts.md -->

| Artifact | Declaration | Why |
|---|---|---|
| `research.md` | `ART:research=no` | Nada a investigar: as três confusões vieram nomeadas por quem tropeçou, e as duas formas de instalar foram executadas. |
| `data-model.md` | `ART:data-model=no` | Nenhuma entidade nova. |
| `contracts/` | `ART:contracts=no` | Nenhuma interface nova; o portão lê o `case` do despachante, que já existe. |
| `checklist.md` | `ART:checklist=no` | Cinco critérios, um deles provado por mutação e os outros por leitura independente. |
| `ux-design.md` | `ART:ux-design=no` | Não toca tela. |

## How

**O README ganha três coisas, nesta ordem** — porque a ordem é o defeito:

1. *"O clone é a ferramenta. O alvo é outro projeto."* — uma frase, antes de qualquer comando,
   e as **duas** direções logo abaixo (de dentro do projeto; de dentro do clone).
2. **A árvore depois da instalação**, gerada de uma instalação real em projeto vazio, com o que
   cada camada é. Ela responde sozinha "o que isso vai fazer no meu repositório?".
3. **Um bloco endereçado a uma IA** que abre o repositório: o que ler, o comando que responde
   pelo estado, o que nunca reescrever, como abrir um ciclo. Aponta, nunca repete.

E `agents` sai do bloco numerado de instalação: ele é **consulta**, e estar como "passo 2 de 3"
era o que fazia parecer obrigatório.

**`check-flags.sh` passa a conferir subcomandos** do `maestro`, com os mesmos dois modos do
ciclo 058: referência (o `usage()`) nos dois sentidos, prosa (README) no sentido "todo
subcomando citado existe". É a mesma classe de mentira que o 058 fechou para flags, aberta na
porta que o 058 construiu.

## Verification (DoD)

| Comando | Esperado |
|---|---|
| instalar de dentro do projeto (`maestro init .`) | funciona — **executado** |
| instalar de dentro do clone apontando para fora | funciona — **executado** |
| a árvore publicada × uma instalação real | idêntica em camadas e contagens, e **declarada como sendo de `--ai claude`**: com outro agente ela é menor |
| **mutação 1**: README anuncia `maestro deploy` | portão **reprova** |
| **mutação 2**: subcomando existente fora do `usage()` | portão **reprova** |
| **contraprova**: subcomando citado só em prosa, existente | passa |
| cada arquivo e comando citado no bloco para IA | existe no disco — conferido um a um |
| os **14 portões bloqueantes** · plugin · build | verdes (os três consultivos — `cycle`, `retro`, `conformance` — são vermelhos por desenho enquanto o ciclo está aberto) |
