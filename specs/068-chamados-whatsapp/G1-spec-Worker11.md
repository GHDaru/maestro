---
gate: G1
papel: fluxo
objeto: specs/068-chamados-whatsapp/spec.md @ 1303db8
veredito: APPROVE
por: Worker11
data: 2026-10-06 14:01 -0300
data_objeto: 2026-10-06 13:50 -0300
---

# Veredito G1 — 068-chamados-whatsapp (fluxo e texto para o cliente)

## Conferência

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

As 6 etapas são em português plain, sem jargão interno (G0, GD, W01…W13,
runner2, VM, barra, APPROVE, REPROVE, hash, caminho). Os gates internos
ficam entre parênteses para a equipe, não aparecem na mensagem do cliente.

Exceções (FR-008): "Aguardando informação sua", "Não aprovado", "Voltou para
ajuste" — também sem jargão.

SC-003 proíbe explicitamente termos internos nas mensagens de saída, e P2
cenário 2 + T2-05 constroem teste que varre os modelos. ✅

### 2. As respostas nos três pontos (G0, G1, G7)

**G0 — reprodução (P3 cenário 1):**
- Texto: "Não conseguimos reproduzir. Pode mandar os passos e uma captura?"
- Evidência: resposta anexada a `conversa.md` e `evidencias/`, chamado volta a "Recebido". ✅

**G1 — dúvidas (P3 cenário 2):**
- `perguntas-cliente.md` → perguntas numeradas por WhatsApp.
- Respostas gravadas em `respostas-cliente.md` com data e hora.
- Chamado registra `clarify respondido`. ✅

**G7 — aceite (P3 cenários 3 e 4):**
- "Aprovo" → `G7-aceite.md` com `veredito: ACEITO`, `por: Mauricio (cliente)`,
  `objeto: <app> @ <hash no staging>` + mensagem original no corpo.
  Conferidor dá G7 PASSOU.
- "Encontrei um problema" → `G7-aceite.md` com `veredito: RECUSADO`,
  descrição + capturas, Office avisada. ✅

Os três pontos têm texto claro para o cliente e a resposta vira evidência
no gate. ✅

### 3. Número não cadastrado e mensagem fora de hora

**Número não cadastrado (P4 cenário 1):**
- Texto: "Não encontramos seu cadastro. Fale com o Escritório de Transformação da sua empresa."
- Nada criado no repositório. Evento no log, sem o texto da mensagem. ✅

**Mensagem fora de hora (NFR-004 + P5 cenário 1):**
- Assinatura HMAC-SHA256 + janela de 5 min no cabeçalho de horário.
- Horário fora de 5 min → 401, sem gravar nada. ✅

Ambos cobertos com texto e comportamento definidos. ✅

### 4. Tasks P1–P5: vermelho antes do verde, coerente com a spec

`tasks.md` Instructions: "Em cada cenário, o teste vermelho vem antes do
código (padrão do chamado, G2)."

Cada P tem [Verify] (vermelho) antes de [Impl] (verde):

| P | Verify → Impl |
|---|---|
| P1 | T1-01→T1-02, T1-03→T1-04, T1-10→T1-11 |
| P2 | T2-01→T2-02/03/04, T2-05→T2-06, T2-07→T2-08 |
| P3 | T3-01→T3-02, T3-03→T3-04, T3-05→T3-06 |
| P4 | T4-01→T4-02 |
| P5 | T5-01→T5-02, T5-03→T5-04, T5-05→T5-06 |

Tasks cobrem todos os acceptance scenarios das user stories P1–P5 e os FRs
correspondentes (FR-001 a FR-011, NFR-004). ✅

---

## Observação (não bloqueante)

FR-012 e FR-013 (retenção e apagamento, adicionados em 1303db8) não têm
tasks explícitas em `tasks.md`. A própria spec diz (Assumption): "O W06
confere no G1; prazo diferente… é decisão do Gilsiley." As tasks de retenção
são intencionalmente deferidas à conferência do W06 no G1 — consistente com
a spec. Não é bloqueante para este G1.
