# Plan 027 — Capítulo 07 no padrão v2

- **Spec**: `spec.md` · **Raia**: leve · **Data**: 2026-08-02

## Constitution Check (principios-maestro.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven | ✅ spec antes da edição, requisitos em EARS |
| II. Orquestração humano-governada | ✅ gate humano ao final; a retro continua cerimônia humana |
| III. Reversibilidade / gates de risco | ✅ documento reversível |
| IV. Test-First / DoD verificável | ✅ esqueleto por script; histórico e branches por comando |
| V. Economia de contexto / fronteira | ✅ um capítulo por ciclo |
| VI. Artefatos vivos | ✅ datação; a evidência é o próprio histórico do repositório |
| VII. Governança leve / YAGNI | ✅ o capítulo justifica o que foi **cortado** |
| VIII. Comunicação inteligível | ✅ cerimônias nomeadas em português; siglas por extenso |

## Como

1. Extrair a evidência do histórico: `git log` do arquivo de anti-padrões (quatro levas com
   ciclo de origem) e `git branch -a` (trabalho em curso igual a um).
2. Preservar a teoria (cerimônia = função; retro amplificada; gargalo é atenção) e ligá-la
   ao que aconteceu de fato, incluindo a parte incômoda: a retro só foi executada depois de
   duas anotações mortas.
3. Traduzir os nomes das cerimônias mantendo a correspondência com Scrum/Shape Up.

## Verificação (DoD)

```bash
scripts/verificar-capitulos.sh
git log --format="%ad %s" --date=short -- skills/anti-padroes/SKILL.md   # as 4 levas
git branch -a                                                            # dev, main
node publicar/build.mjs
```
