# QA-report 009 — Vendorizar o Spec Kit

- **Data**: 2026-07-31 · **Raia**: Plena · **Veredito**: ✅ CONFORME

## Fitness functions (DoD)

| Check | Esperado | Resultado |
|---|---|---|
| `grep -l "I. Spec-Driven" plan-template.md` | não-vazio | ✅ |
| `grep -l "Raia"` e `grep -l "QUANDO"` no spec-template | não-vazios | ✅ |
| `grep -il "gate" tasks-template.md` | não-vazio | ✅ |
| `speckit.converge.md` existe e cita `tasks.md` | sim | ✅ |
| `UPSTREAM.md` cita `0.4.3` e `0117a7b` | sim | ✅ |
| Roadmap F4 ✅ · CHANGELOG | sim | ✅ |
| `publicar/build.mjs` | exit 0, links OK | ✅ |

## Cobertura

- **FR1**: 3 templates agora são fonte nossa, com o formato provado nos ciclos 003–008 e
  guidance embutida (raia, EARS, Constitution Check, gates). Os comandos `/speckit.*`
  verbatim herdam o método ao ler os templates.
- **FR2**: `converge` vendorizado enxuto (anexa, nunca reescreve; sem extension hooks).
- **FR3/FR4**: proveniência completa + regra de sync deliberada + hierarquia de scaffolds.
- **Fora de escopo respeitado**: checklist/constitution/agent-file verbatim (anotados).

## Gate

- Aprovação do Steward ("bora vendorizar"); promoção via `promover-main.sh` com registro
  automático (ADR 0009).
