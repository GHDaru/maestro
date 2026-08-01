# QA-report 014 — Navegação em cinco trilhas

- **Data**: 2026-08-01 · **Raia**: Plena · **Veredito**: ✅ CONFORME

## Fitness functions (DoD)

| Check | Esperado | Resultado |
|---|---|---|
| Build do site | ≥34 páginas, links OK | **34** ✅ |
| Colisão de slug injetada | build falha (exit ≠ 0) e lista | exit **1**, colisão listada ✅ |
| `grep -c '"tipo"' sumario.json` | 5 | 5 ✅ |
| Páginas de README distintas | 5 (jornada, handbook, receitas, adr, registro) | 5 ✅ |
| `blob/main` na capa | 0 | 0 ✅ |
| Link externo na capa | 1 (deliberado, "ver no GitHub") | 1 ✅ |

## Cobertura

FR1–FR5 entregues. Fora de escopo respeitado: companion, migração dos capítulos 01–12,
Jornada em formato longo.

## Defeito encontrado e corrigido no ciclo

Ao criar a quinta trilha, os cinco `README.md` do livro passaram a colidir no mesmo slug
(`readme.html`) — a última página sobrescrevia as anteriores **em silêncio**, e o portão
de links não pegava (o alvo existia). Causa raiz: slug derivado apenas do nome do arquivo,
em duas funções distintas (item e resolvedor de links). Correção: `README.md`/`index.md`
usam o diretório pai; o resolvedor resolve o caminho relativo antes de derivar. Adicionada
a **fitness function** que faltava — testada com colisão deliberada.

**Lição para a retrospectiva**: o portão de links verificava se o alvo *existe*, não se
cada origem tem página *própria*. Verificação de existência ≠ verificação de unicidade.

## Gate

- Aprovação do Steward ("siga com o 014"); promovido via `promover-main.sh`.
