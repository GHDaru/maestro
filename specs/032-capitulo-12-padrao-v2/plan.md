# Plan 032 — Capítulo 12 no padrão v2

- **Spec**: `spec.md` · **Raia**: leve · **Data**: 2026-08-02

## Constitution Check (principios-maestro.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven | ✅ spec antes da edição, requisitos em EARS |
| II. Orquestração humano-governada | ✅ gate humano ao final |
| III. Reversibilidade / gates de risco | ✅ documento reversível; registro superável citado |
| IV. Test-First / DoD verificável | ✅ esqueleto por script; FR5 é um número de saída de comando |
| V. Economia de contexto / fronteira | ✅ um capítulo por ciclo, até o fim |
| VI. Artefatos vivos | ✅ datação; achados abertos declarados no corpo |
| VII. Governança leve / YAGNI | ✅ é o tema; a poda aparece com evidência |
| VIII. Comunicação inteligível | ✅ ADR e siglas por extenso; nomes em português |

## Como

1. Medir as duas forças: `git log` da constituição (três toques), inventário da periferia
   (6 skills, 10 scripts, 10 registros de decisão) e a seção de recusas do modelo.
2. Usar o caso do ciclo 021 (princípio VIII sem linha no Constitution Check) como exemplo de
   governança se auditando — é o argumento mais forte do capítulo e é nosso.
3. Fechar com os achados abertos, nomeados, em vez de conclusão redonda.

## Verificação (DoD)

```bash
scripts/verificar-capitulos.sh        # 13 migrados, 0 pendentes
git log --format="%ad %s" --date=short -- docs/governance/principios-maestro.md
sed -n '/## 10. O que NÃO adotamos/,/^## 11/p' docs/governance/modelo-operacional.md
node publicar/build.mjs
```
