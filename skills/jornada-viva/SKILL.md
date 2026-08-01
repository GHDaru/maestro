---
name: jornada-viva
description: Documentação viva de jornada — doc por jornada, capturas geradas do build real por script versionado, e avaliação heurística datada, tudo no mesmo PR. Use quando a mudança tocar um caminho de usuário (tela, fluxo, interação), ao fechar uma feature com interface, ou quando alguém perguntar "isso está documentado?".
---

# Jornada viva

Uma jornada é o **caminho real do usuário**, não a descrição dele. Documentá-la viva
significa: o que está escrito **é gerado do sistema que roda** — e envelhece junto com ele.

## Iron Law

```
JORNADA SEM CAPTURA DO BUILD REAL É FICÇÃO — E HEURÍSTICA SEM DATA É FICÇÃO VENCIDA
```

Violar a letra é violar o espírito. Isso NÃO é desculpa:
- "a tela não mudou" — se o script não rodou, você não sabe;
- "a captura é de ontem" — então a heurística de ontem também precisa ser revisitada;
- "já avaliei antes" — avaliação sem data nova não prova nada sobre o build de hoje;
- "printei manualmente" — captura à mão não regenera, logo apodrece na primeira mudança.

## As três partes obrigatórias (mesmo PR)

| Parte | O que é | Como se prova |
|---|---|---|
| **1. Documento** | `docs/journeys/NNN-<slug>.md` — o caminho, passo a passo, com o objetivo do usuário | existe e referencia a spec |
| **2. Capturas** | imagens **geradas por script versionado** a partir do build real | arquivo de imagem + script no repositório, com data |
| **3. Heurística** | tabela de achados com **severidade e status**, **datada** | data da revisitação ≥ data das capturas |

## O passo que todo mundo esquece

**Regenerar a captura obriga a revisitar a heurística.** Se as imagens são de hoje e a
tabela de achados é de duas semanas atrás, a documentação afirma sobre um sistema que não
existe mais. Esse foi um caso real: capturas ✅, script ✅, documento ✅ — e a avaliação
heurística parada, descoberta só porque um humano perguntou (anti-padrão 13: o check
media *a seção existe*, não *foi revisitada*).

**Check correto**: `data da heurística ≥ data das capturas`.

## Achado não resolvido também é entrega

Achado que não coube no ciclo **não some**: fica na tabela com severidade e destino
(próximo ciclo, ou registro). Omitir achado aberto é pior que tê-lo.

| Sev. | Quando | Destino |
|---|---|---|
| Alta | quebra a jornada ou bloqueia o usuário | corrige no ciclo |
| Média | atrito ou confusão real | corrige no ciclo, ou registra com prazo |
| Baixa | polimento | registra para ciclo futuro |

## Roteiro

1. Rode o script de captura contra o **build real** (não mock, não figura de design).
2. Se o script quebrou, **conserte o script** — ele é parte da entrega (a regeneração é o
   teste do próprio script).
3. Atualize o documento com o caminho e as capturas novas.
4. **Revisite a heurística** com a data de hoje: cada achado como ✅ conforme, ✅ corrigido
   no ciclo, ou 📝 registrado com severidade.
5. Ligue: jornada ↔ spec ↔ pull request ↔ teste.

**Consumida por:** `qa` (evidência), `tech-writer` (documento), `ux-semantica` (papéis).
**Ver também**: [capítulo 11 — rastreabilidade](../../docs/handbook/11-rastreabilidade.md).
