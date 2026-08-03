# 07 — Cerimônias e cadência: o que sobrevive quando o time é um

> **Capturado em** 2026-08 · última revisão 2026-08-02 · ciclo 027 (migrado ao padrão v2)
>
> **Cerimônia é função, não reunião.** E o limite de trabalho em curso não é a capacidade
> dos agentes — é a **atenção do humano**.

## 1. Objetivos

Ao fim deste capítulo você será capaz de:

1. **Decidir** quais cerimônias manter perguntando pela *função*, não pelo nome;
2. **Explicar** por que a retrospectiva é a cerimônia de maior retorno quando se trabalha
   com agentes — e por que só ela ganha valor;
3. **Aplicar** apetite (tempo fixo, escopo variável) no lugar de estimativa de prazo;
4. **Identificar** o gargalo real do trabalho em curso e o que fazer para escalar sem abrir
   frentes.

## 2. O problema

O repertório de cerimônias que herdamos foi desenhado para times: planejamento, reunião
diária, revisão, refinamento, retrospectiva. Cada um resolve um problema de **coordenação
entre pessoas**.

Quando o time é uma pessoa com N agentes, metade dessas funções deixa de existir — e
mantê-las por hábito produz o pior tipo de processo: aquele que consome tempo e não muda
decisão nenhuma. O erro simétrico também é caro: cortar tudo, inclusive o que ainda tem
função, e perder a única cerimônia que **melhora o sistema**.

## 3. A ideia central

> **Pergunte pela função, não pelo evento.** "Essa função ainda existe no meu contexto?" —
> se não existe, corte sem culpa; se existe, ela precisa acontecer, com ou sem reunião.

## 4. A regra vigente

1. **Cerimônias mínimas**: dar forma e especificar (o planejamento real), executar por
   apetite, checkpoint de ciclo, período de folga, **retrospectiva**.
2. **Cortadas**: reunião diária (não há entre quem sincronizar) e refinamento de backlog
   (não há backlog formal).
3. **Retrospectiva é obrigatória e tem saída obrigatória**: erro recorrente vira **regra
   versionada** — princípio, skill ou script. Retro sem regra não aconteceu.
4. **Apetite**: tempo fixo, escopo variável. Quando o tempo acaba, corta-se escopo — não se
   estende prazo.
5. **Trabalho em curso baixo**, medido em **decisões que o humano segura com qualidade**.
6. **Paralelize dentro** de uma feature já decidida; **não paralelize entre** features
   ambíguas — cada frente nova multiplica gates.
7. **Para escalar, barateie o gate** (Definição de Pronto verificável, reversibilidade), não
   abra mais frentes.

## 5. Fundamentos

### 5.1 Cerimônia por função

| Cerimônia | Função original | Com um humano + N agentes |
|---|---|---|
| Planejamento | comprometer escopo | vira **dar forma + spec** |
| Reunião diária | sincronizar entre pessoas | **função some** → cortada |
| Revisão | inspecionar incremento | vira **checkpoint de ciclo** |
| Refinamento | preparar backlog | **cortada** (sem backlog) |
| **Retrospectiva** | melhorar o processo | **amplificada** (abaixo) |

### 5.2 Por que a retrospectiva ganha valor com agentes

Num time humano, a melhoria que sai da retro é um hábito mole: depende de a pessoa lembrar
na próxima vez. Com agentes, ela vira **instrução versionada** — entra na constituição, numa
skill ou num script, e passa a ser aplicada **automaticamente** no ciclo seguinte, por quem
não estava lá.

É a diferença entre "combinamos de tomar cuidado" e "o comando falha se não tomarmos".

### 5.3 O gargalo é a atenção, não a capacidade

Cinco features sem dependência entre si ainda funilam pelos mesmos gates humanos: aprovar
spec, aprovar plano, aprovar merge. Abrir frentes multiplica gates e o humano vira a fila.
Paralelismo rende **dentro** da feature já decidida, onde não há gate a mais — e a forma de
escalar é tornar cada gate mais barato.

### 5.4 Cadências avaliadas

| Framework | O que traz | Veredito |
|---|---|---|
| **Scrum** | papéis e cinco eventos | **Parcial** — sobrevivem a função do planejamento (vira spec) e a retrospectiva; o resto é cerimônia de papel para quem opera sozinho |
| **Kanban** | fluxo contínuo, limite de trabalho em curso | **Adotado** — o limite é a atenção humana |
| **Shape Up** | apetite, ciclo com folga, sem backlog | **Adotado (esqueleto)** |
| **Scrumban** | híbrido | **Observado** — carrega o overhead de Scrum que não precisamos |

