# QA-report 013 — Livro: guia editorial, piloto e instalador

- **Data**: 2026-08-01 · **Raia**: Plena · **Veredito**: ✅ CONFORME

## Fitness functions (DoD)

| Check | Esperado | Resultado |
|---|---|---|
| Build do site | 25 páginas, links OK | ✅ 25 páginas |
| Seções do capítulo 13 | 9 (esqueleto v2) | **9** ✅ |
| "O que provoca" (uma por decisão) | ≥ 14 | **14** ✅ |
| Instalador em destino limpo | instala o toolkit | **47 arquivos** ✅ |
| Instalador na 2ª execução | mantém existentes | 15 "existe (mantido)" ✅ |
| `--dry-run` | não escreve nada | ✅ |
| ADR 0011 + registro | existe e indexado | ✅ |

## Cobertura

FR1–FR5 entregues. Fora de escopo respeitado: companion (construção em ciclo próprio),
migração dos capítulos 01–12 e reescrita da navegação em 5 trilhas.

## Observação para o próximo ciclo

O índice do handbook agora declara **dois padrões coexistindo** (v1 nos capítulos 01–12,
v2 a partir do 13). Isso é dívida didática assumida e datada: cada migração é um ciclo,
com o capítulo ganhando objetivos, exemplo de ciclo real e verificação.

## Gate

- Decisões do Steward (esqueleto aprovado · chat opção "c" · fazer o piloto) registradas
  no clarify da spec e no ADR 0011. Promovido via `promover-main.sh`.
