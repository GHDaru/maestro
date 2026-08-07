# Plano 041 — Retro: os quatro achados de eval viram regra

- **Spec**: `spec.md` · **Raia**: plena · **Data**: 2026-08-07

## Constitution Check (governance/principles.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-driven | Spec antes; os cinco FR saíram dos achados, não de ideias novas. |
| II. Orquestração governada | A retro decide o que vira regra; o que tem duas amostras vira **gatilho**, não regra — mexer num agente com pouca evidência seria a IA decidindo por conta. |
| III. Reversibilidade / gates | Classe baixa: texto, campos e um script. Nada apagado — o caso 002 é **aposentado**, não removido. |
| IV. Test-first / DoD verificável | As três condições novas do `check-evals.sh` foram vistas acusando antes de virarem verdade. |
| V. Economia de contexto / fronteira | A retro fecha os quatro achados e para. O terceiro caso de eval, a remoção da linha do agente e os dois achados pequenos ficaram fora, por escrito. |
| VI. Artefatos vivos | O achado central é deste princípio: o `retro.sh` era artefato consumido que mentia — pior que documentação morta, porque tinha crédito. |
| VII. Governança leve / YAGNI | Três anti-padrões e quatro campos. Nenhuma ferramenta nova. |
| VIII. Comunicação inteligível | Siglas por extenso na primeira ocorrência de cada artefato novo. |

## Como

**1. O `retro.sh`.** Trocar "existe id no formato `gate-NNN-*`" por "existe commit na linha
principal citando o ciclo". A correção **quebrou na primeira tentativa** por um motivo que
virou regra: `git log | grep -q` sob `pipefail` — o `grep -q` sai no primeiro acerto, o
`git log` leva SIGPIPE e o pipeline reporta falha, então a condição lê "não achou". Esse
mesmo bug já tinha matado o `check-cycle.sh`. Segunda ocorrência ⇒ vira anti-padrão 21.

**2. Os achados viram forma, não conselho.** Cada um vira campo obrigatório, porque conselho
depende de memória:

| Achado | Vira |
|---|---|
| caso 002 não discrimina | anti-padrão 19 + `Axis:` no `case.md` + `Ablation:` na linha de base |
| fixtures com defeito | anti-padrão 20 + `Premise-checked:` + pré-voo obrigatório no `/eval` |
| raia sobredeterminada | **gatilho no roadmap** — duas amostras não mexem num agente |
| linhas de base pendentes | fechado: 001 provado, 002 aposentado |

**3. A aposentadoria, desenhada contra o abuso.** É a única forma de um caso sair do
vermelho sem ser provado, então: exige `Retired-because:`, é **impressa** em toda execução
e é contada à parte (`retired: 1`). O verde passa a dizer "um provado, um aposentado".

**4. A forma que faltava no índice.** O `fecha` auto-referente apareceu duas vezes — ciclos
039 e 041, a segunda enquanto se retrospectava a primeira. Não é desatenção: o protocolo não
oferecia forma para "achado encontrado e corrigido no mesmo ciclo". Agora oferece.

## Verificação (DoD)

```bash
scripts/retro.sh          # zero gates pendentes falsos
scripts/check-evals.sh    # 1 provado + 1 aposentado, 0 pendentes
scripts/check-retro.sh    # dívida zero
```

Prova de que o portão acusa: três injeções (aposentar sem motivo; caso sem `Axis`; linha de
base sem `Ablation`), com a saída no `qa-report.md`.
