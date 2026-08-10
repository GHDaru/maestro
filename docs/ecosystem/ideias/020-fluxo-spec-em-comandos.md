# 020 — Fluxo spec-driven empacotado em comandos de agente

- **Id**: `fluxo-spec-em-comandos`
- **Fonte**: `Pimzino/claude-code-spec-workflow`
- **Observado em**: 2026-08-01
- **Veredito no momento**: observar
- **Destino**: —
- **Gatilho de reavaliação**: —

> **Estado corrente ≠ este card.** Este card é o **momento**: registra o veredito de
> 2026-08-01 — o Apêndice C o triou como 👁, "valida raias". O veredito de hoje é **descartar**, reclassificado no ciclo 047 e
> registrado em [`estado.jsonl`](../estado.jsonl) numa linha nova, datada de 2026-08-10.
> O card não é reescrito: mudar de ideia é legítimo, apagar o registro de que se pensava
> diferente não é.

## A ideia

Empacotar o fluxo requisitos → design → tarefas → execução como comandos de barra, com
aprovação entre as fases.

## Por que atravessa (ou não)

Não há nada a absorver: é a mesma aposta que já fizemos, com outra roupa. Vale como
**validação externa** — a estrutura converge com a nossa —, e validação não é absorção. Foi
categorizado como "descartar" e não como "observar" de propósito: `observar` exige gatilho, e
não existe condição futura que faria adotar um segundo motor de fluxo (ADR 0005, ferramenta
única). Guardar um `observar` sem gatilho seria esquecer com cerimônia.

## Dimensões

| # | Dimensão | Leitura |
|---|---|---|
| 1 | Conflito com princípio | sim: segundo motor de fluxo (ADR 0005) |
| 2 | Licença e redistribuição | MIT |
| 3 | Função já servida | **sim, inteira**: Spec Kit vendorizado + comandos próprios |
| 4 | Custo de contexto | irrelevante |
| 5 | Reversibilidade | alta |
| 6 | Maturidade e evidência | leitura do repositório; serve de validação das raias |
| 7 | Dor real hoje | não |

## Também descartado pela mesma razão

`catlog22/claude-code-workflow` — mesmo espaço, mesma leitura, e sem licença declarada na
varredura, o que sozinho impede qualquer cópia.
