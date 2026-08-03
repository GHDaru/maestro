# QA-report 034 — Retrospectiva dos quatro achados

- **Data**: 2026-08-03 · **Raia**: plena · **Veredito**: **APROVADO** (DoD verde)

## Fitness functions (DoD)

| Check | Esperado | Resultado |
|---|---|---|
| `check-retro.sh` **antes** | falhar com a dívida real | ✅ exit 1 — 5 abertos (limite 4), o mais velho com 11 ciclos |
| `check-retro.sh` depois | 0 abertos | ✅ os cinco fechados por linha nova com o campo `fecha` |
| `check-cycle.sh` **provado falhando** | spec sem raia declarada | ✅ `034-…: no lane declared in the spec header` |
| `check-cycle.sh` depois | raia justificada + commits citando o ciclo | ✅ distribuição impressa: 21 plena · 12 leve |
| `check-links.sh` **provado falhando** | link para arquivo inexistente | ✅ `09-definition-of-ready-done.md → ../receitas/arquivo-que-nao-existe.md` |
| `check-links.sh` depois | 242 links, todos resolvem | ✅ |
| `check-chapters.sh` **provado falhando** | skill mais nova que o capítulo | ✅ 4 capítulos atrasados apontados por nome |
| `check-chapters.sh` depois | exit 0 | ✅ após atualizar a data de revisão dos 13 capítulos (foram tocados no ciclo 033) |
| `check-language.sh`, `check-install.sh`, `check-agents.sh`, `check-roles.sh` | exit 0 | ✅ |
| `node publicar/build.mjs` | exit 0 | ✅ 35 páginas |

## Cobertura dos requisitos

- **FR1**: ✅ gatilho por dívida. **FR2/FR3**: ✅ `check-cycle.sh`. **FR4**: ✅ frescor
  skill × capítulo. **FR5**: ✅ links do repositório inteiro. **FR6**: ✅ cinco achados
  fechados com `fecha`, mais a linha `retro-034`.

## Achados e correções do ciclo

1. **Inventei o protocolo de fechamento no meio do caminho — e ele nasceu errado.** As cinco
   primeiras linhas de fechamento usavam um id novo sem apontar o achado original, então o
   `check-retro.sh` continuava vendo tudo aberto: o fechamento existia no texto e não no
   dado. Corrigido com o campo **`fecha`** (ligação estrutural) e documentado no protocolo do
   índice. É o anti-padrão 13 aplicado ao meu próprio registro — a diferença é que desta vez
   o check acusou antes do commit.
2. **`check-cycle.sh` morria em silêncio.** Com `pipefail`, a substituição que não acha nada
   (uma spec ainda em esqueleto) derrubava o script sem imprimir nada — um check que morre
   parece um check que passou. Corrigido com `|| true` e comentário no lugar.
3. **`check-links.sh` mediu o texto na primeira versão**: contou `![...](...)` escrito como
   *exemplo* dentro de crase como se fosse link. Agora remove os trechos em crase antes de
   varrer. Terceira vez no ciclo em que um check meu precisou ser corrigido para medir o
   fato — e é exatamente por isso que a segunda lei existe.

## Lição para a retrospectiva

Os três achados acima são a mesma família (**o check mede o proxy**) e todos apareceram
**porque os provei falhando**. Nenhum vira regra nova: o anti-padrão 13 já cobre, e o
antídoto (provar falhando) já é lei. Repetir a regra não a torna mais forte — executá-la, sim.

Anti-padrões que entraram no catálogo neste ciclo: **17** (cerimônia sem gatilho) e **18**
(renome em massa por substituição de texto).

## Pendência de gate

- promoção dev → main aguarda aprovação humana.
