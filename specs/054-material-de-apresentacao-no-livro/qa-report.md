# QA report 054 — Material de apresentação dentro do livro

- **Date**: 2026-08-14 · **Lane**: plena · **Verdict**: aprovado após correção do parecer

## Fitness functions (DoD)

| Check | Expected | Result |
|---|---|---|
| `node publicar/build.mjs` | verde, **39** páginas (38 + material) | ✅ |
| o caderno aparece no sumário e abre a partir dele | cartão na seção **Material** | ✅ `site/sumario.html` linka `apresentacao-desenvolvimento-maestro.html` |
| **mutação 1** — material ausente do disco | falha nomeando o caminho | ✅ `✗ 1 material declarado em sumario.json e ausente do disco` |
| **mutação 2** — material colide com página gerada | falha nomeando a colisão | ✅ `roadmap.html ← docs/roadmap.md + docs/handbook/roadmap.html` |
| **mutação 3** — link `.html` em bloco HTML para página não publicada | falha como link quebrado | ✅ |
| **mutação 4** — material chamado `index.html` | falha; a capa mantida à mão sobrevive | ✅ `index.html ← site/index.html (a capa, mantida à mão) + …` |
| **mutação 5** — material chamado `sumario.html` | falha, em vez de publicar e descartar calado | ✅ |
| **mutação 6** — material de domínio `toolkit` | `check-boundary.sh` falha nomeando o arquivo | ✅ `✗ 1 page(s) published from the toolkit without being declared shared: scripts/interno.html` |
| `check-boundary.sh` no estado correto | conta o material | ✅ `39 pages: 29 owned by the guide, 10 declared shared` |
| bateria de 16 portões · plugin | verdes salvo o declarado abaixo | ✅ |

Todas as mutações foram rodadas em **cópia** (`/tmp/mut054`); a árvore de trabalho voltou
intacta, conferida por `git status`.

### O vermelho, declarado

- `check-retro.sh` — dívida real e **anterior a este ciclo**:
  `achado-047-cinco-absorcoes-sem-destino` passou do limite de 6 ciclos. A retro é o próximo
  ciclo. Registrado para não passar como ruído de bateria.

## Closing tail — the evidence

- **TAIL:review** — revisão independente em contexto fresco, instruída a refutar e a rodar as
  mutações por conta própria. **Reprovou o ciclo**, e as duas primeiras coisas que achou eu
  tinha acabado de criar:

  1. **Buraco de sobrescrita silenciosa.** O mapa de colisão continha só itens e materiais.
     `index` e `sumario` nunca foram itens — logo nunca estiveram lá. Um material chamado
     `index.html` **substituía a capa versionada** com o build imprimindo `✓ 40 páginas`; o
     revisor provou com o md5 antes e depois. Antes deste ciclo o buraco não existia: nenhum
     arquivo não-`.md` alcançava a raiz de `site/`. Eu abri a porta e não olhei atrás dela.
  2. **`sumario.html` pior ainda**: o material era escrito, depois sobrescrito pelo sumário,
     e **contado como publicado**. O portão de links passava porque compara com o conjunto
     *declarado*, não com o que existe — medir a frase, não o fato, dentro do meu próprio
     ciclo.
  3. **Uma das três mutações que declarei não reprovava.** Eu escrevi "link interno para
     material não declarado → falha" e provei com um bloco HTML; em link **markdown** o
     motor manda para o GitHub e o portão pula URL absoluta. A afirmação era mais larga que
     o teste. Corrigido virando **limite declarado** na FR2, com o `check-links.sh` nomeado
     como quem cobre o caso do alvo inexistente — em vez de inventar portão para forçar todo
     `.html` do repositório a entrar no livro, que seria exagero (`fontes/05-bpmn-processo.html`
     é fonte de diagrama, e link para o GitHub ali é o certo).
  4. **O `check-boundary.sh` ficou cego para o canal novo.** Ele lê `partes`; material é um
     segundo canal. O revisor provou publicando `scripts/interno.html` como material: site
     recebeu o arquivo do `toolkit` e o portão disse `✓ all clear`. É exatamente a falha que
     aquele script existe para impedir, entrando pela porta que ele não vigiava. Portão
     estendido, mutação 6 prova.

  Mais: `Status: Concluída` com a cauda inteira desmarcada e sem `qa-report`; o plano dizendo
  "verdes salvo `check-retro`" quando havia **dois** vermelhos; a linha do Princípio VIII
  afirmando que as mensagens de erro dizem o que fazer quando **nenhuma** dizia; a linha do
  `ux-design=no` dizendo "reusa" enquanto o ciclo introduzia a afinidade `↩ livro`; contraste
  de **3,8:1** no tema claro (abaixo de AA) por causa de `opacity: .55`; e **duas fontes de
  verdade** para o nome do material (`titulo` do sumário × `<title>` do arquivo), já
  divergentes. Todos corrigidos: mensagens ganharam a linha `→ o que fazer`, a opacidade
  saiu, e o nome passou a ter uma fonte só.

  O revisor **não** achou nada em: portões existentes enfraquecidos (fora do buraco acima),
  mutações 1 e 2 (reprovam pelo motivo certo), correção do envelope (os três decks são
  fragmentos, `height:100%` e `scroll-snap` resolvem, a volta não colide com nenhuma peça
  fixa das três e é focável por teclado), contagem de páginas, e as citações `file:line` do
  plano. Deixou a árvore intacta, conferida.

- **TAIL:security** — classe de risco: **o ciclo mexe num portão bloqueante e abre um canal
  de publicação**, então a passada é a alta. Dois achados e um não-achado:
  **(a)** o canal novo escapava do portão de fronteira — corrigido, é o item 4 acima, e é o
  achado de segurança do ciclo: publicação sem guarda é o vetor, não injeção.
  **(b)** `titulo` e `teaser` entram no HTML sem escape, e `resolve(RAIZ, m.arquivo)` aceita
  caminho absoluto (o revisor publicou `/etc/hostname` como página). **Risco declarado nulo,
  com motivo**: toda entrada é arquivo versionado sob revisão humana — `sumario.json` e o
  deck —, é a mesma fronteira de confiança em que o gerador inteiro já vive, e o laço de
  itens tem a mesma forma desde antes deste ciclo. Não há caminho de entrada não confiável.
  O `teaser` ganhou escape de aspas mesmo assim, porque quebrava o atributo por acidente.
  **(c)** o `<title>` lido do arquivo não escapava para fora do elemento (`[^<]*` exclui `<`)
  — e foi removido de qualquer forma, por ser fonte de verdade duplicada.

- **TAIL:gate** — DoD verde, 15 dos 16 portões verdes com o vermelho declarado acima, plugin
  em dia, build do livro verde. **Aguarda o gate humano**: a promoção `dev` → `main` não é
  deste relatório.

## Requirement coverage

- **FR1** — `materiais` publicado e indexado; cartão na seção **Material** do sumário.
- **FR2** — link do livro para material declarado resolve para dentro do livro; link interno
  `.html` para página não publicada reprova (mutação 3). Limite declarado na própria FR.
- **FR3** — colisão com item, com a **capa** e com o **sumário** reprova (mutações 2, 4, 5).
- **FR4** — material ausente do disco reprova (mutação 1).
- **FR5** — volta `↩ livro` injetada na publicação, sem tocar o arquivo de origem; contraste
  corrigido para passar AA nos dois temas.
- **FR6** — `check-boundary.sh` lê os dois canais; material do `toolkit` reprova (mutação 6).

## Pending gate

- Promoção `dev` → `main` aguarda aprovação humana. Ficam pendentes os ciclos **052, 053 e
  054**.
