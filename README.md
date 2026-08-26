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

Duas situações diferentes, e a primeira coisa a fazer é saber em qual você está:

- **Vim instalar o Maestro em outro projeto** → pule para
  **[Instalar o Maestro no seu projeto](#instalar-o-maestro-no-seu-projeto)**. Nada aqui
  precisa ser lido antes; o comando está na primeira linha da seção, e ele já vem na forma
  que funciona sem terminal.
- **Vim trabalhar no método, neste repositório** → é o resto desta seção. Leia antes de
  escrever qualquer coisa: não é o método, é como se comportar **aqui**.

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

> **Se você é a IA encarregada de instalar:** o Maestro é um método **instalável**, não um
> pacote. Não existe `npm install` nem `pip install`. Instalar é copiar o toolkit — agentes,
> skills, scripts, comandos, templates e governança — para o repositório do projeto e
> **apontar o `CLAUDE.md`/`AGENTS.md` para ele**. As duas metades contam: copiar sem apontar
> deixa arquivos que ninguém lê, e o verificador reprova.

### O comando — inclusive para quem roda sem terminal

```bash
git clone https://github.com/GHDaru/maestro.git /tmp/maestro
cd /caminho/do/meu-app
/tmp/maestro/bin/maestro init . --ai claude --yes
```

**`--yes` não é conveniência.** `init` faz quatro perguntas e, **sem terminal e sem `--yes`,
sai com código 2 sem escrever nada** — `maestro: no terminal to ask about which agent`.
Sessão de agente não tem terminal: sem essa flag, a instalação não acontece e o erro não se
parece com um erro de instalação. Toda pergunta é flag exatamente por isso.

**O alvo é o seu projeto, nunca o clone.** O clone é a ferramenta; nada é instalado dentro
dele. Caminho relativo vale a partir de onde **você** está — daí o `cd` antes do comando.
Rodar os portões de dentro do clone devolve verde sobre o repositório *do método*, não sobre
o seu.

### As flags que decidem a instalação

| Flag | O que faz | Quando você precisa |
|---|---|---|
| `--ai <id>` | escolhe o agente; **recusa** um id que não conhece | sempre — sem ela, assume `claude` |
| `--yes` | aceita o padrão do que não foi declarado | sempre que não houver terminal (CI, sessão de agente) |
| `--dry-run` | mostra o que faria e **não escreve nada** | antes de instalar num repositório alheio |
| `--no-hooks` | instala sem a camada de aplicação | o agente não é Claude Code, ou você não quer os hooks |
| `--force` | adota a versão do método de um arquivo que você alterou, salvando o seu antes | conflito consciente, numa atualização |

### Os ids que o `--ai` aceita

| `--ai` | Agente | Arquivo que ele lê | Comandos | Camada de hooks |
|---|---|---|---|---|
| `claude` | Claude Code | `CLAUDE.md` | `.claude/commands` | **sim** |
| `copilot` | GitHub Copilot | `.github/copilot-instructions.md` | — | não |
| `cursor-agent` | Cursor | `.cursor/rules/specify-rules.mdc` | — | não |
| `codex` | Codex CLI · Amp, opencode, Kiro, Bob, Pi | `AGENTS.md` | — | não |

`—` em comandos significa que **não verificamos** o formato daquele agente, então nada é
instalado ali; hooks são mecanismo do Claude Code, e o instalador **diz** quando não instalou
a camada. Para ver a mesma tabela sem escrever nada: `maestro agents`.

### O que cai no seu projeto

| Camada | Vai para | Papel |
|---|---|---|
| 13 subagentes | `.claude/agents/` | **quem faz** cada papel (inclui UX/semântica) |
| 6 skills | `skills/` | **como fazer** (cada uma com sua Iron Law) |
| 13 scripts, dos quais 9 portões | `scripts/` | o **ritual** repetido e as verificações |
| 12 comandos + 12 templates | `.claude/commands/`, `.specify/templates/` | o **motor** spec-driven |
| governança | `docs/governance/` | a **fonte de verdade** |

A árvore completa, arquivo por arquivo, está na receita:
**[o que fica no seu projeto depois](docs/receitas/instalar-o-maestro.md#o-que-fica-no-seu-projeto-depois)**.

### Prove que instalou — e só então diga que instalou

```bash
cd /caminho/do/meu-app
scripts/check-install.sh
```

Código 0 é a única evidência que conta. Esse portão reprova enquanto o `CLAUDE.md` não
apontar para o método — é ele que mede a segunda metade da instalação. O próprio `init` já o
roda ao final e **sai diferente de zero se ele falhar**: instalar sem provar não conta.

Depois disso, o primeiro ciclo:

```bash
scripts/new-cycle.sh 001 primeiro-ciclo
```

### Instalar é também atualizar

Rodar `init` de novo renova o que o método escreveu e você não tocou, e **mantém** o que você
modificou, deixando a versão nova ao lado como `*.maestro-new`. Nada seu é sobrescrito em
silêncio. Para ver antes sem escrever nada: `--dry-run`.

### Os outros dois caminhos, menores

| Caminho | Leva | Quando |
|---|---|---|
| **Plugin do Claude Code** — `/plugin marketplace add GHDaru/maestro` e depois `/plugin install maestro@ghdaru-maestro` | os 13 subagentes, 6 skills e os comandos, já namespaced; atualiza sozinho | você usa Claude Code e quer só isso |
| **Só as skills** — `npx skills add GHDaru/maestro` | as 6 skills, em Claude Code, Cursor, Codex, Copilot, Cline e outros | quer a fatia menor, em qualquer assistente |

Nenhum dos dois traz scripts nem governança — ou seja, **não trazem os portões**. Para o
método inteiro, é o `init` acima.

**Passo a passo detalhado, um comando por vez**: [receita de instalação](docs/receitas/instalar-o-maestro.md).

---

## Estrutura

| Camada | Onde | Papel |
|---|---|---|
| **Comece por aqui** | [`docs/comece-por-aqui.md`](docs/comece-por-aqui.md) | porta de entrada narrativa (dor → jornada → sistema) |
| **Glossário** | [`docs/governance/glossary.md`](docs/governance/glossary.md) | dicionário de todas as siglas |
| **Princípios** | [`docs/governance/principles.md`](docs/governance/principles.md) | inegociáveis da metodologia (constituição do Maestro) |
| **Modelo operacional** | [`docs/governance/operating-model.md`](docs/governance/operating-model.md) | a regra vigente: papéis, cerimônias, artefatos, raias, gates |
| **Handbook** | [`docs/handbook/`](docs/handbook/README.md) | fundamentos por elemento — 13 capítulos (teoria + frameworks + recomendação) |
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
