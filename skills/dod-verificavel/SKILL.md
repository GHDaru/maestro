---
name: dod-verificavel
description: Transforma critérios de aceite vagos em fitness functions executáveis (grep/ls/teste) que uma máquina consegue verificar sem julgamento humano. Use quando estiver escrevendo os critérios de aceite (DoD) de uma spec.md ou plan.md, ou quando um critério estiver subjetivo ("funciona bem", "está claro") e precisar virar um check objetivo. Complementa o comando /dod, que roda os checks — esta skill ajuda a escrevê-los.
---

# DoD verificável (design-time)

## Iron Law

```
NENHUM CRITÉRIO DE ACEITE SEM O COMANDO QUE O PROVA
```

**Violar a letra desta regra é violar o espírito dela.** Isso NÃO é desculpa:
- "É difícil de automatizar" — então marque explicitamente como gate humano; vago não fica.
- "Todo mundo entende o que significa" — se não há comando, cada um entende uma coisa.

O Princípio IV exige DoD **verificável autonomamente**: um agente confirma sem opinar. Esta
skill transforma critério vago em check executável — o que foi feito à mão, igual, em vários
ciclos.

> **Divisão de trabalho:** esta skill é *design-time* (escrever os checks, ao redigir
> spec/plan). O comando **`/dod`** é *run-time* (executar os checks antes de dar por pronto).
> Uma escreve, o outro roda — não se sobrepõem.

## Quando disparar

Escrevendo critérios de aceite em `spec.md`/`plan.md`; um critério está subjetivo e precisa
virar objetivo.

## Passo a passo

1. Pegue cada critério e pergunte: **"que comando prova isto com saída vazia/não-vazia ou
   exit code?"** Se não dá pra responder, o critério ainda está vago — reescreva.
2. Prefira, nesta ordem: **teste automatizado** > `grep`/`ls`/contagem > inspeção manual
   (último recurso, marque como gate humano).
3. Escreva o **par (comando, esperado)** — ex.: `esperado vazio`, `= 12`, `exit 0`.
4. Cubra **caso feliz e caso de falha** por caso de uso (regra do `qa`).
5. Um invariante de segurança/arquitetura vira **check negativo** (algo que NÃO pode existir):
   `grep -l <proibido> ...` deve dar **vazio**.

## Sintaxe recomendada: EARS (absorvida do Kiro — ADR 0008)

Para critérios de **comportamento**, escreva na forma EARS (Easy Approach to Requirements
Syntax): `QUANDO <condição> O SISTEMA DEVE <comportamento observável>`. O critério vira
teste quase 1:1 — a condição é o *arrange/act*, o comportamento é o *assert*.

- ✅ "QUANDO o push falhar por rede, O SISTEMA DEVE tentar de novo até 4 vezes com
  backoff exponencial" → teste: simule falha, conte tentativas.
- ✅ "QUANDO a árvore estiver suja, O SISTEMA DEVE abortar sem alterar `main`" → teste:
  suje a árvore, rode, verifique exit ≠ 0 e hash intacto (foi o teste real do ciclo 006).
- Para critérios **estruturais** (arquivo existe, invariante), o par (comando, esperado)
  do passo 3 continua sendo a forma.

## Anti-padrões (reescreva)

- ❌ "a documentação está clara" → ✅ `grep -L "^description:" skills/*/SKILL.md` vazio (existe)
  + revisão didática (gate humano explícito para o "clara").
- ❌ "os agentes read-only são seguros" → ✅ `grep -lE "tools:.*(Write|Edit)" review security ...`
  **vazio** (check negativo).
- ❌ "cobertura boa" (meta numérica gameável) → ✅ 1 teste feliz + 1 de falha por caso de uso.

## Exemplo (do plan 004)

> `ls .claude/agents/*.md | wc -l` = 12 · `grep -L "^name:" ...` vazio · `grep -l "WebSearch"
> curador-pesquisa.md` não-vazio.

**Consumido por:** `spec-agent`/`plan-arquiteto` (escrevem), `qa` (roda), comando `/dod`.
