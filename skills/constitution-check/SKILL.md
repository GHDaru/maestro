---
name: constitution-check
description: Produz a tabela Constitution Check (Princípios I–VII do Maestro) dentro de um plan.md, decide quando um princípio conta como violado e o que fazer com a violação. Use quando estiver escrevendo ou revisando um plan.md, abrindo um ciclo (spec-kit), ou sempre que precisar checar um plano contra os princípios inegociáveis do Maestro.
---

# Constitution Check

## Iron Law

```
NENHUM PLAN SEM AS 7 LINHAS — UMA POR PRINCÍPIO, NENHUMA VAZIA
```

**Violar a letra desta regra é violar o espírito dela.** Isso NÃO é desculpa:
- "Este princípio obviamente não se aplica" — então escreva ✅ com a frase do porquê; a linha fica.
- "O ciclo é pequeno" — ciclo pequeno com violação escondida vira dívida grande.

Todo `plan.md` do Maestro carrega uma tabela verificando o plano contra os **7 princípios
inegociáveis** (`docs/governance/principios-maestro.md`). Esta skill padroniza essa tabela —
o mesmo artefato que foi refeito à mão em ciclos anteriores.

## Quando disparar

Escrevendo/revisando um `plan.md`; no `/speckit.plan`; antes de liberar um plano para tasks.

## Passo a passo

1. Para **cada** princípio I–VII, escreva uma linha: `✅` (conforme) ou `⚠️/❌` (tensão/violação)
   + **uma frase** de porquê. Não pule princípio — a tabela é sempre completa.
2. Um princípio conta como **violado** quando o plano só funciona **quebrando-o** (ex.: um
   agente read-only precisaria de `Write`; uma decisão irreversível sem gate humano; um
   artefato de doc sem par vivo). Desconforto ≠ violação; impossibilidade-sem-quebrar = violação.
3. Violação real → **duas saídas, nunca ignorar**:
   - **Reformular** o plano para não violar (preferido); ou
   - Registrar em **Complexity Tracking**: qual princípio, por que é inevitável aqui, e o
     que a torna reversível/limitada. Vai para o gate humano decidir.
4. Feche com o veredito: **"Sem violações."** ou a lista do que foi para Complexity Tracking.

## Os 7 princípios (âncora)

| # | Princípio | Pergunta de checagem |
|---|---|---|
| I | Spec-Driven | Nasce de uma spec aprovada? |
| II | Orquestração humano-governada | O **A** (Accountable) humano é preservado? |
| III | Reversibilidade / gates de risco | Dá pra desfazer? Gate proporcional ao risco? |
| IV | Test-First / DoD verificável | O sucesso é verificável autonomamente? |
| V | Economia de contexto / fronteira | Cada fatia é estreita, cortada por fronteira? |
| VI | Artefatos vivos | Doc e código evoluem juntos (mesmo PR)? |
| VII | Governança leve / YAGNI | Só o necessário agora, sem regra especulativa? |

## Exemplo (do plan 003)

> III. Reversibilidade / gates de risco — ✅ **tools estreitas** = menor superfície de risco
> por agente (read-only onde cabe).

**Consumido por:** `plan-arquiteto` (produz), `guardiao-processo` (verifica).
