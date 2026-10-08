---
gate: G3
papel: fluxo
objeto: painel/entrada/etapas.py @ 5fb3557
veredito: APPROVE
por: Worker11
data: 2026-10-08 14:47 -0300
data_objeto: 2026-10-08 14:03 -0300
---

# Veredito G3 — 068 P2 re-crítica (fluxo e texto ao cliente)

**Autor:** W08
**Vermelho:** 027e550 (só testes, 3 errors ImportError — FALHA_ESPERADA)
**Verde:** 5fb3557 (implementação, 45 passed)
**Branch:** w08/068-p2

---

## Rito

### Vermelho + verde separados — ✅

- 027e550: só testes (3 files, 402 insertions). 3 errors ModuleNotFoundError
  (impl não existe) — FALHA_ESPERADA. ✅
- 5fb3557: implementação (6 files, 574 insertions). 45 passed. ✅

### runner2 não-autor (clone limpo) — ✅

Vermelho (027e550):
```
3 errors in 0.20s (ModuleNotFoundError: No module named 'entrada')
```

Verde (5fb3557):
```
45 passed in 6.76s
```

0 failed, 0 errors no verde. Clone limpo de bundle `--all` + checkout. ✅

### Segredos/telefone/nome real — ✅

Sem segredos, sem telefones reais, sem e-mails de cliente. ✅

---

## Conferência do fluxo e texto

### 1. As 6 etapas sem jargão (FR-008) — ✅

`etapas.py` inalterado desde a primeira entrega (a0a319b). 6 etapas em
português plain, numeradas 1–6. `texto_e_seguro()` verifica todos os
padrões proibidos (P2-AC2). ✅

### 2. As 3 exceções — ✅

`TEXTOS_EXCECAO`: aguardando_informacao, nao_aprovado, recuo.
Recuo G6→G3 com `mensagem_cliente` e `RECUO_PADRAO`. ✅

### 3. Orquestrador — ✅

`orquestrador.py` inalterado. Primeira notificação, mesma etapa (não
reenvia), avanço, recuo — todos testados. ✅

### 4. Agendador Windows 5 min — ✅

`agendador.cmd` inalterado. `schtasks /sc minute /mo 5`. ✅

---

## Correções do RETURN do W06 (não-fluxo, conferidas)

### NFR-011/SC-007 — logs só metadados — ✅

`test_entrada_nfr.py::TestLogSoMetadados`:
- `test_log_registra_metadados`: log tem horário, rota, evento_id, status. ✅
- `test_log_nao_tem_coluna_contato`: tabela `log_envio` sem coluna contato/texto. ✅

### NFR-010/SC-006 — dados/ no .gitignore — ✅

`test_entrada_nfr.py::TestDadosGitignore::test_dados_no_gitignore`:
`git check-ignore` confirma `dados/` ignorado. `.gitignore` com 3 linhas
novas. ✅

### NFR-012 — falhou avisa Office — ✅

`test_entrada_nfr.py::TestFalhouAvisaOffice::test_falhou_cria_alerta`:
mensagem `falhou` cria registro na tabela `alerta_office`. ✅

---

## Veredito: APPROVE

Vermelho+verde separados (027e550 + 5fb3557). Fluxo/texto inalterado e já
aprovado. Correções do W06 (NFR-010/011/012) testadas e passando. runner2
45 passed, 0 failed, 0 errors. Sem segredos.
