# Fontes avaliadas

> Uma linha por **fonte**: onde vimos alguma coisa. O julgamento não está aqui — está nos
> [cards de ideia](ideias/), e o veredito corrente está em [`estado.jsonl`](estado.jsonl).
> Esta lista é só o endereço, e a **licença**, que decide se dá para copiar ou só citar.
>
> Contrato dos campos: `specs/047-catalogo-do-ecossistema/data-model.md`.
> Portão: `scripts/check-ecosystem.sh`.

**`citável, não copiável`** significa que a licença permite ler, aprender e citar, mas
**não** redistribuir dentro da nossa distribuição MIT. `sem licença declarada` é o pior caso
para copiar: sem licença, o padrão é *todos os direitos reservados* (ciclo 046).

| Fonte | O que é | Licença | Observado em |
|---|---|---|---|
| `github/spec-kit` | motor SDD do GitHub: spec/plan/tasks com comandos de agente | MIT | 2026-07-28 · speckit 0.4.3 |
| `Fission-AI/OpenSpec` | alternativa leve ao Spec Kit, orientada a *delta* de mudança | MIT | 2026-07-29 |
| `obra/superpowers` | biblioteca de skills + metodologia para agentes de código | MIT | 2026-07-30 |
| `bmad-code-org/BMAD-METHOD` | framework agêntico com ~12 agentes em time ágil (PM, arquiteto, dev, QA) | MIT | 2026-07-30 |
| `Kiro (AWS)` | IDE agêntica proprietária, spec-first: requirements/design/tasks, critérios em EARS | proprietária · citável, não copiável | 2026-07-30 |
| `eyaltoledano/claude-task-master` | gestor de tasks (MCP + CLI): PRD → grafo de dependências | MIT | 2026-07-30 |
| `buildermethods/agent-os` | injeção de *standards* do codebase + contexto de produto em qualquer agente | MIT | 2026-07-30 |
| `GSD (Get Shit Done)` | framework SDD de baixa cerimônia, nativo de Claude Code | sem licença declarada na varredura · citável, não copiável | 2026-07-30 |
| `Tessl` | *spec-as-source*: a spec como artefato executável, contínua | comercial · citável, não copiável | 2026-07-30 |
| `Pimzino/claude-code-spec-workflow` | fluxo spec-driven em comandos de Claude Code | MIT | 2026-08-01 |
| `catlog22/claude-code-workflow` | workflow de comandos para Claude Code | sem licença declarada na varredura · citável, não copiável | 2026-08-01 |
| `Wirasm/PRPs-agentic-eng` | *Product Requirement Prompt*: contexto de codebase empacotado na spec | MIT | 2026-08-01 |
| `webdevtodayjason/context-forge` | scaffolding de contexto (CLAUDE.md, PRD, regras) para agentes | MIT | 2026-08-01 |
| `kennyjpowers/claude-flow` | orquestração de frota de agentes (fork; upstream `ruvnet`) | MIT | 2026-08-01 |
| `CCPM` | gestão de projeto agêntica com rastreabilidade via GitHub Issues | sem licença declarada na varredura · citável, não copiável | 2026-08-01 |
| `Cline Memory Bank` | memória persistente de sessão para agentes | sem licença declarada na varredura · citável, não copiável | 2026-08-01 |
| `deanpeters/Product-Manager-Skills` | 70 skills de gestão de produto no padrão `SKILL.md` | **CC BY-NC-SA 4.0 · citável, não copiável** | 2026-08-06 |
| `GHDaru/maestro-02` | tentativa anterior do próprio método, estudada como campo | MIT (nosso) | 2026-07-31 |
| `Google ADK / Gemini Enterprise Agent Platform` | plataforma gerenciada: memória de longo prazo, delegação agente-a-agente, fluxos determinísticos | proprietária · citável, não copiável | 2026-08-01 |
| `skill decompose (comunitária)` | quebra uma feature em issues do GitHub do tamanho de um agente | sem licença declarada na varredura · citável, não copiável | 2026-08-06 |
| `Padrões de fatiamento (Lawrence) + SPIDR` | literatura sobre como cortar história/escopo, com regras de desempate | literatura · a ideia é livre, o texto não é copiável | 2026-08-06 |
| `Fatia vertical / INVEST` | a restrição que impede corte por camada | literatura · a ideia é livre, o texto não é copiável | 2026-08-06 |
| `Impact Mapping · OST · Story Mapping · Event Storming` | técnicas de descoberta e de fronteira de domínio | literatura · a ideia é livre, o texto não é copiável | 2026-08-06 |

## O que não está aqui, e por quê

- **Dependências de build** (`markdown-it` e afins): não são redistribuídas e não são ideias
  que atravessaram fronteira. Estão em `THIRD-PARTY-NOTICES.md`, que é o lugar da obrigação.
- **Artigos, posts e análises comparativas**: são fonte de garimpo, não de absorção. Quando
  uma ideia vem de um texto, o card cita o texto no campo de evidência.
- **Números de popularidade** (*stars*): apareciam nas fichas de 2026 vindos de análises de
  terceiros, nunca auditados por nós. Ordem de grandeza não é dimensão de decisão — o que
  conta é a dimensão 6, o que **nós** observamos.

## Migrado de

Esta lista consolida, sem apagar nada, o que estava espalhado em:
[ADR 0005](../adr/0005-raias-de-trabalho-e-specs-de-infra.md) ·
[ADR 0008](../adr/0008-avaliacao-ecossistema-sdd.md) ·
[ficha do ecossistema](../research/avaliacao-ecossistema-sdd.md) ·
[Apêndice C](../handbook/apendice-c-panorama-templates.md) ·
[pesquisa do upstream](../research/upstream-decomposicao.md).
