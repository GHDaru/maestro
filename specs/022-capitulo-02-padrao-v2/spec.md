# Spec 022 — Capítulo 02 no padrão editorial v2

- **Status**: Concluída · **Raia**: leve · **Data**: 2026-08-02
- **Origem**: cadência de migração didática (um capítulo por ciclo, desde o 016) —
  "vamos para o 02", com o método já auto-instalado (ciclo 021).

## O quê e por quê

O capítulo 02 (evidência DORA/SPACE) estava no formato antigo de pesquisa: pergunta,
fundamentação, frameworks, fontes. Bom material, texto que **informa e não ensina** — sem
objetivos, sem exemplo do nosso próprio uso, sem verificação. O guia editorial exige nove
seções e tem Iron Law: *nenhum capítulo publica sem objetivos, exemplo real e verificação*.

E há um segundo problema, de método: no ciclo 016 as nove seções do capítulo 01 foram
contadas **à mão** no relatório de qualidade (QA). Contar à mão funciona uma vez; faltam
dez capítulos. Lei editorial sem executável é lei que depende de memória.

## Requisitos funcionais

- **FR1**: O capítulo 02 DEVE ter as nove seções do guia editorial, na ordem, com o
  cabeçalho de datação (capturado · última revisão · ciclo).
- **FR2**: A seção 6 DEVE trazer evidência **do nosso próprio repositório** — as quatro
  métricas do DORA lidas dos artefatos reais, incluindo a métrica em que vamos mal.
- **FR3**: QUANDO um capítulo tem a estrutura v2, `scripts/verificar-capitulos.sh` DEVE
  cobrar as nove seções na ordem, a datação e a seção 6 com evidência real.
- **FR4**: O script DEVE reportar quantos capítulos ainda faltam migrar, por nome — o
  número de pendentes é fato, não lembrança.
- **FR5**: O reconhecimento de "capítulo migrado" DEVE usar a **estrutura** do arquivo, não
  a frase "migrado ao padrão v2" — texto marcador pode ser apagado e tirar o capítulo do
  check em silêncio.

## Fora de escopo

- Migrar os capítulos 03–12 (um por ciclo, conforme a cadência).
- Instrumentar métricas DORA de verdade (permanece YAGNI — a decisão está no capítulo).

## Critérios de aceite (DoD)

- [x] `scripts/verificar-capitulos.sh` **provado falhando** em quatro modos: seção fora de
      ordem, seção 6 sem a marca ⭐, datação fora do padrão e capítulo que sai do check
- [x] Com o capítulo 02 no padrão, o script sai com código 0 e reporta 3 migrados / 10 pendentes
- [x] Site publica sem link quebrado (`node publicar/build.mjs`)
- [x] Números da seção 6 conferidos no repositório, não estimados

## Clarify

1. O capítulo 13 (piloto, ciclo 013) conta como migrado? → **sim**: tem a estrutura v2. O
   detector é a estrutura, exatamente por isso.
2. Mostrar a métrica ruim? → **sim**. Um capítulo sobre evidência que esconde a própria
   evidência ruim não é capítulo, é folheto.
