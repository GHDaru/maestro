# Comunicação intra-agentes — padrão (para avaliação)

> Como os agentes do Maestro "conversam". Trazido do FlowBuilder (`orientacoes_por_especialista.md`)
> e dos **handoffs** do Spec Kit, alinhado a `[7]` (artefatos) e `[11]` (rastreabilidade).

## Princípio: agentes comunicam por **artefatos**, não por chat

O meio da comunicação é o **artefato versionado**, não uma mensagem efêmera. Um agente
**produz** um artefato; o próximo **consome** aquele artefato. A conversa inteira fica
**rastreável** (`spec ↔ PR ↔ testes ↔ journey`) e sobrevive ao reset de contexto (`[3]`).

Isso é deliberado: mensagens de chat somem e não são auditáveis; artefatos são a **memória
durável** e o contrato claro entre papéis.

## O contrato Produz/Consome (o "quê" da comunicação)

```
Steward ──(intenção)──▶ Spec-agent ──(spec.md)──▶ Plan/Arquiteto ──(plan.md, ADR)──▶
  Dev ──(código+testes)──▶ QA ──(qa-report)──▶ Review(fresco) ──(veredito)──▶
    Security ──(achados)──▶ Steward (gate de merge) ──▶ Tech-Writer ──(docs/changelog)──▶ merge
```

- Curador/Pesquisa alimenta Spec/Plan com `research/*` (fontes citadas).
- O **Guardião de Processo** observa toda a cadeia e barra o que não conforma (Constitution Check).

## O bastão (o "como" — handoffs)

O Spec Kit já traz **handoffs** no frontmatter dos comandos: `/specify` declara o próximo
agente e o prompt de entrada (`handoffs: [{label, agent, prompt}]`). É a passagem explícita
do bastão. No Maestro, o **Orquestrador (humano)** é quem confirma cada handoff e faz o
*reduce* — nenhum agente "chama" outro sem passar pela orquestração (evita ótimo local, `[4]`).

## O que trouxemos do FlowBuilder

- **Mapa produz/consome por especialista** (era o "padrão de comunicação" real — contrato
  de artefatos por papel).
- **Cadeia de governança** ("quem manda em quê") — o Guardião de Processo herda isso.

## Para avaliarmos: dois níveis de formalidade

| | **A. Artefato + handoff (atual)** | **B. Envelope explícito** |
|---|---|---|
| Como passa | Produz/consome + handoff do spec-kit | Um "envelope" por handoff: `de · para · artefato · status · próximo passo` |
| Prós | Simples, rastreável, YAGNI; já temos | Coordenação rica quando há muitos agentes em paralelo |
| Contras | Coordenação fina fica no Orquestrador (humano) | Mais cerimônia; risco de burocracia |
| Quando | Ciclos normais (1 feature por vez) | Se/quando a orquestração paralela crescer |

**Recomendação**: começar em **A** (é o que o modelo já pressupõe e é YAGNI); introduzir o
**envelope (B)** só se a coordenação paralela justificar — e aí como um artefato próprio
(`specs/NNN/handoffs.md` ou um campo no PR), nunca como chat efêmero.

## Checkpoint por task (absorvido do Superpowers — ciclo 011)

Na **raia plena com >3 tasks**, o `dev-implementador` emite um **checkpoint leve** ao
fechar cada task — 3 linhas, sem cerimônia:

```
✔ T3 — <o que fechou>
evidência: <comando/teste e resultado>
próximo: T4 — <o quê>
```

Não é pedido de permissão (execução contínua segue; anti-"devo continuar?"); é rastro
para o Orquestrador auditar sem recarregar contexto — e ponto de corte natural se algo
desviou. O review independente por ciclo continua; o checkpoint não o substitui.

## Pergunta de avaliação

1. Ficamos no nível **A** (artefato + handoff) por ora?
2. Algum handoff da cadeia acima está errado/faltando para o seu jeito de trabalhar?
