# QA-report 029 — Capítulo 09 no padrão v2

- **Data**: 2026-08-02 · **Raia**: leve · **Veredito**: **APROVADO** (DoD verde)

## Fitness functions (DoD)

| Check | Esperado | Resultado |
|---|---|---|
| `scripts/verificar-capitulos.sh` | exit 0 | ✅ 10 migrados · 3 pendentes |
| `ls scripts/verificar-*.sh \| wc -l` | 4 | ✅ |
| `grep -c "process.exit(1)" publicar/build.mjs` | 2 | ✅ colisão de endereço e link/imagem |
| suíte do companion | 11 testes verdes | ✅ |
| citação da skill × arquivo | idêntica | ✅ |
| `node publicar/build.mjs` | exit 0 | ✅ |

## Cobertura dos requisitos

- **FR1**: ✅ por script. **FR2**: ✅ seis portões inventariados por comando.
- **FR3**: ✅ segunda lei com o caso do ciclo 022 (quarto modo). **FR4**: ✅ nove defeitos e
  a resposta certa nomeada.

## Achados

1. **O capítulo era anterior à segunda lei.** Ela nasceu no ciclo 017 e ficou só na skill
   por dez ciclos — o livro ensinava a Definição de Pronto sem a regra mais importante que
   tínhamos aprendido sobre ela. É a mesma classe de deriva que o ciclo 021 achou na
   instrução da Inteligência Artificial (IA): a norma evolui e o material que a ensina não.
2. **Candidato para a retro**: não há check que ligue "regra nova numa skill" a "capítulo
   que a ensina". Hoje isso depende de alguém lembrar. Pergunta objetiva registrada: vale
   um portão que compare a data da última regra das skills com a data de revisão dos
   capítulos que as citam?

## Pendência de gate

- promoção dev → main aguarda aprovação humana.
