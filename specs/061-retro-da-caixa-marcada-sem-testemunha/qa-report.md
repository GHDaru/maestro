# QA report 061 — Retro: a caixa marcada sem testemunha

- **Date**: 2026-08-22 · **Lane**: plena · **Verdict**: DoD verde; aguardando parecer e portão humano

## Fitness functions (DoD)

| Check | Expected | Result |
|---|---|---|
| **contraprova 1**: ciclo recém-criado pelo `new-cycle.sh`, nada marcado | `--ticked-only` **passa** | ✅ — e na primeira versão **reprovava**: ver "o que a contraprova achou" abaixo |
| **mutação 1**: `TAIL:review` marcado, `qa-report` no esqueleto | reprova | ✅ "TAIL:review in qa-report.md is still the placeholder" |
| **mutação 2**: plugin dessincronizado com `TAIL:gate` marcado | reprova | ✅ "TAIL:gate says the battery passed, and package-plugin.sh --verify disagrees" |
| **contraprova 2**: plugin em sincronia, `TAIL:gate` marcado | passa | ✅ "plugin in sync with its sources" |
| **mutação 3**: `SKILL.md` alterado e **não** commitado | `check-chapters.sh` reprova **no mesmo ciclo** | ✅ "skill 'anti-patterns' changed on 2026-08-23; 07-cerimonias-cadencia.md was revised on 2026-08-17" |
| **contraprova 3**: árvore limpa | passa | ✅ |
| **mutação 4**: README afirma 14 subagentes | reprova | ✅ "README.md says 14 subagentes, and a real installation has 13" |
| **contraprova 4**: `75+ agentes` e `**6.** Você não promove` | **não** reprovam | ✅ zero reprovações — número seguido de `+` e marcador de lista não são contagem desta instalação |
| **mutação 5**: duas seções `### Adicionado` em `[Unreleased]` | reprova | ✅ com as duas linhas |
| **contraprova 5**: uma seção por tipo | passa | ✅ |
| **mutação 6**: instrução nomeia arquivo que a instalação não cria | reprova | ✅ o `check-installed.sh` reprovou **a minha própria correção do FR4** |
| os cinco achados | fechados no índice por `fecha` | ✅ |
| `check-retro.sh` | verde por dívida paga | ✅ |
| 14 portões bloqueantes · plugin · build | verdes | ✅ — o `check-language.sh` reprovou primeiro: o código novo tinha prosa em português na superfície instalável (ADR 0014) |

## O que a contraprova achou, e por que ela era o item mais importante do plano

A primeira versão do `--ticked-only` **reprovava um ciclo recém-criado pelo `new-cycle.sh`** —
não pela cauda, que estava corretamente ignorada, mas porque o esqueleto declara
`ART:research=no` sem motivo e o portão cobra o motivo. Ou seja: eu teria posto na CI, como
bloqueante, exatamente o portão sempre-vermelho que este modo existe para evitar, e teria
descrito no `qa-report` que ele "só reprova quem afirmou sem ter".

O portão não estava errado; o **escopo** estava. `--ticked-only` foi reduzido a uma regra só —
uma tique sem lastro — e todo o resto passou por um `soft()`, que reprova na execução
consultiva e apenas relata na bloqueante. O contrato da CI ficou dizível numa frase.

Isso só apareceu porque o plano exigia a **contraprova** junto da mutação. Um portão provado
apenas por mutação prova que sabe reprovar; nada nele prova que sabe **passar**.

## Closing tail — the evidence

- **TAIL:review** — pendente.

- **TAIL:security** — classe de risco **baixa**: portões que leem arquivos do próprio
  repositório e uma instalação em `mktemp -d` com `trap … EXIT`, já existente. Nada abre rede,
  lê segredo ou escreve fora do temporário. Duas superfícies novas merecem nota: (1) o
  `--ticked-only` executa `scripts/package-plugin.sh`, script do próprio repositório, com
  saída descartada e sem argumento vindo de arquivo; (2) o `count_layer()` recebe o
  substantivo **de um `case` fechado** — um substantivo desconhecido devolve vazio e a
  comparação é pulada, nunca interpolada em comando. O `awk` do `check-version.sh` lê o
  CHANGELOG como dado, sem `system()`.

- **TAIL:mutation** — seis mutações e cinco contraprovas, todas com o resultado esperado
  (tabela acima). Duas encontraram defeito **meu, deste ciclo**: o escopo do `--ticked-only`
  (acima) e o `plan-architect` corrigido de um jeito que **criava** o defeito que ele estava
  fechando — a instrução passou a nomear `docs/governance/ubiquitous-language.md`, e o
  `check-installed.sh` reprovou na hora: *"installed files name … which the installation does
  not create"*. Nomear o caminho **é** a promessa. A correção da correção não nomeia arquivo
  nenhum e diz o que fazer quando não existe.

- **TAIL:gate** — pendente. DoD verde; falta o parecer independente e o portão humano.

## Dívida declarada, não apagada

- As seções já **lançadas** do CHANGELOG carregam a mesma repetição que o FR6 fecha (a v0.1.0
  repete `### Changed` duas vezes). Ficam como estão: entrada de changelog lançada é registro
  histórico, e retroatividade transforma portão em ruído — mesmo precedente dos pisos do
  `check-cycle.sh` e do `check-conformance.sh`. O escopo está escrito no portão.
- O `--ticked-only` não cobre `check-cycle` nem `check-retro`, que continuam consultivos pelas
  razões próprias deles. Este ciclo moveu **uma** regra de consultiva para bloqueante, de
  propósito.
