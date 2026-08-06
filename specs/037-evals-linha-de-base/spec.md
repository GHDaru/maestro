# Spec 037 — Evals: linha de base para saída não-determinística

- **Status**: Concluída · **Raia**: plena · **Data**: 2026-08-06
- **Origem**: leitura do artigo *The New Software Lifecycle* (Addy Osmani / O'Reilly,
  15/07/2026, resumo do whitepaper "The New SDLC With Vibe Coding") — a tese "coloque a
  régua no eval, não no demo" expôs uma lacuna medida no próprio repositório.

> **Raia**: plena. **Ambiguidade** média (o objeto — o caso de eval — não existia aqui, mas
> a forma é conhecida); **raio** amplo (mexe na camada de axiomas, que é a base de derivação
> de tudo); **irreversibilidade** baixa (é documento e script novo; nada é apagado).

## O quê e por quê

Os oito portões do Maestro são **todos determinísticos**: contam seções, resolvem links,
comparam listas com o disco. Nenhum olha para a **qualidade** de uma saída que não se
compara por igualdade — o veredito de um agente de revisão, o julgamento de raia de um
guardião, a decisão de um plano.

A medida está no nosso próprio código: a única ocorrência de `judge` em `scripts/` é um
comentário do `check-cycle.sh` (linha 8) admitindo o limite —

> *"It forces the thinking and makes the skew visible; it cannot judge the answer."*

Sabíamos do buraco, documentamos e paramos ali. O resultado é que **treze agentes operam
sem nenhuma linha de base**: se alguém editar `review.md` e piorar o agente, nada acusa.
O T4 ("critério sem comando não é critério") vale hoje só onde `grep` alcança.

O custo já foi pago uma vez: dos **nove defeitos que escaparam** para a linha principal
(capítulo 02), nenhum foi pego por leitura atenta — todos por um check que alguém escreveu.
Para saída não-determinística, esse check não existe.

## Requisitos funcionais

- **FR1**: QUANDO a camada de axiomas for consultada, O SISTEMA DEVERÁ oferecer um teorema
  que derive a necessidade de linha de base para saída não-determinística, com evidência
  deste repositório.
- **FR2**: QUANDO um caso de eval for adicionado, O SISTEMA DEVERÁ exigir dele um alvo
  existente, ao menos uma asserção `MUST-FIND` e ao menos uma asserção `MUST-NOT-CLAIM` —
  um eval que só verifica "respondeu alguma coisa" não discrimina.
- **FR3**: QUANDO o arquivo alvo de um caso mudar depois da linha de base registrada, O
  SISTEMA DEVERÁ falhar identificando o caso como **defasado** — editar um agente sem
  reavaliar é o modo de falha real.
- **FR4**: QUANDO um caso ainda não tiver sido visto discriminando (nenhum vermelho
  registrado), O SISTEMA DEVERÁ falhar contando esses casos — pela segunda lei da
  `verifiable-dod`, um eval que nunca acusou é uma esperança.
- **FR5**: QUANDO alguém precisar produzir ou renovar uma linha de base, O SISTEMA DEVERÁ
  oferecer um comando que execute o caso em **contexto fresco** e grave o resultado.

## Fora de escopo

- Rodar eval em integração contínua — exige modelo no laço, com custo por execução e chave.
  O portão determinístico roda em toda máquina; a execução do eval é sob demanda.
- Cobrir os treze agentes. Dois casos-semente; a cobertura cresce por gatilho, não por meta.
- *Progressive disclosure* de contexto (o outro buraco do artigo) — sem gatilho ainda:
  as seis skills somam 419 linhas. Abrir ciclo agora seria cerimônia (anti-padrão 17).
- Reescrever o `check-cycle.sh` para julgar a resposta. Ele mede o que sabe medir.

## Critérios de aceite (DoD)

- [x] `docs/governance/axioms.md` tem T7 com evidência citável e um corolário associado;
      versão sobe para 1.1.0 e o ADR registra a emenda.
- [x] `scripts/check-evals.sh` existe e cobre FR2, FR3 e FR4.
- [x] O portão foi **visto acusar** em cada uma das três condições (estrutura, defasagem,
      pendência), com a saída registrada no `qa-report.md`.
- [x] `evals/` tem dois casos-semente com alvo real, asserções que discriminam e linha de
      base declarada como **pendente** — a dívida fica no índice de decisões, não implícita.
- [x] `.claude/commands/eval.md` descreve como produzir a linha de base em contexto fresco.
- [x] `scripts/check-language.sh` passa a cobrir `evals/` (superfície instalável, ADR 0014).
- [x] Os oito portões existentes continuam verdes.

## Clarify

1. O portão entra vermelho na entrega? **Sim, e de propósito** — as duas linhas de base
   exigem modelo no laço, que este ciclo não executa. Precedente: `check-install.sh`
   nasceu vermelho no ciclo 021 com deriva real de três ciclos, e foi assim que a deriva
   apareceu. Vermelho declarado é informação; verde falso é dano.
