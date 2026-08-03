# Apêndice B — Estudo hands-on do Superpowers

> **Data do estudo**: 2026-07-31 · **Fonte**: [`GHDaru/superpowers`](https://github.com/GHDaru/superpowers)
> (fork de `obra/superpowers` — Jesse Vincent; commit `44c9b2d`, v6.2.0, MIT)
> **Pergunta**: o que o líder do ecossistema de skills (~93k stars) faz que o Maestro
> deve absorver? Cumpre a promessa do ADR 0008 (reavaliação hands-on sob gatilho — o
> Steward trouxe o fork). Vereditos = **proposta** até aprovação (gate de mérito).

## Anatomia

**14 skills** compostas + bootstrap por **hooks** (session-start injeta a meta-skill em
toda conversa) + distribuição multi-runtime (Claude Code, Codex, Gemini CLI, Copilot,
OpenCode, Pi — via marketplace/plugin). Sem servidor, sem UI: é **só texto bem
engenheirado** — a força do projeto é linguística, não de infraestrutura.

O fluxo canônico: `brainstorming` (design aprovado ANTES de qualquer código) →
`using-git-worktrees` (workspace isolado) → `writing-plans` (tasks de 2–5 min) →
`subagent-driven-development` (subagente fresco por task + review por task + review
final) → `test-driven-development` (RED-GREEN-REFACTOR) → `verification-before-completion`
→ `finishing-a-development-branch`.

## As ideias avaliadas (com veredito proposto)

### 1. Enforcement linguístico — o padrão "Iron Law"

As skills críticas trazem leis formatadas como bloco inegociável, com a fórmula
*"violating the letter of the rules is violating the spirit of the rules"* — e a
meta-skill exige: *"se há 1% de chance de uma skill se aplicar, você DEVE invocá-la"*.
É engenharia de prompt como engenharia de processo: fecha as brechas de racionalização
do modelo **antes** de elas aparecerem.
- **Comparação**: nossas skills são bem estruturadas mas "educadas" — descrevem, não
  **comandam**; não fecham brechas.
- **Veredito: 🔄 absorver** — reescrever as leis das nossas 4 skills no padrão Iron Law
  (destino: skills existentes + guidance no `skill-author`).

### 2. Skills testadas como código (`writing-skills` = TDD para documentação)

A ideia mais original do repo: *"se você não viu um agente falhar SEM a skill, você não
sabe se a skill ensina a coisa certa"*. Escreve-se o cenário de pressão (teste), roda-se
um subagente **sem** a skill (RED — baseline falha), escreve-se a skill, roda-se de novo
(GREEN — compliance), fecham-se brechas (REFACTOR).
- **Comparação**: nossas skills nunca foram testadas contra baseline; assumimos que
  funcionam (exatamente o anti-padrão 7, "parece que funciona", aplicado a nós mesmos).
- **Veredito: 🔄 absorver** — protocolo de teste de skill no `skill-author` (cenário de
  pressão + baseline antes de publicar skill nova).

### 3. `systematic-debugging` — root cause antes de fix

Iron Law: *"NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST"* — fase de investigação
obrigatória antes de propor qualquer correção; symptom fix = falha.
- **Comparação**: **lacuna real** — temos "bug exige teste que reproduz", mas nenhuma
  disciplina de diagnóstico antes do fix.
- **Veredito: 🔄 absorver** — skill `diagnose-before-fix` (nasce com o protocolo de
  teste da ideia 2 — dogfood duplo).

### 4. Review por task (não só por ciclo)

`subagent-driven-development`: subagente fresco por task, **review de spec+qualidade
após CADA task**, e review amplo do branch no fim. Dois níveis de verificação.
- **Comparação**: nosso `review` é por ciclo/PR; validamos o contexto fresco (igual),
  mas não o checkpoint por task.
- **Veredito: 🔄 absorver parcial** — na raia plena com >3 tasks, checkpoint leve por
  task (destino: `comunicacao.md` + system prompt do `dev-implementer`).

### 5. "Assuma zero contexto" nos planos

`writing-plans`: escreva o plano *"assumindo que o engenheiro tem zero contexto do
codebase e gosto questionável"* — todo o necessário na task, tasks de 2–5 minutos.
- **Comparação**: nosso `tasks.md` ordena por fronteira mas não exige autossuficiência
  por task.
- **Veredito: 🔄 absorver** — uma linha de guidance no `tasks-template.md` vendorizado.

### 6. Continuous execution (não pergunte "continuo?")

*"Prompts de 'devo continuar?' desperdiçam o tempo do parceiro — execute o plano até
BLOCKED, ambiguidade real, ou fim."*
- **Comparação**: já é nossa prática operacional; confirma o desenho (atenção humana é
  o gargalo — gasta-se em gates, não em progresso).
- **Veredito: ✅ validação mútua** — nada a fazer.

### 7. Worktrees por task

Isolamento de workspace via git worktree antes de executar planos.
- **Comparação**: já absorvido no ADR 0008 (destino F3 futuro, quando houver dor de
  paralelismo). O estudo confirma a mecânica.
- **Veredito: 👁 mantém observar** (gatilho inalterado).

### 8. Bootstrap por hook de sessão

`hooks/session-start` injeta a meta-skill em TODA conversa — enforcement estrutural,
não dependente de o agente "lembrar" das skills.
- **Comparação**: nosso equivalente é o CLAUDE.md do repo (carga automática), mas ele
  **não manda** consultar as skills.
- **Veredito: 🔄 absorver** — parágrafo de enforcement no CLAUDE.md do maestro
  ("antes de agir, verifique se uma skill de `skills/` se aplica; se sim, siga-a").

## A tensão registrada: HARD-GATE universal × raias

O `brainstorming` impõe design aprovado para **tudo** — e nomeia como anti-padrão o
*"this is too simple to need a design"*. O Maestro decidiu o oposto no ADR 0005: a
**raia leve** existe porque o valor da spec escala com `ambiguidade × raio ×
irreversibilidade` — para um typo, spec é cerimônia de papel.
**Mantemos as raias** (com racional): o Superpowers opera dev-solo-com-agente, sem o
conceito de risco proporcional; nós temos gates por classe de risco que protegem onde
importa. O que absorvemos da posição deles é o *aviso*: na dúvida entre leve e plena,
é plena — regra que já temos (§3).

## Onde não serve (inalterado do ADR 0008)

Sem papéis, sem RACI, sem classes de risco, sem DoR/DoD formal, sem registro de
decisão — é método de **execução** para dev+agente, não governança de portfólio.
Adoção integral criaria segunda fonte de verdade de processo. **Descartada** (mantém).

## Síntese

| # | Ideia | Veredito proposto | Destino |
|---|---|---|---|
| 1 | Iron Law / enforcement linguístico | 🔄 absorver | reescrever leis das 4 skills + guidance no `skill-author` |
| 2 | TDD para skills (baseline + pressão) | 🔄 absorver | protocolo de teste no `skill-author` |
| 3 | Root cause antes de fix | 🔄 absorver | skill nova `diagnose-before-fix` |
| 4 | Review por task | 🔄 absorver parcial | raia plena >3 tasks: checkpoint leve (`comunicacao.md`, `dev-implementer`) |
| 5 | "Assuma zero contexto" na task | 🔄 absorver | 1 linha no `tasks-template.md` |
| 6 | Continuous execution | ✅ validação | — |
| 7 | Worktrees por task | 👁 observar | gatilho F3 inalterado |
| 8 | Bootstrap de enforcement | 🔄 absorver | parágrafo no CLAUDE.md |
| — | Adoção integral | ❌ descartar | mantém ADR 0008 |
| — | HARD-GATE universal | ❌ não absorver | raias mandam (ADR 0005); racional acima |

> **Status: incorporado.** O Steward aprovou todos os vereditos em 2026-07-31
> (`gate-010-vereditos`); absorções materializadas na **spec 011**: Iron Laws nas 5 skills,
> protocolo TDD-para-skills no `skill-author`, skill `diagnose-before-fix`, checkpoint
> por task (`comunicacao.md` + `dev-implementer`), zero-contexto no `tasks-template` e
> enforcement "skills primeiro" no CLAUDE.md. Referências: [ADR 0008](../adr/0008-avaliacao-ecossistema-sdd.md) ·
> [ficha do ecossistema](../research/avaliacao-ecossistema-sdd.md) · [Apêndice A](apendice-a-maestro-02.md).
