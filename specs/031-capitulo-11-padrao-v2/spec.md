# Spec 031 — Capítulo 11 (rastreabilidade) no padrão v2

- **Status**: Concluída · **Raia**: leve · **Data**: 2026-08-02
- **Origem**: cadência de migração didática (um capítulo por ciclo).

## O quê e por quê

O capítulo defendia que a rastreabilidade **emerge** do fluxo e não mostrava um único elo
nosso. O repositório tem a cadeia inteira funcionando — linha de gate → commit → ciclo →
registro de decisão — e tem também um elo frágil que ninguém tinha nomeado: a citação
`spec NNN` na mensagem de commit é convenção, não portão.

## Requisitos funcionais

- **FR1**: O capítulo DEVE cumprir as nove seções com datação (verificado por script).
- **FR2**: A seção ⭐ DEVE percorrer a cadeia **de trás para frente**, com dado real de cada
  elo (linha do índice, commit, pasta do ciclo, registro de decisão).
- **FR3**: O capítulo DEVE nomear o elo que depende de hábito e registrá-lo como candidato a
  portão — em vez de apresentá-lo como virtude.
- **FR4**: A pergunta de verificação DEVE pedir ao leitor o critério verificável que
  transformaria essa convenção em portão.

## Fora de escopo

- Criar o portão da convenção de commit (vira ciclo próprio se o Steward quiser) ·
  migrar o capítulo 12.

## Critérios de aceite (DoD)

- [x] `scripts/verificar-capitulos.sh`: 12 migrados, 1 pendente, exit 0
- [x] A linha JSON citada é idêntica à do `docs/registro/decisoes.jsonl`
- [x] `git log --grep="spec 021"` devolve o commit citado
- [x] 28 commits citam `spec NNN` — número medido

## Clarify

1. Apresentar a convenção frágil no capítulo que a defende? → **sim**: o capítulo perde
   força se esconder que o elo mais citado depende de memória.
