# Spec 009 — Vendorizar o Spec Kit (seletivo) — F4

- **Status**: Aprovada ("bora vendorizar") · **Raia**: Plena · **Data**: 2026-07-31
- **Origem**: F4 do roadmap. Os templates instalados em `.specify/templates/` são os
  genéricos do upstream (inglês, speckit 0.4.3) — sem raias, sem EARS, sem os Princípios
  I–VII. O fork (`GHDaru/spec-kit@0117a7b`) tem o comando `converge`, não instalado.

## O quê e por quê

**Vendorizar** = trazer para dentro do repo, como fonte nossa, o que usamos do Spec Kit —
adaptado ao método. As decisões empacotadas do Maestro precisam morar no nosso pacote,
não em templates genéricos que os comandos `/speckit.*` leem sem as nossas regras.
Upstream passa a ser consultado por decisão, não por acidente.

## Requisitos funcionais

- **FR1 — Templates adaptados** (os 3 do ciclo, em PT, com o formato provado nos ciclos
  003–008): `spec-template.md` (Status/Raia/Origem · O quê e por quê · FRs · Fora de
  escopo · **critérios EARS** · Clarify), `plan-template.md` (**Constitution Check I–VII
  real**, Como, Verificação/DoD executável), `tasks-template.md` (verificação primeiro,
  implementação, **gate humano** ao fim). Guidance embutida em comentários.
- **FR2 — Comando `converge` vendorizado**: `.claude/commands/speckit.converge.md`
  adaptado do fork (sem o mecanismo de extension hooks — YAGNI): compara o estado real
  com spec/plan/tasks e **anexa** o trabalho faltante ao `tasks.md`.
- **FR3 — Proveniência**: `.specify/UPSTREAM.md` — de onde veio cada peça (versão do
  speckit, commit do fork), o que foi adaptado vs. mantido verbatim, e a regra de
  sincronização deliberada (upstream só entra por spec).
- **FR4 — Relação com `novo-ciclo.sh`**: declarar a hierarquia — templates = referência
  completa (usada pelos comandos `/speckit.*`); esqueleto do script = atalho mínimo
  derivado. Divergirem → templates mandam.
- **FR5 — Rastreabilidade**: roadmap F4 ✅; CHANGELOG; site rebuild.

## Fora de escopo

- Adaptar `constitution-template`/`agent-file-template`/`checklist-template` (pouco uso —
  ficam verbatim, anotados no UPSTREAM.md).
- Trazer scripts/workflows do upstream além do necessário aos comandos atuais.
- Templates de jornada/design (ghdaru) — próximo ciclo, não este.

## Critérios de aceite (DoD)

- [ ] QUANDO `/speckit.plan` ler o template, O SISTEMA DEVE apresentar a tabela
      Constitution Check com os 7 princípios nomeados (`grep "I. Spec-Driven"`).
- [ ] `spec-template.md` contém "Raia" e a forma EARS (`grep "QUANDO"`), em PT.
- [ ] `tasks-template.md` termina em gate humano (`grep "gate"`).
- [ ] `.claude/commands/speckit.converge.md` existe e referencia `tasks.md`.
- [ ] `.specify/UPSTREAM.md` cita speckit 0.4.3 e o commit do fork.
- [ ] Roadmap F4 = ✅; CHANGELOG com entrada; build do site verde.

## Clarify (resolvido)

1. **Onde ficam os adaptados?** No mesmo lugar (`.specify/templates/`) — é onde os
   comandos leem; vendorizar é trocar o conteúdo pela nossa versão, com proveniência.
2. **Inglês ou PT?** PT — todo o método é em PT; os templates são parte do método.
