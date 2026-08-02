# 02 — A evidência: velocidade e estabilidade andam juntas

> **Capturado em** 2026-08 · última revisão 2026-08-02 · ciclo 022 (migrado ao padrão v2)
>
> **Não existe o trade-off "rápido ou estável".** Os mesmos times são as duas coisas — e a
> alavanca que produz as duas é a mesma: **lote pequeno**.

## 1. Objetivos

Ao fim deste capítulo você será capaz de:

1. **Explicar** por que velocidade e estabilidade se movem juntas em vez de se oporem;
2. **Distinguir** *outcome* (o que a métrica mede) de *capacidade* (o que o produz) — e
   dizer por que só a segunda é acionável;
3. **Aplicar** as quatro métricas do DORA a um fluxo de uma pessoa com N agentes, sem
   instrumentar painel nenhum;
4. **Avaliar** quando uma métrica vira alvo gameável, e o que fazer nesse caso.

## 2. O problema

A intuição diz: *"quanto mais rápido eu entrego, mais eu quebro"*. Dela nasce a burocracia
defensiva — comitê de mudança, janela de deploy mensal, aprovação em três instâncias.

Com agentes de Inteligência Artificial (IA), a intuição fica ainda mais tentadora: o
agente produz muito, logo é preciso freá-lo. Se a intuição estiver certa, todo método
humano+IA deveria ser um freio. Se estiver errada, freio é desperdício — e a pergunta vira
outra: **o que faz uma mudança ser rápida *e* segura ao mesmo tempo?**

## 3. A ideia central

> **O trade-off real não é entre rápido e estável — é entre *software melhor mais rápido*
> e *software pior mais devagar*.** O que separa os dois é o tamanho do lote.

## 4. A regra vigente

1. **DORA é bússola, não painel.** A pergunta operacional é "levo uma spec ao ar rápido e
   sem quebrar?" — não "qual foi meu número esta semana".
2. **Lote pequeno é regra, não estilo**: diff pequeno, uma fronteira por vez, um ciclo por
   entrega (modelo operacional §3, raias).
3. **Reversibilidade antes de velocidade** (Princípio III): o que torna a falha barata é o
   que autoriza acelerar.
4. **Não instrumentar métricas agora** (Princípio VII, YAGNI): sem base de comparação, o
   painel é débito. As **capacidades** — integração contínua verde, testes, revisão
   independente, diffs pequenos — já são exigidas pela Definição de Pronto (DoD).

## 5. Fundamentos

### 5.1 As quatro métricas, em dois pares

O programa DORA (*DevOps Research and Assessment*) mediu milhares de equipes e chegou a
quatro medidas, que só fazem sentido **aos pares**:

| Par | Métrica | Pergunta |
|---|---|---|
| Throughput | frequência de entrega | com que frequência a mudança chega ao destino? |
| Throughput | *lead time* | quanto tempo entre escrever e estar no ar? |
| Estabilidade | *change fail rate* | que fração das entregas quebra algo? |
| Estabilidade | tempo de recuperação | quanto demora para voltar ao normal? |

Medir só um par é o erro clássico: throughput sozinho premia atropelo; estabilidade
sozinha premia paralisia. **É o par que informa.**

### 5.2 *Outcome* não é acionável; capacidade é

As quatro são **resultados**. Ninguém "faz" lead time — ele cai quando se muda o que o
produz: integração contínua, desenvolvimento em tronco único, testes automatizados,
revisão de código, deploys pequenos. Cobrar o resultado sem mexer na capacidade é cobrar
o termômetro pela febre.

### 5.3 A alavanca única: tamanho de lote

Mudança pequena chega mais vezes (frequência ↑), atravessa mais rápido (lead time ↓), é
fácil de testar e revisar (falha ↓) e, quando falha, é fácil de reverter (recuperação ↑).
Uma alavanca, quatro métricas — é por isso que elas se movem juntas em vez de brigar.

A analogia que usamos no diário da jornada é a **linha de produção cognitiva**: a fábrica
pré-Ford era lenta porque cada peça era única; padronizar componentes barateou o fluxo.
Com uma diferença decisiva a nosso favor: **a linha do Ford não tinha desfazer barato; a
cognitiva tem.** Lote pequeno + reversibilidade = rápido *e* estável.

### 5.4 Frameworks avaliados

| Framework | Foco | Veredito para 1 humano + N agentes |
|---|---|---|
| **DORA** (4 métricas + capacidades) | Desempenho de entrega e o que o causa | **Adotado como bússola qualitativa** — lead time e change fail rate são os que mais importam a quem opera sozinho |
| **SPACE** (Satisfação, Performance, Atividade, Comunicação, Eficiência) | Produtividade multidimensional | **Referência** — lembra que não existe métrica única; prescreve pouco |
| **DX Core 4** (Speed, Effectiveness, Quality, Impact) | Quatro métricas prescritivas | **Observado** — cuidado com o gameável ("PRs por pessoa" mede digitação, não valor) |
| **Painel instrumentado de DORA** | Dashboards | **YAGNI agora** — sem a quem comparar, instrumentar é débito prematuro |

## 6. ⭐ Na prática — o ciclo real

Nós não instrumentamos nada. Mesmo assim as quatro métricas são legíveis no repositório,
porque o método deixa rastro — e o retrato é honesto, inclusive na parte ruim.

