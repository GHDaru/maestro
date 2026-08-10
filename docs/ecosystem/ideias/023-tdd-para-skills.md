# 023 — Skill testada como código (linha de base + pressão)

- **Id**: `tdd-para-skills`
- **Fonte**: `obra/superpowers`
- **Observado em**: 2026-07-31
- **Veredito no momento**: absorver
- **Destino**: `.claude/agents/skill-author.md`
- **Gatilho de reavaliação**: —

## A ideia

Escrever a skill é escrever documentação executável: mede-se o comportamento **sem** ela
(linha de base), aplica-se pressão para que o agente a desobedeça, e só então ela está
pronta. TDD aplicado a prosa.

## Por que atravessa (ou não)

É o ancestral direto do que virou `evals/` no ciclo 037 (teorema T7 e corolário C11): saída
que não se compara por igualdade precisa de linha de base registrada. Absorvida como
protocolo no agente que escreve skills.

## Dimensões

| # | Dimensão | Leitura |
|---|---|---|
| 1 | Conflito com princípio | nenhum; serve o Princípio IV |
| 2 | Licença e redistribuição | MIT na origem; protocolo reimplementado |
| 3 | Função já servida | não à época |
| 4 | Custo de contexto | baixo |
| 5 | Reversibilidade | total |
| 6 | Maturidade e evidência | no `skill-author` desde o ciclo 011; evoluiu para `evals/` no 037 |
| 7 | Dor real hoje | sim: skill escrita e nunca verificada |
