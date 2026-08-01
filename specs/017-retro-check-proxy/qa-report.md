# QA-report 017 — Retrospectiva executada e BPMN

- **Data**: 2026-08-01 · **Raia**: Plena · **Veredito**: ✅ CONFORME

## Fitness functions (DoD)

| Check | Esperado | Resultado |
|---|---|---|
| Anti-padrões no catálogo | 15 | **15** ✅ |
| Leis na `dod-verificavel` | 2 | 2 ✅ |
| Roadmap com F5/F6/F7 + gatilhos | presentes | ✅ |
| BPMN: imagem + página + fonte | 3 artefatos | ✅ |
| Build do site | verde | **35 páginas**, links OK ✅ |

## O que esta retrospectiva encontrou (e por que importa)

Os ciclos 003–016 estavam todos ✅ CONFORME. **Nenhum deles falhou no que verificava** —
falharam no que **não** verificavam. Três achados:

1. **Anti-padrão 13 — check que mede o proxy, não o fato** (3 ocorrências: duas minhas,
   uma no FlowBuilder). Antídoto: provar o check falhando (segunda lei).
2. **Anti-padrão 14 — achado que morre em "candidato"**: escrevi a lição duas vezes sem
   rodar a cerimônia. O ciclo `retro → regra` não é automático; é executado.
3. **Anti-padrão 15 — artefato de planejamento que congela**: o roadmap parou no ciclo 009
   enquanto sete ciclos aconteciam.

## A meta-lição

O processo **não falhou por falta de norma** — falhou por norma sem forcing function. Nos
três casos a regra existia (Princípio IV, Princípio VI, cerimônia de retro) e nada
**barrava** o descumprimento. É a mesma conclusão do capítulo 13 §5.9: o que não tem
forcing function depende de memória, e memória é o que falha primeiro.

**Pendência honesta**: a regra de manter o roadmap vivo hoje é texto no cabeçalho, não
verificação. Se voltar a congelar, vira check (candidato: comparar o maior ciclo em
`specs/` com o maior citado no roadmap) — e desta vez com o gatilho escrito, para não
repetir o anti-padrão 14.

## Gate

- Auditoria do Steward; promovido via `promover-main.sh`.
