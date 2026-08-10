# 018 — Orquestrar uma frota de agentes

- **Id**: `frota-de-agentes`
- **Fonte**: `kennyjpowers/claude-flow`
- **Observado em**: 2026-08-01
- **Veredito no momento**: descartar
- **Destino**: —
- **Gatilho de reavaliação**: existir trabalho paralelo real que a atenção de **um** humano consiga governar — a condição é o humano, não a máquina

> **Estado corrente ≠ este card.** Este card é o **momento**: registra o veredito de
> 2026-08-01 — o Apêndice C o triou como ⛔ ("por ora", com reavaliação prevista). O veredito
> de hoje é **observar**, reclassificado no ciclo 047 e
> registrado em [`estado.jsonl`](../estado.jsonl) numa linha nova, datada de 2026-08-10.
> O card não é reescrito: mudar de ideia é legítimo, apagar o registro de que se pensava
> diferente não é.

## A ideia

Coordenar dezenas de agentes simultâneos com topologia, filas e supervisão automática.

## Por que atravessa (ou não)

Bate de frente com o axioma A2: consequência precisa de dono, e dono é humano. WIP no
Maestro é limitado pela **atenção humana**, não pela capacidade de execução — uma frota
produz mais trabalho do que um humano consegue julgar, e trabalho não julgado é dívida
disfarçada de velocidade. Não é "cedo demais": é uma escolha de fundo, e o gatilho registra
o que teria de mudar para reabri-la.

## Dimensões

| # | Dimensão | Leitura |
|---|---|---|
| 1 | Conflito com princípio | **sim**: Princípio II e axioma A2 (dono da consequência) |
| 2 | Licença e redistribuição | MIT |
| 3 | Função já servida | não |
| 4 | Custo de contexto | alto |
| 5 | Reversibilidade | média |
| 6 | Maturidade e evidência | leitura do repositório; sem uso nosso |
| 7 | Dor real hoje | **não**: o gargalo é o julgamento humano, e frota não o alarga |
