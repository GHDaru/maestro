# Modelo Operacional — Papéis, Cerimônias, Entregáveis e Artefatos

> Como o trabalho é conduzido na Plataforma GHDaru Tecnologia num contexto de
> **um humano orquestrando múltiplos agentes de IA**. Este documento define QUEM faz
> O QUÊ (papéis/responsabilidades), QUANDO (cerimônias/cadência) e O QUE se produz
> (entregáveis/artefatos com gate).
>
> **Status**: Ativo · **Versão**: 1.2.0 · **Data**: 2026-07-22 ·
> **Fundamentação**: `docs/research/resultado-pesquisa-praticas-desenvolvimento-avaliacao.md`
> · **Decisões**: `docs/adr/0004-modelo-operacional.md`,
> `docs/adr/0005-raias-de-trabalho-e-specs-de-infra.md`,
> `docs/adr/0006-enforcement-dod-changelog.md`
> · Novo por aqui? [Comece por aqui](../comece-por-aqui.md). Siglas: [glossário](glossario.md).

## 1. Propósito e escopo

A Constituição (`.specify/memory/constitution.md`) define os **princípios** (o que é
inegociável) e o Spec Kit define o **fluxo técnico de uma feature**
(`/speckit.specify → clarify → plan → tasks → implement`). Faltava a camada de cima:
o **modelo operacional** — a distribuição de papéis entre humano e agentes, a cadência
de trabalho e o catálogo de entregáveis com seus portões de qualidade.

Este documento **não substitui** a Constituição nem o Spec Kit; ele os **integra**.
Onde houver conflito, a Constituição prevalece (Governance).

## 2. Princípio operacional central

Derivado da pesquisa (síntese e Princípios I, V, VII da Constituição):

> **IA para explorar, propor e escrever; humano para especificar, decidir e aprovar;
> testes, gates e revisão independente para validar.**

Três regras operacionais decorrem dele:

1. **A spec é a fonte de verdade, não o código nem o prompt.** Todo trabalho nasce de
   uma especificação (`principios-maestro.md`, Princípio I). O humano *dirige e refina*; o agente escreve.
2. **Quem executa não é quem verifica.** A verificação final passa por um **agente
   revisor em contexto fresco** (e/ou humano), nunca pelo mesmo agente que produziu o
   código. É o contrapeso que substitui o "segundo par de olhos" de um time.
3. **Prove, não declare.** "Pronto" exige evidência que um agente consiga gerar e um
   gate consiga conferir: teste verde, build limpo, lint, screenshot, journey
   atualizada.

## 3. Raias de trabalho (quanto processo cada mudança recebe)

Nem toda mudança merece uma spec completa. O **valor de uma spec escala com
ambiguidade × raio de impacto × irreversibilidade** — quando os três são baixos, a
spec é cerimônia de papel (YAGNI); quando algum é alto, ela se paga. Daí três raias:

| Raia | Quando | Fluxo | Registro | DoD |
|---|---|---|---|---|
| **Leve (delta)** | bug, typo, rename, log, copy — "dá para descrever o diff numa frase" | direto: explore → code → commit (sem `spec.md`/`plan.md`/`tasks.md`) | **o PR é o artefato** (descreve o delta); bug **exige um teste que o reproduz** (falha primeiro) | reduzida: testes + fitness + revisão independente; doc viva só se tocar jornada |
| **Plena (spec)** | feature ambígua, contrato, mudança cross-feature | Spec Kit completo: specify → clarify → plan → tasks → implement | `specs/NNN-*/` | completa (§7) |
| **Infra** | infra, migração, deploy | Spec Kit completo — **sempre plena**, nunca leve (mesmo parecendo pequena) | `specs/NNN-*/` | completa **+ gates de reversibilidade** (§7) |

Regras da raia leve: (1) na dúvida entre leve e plena, é **plena**; (2) infra e
migração **nunca** são leves — o raio e a irreversibilidade as jogam direto na raia
infra; (3) a raia leve **não** afrouxa a revisão independente nem os testes — só
dispensa os artefatos de planejamento (`spec`/`plan`/`tasks`).

