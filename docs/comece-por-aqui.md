# Comece por aqui

> Cinco minutos para entender o Maestro — a história antes das siglas. Se em algum ponto
> aparecer uma sigla que você não conhece, o [glossário](governance/glossary.md) tem todas.

## A dor

Dois jeitos de construir software hoje falham.

**Sem IA (Inteligência Artificial)**, um sistema legado exige dúzias de pessoas só para
*entender o que já existe*: ler código, reconstruir a intenção perdida, gerar documentação.
Lento, caro, e o conhecimento evapora com quem sai.

**Com IA, mas sem método**, acontece o oposto: o agente escreve código que compila e **erra
a intenção**; artefatos nascem e apodrecem; agentes trabalham sem contrapeso. Velocidade sem
governança vira risco.

Falta o **método no meio**.

## A jornada

O Maestro nasceu de uma pergunta simples, levada a sério: *se um agente escreve o código, o
que muda?* A resposta reorganiza tudo. Quando a máquina executa, o valor deixa de estar em
*digitar* e passa a estar em **duas coisas humanas**: deixar a intenção clara e verificar o
resultado.

Disso decorre o nome. Numa orquestra, o maestro não toca os instrumentos — ele **rege**. A
partitura (a *spec*, especificação) diz o que tocar; o compasso (os *gates*, portões de
controle) marca o ritmo; os músicos (os agentes) executam. **Um humano rege, muitos agentes
executam.**

## O sistema

O Maestro é esse método, organizado em **12 elementos, 5 camadas**:

| Camada | O que responde | Elementos |
|---|---|---|
| **Fundamento** | *Por quê* | Princípio central · evidência (DORA) |
| **Mecânica** | *Como o trabalho flui* | Spec-driven · fluxo agentic · orquestração |
| **Estrutura** | *Quem e quando* | Papéis (RACI) · cadência (Shape Up) |
| **Qualidade** | *O que se produz e como se prova* | Artefatos · DoD/DoR · gates de risco · rastreabilidade |
| **Governança** | *Como tudo evolui* | Constituição · ADRs · YAGNI |

Três ideias costuram o sistema inteiro — se você guardar só isto, já entendeu o Maestro:

1. **A spec é a fonte de verdade.** Não o código (que o agente refaz), não o prompt. A
   intenção vive na especificação.
2. **O humano responde pela política, não por cada item.** Ele define os trilhos (o que um
   agente pode fazer sozinho, o que precisa de aprovação) e deixa os agentes correrem
   dentro deles. É o que faz escalar sem virar gargalo.
3. **Reversibilidade compra velocidade.** O que torna seguro delegar não é aprovar tudo — é
   tornar as ações **reversíveis** (backup, dry-run, rollback). Assim erra-se barato, e
   erra-se barato deixa correr rápido.

## Como usar (o mapa de leitura)

1. **[Princípios](governance/principles.md)** — os inegociáveis (5 minutos). Comece aqui.
2. **[Modelo operacional](governance/operating-model.md)** — a regra vigente: papéis,
   cerimônias, artefatos, raias, gates. É o que você segue no dia a dia.
3. **[Handbook](handbook/README.md)** — o *porquê* de cada regra, um capítulo por elemento,
   com teoria e frameworks. Consulte quando quiser fundo.
4. **Praticando**: toda mudança nasce de uma spec (`/speckit.specify`), passa pelos gates
   (DoD, revisão, aprovação humana) e é rastreável (spec ↔ PR ↔ teste). Os templates
   (`.github/pull_request_template.md`, comando `/dod`) já estão prontos.

> Dúvida em qualquer sigla? → [glossário](governance/glossary.md).