## 6. ⭐ Na prática — o ciclo real

**A retrospectiva rendeu regra, e a regra tem data.** O catálogo de anti-padrões tem hoje
dezesseis itens, e o arquivo mostra quando cada leva entrou:

```
$ git log --format="%ad %s" --date=short -- skills/anti-patterns/SKILL.md
2026-08-02  BPMN navegável … (spec 020)      → anti-padrão 16
2026-08-01  retro executada — anti-padrões 13/14/15, segunda lei (spec 017)
2026-07-31  absorções do Superpowers — Iron Laws, causa raiz (spec 011)
2026-07-31  incorpora as sugestões do estudo maestro-02 (spec 008)
```

Repare no anti-padrão **14** — "achado que morre em candidato" — e no motivo dele existir:
duas vezes escrevemos "candidato a anti-padrão" num relatório e **não rodamos a retro**. A
cerimônia que estava faltando virou item de catálogo na primeira vez que foi executada.

**A retro tem script, e o script não decide nada.** `scripts/retro.sh` pré-computa o
material (ciclos, vereditos, gates pendentes, decisões, inventário) e é somente-leitura por
declaração no cabeçalho:

> Read-only: nunca escreve nada. A retro em si continua sendo cerimônia humana; este script
> só elimina o "recarregar contexto de cabeça".

**Trabalho em curso: um.** Vinte e seis ciclos, duas branches no repositório inteiro:

```
$ git branch -a
* dev
  main
```

Nenhuma frente paralela foi aberta em nenhum momento — não por virtude, mas porque cada
frente nova multiplicaria os gates que dependem da mesma pessoa. O que foi paralelizado
ficou **dentro** do ciclo (subagentes por fronteira), exatamente onde não há gate a mais.

**Apetite na prática**: cada ciclo entra na linha principal em um único commit, no mesmo
dia em que abre. Quando o escopo não coube, ele foi cortado e virou o ciclo seguinte — a
migração dos capítulos é o exemplo mais visível: um capítulo por ciclo, treze ciclos em
vez de um "mutirão de documentação" que nunca termina.

## 7. Erros e anti-padrões

- **Cerimônia de papel** (anti-padrão 11) — manter o evento porque tem nome conhecido,
  mesmo sem a função.
- **Achado que morre em "candidato"** (anti-padrão 14) — anotar a melhoria e não executar a
  retro. A regra só existe se for versionada.
- **Estimar prazo em vez de fixar apetite** — o escopo é a variável; o tempo, não.
- **Abrir frentes para "aproveitar" a capacidade dos agentes** — multiplica gates no mesmo
  gargalo.
- **Retro sem saída executável** — conversa boa que não muda o próximo ciclo.

## 8. Verificação

1. Você opera sozinho com agentes e quer manter uma reunião diária. Que **função** ela
   cumpriria? Se não conseguir nomear uma, o que isso significa?
2. Explique por que abrir três features em paralelo **não** triplica a vazão quando o
   humano é o responsável final por spec, plano e merge.
3. Sua retro identificou um erro recorrente. O que precisa acontecer para ela ter dado
   resultado — e como você prova isso daqui a dois ciclos?

## 9. O que roubar

- **Corte por função, não por moda**: nomeie a função de cada cerimônia; sem função, sem
  cerimônia.
- **Faça a retro escrever regra** — princípio, skill ou script. Documento de retro que fica
  em ata é ata.
- **Meça o trabalho em curso em decisões humanas**, não em tarefas abertas.
- **Barateie o gate para escalar.** Mais frentes contra o mesmo gargalo é fila, não vazão.

---

**Conexões**: [06 — papéis e RACI](06-papeis-raci.md) (o responsável final é o gargalo) ·
[05 — orquestração](05-orquestracao.md) (paralelizar dentro da feature) ·
[03 — Spec-Driven](03-spec-driven.md) (apetite e escopo variável = raia certa) ·
[09 — DoR/DoD](09-definition-of-ready-done.md) (gate barato é o que permite escalar) ·
[Receita — rodar a retro](../receitas/rodar-a-retro.md) ·
[Diário da jornada](../research/jornada-aprendizado-modelo-operacional.md) `[6]`.

**Fontes**: Basecamp, *Shape Up* (apetite, ciclo, folga) — https://basecamp.com/shapeup ·
DORA, *four keys* — https://dora.dev/guides/dora-metrics-four-keys/ ·
[Modelo operacional](../governance/operating-model.md) §5 ·
[Skill `anti-patterns`](https://github.com/GHDaru/maestro/blob/main/skills/anti-patterns/SKILL.md).
