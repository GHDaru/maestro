---
gate: G3
papel: codigo
objeto: painel/entrada/saida.py @ 5fb3557
veredito: APPROVE
por: Worker06
data: 2026-10-08 14:45 -0300
data_objeto: 2026-10-08 14:40 -0300
---

# G3 — Re-crítica P2 do 068: envio assinado e log (SEGURANÇA)

**Hash verde:** 5fb3557
**Hash vermelho:** 027e550
**Branch:** w08/068-p2
**Re-crítica de:** 4c3662a (RETURN sobre a0a319b)

---

## Veredito: APPROVE

Os 3 bloqueantes do RETURN (4c3662a) foram corrigidos em 5fb3557. Vermelho/verde separados. Rito runner2 pendente (não bloqueia o veredito de segurança).

---

## Correção 1: NFR-011/SC-007 — logs só metadados ✓

**Lacuna original:** nenhum logging implementado.

**Correção:** tabela `log_envio` com colunas `id, evento_id, chamado, etapa, timestamp, status, tentativas`. Comentário no código: "SÓ metadados (NFR-011, SC-007). Sem contato (telefone) e sem texto."

- **Sem coluna `contato`** (telefone): ✓
- **Sem coluna `texto`** (mensagem): ✓
- Teste `test_log_nao_tem_coluna_contato`: asserta `contato` e `texto` ausentes das colunas. ✓
- Teste `test_log_registra_metadados`: verifica log com `chamado`, `etapa`, `status`, `timestamp`, `evento_id`. ✓

---

## Correção 2: NFR-010/SC-006 — dados/ no .gitignore ✓

**Lacuna original:** `dados/` ausente do `.gitignore`.

**Correção:** `.gitignore` agora tem `dados/` com comentário "NFR-010, SC-006".

- Teste `test_dados_no_gitignore`: roda `git check-ignore dados/` e asserta return code 0. ✓

---

## Correção 3: NFR-012 — falhou avisa Office ✓

**Lacuna original:** status `falhou` gravado mas sem aviso à Office.

**Correção:** tabela `alertas_office` com `evento_id, chamado, motivo, timestamp, lido`. Função `_avisar_falha()` chamada quando status=`falhou` (linha 199). `alertas_nao_lidos()` devolve alertas não lidos.

- Teste `test_falhou_cria_alerta`: força `MAX_TENTATIVAS` falhas e verifica alerta criado com `chamado="068"`. ✓

---

## Item 1: HMAC-SHA256, segredo em env ✓

Inalterado do a0a319b. `hmac.new(segredo.encode(), corpo, hashlib.sha256).hexdigest()`. Segredo de `os.environ.get("MAESTRO_HMAC_SEGREDO")`. Sem hardcoded. ✓

---

## Item 2: Retry 1/5/15/60, max 10/24h ✓

Inalterado. `ESPERAS = [60, 300, 900, 3600]`, `MAX_TENTATIVAS = 10`, `MAX_IDADE_SEGUNDOS = 24*3600`. ✓

---

## Item 5: Nenhum segredo no repo ✓

Tudo em env vars. Testes usam `"segredo"` como string de teste. ✓

---

## Rito

### Vermelho/verde separados ✓

- Vermelho (027e550): só testes (3 arquivos, 402 linhas). ImportError esperado. ✓
- Verde (5fb3557): implementação (6 arquivos, 574 linhas). ✓

### runner2 por não-autor

Pendente. Não bloqueia o veredito de segurança — o código foi conferido estático.

---

## Resumo

| Item | RETURN (4c3662a) | Correção (5fb3557) | Re-crítica |
|---|---|---|---|
| 1. HMAC-SHA256 | ✓ | — | ✓ |
| 2. Retry 10/24h | ✓ parcial | `_avisar_falha()` + `alertas_office` | ✓ |
| 3. Logs metadados (NFR-011) | ✗ bloqueante | `log_envio` sem contato/texto + teste | ✓ |
| 4. dados/ .gitignore (NFR-010) | ✗ bloqueante | `dados/` no .gitignore + teste | ✓ |
| 5. Sem segredos | ✓ | — | ✓ |
| Rito: vermelho/verde | ✗ | 027e550 + 5fb3557 separados | ✓ |
| Rito: runner2 | Pendente | — | Pendente |

---

> Veredito: APPROVE
> Re-crítica de: 4c3662a (RETURN sobre a0a319b)
> runner2 por não-autor: pendente

Sessao: Worker06
