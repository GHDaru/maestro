# Jornada 072 — Painel de regência (rodada 1)

- **Spec**: `specs/072-painel-de-regencia/spec.md` · **UX**: `specs/066-painel-de-regencia/ux-design.md` §3
  · **Capturas geradas em**: 2026-10-24 · **regeradas em 2026-10-25** (pós-T16, `bbfab80`) ·
  **Script**: `docs/jornada/scripts/captura-072.sh` (versionado)

<!-- Skill `living-journey`: documento + captura do build REAL por script + heurística DATADA, tudo
     no mesmo pull request. Uma heurística datada antes das capturas é documentação vencida.
     Marcador de fitness function: **F11** (ux-design §7) — jornada viva com captura gerada por
     script versionado e heurística datada ≥ data da captura. -->

> **As capturas são do build real.** O script sobe o próprio painel
> (`painel/server.py painel/projetos/exemplo.json`, porta alta, derrubado ao fim) e fotografa o
> **DOM renderizado** pelo navegador — não um mock, não um arquivo de desenho. É exatamente o que
> as fitness functions F1/F9 **não** cobrem: elas leem a fonte, não a tela executada
> (**D-072-8**). O ambiente renderizou (Playwright + Edge do sistema, headless), então a captura
> **não** está pendente — o plano B da **D-072-7** não foi necessário.

## O que o regente quer alcançar

> "Em 5 segundos, saber o que me espera e quem morreu; em 5 minutos, decidir."

## O caminho (passo a passo, com evidência)

A rodada 1 serve **duas** telas do §3 — o Kanban (passo 5) e a Fila de decisões (passos 2 e 7).
O Mapa de sessões (passo 4) e a Jornada do chamado (passo 6) ficam para a rodada seguinte; não
são fingidos aqui.

| # | Passo | O que o regente vê | Captura |
|---|---|---|---|
| 1 | abre o painel | cabeçalho "Agora" e, abaixo, o quadro por gate: as colunas **G0…G9** e a faixa **Abertura · Risco** (que é faixa, não coluna) | `img/072-01-kanban.png` |
| 2 | procura o que parou na frente | o cartão do chamado do fixture (`000-exemplo`), na **G0** — o cartão mora no **último gate aprovado** e, sem gate aprovado, cai para G0 | `img/072-01-kanban.png` |
| 3 | lê o cartão de relance | `INVÁLIDO` (veredito normalizado), `SELO: REGISTRO`, `dono: —`, `sessão: —`, `integrado = criticado: não conferido` | `img/072-01-kanban.png` |
| 4 | confere a independência entre quem fez e quem julgou | `—` **com o motivo** — `(motivo: cabeçalho do gate sem autor_da_peca (FR5))`; nunca um valor padrão | `img/072-01-kanban.png` |
| 5 | troca para a Fila de decisões | a tela declara **"fila vazia — nenhuma decisão registrada"**, contador **0** (o registro do fixture não tem linha) — vazio é informação, não erro | `img/072-02-fila.png` |
| 6 | (o que a rodada 1 ainda **não** serve) | Mapa de sessões e Jornada do chamado — declarados como fora da rodada; a concessão de G7/G8 pela fila depende de haver ruling na fila | — |

**Como as capturas foram obtidas.** A derivação do painel é **preguiçosa e assíncrona**
(`chamados.em_cache`): na primeira consulta o servidor devolve a lista vazia enquanto varre o git
em segundo plano. Capturar sem esperar produziria uma foto **falsa** de "quadro vazio". Por isso
o script tem uma fase de **aquecimento** — consulta `/api/chamados` até a derivação estabilizar
(`derivação estabilizada com 1 chamado(s) em 2.1s` na execução que gerou estas imagens) — e só
então fotografa. Esse comportamento virou o achado **R1** da heurística abaixo.

## Avaliação heurística — revisitada em 2026-10-24

| ID | Achado | Severidade | Status |
|---|---|---|---|
| R1 | **Derivação preguiçosa sem estado "carregando".** Na primeira consulta o painel mostra a lista vazia enquanto calcula (varredura do git). O §3 manda que a tela tenha cara própria para **carregando** ("fonte sendo reingerida; mostra `meta.ingerido_em`") e que se > 1 h o painel se declare **defasado** no cabeçalho. Hoje o regente que abre o painel no servidor frio vê um "vazio" que **não é** o estado do projeto. O script contorna (aquece antes de fotografar), mas a tela **não** — confundir "vazio" com "ainda calculando" é a pior hora de errar (às 07:00, o regente decide com essa leitura). | Média | 📝 registrado para a rodada 2 |
| R2 | **Vazio declarado como informação.** A Fila de decisões diz "fila vazia — nenhuma decisão registrada" e mostra 0, em vez de sumir ou de mostrar um placeholder — conforme o §3 ("vazio é informação, não erro"). | — | ✅ conforme |
| R3 | **"—" com motivo, nunca valor padrão.** Fonte ausente aparece como `—` acompanhado do motivo (`cabeçalho do gate sem autor_da_peca (FR5)`), e não como `0`/`n/a` — conforme a anti-regra 3 do §4. | — | ✅ conforme |
| R4 | **Nada é marcado "conferido" o que foi calculado à mão.** O cartão mostra `integrado = criticado: não conferido` — conforme a anti-regra 8 do §4. | — | ✅ conforme |
| R5 | **O veredito original permanece ao lado do normalizado.** O cartão mostra `INVÁLIDO` (normalizado) e o campo `original` — conforme a anti-regra 6 ("não unifica apagando"). | — | ✅ conforme |
| R6 | **A rodada 1 não exercita o caminho do ruling no build real.** O fixture tem a fila vazia, então a concessão de G7/G8 pela fila (§3 passo 7) e o estado **"sem permissão"** (a ação do regente vista por um agente) **não** aparecem em captura. O que prova esse caminho é o teste de contrato (`painel/tests/test_regencia.py`, fatias T03b/T05), não a tela. Fica registrado para a rodada 2, quando houver chamado real na fila. | Baixa | 📝 registrado para a rodada 2 |

