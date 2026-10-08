---
gate: G2
papel: criterio
objeto: painel/tests/test_entrada_orquestrador.py @ 027e550
veredito: FALHA_ESPERADA
por: Worker11
data: 2026-10-08 14:53 -0300
data_objeto: 2026-10-08 14:34 -0300
---

# Vermelho G2 — 068 P2 (testes antes do código)

**Commit:** 027e550 (só testes, sem implementação)
**Esperado:** testes falham porque a implementação não existe.

## Saída do pytest (runner2, clone limpo)

```
$ python3 -m pytest painel/tests/test_entrada_etapas.py painel/tests/test_entrada_orquestrador.py painel/tests/test_entrada_nfr.py

Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/lib/python3.12/importlib/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
painel/tests/test_entrada_nfr.py:14: in <module>
    from entrada import saida  # noqa: E402
    ^^^^^^^^^^^^^^^^^^^^^^^^^
E   ModuleNotFoundError: No module named 'entrada'
=========================== short test summary info ============================
ERROR painel/tests/test_entrada_etapas.py
ERROR painel/tests/test_entrada_orquestrador.py
ERROR painel/tests/test_entrada_nfr.py
!!!!!!!!!!!!!!!!!!! Interrupted: 3 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 3 errors in 0.20s ===============================
```

3 errors ModuleNotFoundError — os testes importam `entrada.etapas`,
`entrada.orquestrador`, `entrada.saida` que não existem neste commit.
FALHA_ESPERADA. ✅
