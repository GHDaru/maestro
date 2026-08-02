# Spec 032 — Capítulo 12 (governança leve) no padrão v2 — fecha a migração

- **Status**: Concluída · **Raia**: leve · **Data**: 2026-08-02
- **Origem**: cadência de migração didática — **último** capítulo pendente.

## O quê e por quê

O capítulo da governança defendia duas forças (aprender e podar) sem mostrar nenhuma das
duas acontecendo aqui. As duas são visíveis no histórico: a constituição mudou três vezes
em 32 ciclos enquanto a periferia executável cresceu para seis skills e dez scripts; e a
poda tem seção própria no modelo operacional, com três registros de decisão dedicados a
**descartar** coisas.

Este ciclo também **fecha a cadência**: com ele, os treze capítulos ficam no padrão v2.

## Requisitos funcionais

- **FR1**: O capítulo DEVE cumprir as nove seções com datação (verificado por script).
- **FR2**: A seção ⭐ DEVE mostrar as duas forças com dado real — frequência de mudança do
  núcleo × crescimento da periferia, e a lista do que foi recusado.
- **FR3**: O capítulo DEVE mostrar a governança se auditando (o caso do princípio VIII sem
  linha no Constitution Check, ciclo 021).
- **FR4**: O capítulo DEVE declarar os achados ainda abertos (retro sem gatilho; régua de
  raias mal aplicada) em vez de encerrar com conclusão limpa.
- **FR5**: QUANDO este ciclo terminar, `scripts/verificar-capitulos.sh` DEVE reportar
  **zero pendentes**.

## Fora de escopo

- Resolver os achados abertos (viram ciclos próprios, se o Steward quiser).

## Critérios de aceite (DoD)

- [x] `scripts/verificar-capitulos.sh`: 13 migrados, **0 pendentes**, exit 0
- [x] Histórico da constituição citado confere com `git log`
- [x] Citação da seção "o que NÃO adotamos" confere com o modelo operacional
- [x] Site sem link quebrado

## Clarify

1. Encerrar o livro com achados abertos? → **sim**: um capítulo sobre governança que
   aprende não pode terminar fingindo que não há o que aprender.
