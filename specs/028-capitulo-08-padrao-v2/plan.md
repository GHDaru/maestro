# Plan 028 — Capítulo 08 no padrão v2

- **Spec**: `spec.md` · **Raia**: leve · **Data**: 2026-08-02

## Constitution Check (principios-maestro.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven | ✅ spec antes da edição, requisitos em EARS |
| II. Orquestração humano-governada | ✅ gate humano ao final |
| III. Reversibilidade / gates de risco | ✅ documento reversível |
| IV. Test-First / DoD verificável | ✅ esqueleto por script; contagens por comando |
| V. Economia de contexto / fronteira | ✅ um capítulo por ciclo |
| VI. Artefatos vivos | ✅ é o tema — e o capítulo mostra a cobrança, não a intenção |
| VII. Governança leve / YAGNI | ✅ o catálogo diz o que **não** criar e por quê |
| VIII. Comunicação inteligível | ✅ ADR e siglas por extenso; nomes dos artefatos em português |

## Como

1. Extrair a evidência: trecho real do gate de changelog na integração contínua, contagem
   de commits por registro de decisão, contagem de ciclos com os quatro artefatos.
2. Investigar a exceção antes de citá-la (skill `diagnostico-antes-do-fix` aplicada a
   texto): o ADR 0008 tem dois commits — ver **o que** mudou antes de afirmar imutabilidade.
3. Traduzir o catálogo para nomes em português e acrescentar o índice de decisões, que não
   estava na tabela.

## Verificação (DoD)

```bash
scripts/verificar-capitulos.sh
grep -n -A8 "changelog" .github/workflows/ci.yml
for f in docs/adr/00*.md; do echo "$(basename $f): $(git log --oneline -- $f | wc -l)"; done
node publicar/build.mjs
```
