---
gate: G1
papel: fluxo
objeto: specs/068-chamados-whatsapp/spec.md @ eb64383
veredito: APPROVE
por: Worker11
data: 2026-10-08 14:15 -0300
data_objeto: 2026-10-06 14:20 -0300
---

# Veredito G1 — 068-chamados-whatsapp (fluxo e texto para o cliente)

## Conferência

### Objeto

`specs/068-chamados-whatsapp/spec.md` @ `eb64383` (correções do RETURN do
W06 + bases legais pendentes). Diff conferido: `1303db8..eb64383`.

### 1. As 6 etapas sem jargão

FR-008 define o mapa gate → etapa do cliente:

| # | Etapa (cliente) | Gates internos |
|---|---|---|
| 1 | Recebido | abertura, G0 |
| 2 | Em análise | GD, G1 |
| 3 | Em desenvolvimento | G2, G3 |
| 4 | Em testes | G4, G5, G6 |
| 5 | Sua validação | G7 |
| 6 | Publicado | G8+ (só depois do G9 PASSOU) |

As 6 etapas são em português plain, sem jargão interno. SC-003 proíbe
termos internos nas mensagens de saída. ✅

### 2. As respostas nos três pontos (G0, G1, G7)

- **G0**: "Não conseguimos reproduzir. Pode mandar os passos e uma captura?" → `conversa.md` + `evidencias/`. ✅
- **G1**: `perguntas-cliente.md` → numeradas por WhatsApp, respostas em `respostas-cliente.md`. ✅
- **G7**: "Aprovo" → `G7-aceite.md` ACEITO; "Encontrei um problema" → RECUSADO + Office avisada. ✅

### 3. Número não cadastrado e mensagem fora de hora

- **Não cadastrado** (P4-AC1): "Não encontramos seu cadastro. Fale com o Escritório de Transformação da sua empresa." ✅
- **Fora de hora** (NFR-004 + P5-AC1): janela de 5 min → 401, sem gravar. ✅

### 4. Tasks P1–P5: vermelho antes do verde, coerente com a spec

Cada P tem [Verify] antes de [Impl]. Tasks cobrem todos os acceptance
scenarios e FRs das user stories P1–P5. ✅

---

## Diferença 1303db8..eb64383 (correções do W06)

O papel deste crítico é fluxo e texto para o cliente. As 6 correções do W06
são de segurança/dados/privacidade — nenhuma altera o fluxo visível ao
cliente ou o texto das mensagens. Conferidas quanto à coerência com a spec:

### NFR-008 — troca do segredo HMAC

Dois segredos válidos simultaneamente (`MAESTRO_WEBHOOK_SEGREDO` e
`_ANTERIOR`); saída assinada só com o atual. Procedimento de troca em 3
passos (pôr novo+velho, trocar no n8n, apagar velho após 24 h sem uso).
Log registra qual dos dois validou, sem o valor. Rotação padrão, coerente. ✅

### NFR-009 — anexos com PII, SC-005 não varre imagens

Anexos são dado do cliente, mesmas regras de retenção do relato. SC-005
varre só texto — imagens/PDFs/planilhas não varridos. Quem cita captura
fora do chamado confere à vista. Coerente — SC-005 não pode escanear
binário por telefone; NFR-009 reconhece e adiciona checagem visual. ✅

### P5-AC4 + NFR-012 — limite de retry

10 tentativas ou 24 h, o que vier antes → `falhou`, para de tentar, aviso
direto à Office (mensagem na sessão, não só painel) com chamado, etapa e
último erro, sem o texto. Assistente lista `falhou` no ciclo de 30 min.
Nota de alcance do P5-AC3 clarifica que entrega n8n→Evolution fica com o
n8n. Coerente — retry limitado com escalonamento. ✅

### NFR-010 + SC-006 — dados/ no .gitignore

`dados/` (contatos.db, entrada.db, logs, pendentes) no `.gitignore` do
maestro e do repo `chamados`. Teste `git check-ignore` nos três caminhos.
Coerente — dado local nunca commitado. ✅

### NFR-011 + SC-007 — logs só com metadados

Logs só com horário, rota, evento_id, contato (c-NNNN), chamado, status
HTTP, duração, qual segredo validou. Nunca texto, telefone, nome, anexo ou
segredo. Teste varre log da suíte P1–P5. Coerente — log metadata-only. ✅

### Bases legais pendentes (art. 7º e art. 16, GD classe C)

GD subiu para C em 06/10. Base legal do tratamento (art. 7º) e base legal
para retenção de 12 meses no git (art. 16) — ambas PENDENTE do Gilsiley.
Implementação não começa até a decisão dele. Coerente — corretamente
bloqueado, não é defeito da spec. ✅

---

## Conclusão

As 6 correções do W06 são coerentes com a spec e não alteram o fluxo nem o
texto visível ao cliente que este crítico já aprovou em 1303db8. O veredito
se mantém: **APPROVE**.
