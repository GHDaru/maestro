# Plan 010 — Estudo hands-on do Superpowers

- **Spec**: `spec.md` · **Raia**: Plena · **Data**: 2026-07-31

## Constitution Check (principios-maestro.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven | ✅ nasce da spec 010; cumpre promessa do ADR 0008 (hands-on sob gatilho) |
| II. Orquestração humano-governada | ✅ vereditos são proposta; decisão é do Steward (FR3) |
| III. Reversibilidade / gates de risco | ✅ estudo read-only; nada instalado |
| IV. Test-First / DoD verificável | ✅ DoD por grep + build (EARS no critério do sumário) |
| V. Economia de contexto / fronteira | ✅ estudo vira apêndice consultável; próximo ciclo não relê o repo |
| VI. Artefatos vivos | ✅ entra no livro (sumário + índice do handbook) |
| VII. Governança leve / YAGNI | ✅ só estudo + vereditos; incorporação fica para ciclo aprovado |

**Sem violações.**

## Como

- Padrão do Apêndice A: anatomia → ideias com veredito/destino → onde não serve →
  tensões → síntese. Comparar cada prática com o equivalente do Maestro (validação
  mútua ou lacuna real).
- Registrar explicitamente a **tensão** HARD-GATE universal (design para tudo) ×
  raias proporcionais (nossa posição, ADR 0005) — com racional.
- Sumário: linha nova na seção Apêndices; índice do handbook: linha na tabela.

## Verificação (DoD)

- `node publicar/build.mjs` → exit 0, 22 páginas.
- `grep -c "Veredito" docs/handbook/apendice-b-superpowers.md` ≥ 6.
- `grep -l "44c9b2d"` e `grep -l "raia"` no apêndice → não-vazios.
