# 019 — Gerar por scaffolding os arquivos de contexto do agente

- **Id**: `scaffolding-de-contexto`
- **Fonte**: `webdevtodayjason/context-forge`
- **Observado em**: 2026-08-01
- **Veredito no momento**: observar
- **Destino**: —
- **Gatilho de reavaliação**: —

> **Estado corrente ≠ este card.** Este card é o **momento**: registra o veredito de
> 2026-08-01 — o Apêndice C o triou como 👁. O veredito de hoje é **descartar**, reclassificado no ciclo 047 e
> registrado em [`estado.jsonl`](../estado.jsonl) numa linha nova, datada de 2026-08-10.
> O card não é reescrito: mudar de ideia é legítimo, apagar o registro de que se pensava
> diferente não é.

## A ideia

Uma CLI que gera `CLAUDE.md`, PRD e regras do projeto a partir de um questionário, para
começar rápido.

## Por que atravessa (ou não)

O Maestro já resolve isto, e resolve melhor para o próprio problema: o
`install-maestro.sh --block` **gera a instrução a partir do disco**, lendo as skills que
existem de verdade. Um gerador por questionário produz uma lista escrita à mão, que envelhece
em silêncio — que foi exatamente a falha do ciclo 021, corrigida pelo ADR 0013. Adotar seria
reintroduzir o defeito que já custou um ciclo.

## Dimensões

| # | Dimensão | Leitura |
|---|---|---|
| 1 | Conflito com princípio | sim: reintroduz lista escrita à mão contra o Princípio VI (ADR 0013) |
| 2 | Licença e redistribuição | MIT |
| 3 | Função já servida | **sim, e melhor**: instrução gerada do disco |
| 4 | Custo de contexto | uma dependência de CLI |
| 5 | Reversibilidade | alta |
| 6 | Maturidade e evidência | leitura do repositório |
| 7 | Dor real hoje | não |
