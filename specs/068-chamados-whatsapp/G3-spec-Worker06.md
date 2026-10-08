---
gate: G3
papel: seguranca
objeto: painel/entrada/saida.py @ a0a319b
veredito: RETURN
por: Worker06
data: 2026-10-08 14:17 -0300
data_objeto: 2026-10-08 14:03 -0300
---

# G3 — Crítica P2 do 068: envio assinado e log (SEGURANÇA)

**Hash:** a0a319b
**Branch:** w08/068-p2
**Base:** 48ffd83
**Arquivos:** painel/entrada/{saida.py, orquestrador.py, etapas.py, __init__.py, agendador.cmd} + 2 testes

---

## Veredito: RETURN

2 lacunas bloqueantes (logs e .gitignore), 1 de rito (vermelho/verde), 1 parcial (aviso Office).

---

## Item 1: Envio assinado HMAC-SHA256 ✓

**saida.py:42-47:** `hmac.new(segredo.encode(), corpo, hashlib.sha256).hexdigest()` — usa `hmac` + `hashlib.sha256`. Assinatura no header `X-Maestro-Assinatura: sha256=...`. Horário em `X-Maestro-Horario`, evento_id em `X-Maestro-Evento-Id`.

**Segredo em env:** `orquestrador.py:172`: `segredo = os.environ.get("MAESTRO_HMAC_SEGREDO")`. Passado como parâmetro até `saida.enviar()`. **Nenhum segredo hardcoded.** ✓

**Corpo:** `{"chamado", "contato", "texto"}` — envia `contato` (c-NNNN), não telefone. ✓

---

## Item 2: Retry 1/5/15/60 min, max 10/24h, "falhou" ✓ (parcial)

**saida.py:18-21:** `ESPERAS = [60, 300, 900, 3600]` (1, 5, 15, 60 min). ✓
**saida.py:24-25:** `MAX_TENTATIVAS = 10`, `MAX_IDADE_SEGUNDOS = 24 * 3600`. ✓
**saida.py:113-116:** `if tentativas >= MAX_TENTATIVAS or idade >= MAX_IDADE_SEGUNDOS` → status `falhou` com `ultimo_erro`. ✓

**Lacuna parcial:** NFR-012 diz "vira aviso direto à Office (mensagem na sessão, não só o cartão do painel)". O status `falhou` é gravado, mas **não há aviso à Office** — `despachar()` só retorna contagem `{"enviados": N, "falharam": N}`. O aviso direto não está implementado. **Sugerir:** adicionar gravação de aviso (evento `falhou` no painel ou chamada à sessão da Office) quando uma mensagem passa a `falhou`.

---

## Item 3: Logs só com metadados (NFR-011, SC-007) ✗

**Nenhum logging implementado.** `saida.py` e `orquestrador.py` não importam `logging`, não escrevem logs, não criam `dados/logs/`. A spec exige:

- **NFR-011:** logs só com metadados (horário, rota, evento_id, contato c-NNNN, chamado, status HTTP, duração, qual segredo validou). Nunca texto de mensagem, telefone, nome, anexo ou segredo.
- **SC-007:** teste que varre log gerado nos testes de P1 a P5 atrás de telefone, texto e segredo.

**Sem logs, não há como auditar envios, falhas ou troca de segredo.** Isto é bloqueante para segurança. **RETURN.**

---

## Item 4: dados/ no .gitignore (NFR-010, SC-006) ✗

**`dados/` não está no `.gitignore`.** Verificado: `git show a0a319b:.gitignore` não contém `dados`. A spec exige:

- **NFR-010:** `dados/` (contatos.db, entrada.db, logs, pendentes) no `.gitignore` do maestro e do repo `chamados`.
- **SC-006:** `git check-ignore` confirma os caminhos.

**Sem `.gitignore`, `dados/entrada.db` (que contém `texto` das mensagens e `contato`) pode ser acidentalmente commitado.** Bloqueante. **RETURN.**

---

## Item 5: Nenhum segredo no repo ✓

- `MAESTRO_HMAC_SEGREDO`, `MAESTRO_WEBHOOK_URL`, `MAESTRO_DADOS_DIR`, `MAESTRO_CFG_JSON` — todos lidos de `os.environ`. ✓
- Nenuma URL, token, senha ou endereço hardcoded. ✓
- Testes usam `"segredo"` como string de teste, não um segredo real. ✓

---

## Rito

### Vermelho + verde separados? ✗

W08 mandou **1 commit** (a0a319b) com implementação + testes juntos. O rito exige vermelho (testes que falham) e verde (implementação que passa) em commits separados. **Cobrar.**

### runner2 por não-autor

Pendente. O número do gate deve vir de quem não é o autor (W08). **Aguardar runner2.**

---

## Resumo

| Item | Status | Nota |
|---|---|---|
| 1. HMAC-SHA256, segredo em env | ✓ | `hmac.new` + env var, sem hardcoded |
| 2. Retry 1/5/15/60, max 10/24h | ✓ parcial | `falhou` sem aviso à Office (NFR-012) |
| 3. Logs só metadados (NFR-011) | ✗ RETURN | Nenhum logging implementado |
| 4. dados/ no .gitignore (NFR-010) | ✗ RETURN | `dados/` ausente do .gitignore |
| 5. Nenhum segredo no repo | ✓ | Tudo em env vars |
| Rito: vermelho/verde | ✗ | 1 commit, cobrar separação |
| Rito: runner2 não-autor | Pendente | |

---

> Veredito: RETURN
> 2 bloqueantes: logs (NFR-011) e .gitignore (NFR-010)
> 1 parcial: aviso à Office no `falhou` (NFR-012)
> 1 rito: vermelho/verde não separados

Sessao: Worker06
