# Plan 009 — Vendorizar o Spec Kit (seletivo)

- **Spec**: `spec.md` · **Raia**: Plena · **Data**: 2026-07-31

## Constitution Check (principios-maestro.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven | ✅ nasce da spec 009 (F4 do roadmap) |
| II. Orquestração humano-governada | ✅ templates embutem os gates humanos (DoR/plan/merge) no próprio fluxo |
| III. Reversibilidade / gates de risco | ✅ upstream preservado no fork; sync futura é deliberada (por spec), reversível por git |
| IV. Test-First / DoD verificável | ✅ DoD por grep (inclusive escrito em EARS — dogfood do próprio template) |
| V. Economia de contexto / fronteira | ✅ template = decisão empacotada; agente não re-deriva o formato a cada ciclo |
| VI. Artefatos vivos | ✅ UPSTREAM.md registra proveniência; roadmap/CHANGELOG atualizados |
| VII. Governança leve / YAGNI | ✅ só os 3 templates + converge; extension hooks do fork descartados; demais verbatim |

**Sem violações.**

## Como

- **FR1**: reescrever os 3 templates com o formato **provado** nos ciclos 003–008 (o
  mesmo que `novo-ciclo.sh` esqueleta), enriquecido com guidance em comentários HTML:
  quando usar EARS vs check estrutural (skill `dod-verificavel`), como classificar a
  raia (`ambiguidade × raio × irreversibilidade`), Constitution Check preenchível
  (skill `constitution-check`), gate humano explícito no tasks.
- **FR2**: `speckit.converge.md` reescrito enxuto: ler spec/plan/tasks do ciclo →
  inspecionar o estado real → listar o que falta → **anexar** como tasks novas (nunca
  reescrever as feitas) → reportar. Sem hooks de extensão.
- **FR3**: `UPSTREAM.md` com tabela peça → origem → estado (adaptado/verbatim) + regra
  de sync (upstream entra por spec, nunca ad-hoc).
- **FR4**: nota no UPSTREAM.md + comentário no `novo-ciclo.sh` (templates mandam).
- **FR5**: roadmap linha F4 → ✅; CHANGELOG [Unreleased]; `publicar/build.mjs`.

## Verificação (DoD)

- `grep -l "I. Spec-Driven" .specify/templates/plan-template.md` não-vazio.
- `grep -l "Raia" .specify/templates/spec-template.md` e `grep -l "QUANDO"` não-vazios.
- `grep -il "gate" .specify/templates/tasks-template.md` não-vazio.
- `ls .claude/commands/speckit.converge.md`; `grep -l "tasks.md"` nele.
- `grep -l "0.4.3" .specify/UPSTREAM.md` e `grep -l "0117a7b"` não-vazios.
- `grep -l "F4.*✅\|✅.*vendoriz" docs/roadmap.md`; build do site exit 0.
