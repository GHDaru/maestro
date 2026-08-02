# Plan 026 — Capítulo 06 no padrão v2

- **Spec**: `spec.md` · **Raia**: leve · **Data**: 2026-08-02

## Constitution Check (principios-maestro.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven | ✅ spec antes da edição, requisitos em EARS |
| II. Orquestração humano-governada | ✅ é o tema do capítulo; gate humano ao final do ciclo |
| III. Reversibilidade / gates de risco | ✅ documento reversível |
| IV. Test-First / DoD verificável | ✅ esqueleto por script; comandos citados reproduzem os números |
| V. Economia de contexto / fronteira | ✅ um capítulo por ciclo |
| VI. Artefatos vivos | ✅ datação; o caso do papel sem executável fica registrado no livro |
| VII. Governança leve / YAGNI | ✅ papéis de time grande explicitamente rejeitados |
| VIII. Comunicação inteligível | ✅ RACI e IA por extenso na primeira ocorrência |

## Como

1. Medir antes de afirmar: quais agentes não têm `Write`/`Edit`, quantos gates humanos
   estão registrados, o que `verificar-papeis.sh` devolve hoje.
2. Preservar a teoria correta (RACI adaptado, A indelegável, funil, C independente) e
   substituir a seção de "insight" por evidência.
3. Ligar cada regra a um verificador: independência → `verificar-agentes.sh`; papel
   prescrito → `verificar-papeis.sh`; A humano → índice de decisões.

## Verificação (DoD)

```bash
scripts/verificar-capitulos.sh
for f in .claude/agents/*.md; do grep -q "^tools:.*\(Write\|Edit\)" "$f" || basename "$f"; done
grep -c '"id": "gate-main' docs/registro/decisoes.jsonl
node publicar/build.mjs
```
