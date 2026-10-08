---
gate: G3
papel: runner2
objeto: painel/entrada/saida.py @ 5fb3557
veredito: OK
por: W13
data: 2026-10-08 15:19 -0300
data_objeto: 2026-10-08 14:40:09 -0300
numeros: "pytest 63/0/0 (painel/); pytest global 73/1/0 (falha anterior, presente em 48ffd83, exclusão pendente da Office)"
---

# G3 runner2 — 068 P2 @ 5fb3557

Objeto: painel/entrada/saida.py @ 5fb3557

## Veredito: OK

0 failed, 0 errors na suíte relevante (painel/). A 1 falha global é anterior à trilha 068, presente em 48ffd83 (base sem 068), exclusão pendente da Office.

## Evidência (runner2, clone limpo)

### pytest — suíte painel/ (068 P2) @ 5fb3557
```
63 passed, 0 failed, 0 errors
```
✓

### pytest — global @ 5fb3557
```
73 passed, 1 failed, 0 errors
FAILED companion/backend/tests/test_smoke.py::test_corpus_cobre_todas_as_paginas_do_livro
```
A falha: `corpus desatualizado — Páginas ausentes: ['Catálogo do ecossistema']`.

### pytest — smoke test @ 48ffd83 (base, sem 068)
```
1 failed
FAILED companion/backend/tests/test_smoke.py::test_corpus_cobre_todas_as_paginas_do_livro
AssertionError: corpus desatualizado — Páginas ausentes: ['Catálogo do ecossistema']
```
Mesma falha em 48ffd83 (base sem 068). É falha anterior, não introduzida pela trilha 068. Exclusão pendente da Office.

## Clones
- 5fb3557: clone limpo /tmp/maestro-068 no runner2
- 48ffd83: bundle w08/068-p2 → /dev/shm/maestro-base no runner2
