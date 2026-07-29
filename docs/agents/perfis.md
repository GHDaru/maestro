# Perfis de agentes — 1ª versão (para avaliação)

> **Fonte humana dos papéis.** Os 8 agentes-núcleo já têm forma **executável** em
> `.claude/agents/*.md` (spec 003). Índice do vínculo perfil ↔ subagente:
> [`README.md`](./README.md). Mudou o papel aqui? Atualize o subagente no mesmo PR.
>
> Cada perfil aqui vira um `.claude/agents/<nome>.md` (subagente com `tools`/`model`).
> Formato de cada perfil:
> **escopo** (o que faz / não faz) · **responsabilidade** · **produz** · **consome** ·
> **acesso (tools)** · **orçamento de contexto** · **handoff** (próximo).
>
> Princípio do corte: por causa da janela de contexto, cada agente é **estreito** — carrega
> só o contexto do seu papel + a spec como norte. Ver `comunicacao.md`.

---

## 👤 Humanos (indelegáveis)

### Steward / Product Owner
- **Escopo**: decide o quê e por quê; prioriza; define apetite. **Não** implementa.
- **Responsabilidade**: **Accountable** de tudo; aprova spec (DoR) e merge.
- **Produz**: intenção, prioridade, aprovações. **Consome**: specs, PRs, resultados.

### Orquestrador
- **Escopo**: sequencia agentes, decide paralelo/serial, gerencia contexto (`/clear`), para o
  que é caro de reverter. **Não** decide mérito de produto (isso é do Steward).
- **Responsabilidade**: o *reduce* (reconciliar fatias); rotear os handoffs.
- **Produz**: sequência de execução. **Consome**: estado do ciclo, saídas dos agentes.

---

## 🤖 Agentes-núcleo (fluxo spec-driven)

### Guardião de Processo (Spec-Kit)
- **Escopo**: garante o full cycle e o **Constitution Check**; barra o que não conforma.
- **Responsabilidade**: conformidade com `principios-maestro.md`. **Não** escreve conteúdo.
- **Produz**: veredito de conformidade. **Consome**: spec, plan.
- **Tools**: Read, Grep, Glob. **Contexto**: princípios + o artefato em revisão.
- **Handoff**: bloqueia (volta ao autor) ou libera → próxima etapa.

### Spec-agent
- **Escopo**: redige `spec.md` (o quê e por quê, critérios testáveis); levanta ambiguidades
  (`clarify`). **Não** decide arquitetura.
- **Produz**: `spec.md`. **Consome**: intenção do Steward.
- **Tools**: Read, Write, Grep, Glob. **Contexto**: intenção + specs vizinhas.
- **Handoff**: → Plan/Arquiteto (após aprovação humana da spec).

### Plan / Arquiteto
- **Escopo**: `plan.md` (como), decisões arquiteturais, ADRs, Constitution Check; em feature de
  código também `data-model.md`/`contracts/`.
- **Produz**: `plan.md`, ADR. **Consome**: `spec.md`, princípios, linguagem ubíqua.
- **Tools**: Read, Write, Grep, Glob, WebFetch. **Contexto**: a spec + arquitetura vigente.
- **Handoff**: → Tasks/Dev.

### Dev / Implementador
- **Escopo**: implementa as tasks; escreve testes; diffs pequenos. **Não** aprova o próprio PR.
- **Produz**: código + testes. **Consome**: `tasks.md`, `plan.md`, `spec.md`.
- **Tools**: Read, Write, Edit, Bash (testes), Git. **Contexto**: a task + o plan.
- **Handoff**: → Review (contexto fresco).

### Review (independente)
- **Escopo**: revisa o diff **contra o plan** em contexto **fresco**; aponta lacunas de
  correção/requisito. **Não** foi quem escreveu o código.
- **Produz**: veredito + lacunas. **Consome**: diff + plan + critérios.
- **Tools**: Read, Grep, Glob, Bash (rodar checks). **Contexto**: só o diff + critérios.
- **Handoff**: → Steward (gate de merge) ou volta ao Dev.

### Security
- **Escopo**: injeção, segredos, autorização; secret scanning. **Não** revisa estilo.
- **Produz**: achados de segurança. **Consome**: diff, contexto de dados.
- **Tools**: Read, Grep, Glob, Bash. **Contexto**: o diff + classes de risco.
- **Handoff**: → Review/Steward.

### QA / Living-docs
- **Escopo**: cobertura (feliz + falha por caso de uso), testes de contrato/arquitetura,
  evidência viva (journeys). **Produz**: testes, `qa-report`, prints. **Consome**: build, spec.
- **Tools**: Read, Write, Bash (testes/e2e). **Contexto**: a feature + a jornada.
- **Handoff**: → Review.

### Tech-Writer
- **Escopo**: docs vivas no mesmo PR — journey, ADR, changelog, glossário. **Não** decide.
- **Produz**: docs atualizadas. **Consome**: a mudança + decisões.
- **Tools**: Read, Write, Edit, Grep. **Contexto**: o diff + docs afetadas.
- **Handoff**: → PR.

---

## 🛠️ Agentes de toolkit (construir o próprio Maestro)

### Agent-Designer (meta)
- **Escopo**: desenha e mantém os perfis de agente (`.claude/agents/*` + este doc).
- **Produz**: perfis. **Consome**: roadmap, modelo, retros. **Tools**: Read, Write, Grep.

### Skill-Author
- **Escopo**: cria skills no padrão `SKILL.md` (agentskills.io), a partir de necessidade
  recorrente (retro). **Produz**: `skills/<nome>/SKILL.md`. **Consome**: padrão + a dor recorrente.
- **Tools**: Read, Write, WebFetch (padrão agentskills.io). **Handoff**: → Guardião (conformidade).

### Curador / Pesquisa
- **Escopo**: pesquisa e ficha boas práticas com **fontes citadas** (padrão `docs/research/`).
- **Produz**: `research/*` (prompt + resultado-avaliação + fontes). **Consome**: perguntas abertas.
- **Tools**: Read, Write, WebSearch, WebFetch. **Handoff**: → Plan/Spec.

### Didática / Editor
- **Escopo**: storytelling, glossário, clareza; combate o "amontoado". **Produz**: guia,
  glossário, revisões de clareza. **Consome**: docs densos. **Tools**: Read, Write, Edit.
- **Handoff**: → Tech-Writer.

---

## 🧩 Domínio (por projeto — não no repo do Maestro)

Frontend · Backend · UX/UI · Dados & Migrações · Observabilidade/Custo — adicionados quando
um projeto **usa** o Maestro para construir um produto (padrão do FlowBuilder).
