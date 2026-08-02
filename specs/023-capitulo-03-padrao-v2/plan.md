# Plan 023 — Capítulo 03 no padrão editorial v2

- **Spec**: `spec.md` · **Raia**: leve · **Data**: 2026-08-02

## Constitution Check (principios-maestro.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven | ✅ spec antes da edição; requisitos em EARS |
| II. Orquestração humano-governada | ✅ texto proposto pela IA, mérito e gate do humano |
| III. Reversibilidade / gates de risco | ✅ edição de documento; `git revert` desfaz |
| IV. Test-First / DoD verificável | ✅ o esqueleto é cobrado por script (ciclo 022), não por leitura |
| V. Economia de contexto / fronteira | ✅ um capítulo por ciclo |
| VI. Artefatos vivos | ✅ datação obrigatória; números reproduzíveis por comando |
| VII. Governança leve / YAGNI | ✅ nenhuma ferramenta nova |
| VIII. Comunicação inteligível | ✅ EARS, IA, ADR e DoD por extenso na primeira ocorrência |

## Como

1. Levantar os números **antes** de escrever a seção 6 (`grep -l "O SISTEMA DEVE"`,
   distribuição de raias nas specs) — e desconfiar de afirmação bonita: a primeira versão
   do parágrafo dizia que as correções entravam como raia leve; o comando mostrou 19 plena
   contra 2 leve, e o texto passou a dizer isso.
2. Escolher **um** requisito e segui-lo do começo ao fim (FR3 do ciclo 021 → laço no
   `verificar-instalacao.sh` → saída vermelha da primeira execução). Um caminho completo
   ensina mais que cinco exemplos truncados.
3. Preservar o conteúdo técnico correto do capítulo antigo (inversão de dependência, raias,
   tabela de ferramentas) e acrescentar o que faltava: objetivos, problema, ideia central,
   regra vigente, anti-padrões, verificação e "o que roubar".

## Verificação (DoD)

```bash
scripts/verificar-capitulos.sh                        # 4 migrados, 9 pendentes, exit 0
grep -l "O SISTEMA DEVE" specs/*/spec.md | wc -l      # 14, o número citado
grep -h "Raia\*\*:" specs/*/spec.md | sort | uniq -c  # 19 plena × 2 leve
node publicar/build.mjs                               # site sem link quebrado
```
