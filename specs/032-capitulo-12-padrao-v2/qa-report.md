# QA-report 032 — Capítulo 12 no padrão v2 (migração encerrada)

- **Data**: 2026-08-02 · **Raia**: leve · **Veredito**: **APROVADO** (DoD verde)

## Fitness functions (DoD)

| Check | Esperado | Resultado |
|---|---|---|
| `scripts/verificar-capitulos.sh` | 13 migrados, **0 pendentes** | ✅ `pendentes: 0 (nenhum)` |
| `git log -- principios-maestro.md` | três toques | ✅ 2026-07-27, 07-28, 08-01 |
| seção "o que NÃO adotamos" | citada como está | ✅ confere com o modelo §10 |
| `node publicar/build.mjs` | exit 0 | ✅ 35 páginas |

## Cobertura dos requisitos

- **FR1**: ✅ por script. **FR2**: ✅ duas forças medidas. **FR3**: ✅ caso do ciclo 021.
- **FR4**: ✅ achados abertos no corpo. **FR5**: ✅ zero pendentes.

## Achados

1. **A migração fechou com o mesmo padrão em todos os treze capítulos**: em nenhum deles
   faltava teoria — faltava a evidência do próprio uso. Onze capítulos foram migrados em
   onze ciclos, e em nove deles a seção ⭐ trouxe pelo menos um número que ninguém tinha
   medido antes.
2. **Dois enxertos fora do esqueleto foram achados pelo script** (as seções "6b" dos
   capítulos 04 e 10), ambos incorporados no lugar certo. Nenhum humano os tinha notado em
   revisões anteriores.
3. **Achados abertos, herdados dos ciclos e agora publicados no livro**: retrospectiva sem
   gatilho (027), régua de raias mal aplicada — 19 plena × 2 leve (023), elo de commit sem
   portão (031) e ausência de check ligando regra nova ao capítulo que a ensina (029). Os
   quatro estão registrados com pergunta objetiva; nenhum foi transformado em regra ainda.

## Pendência de gate

- promoção dev → main aguarda aprovação humana.
