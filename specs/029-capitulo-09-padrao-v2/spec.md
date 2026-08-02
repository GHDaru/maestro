# Spec 029 — Capítulo 09 (DoR/DoD) no padrão v2

- **Status**: Concluída · **Raia**: leve · **Data**: 2026-08-02
- **Origem**: cadência de migração didática (um capítulo por ciclo).

## O quê e por quê

O capítulo da Definição de Pronto (DoD) definia a propriedade certa — verificável
autonomamente — e não mostrava **um único portão nosso**. Além disso, a segunda lei
("prove o check falhando") nasceu depois que o capítulo foi escrito e não estava nele.

## Requisitos funcionais

- **FR1**: O capítulo DEVE cumprir as nove seções com datação (verificado por script).
- **FR2**: A seção ⭐ DEVE inventariar os portões executáveis do repositório com comando.
- **FR3**: O capítulo DEVE ensinar a segunda lei com **caso real** de check provado
  falhando, incluindo o modo que só apareceu por insistência (ciclo 022).
- **FR4**: O capítulo DEVE mostrar o limite do verde com os nove defeitos escapados
  (capítulo 02) e dizer qual é a resposta certa a um escape.

## Fora de escopo

- Criar portões novos · migrar 10–12 (um por ciclo).

## Critérios de aceite (DoD)

- [x] `scripts/verificar-capitulos.sh`: 10 migrados, 3 pendentes, exit 0
- [x] Inventário confere: 4 scripts `verificar-*`, 2 saídas de erro no gerador, 11 testes
- [x] Citação da skill confere com `skills/dod-verificavel/SKILL.md`
- [x] Site sem link quebrado

## Clarify

1. Repetir os nove defeitos do capítulo 02? → **sim**: lá é sintoma medido; aqui é a prova
   de que verde é necessário e não suficiente.
