# Plan 030 — Capítulo 10 no padrão v2

- **Spec**: `spec.md` · **Raia**: leve · **Data**: 2026-08-02

## Constitution Check (principios-maestro.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven | ✅ spec antes da edição, requisitos em EARS |
| II. Orquestração humano-governada | ✅ é o tema: o script executa, o humano decide |
| III. Reversibilidade / gates de risco | ✅ o capítulo é a materialização do princípio III |
| IV. Test-First / DoD verificável | ✅ esqueleto por script; guardas conferidas no arquivo |
| V. Economia de contexto / fronteira | ✅ um capítulo por ciclo |
| VI. Artefatos vivos | ✅ datação; a seção "6b" fora do esqueleto foi absorvida na regra |
| VII. Governança leve / YAGNI | ✅ declara o que ainda não foi exercitado, em vez de encenar |
| VIII. Comunicação inteligível | ✅ IA e siglas por extenso; classes nomeadas em português |

## Como

1. Extrair as guardas reais do `promover-main.sh` e a saída de registro de gate.
2. Absorver a seção "6b" (enxerto do ciclo 008) como item da regra vigente — o esqueleto
   editorial não admite seção extra, e a ideia não se perde.
3. Declarar o limite: só as três primeiras classes foram exercitadas.

## Verificação (DoD)

```bash
scripts/verificar-capitulos.sh
grep -n "abortado" scripts/promover-main.sh
grep -c '"id": "gate-main' docs/registro/decisoes.jsonl
node publicar/build.mjs
```
