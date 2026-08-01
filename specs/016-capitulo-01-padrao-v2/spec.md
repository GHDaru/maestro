# Spec 016 — Capítulo 01 migrado ao padrão v2

- **Status**: Aprovada ("sim") · **Raia**: Plena · **Data**: 2026-08-01
- **Origem**: ADR 0011 (migração gradual dos capítulos ao esqueleto v2, um por ciclo).
  Primeiro da fila: o 01, porque é a porta de entrada conceitual do método.

## O quê e por quê

O capítulo 01 explicava bem, mas era **documentação de referência**: sem objetivos de
aprendizagem, sem exemplo real, sem verificação. Quem lia entendia a tese e não sabia se
tinha aprendido. Migrar ao v2 fecha o ciclo pedagógico (Backward Design) e liga a teoria
à nossa própria evidência.

**Regra editorial**: reescrever a **forma**, preservar o **fato** — nada de conteúdo
técnico perdido na migração.

## Requisitos funcionais

- **FR1**: capítulo 01 no esqueleto de 9 seções do [guia editorial](../../docs/livro/guia-editorial.md).
- **FR2**: §6 com **exemplo de ciclo real** (obrigatório no v2): o `promover-main.sh` como
  materialização do princípio, com saída de comando verificada.
- **FR3**: preservar todo o conteúdo técnico do v1 — *accountability* × capacidade,
  *ex-ante* × *ex-post*, reversibilidade, os 5 frameworks avaliados e as 6 fontes.
- **FR4**: índice do handbook e sumário refletindo a migração (marca ✨, título novo).
- **FR5**: corpus do companion regenerado — senão o tutor responde com o livro velho.

## Fora de escopo

- Migrar os capítulos 02–12 (um por ciclo).
- Reescrever o diário da jornada.

## Critérios de aceite (DoD)

- [ ] `grep -c "^## " 01-principio-central.md` = 9 (as nove seções do v2).
- [ ] QUANDO uma página do livro não estiver no corpus, O SISTEMA DEVE falhar o conjunto
      de testes com a instrução de regenerar (fitness function nova).
- [ ] Os 5 frameworks e as 6 fontes do v1 continuam presentes.
- [ ] `pytest` verde; build do site verde (34 páginas, links OK).

## Clarify (resolvido)

1. **Reescrever ou acrescentar?** Reescrever a forma, preservando cada fato — o v1 tinha
   conteúdo bom, faltava-lhe pedagogia.
