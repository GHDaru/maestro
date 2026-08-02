# Plan 022 — Capítulo 02 no padrão editorial v2

- **Spec**: `spec.md` · **Raia**: leve · **Data**: 2026-08-02

## Constitution Check (principios-maestro.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven | ✅ spec antes da edição; requisitos em EARS (*Easy Approach to Requirements Syntax*) |
| II. Orquestração humano-governada | ✅ o script cobra o esqueleto; o mérito do texto continua humano |
| III. Reversibilidade / gates de risco | ✅ edição de documento, reversível por `git revert` |
| IV. Test-First / DoD verificável | ✅ `verificar-capitulos.sh` provado falhando em quatro modos antes de valer |
| V. Economia de contexto / fronteira | ✅ um capítulo por ciclo; o script é um arquivo de responsabilidade única |
| VI. Artefatos vivos | ✅ datação obrigatória verificada; pendentes listados por nome a cada execução |
| VII. Governança leve / YAGNI | ✅ 50 linhas de shell; nenhum linter de Markdown adotado |
| VIII. Comunicação inteligível | ✅ IA, DORA, DoD e QA por extenso na primeira ocorrência de cada texto |

## Como

1. **Ler o guia editorial antes de escrever** (§2 esqueleto, §3 regras, §4 datação) e o
   capítulo 01 como referência de tom.
2. **Levantar a evidência real antes da prosa** — a seção 6 é a marca do livro, então os
   números vêm do repositório: gates no índice de decisões, defeitos em `Fixed` no
   changelog, ausência de reversões no histórico. Nada estimado.
3. **Escrever o capítulo** preservando o conteúdo técnico que já estava certo (as quatro
   métricas, os quatro frameworks avaliados, a analogia da linha de produção cognitiva) e
   acrescentando o que faltava: objetivos, problema, ideia central, regra vigente, prática,
   anti-padrões, verificação e "o que roubar".
4. **Transformar a Iron Law editorial em executável** (`verificar-capitulos.sh`), provando
   cada modo de falha — inclusive o modo que só apareceu ao provar: capítulo que **sai** do
   check quando perde a frase marcadora. Trocado por detecção estrutural.

## Verificação (DoD)

```bash
scripts/verificar-capitulos.sh    # 3 migrados, 10 pendentes por nome, exit 0
node publicar/build.mjs           # site sem link quebrado
grep -c '"id": "gate-main' docs/registro/decisoes.jsonl   # o 17 citado no capítulo
git log --grep=revert -i --oneline | wc -l                # o zero citado no capítulo
```
