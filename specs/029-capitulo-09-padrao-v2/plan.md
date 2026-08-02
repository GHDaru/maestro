# Plan 029 — Capítulo 09 no padrão v2

- **Spec**: `spec.md` · **Raia**: leve · **Data**: 2026-08-02

## Constitution Check (principios-maestro.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven | ✅ spec antes da edição, requisitos em EARS |
| II. Orquestração humano-governada | ✅ o capítulo delimita o que fica com o humano |
| III. Reversibilidade / gates de risco | ✅ bloco de reversibilidade citado na regra vigente |
| IV. Test-First / DoD verificável | ✅ é o tema; a segunda lei entra com caso real |
| V. Economia de contexto / fronteira | ✅ um capítulo por ciclo |
| VI. Artefatos vivos | ✅ datação; inventário de portões medido na hora |
| VII. Governança leve / YAGNI | ✅ cobertura como meta segue rejeitada, com motivo |
| VIII. Comunicação inteligível | ✅ DoD e DoR por extenso; nomes em português |

## Como

1. Inventariar os portões por comando (`ls scripts/verificar-*.sh`, `grep -c process.exit(1)`,
   suíte do companion) antes de escrever.
2. Trazer a segunda lei para o corpo do capítulo — ela é de 2026-08-01 (ciclo 017) e o
   capítulo era anterior.
3. Ligar o limite do verde ao dado do capítulo 02 (nove defeitos escapados) e nomear a
   resposta certa: ampliar a família coberta (anti-padrão 16), não "revisar melhor".

## Verificação (DoD)

```bash
scripts/verificar-capitulos.sh
ls scripts/verificar-*.sh | wc -l          # 4
grep -c "process.exit(1)" publicar/build.mjs   # 2
cd companion && python3 -m pytest -q       # 11 passed
node publicar/build.mjs
```
