# Catálogo do ecossistema

> O que já olhamos do trabalho dos outros, o que atravessou a fronteira e o que não
> atravessou — com o motivo, e com o portão que verifica se ainda é verdade.

Este catálogo existe porque a resposta honesta à pergunta *"temos em algum lugar todos os
repositórios que avaliamos e as decisões que tomamos?"* era **"em parte, e espalhado"**: o
julgamento vivia em sete documentos que não se conheciam, julgando por **ferramenta** e sem
lugar nenhum onde o veredito **corrente** morasse. Cinco ideias constavam como absorvidas,
com destino condicional, e nenhuma delas tinha chegado a um arquivo.

## As três peças

| Peça | O que é | Muda? |
|---|---|---|
| [`fontes.md`](fontes.md) | uma linha por **fonte**: endereço, o que é, **licença**, quando observamos | pouco |
| [`ideias/`](ideias/) | um card por **ideia**, datado — o que vimos e o que julgamos **naquele momento** | **nunca** |
| [`estado.jsonl`](estado.jsonl) | o veredito **de hoje**, append-only; o corrente é a última linha de cada id | sempre que mudar |

**A unidade é a ideia, não a ferramenta.** O Maestro quase nunca adota uma ferramenta: ele
absorve ideias e descarta o resto. "Superpowers: absorver + observar" não é acionável.
"Causa raiz antes do conserto: absorver, destino `skills/diagnose-before-fix/SKILL.md`" é —
e é falsificável, que é o ponto.

**Momento e estado são artefatos diferentes.** Um card diz o que se julgou num dia, olhando
uma versão. Isso é verdade para sempre. O veredito de hoje muda, e mora no índice. Enquanto
o estado morava dentro da observação, "absorver quando doer" e "observar até doer" eram a
mesma frase escrita em duas colunas diferentes — foi o caso de
[worktree por task](ideias/003-worktree-por-task.md), que o ADR 0008 registrou sob um
cabeçalho de absorção com um destino condicional, e que o Apêndice B, três ciclos depois,
escreveu como `observar` **sem contradizer o ADR**. Nenhum dos dois estava errado; faltava
o lugar onde o estado corrente morasse.

## O vocabulário de veredito (fechado)

| Estado | Significa | O que o portão exige |
|---|---|---|
| `adotar` | a ferramenta entra, como dependência do método | um destino que é **arquivo** (não pasta) **e** uma `prova`: texto literal que tem de ser encontrado dentro dele |
| `absorver` | a **ideia** entra, reimplementada em artefato nosso | idem |
| `observar` | não agora; pode mudar | **gatilho** de reavaliação não vazio |
| `descartar` | não entra — conflito de princípio, de licença, ou função já servida | nada; o card diz qual |

`observar` sem gatilho é esquecer com cerimônia, e por isso o portão o recusa. Quando não
existe condição futura capaz de mudar a decisão, o veredito honesto é `descartar` — foi o
caso de [020](ideias/020-fluxo-spec-em-comandos.md) e [021](ideias/021-baixa-cerimonia-para-mudanca-simples.md).

## As sete dimensões

Todo card avalia as sete, sempre, nesta ordem. Duas **reprovam sozinhas**: uma licença
incompatível ou um conflito insanável de princípio não se compensam com maturidade.

| # | Dimensão | Pergunta | Reprova sozinha? |
|---|---|---|---|
| 1 | Conflito com princípio | qual princípio, e é insanável? | **sim** |
| 2 | Licença e redistribuição | dá para copiar, ou só citar? | **sim** |
| 3 | Função já servida | duplica algo que já temos (Princípio VI)? | não |
| 4 | Custo de contexto | quanto custa carregar? | não |
| 5 | Reversibilidade | quanto custa sair depois (*lock-in*)? | não |
| 6 | Maturidade e evidência | o que **nós** observamos, em que versão — não *stars* de terceiros | não |
| 7 | Dor real hoje | a dor que isso resolve existe aqui, agora (YAGNI)? | não |

