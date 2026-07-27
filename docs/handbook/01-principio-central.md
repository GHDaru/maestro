# Capítulo 01 — Princípio operacional central (elemento `[1]`)

> **IA para explorar, propor e escrever; humano para especificar, decidir e aprovar;
> testes, gates e revisão independente para validar.**

## 1. Pergunta central

Se um agente *é capaz* de tomar qualquer decisão — inclusive registrar alternativas e
racional impecáveis — **o que ainda exige o humano?**

## 2. Fundamentação teórica

Quando é o agente que escreve o código, o eixo de controle se desloca: o que garante que
o software faz o que o negócio quer não é mais digitar código — é a clareza da
**intenção** e a força da **verificação**. Três pilares:

1. **A intenção vive na especificação**, não no código nem no prompt (base do `[2]`). O
   humano dirige e refina; o agente escreve.
2. **Quem executa não é quem verifica.** A verificação passa por um revisor independente,
   de preferência em *contexto fresco* — segregação de funções aplicada a agentes.
3. **Prove, não declare.** "Pronto" exige evidência que o agente gere e um gate confira.

**Accountability × capacidade.** Capacidade de *raciocinar* não é o mesmo que *responder
pelas consequências*. O gate humano não mede a qualidade do raciocínio do agente; ele
**localiza a responsabilidade**.

**Ex-ante × ex-post.** Um registro auditável é *ex-post* — descreve a decisão depois de
tomada. Um gate é *ex-ante* — barra antes de executar. Para uma ação **irreversível**,
auditar não impede o dano.

**A alavanca real: reversibilidade.** O que torna uma ação irreversível *segura de
delegar* não é a aprovação — é convertê-la em reversível (backup, dry-run, staging,
soft-delete). O gate humano sempre foi um **proxy** de "torne reversível ou olhe antes".

## 3. Frameworks / abordagens avaliados

| Abordagem | O que oferece | Veredito |
|---|---|---|
| **Human-in-the-loop / mixed-initiative** (Horvitz) | Humano no ponto de decisão para ações consequentes | **Adotado** — espinha do princípio |
| **Política declarativa `allow/deny/ask`** (Const. §IV; OpenAI Agents; OPA) | Decidir *classes* de ação autônoma, não cada instância | **Adotado** — humano decide a política, que fica registrada |
| **ADR** (Nygard) | Registro auditável: decisão + contexto + consequências + alternativas | **Adotado** — protocolo de registro de decisão |
| **Reversibility patterns** (backup/dry-run/staging/soft-delete; git checkpoint/rewind) | Tornar o irreversível reversível | **Adotado** — requisito de DoD para ação irreversível |
| **Taxonomia de classes de risco** (Const. §IV) | Grada o gate por risco | **Adotado** — mapa dos gates humanos |

## 4. Recomendação de utilização (1 humano + N agentes)

- **O humano decide a política de delegação, e ela vai ao registro** — a responsabilidade
  sobe da instância para a política (`allow/deny/ask`).
- **Verificação independente valida** — revisor em contexto fresco (`[3]`).
- **Ação irreversível exige reversibilidade engenheirada** antes de delegar (DoD de
  infra — `modelo-operacional.md` §7, §8).
- Gates indelegáveis: aprovar spec, plan, merge, autorizar deploy/migração.

## 5. Conexões

- **`[2]` Spec-Driven** — a spec é onde a intenção humana vive.
- **`[3]` Fluxo agentic** — reversibilidade = o checkpoint/rewind/git; verificação = revisor fresco.
- **`[10]` DORA** — "recuperável > cauteloso" é a evidência empírica da reversibilidade.
- **`[9]` Gates/risco** — a taxonomia que operacionaliza o gate.

## 6. Insight da jornada e impacto no modelo

Refinado ao ser **criticado**: de "toda decisão pode ser automatizada com registro" →
"o humano delega e a delegação vai ao registro" → **reversibilidade é o que torna o
irreversível seguro de delegar**. Sem impacto normativo direto (o princípio já constava);
alimentou os gates de reversibilidade formalizados no `[2]`/§7. Diário: `[1]` em
`research/jornada-aprendizado-modelo-operacional.md`.

## 7. Fontes

- Anthropic — *Building effective agents*: https://www.anthropic.com/engineering/building-effective-agents
- Claude Code — *Best practices*: https://code.claude.com/docs/en/best-practices
- E. Horvitz — *Principles of Mixed-Initiative UI*: https://www.microsoft.com/en-us/research/publication/principles-mixed-initiative-user-interfaces/
- M. Nygard — *Documenting Architecture Decisions*: https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- OWASP — *LLM01 Prompt Injection*: https://genai.owasp.org/llmrisk/llm01-prompt-injection/
- Constituição da Plataforma (Princípio IV).
