# Capítulo 10 — Gates humanos e classes de risco (elemento `[9]`)

> Um gate **uniforme** está sempre errado: pesado demais vira funil, leve demais deixa o
> irreversível escapar. O peso do gate escala com **irreversibilidade × impacto**.

## 1. Pergunta central

Você barateou os gates mecânicos (`[8]`) e guardou o humano para o global e o "é a coisa
certa". Mas aprovar um typo ≠ aprovar uma migração destrutiva. **Por que graduar o gate
por risco em vez de um gate uniforme — e qual eixo decide o peso?**

## 2. Fundamentação teórica

**Os dois fracassos do gate uniforme:**
- **pesado em tudo** → você aprova até o trivial → vira o **funil** (o gargalo do `[6]`);
- **leve em tudo** → uma ação irreversível **escapa** sem aprovação → a migração do `[1]`.

**O eixo: irreversibilidade × impacto (blast radius).** O gate deve ser **proporcional ao
risco**: automatize o baixo, escale o alto. Taxonomia oficial (Constituição §IV; modelo
§8):

| Classe | Exemplo | Agente sozinho? | Gate |
|---|---|---|---|
| Leitura | explorar, buscar | ✅ | nenhum |
| Leitura sensível | PII/segredos | ⚠️ política + máscara | revisão |
| Criação reversível | feature em branch | ✅ | merge |
| **Alteração** | refactor amplo, contrato | ❌ | aprovação com resumo |
| **Exclusão / externa** | apagar dados, push, API externa | ❌ | confirmação forte |
| **Financeira / irreversível** | deploy, migração destrutiva | ❌ | dupla aprovação |
| **Lote / cross-tenant / admin** | migração em massa | ❌ **bloqueado** | workflow humano formal |

**Dois amarres:**
1. **Mesmo eixo das raias (`[2]`).** `ambiguidade × raio × irreversibilidade` decide quanto
   **processo** (spec); `irreversibilidade × impacto` decide quanto **gate**. Mesma física:
   *processo* para construir, *gate* para agir.
2. **Reversibilidade rebaixa a classe.** Tornar a ação reversível (backup/staging/
   soft-delete — `[1]`) move-a escada de risco **abaixo** → gate mais leve → menos funil.

## 3. Frameworks / abordagens avaliados

| Abordagem | O que oferece | Veredito |
|---|---|---|
| **Política `allow/deny/ask`** (OpenAI Agents approvals; OPA) | Decisão declarativa por classe | **Adotado** — a máquina de estados de ação (Const. §IV) |
| **Taxonomia de classes de risco** (Const. §IV) | Grada o gate | **Adotado** — base do `[9]` |
| **Human approval for high-stakes** (Anthropic) | Humano no ponto consequente | **Adotado** — gates indelegáveis |
| **Least privilege / RBAC-ABAC** | Autorização fora do LLM | **Adotado** — política decide, não o modelo |
| **Gate uniforme (um approve pra tudo)** | Simplicidade aparente | **Rejeitado** — funil ou catástrofe |

## 4. Recomendação de utilização (1 humano + N agentes)

- **Gate proporcional** pela taxonomia do modelo §8; automatizar baixo risco, escalar alto,
  **bloquear** lote/cross-tenant/admin.
- **Indelegáveis** (sempre humano): aprovar spec, plan, merge, autorizar deploy/migração.
- **Autorização fora do LLM** (RBAC/ABAC/política) — o modelo nunca decide permissão.
- **Investir em reversibilidade** para rebaixar classes e reduzir gates pesados.

## 5. Conexões

- **`[1]`** — reversibilidade é o eixo e a alavanca (rebaixa a classe).
- **`[2]`** — mesma física das raias, aplicada a ações.
- **`[5]`** — o A humano age exatamente nos gates altos; delega os baixos.
- **`[6]` / `[8]`** — gate barato/automático no baixo risco evita o funil.

## 6. Insight da jornada e impacto no modelo

Insights do aprendiz: o eixo é **irreversibilidade × impacto**; um gate uniforme é funil
ou catástrofe; logo **gate proporcional**. Fundamenta o mapa de gates do
`modelo-operacional.md` §8 e a taxonomia da Constituição §IV. Diário: `[9]`.

## 7. Fontes

- Anthropic — *Building effective agents* (revisão humana para alto risco): https://www.anthropic.com/engineering/building-effective-agents
- OWASP — *LLM01 Prompt Injection* (dados também são hostis; política fora do LLM): https://genai.owasp.org/llmrisk/llm01-prompt-injection/
- Open Policy Agent: https://www.openpolicyagent.org/docs
- `principios-maestro.md` (Princípio III, classes de risco); `docs/governance/modelo-operacional.md` §8.
