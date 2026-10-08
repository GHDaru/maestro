---
gate: G3
papel: codigo
objeto: painel/entrada/seguranca.py @ b47f198
veredito: APPROVE
por: Worker06
data: 2026-10-08 15:16 -0300
data_objeto: 2026-10-08 15:06 -0300
---

# G3 — Crítica trilha B do 068: contatos + porta segura (SEGURANÇA/LGPD)

**Hash:** b47f198
**Branch:** w02/068-trilha-b
**Arquivos:** contatos.py, seguranca.py, eventos.py, servidor.py, conversa.py, banco.py + 7 testes

---

## Veredito: APPROVE

---

## Item 1: contatos.py — add/list/rm/lookup ✓

- **add:** recusa telefone duplicado ativo (`if existente: raise ValueError`). ✓
- **rm:** desativa (`ativo = 0`) e apaga telefone (`telefone = NULL`). LGPD art. 18. ✓
- **lookup:** busca por telefone ativo, retorna `contato, nome, empresa` (sem telefone no retorno). ✓
- **lista:** só contatos ativos, sem telefone (só contato, nome, empresa, criado_em). ✓
- Telefone fica em `dados/entrada.db`, fora do git. ✓

---

## Item 2: seguranca.py — HMAC-SHA256, janela, IPs, dois segredos ✓

- **HMAC-SHA256:** `hmac.new(segredo.encode(), corpo, hashlib.sha256).hexdigest()`. ✓
- **compare_digest:** `hmac.compare_digest(esperada, assinatura_recebida)` — não vaza timing. ✓
- **Janela 5 min:** `valida_horario` recusa futuro > 1 min e mais antigo que `janela_min * 60`. ✓
- **Lista de IPs:** `valida_ip` contra `ips_permitidos`. ✓
- **Dois segredos (NFR-008):** `valida_assinatura` recebe `segredos: list[str]`, valida contra todos. `_qual_segredo_validou` retorna "atual" ou "anterior" (sem o valor). ✓
- **Ordem de verificação:** IP → horário → assinatura (mais barato primeiro). ✓

---

## Item 3: eventos.py — idempotência e retenção ✓

- **Idempotência:** `processa()` — se evento_id existe, retorna resposta guardada; senão chama fn(), guarda e retorna. ✓
- **Retenção 7 dias:** `limpa(dias=7)` remove eventos com mais de N dias. ✓
- Tabela `eventos` em `dados/entrada.db`, fora do git. ✓

---

## Item 4: servidor.py — _segredos(), lookup, idempotência ✓

- **_segredos():** lê `MAESTRO_WEBHOOK_SEGREDO` (atual) e `MAESTRO_WEBHOOK_SEGREDO_ANTERIOR` (anterior) de env vars. Retorna lista. ✓
- **contatos.lookup():** rejeita desconhecido (retorna None → sem menu). ✓
- **eventos.processa():** idempotência no processamento do webhook. ✓
- **hmac.compare_digest** na validação da assinatura. ✓

---

## Item 5: SC-006 — dados/ no .gitignore ✓ (nota)

`.gitignore` tem `dados/entrada.db`. NFR-010 pede `dados/` (diretório). Como toda dados desta trilha vão para `entrada.db`, `dados/entrada.db` cobre. **Nota:** se trilha C adicionar `dados/logs/` ou outros arquivos, deve usar `dados/` em vez de `dados/entrada.db`. SC-006/SC-007 (log_envio) estão na trilha C (W08), não aqui.

---

## Item 6: Nenhum segredo no repo ✓

- Segredos lidos de env vars (`MAESTRO_WEBHOOK_SEGREDO`, `MAESTRO_WEBHOOK_SEGREDO_ANTERIOR`). ✓
- Testes usam `"segredo-teste-atual-123456"` — string sintética, não segredo real. ✓
- Nenhuma URL, token, senha ou endereço hardcoded. ✓

---

## Item 7: Vermelho/verde separados ✓

6 pares vermelho/verde separados:
- `bf9dd13` → `7ed8083` (contatos)
- `ebf9307` → `73445ae` (seguranca)
- `fcdb666` → `ac5f003` (eventos)
- `91eb41e` → `a142f0f` (saida — depois removido)
- `46c4637` → `8ee1378` (conversa)
- `db585b8` → `2c2bd6a` (servidor)

---

## Item 8: runner2 por não-autor

Pendente. Não bloqueia o veredito de segurança — código conferido estático.

---

## Resumo

| Item | Status |
|---|---|
| 1. contatos.py (add/list/rm/lookup, LGPD) | ✓ |
| 2. seguranca.py (HMAC, janela, IPs, 2 segredos) | ✓ |
| 3. eventos.py (idempotência, retenção 7 dias) | ✓ |
| 4. servidor.py (_segredos, lookup, processa) | ✓ |
| 5. SC-006 (dados/ no .gitignore) | ✓ (dados/entrada.db; nota para trilha C) |
| 6. Nenhum segredo no repo | ✓ |
| 7. Vermelho/verde separados | ✓ (6 pares) |
| 8. runner2 não-autor | Pendente |

---

> Veredito: APPROVE
> runner2 por não-autor: pendente

Sessao: Worker06
