# 12 — Governança leve: aprender sem inchar

> **Capturado em** 2026-08 · última revisão 2026-08-02 · ciclo 032 (migrado ao padrão v2)
>
> **Um sistema de regras que só cresce vira o processo pesado que você cortou no começo.**
> Governança precisa de duas forças opostas: aprender e podar.

## 1. Objetivos

Ao fim deste capítulo você será capaz de:

1. **Nomear** o modo de falha de um corpo de regras que só acumula;
2. **Aplicar** a arquitetura de camadas com velocidades diferentes — núcleo firme, periferia
   evoluível, memória imutável;
3. **Podar** uma regra que não paga o próprio custo, com critério e registro;
4. **Avaliar** se uma governança aplica a si mesma os princípios que exige dos outros.

## 2. O problema

Toda regra nasce de uma dor real, e por isso cada uma parece justificada. O corpo de regras
cresce um item por incidente — e ninguém nunca remove, porque remover exige argumentar
contra uma dor que existiu.

O resultado previsível: o método vira o inverso do que prometia. O leitor novo desiste no
terceiro documento, o operador experiente ignora metade, e a governança passa a existir
para se manter, não para melhorar o trabalho. É o ponto em que "processo" vira palavrão.

## 3. A ideia central

> **Duas forças em equilíbrio: aprender e podar.** A retrospectiva adiciona regra; a
> regra que não paga o próprio custo sai — e a saída também fica registrada.

## 4. A regra vigente

1. **Núcleo firme, periferia rápida**: a constituição muda por emenda versionada; o modelo
   operacional e o livro mudam com versão própria, subordinados a ela.
2. **Memória imutável**: toda decisão que muda o sistema vira registro (ADR), superável por
   outro, nunca reescrito no mérito.
3. **Emenda pela retrospectiva**: erro recorrente vira regra versionada — princípio, skill
   ou script.
4. **Poda por YAGNI**: complexidade além do necessário **deve ser justificada por escrito
   ou removida**.
5. **O que não se adota também se escreve** — a lista do que foi recusado evita a
   reabertura infinita da mesma discussão.
6. **A governança se aplica a si mesma**: versionada, aprovada em gate humano, registrada e
   podada.

## 5. Fundamentos

### 5.1 O modo de falha: acúmulo e ossificação

Regras acumulam porque adicionar é barato e remover é politicamente caro. Sem uma força
contrária explícita, o conjunto endurece: ninguém sabe mais quais regras estão vivas, e a
resposta racional de quem opera é ignorar tudo o que não for cobrado.

### 5.2 Camadas com velocidades diferentes

| Camada | Muda | Como |
|---|---|---|
| **Constituição** (princípios) | devagar | emenda versionada, com relatório de impacto |
| **Modelo operacional e livro** | rápido | versão própria, subordinada à constituição |
| **Registros de decisão** | nunca | imutáveis; um novo pode superar o anterior |
| **Skills e scripts** | conforme a dor | nascem de retrospectiva, com lei própria |

A separação é o que permite evoluir sem instabilidade: quem muda toda semana não é o mesmo
documento que sustenta as decisões de meses.

### 5.3 Registro imutável dá reversibilidade à decisão

Um registro que pode ser superado — mas não reescrito — mantém duas coisas ao mesmo tempo:
a liberdade de mudar de ideia e a memória de por que se pensava diferente. É a
reversibilidade do capítulo 01 aplicada à governança.

### 5.4 Abordagens avaliadas

| Abordagem | O que oferece | Veredito |
|---|---|---|
| **Constituição versionada** | fonte de verdade com emenda disciplinada | **Adotado** — núcleo firme |
| **Registro de decisão imutável** | memória com racional e alternativas | **Adotado** |
| **Acordos de trabalho evoluíveis** | convenções que mudam rápido | **Adotado** — modelo e livro |
| **Processo de RFC pesado** | revisão formal ampla | **Rejeitado** — o registro de decisão cobre |
| **"Adicionar sempre"** | mais regra = mais controle | **Rejeitado** — leva ao acúmulo |

## 6. ⭐ Na prática — o ciclo real

**As duas forças são visíveis no histórico.** A constituição foi tocada **três vezes** em
trinta e dois ciclos:

```
$ git log --format="%ad %s" --date=short -- docs/governance/principios-maestro.md
2026-08-01  Princípio VIII — comunicação inteligível (ADR 0010)
2026-07-28  camada didática de governança
2026-07-27  fundação do repositório
```

