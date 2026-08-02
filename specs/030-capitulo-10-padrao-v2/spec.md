# Spec 030 — Capítulo 10 (gates e classes de risco) no padrão v2

- **Status**: Concluída · **Raia**: leve · **Data**: 2026-08-02
- **Origem**: cadência de migração didática (um capítulo por ciclo).

## O quê e por quê

O capítulo dos gates tinha a taxonomia completa e nenhum gate nosso à vista. Ele também
carregava uma seção "6b" (gates dentro da tarefa) enxertada depois, fora do esqueleto
editorial — e não dizia que **a maior parte da taxonomia nunca foi exercitada** aqui.

## Requisitos funcionais

- **FR1**: O capítulo DEVE cumprir as nove seções com datação (verificado por script).
- **FR2**: A seção ⭐ DEVE mostrar o gate de merge como script que **se recusa a decidir**,
  com saída real de aborto e de registro.
- **FR3**: O capítulo DEVE explicar por que promovemos com frequência sem dupla aprovação —
  classe baixa por reversibilidade, não gate frouxo.
- **FR4**: O capítulo DEVE declarar quais classes da taxonomia **nunca** foram exercitadas
  neste repositório.

## Fora de escopo

- Mudar a taxonomia · migrar 11–12 (um por ciclo).

## Critérios de aceite (DoD)

- [x] `scripts/verificar-capitulos.sh`: 11 migrados, 2 pendentes, exit 0
- [x] Guardas citadas conferem com `scripts/promover-main.sh`
- [x] 21 gates de merge registrados — número medido
- [x] Site sem link quebrado

## Clarify

1. Manter a seção "6b" (gate dentro da tarefa)? → **não** como seção fora do esqueleto; a
   ideia entra como regra vigente ("fases com gate valem em qualquer granularidade").
