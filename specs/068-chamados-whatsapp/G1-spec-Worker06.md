---
gate: G1
papel: seguranca
objeto: specs/068-chamados-whatsapp/spec.md @ eb64383
veredito: APPROVE
por: Worker06
data: 2026-10-06 14:33 -0300
data_objeto: 2026-10-06 14:20 -0300
---

# G1 — Crítica de spec: 068-chamados-whatsapp (re-crítica)

## Veredito: APPROVE (nos 5 pontos técnicos)

As 5 lacunas do RETURN (8ed2338 sobre 1303db8) foram corrigidas em eb64383. As bases legais (LGPD art. 7º e art. 16) continuam pendentes do Gilsiley (GD classe C, Office 09461a2) — não bloqueiam o veredito nos pontos técnicos.

---

## Re-crítica: diff 1303db8..eb64383

### 1. NFR-008: Troca do segredo HMAC ✓

**Lacuna original:** procedimento de rotação de segredo não definido.

**Correção (NFR-008):** dois segredos válidos simultaneamente (`MAESTRO_WEBHOOK_SEGREDO` e `MAESTRO_WEBHOOK_SEGREDO_ANTERIOR`). Valida contra os dois, assina só com o atual. Procedimento: (a) pôr novo como atual e velho como anterior + reiniciar; (b) trocar no n8n; (c) após 24 h sem chamada assinada com o velho, apagar o anterior. Log registra qual dos dois validou, sem o valor.

**Avaliação:** janela de sobreposição sem parar a entrada, procedimento em 3 passos, cleanup automático após 24 h, log sem o valor do segredo. ✓ Resolvido.

### 2. NFR-009: Anexos e capturas são dado do cliente ✓

**Lacuna original:** anexos podem conter PII (capturas não varridas por SC-005).

**Correção (NFR-009):** anexos são dado do cliente, podem ter dado pessoal (nome, e-mail, CPF, dados de terceiros). Ficam em `evidencias/` com as mesmas regras de retenção e apagamento do relato. SC-005 varre só texto — imagens, PDFs e planilhas não são varridos. Quem cita captura fora do chamado confere à vista que não há dado pessoal.

**Avaliação:** reconhece PII em anexos, mesmas regras de retenção, limitação do SC-005 explícita, conferência visual antes de citar fora. ✓ Resolvido.

### 3. P5-AC3 + P5-AC4 + NFR-012: n8n/Evolution fora e limite de retry ✓

**Lacuna original:** Evolution cair não mencionado; retry sem limite/alerta.

**Correção:**
- Nota de alcance do P5-AC3: aplicação só enxerga o webhook do n8n; cobre n8n fora e Evolution fora com n8n respondendo erro. Mensagem que n8n aceitou com 200 e Evolution não entregou fica com o n8n, fora do escopo.
- P5-AC4: 10 tentativas ou 24 h → `falhou`, para de tentar, Office recebe aviso direto (NFR-012).
- NFR-012: limite de 10 tentativas ou 24 h (o que vier antes). Fica `falhou`, vira aviso direto à Office com chamado, etapa e último erro (sem o texto). Assistente lista `falhou` no ciclo de 30 min.

**Avaliação:** Evolution coberto, limite definido (10/24h), aviso direto à Office (não só painel), Assistente monitora. ✓ Resolvido.

### 4. NFR-010 + SC-006: dados/ no .gitignore ✓

**Lacuna original:** `dados/` fora do git não explicitado em .gitignore ou teste.

**Correção (NFR-010):** `dados/` (contatos.db, entrada.db, logs, pendentes) no `.gitignore` do maestro e do repo `chamados`. SC-006: `git check-ignore` confirma `dados/contatos.db`, `dados/entrada.db` e `dados/logs/` nos dois repos.

**Avaliação:** .gitignore em ambos os repos, teste automático com git check-ignore. ✓ Resolvido.

### 5. NFR-011 + SC-007: logs só com metadados ✓

**Lacuna original:** conteúdo dos logs não especificado; logs poderiam conter PII.

**Correção (NFR-011):** logs só com metadados: horário, rota, `evento_id`, `contato` (c-NNNN), chamado, status HTTP, duração e qual segredo validou. Nunca texto de mensagem, telefone, nome do contato, conteúdo de anexo ou segredo. SC-007: teste varre log gerado nos testes de P1 a P5 atrás de telefone, texto de mensagem e segredo de teste.

**Avaliação:** lista exaustiva do que entra (metadados) e do que não entra (PII), teste automático que varre o log. ✓ Resolvido.

---

## Bases legais (LGPD) — pendentes do Gilsiley

A seção "Bases legais (LGPD): pendentes do Gilsiley" foi adicionada em eb64383:
- Base legal do tratamento (art. 7º): PENDENTE — candidatas: execução de contrato (art. 7º V), legítimo interesse (art. 7º IX).
- Base legal para retenção de 12 meses em git (art. 16): PENDENTE.

Estas são decisão do Gilsiley (controlador), GD classe C (Office 09461a2). **Não bloqueiam o veredito nos 5 pontos técnicos.** A implementação não começa até a Office preencher com a decisão dele.

---

## Resumo

| Item | RETURN (8ed2338) | Correção (eb64383) | Re-crítica |
|---|---|---|---|
| 1. Troca de segredo | Sem procedimento | NFR-008: dois segredos, 3 passos, cleanup 24 h | ✓ APPROVE |
| 2. Anexos com PII | SC-005 não varre imagens | NFR-009: anexos são dado, conferência visual | ✓ APPROVE |
| 3. n8n/Evolution + retry | Evolution não citado; sem limite | P5-AC4 + NFR-012: 10/24h, `falhou`, aviso Office | ✓ APPROVE |
| 4. dados/ no .gitignore | Não explicitado | NFR-010 + SC-006: .gitignore + git check-ignore | ✓ APPROVE |
| 5. Logs com metadados | Conteúdo não especificado | NFR-011 + SC-007: só metadados, teste varre log | ✓ APPROVE |
| Bases legais (art. 7º, 16) | Não citadas | Seção pendente do Gilsiley (GD C) | Pendente (não bloqueia) |

---

> Veredito: APPROVE (nos 5 pontos técnicos; bases legais pendentes do Gilsiley, GD C)
> Re-crítica de: 8ed2338 (RETURN sobre 1303db8)

Sessao: Worker06
