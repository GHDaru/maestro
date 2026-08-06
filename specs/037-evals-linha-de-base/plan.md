# Plano 037 — Evals: linha de base para saída não-determinística

- **Spec**: `spec.md` · **Raia**: plena · **Data**: 2026-08-06

## Constitution Check (governance/principles.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-driven | Spec escrita antes; FR2–FR4 viraram literalmente as três condições do portão. |
| II. Orquestração governada | O eval **não** aprova nada sozinho: produz veredito por asserção; a leitura do veredito e a decisão continuam humanas. O agente avaliado não escreve a própria linha de base (contexto fresco, T2). |
| III. Reversibilidade / gates | Classe baixa: arquivos novos, nada apagado, nada publicado. Sem gate extra além do merge. |
| IV. Test-first / DoD verificável | O portão foi escrito antes dos casos e **visto acusar** nas três condições — evidência no `qa-report.md`. É o princípio que o ciclo inteiro serve. |
| V. Economia de contexto / fronteira | Dois casos, não treze. A fronteira é "avaliar saída de agente"; *progressive disclosure* ficou fora por não ter gatilho. |
| VI. Artefatos vivos | O caso de eval só sobrevive porque o portão o consome e falha quando defasa (T5). A linha de base é datada e amarrada ao commit do alvo. |
| VII. Governança leve / YAGNI | Nenhuma infraestrutura de eval: três arquivos de texto por caso e um script `bash`. Sem painel, sem serviço, sem chave em CI. |
| VIII. Comunicação inteligível | Sigla por extenso na primeira ocorrência em cada artefato novo (SDLC, DoD, ADR, CI); *eval* entra no glossário. |

## Como

**1. A camada de axiomas.** T7 deriva de A2 (consequência precisa de dono) e A4 (só o
escrito sobrevive), pelo mesmo caminho do T4, e vale onde o T4 não alcança: quando a saída
não se compara por igualdade, o critério precisa de **linha de base**, não de leitura
atenta. Corolário C11 dá a regra operacional: *o eval mede o alvo declarado, e defasa
quando o alvo muda*. Versão 1.0.0 → 1.1.0 (MINOR: expansão). ADR 0016 registra a emenda
e o limite.

**2. A anatomia de um caso.** Três arquivos, porque cada um responde uma pergunta distinta:

| Arquivo | Pergunta | Campos obrigatórios |
|---|---|---|
| `case.md` | o que é dado ao agente | `Target:` (arquivo que existe), `Question:` |
| `expect.md` | o que discrimina uma resposta boa de uma plausível | ≥1 `MUST-FIND:`, ≥1 `MUST-NOT-CLAIM:` |
| `baseline.md` | o que se observou, e quando | `Date:`, `Target-commit:`, `First-red:`, `Verdict:` |

`MUST-NOT-CLAIM` é o campo que impede o modo de falha clássico: um eval que só pergunta
"achou alguma coisa?" passa com qualquer resposta prolixa. Ele exige que a resposta **não**
afirme o que seria falso — é o lado negativo, sem o qual não há discriminação.

`First-red` é a segunda lei da `verifiable-dod` virada campo: enquanto ninguém tiver visto
aquele caso reprovar uma saída, ele é esperança, e o portão diz isso em voz alta.

**3. O portão** (`scripts/check-evals.sh`) — determinístico, roda em qualquer máquina:
estrutura → alvo existe → asserções discriminam → linha de base defasada (compara
`Target-commit` com `git log -1 -- <alvo>`) → linhas de base pendentes.

**4. A execução com modelo no laço** (`.claude/commands/eval.md`) — sob demanda, em
contexto fresco, grava `baseline.md`. Fica fora da integração contínua (CI) de propósito:
custo por execução e chave de interface de programação (API) não pertencem a um portão que
todo mundo precisa conseguir rodar.

**5. Onde ele entra.** `evals/` vira superfície instalável (ADR 0014 → inglês, e entra nos
alvos do `check-language.sh`); `check-evals.sh` entra na lista de fitness functions do
`CLAUDE.md`; a dívida das duas linhas de base entra no índice de decisões como achado
aberto, para o gatilho da retro enxergá-la.

## Verificação (DoD)

```bash
scripts/check-evals.sh                 # vermelho declarado: 2 linhas de base pendentes
scripts/check-language.sh              # verde, agora cobrindo evals/
scripts/check-links.sh                 # verde (links novos resolvem)
scripts/check-install.sh               # verde
node publicar/build.mjs                # verde
```

Prova de que o portão acusa (princípio IV): três injeções deliberadas — apagar `expect.md`,
remover a linha `MUST-NOT-CLAIM`, e tocar o arquivo alvo depois da linha de base — cada uma
com a saída vermelha copiada para o `qa-report.md`.