## Avaliação heurística — revisitada em 2026-10-25

Por **acréscimo**, não por reescrita: a tabela de 2026-10-24 acima fica exatamente como está (a
datação é histórico) e esta revisão só **registra o que ela não listava**. A revisão olha a
**mesma** captura de 2026-10-24 — que já mostrava os dois achados abaixo — junto com a medição
feita sobre o **build real** desta rodada; a data desta heurística é **posterior** à da captura,
como a skill `living-journey` exige.

| ID | Achado | Severidade | Status |
|---|---|---|---|
| R7 | **O quadro não parece um quadro.** O §3 passo 5 pede as colunas **G0…G9** lado a lado, para o regente ler o fluxo de um relance. No build real elas **empilham numa coluna estreita**: medido na página renderizada (janela de 1440×900), o `<main id="main">` fica com **232 px** dentro do grid `.app` (`232px 1208px`), o invólucro do quadro fica com **176 px** e o grid do quadro resolve para **uma** trilha de `210px` (`repeat(auto-fill, minmax(210px,1fr))`, `painel/index.html:917`). Resultado: as 10 seções têm **todas `x = 28`** e `y` de 1499 a 2386 — empilhadas, não lado a lado. A captura `img/072-01-kanban.png` mostra o mesmo: coluna única à esquerda, o resto da tela vazio. | Média | 📝 registrado para a **rodada 2** — não é desta rodada consertar |
| R8 | **O aviso de leitura velha tem arredondamento discordante.** O banner monta as horas com `Math.floor` e os minutos com `Math.round` sobre um valor **fracionário** (`painel/index.html:962`), e esse valor chega com uma casa decimal de `painel/server.py:295` (`round(…, 1)`). Com 119,6 minutos isso rende **`1h60m`** — um horário impossível, que não é 2 h nem 1 h 59 m. A captura de 2026-10-24 registra exatamente esse texto: `LEITURA VELHA: 1H60M DESDE O ÚLTIMO INGEST`; medido ao vivo nesta revisão, 829,5 min rendeu `13h50m`. | Baixa | 📝 destino: **T16 (Worker04)** — nesta worktree (`e9601ac`) o T16 ainda **não** está integrado |

> **Sobre uma captura nova (2026-10-25).** O T16 mexe no banner, então uma captura *depois* dele
> mostraria o R8 fechado. Nesta worktree o **T16 não está integrado** — `painel/index.html:962` e
> `painel/server.py:295` seguem pré-correção — por isso **não** regenerei as imagens: as mesmas
> `img/072-01-kanban.png` e `img/072-02-fila.png` continuam válidas para este build, e sobrescrevê-las
> trocaria a evidência do `1h60m` por uma foto **ainda defeituosa**, deixando o cabeçalho (que data
> 2026-10-24) mentindo. A captura nova fica **pendente do T16**.

> **A captura nova está feita (2026-10-25, pós-T16).** O **T16 foi integrado** (`bbfab80`, ancestral
> do HEAD `d71cee6`) e a pendência declarada logo acima fica **fechada**: o
> `docs/jornada/scripts/captura-072.sh` foi rodado de novo e regravou `img/072-01-kanban.png` e
> `img/072-02-fila.png` a partir do **build real** — as imagens em disco agora são **deste** build.
>
> Medido ao vivo na página renderizada (janela de 1440×900): o banner resolve para
> **`LEITURA VELHA: 15H35M DESDE O ÚLTIMO INGEST`** (ingestão de 935,1 min; `floor(15,58 h)=15`,
> `round(35,1 min)=35` — coerente). O **`1H60M` impossível não aparece mais**: o **R8 está fechado**
> neste build — o banner passa a vir pronto do servidor
> (`painel/regencia/normalizacao.py`), não mais montado no JS. Em contrapartida, a imagem de
> 2026-10-24 que registrava o `1H60M` foi **sobrescrita** (o script grava em nome fixo); o achado
> segue registrado **no texto** da linha R8 acima, mas a foto do defeito não existe mais em disco.
>
> O **R7 não é desta rodada** e **reproduz igual**: `main` = 232 px no grid `.app`
> (`232px 1208px`), grid do quadro = **uma** trilha de `210px`, as 10 seções G0…G9 todas em
> `x = 28` — coluna única à esquerda, resto da tela vazio. Segue para a **rodada 2**.

## Rastreabilidade

`spec 072` ↔ `pull request deste ciclo (w/worker01)` ↔ `test painel/tests/test_regencia.py` ↔ esta jornada.
