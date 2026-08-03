# Apêndice C — Panorama exploratório: templates e frameworks do ecossistema

> **Data da pesquisa**: 2026-08-01 · **Natureza**: exploratória (varredura + triagem),
> diferente dos apêndices A/B (hands-on). Alimenta o **funil de avaliação**:
> exploratório → gatilho → estudo hands-on → absorção por gate.
> Já julgados em profundidade: Spec Kit ✅ · OpenSpec ❌ (ADR 0005) · BMAD ❌ · Kiro/EARS 🔄 ·
> GSD 👁 · Tessl 👁 · Taskmaster 👁 · Agent OS 🔄 ([ficha](../research/avaliacao-ecossistema-sdd.md), ADR 0008) ·
> maestro-02 ([Apêndice A](apendice-a-maestro-02.md)) · Superpowers ([Apêndice B](apendice-b-superpowers.md)).
> Este apêndice cobre **o resto do panorama** — sem repetir os já decididos.

## Como ler

Cada item: o que é → o que teria a nos ensinar → **triagem**:
🔬 candidato a hands-on (com gatilho) · 👁 observar · ⛔ fora do nosso problema.

---

## A. Frameworks SDD completos (concorrentes do nosso fluxo)

### claude-code-spec-workflow (Pimzino)
Workflow automatizado em 2 trilhas: feature (`Requirements → Design → Tasks →
Implementation`) e **bug-fix** (`Report → Analyze → Fix → Verify`).
- **O que ensina**: a trilha dupla é a **validação externa das nossas raias** — feature
  = plena, bug = leve; e o `Analyze` antes do `Fix` ecoa nossa `diagnose-before-fix`.