> **Uma única ferramenta de spec-driven (Spec Kit).** A raia leve (modelo *delta*)
> mora **dentro** dela, não numa segunda ferramenta. Ver §10 (OpenSpec avaliado e
> descartado).

## 4. Papéis e responsabilidades

Num time minúsculo os papéis clássicos **acumulam-se**, mas os **contrapesos** são
preservados movendo o *verifica* para um agente independente e mantendo o *decide*
sempre no humano. Cada "papel" é um **modo de trabalho** exercido por humano, agente,
ou os dois com gate.

| Papel (modo) | Exercido por | Responsabilidade | Gate |
|---|---|---|---|
| **Product Steward / PO** | **Humano** | Decide o quê e por quê; prioriza; define apetite do ciclo; aprova specs e releases | Accountable de tudo |
| **Arquiteto / Tech Lead** | Humano + `plan-agent` | Decisões arquiteturais (DDD/hexagonal, contratos, ADRs); Constitution Check | Humano aprova o plan |
| **Spec-agent** (`/speckit.specify`, `clarify`) | Agente (humano decide) | Redige `spec.md` a partir da intenção; levanta ambiguidades | Humano aprova a spec |
| **Plan-agent** (`/speckit.plan`) | Agente | Redige `plan.md`, `ux-design.md`, Constitution Check | Humano aprova o plan |
| **UX-agent** | Agente + skills | Consulta design system + camada semântica; define `ux-design.md` | Objeto semântico obrigatório (P. VII) |
| **Dev-agent** (`/speckit.implement`) | Agente | Implementa tasks; escreve testes; diffs pequenos | Testes verdes + fitness functions |
| **QA/SDET-agent** | Agente | Cobertura feliz + falha por caso de uso; testes de contrato/arquitetura | DoD (§7) |
| **Review-agent** (revisor independente) | Agente em **contexto fresco** | Revisa o diff contra o plan; aponta lacunas de correção/requisito | `/code-review`, gate de merge |
| **Security-agent** | Agente | Revisão de injeção/segredos/autorização; secret scanning | Gate de segurança leve (§7) |
| **Tech Writer-agent** | Agente | Atualiza `docs/journeys/`, ADRs, changelog no mesmo PR | Documentação viva (P. VII) |
| **Orquestrador** | **Humano** | Sequencia agentes; `/clear` entre tarefas; decide paralelo/pipeline; para quando algo é caro de reverter | — |

**RACI por etapa do ciclo de vida** (R = executa, A = aprova/accountable,
C = consultado, I = informado):

| Etapa | Executa (R) | Verifica (C) | Aprova (A) |
|---|---|---|---|
| Definir intenção/apetite | Humano | — | **Humano** |
| Spec (`spec.md`) | Spec-agent | Humano | **Humano** |
| Plan + Constitution Check | Plan-agent | Review-agent | **Humano** |
| UX design | UX-agent | Humano | **Humano** |
| Implementação | Dev-agent | QA-agent | Review-agent → **Humano** |
| Revisão de código | Review-agent (fresco) | Security-agent | **Humano** |
| Documentação/jornadas | Tech Writer-agent | Humano | **Humano** |
| Release/deploy | Humano + CI | Review-agent | **Humano** |

> **O humano é Accountable fixo em toda linha de risco.** Nenhum agente decide sozinho
> nada que caia nas classes de risco de alteração/exclusão/externa/irreversível
> (`principios-maestro.md`, Princípio III) — ver §8.

## 5. Cerimônias e cadência

Adotamos o **esqueleto Shape Up + Kanban**, não o Scrum. Cortamos daily e sprint
planning (cerimônia de papel para um solo). Trabalho em **fluxo contínuo com WIP
limitado a uma feature/spec por vez**, organizado em **ciclos com apetite fixo**.

