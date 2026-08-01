# Spec 018 — Instalação visível + UX e jornadas executáveis

- **Status**: Aprovada (auditoria do Steward) · **Raia**: Plena · **Data**: 2026-08-01
- **Origem**: dois relatos do Steward — (a) outra Inteligência Artificial (IA) tentou
  instalar o Maestro e disse que "não tinha"; (b) UX e jornadas não apareciam no diagrama
  BPMN (*Business Process Model and Notation*).

## O quê e por quê

Duas lacunas confirmadas por inspeção, com naturezas diferentes:

1. **O instalador existia e era invisível.** `scripts/instalar-maestro.sh` estava no repo
   desde o ciclo 013, mas o `README.md` — o único lugar que uma IA lê primeiro — **não o
   mencionava**. Artefato que existe e não está no ponto de entrada não existe para quem chega.
2. **A norma prescrevia o que o toolkit não entregava.** O modelo operacional cita
   **UX-agent** (§4), **`ux-design.md`** (§6, essencial se houver interface), **journey doc**
   (§6) e exige `ux-design.md` na Definição de Pronto para Iniciar (DoR, §7) — e não havia
   agente, skill nem template para nenhum deles. O BPMN estava **correto quanto ao toolkit
   e incompleto quanto à norma**.

## Requisitos funcionais

- **FR1**: seção de instalação no `README.md`, no topo, com nota explícita para IA
  ("não existe `npm install`; instalar = copiar o toolkit e apontar o `CLAUDE.md`").
- **FR2**: agente `ux-semantica` — o UX-agent que o modelo prescrevia.
- **FR3**: skill `jornada-viva` — documento + capturas do build real + **heurística datada**,
  com o check que faltava (`data da heurística ≥ data das capturas`).
- **FR4**: templates `ux-design-template.md` e `journey-template.md`.
- **FR5**: **fitness function** `verificar-papeis.sh` — todo papel prescrito no modelo tem
  agente; todo artefato essencial tem template. Impede a divergência de voltar.
- **FR6**: BPMN com o **ramo de interface** (tem UI? → semântica → `ux-design.md` → ◆gate
  de UX → captura → heurística datada → journey).
- **FR7**: índices, instalador e contagens atualizados (13 agentes · 6 skills · 6 scripts).

## Fora de escopo

- Agentes de domínio (frontend/backend/dados) — seguem entrando por projeto.
- Catálogo semântico de componentes: é do **projeto** que usa o Maestro, não do método.

## Critérios de aceite (DoD)

- [ ] QUANDO um papel prescrito pelo modelo não tiver agente, O SISTEMA DEVE falhar
      `verificar-papeis.sh` com código ≠ 0 nomeando o papel. *(provado falhando)*
- [ ] `grep -c "instalar-maestro.sh" README.md` ≥ 1.
- [ ] `ls .claude/agents/*.md | wc -l` = 13; `ls skills/*/SKILL.md | wc -l` = 6.
- [ ] Templates de UX e jornada existem em `.specify/templates/`.
- [ ] BPMN contém a raia "Ramo de interface"; build do site verde.

## Clarify (resolvido)

1. **UX vira agente de domínio ou de método?** De **método** — a *semântica* (papel antes
   do componente) é regra do Maestro; o *design system* é do projeto.