- **Triagem**: 👁 observar — nada que nossas raias + skills não cubram; confirma o desenho.
- Fonte: [github.com/Pimzino/claude-code-spec-workflow](https://github.com/Pimzino/claude-code-spec-workflow)

### CCPM — Claude Code Project Manager
Spec-driven + **integração com GitHub Issues** + execução paralela de agentes + "toda
linha de código rastreia até a spec".
- **O que ensina**: rastreabilidade `spec ↔ issue ↔ código` executada via ferramenta de
  projeto real (Issues) — nosso elo `spec ↔ PR ↔ teste` sem tooling dedicado.
- **Triagem**: 🔬 hands-on **com gatilho**: quando o Maestro reger um projeto multi-dev
  com backlog em Issues (hoje: solo, YAGNI).
- Fonte: [cc.deeptoai.com/docs/en/tools/ccpm-claude-code-project-manager](https://cc.deeptoai.com/docs/en/tools/ccpm-claude-code-project-manager)

### Claude-Code-Workflow (catlog22)
Framework JSON-driven com 22 agentes e orquestração de múltiplos CLIs (Gemini/Qwen/Codex).
- **Triagem**: ⛔ fora do problema — orquestração multi-CLI não é nossa dor; complexidade
  sem contrapartida (anti-padrão 4).
- Fonte: [github.com/catlog22/claude-code-workflow](https://github.com/catlog22/claude-code-workflow)

## B. Engenharia de contexto (a spec como pacote de contexto)

### PRPs-agentic-eng (Wirasm) — Product Requirement Prompt
A tese: falhamos por "sobre-especificar o quê e sub-especificar o contexto". PRP = PRD +
**inteligência curada do codebase** + runbook do agente — "o pacote mínimo viável para a
IA entregar software funcional de primeira".
- **O que ensina**: nossa spec diz o quê/por quê; o PRP acrescenta **empacotar o contexto
  do codebase junto** (arquivos-chave, convenções, gotchas). Casa com o Princípio V e com
  a task zero-contexto do ciclo 011 — é a mesma ideia no nível da spec.
- **Triagem**: 🔬 hands-on **com gatilho**: primeiro ciclo do Maestro regendo **código de
  produto** (lá o contexto de codebase pesa; em ciclos de método, não).
- Fontes: [github.com/Wirasm/PRPs-agentic-eng](https://github.com/Wirasm/PRPs-agentic-eng) ·
  [Context Engineering 2/2 — PRPs (A B Vijay Kumar)](https://abvijaykumar.medium.com/context-engineering-2-2-product-requirements-prompts-46e6ed0aa0d1)

### Cline Memory Bank (padrão)
Memória persistente como **arquivos markdown estruturados** (project brief, contexto
ativo, progresso) que o agente relê a cada sessão.
- **O que ensina**: já temos o equivalente distribuído (CLAUDE.md + specs + registro
  JSONL); a ideia nova é o **"contexto ativo"** — um arquivo curto de estado corrente.
- **Triagem**: 👁 observar — nosso `retro.sh` + registro cumprem; reavaliar se sessões
  longas multi-dia doerem.
- Fonte: [Practical Context Engineering (A B Vijay Kumar)](https://abvijaykumar.medium.com/practical-context-engineering-for-vibe-coding-with-claude-code-6aac4ee77f81)

### context-forge
CLI que faz scaffold de documentação de context engineering (planos por estágio, regras).
- **Triagem**: 👁 — nosso `new-cycle.sh` + templates vendorizados já fazem o scaffold.
- Fonte: [github.com/webdevtodayjason/context-forge](https://github.com/webdevtodayjason/context-forge)

## C. Orquestração multi-agente pesada

### claude-flow
Plataforma de orquestração "enterprise" (swarms, hive-mind, dezenas de agentes).
- **Triagem**: ⛔ por ora — nosso princípio é a **menor autonomia que resolve** (cap. 05);
  swarm é a antítese do WIP=1 com gates. Reavaliar apenas se um dia houver frota real.
- Fonte: [github.com/kennyjpowers/claude-flow](https://github.com/kennyjpowers/claude-flow) (fork; upstream ruvnet)

### Google ADK / Gemini Enterprise Agent Platform (Memory Bank)
Plataforma gerenciada: memória de longo prazo, delegação agente-a-agente, fluxos
determinísticos para compliance.
- **O que ensina**: a direção enterprise (memória gerenciada + orquestração determinística
  para fluxos críticos) valida nossos gates mecânicos; é infraestrutura, não método.
- **Triagem**: 👁 — relevante só se formos a nuvem gerenciada.
- Fonte: [cloud.google.com — Gemini Enterprise Agent Platform](https://cloud.google.com/blog/products/ai-machine-learning/introducing-gemini-enterprise-agent-platform)

## D. Coleções e marketplaces (fontes de garimpo, não frameworks)

- **awesome-claude-code / awesome-claude-skills** — diretórios curados (centenas de
  skills/comandos/agentes). **Uso**: fonte de garimpo pontual pelo `research-curator`
  quando uma dor específica surgir — nunca importação em bloco (YAGNI).
- **Claude Plugins Plus Skills** — marketplace comunitário (~425 plugins / ~2.810 skills,
  05/2026) com CLI próprio. Mesmo uso: garimpo por dor.
- **claude-code-ultimate-guide** — 225 templates, documentação extensa; referência de
  consulta.
- Fontes: [scriptbyai.com — resource list](https://www.scriptbyai.com/claude-code-resource-list/) ·
  [ayautomate — best repos](https://www.ayautomate.com/blog/best-claude-code-github-repos) ·
  [claudecodeguides — CLAUDE.md patterns](https://claudecodeguides.com/claude-md/)

---

## Síntese da triagem

| Item | Triagem | Gatilho de reavaliação |
|---|---|---|
| claude-code-spec-workflow | 👁 valida raias | — |
| **CCPM** | 🔬 hands-on | projeto multi-dev com GitHub Issues |
| Claude-Code-Workflow | ⛔ | — |
| **PRP (Wirasm)** | 🔬 hands-on | 1º ciclo regendo código de produto |
| Cline Memory Bank | 👁 | sessões multi-dia doerem |
| context-forge | 👁 | — |
| claude-flow | ⛔ por ora | frota real de agentes |
| Google ADK/Gemini | 👁 | ida a nuvem gerenciada |
| Coleções/marketplaces | fonte de garimpo | dor específica (via `research-curator`) |

**Leitura crítica**: o panorama converge para as apostas que já fizemos — spec como
contexto, trilhas por tipo de mudança, rastreabilidade, disciplina de diagnóstico. As
duas ideias genuinamente novas para nós são **PRP** (contexto de codebase empacotado na
spec) e **CCPM** (rastreabilidade via Issues) — ambas com gatilho claro: **quando o
Maestro sair do próprio repo e reger código de produto**. Até lá, observar é a decisão
certa (YAGNI). O funil segue aberto: item que disparar gatilho vira estudo hands-on
(padrão Apêndice A/B) antes de qualquer absorção.