| Cerimônia | Cadência | Quem | Propósito | Saída |
|---|---|---|---|---|
| **Shaping / Spec** | Por feature | Humano + spec/plan-agent | Definir apetite, escopo e critérios de aceite testáveis; é o "planning" real | `spec.md` aprovada |
| **Execução do ciclo** | Contínua (apetite fixo) | Orquestrador + agentes | Implementar com escopo variável dentro do apetite; parar ao estourar o apetite, não ao "terminar tudo" | PRs mergeados |
| **Checkpoint de ciclo** | Fim de cada ciclo | Humano | Inspecionar o que entrou; decidir cooldown/próxima aposta | Decisão de próxima spec |
| **Cooldown** | Após o ciclo | Humano + agentes | Dívida técnica, manutenção, bugs pequenos (raia leve, §3), curadoria de skills | — |
| **Retro individual** | Fim de cada ciclo | Humano | O que os agentes erraram de forma recorrente → vira regra | Regra em `CLAUDE.md`/constituição/ADR |

> **A retro é a cerimônia de maior ROI neste modelo.** Cada correção recorrente que
> você faz num agente deve virar **instrução versionada** (`CLAUDE.md`, skill, ou
> emenda de constituição). O processo aprende; você não repete a mesma correção.

**Apetite (Shape Up)**: o ciclo tem tempo fixo e escopo variável — o oposto de estimar
prazo. Casa direto com YAGNI e "diffs pequenos": quando o apetite acaba, corta-se
escopo, não se estende o prazo.

## 6. Entregáveis e artefatos

Catálogo dos artefatos do ciclo de vida, com **dono**, **gate** e **onde vive**.
"Essencial" = obrigatório agora; "Fase 2/YAGNI" = observado, não adotado (§10).

| Artefato | Dono | Onde vive | Gate | Status |
|---|---|---|---|---|
| **Brief / intenção** | Humano | issue/spec header | — | Essencial |
| **Spec** (`spec.md`) | Spec-agent | `specs/NNN-*/` | Humano aprova (DoR) | Essencial (raia plena) |
| **Plan** (`plan.md`) + Constitution Check | Plan-agent | `specs/NNN-*/` | Humano aprova | Essencial (raia plena) |
| **UX design** (`ux-design.md`) | UX-agent | `specs/NNN-*/` | Objeto semântico (P. VII) | Essencial (se UI) |
| **Tasks** (`tasks.md`) | Plan-agent | `specs/NNN-*/` | — | Essencial (raia plena) |
| **Spec de infra** | Humano + agente | `specs/NNN-*/` | Sempre raia plena + gates de reversibilidade (§7) | Essencial (infra/migração) |
| **Código + testes** | Dev-agent | `apps/` | Testes + fitness functions verdes | Essencial |
| **ADR** | Tech Writer-agent | `docs/adr/NNNN-*.md` | Decisão arquitetural registrada | Essencial (por decisão) |
| **Journey doc** | Tech Writer-agent | `docs/journeys/NNN-*.md` | Capturas + heurística no mesmo PR (P. VII) | Essencial (se jornada) |
| **Runbook** | Humano + agente | `docs/infra/` | Estratégia de rollback documentada | Essencial (infra) |
| **Changelog / release notes** | Tech Writer-agent | `CHANGELOG.md` | Atualizado no PR de release | **A formalizar** |
| **Definition of Ready/Done** | Humano | este doc (§7) | Checklist verificável | Essencial (este doc) |
| **PR** | Dev-agent | GitHub | Gate de merge (§7); **na raia leve, o PR é o próprio artefato** | Essencial |
| **C4 diagrams** | — | `docs/architecture/` | — | Fase 2 / YAGNI |
| **RFC process pesado** | — | — | — | YAGNI (ADR basta) |
| **Painel de métricas DORA** | — | — | — | Fase 2 / YAGNI |

## 7. Definition of Ready e Definition of Done

Escritas como **checklists verificáveis** — um agente consegue satisfazê-las e um
Stop-hook/`/goal` consegue conferi-las. A DoR aplica-se à **raia plena** (§3); a raia
leve entra direto na execução com a **DoD reduzida** indicada abaixo.

