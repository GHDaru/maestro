# Handbook do Modelo Operacional — Fundamentos por elemento

> Manual de referência dos elementos do modelo operacional
> (`docs/governance/modelo-operacional.md`). **Um capítulo por elemento**, cada um com
> a mesma anatomia: fundamentação teórica → frameworks avaliados → recomendação de uso
> no nosso contexto (1 humano orquestrando N agentes de IA).
>
> Este handbook é **didático e fundamentado**; complementa — não substitui — os outros
> três documentos:
>
> | Documento | Papel |
> |---|---|
> | `governance/modelo-operacional.md` | **Normativo** — a regra vigente (o quê é obrigatório) |
> | `handbook/` (aqui) | **Fundamentos** — por que a regra é essa; teoria + frameworks + recomendação |
> | `research/jornada-aprendizado-modelo-operacional.md` | **Diário** — os insights construídos ao criticar cada elemento |
> | `research/resultado-pesquisa-*-avaliacao.md` | **Pesquisa** — a síntese citada que embasa tudo |

## Anatomia obrigatória de cada capítulo (7 seções)

1. **Pergunta central** — a pergunta que o capítulo responde.
2. **Fundamentação teórica** — o conceito, sua origem e o princípio que o sustenta.
3. **Frameworks / abordagens avaliados** — o que existe lá fora, comparado, com veredito.
4. **Recomendação de utilização** — como aplicamos no contexto 1 humano + N agentes;
   ligação com o `modelo-operacional.md` e com a Constituição.
5. **Conexões** — como o elemento se liga aos demais capítulos.
6. **Insight da jornada e impacto no modelo** — o que refinamos ao avaliar criticamente
   e o efeito normativo (ADR/versão), com link ao diário.
7. **Fontes** — citadas, com data.

## Índice (ordem de leitura = ordem de dependência)

| Cap. | Elem. | Título | Resumo (ideia central) |
|---|---|---|---|
| 01 | `[1]` | [Princípio operacional central](01-principio-central.md) | IA escreve · humano decide/aprova · verificação independente valida. O que torna o **irreversível** seguro de delegar é a **reversibilidade engenheirada**. |
| 02 | `[10]` | [Evidência: DORA/SPACE](02-dora-space.md) | Velocidade e estabilidade **não são trade-off**. Alavanca: **lote pequeno + reversibilidade**. Bússola, não painel. |
| 03 | `[2]` | [Spec-Driven](03-spec-driven.md) | A **spec é a fonte de verdade** (input que gera código, não descrição). Raias leve/plena/infra por `ambiguidade × raio × irreversibilidade`. |
| 04 | `[3]` | [Fluxo agentic e economia de contexto](04-fluxo-agentic-contexto.md) | `explore→plan→code→commit` + subagentes + `/clear` + revisor fresco = **economia de contexto**. A spec é o contexto integrador. |
| 05 | `[4]` | [Orquestração de agentes](05-orquestracao.md) | **Map-reduce cognitivo**: reduce do orquestrador; corte nas costuras (bounded contexts). Espectro workflow↔agent; **menor autonomia que resolve**. |
| 06 | `[5]` | [Papéis e RACI](06-papeis-raci.md) | Papéis como modos. Delega-se **R/C/I; nunca o A**. Humano Accountable **pela política/gates/critérios — não por item**. |
| 07 | `[6]` | [Cerimônias e cadência](07-cerimonias-cadencia.md) | Cerimônia = **função**, não reunião. **Retro amplificada** por agentes. **WIP = atenção humana**. Shape Up + Kanban. |
| 08 | `[7]` | [Entregáveis e artefatos](08-entregaveis-artefatos.md) | Artefato vive se é **input consumido com forcing function** (ou imutável, como o ADR). Não duplicar função já servida. |
| 09 | `[8]` | [Definition of Ready / Done](09-definition-of-ready-done.md) | "Done" precisa ser **verificável autonomamente**; converter **julgamento em check**. **Verde ≠ certo** — global fica com o humano. |
| 10 | `[9]` | [Gates e classes de risco](10-gates-classes-de-risco.md) | Gate **proporcional** a `irreversibilidade × impacto`. Uniforme = funil ou catástrofe. **Reversibilidade rebaixa a classe**. |
| 11 | `[11]` | [Rastreabilidade](11-rastreabilidade.md) | `spec ↔ PR ↔ teste ↔ journey` = **memória durável** (sobrevive ao reset do agente). **Emerge** do workflow, sem ferramenta. |
| 12 | `[12]` | [Governança leve](12-governanca-leve.md) | **Aprende sem inchar**: núcleo firme + periferia evoluível + **YAGNI**. A jornada *foi* o loop de governança em ação. |

> **Nota**: o número do capítulo (ordem de leitura) ≠ o rótulo do elemento `[x]`
> (nossa linguagem compartilhada na jornada). A tabela mapeia os dois.

## Formatos

- 📄 **PDF completo** (livro A4, capa + 12 capítulos): [`maestro-handbook.pdf`](maestro-handbook.pdf)
- 🎼 Apresentação **executiva** (HTML): [`apresentacao-executiva-maestro.html`](apresentacao-executiva-maestro.html)
- 📐 Caderno **técnico** (HTML): [`apresentacao-tecnica-maestro.html`](apresentacao-tecnica-maestro.html)
