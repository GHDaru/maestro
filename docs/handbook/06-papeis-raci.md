# Capítulo 06 — Papéis e responsabilidades (elemento `[5]`)

> Preservar os contrapesos de um time — **decide ≠ executa ≠ verifica** — sem ter um
> time: papéis como modos de trabalho numa **matriz humano × agentes**.

## 1. Pergunta central

Num time, decidir, executar e verificar são **pessoas diferentes** — é justamente essa
separação que cria o contrapeso. Você é **uma** pessoa + N agentes. **Como preservar os
contrapesos sem colapsar os três numa só cabeça?**

## 2. Fundamentação teórica

**Papéis são modos de trabalho, não cargos.** Cada papel é exercido por humano, agente,
ou os dois com gate. Num time minúsculo os papéis **acumulam-se** — o risco é perder os
contrapesos ao concentrar tudo numa pessoa.

**RACI** dá o vocabulário: **R**esponsible (executa), **A**ccountable (responde/aprova),
**C**onsulted (verifica/consultado), **I**nformed. Regra clássica: **exatamente um
Accountable por tarefa** (um pescoço a apertar).

**Delegabilidade em solo+IA:**
- **R (executa)** → agente (dev/spec/plan/etc.).
- **C (verifica)** → agente **independente**, em contexto fresco (`[3]`) — nunca o mesmo
  que executou, nunca só o próprio humano (senão "eu decidi, eu confiro" mata a
  independência).
- **I (informado)** → logs / ExecutionTrace.
- **A (Accountable)** → **humano, sempre.** Um agente raciocina, executa e revisa, mas
  **não responde pelas consequências** — accountability não delega (`[1]`).

**A armadilha do funil.** Se o humano é A **e** confere à mão cada saída de agente, ele
recria "fazer tudo sozinho" — o A vira gargalo. Resolução: **o humano é Accountable pela
política, pelos gates e pelos critérios — não por cada instância.** Ele projeta os
trilhos (`allow/deny/ask` + DoD verificável + critérios da spec); os agentes operam
dentro deles; ele faz spot-check e responde pelos resultados. É a *política de delegação*
do `[1]` aplicada a papéis — o que faz o modelo escalar.

## 3. Frameworks / abordagens avaliados

| Abordagem | O que oferece | Veredito |
|---|---|---|
| **Matriz RACI/RASCI** | Quem executa/responde/consulta/informa por tarefa | **Adotado** — adaptado a humano × agentes |
| **Regra "um Accountable"** | Responsabilidade não se dilui | **Adotado** — o humano é o A único e fixo no risco |
| **Papéis Scrum** (PO/SM/Dev Team) | Papéis de time cross-funcional | **Parcial** — PO = Steward humano; Scrum Master e "dev team" são cerimônia de papel para solo (ver `[6]`) |
| **Time T-shaped / cross-funcional** | Largura de skills + profundidade | **Reinterpretado** — o agente cobre a **largura** (muitas skills); o humano guarda a **profundidade da decisão** |

## 4. Recomendação de utilização (1 humano + N agentes)

- Adotar a **matriz de papéis-modo** do `modelo-operacional.md` §4: Product Steward,
  Arquiteto/Tech Lead, Spec/Plan/UX/Dev/QA/Review/Security/Tech-Writer-agents,
  Orquestrador.
- **R/C/I → agentes; A → humano**, e o humano é Accountable **pela política/gates/
  critérios**, não por item.
- **C sempre independente do R** (contexto fresco).
- Indelegável ao agente: aprovar spec, plan, merge, autorizar deploy/migração.

## 5. Conexões

- **`[1]`** — accountability indelegável + política de delegação (o "de que" o humano é A).
- **`[3]`** — o revisor em contexto fresco **implementa** o C independente.
- **`[8]` DoR/DoD** — critérios verificáveis são o que **permite** delegar o C a um agente.
- **`[9]` Gates/risco** — a taxonomia de risco define onde o A **tem** que agir.

## 6. Insight da jornada e impacto no modelo

Insights do aprendiz: **"delega-se tudo menos o A"** (porque accountability responde pelas
consequências) e **"o humano é Accountable pela política, gates e critérios — não por cada
item"** (o que evita o funil e faz escalar). Sem impacto normativo novo — consolida e
fundamenta a matriz RACI já presente no §4. Diário: `[5]`.

## 7. Fontes

- Anthropic — *Building effective agents* (revisão humana crucial em agentes de código): https://www.anthropic.com/engineering/building-effective-agents
- Matriz RACI — prática consolidada de atribuição de responsabilidades em gestão.
- `docs/governance/modelo-operacional.md` §4 (papéis + RACI); Capítulo 01 (`[1]`).
