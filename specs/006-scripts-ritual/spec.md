# Spec 006 — Scripts do ritual (F3)

- **Status**: Aprovada (defaults) · **Raia**: Plena · **Data**: 2026-07-29
- **Origem**: Fase 3 do roadmap + **retro**. Dois passos manuais se repetiram idênticos em
  todos os ciclos; viram script para tirar erro humano e economizar atenção do Orquestrador.

## O quê e por quê

**Dor de retro (comprovada, não especulação):**
- A **promoção `dev → main`** foi feita à mão em 003/004/005 — sempre
  `git branch -f main dev` + `git push` com **retry exponencial**. Passo mecânico, arriscado
  se digitado errado, e **indelegável no *gate*** (a decisão é humana) mas **mecânico na
  *execução*** (o comando não).
- O **scaffold de ciclo** — `mkdir specs/NNN-*` + criar `spec/plan/tasks/qa-report` — foi
  repetido em cada ciclo. Padroniza a estrutura e lembra os artefatos obrigatórios.

**Princípio-guia (II + III):** o script executa o **mecânico**; o **gate humano continua**
— `promover-main.sh` só roda depois do "sim" e exige confirmação; não decide por ninguém.

## Requisitos funcionais

- **FR1**: `scripts/promover-main.sh` — promove `dev → main` com push e **retry exponencial**
  (2s/4s/8s/16s). Exige **confirmação explícita** (não promove sozinho); aborta se a árvore
  estiver suja ou se `dev` não estiver à frente de `main`. Ecoa o que vai fazer antes.
- **FR2**: `scripts/novo-ciclo.sh <NNN> <slug>` — cria `specs/NNN-slug/` com os 4 artefatos
  (`spec.md`, `plan.md`, `tasks.md`, `qa-report.md`) a partir de **cabeçalhos-esqueleto**
  (não vazios: título + campos Status/Raia/Data + Constitution Check em branco). Não
  sobrescreve ciclo existente.
- **FR3**: `scripts/verificar-agentes.sh` — roda os invariantes estruturais dos agentes
  (contagem, frontmatter, read-only sem Write/Edit) — a "fitness function" que rodei à mão
  em 003/004. Exit ≠ 0 se algum invariante quebrar.
- **FR4**: `scripts/README.md` — o que cada script faz, quando usar, e o que ele **não**
  decide (o gate humano).

## Fora de escopo

- Workflows de orquestração multiagente pesados — só quando a dor aparecer (YAGNI); F3 aqui
  entrega **scripts**, o degrau concreto.
- Automatizar o **gate** (a decisão de promover) — isso é indelegável (Princípio II).

## Critérios de aceite (DoD)

- [ ] 3 scripts em `scripts/*.sh`, todos com `#!/usr/bin/env bash`, `set -euo pipefail` e
      executáveis (`chmod +x`).
- [ ] `promover-main.sh` **aborta sem confirmação** e com árvore suja (testável a seco).
- [ ] `novo-ciclo.sh` cria os 4 artefatos e **não sobrescreve** existente.
- [ ] `verificar-agentes.sh` sai 0 no estado atual (12 agentes ok) e ≠ 0 se um invariante quebra.
- [ ] `scripts/README.md` lista os 3 + o limite do gate humano.

## Clarify (resolvido — defaults, 2026-07-29)

1. **Escopo F3**: **scripts** (dor de retro), workflows pesados adiados (YAGNI).
2. **Segurança**: script executa o mecânico; **gate humano preservado** (confirmação + aborta).
