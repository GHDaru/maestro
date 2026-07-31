# Tasks 008 — Absorções do estudo maestro-02

## Verificação primeiro
- [x] T0 — Checks: JSONL parse, bash -n/+x/exit 0, contagens, greps, status ADR.

## Implementação
- [x] T1 — FR1: `docs/registro/` (README + decisoes.jsonl seed 6) + `registrar-decisao.sh`
  (valida JSON, campos, id único; append-only) — guard de duplicado testado.
- [x] T2 — FR2: `scripts/retro.sh` (ciclos+vereditos, gates pendentes, últimas decisões,
  inventário, perguntas) — rodado ao vivo, exit 0.
- [x] T3 — FR3: `skills/anti-padroes/SKILL.md` (12 anti-padrões em 4 famílias) + catálogo.
- [x] T4 — FR4: handbook cap. 10 §6b (wave — gates em nível de task).
- [x] T5 — FR5: handbook cap. 04 §6b (economia de contexto medida).
- [x] T6 — FR6: EARS na skill `dod-verificavel` (com exemplo real do ciclo 006).
- [x] T7 — FR7: ADR 0008 → Aceito; índice ADR linka registro; Apêndice A "incorporado";
  scripts/skills READMEs; CHANGELOG [Unreleased]; site rebuild.

## Gate
- [x] T8 — DoD verde + aprovação prévia do Steward ("pode incorporar todas as sugestões")
  → promoção via `promover-main.sh`.
