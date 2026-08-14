# Spec 054 — Material de apresentação dentro do livro

- **Status**: Concluída · **Raia**: plena · **Data**: 2026-08-14
- **Origem**: pedido do Steward — "coloque esta apresentação no livro, como material",
  sobre o caderno de desenvolvimento criado no ciclo 053.

> **Raia**: plena. **Ambiguidade** média — "material" é um conceito que o sumário não tem, e
> a forma de entrada dele no livro é decisão de desenho, não transcrição. **Raio**: o motor
> de publicação (`publicar/build.mjs`), que é **portão bloqueante da CI** — quebrá-lo pinta
> o pipeline de vermelho para todo mundo. **Irreversibilidade** baixa (é um gerador; o
> `site/` é regenerado a cada build). Dois dos três altos o bastante para não ser leve; na
> dúvida entre leve e plena, é plena.

## O quê e por quê

O livro publica **markdown**: `publicar/build.mjs` lê `sumario.json`, converte cada item
`.md` em página e reprova o build se um link interno não resolver. Uma apresentação é HTML
de página inteira — rolagem por slide, trilho fixo, altura total — e não é markdown nem cabe
dentro do miolo de uma página do livro.

Por isso as duas apresentações que existem desde antes (`executiva` e `técnica`) **estão
fora do livro**: não há por onde entrarem. Um leitor do site não descobre que elas existem, e
um link para elas hoje sairia do livro para o GitHub, onde HTML aparece como código-fonte.

O que falta é um terceiro tipo de conteúdo, ao lado de *item* e *parte*: **material** —
página autocontida que o livro **publica e indexa**, mas não renderiza no seu próprio molde.

## Requisitos funcionais

- **FR1**: QUANDO `sumario.json` declarar um material, O SISTEMA DEVERÁ publicá-lo em
  `site/` como página autocontida e listá-lo no sumário do livro.
- **FR2**: O SISTEMA DEVERÁ tratar o material como **página do livro** para efeito do portão
  de links: um link de dentro do livro para um material declarado deve resolver **para dentro
  do livro**, e um link interno `.html` para uma página que o livro não publica deve
  continuar reprovando o build.
  > **Limite declarado** (a revisão do ciclo cobrou a versão anterior desta frase, que
  > prometia mais do que entrega): um link **markdown** para um `.html` que existe no
  > repositório e não é material vira link para o GitHub, e isso é **correto** — é o caso do
  > `fontes/05-bpmn-processo.html`, que é fonte de diagrama, não leitura. Quem pega alvo
  > inexistente é o `check-links.sh`, que já cobre todo `.md` do repositório. A reprovação
  > desta FR vale para link interno em bloco HTML, que é o que o motor consegue julgar.
- **FR3**: QUANDO um material colidir de nome com **qualquer página que exista em `site/`** —
  inclusive a capa mantida à mão e o próprio sumário —, O SISTEMA DEVERÁ **falhar o build**
  dizendo quais são. Uma página sobrescrever a outra em silêncio é a falha; de onde vem cada
  uma não muda nada.
- **FR4**: QUANDO um material declarado **não existir no disco**, O SISTEMA DEVERÁ falhar o
  build. Entrada faltando é reprovação, nunca silêncio (anti-padrão 16).
- **FR5**: O material publicado DEVERÁ oferecer volta para o livro, sem que o livro precise
  alterar o arquivo de origem — quem o abre pelo site tem que conseguir voltar.
- **FR6**: O material DEVERÁ ser visível ao portão de fronteira (`check-boundary.sh`) como
  página publicada. Publicar por um canal que o portão não lê é criar uma porta sem
  guarda — e um portão que lê um de dois canais não distingue "nada vazou" de "não olhei".

## Fora de escopo

- Registrar as apresentações **executiva** e **técnica** como material. O mecanismo passa a
  servi-las e cada uma é uma linha no `sumario.json`, mas colocá-las no livro é decisão do
  Steward, não consequência deste pedido.
- Renderizar material dentro do molde do livro (cabeçalho, navegação lateral, paginação).
  Uma apresentação de tela cheia dentro do miolo de uma página é uma briga de layout sem
  ganho para o leitor.
- **Material com asset** (imagem, folha de estilo ou script em arquivo separado). O material
  é publicado sozinho, sem cópia de assets — e o portão de imagens do motor **reprova** quem
  tentar, o que é o comportamento certo: "autocontido" passa a ser exigência verificada, não
  promessa. Copiar assets de material é ciclo próprio, quando houver material que precise.
- PDF do material.

## Critérios de aceite (DoD)

<!-- Sem caixas: esta seção diz o que deve valer; se valeu, quem diz é o qa-report. -->
- O caderno de desenvolvimento aparece no sumário do livro e abre a partir dele.
- O build reprova, com mensagem que nomeia o caso **e diz o que fazer**, em: material ausente
  do disco; material colidindo com página gerada; material colidindo com a **capa** ou com o
  **sumário**; e link interno `.html` para página não publicada.
- O `check-boundary.sh` conta o material entre as páginas publicadas e reprova material de
  domínio `toolkit` não declarado como compartilhado.
- Cada uma dessas reprovações é **provada por mutação** — quebrada de propósito e vista
  falhando — antes de o ciclo fechar.
- O build segue verde no estado correto, e a contagem de páginas cresce exatamente pelo
  material acrescentado.

## Clarify

1. Material entra no molde do livro ou autocontido? → **autocontido**, com volta para o
   sumário, pelo motivo registrado em "fora de escopo".
2. O material vira uma parte nova do sumário ou entra numa existente? → **seção própria**,
   porque não é leitura sequencial: não tem anterior/próximo e não pertence a nenhuma trilha.
