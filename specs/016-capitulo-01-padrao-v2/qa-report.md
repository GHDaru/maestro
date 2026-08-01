# QA-report 016 — Capítulo 01 no padrão v2

- **Data**: 2026-08-01 · **Raia**: Plena · **Veredito**: ✅ CONFORME

## Fitness functions (DoD)

| Check | Esperado | Resultado |
|---|---|---|
| Seções do capítulo | 9 (esqueleto v2) | **9** ✅ |
| Frameworks do v1 preservados | 5 | 5 ✅ |
| Fontes preservadas | 5 externas + 1 interna | 5 + 1 ✅ |
| Conceitos-chave do v1 | presentes | ✅ (12 ocorrências) |
| `pytest` | verde | **11 passaram** ✅ |
| Fitness function do corpus | falha com página ausente | falhou com a instrução ✅ |
| Build do site | 34 páginas, links OK | ✅ |

## Cobertura

FR1–FR5 entregues. Migração sem perda: cada bloco do v1 foi mapeado para a seção
correspondente do v2, e o capítulo ganhou o que faltava — objetivos, exemplo real,
anti-padrões, verificação e leitura executiva.

## Automação nascida no ciclo

O README do companion *pedia* para regenerar o corpus a cada mudança do livro — regra de
papel, do tipo que se esquece. Virou **teste**: se uma página do sumário não estiver no
corpus, o conjunto falha com a instrução do comando a rodar. Provado com página injetada.

**Limite declarado**: o teste compara títulos, então pega página **faltando**, não
conteúdo **desatualizado** dentro de uma página existente. Está escrito no próprio teste —
o que a fitness function não cobre precisa ser dito, senão vira falso senso de segurança
(anti-padrão registrado no capítulo 13 §5.5).

## Lição para a retrospectiva (segunda ocorrência)

Meu check de fontes (`grep -c "https://"`) contou **linhas**, não URLs, e reportou 5 onde
havia 6 fontes. É a segunda vez em dois ciclos que um check meu prova a coisa errada (no
015 foi `grep -l companion`, que casou com texto legítimo). Padrão recorrente → candidato
a entrada no catálogo de anti-padrões: **"check que mede o proxy, não o fato"**.

## Gate

- Aprovação do Steward ("sim"); promovido via `promover-main.sh`.
