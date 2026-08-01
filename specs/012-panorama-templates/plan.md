# Plan 012 — Apêndice C: panorama exploratório

- **Spec**: `spec.md` · **Raia**: Plena · **Data**: 2026-08-01

## Constitution Check (principios-maestro.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven | ✅ nasce da spec 012 |
| II. Orquestração humano-governada | ✅ triagem propõe; hands-on/absorção só por gatilho + gate |
| III. Reversibilidade / gates de risco | ✅ pesquisa read-only |
| IV. Test-First / DoD verificável | ✅ DoD por grep + build (EARS) |
| V. Economia de contexto / fronteira | ✅ funil evita reler o ecossistema a cada dúvida — vira link |
| VI. Artefatos vivos | ✅ entra no livro; remete aos já decididos sem duplicar |
| VII. Governança leve / YAGNI | ✅ observar-com-gatilho como default; nada importado |

**Sem violações.**

## Como

Papel `curador-pesquisa` (3 varreduras web) → apêndice em 4 famílias (SDD completos,
engenharia de contexto, orquestração pesada, coleções/marketplaces) → triagem + gatilho
por item → síntese crítica (o que é genuinamente novo: PRP, CCPM).

## Verificação (DoD)

- `node publicar/build.mjs` → 23 páginas, links OK.
- `grep -c "Triagem" apendice-c` ≥ 8; `grep -c "https" apendice-c` ≥ 8.
