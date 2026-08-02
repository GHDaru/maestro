# QA-report 031 — Capítulo 11 no padrão v2

- **Data**: 2026-08-02 · **Raia**: leve · **Veredito**: **APROVADO** (DoD verde)

## Fitness functions (DoD)

| Check | Esperado | Resultado |
|---|---|---|
| `scripts/verificar-capitulos.sh` | exit 0 | ✅ 12 migrados · 1 pendente |
| linha JSON citada × `decisoes.jsonl` | idêntica | ✅ `gate-main-0021b20` |
| `git log --grep="spec 021"` | o commit citado | ✅ `12332c3` |
| commits citando `spec NNN` | 28 | ✅ medido |
| `node publicar/build.mjs` | exit 0 | ✅ |

## Cobertura dos requisitos

- **FR1**: ✅ por script. **FR2**: ✅ cadeia percorrida de trás para frente com dados reais.
- **FR3**: ✅ elo frágil nomeado. **FR4**: ✅ exercício 3 pede o critério verificável.

## Achados

1. **O elo mais usado do repositório é o menos protegido.** A citação `spec NNN` no assunto
   do commit aparece em 28 commits e **nenhum portão a exige**. Sobreviveu por hábito — e a
   lição do ciclo 021 é justamente que hábito é o que falha primeiro. Registrado como
   candidato a portão, com o critério já esboçado no exercício de verificação do capítulo.
2. **Nenhum elo se perdeu até aqui**, o que é bom e enganoso: 28 commits em sete dias, com
   o mesmo operador. A ausência de falha não é evidência de robustez quando a amostra é
   curta e homogênea.

## Pendência de gate

- promoção dev → main aguarda aprovação humana.
