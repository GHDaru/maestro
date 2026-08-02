# Spec 020 — BPMN navegável no livro (o diagrama como índice)

- **Status**: Concluída · **Raia**: leve · **Data**: 2026-08-02
- **Origem**: pedido do Steward — "podemos colocar o BPMN no livro. O gráfico poderia ter
  link para a referência".

## O quê e por quê

O BPMN (*Business Process Model and Notation*, Notação de Modelagem de Processos de
Negócio) do método existia só como imagem, e **a imagem sequer aparecia no site**: o motor
de publicação nunca copiava os arquivos referenciados por `![...](...)` para `site/`, e o
portão de links só validava `<a href>`, então a página quebrada passava verde.

Além de consertar isso, o diagrama vira **navegação**: cada caixa é um link para o
capítulo, receita ou norma que define aquele passo. Quem lê o processo entra em qualquer
estação sem procurar no sumário — o desenho passa a ser o índice do livro na ordem em que
o trabalho acontece.

## Requisitos funcionais

- **FR1**: QUANDO uma página do livro referencia uma imagem relativa, O SISTEMA DEVE
  copiá-la para `site/` junto da página gerada.
- **FR2**: QUANDO o HTML publicado contém um `<img src>` interno sem arquivo
  correspondente, O SISTEMA DEVE falhar o build com código de saída ≠ 0.
- **FR3**: QUANDO um bloco de HTML embutido no Markdown contém `<a href="...md">`, O
  SISTEMA DEVE reescrever o destino com a mesma regra dos links Markdown (`.md` publicado
  → `.html`; o resto → GitHub), para o link valer nos dois contextos.
- **FR4**: QUANDO sobra um `href` relativo terminado em `.md` no HTML publicado, O SISTEMA
  DEVE falhar o build — link não reescrito é link que some no site.
- **FR5**: A página do BPMN DEVE apresentar o diagrama em versão navegável (todas as raias,
  cada nó com link para sua referência) **e** manter a imagem única para apresentação e
  impressão.
- **FR6**: A versão navegável DEVE distinguir visualmente humano, agente, automação, gate
  humano (ouro), DoD mecânica (verde) e artefato — nos dois temas (claro e escuro).

## Fora de escopo

- Regerar a imagem PNG (a v3, do ciclo 019, continua correta).
- Editor de diagrama ou biblioteca de BPMN — o desenho é HTML+CSS do próprio tema.
- Tornar navegáveis os outros diagramas (01–04) — se provar valor aqui, replica depois.

## Critérios de aceite (DoD)

- [x] `node publicar/build.mjs` sai com código 0 e a imagem do BPMN existe em `site/`
- [x] Portão de imagens **provado falhando**: apontar para imagem inexistente → exit 1
- [x] Portão de `.md` cru **provado falhando**: desligar a reescrita → exit 1, 38 achados
- [x] Nenhum `href` do bloco navegável termina em `.md` no HTML publicado (medido no navegador)
- [x] Quatro nós clicados em navegador real levam ao capítulo/receita correto
- [x] Captura do bloco nos dois temas, sem estouro horizontal

## Clarify

1. Substituir a imagem pelo bloco navegável ou manter as duas? → **Manter as duas**: a
   imagem serve slide e impressão; o bloco serve leitura e navegação.
2. Os links do bloco quebrariam no GitHub (lá não existe `.html`)? → resolvido pelo FR3:
   o Markdown guarda `.md`, e o motor reescreve na publicação.
