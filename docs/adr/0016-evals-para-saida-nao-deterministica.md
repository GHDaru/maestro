# ADR 0016 — Evals como critério para saída não-determinística

- **Status**: Aceito · **Data**: 2026-08-06
- **Ciclo**: 037 · **Decisor**: Steward
- **Emenda**: `docs/governance/axioms.md` 1.0.0 → 1.1.0 (teorema T7, corolário C11)

## Contexto

Os oito portões do Maestro medem o que se compara por igualdade: seção presente, link que
resolve, lista que bate com o disco. Nenhum mede um **julgamento** — o veredito de um agente
de revisão, a chamada de raia de um guardião, o trade-off de um plano.

O limite estava conhecido e escrito. A única ocorrência de `judge` em `scripts/` é o
comentário do `check-cycle.sh` (linha 8) admitindo que o portão *"cannot judge the answer"*.
Ou seja: identificamos a lacuna, documentamos e paramos ali — por trinta e seis ciclos,
treze agentes operaram **sem nenhuma linha de base**. Se alguém editasse `review.md` e
piorasse o agente, nada acusaria.

O gatilho externo foi a leitura de *The New Software Lifecycle* (Addy Osmani / O'Reilly,
15/07/2026, resumo do whitepaper "The New SDLC With Vibe Coding" — *software development
lifecycle*, ciclo de vida de desenvolvimento de software). O artigo separa dois mecanismos
de verificação: testes para saída determinística e **evals** para saída não-determinística,
com a régua "no eval, não no demo". A separação nomeia exatamente o buraco que já era nosso.

## Decisão

1. **Teorema T7** entra na camada de axiomas: onde a saída não se compara por igualdade, o
   critério é uma **linha de base registrada** — entrada fixa, asserções que discriminam,
   observação datada. Deriva de A2 e A4, pelo mesmo caminho do T4, e cobre onde o T4 não
   alcança. **Corolário C11**: um eval nomeia seu alvo e defasa quando o alvo muda.

2. **A anatomia de um caso** é três arquivos de texto em `evals/<NNN-slug>/`:

   | Arquivo | Campos obrigatórios |
   |---|---|
   | `case.md` | `Target:` (caminho existente) · `Question:` |
   | `expect.md` | ≥1 `MUST-FIND:` · ≥1 `MUST-NOT-CLAIM:` |
   | `baseline.md` | `Date:` · `Target-commit:` · `First-red:` · `Verdict:` |

   Dois campos carregam o desenho inteiro. **`MUST-NOT-CLAIM`** é o que discrimina: um caso
   só com `MUST-FIND` passa com qualquer resposta prolixa que mencione as palavras certas; a
   asserção negativa diz o que uma resposta errada afirmaria. **`First-red`** é a segunda lei
   da `verifiable-dod` virada campo — enquanto ninguém viu o caso reprovar alguma coisa, ele
   é esperança, e o portão fala isso em voz alta.

3. **A verificação é partida em duas**, e a divisão é a decisão que mais importa aqui:

   - **determinística e gratuita** (`scripts/check-evals.sh`): estrutura, alvo existente,
     asserções que discriminam, linha de base defasada, linha de base pendente. Roda em
     qualquer máquina, sem chave, sem custo por execução.
   - **com modelo no laço** (`/eval`, comando): executa o caso em **contexto fresco** e grava
     a linha de base. Sob demanda, **fora da integração contínua** (CI).

4. **A defasagem é a forcing function.** A linha de base grava o commit do alvo; editar
   `.claude/agents/review.md` deixa o caso defasado e o portão nomeia a deriva. É isso que
   impede `evals/` de virar a documentação que ninguém consome (T5, corolário C9).

5. **`evals/` é superfície instalável** — escrita em inglês e coberta pelo
   `check-language.sh` (ADR 0014).

## Alternativas consideradas

- **Eval na integração contínua.** Rejeitada: exige chave e custo por execução, e um portão
  que nem todo mundo consegue rodar deixa de ser portão para virar privilégio. O que roda em
  CI é a saúde do corpus, que é determinística.
- **Um agente juiz automático que aprova ou reprova o ciclo.** Rejeitada por A2 e pelo
  princípio II: o eval produz veredito por asserção; ler o veredito e decidir continua humano.
- **Cobrir os treze agentes de saída.** Rejeitada por YAGNI e pelo princípio V. Dois casos;
  a cobertura cresce por gatilho — um agente que regrediu ganha caso.
- **Não fazer nada e confiar na revisão atenta.** É a alternativa que já foi testada: nove
  defeitos escaparam para a linha principal e **nenhum** foi pego por leitura.

## Consequências

**Boas.** A camada de axiomas passa a cobrir a verificação de julgamento, que era o vão
entre o T4 e a prática. O corpus tem forcing function própria (defasagem) e uma regra
anti-autoengano embutida (`First-red`). O custo é três arquivos de texto e um script `bash`.

**Ruins, e assumidas.**

- **O portão nasce vermelho.** As duas linhas de base exigem modelo no laço, que o ciclo 037
  não executou. Vermelho declarado é informação; verde falso é dano — e há precedente direto:
  o `check-install.sh` nasceu vermelho no ciclo 021 com deriva real de três ciclos, e foi
  assim que a deriva apareceu. A dívida está no índice de decisões como achado aberto, ao
  alcance do gatilho da retro.
- **Nenhum eval executado ainda mede qualidade de verdade.** Este ADR entrega a forma, não a
  medida. A forma sem a medida é metade do valor, e a metade que falta é a que custa dinheiro.
- **`MUST-FIND`/`MUST-NOT-CLAIM` são julgados por leitura de quem roda `/eval`.** Ou seja: o
  eval reduz o julgamento, não o elimina. Fingir o contrário seria o anti-padrão 13 (o check
  que mede o proxy) aplicado ao próprio mecanismo anti-proxy.
- **Dois casos não cobrem treze agentes.** A cobertura é declarada, não estimada.

## Referências

- `docs/governance/axioms.md` (T7, C11) · `evals/README.md` · `scripts/check-evals.sh`
- ADR 0015 (a camada de axiomas) · ADR 0014 (inglês no instalável)
- Capítulo 02 do livro — os nove defeitos escapados e a leitura DORA