**Frequência de entrega.** O índice de decisões (`docs/registro/decisoes.jsonl`) registra
cada promoção para a linha principal, porque o `promover-main.sh` grava o gate sozinho:

```
$ grep -c '"id": "gate-main' docs/registro/decisoes.jsonl
17
```

Dezessete promoções em **três dias** de operação (31/07: 4 · 01/08: 9 · 02/08: 4). Não é
mérito de velocidade individual: é consequência de a unidade de trabalho ser um ciclo
pequeno com gate próprio.

**Lead time.** Cada ciclo entra na linha principal em **um único commit**, no mesmo dia em
que abre. Do `novo-ciclo.sh` ao `promover-main.sh`, as horas do ciclo 021 desta página
cabem numa sessão de trabalho — e o que o encurta não é pressa, é escopo: uma spec, uma
fronteira, um gate.

**Change fail rate — a nossa métrica pior.** O `CHANGELOG.md` lista, em `Fixed`, **nove
defeitos** que escaparam para a linha principal e só apareceram ciclos depois: a imagem do
BPMN que nunca era publicada, o widget ilegível no tema claro, a colisão de cinco páginas
no mesmo endereço, o template de plano parado em I–VII, a instrução da IA derivada em três
pontos. Com 17 promoções, é grosseiramente **um defeito escapado a cada duas entregas.**

E o padrão é o mesmo nos nove: **nenhum foi pego por revisão — todos foram pegos quando
alguém escreveu um check.** Foi assim que a imagem quebrada apareceu (portão de `<img
src>`, ciclo 020) e assim que a skill invisível apareceu (`verificar-instalacao.sh`, ciclo
021, que nasceu vermelho com deriva de três ciclos).

**Tempo de recuperação.** Zero reversões no histórico (`git log --grep=revert` → nenhuma).
Todo defeito foi corrigido avançando, no ciclo seguinte, porque cada um era pequeno o
bastante para caber num commit — a reversibilidade estava lá, não precisou ser usada.

**A leitura DORA deste retrato**: throughput de elite, estabilidade medíocre. A resposta
certa **não** é entregar mais devagar — é atacar a capacidade que falta. No nosso caso ela
tem nome: *fitness function* onde hoje há só leitura atenta. Foi o que os ciclos 020 e 021
fizeram, e é por isso que a segunda lei da skill `dod-verificavel` existe:

```
UM CHECK QUE VOCÊ NUNCA VIU ACUSAR NÃO É UM CHECK — É UMA ESPERANÇA
```

## 7. Erros e anti-padrões

- **Métrica virando meta** (Goodhart): "PRs por semana" produz PRs, não valor. Se a
  métrica vira alvo, ela para de medir.
- **Medir um par só** — throughput sem estabilidade é atropelo com relatório bonito.
- **Instrumentar antes de precisar** — painel sem decisão associada é cerimônia de papel
  (anti-padrão 11 do catálogo).
- **Confundir *outcome* com capacidade** — cobrar lead time sem mexer em lote, testes e
  revisão é cobrar o termômetro.
- **Ler a estabilidade como convite a frear** — o freio piora as quatro; lote menor melhora
  as quatro.

## 8. Verificação

1. Uma equipe entrega uma vez por mês e mesmo assim quebra a produção em metade das
   entregas. Explique, com o argumento do lote, por que entregar **menos** vezes não vai
   consertar a estabilidade.
2. Nosso *change fail rate* é ruim (nove defeitos escapados em dezessete entregas). Cite
   duas **capacidades** que atacam essa métrica e diga por que "revisar com mais atenção"
   não é uma delas.
3. Por que decidimos **não** instrumentar um painel de DORA — e que fato mudaria essa
   decisão?

## 9. O que roubar

- **Leia as quatro aos pares.** Uma métrica de velocidade sozinha é como pedir para o time
  correr sem dizer para onde.
- **Encolha o lote antes de qualquer outra intervenção** — é a única alavanca que melhora
  as quatro ao mesmo tempo.
- **Ataque a capacidade, não o número.** Se a estabilidade está ruim, a pergunta é "que
  check não existe?", não "quem foi menos cuidadoso?".
- **Você pode ler DORA sem painel**: se o método deixa rastro (registro de gates, changelog
  honesto, histórico), as quatro métricas já estão no repositório.

---

**Conexões**: [01 — o princípio central](01-principio-central.md) (reversibilidade como
alavanca) · [04 — contexto e fluxo agentic](04-fluxo-agentic-contexto.md) (rollback rápido
= checkpoint/rewind) · [09 — Definition of Ready / Done](09-definition-of-ready-done.md)
(as capacidades DORA são os itens da DoD) ·
[Diário da jornada](../research/jornada-aprendizado-modelo-operacional.md) `[10]`.

**Fontes**: DORA, *DORA metrics (four keys)* —
https://dora.dev/guides/dora-metrics-four-keys/ ·
Swarmia, *Comparing DORA, SPACE and DX Core 4* —
https://www.swarmia.com/blog/comparing-developer-productivity-frameworks/ ·
N. Forsgren, J. Humble, G. Kim, *Accelerate* (2018) ·
[Princípios do Maestro](../governance/principios-maestro.md) (III — reversibilidade;
VII — governança leve).
