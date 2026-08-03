# Receita — abrir um ciclo

> Objetivo: sair de "chegou uma demanda" para "spec aprovada, pronta para planejar".
> Tempo: ~10 min. Papel: Steward (humano) + `spec-agent`.

## 1. Classifique a raia (30 segundos)

Pergunte: `ambiguidade × raio de impacto × irreversibilidade`.

| Se… | Raia | O que fazer |
|---|---|---|
| Dá para descrever o diff numa frase (typo, log, correção óbvia) | **leve** | Não abra ciclo — o pull request (PR) é o artefato. **Pule esta receita.** |
| Feature ambígua, mudança de contrato, cross-feature | **plena** | Siga abaixo |
| Infraestrutura, migração, deploy | **infra** | Siga abaixo **+** bloco de reversibilidade |

Na dúvida entre leve e plena → **plena**. Infra **nunca** é leve.

## 2. Crie o esqueleto

```bash
scripts/new-cycle.sh 014 nome-do-ciclo    # NNN de 3 dígitos, slug em kebab-case
```

Cria `specs/014-nome-do-ciclo/` com os quatro artefatos. Não sobrescreve ciclo existente.

## 3. Escreva a spec (o quê e por quê — nunca o como)

Preencha, na ordem: **Origem** (de onde veio a demanda) → **O quê e por quê** (o problema
e o valor) → **Requisitos funcionais** (FR1, FR2…) → **Fora de escopo** (tão importante
quanto o escopo) → **Critérios de aceite** ([receita própria](escrever-criterio-verificavel.md))
→ **Clarify** (o que está ambíguo).

**Não invente requisito não dito.** Ambiguidade vira pergunta no Clarify.

## 4. Passe o gate de Prontidão (DoR — Definition of Ready)

O humano aprova a spec antes de qualquer plano. Checklist:

- [ ] Critérios de aceite testáveis (um comando prova cada um)
- [ ] Ambiguidades resolvidas ou registradas no Clarify
- [ ] Fora de escopo explícito
- [ ] Apetite definido (quanto tempo essa aposta merece)

## 5. Só então planeje

`plan.md` com o **Constitution Check** completo — as oito linhas, uma por princípio
(skill `constitution-check`). Violação → reformule ou registre em Complexity Tracking.

## Pronto quando

- [ ] `specs/NNN-slug/spec.md` preenchida e **aprovada por humano**
- [ ] Raia declarada no cabeçalho
- [ ] Nenhum `<...>` de template sobrando

**Por quê?** → [Capítulo 03 — Spec-Driven](../handbook/03-spec-driven.md) ·
[Capítulo 09 — DoR/DoD](../handbook/09-definition-of-ready-done.md)
