# Spec 064 — Portão de slop: o julgamento editorial vira checagem

- **Status**: Rascunho · **Raia**: plena · **Data**: 2026-08-13
- **Origem**: porte do portão escrito para os dois livros irmãos do mesmo autor
  (*Teoria das Restrições*, spec 009; *Engenharia de Harness*, spec 069), a pedido do autor.

> **Raia**: plena. **Ambiguidade** média — o que conta como "soa gerado" precisa de decisão
> escrita, e três regras do guia de origem foram descartadas com medição. **Raio** amplo: o
> portão passa a bloquear o build de todo capítulo futuro. **Irreversibilidade** baixa: é um
> arquivo novo e uma linha no `package.json`.

## O quê e por quê

O livro do Maestro é escrito com apoio de IA — é o próprio método em uso. E **nenhum portão
olha a prosa**: `check-chapters.sh` mede as nove seções e a datação, `check-links.sh` mede
link, `build.mjs` mede slug e imagem. Um capítulo inteiro escrito no registro "esta prática
desempenha um papel crucial no cenário em evolução da engenharia" passa hoje com tudo verde.

É o Princípio IV aplicado à prosa: o trabalho é **transformar julgamento em checagem**.
"Este capítulo soa gerado" era julgamento editorial, disponível só quando alguém lia com
atenção — e memória de revisor relata intenção, não fato (C13). O `fight-the-pile-up`
combate o amontoado; falta quem combata o registro genérico.

## Requisitos funcionais

- **FR1**: QUANDO um arquivo do livro contiver um dos padrões declarados, O SISTEMA DEVE
  falhar o build citando arquivo, linha, seção do guia e o trecho.
- **FR2**: QUANDO o trecho for legítimo, O SISTEMA DEVE aceitar `<!-- slop-ok: motivo -->` na
  linha anterior — e só com motivo escrito.
- **FR3**: QUANDO qualquer expressão for afrouxada ou quebrada, O SISTEMA DEVE falhar por
  conta própria, sem depender de haver slop no corpus.
- **FR4**: QUANDO a frase estiver quebrada em duas linhas, O SISTEMA DEVE acusar do mesmo
  jeito (Markdown quebra parágrafo onde o parágrafo mandar).

## Fora de escopo

- `docs/governance/` — está em inglês (ADR 0014) e é norma, não prosa de livro.
- `docs/research/` — notas que citam fonte externa literalmente; a única ocorrência que o
  portão marcaria lá está **dentro de aspas**, copiada de um paper (§373 do guia isenta texto
  de segunda mão, e um portão não distingue citação de uso).
- `docs/adr/`, `docs/records/`, `docs/ecosystem/` — memória append-only. Um portão que
  exigisse correção ali pediria exatamente o que o `PreToolUse` impede: achado sem saída.
- §14 (travessão) e §18 (emoji) — descartados **com medição**; ver ADR 0021.
- Unificar as três cópias do portão num pacote só.

## Critérios de aceite (DoD)

- `node publicar/verifica-slop.mjs` sai 0 no livro atual.
- `npm run build --prefix publicar` roda o portão antes do `build.mjs` e sai 0.
- Slop plantado num capítulo faz o portão sair 1, citando arquivo e linha.
- Um canário dobrado no meio continua sendo acusado (FR4, verificado pelo autoteste).
- Todo padrão tem canário e o acusa; padrão sem canário falha o build (FR3).
- `<!-- slop-ok: motivo -->` suprime a linha seguinte, e só ela (FR2).
- Menos de 25 arquivos ou 2.000 linhas varridas falha: portão vazio não passa por verde.
- `scripts/check-language.sh` continua verde (o portão mora em `publicar/`, fora da
  superfície instalável — por isso pode ser português, como o `build.mjs` ao lado).

## Clarify

1. ~~O portão vai em `scripts/` (inglês, ADR 0014) ou em `publicar/` (português)?~~
   Resolvido no plan: `publicar/`, com a justificativa registrada no ADR 0021.