Enquanto isso, a periferia executável cresceu bem mais rápido: seis skills, dez scripts,
dez registros de decisão. **É o desenho funcionando** — o que muda toda semana não é o que
sustenta o resto.

**A emenda vem da retrospectiva, e a retrospectiva vem de erro repetido.** O princípio
VIII nasceu de um pedido do Steward, mas os anti-padrões 13 a 16 nasceram de reincidência
nossa — cada um com o ciclo de origem no arquivo. Aprender aqui não é adicionar o que
parece bom: é adicionar o que já custou caro.

**A poda também está escrita.** O modelo operacional tem uma seção inteira dedicada ao que
**não** adotamos, com motivo:

> **Scrum completo** — cerimônia de papel para quem opera sozinho · **Backlog formal** —
> ideias importantes voltam · **Segunda ferramenta de spec-driven** — avaliada e descartada
> · **Processo de RFC pesado** — o registro de decisão já cobre · **Instrumentação de
> métricas** — reavaliar quando a escala justificar · **Estimativas de prazo** — usamos
> apetite.

Três dos dez registros de decisão existem justamente para **descartar** alguma coisa. Num
método que só acumulasse, esses três não existiriam.

**E a governança se aplica a si mesma — inclusive quando dói.** No ciclo 021, a auto-
instalação mostrou que a constituição tinha oito princípios e o Constitution Check dos
planos só checava sete: a norma tinha evoluído e o executável que a cobra, não. A correção
não foi editar o texto do template e seguir; foi criar a verificação que compara os dois
lados e falha quando divergem. Governança que confia em si mesma é governança que
apodrece.

**O limite honesto**: a retrospectiva ainda não tem gatilho (achado do ciclo 027) e a
distribuição de raias mostra a régua mal aplicada (achado do ciclo 023). As duas forças
existem; o que ainda falta é o relógio que dispara a primeira.

## 7. Erros e anti-padrões

- **Governança que só adiciona** — acúmulo até a ossificação.
- **Regra sem forcing function** — norma que depende de memória, e memória é o que falha
  primeiro.
- **Editar decisão no mérito** — apaga a memória; o certo é superar com registro novo.
- **Artefato de planejamento que congela** (anti-padrão 15) — mapa que descreve um projeto
  que não é mais o seu.
- **Poda sem registro** — remover regra sem dizer por quê reabre a mesma discussão adiante.

## 8. Verificação

1. Seu método ganhou catorze regras em seis meses e nenhuma saiu. Que pergunta você faz a
   cada uma para decidir a poda — e onde registra o resultado?
2. Por que a constituição e o livro precisam de velocidades diferentes? O que quebra se os
   dois mudarem no mesmo ritmo?
3. A constituição ganhou um princípio novo. Que verificação garante que ele passa a ser
   realmente cobrado — e por que a boa vontade não basta?

## 9. O que roubar

- **Separe o que muda devagar do que muda rápido** — e escreva a subordinação entre eles.
- **Registre a decisão de forma imutável e superável**: liberdade de mudar sem perder a
  memória.
- **Escreva o que você recusou.** A lista do "não adotamos" economiza mais discussão do que
  qualquer regra nova.
- **Faça a governança se auditar**: se a norma cresceu, algum executável tem que ter
  crescido junto — e um script deve provar isso.

---

**Conexões**: [01 — o princípio central](01-principio-central.md) (reversibilidade aplicada
à decisão) · [07 — cerimônias](07-cerimonias-cadencia.md) (a retrospectiva é o motor de
emenda) · [08 — artefatos](08-entregaveis-artefatos.md) (o registro imutável) ·
[10 — gates](10-gates-classes-de-risco.md) (a emenda passa por gate humano) ·
[13 — decisões de engenharia](13-decisoes-de-engenharia.md) ·
[Diário da jornada](../research/jornada-aprendizado-modelo-operacional.md) `[12]`.

**Fontes**: M. Nygard, *Documenting Architecture Decisions* —
https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions ·
GitHub Spec Kit (constituição versionada) — https://github.com/github/spec-kit ·
[Princípios do Maestro](../governance/principios-maestro.md) ·
[Modelo operacional](../governance/modelo-operacional.md) §10–§11 ·
[Registros de decisão](../adr/README.md).
