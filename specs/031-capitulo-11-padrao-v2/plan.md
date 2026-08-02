# Plan 031 — Capítulo 11 no padrão v2

- **Spec**: `spec.md` · **Raia**: leve · **Data**: 2026-08-02

## Constitution Check (principios-maestro.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven | ✅ spec antes da edição, requisitos em EARS |
| II. Orquestração humano-governada | ✅ gate humano ao final |
| III. Reversibilidade / gates de risco | ✅ documento reversível |
| IV. Test-First / DoD verificável | ✅ esqueleto por script; cada elo conferido por comando |
| V. Economia de contexto / fronteira | ✅ um capítulo por ciclo |
| VI. Artefatos vivos | ✅ é o tema: o elo existe porque o fluxo o obriga |
| VII. Governança leve / YAGNI | ✅ matriz formal segue rejeitada, com motivo |
| VIII. Comunicação inteligível | ✅ siglas por extenso; nomes em português |

## Como

1. Reconstituir a cadeia real de um ciclo, do índice de decisões até o registro de decisão,
   copiando os dados como estão (sem parafrasear).
2. Medir a força de cada elo: quais são obrigados por script e quais são convenção.
3. Nomear o elo frágil no corpo do capítulo e transformá-lo em exercício de verificação.

## Verificação (DoD)

```bash
scripts/verificar-capitulos.sh
grep "gate-main-0021b20" docs/registro/decisoes.jsonl
git log --oneline --grep="spec 021"
git log --oneline --all | grep -c "spec 0"     # 28
node publicar/build.mjs
```
