# QA-report 028 — Capítulo 08 no padrão v2

- **Data**: 2026-08-02 · **Raia**: leve · **Veredito**: **APROVADO** (DoD verde)

## Fitness functions (DoD)

| Check | Esperado | Resultado |
|---|---|---|
| `scripts/verificar-capitulos.sh` | exit 0 | ✅ 9 migrados · 4 pendentes |
| trecho do gate × `.github/workflows/ci.yml` | idêntico | ✅ |
| commits por ADR | 9 com 1; `0008` com 2 | ✅ o segundo commit alterou só a linha de status |
| ciclos com os quatro artefatos | 26 de 28 | ✅ os dois restantes são os ciclos em aberto |
| `node publicar/build.mjs` | exit 0 | ✅ |

## Cobertura dos requisitos

- **FR1**: ✅ por script. **FR2**: ✅ gate citado com a válvula `skip-changelog`.
- **FR3**: ✅ exceção investigada antes de afirmada. **FR4**: ✅ 26/28, sem arredondar.

## Achados

1. **Quase publiquei "dez ADRs, dez commits — imutabilidade perfeita".** A contagem mostrou
   dois commits no ADR 0008. Investigar antes de escrever (em vez de omitir a exceção)
   mostrou que a alteração foi na linha de status, não no mérito — e a exceção explicada
   ficou mais forte que a afirmação redonda teria ficado.
2. **O índice de decisões não estava no catálogo do capítulo**, embora seja um dos
   artefatos mais baratos e mais consultados do repositório (38 linhas, nenhuma editada,
   escrita por script). Incluído.

## Pendência de gate

- promoção dev → main aguarda aprovação humana.
