# QA-report 022 — Capítulo 02 no padrão editorial v2

- **Data**: 2026-08-02 · **Raia**: leve · **Veredito**: **APROVADO** (DoD verde)

## Fitness functions (DoD)

| Check | Esperado | Resultado |
|---|---|---|
| `verificar-capitulos.sh` — seção fora de ordem | exit 1 | ✅ `seção 2 é 'Contexto geral', esperada 'O problema'` |
| `verificar-capitulos.sh` — seção 6 sem ⭐ | exit 1 | ✅ `falta a seção 6 marcada '⭐ Na prática'` |
| `verificar-capitulos.sh` — datação fora do padrão | exit 1 | ✅ `cabeçalho de datação fora do padrão` |
| `verificar-capitulos.sh` — estado atual | exit 0 | ✅ `3 migrados · 10 pendentes` (listados por nome) |
| `node publicar/build.mjs` | exit 0 | ✅ 35 páginas + sumário, links OK |
| Números da seção 6 | conferidos no repo | ✅ 17 gates (`grep -c`), 9 itens em `Fixed`, 0 reversões (`git log --grep`) |

## Cobertura dos requisitos

- **FR1** (nove seções + datação): ✅ verificado por script, não por leitura.
- **FR2** (evidência própria, inclusive a ruim): ✅ change fail rate declarado como a nossa
  métrica pior — ~1 defeito escapado a cada 2 entregas — com o padrão por trás dos nove
  (nenhum pego por revisão; todos por check escrito depois).
- **FR3/FR4** (script cobra e reporta pendentes): ✅.
- **FR5** (detecção estrutural): ✅ trocado após o quarto modo de falha aparecer.

## Achados

1. **O check quase mediu o proxy — de novo.** A primeira versão reconhecia capítulo
   migrado pela frase "migrado ao padrão v2". Ao provar o modo "datação fora do padrão", o
   capítulo simplesmente **saiu do check** (a frase morava na linha alterada) e o script
   deu verde. Anti-padrão 13, quarta reincidência; o antídoto do anti-padrão 16 —
   enumerar a família e provar em **cada** modo — foi o que expôs o defeito. Corrigido:
   detecção pela estrutura (`## 1. Objetivos`).
2. **A Iron Law editorial existia desde o ciclo 013 sem executável.** O capítulo 01
   (ciclo 016) foi conferido à mão no relatório de qualidade (QA). Agora a lei é script,
   e o número de pendentes é saída de comando.

## Pendência de gate

- promoção dev → main aguarda aprovação humana.