**Sem nota agregada, por decisão.** Uma média esconde qual dimensão decidiu — e em quase
todo card deste catálogo, uma decidiu sozinha.

Para avaliar algo novo: `.specify/templates/evaluation-template.md`.

**Idioma.** O template é instalável e por isso está em **inglês** (ADR 0014); este catálogo é
memória do método e é publicado no livro, e por isso está em **português**, como `docs/adr/`.
O portão lê as duas grafias de cada campo e do vocabulário — precedente do
`check-conformance.sh`, que aceita os dois títulos da seção de critérios.

## O estado corrente

Quarenta ideias, vinte e três fontes. Os números abaixo são de 2026-08-10; a verdade
corrente está sempre em [`estado.jsonl`](estado.jsonl) — o estado de cada ideia é a **última
linha** com o seu id.

| Estado | Quantas | Leitura |
|---|---|---|
| `absorver` | 14 | ideias que **estão no disco**, cada uma com o arquivo e o texto que provam |
| `observar` | 15 | cada uma com gatilho escrito |
| `descartar` | 10 | com o motivo, e sem porta dos fundos |
| `adotar` | 1 | o Spec Kit — a única ferramenta de terceiro adotada, e a decisão mais consequente do método ([031](ideias/031-spec-kit.md)) |

## O que este catálogo achou no dia em que nasceu

O portão foi escrito antes do conteúdo. Ele **não** encontrou uma linha defeituosa que já
estivesse no disco — as linhas `destino: scripts/` e `destino: docs/standards/` foram
escritas **nesta migração**, tentando expressar como fato verificável o que o ADR 0008 dizia
em prosa. Foi aí que o defeito apareceu: a promessa não sobreviveu à tradução para uma forma
que pudesse ser conferida.

Cinco ideias estavam registradas como **absorver** com destino condicional — worktree por
task, standards por camada, padrões de fatiamento, fatia vertical e contrato por fatia — e
nenhuma delas chegou a um arquivo. Todas voltaram para `observar` **com gatilho**, em linha
nova datada de 2026-08-10: é o que sempre foram, já que o destino vinha escrito como "quando
houver dor real".

Duas consequências ficaram no portão, e as duas nasceram de tentativas de burlá-lo:

- o destino tem de ser um **arquivo**, não uma pasta — `scripts/` existe por outros motivos e
  fazia a promessa parecer cumprida;
- o destino precisa de **prova**: um texto literal que tem de ser encontrado dentro do
  arquivo. Sem isso, apontar para `README.md` satisfaria qualquer absorção já declarada.

A correção foi sempre no conteúdo. O portão não ganhou exceção nenhuma.

## Como isto se relaciona com as notas de terceiros

Este catálogo julga **ideias**. [`THIRD-PARTY-NOTICES.md`](../../THIRD-PARTY-NOTICES.md)
cumpre a **obrigação legal** sobre o que é redistribuído. São perguntas diferentes: uma
ideia reimplementada não gera obrigação, e um arquivo copiado gera, mesmo sem ideia nova.
Quando as duas se encontram — como em [013](ideias/013-root-cause-antes-do-fix.md) —, a
atribuição vale por precaução.

## Migrado de (nada foi apagado)

[ADR 0005](../adr/0005-raias-de-trabalho-e-specs-de-infra.md) ·
[ADR 0008](../adr/0008-avaliacao-ecossistema-sdd.md) ·
[ficha do ecossistema](../research/avaliacao-ecossistema-sdd.md) ·
[Apêndice A](../handbook/apendice-a-maestro-02.md) ·
[Apêndice B](../handbook/apendice-b-superpowers.md) ·
[Apêndice C](../handbook/apendice-c-panorama-templates.md) ·
[pesquisa do upstream](../research/upstream-decomposicao.md).
