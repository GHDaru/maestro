# Spec 023 — Capítulo 03 (Spec-Driven) no padrão editorial v2

- **Status**: Concluída · **Raia**: leve · **Data**: 2026-08-02
- **Origem**: cadência de migração didática, um capítulo por ciclo (016, 022, este).

## O quê e por quê

O capítulo que explica **por que existe spec** era o mais irônico do livro: estava no
formato antigo de pesquisa, sem objetivos, sem exemplo próprio e sem verificação — ou
seja, não seguia a norma que ele mesmo defende.

Há também uma dívida de conteúdo: EARS (*Easy Approach to Requirements Syntax*, sintaxe
simples para requisitos) foi absorvido no ciclo 008 (ADR 0008) e o capítulo não explicava
o que é nem mostrava uma frase virando executável.

## Requisitos funcionais

- **FR1**: O capítulo 03 DEVE cumprir as nove seções do guia editorial, com datação —
  verificado por `scripts/verificar-capitulos.sh`, não por leitura.
- **FR2**: O capítulo DEVE explicar EARS com uma frase real do repositório e mostrar o
  caminho **spec → executável → primeira execução**.
- **FR3**: QUANDO o capítulo cita número do próprio repositório, O SISTEMA DEVE ser capaz
  de reproduzi-lo por comando (nada estimado).
- **FR4**: O capítulo DEVE expor o dado desconfortável da própria operação sobre raias, se
  houver — evidência que só mostra o lado bom não é evidência.

## Fora de escopo

- Migrar os capítulos 04–12 (um por ciclo).
- Reclassificar as specs antigas de plena para leve — o achado vai à retrospectiva, não
  vira reescrita retroativa de registro.

## Critérios de aceite (DoD)

- [x] `scripts/verificar-capitulos.sh` sai com código 0 e conta 4 migrados / 9 pendentes
- [x] Números conferidos por comando: 14 specs em EARS, 22 specs, 19 plena × 2 leve
- [x] Trecho de código citado confere com `scripts/verificar-instalacao.sh`
- [x] Site publica sem link quebrado

## Clarify

1. Mostrar a distribuição de raias, sabendo que ela nos desabona? → **sim** (FR4). Um
   capítulo sobre honestidade de especificação não pode maquiar a própria amostra.
