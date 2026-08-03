# Receita — escrever um critério verificável

> Objetivo: transformar critério vago em check que uma máquina confere sozinha.
> Tempo: ~5 min por critério. Skill: `verifiable-dod`.

## A pergunta que resolve tudo

> **"Que comando prova isto?"**

Se você não consegue responder, o critério ainda está vago. Reescreva.

## 1. Escolha a forma certa

**Comportamento** → sintaxe EARS (*Easy Approach to Requirements Syntax*, Abordagem Simples
de Sintaxe de Requisitos):

```
QUANDO ‹condição› O SISTEMA DEVE ‹comportamento observável›
```

A condição é o *preparar/agir*; o comportamento é o *verificar*. Vira teste quase 1:1.

**Estrutura ou invariante** → par (comando, esperado):

```
`ls skills/*/SKILL.md | wc -l`  →  esperado: 5
`grep -L "Iron Law" skills/*/SKILL.md`  →  esperado: vazio
```

## 2. Prefira nesta ordem

1. **Teste automatizado** (roda no pipeline)
2. **`grep` / `ls` / contagem** (barato e explícito)
3. **Inspeção humana** — último recurso, e marque como **gate humano** no critério

## 3. Use check negativo para invariante de segurança

O que **não pode existir** vira busca que deve dar vazio:

```
`grep -lE "tools:.*(Write|Edit)" review.md security.md`  →  esperado: vazio
```

## 4. Cubra falha, não só sucesso

Um caso feliz **e** um de falha por caso de uso. Bug exige um teste que o reproduz
**antes** do reparo.

## Reescreva estes (anti-padrões)

| ❌ Vago | ✅ Verificável |
|---|---|
| "a documentação está clara" | `grep -L "^description:"` vazio **+** revisão didática (gate humano declarado) |
| "os agentes são seguros" | `grep -lE "tools:.*(Write\|Edit)" <read-only>` → vazio |
| "cobertura boa" | 1 teste feliz + 1 de falha por caso de uso |
| "o script é robusto" | QUANDO a árvore estiver suja, O SISTEMA DEVE abortar sem alterar `main` |

## Pronto quando

- [ ] Cada critério tem comando **ou** está marcado como gate humano
- [ ] Nenhuma meta numérica gameável (`cobertura ≥ X%`)
- [ ] Os invariantes viraram check negativo

**Por quê?** → [Capítulo 09 — DoR/DoD](../handbook/09-definition-of-ready-done.md) ·
[Capítulo 13 §5.12](../handbook/13-decisoes-de-engenharia.md)
