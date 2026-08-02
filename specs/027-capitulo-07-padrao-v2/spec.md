# Spec 027 — Capítulo 07 (cerimônias e cadência) no padrão v2

- **Status**: Concluída · **Raia**: leve · **Data**: 2026-08-02
- **Origem**: cadência de migração didática (um capítulo por ciclo).

## O quê e por quê

O capítulo dizia que a retrospectiva é a cerimônia de maior retorno com agentes e não
mostrava **nenhuma retro nossa**. A evidência existe e é datada: o catálogo de anti-padrões
cresceu em quatro levas, cada uma com o ciclo de origem no histórico do arquivo — inclusive
o anti-padrão 14, que nasceu justamente de duas retros **não executadas**.

## Requisitos funcionais

- **FR1**: O capítulo DEVE cumprir as nove seções com datação (verificado por script).
- **FR2**: A seção ⭐ DEVE mostrar a retrospectiva **produzindo regra versionada**, com o
  histórico do arquivo como evidência.
- **FR3**: QUANDO o capítulo afirma que o trabalho em curso é um, O SISTEMA DEVE poder
  confirmar por comando (`git branch -a`).
- **FR4**: O capítulo DEVE nomear as cerimônias em português (Princípio VIII) sem perder o
  vínculo com os nomes de origem.

## Fora de escopo

- Mudar a cadência · migrar 08–12 (um por ciclo).

## Critérios de aceite (DoD)

- [x] `scripts/verificar-capitulos.sh`: 8 migrados, 5 pendentes, exit 0
- [x] O histórico citado confere com `git log -- skills/anti-padroes/SKILL.md`
- [x] `git branch -a` devolve apenas `dev` e `main`
- [x] Site sem link quebrado

## Clarify

1. Mostrar que a retro só foi executada uma vez em 26 ciclos? → **sim**: é o que dá sentido
   ao anti-padrão 14, e esconder isso enfraqueceria a própria regra.
