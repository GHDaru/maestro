# Spec 025 — Capítulo 05 (orquestração) no padrão v2

- **Status**: Concluída · **Raia**: leve · **Data**: 2026-08-02
- **Origem**: cadência de migração didática (um capítulo por ciclo).

## O quê e por quê

O capítulo dos padrões de orquestração listava seis padrões e não dizia **quais nós
usamos**. Um catálogo sem uso vira vitrine: o leitor sai sabendo os nomes e sem saber
escolher. E o dado mais útil que temos é justamente o negativo — em 25 ciclos, o padrão
autônomo nunca foi usado, e o encadeamento fixo respondeu por quase tudo.

## Requisitos funcionais

- **FR1**: O capítulo DEVE cumprir as nove seções com datação (verificado por script).
- **FR2**: A seção ⭐ DEVE dizer **quais** padrões foram usados no repositório e quais não,
  com evidência por comando.
- **FR3**: QUANDO o capítulo cita o laço avaliador-otimizador, O SISTEMA DEVE poder listar
  os ciclos que documentaram portão provado falhando.
- **FR4**: O capítulo DEVE retomar o achado das raias (roteamento que não roteia) em vez de
  apresentá-las como se funcionassem bem.

## Fora de escopo

- Mudar a política de orquestração · migrar 06–12 (um por ciclo).

## Critérios de aceite (DoD)

- [x] `scripts/verificar-capitulos.sh`: 6 migrados, 7 pendentes, exit 0
- [x] Lista de comandos citada confere com `ls .claude/commands/`
- [x] Os quatro ciclos citados conferem com `grep -rli "prova.* falhando" specs/*/qa-report.md`
- [x] Site sem link quebrado

## Clarify

1. Vitrine de padrões ou uso real? → **uso real**, incluindo o que nunca foi usado.