### Definition of Ready (uma spec pode entrar em execução? — raia plena)
- [ ] `spec.md` descreve **o quê e por quê** com critérios de aceite **testáveis**.
- [ ] Ambiguidades resolvidas (`/speckit.clarify`) ou registradas.
- [ ] `plan.md` passou pelo **Constitution Check** (violação → justificada ou removida).
- [ ] `ux-design.md` declara papéis/objetos semânticos consumidos/introduzidos (se UI).
- [ ] **Apetite** definido (tempo fixo do ciclo).

### Definition of Done (uma feature está pronta?)
- [ ] Testes verdes: unitário de domínio + contrato por porta + integração por rota.
- [ ] **Fitness functions** (regras de dependência DDD/hexagonal) verdes no CI (P. V).
- [ ] Lint + typecheck limpos.
- [ ] **Revisão independente** (`/code-review` em contexto fresco) sem lacunas de
      correção/requisito abertas.
- [ ] **Gate de segurança leve**: secret scanning limpo; revisão de injeção/autorização
      onde aplicável (P. IV).
- [ ] **Documentação viva atualizada no mesmo PR**: journey (capturas + heurística),
      ADR se houve decisão, changelog.
- [ ] **Rastreabilidade** registrada: spec NNN ↔ PR ↔ testes ↔ journey (§9).
- [ ] Evidência anexada (output de teste/build/screenshot) — "prove, não declare".

**DoD reduzida (raia leve, §3)**: valem os itens de testes, fitness functions, lint/
typecheck e **revisão independente**; dispensam-se os artefatos de planejamento e a
doc viva **exceto** se a mudança tocar uma jornada. Bug **exige um teste que o
reproduz** antes do fix.

### Bloco obrigatório para ações irreversíveis (raia infra, §3)
Além da DoD acima, toda ação irreversível (migração destrutiva, deploy, exclusão de
dados) exige — materializando a "reversibilidade engenheirada":
- [ ] **backup/snapshot** antes de qualquer ação destrutiva;
- [ ] **dry-run + validação em staging** antes da produção;
- [ ] **estratégia de rollback** documentada no runbook (soft-delete quando aplicável);
- [ ] **aprovação humana explícita** (classe de risco "financeira/irreversível", §8).

## 8. Mapa de gates humanos inegociáveis

Reaproveita a **taxonomia de classes de risco** de `principios-maestro.md` (Princípio III — classes de risco). O
agente age sozinho em risco baixo; o humano **DEVE** aprovar a partir de "alteração".

| Classe de risco | Exemplo | Agente pode sozinho? | Gate humano |
|---|---|---|---|
| Leitura | Ler código, buscar, explorar | ✅ Sim | Não |
| Leitura sensível | Dados com PII/segredos | ⚠️ Com política + mascaramento | Revisão |
| Criação reversível | Nova feature em branch, rascunho | ✅ Sim | Merge |
| **Alteração** | Refactor amplo, mudança de contrato | ❌ Não | **Aprovação com resumo** |
| **Exclusão / ação externa** | Apagar dados, chamar API externa, push | ❌ Não | **Confirmação forte** |
| **Financeira / irreversível** | Deploy em produção, migração destrutiva | ❌ Não | **Dupla aprovação / reautenticação** |
| **Lote / cross-tenant / admin** | Migração em massa, ação administrativa | ❌ **Bloqueado** | **Workflow humano formal** |

Gates humanos inegociáveis, sempre: **aprovar a spec**, **aprovar o plan (Constitution
Check)**, **aprovar o merge**, **autorizar deploy/migração**. Nenhum desses é delegável
a agente.

## 9. Rastreabilidade e fluxo end-to-end

```
intenção → spec.md (NNN) → plan.md (+Constitution Check) → ux-design.md → tasks.md
   → implementação (Dev-agent) → testes + fitness functions (CI)
   → revisão independente (Review-agent) + segurança
   → docs vivas (journey/ADR/changelog) → PR → gate humano de merge → release
```

