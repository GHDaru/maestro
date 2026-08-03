# Receita — rodar a retrospectiva

> Objetivo: transformar erro recorrente em regra versionada. É a cerimônia de **maior
> retorno** do método — o processo aprende e você não repete a mesma correção.
> Tempo: ~15 min. Papel: Steward (humano); o script prepara o material.

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
