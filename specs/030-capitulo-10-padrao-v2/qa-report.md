# QA-report 030 — Capítulo 10 no padrão v2

- **Data**: 2026-08-02 · **Raia**: leve · **Veredito**: **APROVADO** (DoD verde)

## Fitness functions (DoD)

| Check | Esperado | Resultado |
|---|---|---|
| `scripts/verificar-capitulos.sh` | exit 0 | ✅ 11 migrados · 2 pendentes |
| guardas citadas × `promover-main.sh` | conferem | ✅ árvore suja, branch inexistente, sem avanço, confirmação |
| `grep -c '"id": "gate-main'` | 21 | ✅ |
| `node publicar/build.mjs` | exit 0 | ✅ |

## Cobertura dos requisitos

- **FR1**: ✅ por script. **FR2**: ✅ aborto e registro reais.
- **FR3**: ✅ explicado como classe baixa por reversibilidade. **FR4**: ✅ classes não
  exercitadas declaradas no corpo.

## Achados

1. **A seção "6b" era um enxerto.** Entrou no ciclo 008 fora do esqueleto editorial e
   sobreviveu a duas revisões porque ninguém verificava a estrutura. Desde o ciclo 022 o
   script verifica — e foi ele que forçou a decisão de absorvê-la na regra vigente. Segundo
   caso (com o "6b" do capítulo 04) de conteúdo bom em lugar errado, achado pelo mesmo
   portão.
2. **A taxonomia é maior que a experiência.** Quatro das sete classes nunca foram
   exercitadas neste repositório. O capítulo declara isso: catálogo herdado de fonte externa
   sem uso próprio é conhecimento, não evidência — e misturar os dois seria o mesmo erro que
   o livro cobra dos outros.

## Pendência de gate

- promoção dev → main aguarda aprovação humana.
