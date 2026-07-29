# Spec 005 — Skills V0 (padrão agentskills.io)

- **Status**: Aprovada (defaults) · **Raia**: Plena · **Data**: 2026-07-29
- **Origem**: Fase 2 do roadmap. Agora que o `skill-author` existe, empacotamos como
  **skills** os procedimentos que já se repetiram nos nossos próprios ciclos (001–004).

## O quê e por quê

Skill = procedimento recorrente empacotado no padrão aberto `SKILL.md` (agentskills.io):
frontmatter `name` + `description` (com **gatilhos** claros de quando disparar) + corpo com
passos verificáveis. Dispara sozinha no contexto certo, então padroniza a execução sem o
humano ter que lembrar o passo a passo.

**Dor real observada (não especulação):**
- Todo `plan.md` refez a mão a tabela **Constitution Check** I–VII (003, 004 idênticos).
- Todo ciclo reescreveu à mão os **checks de DoD** como `grep`/`ls`/teste (003, 004 iguais).
- O usuário sinalizou explicitamente o **"amontoado"** (docs densos, siglas sem dicionário)
  como o defeito a combater — revisão didática é recorrente.

## Requisitos funcionais

- **FR1**: `skills/constitution-check/SKILL.md` — guia para produzir a tabela I–VII no
  `plan.md`, quando um princípio conta como violado, e o que fazer (Complexity Tracking).
- **FR2**: `skills/dod-verificavel/SKILL.md` — transformar critérios de aceite em **fitness
  functions executáveis** (`grep`/`ls`/teste) no momento de escrever spec/plan. Complementa
  o comando `/dod` (que **roda**; a skill ajuda a **escrever** os checks). Sem duplicar.
- **FR3**: `skills/combater-amontoado/SKILL.md` — checklist de revisão didática (um assunto
  por página, sigla expandida na 1ª ocorrência, sem jargão órfão, ordem que conta história).
- **FR4**: cada `SKILL.md` tem frontmatter válido (`name`, `description` com gatilhos) e
  corpo com passos verificáveis + exemplo concreto.
- **FR5**: índice `skills/README.md` liga cada skill ao agente/comando que a usa.

## Fora de escopo

- Workflows e scripts (Fase 3) — inclusive `promote-main.sh`.
- Skills especulativas sem dor recorrente comprovada (YAGNI).

## Critérios de aceite (DoD)

- [ ] 3 arquivos `skills/*/SKILL.md` com frontmatter `^name:` e `^description:`.
- [ ] Cada `description` contém gatilho ("Use quando…").
- [ ] `dod-verificavel` referencia `/dod` (complementaridade explícita, não duplicação).
- [ ] `skills/README.md` lista as 3.

## Clarify (resolvido — defaults, 2026-07-29)

1. **Quais skills**: as 3 de dor comprovada nos ciclos 001–004 (acima). Demais entram por
   retro futura, não especulação.
2. **Padrão**: agentskills.io (frontmatter name/description + corpo).
