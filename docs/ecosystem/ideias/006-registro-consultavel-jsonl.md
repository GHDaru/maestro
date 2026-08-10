# 006 — Decisões num índice consultável por máquina (JSONL)

- **Id**: `registro-jsonl`
- **Fonte**: `GHDaru/maestro-02`
- **Observado em**: 2026-07-31
- **Veredito no momento**: absorver
- **Destino**: `docs/records/decisoes.jsonl`
- **Gatilho de reavaliação**: —

## A ideia

Além da prosa da decisão, um índice **append-only**, uma linha JSON por decisão, que um
agente consulta sem carregar documentos inteiros no contexto.

## Por que atravessa (ou não)

Da tentativa anterior do próprio método. Resolve uma tensão real entre o Princípio V
(economia de contexto) e a rastreabilidade: a prosa fica no ADR para quem lê, o índice fica
em JSONL para quem consulta. É também o padrão que **este catálogo reusa** para separar
momento de estado — a linha nova corrige sem apagar.

## Dimensões

| # | Dimensão | Leitura |
|---|---|---|
| 1 | Conflito com princípio | nenhum; serve o V e o XI (rastreabilidade) |
| 2 | Licença e redistribuição | material próprio (MIT) |
| 3 | Função já servida | não: havia prosa, não havia índice |
| 4 | Custo de contexto | uma linha por decisão |
| 5 | Reversibilidade | total |
| 6 | Maturidade e evidência | 98 decisões registradas; `record-decision.sh` valida a entrada |
| 7 | Dor real hoje | sim: "quais foram as últimas decisões?" exigia ler ADRs inteiros |
