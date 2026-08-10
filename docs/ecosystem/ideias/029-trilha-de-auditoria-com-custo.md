# 029 — Trilha de auditoria com custo por invocação

- **Id**: `trilha-com-custo`
- **Fonte**: `GHDaru/maestro-02`
- **Observado em**: 2026-07-31
- **Veredito no momento**: observar
- **Destino**: —
- **Gatilho de reavaliação**: alguém precisar responder "quanto custou este ciclo?" com número, e não com estimativa

## A ideia

Cada invocação de agente registra custo e tokens, formando uma trilha que responde onde o
orçamento foi gasto.

## Por que atravessa (ou não)

Era o "primeiro degrau da telemetria" no Apêndice A, e continua sendo. O registro de
decisões cobre **o que** foi decidido; custo é outra pergunta, e ninguém a fez ainda aqui.
Observar com gatilho é honesto: a instrumentação é fácil, e construí-la sem a pergunta é
YAGNI.

## Dimensões

| # | Dimensão | Leitura |
|---|---|---|
| 1 | Conflito com princípio | nenhum |
| 2 | Licença e redistribuição | material próprio (MIT) |
| 3 | Função já servida | não |
| 4 | Custo de contexto | baixo |
| 5 | Reversibilidade | total |
| 6 | Maturidade e evidência | existiu no maestro-02; não foi portado |
| 7 | Dor real hoje | **não**: ninguém pediu o número |
