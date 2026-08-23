# Maestro

> **v0.3.0** (2026-08-22) — o método ganhou **porta de entrada**, e instalar passou a ser
> **atualizar**. Quantos portões são, quantos bloqueiam na integração contínua, e o que a
> versão reconhecidamente **não** tem: tudo na nota de release do
> [CHANGELOG](CHANGELOG.md), que é onde essa contagem vive.
>
> **Metodologia de engenharia de software com 1 humano regendo N agentes de IA.**
> Um humano rege · muitos agentes executam · a spec é a partitura · os gates, o compasso.

Maestro **não** é "a IA escreve código". É **orquestração governada**: a especificação é
a fonte de verdade, os agentes executam em paralelo, e o humano decide, aprova e verifica.
A tese: humano + IA, com a metodologia certa, entrega o que antes exigia dúzias de
pessoas — mais rápido e com artefatos que não apodrecem — sobretudo em **sistemas legados**.

Este repositório é o **lar da metodologia**, evoluído de forma independente (origem:
prática consolidada em `ghdaru` e `flowbuilder`; ver `docs/adr/0007`).

> **Novo por aqui?** Leia primeiro o **[Comece por aqui](docs/comece-por-aqui.md)** (a
> história em 5 minutos). Dúvida em alguma sigla? → **[Glossário](docs/governance/glossary.md)**.

---

## Se você é uma IA e acabou de abrir este repositório

Leia isto antes de escrever qualquer coisa. Não é o método — é como se comportar **aqui**.

**1. Não responda "estou seguindo o método?" de memória.** Rode e leia:

```bash
scripts/check-conformance.sh          # os artefatos de cada ciclo, com evidência
scripts/check-retro.sh                # dívida de achados aberta
```

Memória de agente relata **intenção**, não fato.

**2. Leia, nesta ordem, antes de agir:**

| Arquivo | O que é |
|---|---|
| [`CLAUDE.md`](CLAUDE.md) | a instrução vigente deste repositório — a sua |
| [`docs/governance/principles.md`](docs/governance/principles.md) | a constituição: oito princípios inegociáveis |
| [`docs/governance/operating-model.md`](docs/governance/operating-model.md) | a regra do dia a dia: raias, artefatos, portões |
| [`skills/anti-patterns/SKILL.md`](skills/anti-patterns/SKILL.md) | 23 erros já cometidos aqui, cada um com o ciclo de origem |

**3. Três coisas nunca são reescritas** — e um hook `PreToolUse` **recusa** a chamada, não
apenas pede:

- o corpo de um ADR já commitado → a correção é um **ADR novo** que o supersede
- `docs/records/decisoes.jsonl` → só cresce, por `scripts/record-decision.sh`
- `docs/ecosystem/ideias/*.md` → observação **datada**; o veredito de hoje é linha nova em
  `docs/ecosystem/estado.jsonl`

**4. Todo trabalho nasce de um ciclo**, e a raia decide quanto processo ele merece:

```bash
scripts/new-cycle.sh NNN <slug>       # spec.md, plan.md, tasks.md, qa-report.md
```

O `plan.md` declara os artefatos condicionais (`ART:...`), o `tasks.md` carrega a cauda de
fechamento (`TAIL:review`, `TAIL:security`, `TAIL:mutation`, `TAIL:gate`), e a **evidência**
de cada passo vai no `qa-report.md`. Caixa marcada não é testemunha.

**5. Se você criar ou alterar um portão, quebre-o de propósito e veja reprovar.** É
obrigatório (`TAIL:mutation`), e a razão está escrita: em seis dos nove ciclos 046–054 a
revisão independente encontrou um portão que media a frase e não o fato.

**6. Você não promove.** `dev` → `main` passa por `scripts/promote-main.sh` e por um humano.

## Instalar o Maestro no seu projeto

> **Para uma IA que leu isto:** o Maestro é um método instalável, não uma biblioteca de
> pacote. Instalar = **copiar o toolkit** (agentes, skills, scripts, comandos, templates e
> governança) para o repositório do projeto e apontar o `CLAUDE.md`/`AGENTS.md` para ele.
> Não existe `npm install` nem `pip install` — os passos abaixo são a instalação.

Há **três caminhos**, do mais completo ao mais leve. Escolha pelo que você precisa:

### A. Método completo (qualquer agente) — recomendado

> **O clone é a ferramenta. O alvo é outro projeto.**
> Você clona o Maestro uma vez, em qualquer lugar, e a partir dele instala o método **dentro
> do seu projeto**. Nada é instalado na pasta do Maestro.

```bash
git clone https://github.com/GHDaru/maestro.git
```

Depois, **de dentro do seu projeto** — a forma do dia a dia:

```bash
cd /caminho/do/meu-app
/onde/clonei/maestro/bin/maestro init .
```

Ou **de dentro do clone**, apontando para fora:

```bash
cd /onde/clonei/maestro
./bin/maestro init /caminho/do/meu-app
```

Caminho relativo vale a partir de onde **você** está. Cansou de digitar o caminho?
`export PATH="$PATH:/onde/clonei/maestro/bin"` e depois é só `maestro init .`.

