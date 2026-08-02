# Roadmap & Mapa — Construir o Maestro

> O plano de trabalho para evoluir o Maestro de "documentação" para **toolkit** (agentes,
> skills, workflows, scripts). Também serve de **orientação**: se você está perdido, comece
> por aqui. Documento vivo — atualizado a cada fase.
>
> **Status**: Ativo · **Atualizado**: 2026-08-02 (ciclo 021) · **Regra**: este mapa é
> artefato vivo — todo ciclo concluído atualiza a tabela de fases **no mesmo PR**
> (anti-padrão 15: artefato de planejamento que congela).

## 1. Por onde começar (a ordem de leitura)

1. [`comece-por-aqui.md`](comece-por-aqui.md) — a história em 5 min.
2. [`governance/principios-maestro.md`](governance/principios-maestro.md) — os inegociáveis.
3. [`governance/modelo-operacional.md`](governance/modelo-operacional.md) — a regra do dia a dia.
4. [`handbook/README.md`](handbook/README.md) — o *porquê* de cada regra (consulta).
5. **Este roadmap** — o que vamos construir e em que ordem.
6. Dúvida em sigla → [`governance/glossario.md`](governance/glossario.md).

## 2. O que já temos (inventário)

| Área | Temos | Onde |
|---|---|---|
| Princípios + modelo | ✅ constituição + modelo operacional v1.2.0 | `governance/` |
| Fundamentos | ✅ handbook (12 caps) + decks + PDFs | `handbook/` |
| Decisões | ✅ ADRs 0004–0007 | `adr/` |
| Fluxo spec-driven | ✅ Spec Kit instalado (`/speckit.*` + templates) | `.claude/commands/`, `.specify/` |
| Enforcement | ✅ CI (gate changelog), PR template, comando `/dod` | `.github/`, `.claude/commands/dod.md` |
| Onboarding | ✅ guia + glossário (ciclo 001) | `docs/` |

## 3. O que é o Spec Kit e o que ele atende

Spec Kit = o **motor do passo a passo** ("defina o que construir antes de construir").
Comandos: `constitution · specify · clarify · plan · tasks · analyze · checklist · implement`.

**Quando cada artefato entra** (isto respondia sua dúvida):

| Artefato | Gerado em | Aplica-se a |
|---|---|---|
| `spec.md` | `/specify` | **sempre** (o quê e por quê) |
| `plan.md` | `/plan` | **sempre** (como + Constitution Check) |
| `research.md` | `/plan` | quando há incógnitas técnicas a resolver |
| `data-model.md`, `contracts/` | `/plan` | **features de código** (entidades, APIs) — não em docs |
| `tasks.md` | `/tasks` | sempre |
| `checklist.md` | `/checklist` | quando vale um checklist de qualidade específico |

> No ciclo 001 (docs) geramos spec/plan/tasks; **não** data-model/contracts — não se
> aplicavam. Isto passa a estar documentado aqui (era uma confusão legítima).

## 4. Perfis de agentes (o gap a resolver)

Hoje temos papéis conceituais (RACI, cap 06); falta o **perfil concreto de cada agente**.
Por causa da **janela de contexto**, cada agente precisa de escopo estreito e definido.
Cada perfil (um `.claude/agents/<nome>.md`) declara:

- **nome + propósito** (o papel que exerce);
- **escopo / o que faz** (e o que NÃO faz);
- **acesso** (tools permitidas) e **modelo**;
- **produz / consome** (artefatos de entrada e saída);
- **orçamento de contexto** (o que carrega, o que delega).

**Semente**: o `orientacoes_por_especialista.md` do FlowBuilder (mapa "por especialista:
produz/consome") — adaptamos para os agentes do Maestro (spec-agent, plan-agent, dev-agent,
review-agent, security-agent, tech-writer-agent, orquestrador).

## 5. Estrutura de documentos recomendada

Baseada no que o ghdaru provou + o que já temos. Proposta:

```
docs/
  comece-por-aqui.md        ✅ guia narrativo
  roadmap.md                ✅ este mapa
  governance/               ✅ principios · modelo · glossario
  handbook/                 ✅ 12 capítulos + decks + PDFs
  adr/                      ✅ decisões imutáveis
  research/                 ✅ pesquisa + diário
  architecture/             ➕ visão de arquitetura do toolkit (a criar)
  agents/                   ➕ perfis de agentes (fonte; espelha .claude/agents/)
  linguagem-ubiqua.md       ➕ termos do domínio (DDD) — se/quando houver domínio
specs/                      ✅ specs numeradas (001…)
skills/  workflows/  scripts/   ➕ o toolkit (a construir)
```

## 6. O que trazemos de cada fonte (curadoria)

| Fonte | O que trazer | Vira |
|---|---|---|
| **spec-kit** (fork) | fluxo completo + templates + comando `converge` | `.specify/` + `.claude/commands/` (vendorizar seletivo) |
| **ghdaru** | `linguagem-ubiqua` (DDD), `journeys/TEMPLATE`, `integration/manifesto`, `architecture` | referências para `docs/` |
| **flowbuilder** | `orientacoes_por_especialista` (produz/consome por papel); decisões de interface/infra | base dos **perfis de agentes** |
| **externo** (teoria + **agentskills.io**) | padrão `SKILL.md`; boas práticas citadas | `skills/` no padrão aberto |

