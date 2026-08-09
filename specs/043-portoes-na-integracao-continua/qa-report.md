# Relatório de QA 043 — Os portões entram na integração contínua

- **Data**: 2026-08-07 · **Raia**: infra · **Veredito**: aprovado **depois de reprovado**

## Fitness functions (DoD)

| Check | Esperado | Resultado |
|---|---|---|
| simulação do passo bloqueante (8 portões) | verde | ✅ todos OK |
| `scripts/package-plugin.sh --verify` | verde | ✅ 32 arquivos em sincronia |
| `npm ci --ignore-scripts --prefix publicar && node publicar/build.mjs` | verde | ✅ 37 páginas |
| `scripts/check-conformance.sh` | verde | ✅ 042 e 043 conformes |
| `MAESTRO_TRACE_BASE=origin/main scripts/check-cycle.sh` · `check-retro.sh` | consultivos | ✅ ambos verdes |
| `bash -n` em `ci.yml` (via revisão) e em `promote-main.sh` | sintaxe | ✅ |

## Closing tail — a evidência

- **TAIL:review** — revisão independente em contexto fresco, por subagente com a instrução
  de `.claude/agents/review.md`, num **clone limpo** do repositório (para que bit de
  execução, symlink e ausência de `node_modules` fossem reais). **Veredito: "Do not merge
  as-is."** Quatro achados, dois bloqueantes e um de julgamento — o último mudou o desenho
  do ciclo. Detalhe abaixo.
- **TAIL:security** — passagem executada, não dispensada. Itens conferidos: gatilho é
  `pull_request` e **não** `pull_request_target` (PR de fork roda com token somente-leitura
  e sem segredo — é a propriedade mais consequente do arquivo); nenhum segredo é referenciado;
  `permissions: contents: read` no topo; a única interpolação `${{ }}` num corpo `run:` era
  o SHA da base, agora passada por `env` para eliminar a **classe** de erro; `npm ci` com
  *lockfile* e agora `--ignore-scripts`; `timeout-minutes` nos dois jobs.
  **Riscos residuais, declarados**: as *actions* estão fixadas por tag maior (`@v4`) e não
  por SHA — comprometer a tag daria execução num runner efêmero com token somente-leitura e
  sem segredo, ou seja, acesso ao que já era público; e `on: push: ["**"]` executa scripts
  do repositório a partir de qualquer branch empurrada, o que é inerente e **não** é buraco
  novo (quem empurra já tinha esse poder). Os dois deixam de ser aceitáveis no dia em que um
  segredo entrar neste workflow — está escrito no arquivo, na linha que se deve revisitar.
- **TAIL:gate** — pendente: promoção `dev` → `main` aguarda aprovação humana.

## O achado que mudou o desenho (G4)

A revisão marcou como julgamento para o humano, e estava certa:

> *"a gate that is red on almost every push is a gate people learn to scroll past, which is
> the failure mode the cycle exists to prevent."*

`check-conformance` estava na lista bloqueante. Mas o `new-cycle.sh` gera o `qa-report.md`
como placeholder **por desenho**, e o portão rejeita placeholder — logo ele fica vermelho
do primeiro ao último commit de qualquer ciclo. É exatamente o critério que eu tinha usado
para mover `check-cycle` e `check-retro` para consultivo, e mesmo assim coloquei este no
bloqueante.

**Resolução escolhida**: conformidade sai do bloqueante da CI e é aplicada **onde um ciclo
de fato termina** — o `promote-main.sh` agora **recusa promover** enquanto ela estiver
vermelha. O sinal fica mais forte, não mais fraco: durante o ciclo é aviso; na hora de
entrar na linha principal é impedimento.

## O erro que cometi pela terceira vez

Marquei `TAIL:review` e `TAIL:security` com `[x]` apontando para evidência que não existia —
o `qa-report.md` era o esqueleto do gerador. Igual ao ciclo 042. **E desta vez a simulação
local já tinha mostrado o vermelho** (`check-conformance FALHOU`) e eu segui mesmo assim,
preenchendo spec, plano e tarefas e deixando o relatório para depois.

Terceira ocorrência com a mesma pessoa e a mesma intenção. Duas coisas mudaram por causa
dela: o `tasks-template.md` e o `new-cycle.sh` agora dizem **"marque apenas enquanto escreve
a evidência, nunca antes — a caixa registra o que aconteceu, não é plano"**; e a promoção
passou a recusar conformidade vermelha, o que faz uma caixa marcada sem testemunha não
alcançar a `main`.

## Os outros três achados

| # | Achado | O que fiz |
|---|---|---|
| G1 | o job ficava vermelho no próprio commit que o introduz | `qa-report.md` escrito (este) + conformidade movida para consultivo |
| G2 | `T7` marcado com `CHANGELOG`, roadmap e índice ausentes do diff — o que também derrubava o job de `CHANGELOG` | os três entraram; `achado-042-portoes-fora-da-ci` fechado |
| G3 | o critério "simulado localmente, com a saída no relatório" estava `[x]` sem relatório | este relatório |

Nits da revisão também absorvidos: `concurrency` (o job rodava duas vezes por commit em PR
do mesmo repositório), `timeout-minutes` nos dois jobs, `python3` declarado em comentário
como dependência não-explícita, e a base do `CHANGELOG` por `env`.

## O que a revisão confirmou que estava certo

Ela simulou num clone limpo e verificou: os `scripts/*.sh` mantêm o bit de execução
(`100755` no índice); `AGENTS.md` é symlink modo `120000` e o `check-install` o segue;
`fetch-depth: 0` é carga real, não enfeite; o passo consultivo **nunca** bloqueia (o corpo
do laço termina em `|| echo`, e o `for` devolve o status do último comando); e o passo
bloqueante bloqueia mesmo (o `fail` trava e o `exit "$fail"` devolve 1, com os portões
seguintes ainda rodando).

## Cobertura dos requisitos

- **FR1** ✅ oito portões estruturais + plugin + build, todos bloqueantes.
- **FR2** ✅ três consultivos agora (`check-cycle`, `check-retro`, `check-conformance`),
  com a razão do terceiro escrita no arquivo.
- **FR3** ✅ `permissions: contents: read`, nenhum segredo.
- **FR4** ✅ `MAESTRO_TRACE_BASE=origin/main` + fetch. A revisão notou que com
  `fetch-depth: 0` a referência já existe — o fetch fica como seguro, não como carga.

## Lição para a retrospectiva

**Marcar caixa antes de fazer o trabalho, três vezes.** Já virou regra em dois artefatos e
num portão de promoção. Se acontecer uma quarta, a conclusão deixa de ser sobre disciplina e
passa a ser sobre a ordem em que os artefatos do ciclo são escritos — provavelmente o
`tasks.md` não deveria ser escrito de uma vez.

## Pendência de gate

- Promoção `dev` → `main`: aguarda aprovação humana.