**Um comando só instala: `init`.** Ele conduz quatro passos — agente, destino, instalação e
**verificação** — e sai com erro se a verificação falhar. Instalar sem provar não conta.

Sem `--ai`, ele instala para o **Claude Code**. Para ver as outras opções antes de decidir
(é só uma consulta, não escreve nada):

```bash
maestro agents
```

Instalar é também **atualizar**: o que o método escreveu e você não tocou é renovado; o que
você modificou é mantido, com a versão nova ao lado como `*.maestro-new`. Nada seu é
sobrescrito em silêncio. Para ver antes sem escrever nada: `--dry-run`.

#### O que aparece no seu projeto

A árvore completa, com o que cada camada é, está na receita:
**[o que fica no seu projeto depois](docs/receitas/instalar-o-maestro.md#o-que-fica-no-seu-projeto-depois)**.

Funciona com qualquer assistente que leia `CLAUDE.md`/`AGENTS.md`; os hooks são mecanismo do
Claude Code e não são instalados para os outros — e o instalador **diz** quando não instalou.

### B. Plugin do Claude Code — instala e atualiza sozinho

```
/plugin marketplace add GHDaru/maestro
/plugin install maestro@ghdaru-maestro
```

Traz os **13 subagentes, 6 skills e os comandos** já namespaced. Não traz scripts nem
governança — para o método inteiro, use o caminho A.

### C. Só as skills (75+ agentes) — padrão aberto da comunidade

```bash
npx skills add GHDaru/maestro
```

Instala as **6 skills** (`constitution-check`, `verifiable-dod`, `fight-the-pile-up`,
`anti-patterns`, `diagnose-before-fix`, `living-journey`) em Claude Code, Cursor, Codex,
Copilot, Cline e outros. É a fatia menor — sem agentes, scripts ou fluxo.

O script leva cinco camadas e imprime, ao final, o bloco pronto para colar no
`CLAUDE.md` do seu projeto:

| Camada | Vai para | Papel |
|---|---|---|
| 13 subagentes | `.claude/agents/` | **quem faz** cada papel (inclui UX/semântica) |
| 6 skills | `skills/` | **como fazer** (cada uma com sua Iron Law) |
| 13 scripts | `scripts/` | o **ritual** repetido e as verificações |
| comandos + templates | `.claude/commands/`, `.specify/templates/` | o **motor** spec-driven |
| governança | `docs/governance/` | a **fonte de verdade** |

Depois: `scripts/check-agents.sh` (deve sair com código 0) e
`scripts/new-cycle.sh 001 primeiro-ciclo`.

**Passo a passo detalhado**: [receita de instalação](docs/receitas/instalar-o-maestro.md).

---

## Estrutura

| Camada | Onde | Papel |
|---|---|---|
| **Comece por aqui** | [`docs/comece-por-aqui.md`](docs/comece-por-aqui.md) | porta de entrada narrativa (dor → jornada → sistema) |
| **Glossário** | [`docs/governance/glossary.md`](docs/governance/glossary.md) | dicionário de todas as siglas |
| **Princípios** | [`docs/governance/principles.md`](docs/governance/principles.md) | inegociáveis da metodologia (constituição do Maestro) |
| **Modelo operacional** | [`docs/governance/operating-model.md`](docs/governance/operating-model.md) | a regra vigente: papéis, cerimônias, artefatos, raias, gates |
| **Handbook** | [`docs/handbook/`](docs/handbook/README.md) | fundamentos por elemento — 12 capítulos (teoria + frameworks + recomendação) |
| **Decisões** | [`docs/adr/`](docs/adr/README.md) | ADRs (imutáveis) |
| **Pesquisa + diário** | [`docs/research/`](docs/research/) | a síntese citada e o diário de aprendizado |
| **Templates** | `.github/pull_request_template.md`, `.claude/commands/dod.md`, `.github/workflows/ci.yml` | boas práticas prontas para reuso |

## Os 12 elementos (5 camadas)

```
Fundamento   [1] Princípio central   · [10] Evidência (DORA)
Mecânica     [2] Spec-driven         · [3] Fluxo agentic     · [4] Orquestração
Estrutura    [5] Papéis (RACI)       · [6] Cadência (Shape Up)
Qualidade    [7] Artefatos · [8] DoR/DoD · [9] Gates de risco · [11] Rastreabilidade
Governança   [12] Constituição · ADRs · YAGNI
```

Índice detalhado com resumos em [`docs/handbook/README.md`](docs/handbook/README.md).

## Apresentações

- Executiva (porquê/ROI, Antes × Depois): `docs/handbook/apresentacao-executiva-maestro.html`
- Técnica (deep-dive por capítulo): `docs/handbook/apresentacao-tecnica-maestro.html`
- Prompts de imagem por slide: `docs/handbook/apresentacao-prompts-imagens.md`

## Como começar

1. Leia os **princípios** e o **modelo operacional**.
2. Consulte o **handbook** para o "porquê" de cada regra.
3. Use os **templates** (PR, `/dod`, gate de CHANGELOG) numa feature real.

> **Antes de qualquer trabalho, leia `docs/governance/principles.md`.**