> Regra (YAGNI): trazemos **conceito/contrato adaptado**, não cópia em bloco. Cada item
> entra por uma spec, não ad-hoc.

**Ecossistema avaliado** (resposta canônica a "isso foi avaliado?"): Spec Kit ✅ adotado ·
OpenSpec ❌ (ADR 0005) · Superpowers/BMAD/Kiro/Taskmaster/Agent OS/GSD/Tessl → ficha
[`research/avaliacao-ecossistema-sdd.md`](research/avaliacao-ecossistema-sdd.md) + decisão
[`adr/0008`](adr/0008-avaliacao-ecossistema-sdd.md) (ciclo 007). Ideias absorvidas: **EARS**
(critério de aceite) e **worktree/rigor mandatório** (Superpowers), com destino nomeado.

## 7. As fases (o plano de trabalho)

Cada fase = **um ciclo** (uma spec, um gate). Ordem por dependência:

| Fase | Entrega | Spec | Status |
|---|---|---|---|
| **F0 — Fundação** | roadmap (este) + ADR de curadoria de fontes | 002 | ✅ |
| **F1 — Agentes** | 12 subagentes executáveis (`.claude/agents/*` + `docs/agents/`): 8 núcleo + 4 toolkit | 003+004 | ✅ |
| **F2 — Skills** | leva V0 de skills agentskills.io: `constitution-check`, `dod-verificavel`, `combater-amontoado` | 005 | ✅ |
| **F3 — Scripts** | scripts do ritual (`promover-main`, `novo-ciclo`, `verificar-agentes` + `retro`, `registrar-decisao`) | 006, 008 | ✅ |
| **F4 — Vendorizar spec-kit** | templates spec/plan/tasks adaptados (PT, raias, EARS, Constitution Check) + comando `converge` do fork + proveniência (`.specify/UPSTREAM.md`) | 009 | ✅ |
| **F5 — O Livro** | padrão editorial (9 seções) + navegação em 5 trilhas + receitas + mapa da Jornada | 013, 014 | ✅ |
| **F6 — Companion** | tutor do livro: backend (busca no corpus + NVIDIA NIM + Neon) e widget | 015 | ✅ (falta publicar o serviço) |
| **F7 — Estudos de campo** | apêndices A (maestro-02), B (Superpowers) e C (panorama) + absorções | 010–012 | ✅ |
| **F8 — Método instalável** | instalação visível + agente `ux-semantica` + skill `jornada-viva` + `verificar-papeis.sh`; distribuição em três camadas (script · plugin · `npx skills add`) | 018, 019 | ✅ |
| **F9 — O processo visível** | BPMN com raia de UX e de distribuição; diagrama **navegável** no livro (cada caixa aponta para sua referência) + portões de imagem e de link em HTML bruto | 020 | ✅ |
| **F10 — Dogfood: o Maestro no Maestro** | `verificar-instalacao.sh` (camadas + IA instruída + skills visíveis), instrução gerada do disco (`--bloco`), `AGENTS.md` como fonte única, Constitution Check I–VIII | 021 | ✅ |
| **(contínuo) — Migração didática** | capítulos ao padrão v2, **um por ciclo**: 01 ✅ · 02–12 ⏳ | 016 e seguintes | 🔄 1/12 |
| **(contínuo) — Retrospectiva** | erro recorrente → regra versionada (catálogo de anti-padrões, leis das skills) | 017 e seguintes | 🔄 |

### Gatilhos abertos (decisões adiadas, com condição de revisão)

| Item | Gatilho para reavaliar |
|---|---|
| **PRP** (contexto de codebase na spec) | 1º ciclo regendo **código de produto** |
| **CCPM** (rastreabilidade via Issues) | projeto **multi-dev** com backlog em Issues |
| **Worktree por task** (Superpowers) | dor real de **paralelismo** entre tasks |
| **Telemetria de custo** (maestro-02) | quando medir custo por ciclo importar |
| Taskmaster · GSD · Tessl · Agent OS | ver [Apêndice C](handbook/apendice-c-panorama-templates.md) |

> Nota de numeração: os agentes ocuparam **duas** specs (003 núcleo, 004 toolkit), então as
> specs seguintes deslocam +1 em relação ao plano original. Fase é conceito; spec é sequência.

## 8. Como avaliamos (a régua)

- **Por ciclo**: DoD verificável + revisão independente + gate humano de merge (o que já
  fizemos no 001).
- **Por fase**: uma retro curta → erros recorrentes viram regra/skill/script.
- **Métrica-bússola**: o Maestro fica *mais fácil de usar por um humano+agente* a cada fase
  (menos confusão, menos ad-hoc) — o oposto do "amontoado".

---

**Próximo passo proposto**: abrir a **Fase 0 (spec 002 — Fundação)**, que oficializa este
roadmap, cria o ADR de curadoria de fontes e o `promote-main.sh`. Depois, F1 (agentes).
