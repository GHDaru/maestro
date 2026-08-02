# Spec 028 — Capítulo 08 (entregáveis e artefatos) no padrão v2

- **Status**: Concluída · **Raia**: leve · **Data**: 2026-08-02
- **Origem**: cadência de migração didática (um capítulo por ciclo).

## O quê e por quê

O capítulo definia o critério certo — consumidor + forcing function, ou imutabilidade — e
não mostrava **nenhum dos nossos artefatos sendo cobrado**. Aqui a evidência é literal: o
gate do changelog está no arquivo da integração contínua, e a imutabilidade dos registros
de decisão é contável por `git log`.

## Requisitos funcionais

- **FR1**: O capítulo DEVE cumprir as nove seções com datação (verificado por script).
- **FR2**: A seção ⭐ DEVE citar a forcing function do changelog **como ela é**, incluindo a
  válvula de escape declarada.
- **FR3**: QUANDO o capítulo afirma que registro de decisão é imutável, O SISTEMA DEVE poder
  contar os commits de cada um e explicar a exceção.
- **FR4**: O capítulo DEVE reportar quantos ciclos têm os quatro artefatos completos, sem
  arredondar para cima.

## Fora de escopo

- Criar artefatos novos · migrar 09–12 (um por ciclo).

## Critérios de aceite (DoD)

- [x] `scripts/verificar-capitulos.sh`: 9 migrados, 4 pendentes, exit 0
- [x] Trecho do gate confere com `.github/workflows/ci.yml`
- [x] Contagem de commits por ADR confere (9 com 1 commit; 0008 com 2, só status)
- [x] 26 de 28 ciclos com os quatro artefatos — número medido, não estimado

## Clarify

1. Contar os dois ciclos incompletos (os abertos agora)? → **sim**, com a explicação.
