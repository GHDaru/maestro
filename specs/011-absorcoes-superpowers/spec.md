# Spec 011 — Absorções do Superpowers (Apêndice B)

- **Status**: Aprovada ("Tudo aprovado" — `gate-010-vereditos`) · **Raia**: Plena · **Data**: 2026-07-31
- **Origem**: vereditos do Apêndice B aprovados integralmente pelo Steward.

## O quê e por quê

Materializar as 5 absorções aprovadas: enforcement linguístico (Iron Laws) nas skills,
protocolo de teste de skill (TDD para documentação), skill de diagnóstico antes do fix,
checkpoint de review por task, autossuficiência de task, e bootstrap de enforcement no
CLAUDE.md. Valor: as skills passam a **comandar** (não sugerir) e a serem **testadas**
(não presumidas).

## Requisitos funcionais

- **FR1 — Iron Laws nas skills existentes**: cada uma das 4 skills ganha sua lei
  inegociável no padrão "violar a letra é violar o espírito": `dod-verificavel`
  ("nenhum critério sem comando que o prove"), `constitution-check` ("nenhum plan sem
  as 7 linhas"), `combater-amontoado` ("nenhuma sigla nua"), `anti-padroes` ("nomeie o
  anti-padrão antes de corrigi-lo").
- **FR2 — TDD para skills**: `skill-author` (agente) ganha o protocolo — cenário de
  pressão → baseline SEM a skill (RED) → escrever → reteste (GREEN) → fechar brechas;
  regra também no `skills/README.md` (regra de nascimento ampliada).
- **FR3 — Skill nova `diagnostico-antes-do-fix`**: Iron Law "nenhum fix sem investigação
  de causa raiz"; fases investigação → hipótese → prova (teste que reproduz) → fix.
- **FR4 — Review por task**: na raia plena com >3 tasks, checkpoint leve após cada task
  (`docs/agents/comunicacao.md` + system prompt do `dev-implementador`).
- **FR5 — Zero contexto por task**: guidance no `tasks-template.md` ("escreva a task
  para quem tem zero contexto — tudo que precisa está nela ou linkado").
- **FR6 — Bootstrap de enforcement**: parágrafo no `CLAUDE.md` do maestro mandando
  verificar skills aplicáveis antes de agir.

## Fora de escopo

- Worktrees por task (segue em observar, gatilho F3).
- HARD-GATE universal (raias mandam — decisão registrada no Apêndice B).

## Critérios de aceite (DoD)

- [ ] QUANDO qualquer skill for lida, O SISTEMA DEVE apresentar sua Iron Law
      (`grep -L "Iron Law" skills/*/SKILL.md` → vazio).
- [ ] `ls skills/*/SKILL.md | wc -l` = 5 (nova: `diagnostico-antes-do-fix`).
- [ ] `grep -l "baseline" .claude/agents/skill-author.md` não-vazio (protocolo TDD).
- [ ] `grep -l "checkpoint" docs/agents/comunicacao.md` e no `dev-implementador.md`.
- [ ] `grep -l "zero contexto" .specify/templates/tasks-template.md` não-vazio.
- [ ] `grep -il "skills" CLAUDE.md` com o parágrafo de enforcement.

## Clarify (resolvido)

1. **Testar as skills novas com baseline já?** A skill 011 nasce adaptada de fonte
   já testada em produção (Superpowers); o protocolo de baseline vale para skills
   **novas originais** daqui em diante — anotado no qa-report (honestidade).