Na **raia leve** (§3) o caminho encurta para `intenção → code → teste → revisão
independente → PR (o artefato) → merge`, sem `spec/plan/tasks`.

Cada feature mantém o elo **spec NNN ↔ PR ↔ testes ↔ journey** explícito (parte da
DoD). Isso dá a rastreabilidade decisão→código→verificação que a governança leve exige,
sem ferramenta pesada.

## 10. O que NÃO adotamos (anti-processo / YAGNI)

Explicitado para evitar processo especulativo (Constituição, Governance/YAGNI):

- **Scrum completo** (Scrum Master, sprint planning, daily de time) — cerimônia de
  papel para solo+IA. Ficamos com shaping + cooldown + retro.
- **Backlog formal** — Shape Up mostra que ideias importantes voltam via re-shaping;
  não acumulamos backlog.
- **Segunda ferramenta de spec-driven (ex.: OpenSpec)** — avaliada e descartada: não
  manter duas ferramentas SDD. O que valia era a ideia do modelo *delta* para mudanças
  pequenas, absorvida como **raia leve dentro do Spec Kit** (§3).
- **RFC process pesado** — o ADR já cobre decisão + contexto + consequências.
- **C4 formal e instrumentação de métricas DORA** — hoje mermaid + linguagem-ubíqua e
  o CI verde bastam; reavaliar quando o time/escala justificar (Fase 2).
- **Estimativas de prazo** — usamos apetite (tempo fixo, escopo variável).

## 11. Evolução deste documento

Este documento é **versionado** e evolui como a Constituição: mudanças materiais
sobem versão (MINOR: novo papel/cerimônia/artefato/raia; PATCH: clarificação) e são
registradas em ADR. A **retro de ciclo** é a fonte primária de emendas — toda regra
nova nasce de um erro recorrente observado. Revisão obrigatória ao fim de cada fase
do projeto.

**Histórico**: 1.0.0 (2026-07-22, ADR 0004) fundação · 1.1.0 (2026-07-22, ADR 0005)
raias de trabalho (leve/plena/infra), spec de infra com gates de reversibilidade,
OpenSpec avaliado e descartado · 1.2.0 (2026-07-22, ADR 0006) aplicação e enforcement
(§12): PR template com a DoD, gate de CHANGELOG na CI, comando `/dod`.

## 12. Aplicação e enforcement (como garantir que o modelo é aplicado)

A garantia não vem de disciplina nem de memória — vem de **tornar cada critério
executável e bloqueante** (o próprio `[8]` aplicado ao modelo). Cada item tem um
mecanismo, dividido entre **mecânico** (hard gate, bloqueia sozinho) e **julgamento**
(checklist + aprovação humana):

| Item | Mecanismo | Onde |
|---|---|---|
| Testes + fitness functions + build/typecheck | **Hard gate (CI)** — bloqueia o merge | `.github/workflows/ci.yml` |
| Entrada no CHANGELOG | **Hard gate (CI)** — job `changelog` (bypass: label `skip-changelog`) | `ci.yml` + `CHANGELOG.md` |
| Secret scanning | **Setting nativo do GitHub** (secret scanning + push protection) | configuração do repo |
| DoD/DoR, raia, rastreabilidade, gate de risco | **Checklist obrigatório** | `.github/pull_request_template.md` |
| Self-check do agente antes de "pronto" | **Comando** `/dod` | `.claude/commands/dod.md` |
| DoR (spec pronta) + Constitution Check | **Templates spec-kit** + Constituição | `.specify/templates/`, `/speckit.plan` |
| Ler Constituição/modelo antes de agir | **Diretriz** | `CLAUDE.md` / `AGENTS.md` |

**A divisão é a mesma do `[5]`**: o que é mecânico (R/C automatizáveis) vira hard gate na
máquina; o que exige julgamento — "é a coisa certa?", classe de risco (`[9]`) — fica no
checklist do PR + aprovação humana (o A). *Pendências (follow-up)*: habilitar secret
scanning nativo; avaliar lint (ruff/eslint).
