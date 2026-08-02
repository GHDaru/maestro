# 05 — Padrões de orquestração de agentes

> **Capturado em** 2026-08 · última revisão 2026-08-02 · ciclo 025 (migrado ao padrão v2)
>
> **Fatiar é fácil; juntar de volta é o trabalho.** E o corte errado é pior que o
> *reduce* ruim — nenhuma reconciliação salva fatias cortadas fora da costura.

## 1. Objetivos

Ao fim deste capítulo você será capaz de:

1. **Explicar** por que o *map* paralelo não basta e o que é o *reduce* cognitivo;
2. **Escolher** entre fluxo fixo e agente autônomo pela regra da menor autonomia que
   resolve;
3. **Aplicar** os seis padrões de orquestração a um caso concreto, nomeando qual usar;
4. **Avaliar** quando paralelizar é ganho e quando é só custo de reconciliação.

## 2. O problema

Cinco subagentes recebem a mesma especificação e devolvem cinco fatias. Elas **não se
encaixam sozinhas**: uma renomeou o que a outra chama de outro jeito, duas implementaram
os dois lados do mesmo contrato com entendimentos diferentes, uma otimizou a sua parte
quebrando uma invariante do todo.

A tentação é resolver com mais paralelismo ("um agente para consolidar"). Mas quem
consolida precisa do contexto **global** — que é exatamente o que a paralelização tinha
distribuído. Sem alguém com a visão inteira, o resultado é média de opiniões, não decisão.

## 3. A ideia central

> **Map-reduce, mas cognitivo.** O *reduce* não é concatenação: é julgamento com contexto
> global — e por isso pertence a quem tem esse contexto, o orquestrador.

## 4. A regra vigente

1. **O padrão é o fluxo fixo** (encadeamento, roteamento, paralelização): barato,
   previsível, depurável.
2. **Paralelize por fronteira** (contexto delimitado, contrato, camada) — nunca por
   quantidade.
3. **O *reduce* é do orquestrador humano**, porque exige contexto global e responde pelo
   resultado.
4. **Menor autonomia que resolve**: suba para corte dinâmico só quando o corte
   genuinamente não puder ser predefinido.
5. **Agente autônomo aberto fica de fora** (Princípio VII, YAGNI): exige guarda-corpos que
   custam mais do que o problema que resolveriam aqui.

## 5. Fundamentos

### 5.1 O corte é mais traiçoeiro que o *reduce*

O *map-reduce* clássico pressupõe partes independentes. Em software elas quase nunca são:
porta e adaptador dividem um contrato; tela e serviço dividem um formato. Cortar ao longo
das **fronteiras arquiteturais** é o que torna a paralelização segura — cortar
transversalmente produz fatias que só se encaixam com retrabalho.

### 5.2 O espectro: fluxo ↔ agente

Num extremo, **você** fixa o caminho: previsível, focado, fácil de depurar. No outro, o
modelo decide o corte na hora: flexível, porém variável e sujeito ao ótimo local. A regra é
começar simples e só adicionar autonomia quando o simples **comprovadamente** falhar — não
quando parecer limitado.

### 5.3 Boa arquitetura empurra para o lado barato

Quanto melhores as fronteiras, mais trabalho cabe no lado previsível do espectro. Investir
em fronteira é comprar previsibilidade: o corte deixa de precisar de inteligência porque já
está desenhado.

### 5.4 Os seis padrões e onde cada um vive no método

| Padrão | O que é | Tipo | Onde vive |
|---|---|---|---|
| **Encadeamento** | passos fixos em sequência | fluxo | `specify → clarify → plan → tasks → implement` |
| **Roteamento** | classifica a entrada e escolhe o tratamento | fluxo | as **raias** (leve/plena/infra) |
| **Paralelização** | fatias independentes ou N tentativas | fluxo | subagentes por fronteira |
| **Orquestrador-trabalhadores** | corte dinâmico + *reduce* | agente | o papel do Orquestrador |
| **Avaliador-otimizador** | gera → critica → refina | fluxo com laço | escritor/revisor e o portão provado falhando |
| **Autônomo** | modelo aberto com guarda-corpos | agente | **evitado** (YAGNI) |

## 6. ⭐ Na prática — o ciclo real

Vinte e cinco ciclos operados, e o padrão dominante é o **mais barato do espectro**: o
encadeamento fixo. Ele não vive num diagrama — vive em onze comandos versionados:

