# QA report 062 — Fechar a v0.3.0

- **Date**: 2026-08-22 · **Lane**: plena · **Verdict**: DoD verde; aguardando parecer e portão humano

## Fitness functions (DoD)

| Check | Expected | Result |
|---|---|---|
| `check-version.sh` | verde com `0.3.0` | ✅ CHANGELOG, README, roadmap e plugin |
| **mutação 1**: README declarando `0.2.0` | reprova | ✅ "the front page says 0.2.0 and the CHANGELOG says 0.3.0" |
| **mutação 2**: roadmap declarando `0.2.0` | reprova | ✅ idem, nomeando o roadmap |
| **mutação 3**: plugin declarando `0.2.0` | reprova | ✅ idem, nomeando o plugin |
| **mutação 4**: CHANGELOG cortando `0.2.1` | reprova | ✅ 4 reprovações — os três lugares + a ordem |
| **mutação 5**: exemplo da receita com versão velha | `check-installed.sh` reprova | ✅ "sample says maestro_version='0.2.0', and init writes '0.3.0'" |
| **mutação 6**: exemplo com chave que o instalador não grava | reprova | ✅ "key 'telemetry' is in the recipe's sample and not in the other" |
| **mutação 7**: o bloco de exemplo some da receita | reprova | ✅ "publishes no install-options.json sample the gate can parse" |
| **contraprova 5–7**: exemplo correto | passa | ✅ |
| `[Unreleased]` novo | existe e está vazio | ✅ |
| `git ls-remote --tags origin` | o que a nota afirma é o que isto devolve | ✅ devolve **vazio**; a nota diz "nenhuma tag existe no remoto — nem esta" |
| 14 portões bloqueantes · `--ticked-only` · plugin · build | verdes | ✅ |

## A tag: o que foi tentado e o que aconteceu

`git tag -a v0.3.0` criou a tag **local**, anotada, sobre o commit do corte. `git push origin
v0.3.0` foi tentado **quatro vezes**, com espera exponencial, e morreu nas quatro em
`send-pack: unexpected disconnect while reading sideband packet`. O ambiente onde este corte
foi feito roteia o git por um proxy que não relaia ref de tag — os pushes de **branch** no
mesmo remoto funcionam normalmente, incluindo os deste ciclo.

Em seguida `git ls-remote --tags origin` foi executado e devolveu **vazio**. Isso não é só
sobre a v0.3.0: **nenhuma** tag existe no repositório remoto, nem a v0.1.0 nem a v0.2.0. A nota
de release afirma exatamente isso, e nomeia o comando que resolve, de uma máquina com acesso
direto: `git push origin v0.1.0 v0.2.0 v0.3.0` (as duas primeiras precisam ser criadas — não
existem nem localmente).

Uma nota de release que anunciasse um lançamento publicado seria o anti-padrão 13 aplicado ao
próprio lançamento: medir a frase ("cortamos a v0.3.0") em vez do fato (o que está no remoto).

## Closing tail — the evidence

- **TAIL:review** — **não executada**. A revisão independente em contexto fresco rodou em
  todos os ciclos 053–060 e **reprovou em todos**, com 19–20 achados por ciclo. Nestes dois
  ela não rodou: esta sessão está configurada para não abrir subagente sem pedido explícito do
  Steward. Isso está registrado aqui em vez de comprado com um `n/a`, porque estes ciclos
  **mexeram em portão** — que é exatamente o caso em que a dispensa não existe.

- **TAIL:security** — classe de risco **média por um item só**: a tag é o único artefato deste
  ciclo destinado a sair do repositório, e ela **não saiu**. O resto é texto. O portão novo lê
  o CHANGELOG e a receita como **dados**: o `python3` recebe caminhos por `argv` e faz
  `json.loads` do bloco cercado — nada é interpolado em comando, e um bloco `json` inválido é
  ignorado em vez de explodir. Nenhum segredo, nenhuma rede, nenhuma escrita fora de `mktemp`.

- **TAIL:mutation** — sete mutações e uma contraprova, todas com o resultado esperado (tabela
  acima). O portão do FR3 nasceu **acusando**: o `maestro_version` publicado na receita estava
  em `0.2.0` havia onze ciclos, e nada o lia. A mutação 4 rendeu o achado mais útil — cortar
  uma versão errada no CHANGELOG derruba os três lugares de uma vez, que é o comportamento
  correto e não estava provado.

- **TAIL:gate** — DoD verde (14 portões bloqueantes, `--ticked-only`, plugin em sincronia,
  livro gerando) → **portão humano concedido pelo Steward em 2026-08-22** ("mande para main"),
  com a ausência da revisão independente dita antes da decisão, não depois.

## Dívida declarada, não apagada

- **A revisão independente não rodou nos ciclos 061 e 062.** Rodou em 053–060 e reprovou nos
  oito, com 19–20 achados por ciclo. Estes dois criaram ou alteraram **seis** portões
  (`check-conformance --ticked-only`, `check-chapters`, duas comparações novas no
  `check-installed`, `check-version`, e o portão do `install-options.json`) e cada um deles foi
  provado por mutação **e** contraprova — mas mutação é prova de que o portão sabe reprovar, não
  de que ele mede a coisa certa. Foi disso que a revisão viveu nos oito ciclos anteriores.
- **O `check-conformance.sh` aceitou "pendente." como evidência** de `TAIL:review` e
  `TAIL:gate`, e imprimiu `✓` para as duas — anti-padrão 13 dentro do portão que existe para
  pegá-lo. Registrado como `achado-062-pendente-passa-por-evidencia`. Este ciclo escreveu a
  verdade no lugar da palavra em vez de aproveitar o verde.

- **As tags não existem no remoto** — nem v0.1.0, nem v0.2.0, nem v0.3.0. Registrado como
  achado no índice, com o comando exato e a razão pela qual precisa da máquina do Steward.
- **O `check-cycle.sh` está vermelho por um commit deste conjunto**: a mensagem do ciclo 061
  diz `ciclo 061 (retro):` e o portão procura a citação sem o parêntese logo depois. O commit
  já está publicado; reescrever histórico compartilhado para deixar um portão consultivo verde
  seria pior que a dívida. Fica declarado.
