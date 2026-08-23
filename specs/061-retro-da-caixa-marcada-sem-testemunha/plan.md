# Plan 061 — Retro: a caixa marcada sem testemunha

- **Spec**: `spec.md` · **Lane**: plena · **Date**: 2026-08-22

## Constitution Check (governance/principles.md)

| Principle | Compliance |
|---|---|
| I. Spec-driven | ✅ Seis FRs, cada um amarrado a um achado aberto nomeado; nenhum remédio sem achado, nenhum achado sem remédio. |
| II. Human-governed orchestration | ✅ A retro foi **chamada pelo Steward**, com o vermelho consultivo à vista desde o ciclo 060. O portão de mérito continua humano. |
| III. Reversibility / risk gates | ✅ Portões e texto. O único que muda comportamento de terceiro é a instrução do `plan-architect`, que **retira** uma exigência — nunca acrescenta. |
| IV. Test-first / verifiable DoD | ✅ Cada portão criado ou alterado tem mutação **e** contraprova. A contraprova é o que faltava: o FR1 só vale se um ciclo recém-aberto passar. |
| V. Context economy / boundary | ✅ Nenhum portão novo: FR1 e FR5 entram em `check-conformance.sh` e `check-installed.sh`, que já existem e já fazem o trabalho caro. |
| VI. Living artifacts | ✅ É o ponto do ciclo: cinco achados saem do índice fechados por decisão, não por esquecimento. |
| VII. Light governance / YAGNI | ✅ O FR2 bloqueia **uma metade** do `check-conformance.sh`, não ele inteiro — a razão de ele ser consultivo continua válida e continua respeitada. |
| VIII. Intelligible communication | ✅ O CHANGELOG passa a distinguir nota de release de diário de bordo. |

## Artifacts of this cycle (declare all five — silence is not a decision)

<!-- Read by scripts/check-conformance.sh. Declaring =yes means the file MUST exist here.
     What each one is for: docs/governance/artifacts.md -->

| Artifact | Declaration | Why |
|---|---|---|
| `research.md` | `ART:research=no` | Os fatos vieram do `retro.sh` e do `git log`, e estão na spec. |
| `data-model.md` | `ART:data-model=no` | Nenhuma entidade nova. |
| `contracts/` | `ART:contracts=no` | Nenhuma interface entre partes. |
| `checklist.md` | `ART:checklist=no` | Quatro critérios de aceitação, todos provados por mutação e contraprova. |
| `ux-design.md` | `ART:ux-design=no` | Não toca tela. |

## How

**FR1 + FR2 — a metade que pode bloquear.** O `check-conformance.sh` ganha um modo
`--ticked-only`: percorre os mesmos ciclos, mas só reprova quando uma caixa `TAIL` está
**marcada** e a evidência correspondente **não** está no `qa-report.md`. Ciclo sem caixa
marcada passa. Esse modo entra na lista **bloqueante** da CI; o `check-conformance.sh`
completo continua consultivo, no job que já existe. Uma leitura, dois níveis de exigência.

**O plugin entra pela mesma porta.** `TAIL:gate` marcado é a afirmação de que a bateria
passou; o modo `--ticked-only` roda `package-plugin.sh --verify` quando encontra `TAIL:gate`
marcado no ciclo mais novo. Quatro ocorrências seguidas param de depender de memória.

**FR3 — data de commit não é data de mudança.** O `check-chapters.sh` passa a perguntar
antes: se `git status --porcelain` acusa o `SKILL.md` como modificado (ou não rastreado), a
data efetiva é **hoje**; senão, é a do último commit. Uma linha antes do `git log`, e o portão
deixa de ser estruturalmente incapaz de disparar no ciclo que o causa.

**FR4 — tirar a promessa.** O `plan-architect`, nas duas cópias (raiz e `.claude/agents/`),
para de mandar consumir a linguagem ubíqua como se ela existisse: passa a dizer que **se**
`docs/governance/ubiquitous-language.md` existir, é fonte obrigatória; se não existir e o
domínio pedir, o próprio plano deve propor criá-la. Instrução que funciona nos dois mundos.

**FR5 — as contagens.** O `check-installed.sh` já faz a instalação de onde todos esses números
saem. Ele passa a extrair de `README.md` e da receita os pares *(número, coisa)* que afirmam
contagem de uma camada instalada, e a compará-los com o que a instalação tem. Só as camadas
que a instalação **cria** — número em prosa sobre outra coisa não é promessa.

**FR6 — o CHANGELOG.** As quatro seções `### Adicionado` de `[Unreleased]` viram uma. O
`check-version.sh`, que já lê o CHANGELOG para achar a versão, passa a reprovar tipo repetido
dentro de uma mesma versão.

**Por fim, os cinco `fecha`.** Cada achado ganha uma linha nova no índice nomeando-o. O
`achado-055` fecha por **decisão** (a promessa saiu), não por evento — que é exatamente a
lição do FR1 do ciclo 055.

## Verification (DoD)

| Comando | Esperado |
|---|---|
| **mutação 1**: caixa `TAIL:review` marcada, evidência apagada do `qa-report` | `--ticked-only` reprova |
| **contraprova 1**: ciclo recém-criado pelo `new-cycle.sh`, nenhuma caixa marcada | `--ticked-only` **passa** |
| **mutação 2**: plugin dessincronizado com `TAIL:gate` marcado | `--ticked-only` reprova |
| **mutação 3**: `SKILL.md` alterado e não commitado, capítulo com data antiga | `check-chapters.sh` reprova **no mesmo ciclo** |
| **contraprova 3**: árvore limpa | `check-chapters.sh` passa |
| **mutação 4**: README afirma 14 subagentes | `check-installed.sh` reprova |
| **mutação 5**: duas seções `### Adicionado` na mesma versão | `check-version.sh` reprova |
| `check-retro.sh` | verde, com os cinco achados fechados no índice |
| os 14 portões bloqueantes · plugin · build | verdes |