```
$ ls .claude/commands/
dod.md  speckit.analyze.md  speckit.checklist.md  speckit.clarify.md
speckit.constitution.md  speckit.converge.md  speckit.implement.md
speckit.plan.md  speckit.specify.md  speckit.tasks.md  speckit.taskstoissues.md
```

Cada ciclo percorre a mesma sequência, e é por isso que começar um ciclo custa pouco:
ninguém decide *como* trabalhar, só *o que* fazer.

**Roteamento** é a raia — e o capítulo 03 já mostrou o quanto ela está sendo mal usada
aqui: 19 specs marcadas como plena contra 2 leves. Roteamento que manda quase tudo para o
mesmo tratamento não está roteando.

**Avaliador-otimizador** é o padrão que mais rendeu, e tem marca própria nos registros:
quatro relatórios de qualidade (QA) documentam portão **provado falhando** antes de ser
aceito — ciclos 017, 018, 020 e 021:

```
$ grep -rli "prova.* falhando" specs/*/qa-report.md
specs/017-retro-check-proxy/qa-report.md
specs/018-instalacao-e-ux-jornadas/qa-report.md
specs/020-bpmn-navegavel-no-livro/qa-report.md
specs/021-maestro-instalado-no-maestro/qa-report.md
```

O laço aqui não é "gerar e refinar texto": é **gerar o check → tentar refutá-lo → só então
confiar nele**. No ciclo 020 esse laço rodou quatro vezes dentro do mesmo ciclo, e cada
volta encontrou um formato de link que o portão ignorava.

**O que não aconteceu** informa tanto quanto o que aconteceu: em vinte e cinco ciclos, zero
uso do padrão autônomo, e a paralelização massiva de subagentes praticamente não apareceu —
o trabalho coube num encadeamento com verificação. É a regra da menor autonomia sendo
obedecida, e o custo evitado é real: cada agente a mais é um *handoff* a mais para
reconciliar.

## 7. Erros e anti-padrões

- **Multi-agente para problema de agente único** (anti-padrão 4) — orquestração cobra
  handoff, reconciliação e contexto duplicado.
- **Cortar por quantidade** — "metade dos arquivos para cada" garante fatias que não fecham.
- **Esperar que o *reduce* conserte o corte** — nenhuma reconciliação salva costura errada.
- **Autonomia como padrão** — flexibilidade que ninguém pediu, paga em variância e
  depuração.
- **Roteamento que não roteia** — uma raia só, na prática, é ausência de roteamento.

## 8. Verificação

1. Cinco fatias voltam inconsistentes entre si. Diga o que estruturalmente falhou — o
   *map*, o *reduce* ou o corte — e como distinguir os três.
2. Alguém propõe um agente autônomo para "descobrir sozinho o que refatorar". Aplique a
   regra da menor autonomia: que evidência você exigiria antes de aceitar?
3. Qual dos seis padrões descreve "escrever o check, prová-lo falhando e só então confiar"?
   Por que ele é fluxo com laço, e não agente?

## 9. O que roubar

- **Comece pelo fluxo fixo.** Autonomia é melhoria cara; exija prova de que o simples falha.
- **Corte na costura**: fronteira arquitetural, não quantidade de arquivos.
- **Deixe o *reduce* com quem tem o contexto global** — e assuma que ele é julgamento, não
  colagem.
- **Conte quantas vezes usou cada padrão.** Inventário grande com uso de um só ou é
  problema simples (ótimo) ou é régua não aplicada.

---

**Conexões**: [04 — contexto](04-fluxo-agentic-contexto.md) (o ótimo local que este
capítulo resolve) · [03 — Spec-Driven](03-spec-driven.md) (a spec como norte de cada
trabalhador; as raias como roteamento) · [06 — papéis e RACI](06-papeis-raci.md) (quem faz
o *reduce* e por quê) · [10 — gates e risco](10-gates-classes-de-risco.md) ·
[Diário da jornada](../research/jornada-aprendizado-modelo-operacional.md) `[4]`.

**Fontes**: Anthropic, *Building effective agents* (fluxo × agente; seis padrões; menor
autonomia) — https://www.anthropic.com/engineering/building-effective-agents ·
Claude Code, *Best practices* — https://code.claude.com/docs/en/best-practices ·
[Modelo operacional](../governance/modelo-operacional.md) §3–§4.
