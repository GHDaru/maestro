# 31 — O motor spec-driven adotado

- **Id**: `spec-kit`
- **Fonte**: `github/spec-kit`
- **Observado em**: 2026-07-28
- **Veredito no momento**: adotar
- **Destino**: `.specify/UPSTREAM.md`
- **Gatilho de reavaliação**: —

## A ideia

Fluxo spec → plan → tasks como comandos de agente, com templates versionados e scripts de apoio. É a **única ferramenta de terceiro adotada** pelo Maestro, e a decisão mais consequente do método.

## Por que atravessa (ou não)

Estava fora do catálogo na primeira versão, sob o argumento de que `.specify/UPSTREAM.md` já registra a proveniência. Mas proveniência responde *o que foi vendorizado*, não *por que foi escolhido* — e um catálogo que responde tudo menos a decisão mais importante não responde nada. O `UPSTREAM.md` continua sendo o registro de linhagem; este card é a avaliação.

## Dimensões

| # | Dimensão | Leitura |
|---|---|---|
| 1 | Conflito com princípio | nenhum — dá forma ao Princípio I; a regra de 'uma ferramenta SDD só' (ADR 0005) existe justamente para protegê-lo |
| 2 | Licença e redistribuição | MIT, e desde o ciclo 046 atribuído com titular em `THIRD-PARTY-NOTICES.md` |
| 3 | Função já servida | não: era a lacuna central |
| 4 | Custo de contexto | os templates são carregados a cada ciclo — é o maior custo fixo de contexto do método, e aceito |
| 5 | Reversibilidade | média: os artefatos são markdown nosso, mas os comandos e scripts vieram do upstream. A divergência é declarada em `UPSTREAM.md`, nunca silenciosa |
| 6 | Maturidade e evidência | 47 ciclos de uso próprio, com um fork da casa para o comando `converge` |
| 7 | Dor real hoje | sim, desde o ciclo 001 |
