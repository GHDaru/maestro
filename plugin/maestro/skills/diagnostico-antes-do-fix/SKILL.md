---
name: diagnostico-antes-do-fix
description: Disciplina de causa raiz — investigar antes de corrigir. Use quando encontrar qualquer bug, teste falhando ou comportamento inesperado, ANTES de propor ou aplicar qualquer correção. Corrigir sintoma sem causa é falha, não progresso.
---

# Diagnóstico antes do fix

## Iron Law

```
NENHUM FIX SEM INVESTIGAÇÃO DE CAUSA RAIZ ANTES
```

**Violar a letra desta regra é violar o espírito dela.** Isso NÃO é desculpa:
- "É óbvio o que está errado" — se fosse, por que o bug existe? Prove com evidência.
- "O fix é pequeno, testo depois" — fix sem causa confirmada é aposta, não engenharia.
- "Já vi esse erro antes" — padrão parecido ≠ mesma causa; a checagem custa minutos.

## As fases (em ordem, sem pular)

1. **Leia o erro de verdade** — a mensagem inteira, o stack completo, o log em volta.
   A maioria dos "mistérios" está escrita no erro que ninguém leu.
2. **Reproduza** — se não reproduz, você não sabe o que está consertando. Bug exige um
   **teste que o reproduz** (red) antes do fix — regra que já era nossa; aqui ela ganha
   a fase de investigação antes.
3. **Isole** — estreite até a menor condição que dispara (bissecção de commit/dado/
   config; logs no caminho suspeito; um fator por vez).
4. **Hipótese única e explícita** — "a causa é X, porque a evidência Y". Se há duas
   hipóteses, há mais investigação a fazer — não dois fixes a tentar.
5. **Prove** — o teste da fase 2 passa a falhar exatamente pela causa X (não por acaso).
6. **Só então corrija** — o fix ataca X; o teste vira verde; rode o conjunto (verde
   local ≠ certo global).

## Sinais de que você pulou fase (pare e volte)

- Está no segundo "tenta isso" seguido (anti-padrão 5, retry cego).
- O fix "funcionou" mas você não sabe explicar por quê.
- A correção alarga escopo ("aproveitei para...") — anti-padrão 10.

**Consumida por:** `dev-implementador`, `qa`. **Handoff:** fix + teste → `review`.
**Fontes:** systematic-debugging (Superpowers, Apêndice B — adaptado); retros; anti-padrões 5/7/10.
