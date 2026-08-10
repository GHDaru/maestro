# 35 — Contrato de entrada e saída declarado por fatia

- **Id**: `contrato-por-fatia`
- **Fonte**: `Padrões de fatiamento (Lawrence) + SPIDR`
- **Observado em**: 2026-08-06
- **Veredito no momento**: absorver
- **Destino**: —
- **Gatilho de reavaliação**: dois ou mais agentes trabalhando em fatias da mesma intenção ao mesmo tempo

## A ideia

Cada fatia declara o que consome e o que entrega, para que fatias paralelas possam ser trabalhadas sem que uma descubra a outra tarde demais.

## Por que atravessa (ou não)

Registrado como "vira campo obrigatório" — e nenhum template ganhou o campo. Como [003](003-worktree-por-task.md), é uma ideia sobre **paralelismo** numa metodologia cujo WIP é limitado pela atenção de um humano: a dor é a mesma que ainda não existe.

## Dimensões

| # | Dimensão | Leitura |
|---|---|---|
| 1 | Conflito com princípio | nenhum |
| 2 | Licença e redistribuição | literatura: ideia livre, texto não |
| 3 | Função já servida | não |
| 4 | Custo de contexto | um campo por fatia |
| 5 | Reversibilidade | total |
| 6 | Maturidade e evidência | maduro na origem; sem uso nosso |
| 7 | Dor real hoje | **não**: sem paralelismo real, não há contrato a violar |
