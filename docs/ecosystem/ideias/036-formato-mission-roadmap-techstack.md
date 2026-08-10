# 36 — Upstream mínimo em três documentos (mission, roadmap, tech-stack)

- **Id**: `formato-mission-roadmap-techstack`
- **Fonte**: `buildermethods/agent-os`
- **Observado em**: 2026-08-06
- **Veredito no momento**: absorver
- **Destino**: `docs/roadmap.md`
- **Gatilho de reavaliação**: —

## A ideia

Acima da spec, três documentos curtos e estáveis: para onde vamos, o que está no caminho, e sobre o que construímos. O item do roadmap liga-se ao ciclo que o entrega.

## Por que atravessa (ou não)

Foi absorvido o **formato**, não a ferramenta: o roadmap do Maestro tem exatamente a coluna que liga fase → spec do ciclo que a entregou, que era a parte apontada como faltante. Mission e tech-stack não foram criados e não fazem falta num repositório cujo produto é o próprio método.

## Dimensões

| # | Dimensão | Leitura |
|---|---|---|
| 1 | Conflito com princípio | nenhum |
| 2 | Licença e redistribuição | MIT na origem; formato reimplementado |
| 3 | Função já servida | parcialmente: o roadmap já existia, sem a ligação item ↔ ciclo |
| 4 | Custo de contexto | baixo |
| 5 | Reversibilidade | total |
| 6 | Maturidade e evidência | a coluna existe e é atualizada a cada ciclo desde o 002 |
| 7 | Dor real hoje | sim: fase entregue sem rastro de qual ciclo a entregou |
