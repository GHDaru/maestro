# Spec 052 — Symlink não é porta de saída

- **Status**: Concluída · **Raia**: leve · **Data**: 2026-08-11
- **Origem**: achado `achado-051-symlink-de-diretorio-no-alvo`, aberto no ciclo anterior.

> **Raia**: leve. **Ambiguidade** baixa (a correção é uma recusa); **raio** contido a um
> script; **irreversibilidade** baixa. Leve, mas com revisão independente — que a raia leve
> mantém.

## O quê e por quê

Um *symlink* dentro do alvo é uma porta para fora dele. O `cp` escreve **através** de um
link, e um diretório linkado faz todo caminho abaixo dele cair em outro lugar — então, desde
que o ciclo 051 deu ao instalador o poder de **remover**, a poda apagaria fora do repositório
para o qual ela foi apontada.

Verificado em 2026-08-11, antes da correção: com `ln -s /fora <alvo>/skills`, o instalador
escrevia dentro de `/fora`.

## Requisitos funcionais

- **FR1**: QUANDO o caminho de destino, ou qualquer diretório acima dele dentro do alvo, for
  um *symlink*, O SISTEMA DEVERÁ **recusar** escrever e dizer qual caminho recusou.
- **FR2**: QUANDO a poda encontrar o mesmo caso, O SISTEMA DEVERÁ **recusar** remover.
- **FR3**: QUANDO recusar, O SISTEMA DEVERÁ contá-lo no resumo — recusa silenciosa é
  indistinguível de "nada a fazer".

## Critérios de aceite (DoD)

<!-- Sem caixas: esta seção diz o que deve valer; se valeu, quem diz é o qa-report. -->
- Com um *symlink* de diretório apontando para fora, nada é escrito lá, e o arquivo que
  estava lá continua intacto.
- A recusa aparece nomeada na saída e no resumo.
- `check-installed.sh` cobre os dois — escrita através do link e recusa nomeada.
