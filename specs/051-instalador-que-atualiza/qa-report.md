# QA report 051 — O instalador que atualiza

- **Date**: 2026-08-11 · **Lane**: plena · **Verdict**: aprovado após reprovação e correção

## Fitness functions (DoD)

| Check | Expected | Result |
|---|---|---|
| `scripts/check-installed.sh` — cenário de upgrade | dez asserções verdes | ✅ |
| reinstalar sem mudança (3×) | idempotente, `already current` | ✅ hash da árvore idêntico |
| `--force` | sobrescreve em lugar, guarda `.maestro-old`, não aninha | ✅ |
| `--force --dry-run` | não escreve nada | ✅ |
| os outros quinze portões · plugin · build | verdes | ✅ |
| `scripts/check-conformance.sh 051` | verde | ✅ |

### O defeito de origem, reproduzido antes de qualquer correção

| Comando | Antes |
|---|---|
| `install-maestro.sh <alvo>` (2ª vez) | `= exists (kept)` para tudo — **zero** entregue |
| `install-maestro.sh <alvo> --force` | `cp -r` sobre diretório existente **aninha**: `.claude/agents/agents/` |

### As cinco mutações que provam o cenário novo

O revisor mutou o **instalador corrigido**, uma vez por invariante, e cada mutante matou
exatamente a asserção correspondente: sem poda → só "removed" vermelha; sempre sobrescreve →
"kept" e "beside"; sem `.maestro-new` → "beside"; nunca atualiza → "refreshed". Com o
instalador **antigo**, o cenário fica vermelho já no manifesto.

## Closing tail — the evidence

- TAIL:review — revisão independente em contexto fresco, por quem não executou. Veredito:
  **NÃO PROMOVER COMO ESTÁ**, dois bloqueantes e cinco relevantes. **O primeiro bloqueante é
  o pior defeito que eu poderia ter escrito neste ciclo**: `install_file` gravava o caminho no
  manifesto **antes de qualquer decisão**, então um arquivo que o projeto já tinha e que por
  acaso fosse byte-idêntico ao nosso — o caso real de quem rodou `specify init` por conta
  própria, cujo `.specify/scripts/bash/` é o mesmo — era adotado como nosso **sem uma linha
  de saída**, e a poda o **apagava** no release seguinte. Um instalador que apaga arquivo
  alheio é exatamente o risco que a raia plena deste ciclo existe para conter, e eu o
  introduzi. O segundo: `--force --dry-run` lia só `$2`, virava `FORCE=1 DRY=0` — a flag
  destrutiva vencendo e o freio ignorado, no único script que apaga. Relevantes: `--force`
  destruía edição do projeto **sem cópia** enquanto a própria saída o recomendava; a poda
  aceitava `../` vindo do manifesto (que mora no repositório alheio e é comitável) e apagou
  arquivo **fora do alvo**; o manifesto não era transacional; e o `--force` — o defeito
  relatado — **não tinha cenário nenhum** no portão. **Todos corrigidos**, e os três ataques
  do revisor foram reproduzidos contra a versão corrigida: manifesto não reivindica (0),
  `--force --dry-run` preserva, travessia recusada com aviso.
- TAIL:security — passe proporcional, e **esta é a classe de risco mais alta da sessão**: o
  script roda dentro do repositório de terceiro e **apaga**. Quatro superfícies. **(a)
  Travessia**: o manifesto é dado, nunca comando; toda entrada com `/` inicial ou `..` é
  recusada com aviso antes de chegar ao `rm`. **(b) Escopo da remoção**: só caminhos que o
  manifesto prova que **nós** escrevemos, e só enquanto o hash bater; o que o projeto
  modificou é mantido e dito. **(c) Destruição por flag**: `--force` passa a guardar
  `.maestro-old`, e `--dry-run` vence qualquer combinação. **(d) Permissões**: o bit de
  execução vai só para os scripts que **nós** escrevemos — antes ia para todo `.sh` do
  diretório, inclusive os do projeto. Limite declarado: *symlink* de diretório no alvo faz o
  `cp` escrever através dele; comportamento herdado, agora com remoção junto — registrado
  como achado.
- TAIL:gate — DoD verde, dezesseis portões + plugin + build verdes, `check-conformance 051`
  verde. **Aguarda o gate humano** de promoção `dev` → `main`.

## Requirement coverage

- **FR1** — manifesto `hash⇥caminho`, e agora **só** do que escrevemos: reivindicar é
  consequência de escrever, não de olhar.
- **FR2** — inalterado desde a última instalação **e** diferente da origem → atualiza.
- **FR3** — modificado pelo projeto → mantido, com `.maestro-new` ao lado; o manifesto guarda
  o hash que **nós** escrevemos, para não adotar a edição alheia na execução seguinte.
- **FR4** — poda só do que o manifesto prova ser nosso e inalterado; caminho validado.
- **FR5** — `find -type f` arquivo a arquivo; nenhum diretório aninhado, com e sem `--force`.
- **FR6** — instalação anterior ao manifesto não sobrescreve nada, explica por quê **e nomeia
  os caminhos aposentados** que ela não pode remover sem prova.

## Achados registrados neste ciclo

- **Eu dei ao instalador o poder de apagar e, na mesma versão, fiz com que ele reivindicasse
  arquivo que nunca escreveu.** Os dois juntos apagam trabalho alheio em silêncio. Só a
  revisão em contexto fresco viu.
- **A mitigação que declarei no Constitution Check não existia**: escrevi que o `--dry-run`
  mostra antes, e `--force --dry-run` ignorava o freio.
- ***Symlink* de diretório no alvo**: o `cp` escreve através dele e a poda removeria através
  dele. Herdado do `cp -r`, agora com consequência maior. Fica aberto.

## Pending gate

- Promoção `dev` → `main` aguarda aprovação humana.
