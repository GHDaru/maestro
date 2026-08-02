# QA-report 027 — Capítulo 07 no padrão v2

- **Data**: 2026-08-02 · **Raia**: leve · **Veredito**: **APROVADO** (DoD verde)

## Fitness functions (DoD)

| Check | Esperado | Resultado |
|---|---|---|
| `scripts/verificar-capitulos.sh` | exit 0 | ✅ 8 migrados · 5 pendentes |
| `git log -- skills/anti-padroes/SKILL.md` | as quatro levas citadas | ✅ specs 008, 011, 017, 020 |
| `git branch -a` | só `dev` e `main` | ✅ |
| `node publicar/build.mjs` | exit 0 | ✅ |

## Cobertura dos requisitos

- **FR1**: ✅ por script. **FR2**: ✅ histórico do arquivo como prova da regra versionada.
- **FR3**: ✅ comando confirma. **FR4**: ✅ cerimônias em português com origem preservada.

## Achados

1. **A retro de fato só foi executada uma vez em 26 ciclos** (ciclo 017), e ela nasceu de
   uma cobrança do Steward, não do calendário. O capítulo publica isso porque é a origem do
   anti-padrão 14 — a cerimônia mais valiosa era também a mais adiada.
2. **Candidato a próxima retro**: a cadência de retrospectiva não tem gatilho. Hoje ela
   acontece quando alguém percebe; o método não define "a cada N ciclos" nem tem check que
   acuse a ausência. Registrado com pergunta objetiva: qual gatilho — número de ciclos,
   número de achados abertos ou ambos?

## Pendência de gate

- promoção dev → main aguarda aprovação humana.
