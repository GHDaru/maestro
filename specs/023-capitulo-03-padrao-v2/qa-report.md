# QA-report 023 — Capítulo 03 no padrão editorial v2

- **Data**: 2026-08-02 · **Raia**: leve · **Veredito**: **APROVADO** (DoD verde)

## Fitness functions (DoD)

| Check | Esperado | Resultado |
|---|---|---|
| `scripts/verificar-capitulos.sh` | exit 0, 4 migrados | ✅ `4 migrados · 9 pendentes` (listados por nome) |
| `grep -l "O SISTEMA DEVE" specs/*/spec.md \| wc -l` | o número citado no capítulo | ✅ 14 |
| `grep -h "Raia\*\*:" specs/*/spec.md \| sort \| uniq -c` | a distribuição citada | ✅ 19 plena · 2 leve · 1 esqueleto não preenchido |
| Trecho de código citado × arquivo real | idêntico em comportamento | ✅ confere com `scripts/verificar-instalacao.sh` |
| `node publicar/build.mjs` | exit 0 | ✅ 35 páginas + sumário |

## Cobertura dos requisitos

- **FR1** (nove seções + datação): ✅ por script.
- **FR2** (EARS ponta a ponta): ✅ FR3 do ciclo 021 → laço do check → saída vermelha real.
- **FR3** (números reproduzíveis): ✅ todos por comando; nenhum estimado.
- **FR4** (dado desconfortável): ✅ 19 plena × 2 leve publicado no capítulo.

## Achados

1. **Escrevi uma afirmação plausível e falsa** — a primeira versão da seção 6 dizia que as
   correções de texto entravam como raia leve, "com o pull request servindo de artefato".
   Soava certo e batia com a norma; o comando mostrou 19 plena contra 2 leve, e **todas**
   as 22 têm spec própria. Corrigido antes de publicar. É o anti-padrão 7 ("parece que
   funciona") aplicado a prosa: afirmação sobre o método precisa de caminho ou comando,
   como manda o guia editorial §3.
2. **Achado para a retrospectiva — a régua de raias não está sendo aplicada.** Com 19 de 22
   specs em plena, ou o trabalho é todo de raio largo (improvável: houve ajuste de tema e
   correção de texto), ou marcar "plena" virou hábito. Sem dono, isso vira o anti-padrão 14
   ("achado que morre em candidato"), então fica **registrado com pergunta objetiva**: nas
   próximas cinco specs, qual raia cada uma teria se a régua fosse aplicada friamente?

## Pendência de gate

- promoção dev → main aguarda aprovação humana.
