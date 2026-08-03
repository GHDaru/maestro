# QA-report 035 — Axiomas e BPMN v4

- **Data**: 2026-08-03 · **Raia**: plena · **Veredito**: **APROVADO** (DoD verde)

## Fitness functions (DoD)

| Check | Esperado | Resultado |
|---|---|---|
| `check-language.sh` | exit 0 com o documento novo | ✅ `docs/governance` limpo |
| `check-links.sh` | exit 0 após o BPMN mudar | ✅ todo link relativo resolve |
| `check-cycle.sh` | raia justificada + commits citando o ciclo | ✅ |
| `check-retro.sh` | 0 achados abertos | ✅ |
| `node publicar/build.mjs` | 36 páginas | ✅ axiomas publicado na trilha Referência |
| Imagem do BPMN | 7 raias, sem corte | ✅ regenerada do fonte versionado, recorte na altura real |

## Cobertura dos requisitos

- **FR1**: ✅ três camadas separadas. **FR2**: ✅ independência declarada nos cinco.
- **FR3**: ✅ evidência em todos os seis teoremas, inclusive a desfavorável (T4).
- **FR4**: ✅ constituição v1.3.0 aponta; o Constitution Check segue nos princípios.
- **FR5**: ✅ inglês. **FR6**: ✅ as duas versões do BPMN atualizadas.

## Achados e correções do ciclo

1. **A primeira renderização do BPMN saiu cortada à direita** — a raia nova (portões) e a de
   distribuição estouravam o viewport, e o rodapé perdeu um cartão. Foi visto porque a imagem
   **foi olhada**, não porque algum check acusou: nenhum portão mede "a imagem está inteira".
   Corrigido com viewport maior e recorte na altura real do conteúdo. Fica registrado como
   limite conhecido: imagem gerada não tem portão — só olho.
2. **Cinco axiomas, e um deles quase virou dois.** "Contexto é finito" e "o que está escrito
   sobrevive" pareciam o mesmo até o teste de independência: remover A3 mantém a memória
   (A4) e destrói o fatiamento; remover A4 mantém o fatiamento e destrói a continuidade. São
   independentes, e o teste é o que provou.

## Lição para a retrospectiva

Não há erro recorrente novo neste ciclo. O achado 1 é candidato a portão futuro (verificar
que a imagem gerada não tem conteúdo cortado), mas ainda **não** foi registrado como achado
aberto: com dor única, seria regra especulativa — YAGNI. Se acontecer de novo, entra como
`achado-NNN` e o `check-retro.sh` cobra.

## Pendência de gate

- promoção dev → main aguarda aprovação humana.
