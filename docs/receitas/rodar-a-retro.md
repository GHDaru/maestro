# Receita — rodar a retrospectiva

> Objetivo: transformar erro recorrente em regra versionada. É a cerimônia de **maior
> retorno** do método — o processo aprende e você não repete a mesma correção.
> Tempo: ~15 min. Papel: Steward (humano); o script prepara o material.

## 0. Quando rodar — o gatilho é dívida, não calendário

A retrospectiva não tem data marcada: ela é cobrada pela **dívida de achados abertos**
(ciclo 034). Todo achado que não coube no ciclo entra no índice de decisões como
`achado-NNN-<slug>` com status `aberta`:

```bash
scripts/record-decision.sh '{"id":"achado-035-nome","data":"2026-08-03","titulo":"...","status":"aberta","registro":"specs/035-*/qa-report.md","ciclo":"035"}'
scripts/check-retro.sh    # falha com ≥4 abertos, ou com um aberto há ≥6 ciclos
```

Cerimônia com data marcada vira teatro; cerimônia cobrada por dívida acontece quando é
necessária. Foi assim que este gatilho nasceu: a retro era a cerimônia de maior retorno do
método e **não tinha relógio** — acontecia quando alguém percebia (anti-padrão 17).

## 1. Pré-compute o material (o script faz)

```bash
scripts/retro.sh
```

Ele **não decide nada** — só reúne: ciclos e vereditos, gates pendentes cruzados com o
registro, últimas decisões, inventário do toolkit e as três perguntas abaixo.

## 2. Responda as três perguntas

| Pergunta | Se a resposta for "sim" |
|---|---|
| **1.** Que erro/correção se **repetiu**? | Vira **regra versionada** — nunca corrija a mesma coisa duas vezes |
| **2.** Que regra existente **não pagou** o custo? | **Pode** (YAGNI — *You Aren't Gonna Need It*, "você não vai precisar disso") |
| **3.** Que passo manual se repetiu **idêntico**? | Candidato a **script ou skill** |

## 2b. Feche os achados no índice

Achado fechado não se edita — ganha **linha nova** (o índice é append-only):

```bash
scripts/record-decision.sh '{"id":"achado-035-nome-fechado","data":"...","titulo":"Fechado por <regra>","status":"fechada por retro-036","registro":"specs/036-*/qa-report.md","ciclo":"036"}'
```

## 3. Escolha o destino da regra nova

| Natureza | Vai para |
|---|---|
| Inegociável, vale para todo o método | **Princípio** (constituição, sobe versão + ADR) |
| Regra do dia a dia | **Modelo operacional** (sobe versão) |
| Procedimento recorrente | **Skill** (`skills/`, com Iron Law e baseline testado) |
| Passo mecânico repetido | **Script** (`scripts/`) |
| Decisão pontual com alternativas | **ADR** (Registro de Decisão de Arquitetura) |

## 4. Registre

```bash
scripts/record-decision.sh '{"id":"adr-00NN","data":"AAAA-MM-DD","titulo":"...","status":"aceita","registro":"docs/adr/00NN-....md"}'
```

## Exemplo real (ciclo 008 → 009)

O primeiro `retro.sh` mostrou que relatórios de ciclos já promovidos ainda diziam "aguarda
aprovação" — o gate acontecera na conversa, sem artefato. Pergunta 1 disparou → virou o
**ADR 0009** → virou **automação** no `promote-main.sh`. Ferramenta achou a falha, falha
virou regra, regra virou código. Em dois ciclos.

## Pronto quando

- [ ] As três perguntas respondidas
- [ ] Toda resposta "sim" tem destino escolhido **e** artefato criado
- [ ] Decisão registrada no índice consultável

**Por quê?** → [Capítulo 07 — cerimônias](../handbook/07-cerimonias-cadencia.md) ·
[Capítulo 12 — governança leve](../handbook/12-governanca-leve.md)
