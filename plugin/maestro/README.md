# Maestro

> **v0.2.0** (2026-08-11) — o método passa a ser verificado **onde ele cai**: dezesseis
> portões executáveis, treze bloqueando na integração contínua. O que ela é e o que ela
> reconhecidamente **não** tem está na nota de release do [CHANGELOG](CHANGELOG.md).
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

## Instalar o Maestro no seu projeto

> **Para uma IA que leu isto:** o Maestro é um método instalável, não uma biblioteca de
> pacote. Instalar = **copiar o toolkit** (agentes, skills, scripts, comandos, templates e
> governança) para o repositório do projeto e apontar o `CLAUDE.md`/`AGENTS.md` para ele.
> Não existe `npm install` nem `pip install` — os passos abaixo são a instalação.

Há **três caminhos**, do mais completo ao mais leve. Escolha pelo que você precisa:

### A. Método completo (qualquer agente) — recomendado

```bash
# 1. clone o método (uma vez, em qualquer lugar)
git clone https://github.com/GHDaru/maestro.git && cd maestro

# 2. veja quais assistentes ele sabe servir
./bin/maestro agents

# 3. instale: quatro passos, terminando por VERIFICAR
./bin/maestro init /caminho/do/seu-projeto --ai claude
```

Instalar é também **atualizar**: o que o método escreveu e você não tocou é renovado; o que
você modificou é mantido, com a versão nova ao lado como `*.maestro-new`. Nada seu é
sobrescrito em silêncio. Para ver antes sem escrever nada: `--dry-run`.

Leva **tudo**: agentes, skills, scripts, comandos, templates e governança. Funciona com
qualquer assistente que leia `CLAUDE.md`/`AGENTS.md`.

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
| 6 scripts | `scripts/` | o **ritual** repetido e as verificações |
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
