# A Jornada — como o método foi construído

> Trilha **tutorial** (Diátaxis): a sequência de conhecimento. Aqui o método não é
> *apresentado* — é **reconstruído**, na ordem em que foi descoberto, com a pergunta que
> gerou cada regra. Se você seguir as paradas, entende não só o *que* o Maestro faz, mas
> por que não poderia ser diferente.
>
> **Como ler**: cada parada tem uma **tensão** (o que estava errado), a **pergunta** que a
> destravou e a **regra** que nasceu. Leia a pergunta e tente responder antes de continuar
> — foi assim que o método nasceu de verdade.

## O mapa em cinco camadas

```
FUNDAMENTO   Por quê          → [1] princípio central · [10] evidência (DORA)
MECÂNICA     Como flui        → [2] spec-driven · [3] contexto · [4] orquestração
ESTRUTURA    Quem e quando    → [5] papéis (RACI) · [6] cerimônias (apetite)
QUALIDADE    Como se prova    → [7] artefatos · [8] pronto · [9] gates · [11] rastro
GOVERNANÇA   Como evolui      → [12] governança leve (constituição · ADR · YAGNI)
```

## As paradas

| # | Parada | A tensão | A pergunta que destravou | A regra que nasceu |
|---|---|---|---|---|
| 1 | **Princípio central** | "O humano decide" parece dogma | *E se toda decisão puder ser automatizada — desde que auditável?* | O que importa não é **quem** decide, mas o **registro** (alternativas + racional) → o ADR |
| 2 | **Delegação** | Delegar parece perder controle | *O humano pode delegar — e isso vai para o registro?* | Delega-se R/C/I; o **A (Accountable)** nunca. A delegação é declarada, não presumida |
| 3 | **Risco** | Aprovar tudo vira gargalo | *Quanto custa desfazer?* | **Reversibilidade compra velocidade**; gate proporcional ao risco, não uniforme |
| 4 | **Spec-Driven** | Documentação apodrece | *E se a spec fosse o input que gera o código?* | A spec é fonte de verdade — não descrição, mas insumo |
| 5 | **Raias** | Spec para um typo é papel | *E quando a mudança é simples?* | `ambiguidade × raio × irreversibilidade` → leve / plena / infra |
| 6 | **Contexto** | O agente "esquece" | *O problema é falta de contexto ou falta de foco?* | **Economia de contexto**: carregar só o papel; resetar quando o papel muda |
| 7 | **Ótimo local** | Delegar demais degrada | *O agente resolveu a task — mas atendeu a jornada?* | Verde local ≠ certo global — o julgamento do todo é humano |
| 8 | **Papéis** | Papéis clássicos não cabem em um solo | *Quem verifica, se sou eu que executo?* | Verificação vai para **agente independente em contexto fresco** |
| 9 | **Gargalo** | A IA acelera, e aí? | *O que passa a ser escasso?* | A **atenção humana** — logo, poucos gates, nos pontos irreversíveis |
| 10 | **Pronto** | "Pronto" é opinião | *Como um agente confirma sem opinar?* | DoD **verificável autonomamente**: todo critério tem comando que o prova |
| 11 | **Rastro** | Por que isso foi feito assim? | *O que sobrevive ao reset do agente?* | `spec ↔ PR ↔ teste ↔ jornada` — a memória durável |
| 12 | **Governança** | Processo incha e ossifica | *Como aprender sem virar burocracia?* | **Retro → regra versionada** + YAGNI podando o que não paga |

## O que a jornada provou

Três coisas que só aparecem quando se percorre a construção, não o resultado:

1. **Cada regra nasceu de uma dor, não de um framework.** As raias existem porque o
   spec-driven cobrou um preço (parada 5 resolvendo o custo da parada 4). Nenhuma regra
   foi adotada por prestígio.
2. **O método se aplicou a si mesmo.** A retrospectiva executável, ao rodar pela primeira
   vez, encontrou uma falha real do próprio processo — que virou regra e depois automação,
   em dois ciclos. Está documentado no [capítulo 13 §6](../handbook/13-decisoes-de-engenharia.md).
3. **O preço está escrito.** Toda decisão registra o que **provoca** de indesejado — é o
   que a torna revogável depois.

## Continue

- Quer o material cru, elemento a elemento? → [Diário da jornada](../research/jornada-aprendizado-modelo-operacional.md)
- Quer a história curta? → [Comece por aqui](../comece-por-aqui.md)
- Quer executar? → [Receitas](../receitas/README.md)
- Quer o fundo teórico? → [Capítulos](../handbook/README.md)

> **Nota de livro vivo** (capturado em 2026-08): esta trilha é o **mapa** da jornada. A
> versão longa — cada parada como diálogo navegável, com o companion respondendo dúvidas —
> é o próximo ciclo do livro.
