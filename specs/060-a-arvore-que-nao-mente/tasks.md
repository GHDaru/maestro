# Tasks 060 — A árvore que não mente

## Verification first
- [x] T0 — medir onde a árvore está e onde não está (`grep -rln`, `sumario.json`), em vez de
      supor que "documentação" e "capa do repositório" são a mesma coisa.

## Implementation
- [x] T1 — a árvore sai do README e entra na receita, sob título ASCII (âncora que resolve nos dois).
- [x] T2 — o README aponta para a âncora. A frase-resumo que o plano previa foi **retirada**:
      repetia palavra por palavra o parágrafo apontado, e um fato dito em dois lugares sem nada
      comparando os dois é o defeito que este ciclo existe para fechar (achado da revisão).
- [x] T3 — o livro diz que existe instrução para IA e onde ela mora, e por que mora lá.
- [x] T4 — `check-installed.sh` compara a árvore publicada com uma instalação feita na hora.
- [x] T5 — `check-installed.sh` compara os ids `--ai` publicados na receita com os que o
      instalador aceita. Não estava no plano: entrou porque a revisão achou a receita mandando
      usar `--ai cursor` e `--ai generic`, ids que o instalador **recusa** desde o ciclo 057.
- [x] T6 — o passo 4 da receita passa a mandar `cd` para o projeto antes de rodar os portões.
      Sem isso, os quatro comandos devolviam um verde do repositório do método — o defeito do
      `cd "$HERE"` do ciclo 058, reaberto em prosa.

## Closing tail — MANDATORY, one line each, never delete
<!-- TICK ONLY WHILE WRITING THE EVIDENCE, never in advance: the box records what happened.
     Do not delete a line to say it does not apply: write `n/a: <reason>` on it.
     check-conformance.sh requires the evidence of every non-n/a step in qa-report.md. -->
- [x] TAIL:review — independent review in fresh context, by whoever did not execute
- [x] TAIL:security — security pass proportional to the risk class
- [x] TAIL:mutation — every gate created or changed here, broken on purpose and seen refusing
- [x] TAIL:gate — DoD green -> guardian verdict -> human merge gate (not delegable)
