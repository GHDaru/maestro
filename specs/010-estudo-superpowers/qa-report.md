# QA-report 010 — Estudo hands-on do Superpowers

- **Data**: 2026-07-31 · **Raia**: Plena · **Veredito**: ✅ CONFORME (estudo; mérito no gate)

## Fitness functions (DoD)

| Check | Esperado | Resultado |
|---|---|---|
| Build do site com o Apêndice B | exit 0, 22 páginas | ✅ 22 páginas, links OK |
| `grep -c "Veredito" apendice-b` | ≥ 6 | **10** ✅ |
| Commit estudado citado (`44c9b2d`) | não-vazio | ✅ |
| Tensão com raias registrada | não-vazio | ✅ |

## Cobertura

- **FR1**: 8 ideias avaliadas + 2 posições mantidas (adoção integral ❌, HARD-GATE ❌),
  cada uma com comparação ao equivalente Maestro e destino concreto.
- **FR2**: no livro (sumário + índice).
- **FR3**: vereditos como proposta — decisão do Steward pendente.

## Nota do ciclo (teste de fogo da vendorização)

Primeiro ciclo pós-009: spec com critério **EARS** e raia classificada saiu direto do
template vendorizado, sem retrabalho de formato. A vendorização se pagou no primeiro uso.

## Pendência de gate

- **T5**: aprovação/amendas dos vereditos (5 absorções propostas: Iron Laws, TDD-para-
  skills, diagnóstico-antes-do-fix, review por task, zero-contexto + enforcement no
  CLAUDE.md) → vira ciclo de incorporação.
