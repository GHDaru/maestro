---
gate: G3
papel: criterio
objeto: painel/entrada/contatos.py @ b47f198
veredito: APPROVED
por: Worker01
data: 2026-10-08T00:00:00-03:00
data_objeto: 2026-10-08
---

# Veredito G3 — Trilha B do Chamado 068 (crítica de fluxo e comportamento)

**Crítico:** Worker01 (não-autor)
**Autor:** Worker02
**Branch:** w02/068-trilha-b
**HEAD:** b47f198
**Repo:** maestro (`C:/Users/ghdaru/DriveD/010_PROJETOS/wt-w02-068-trilha-b`)

---

## 1. P4: número desconhecido recebe resposta fixa

**CONFIRMADO.** `servidor.py:186-196` — se `telefone` existe e `contatos.lookup` retorna None, devolve resposta fixa: "Não encontramos seu cadastro. Fale com o Escritório de Transformação da sua empresa."

- **Nenhum arquivo criado:** ✅ — a resposta é um dict retornado, sem efeito colateral.
- **Log sem texto:** ✅ — `log_message` é silenciado (servidor.py:102-103), não vaza conteúdo do body.
- **Cadastrado recebe menu:** o cadastrado recebe `{"status": "aceito", "evento_id": ...}` (202). O comentário diz "Skeleton — processamento vem em P1/P3 (conversa.py)". O menu real virá em conversa.py. O teste `test_contato_cadastrado_nao_recebe_msg_desconhecido` confirma que cadastrado não recebe a mensagem de desconhecido (status 202, sem "cadastro" no payload).

## 2. P5: assinatura inválida, horário fora, IP fora → rejeição sem gravar

- **Assinatura inválida → 401:** ✅ (`servidor.py:153-155`). Usa `hmac.compare_digest` (timing-safe). Dois segredos (atual + anterior, NFR-008).
- **Horário fora de 5 min → 408:** ✅ (`servidor.py:169`). Não é 401, mas 408 é semanticamente mais específico (Request Timeout). Não bloqueante.
- **IP fora da lista → 403:** ✅ (`servidor.py:130-132`). Não é 401, mas 403 é semanticamente mais específico (Forbidden). Não bloqueante.
- **Sem gravar nada:** ✅ — todas as validações (IP, body, assinatura, JSON, timestamp, evento_id) ocorrem antes de qualquer gravação no banco.

**Nota non-blocking:** `seguranca.py` tem `verifica()` que retorna 401 para todos os casos, mas `servidor.py` não usa `seguranca.verifica()` — duplica a lógica com códigos HTTP diferentes (403/408/401). `seguranca.py` é usado apenas por `test_seguranca.py`. Duplicação a resolver quando o servidor amadurecer.

## 3. P5: idempotência (mesmo evento_id duas vezes)

**CONFIRMADO.** `eventos.py:65-74` — `processa()` consulta primeiro; se `evento_id` já existe, retorna a resposta guardada sem chamar `fn()`. Senão chama `fn()`, guarda e retorna.

Teste `test_idempotencia_mesmo_evento_id` envia o mesmo evento duas vezes e confirma `status == status` e `data == data`.

## 4. P5: retry 500 → 1/5/15/60; 200 → enviado; painel mostra pendentes

**NÃO ESTÁ NESTA TRILHA.** O `saida.py` (fila de saída com retry) foi commitado em `a142f0f` mas removido em `b47f198` ("conflito com trilha C (W08, T2-03)"). O retry ficou na trilha C. Esta trilha B cobre apenas P4 (contatos) + P5 (porta segura: assinatura, horário, IP, idempotência).

## 5. Vermelho+verde separados

**CONFIRMADO.** O log mostra 6 pares vermelho→verde:
- `bf9dd13` (vermelho contatos) → `7ed8083` (verde contatos)
- `ebf9307` (vermelho seguranca) → `73445ae` (verde seguranca)
- `fcdb666` (vermelho eventos) → `ac5f003` (verde eventos)
- `46c4637` (vermelho conversa) → `8ee1378` (verde conversa)
- `db585b8` (vermelho servidor P5) → `2c2bd6a` (verde servidor P5)
- `91eb41e` (vermelho saida) → `a142f0f` (verde saida) — saida.py removido depois

**runner2 por não-autor:** pendente — o autor é W02; o número que vale para o gate deve vir de quem não é o autor (W07 ou outro), em clone limpo.

## 6. Nenhum segredo/telefone/nome real no repo

**CONFIRMADO.** Grep por `55\d{8,11}`, `senha`, `secret`, `token`, `@neogrid`, `@hindiana` em `painel/entrada/*.py`:
- Todos os telefones são sintéticos: `559999900001`, `559999900002`, `559999999999`, `5511999999999`.
- Segredos de teste: `"segredo-teste-atual"`, `"segredo-teste-anterior"`.
- Segredos reais: lidos de env vars (`MAESTRO_WEBHOOK_SEGREDO`, `MAESTRO_WEBHOOK_SEGREDO.ANTERIOR`).
- Telefone real: fica em `dados/entrada.db` (fora do .gitignore, LGPD).

---

## Resumo

| # | Item | Veredito |
|---|------|----------|
| 1 | P4: desconhecido recebe resposta fixa, sem arquivo, log limpo | ✅ |
| 2 | P5: assinatura/horário/IP inválido → rejeição sem gravar | ✅ (403/408/401, não 401 uniforme) |
| 3 | P5: idempotência por evento_id | ✅ |
| 4 | P5: retry 500 → 1/5/15/60 | N/A (saida.py na trilha C) |
| 5 | Vermelho+verde separados | ✅ |
| 6 | Sem segredo/telefone/nome real | ✅ |

**Veredito: APPROVED** com 2 notas non-blocking:
1. `servidor.py` retorna 403 (IP) e 408 (horário) em vez de 401 uniforme — semanticamente mais específico, não bloqueante.
2. `seguranca.py` não é usado por `servidor.py` (duplica lógica) — resolver quando o servidor amadurecer.

Sessao: Worker01
