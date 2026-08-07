# Spec 041 — Retro: os quatro achados de eval viram regra

- **Status**: Concluída · **Raia**: plena · **Data**: 2026-08-07
- **Origem**: **o gatilho disparou sozinho**. Depois do ciclo 040, o `check-retro.sh` foi a
  vermelho: `✗ 4 open findings (limit 4)`. Ninguém lembrou da retro — a dívida cobrou.

> **Raia**: plena. **Ambiguidade** média (os achados eram conhecidos; o que fazer com cada
> um, não); **raio** amplo (mexe em skill, portão, comando e protocolo do índice);
> **irreversibilidade** baixa.

## O quê e por quê

O ciclo 034 deu gatilho à retro para ela não depender de memória. Sete ciclos depois o
gatilho funcionou pela primeira vez de verdade: quatro achados abertos, todos do mecanismo
de eval, e a retro pedindo passagem sem que nenhum humano tivesse de lembrar.

A retro encontrou um quinto achado que ninguém tinha registrado: **a própria ferramenta da
retro estava mentindo**. O `retro.sh` casava ids no formato `gate-NNN-*`, que só **sete**
gates usaram; desde o ADR 0009 o `promote-main.sh` grava `gate-main-<sha>` — **33 deles**.
Resultado: todo ciclo de 011 em diante era reportado como gate pendente. Por 29 ciclos.

## Requisitos funcionais

- **FR1**: QUANDO a retro apurar gates, O SISTEMA DEVERÁ decidir pelo fato (o commit que
  cita o ciclo está na linha principal), não pelo formato do identificador.
- **FR2**: QUANDO um caso de eval for criado, O SISTEMA DEVERÁ exigir o **eixo** que ele
  separa — sem eixo não há o que ablar, e uma aprovação não prova nada.
- **FR3**: QUANDO uma linha de base for gravada, O SISTEMA DEVERÁ exigir o resultado da
  **ablação** e da **conferência da premissa**.
- **FR4**: QUANDO um caso for aposentado, O SISTEMA DEVERÁ exigir o motivo e **imprimi-lo**
  — aposentadoria sem motivo é apagar, e aposentadoria silenciosa é esconder vermelho.
- **FR5**: QUANDO um achado for encontrado e corrigido no mesmo ciclo, O SISTEMA DEVERÁ
  oferecer uma forma de registro para isso.

## Fora de escopo

- **Remover a linha "check the declared lane" do `process-guardian.md`.** Há duas amostras
  apontando que ela é redundante; duas amostras não bastam para mexer num agente. Vira
  gatilho no roadmap.
- Escrever um terceiro caso de eval. O corpus fica com um caso provado.
- Fechar versão no `CHANGELOG` e a linha congelada do roadmap — são os achados pequenos
  levantados antes, e continuam fora desta retro.

## Critérios de aceite (DoD)

- [x] `retro.sh` decide gate pelo fato; zero gates pendentes falsos.
- [x] Três anti-padrões novos (19, 20, 21), cada um com o ciclo de origem.
- [x] `check-evals.sh` cobre FR2, FR3 e FR4, **visto acusar** nas três.
- [x] Caso 002 aposentado com motivo; corpus verde com 1 provado + 1 aposentado.
- [x] `docs/records/README.md` ganha a forma do FR5.
- [x] Os quatro achados fechados; dívida de retro em zero.

## Clarify

1. O portão de evals ficar verde depois de aposentar um caso não é maquiagem? **Não, e o
   mecanismo é desenhado contra isso**: a aposentadoria exige motivo, é impressa em toda
   execução e é contada separadamente (`retired: 1`). O verde diz "um caso provado, um
   aposentado", não "dois casos bons".
