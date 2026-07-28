# Maestro

> **Metodologia de engenharia de software com 1 humano regendo N agentes de IA.**
> Um humano rege · muitos agentes executam · a spec é a partitura · os gates, o compasso.

Maestro **não** é "a IA escreve código". É **orquestração governada**: a especificação é
a fonte de verdade, os agentes executam em paralelo, e o humano decide, aprova e verifica.
A tese: humano + IA, com a metodologia certa, entrega o que antes exigia dúzias de
pessoas — mais rápido e com artefatos que não apodrecem — sobretudo em **sistemas legados**.

Este repositório é o **lar da metodologia**, evoluído de forma independente (origem:
prática consolidada em `ghdaru` e `flowbuilder`; ver `docs/adr/0007`).

> **Novo por aqui?** Leia primeiro o **[Comece por aqui](docs/comece-por-aqui.md)** (a
> história em 5 minutos). Dúvida em alguma sigla? → **[Glossário](docs/governance/glossario.md)**.

## Estrutura

| Camada | Onde | Papel |
|---|---|---|
| **Comece por aqui** | [`docs/comece-por-aqui.md`](docs/comece-por-aqui.md) | porta de entrada narrativa (dor → jornada → sistema) |
| **Glossário** | [`docs/governance/glossario.md`](docs/governance/glossario.md) | dicionário de todas as siglas |
| **Princípios** | [`docs/governance/principios-maestro.md`](docs/governance/principios-maestro.md) | inegociáveis da metodologia (constituição do Maestro) |
| **Modelo operacional** | [`docs/governance/modelo-operacional.md`](docs/governance/modelo-operacional.md) | a regra vigente: papéis, cerimônias, artefatos, raias, gates |
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

> **Antes de qualquer trabalho, leia `docs/governance/principios-maestro.md`.**
