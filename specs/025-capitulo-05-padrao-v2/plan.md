# Plan 025 — Capítulo 05 no padrão v2

- **Spec**: `spec.md` · **Raia**: leve · **Data**: 2026-08-02

## Constitution Check (principios-maestro.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven | ✅ spec antes da edição, requisitos em EARS |
| II. Orquestração humano-governada | ✅ é o tema: o *reduce* fica com o humano; gate ao final |
| III. Reversibilidade / gates de risco | ✅ documento reversível |
| IV. Test-First / DoD verificável | ✅ esqueleto por script; números por comando |
| V. Economia de contexto / fronteira | ✅ o capítulo defende corte por costura, não por quantidade |
| VI. Artefatos vivos | ✅ datação; achado das raias retomado em vez de escondido |
| VII. Governança leve / YAGNI | ✅ registra explicitamente o padrão que **não** adotamos |
| VIII. Comunicação inteligível | ✅ QA, IA e siglas por extenso na primeira ocorrência |

## Como

1. Levantar o uso real por comando: comandos versionados (encadeamento), ciclos com portão
   provado falhando (avaliador-otimizador), ausência de autônomo.
2. Traduzir os nomes em português no corpo (encadeamento, roteamento, paralelização,
   orquestrador-trabalhadores, avaliador-otimizador, autônomo) — Princípio VIII.
3. Reaproveitar a teoria correta (corte × reduce, espectro, menor autonomia) e ligar cada
   padrão ao lugar onde ele vive no método.

## Verificação (DoD)

```bash
scripts/verificar-capitulos.sh
ls .claude/commands/ | wc -l                                  # 11, citados no capítulo
grep -rli "prova.* falhando" specs/*/qa-report.md             # os 4 ciclos citados
node publicar/build.mjs
```
