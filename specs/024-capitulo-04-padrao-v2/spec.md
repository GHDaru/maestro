# Spec 024 — Capítulo 04 (fluxo agentic e contexto) no padrão v2

- **Status**: Concluída · **Raia**: leve · **Data**: 2026-08-02
- **Origem**: cadência de migração didática, um capítulo por ciclo (016, 022, 023, este).

## O quê e por quê

O capítulo 04 explicava bem a teoria — janela finita, acúmulo em vez de falta — e não
mostrava **nada do nosso próprio uso**. É o capítulo em que a evidência é mais fácil de
exibir e estava faltando: os treze subagentes do repositório *são* a economia de contexto
materializada, com tamanho medido e permissão de escrita negada por arquivo.

## Requisitos funcionais

- **FR1**: O capítulo DEVE cumprir as nove seções com datação (verificado por script).
- **FR2**: A seção ⭐ DEVE mostrar a economia de contexto como **medida** — tamanho dos
  agentes e ferramentas declaradas —, não como afirmação.
- **FR3**: QUANDO o capítulo afirma que um papel é somente-leitura, O SISTEMA DEVE poder
  confirmar por comando (`grep "^tools:"`) e pela fitness function `verificar-agentes.sh`.
- **FR4**: O capítulo DEVE registrar o limite honesto: nem todos os treze papéis são
  acionados em todo ciclo.

## Fora de escopo

- Migrar 05–12 (um por ciclo) · instrumentar contagem real de tokens por recorte.

## Critérios de aceite (DoD)

- [x] `scripts/verificar-capitulos.sh`: 5 migrados, 8 pendentes, exit 0
- [x] Números conferidos: 267 linhas totais, 13 agentes, menor com 17 linhas
- [x] `tools:` citados conferem com os arquivos reais
- [x] Site publica sem link quebrado

## Clarify

1. Citar a contagem de menções a agentes nos ciclos, sabendo que ela mostra papéis pouco
   usados? → **sim**: inventário maior que o uso é fato, e o capítulo explica por quê.
