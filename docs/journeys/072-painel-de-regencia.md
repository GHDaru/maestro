# Jornada 072 — Painel de regência (rodada 1)

- **Spec**: `specs/072-painel-de-regencia/spec.md` · **UX**: `specs/066-painel-de-regencia/ux-design.md` §3
  · **Capturas geradas em**: 2026-10-24 ·
  **Script**: `docs/journeys/scripts/captura-072.sh` (versionado)

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

## Rastreabilidade

`spec 072` ↔ `pull request deste ciclo (w/worker01)` ↔ `test painel/tests/test_regencia.py` ↔ esta jornada.
