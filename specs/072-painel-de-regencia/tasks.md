# Tasks 072 — Painel de regência, rodada 1: kanban por gate e fila de decisões

> Uma seção por Worker, com a etiqueta `[[TASK ...]]` sozinha na linha (task-ledger). Quem executa
> termina com `[[DONE id=… outcome=delivered|blocked|failed]]`. **Nenhuma caixa é marcada antes de a
> evidência existir** — a caixa registra o que aconteceu, não o que se pretende.
>
> Plano: `plan.md` — **aprovado COM CONDIÇÕES** no gate do plano (delegado ao crítico independente,
> ADR 0026); **a reconciliação `072-T02b` com os testes faz parte desse gate**, não o pressupõe. Spec:
> `spec.md` — **revisão T01b**, 25 FR. Os **13 testes já existem** (`c1eb802`,
> `painel/tests/test_regencia.py`, 465 linhas) e são a autoridade das assinaturas — ver a tabela
> **"Nomes fixados"** de `plan.md`.
>
> Siglas: ADR (*Architecture Decision Record*) · AST (*Abstract Syntax Tree*) · CI (*Continuous
> Integration*) · DoD (*Definition of Done*) · FR (*functional requirement*) · HTML (*HyperText Markup
> Language*) · JSONL (*JSON Lines*) · PR (*pull request*). Correção de contagem (T14): a spec tem
> **27 FR** (FR1–FR27), não 25.

## Verification first

- [x] **V0** — A DoD executável de `plan.md § Verification` (**`Ran 15 tests`**: os 13 de `c1eb802` +
  as 2 provas de FR16 que o gate do plano acrescentou) é a régua deste ciclo. Os testes **já existem e
  já estão vermelhos**: neste ciclo o vermelho **precede** o verde no repositório (Princípio IV).
  Cada Worker deixa **verde a sua fatia** e registra no `qa-report.md` o **hash** em que o vermelho
  foi capturado e o hash do verde.
- [ ] **V0b — três regras de convivência com o arquivo de testes** (fonte de conflito, declaradas para
  não se repetir a dor): (i) **ninguém reescreve a fatia de outro** — cada Worker **apensa** o seu
  bloco ao fim, com comentário-cabeçalho `# --- FATIA W0N ---`; (ii) só se **adapta** um teste quando a
  tabela "Nomes fixados" de `plan.md` marca **"adapta"** para a sua fatia; (iii) ninguém "conserta" um
  teste mudando a regra do plano em silêncio — a divergência volta ao plano.

## Escopo A — kanban por gate

### Worker03 — domínio puro + parser (FR5)

`[[TASK id=072-T03 kind=implement cycle=072 attempt=1]]`

- [x] Criar `painel/regencia/` (**puro**): `__init__.py` (**reexporta todos os nomes públicos** — os
      testes resolvem as funções **pelo pacote**, `test_regencia.py:64`), `normalizacao.py`
      (`normaliza(valor, erros=None)` — FR10, `sem_fonte` — FR22, `aviso_ingestao` — FR25),
      `kanban.py` (`coluna_do_cartao`, `independencia`, `idade_do_carimbo`, `cartao`,
      `proposta_transicao`, `faixa_abertura_gd` — FR2/FR4/FR23/FR8/FR1) e `fila.py` (`valida_pedido`,
      `valida_ruling(ruling, pessoas=None, pedidos=None)`, `sai_da_fila`, `ordena_fila`,
      `portao_derivado`, `portoes_do_regente` — FR11/FR14/FR20/FR12/FR15). **Nada** em
      `painel/regencia/` importa `http.server`, `sqlite3`, `chamados` nem abre arquivo.
- [x] **Adaptar a sua fatia** de `painel/tests/test_regencia.py` (a autoridade): **F6** (`normaliza`
      devolve **dict**, não `str`) e **F2** (`proposta_transicao` devolve `{permitido, falta?}`, não
      levanta `ValueError`) — só esses dois "adaptam" nesta fatia. Os outros quatro (**F4**, **F5**,
      **F7**, **F8**) já chamam nomes que o plano fixou; deixá-los verdes **sem** reescrever a fatia de
      outro Worker.
- [x] **FR5**: estender `painel/chamados.py` (`valida`/`confere`, ~`painel/chamados.py:81-148`) para
      ler `autor_da_peca` do cabeçalho do gate e devolvê-lo **no item**, ao lado de `por`. **Sem o
      campo → "—" com motivo** (nunca verde presumido). Não tocar `conferir_chamado.py`.
- [x] Regressão: `painel/tests/test_chamados.py` verde e `python painel/chamados.py
      painel/projetos/exemplo.json` → exit 0.
- Evidência: hash do vermelho e do verde; saída dos testes no `qa-report.md`.
- **Depende de**: `plan.md` reconciliado (T02b). **Entrega para**: W04, W05, W07 (a tabela "Nomes
  fixados" pronta + o pacote reexportando).

### Worker04 — rotas e tela do kanban

`[[TASK id=072-T04 kind=implement cycle=072 attempt=1]]`

- [x] `GET /api/regencia/kanban` em `painel/server.py`: dez colunas G0–G9 (FR1) **reusando**
      `chamados.confere` (não criar segundo conferidor), o cartão com id/frente/dono(papel+sessão)/
      veredito normalizado **ao lado do original**/idade/selo (FR3), o marcador de independência
      (FR4) e a **faixa `abertura`·`GD`** acima do kanban (limites da spec).
- [x] `POST /api/regencia/transicao` com corpo **`{chamado, de, para}`** (`contracts/rotas.md`):
      consome `proposta_transicao(...)` e devolve a proposta; **não move nem grava**; recusa → **422
      com o motivo do campo `falta`** (FR9). Manter a recusa fora de localhost
      (`painel/server.py:507`) e o `ValueError`→422 (`:523`).
- [x] `cfg["frentes"]` exposto em `/api/meta` (`v_meta`, `painel/server.py:283`) e filtro por frente
      na tela (FR7); sem escolha, todas.
- [x] Tela do kanban em `painel/index.html` (`vKanban` + botão de nav): lista (não `div` solta),
      estado nunca só cor, todo número/selo com `data-fonte` (FR21), "—" com `motivo:` (FR22),
      botões só-ícone com `aria-label` (FR24).
- [x] **Adaptar F3** (corpo `{chamado, de, para}` e o caminho `/api/regencia/transicao`) e deixar
      verdes **F1**, **F9** (sobre o **HTML renderizado**, não `grep` no fonte) e **F10** — todas
      **apensadas ao fim** do arquivo, no bloco `# --- FATIA W04 ---`.
- Evidência: hash; a saída dos testes de HTML renderizado no `qa-report.md`.
- **Depende de**: W03 (parser + `regencia/`). **Fatia**: `painel/server.py` (funções do kanban e da
  transição), `painel/index.html` (`vKanban`).

## Escopo B — fila de decisões

### Worker05 — registro (com backup), rotas e tela da fila

`[[TASK id=072-T05 kind=implement cycle=072 attempt=1]]`

- [x] `painel/fila_registro.py` (adaptador): `caminho(cfg)` (padrão
      `painel/dados/fila-<projeto>.jsonl`, chave `cfg["fila_decisoes"]`), `acrescenta(caminho, linha)`
      — **sempre** `open(..., "a", encoding="utf-8")`, `json.dumps(..., ensure_ascii=False)` + `\n`,
      **nunca** `"w"`/`truncate`/`seek` — `le(caminho)` tolerante a linha inválida (FR16) e
      **`backup_datado(caminho, agora)`** (cópia do dia antes da primeira escrita), tudo sob um
      `threading.Lock` de módulo (FR16; `plan.md` §2 e `adr-0027-rascunho.md`).
- [x] `GET /api/regencia/fila` (pedidos + portões derivados, ordenados por prazo × bloqueio com nº de
      destravados — FR15) e `POST /api/regencia/fila` (acrescenta `pedido` ou `ruling`; **422 com
      motivo** — FR11/FR14/**FR20**). Manter a recusa fora de localhost. A resposta do acréscimo traz
      `"backup"` quando o backup do dia foi criado nessa chamada (`contracts/rotas.md`).
- [x] **FR20**: para cada G7/G8/`TAIL:gate` pendente, criar o **item de fila** com id derivado
      (chamado+gate), status do arquivo de gate e "desde quando" do commit; **marcador no cartão** com
      link para o item; a um agente, **somente leitura** ("portão do regente"). O adaptador resolve
      **`cfg["regencia"]["pessoas"]`** (autor humano fora da lista → 422) e os **pedidos conhecidos**
      (ruling para pedido inexistente → 422) e passa os dois a `valida_ruling`.
- [x] Tela da fila em `painel/index.html` (`vFila` + botão de nav): item, idade **"há Xh Ymin" + o
      carimbo absoluto** no atributo do elemento, **contador da idade do item mais velho no
      cabeçalho** (FR23); "responder" grava `autor = humano` do formulário (FR18), **nunca
      pré-marcado** (FR19); "devolver a quem pediu" registrado (FR13); "encaminhado a …" (FR13);
      fila vazia = "fila vazia — última decisão às HH:MM".
- [x] **Adaptar F14** para `import fila_registro` (o `acrescenta` vive no **adaptador**, nunca no
      pacote puro) e **apensar as 2 provas novas** do gate do plano:
      `test_f14_registro_abre_sempre_em_append` (AST: todo `open` de `fila_registro.py` é de
      acrescentar) e `test_f14_registro_concorrente_sem_perda` (2 `POST` paralelos → 2 linhas). Manter
      `test_portao_do_regente_item_com_id_derivado` verde e acrescentar os **2 negativos de FR20**.
      Bloco `# --- FATIA W05 ---` no fim do arquivo.
- Evidência: hash; a saída do teste do prefixo de bytes, do AST e do concorrente no `qa-report.md`.
- **Depende de**: W03 **e** `072-T09` (a linha da ADR 0027 no índice entra **antes** deste código).
  **Fatia**: `painel/server.py` (`v_fila` + ramo do JSONL), `painel/index.html` (`vFila`).

## Escopo C — herança do 070 (a dívida 5 vira FR)

### Sessão Worker02 [cb28ea] — append-only mecânico na base (FR17)

`[[TASK id=072-T07 kind=implement cycle=072 attempt=1]]`

- [x] `painel/schema_workflow.sql`: **quatro** `TRIGGER`. `rodadas`, `transicoes` e `fila` recusam
      `UPDATE` **e** `DELETE`; `passos` recusa `DELETE` sempre e `UPDATE` **com `WHEN`** — permitido
      **só** enquanto `saida_em IS NULL` **e** só nas colunas `saida_em`, `resumo`, `resultado`;
      qualquer outra coluna (ou um passo já fechado) → `RAISE(ABORT, 'append-only: …')`. Hoje **não há
      gatilho nenhum** no arquivo (só `CREATE TABLE`, `painel/schema_workflow.sql:11-45`).
- [x] **`painel/hooks/workflow_stop.py` NÃO é tocado**: o `WHEN` libera exatamente o `UPDATE` que o
      `Stop` faz para fechar o passo (FR3 do 070). Nada de "consertar" o hook — é assim que a dívida 5
      é paga **sem** inverter o FR3 (dívida 7 continua na rodada 2; declarar no `qa-report.md`).
- [x] `CREATE TRIGGER IF NOT EXISTS` nas cópias de `_ensure_schema` (hooks + `fila_outbox.py`) para
      que um banco vivo ganhe os gatilhos — e **declarar** que a dívida 2 **piora** (D-072-2).
- [x] **Adaptar** `test_divida5_gatilho_recusa_update_e_delete` ao desenho real do gatilho (a forma
      antiga do teste recusava **todo** `UPDATE passos`; com o `WHEN` isso mudou): `rodadas`,
      `transicoes` e `fila` → `UPDATE`/`DELETE` recusados; `passos` → `DELETE` recusado sempre;
      `UPDATE passos SET resumo=…` **com `saida_em IS NULL` passa** (é o fechamento do passo);
      `UPDATE passos` **já fechado** e `UPDATE` de coluna fora das três → recusados. Bloco
      `# --- FATIA W07 ---` no fim do arquivo.
- Evidência: hash; a saída do teste do gatilho no `qa-report.md`; a declaração de que a dívida 2
  **piora** (D-072-2) e de que a dívida 7 **não** é paga nem o hook foi retocado.
- **Depende de**: nada (paralelo a W03/W04/W05). **Não compartilha arquivo** com W04/W05 (`server.py`
  / `index.html`), então pode correr junto.

### Sessão Worker02 [31f7bf] — ajustes de texto pós-T03/T07 (T11, decisão do regente)

`[[TASK id=072-T11 kind=fix cycle=072 attempt=1]]`

> Decisão do regente (24/10, ao aceitar T03 e T07): o texto do 422 do *ruling* sem destinatário
> fica **"ruling sem destino"** — o contrato adapta-se ao teste F5 (que exige `destino` no
> motivo) e ao glossário ("destino da resposta"); a função pura devolve o mesmo texto.

- [x] `specs/072-painel-de-regencia/contracts/rotas.md`: o corpo 422 passa a
      `{"erro": "ruling sem destino"}` (o **campo** `destinatario` do esquema do ruling **não**
      muda — é nome de campo, não mensagem).
- [x] `painel/regencia/fila.py`: `valida_ruling` devolve `"ruling sem destino"` (sem o híbrido
      `"(destinatario)"` usado no T03 para manter a fatia verde).
- [x] Conferir — **não refazer** — que o plano já traz `cabecalho_fila` na tabela "Nomes
      fixados" e a DoD com `Ran 24 tests` (commit `2d9ef37`); se algo tiver faltado, completar e
      declarar.
- Evidência: `grep -n 'ruling sem destino' specs/072-painel-de-regencia/contracts/rotas.md
  painel/regencia/fila.py` → 2 ocorrências; `pytest painel/tests/test_regencia.py::TestF5Ruling
  -q` → verde.
- Commit: "ciclo 072: plano e contratos ajustados após T03/T07".

## Escopo D — jornada viva e artefatos vivos

### Sessão Worker01 [21d8d2] — ADR 0027 + índice + glossário (bloqueia W05)

`[[TASK id=072-T09 kind=docs cycle=072 attempt=1]]`

- [x] `docs/adr/0026-gate-humano-por-delegacao-de-politica.md` **já existe** (a decisão do DoR/plano) —
      conferir e **não** reescrever; e escrever `docs/adr/0027-registro-da-fila-e-append-only-mecanico.md`
      a partir do rascunho `specs/072-painel-de-regencia/adr-0027-rascunho.md` (padrão do cabeçalho dos
      vizinhos), somando a linha ao `README.md` dos ADRs.
- [x] `docs/records/decisoes.jsonl`: **só acrescentar** a linha da ADR 0027 via
      `scripts/record-decision.sh` (o comando exato está no fim do rascunho) — **nunca** reescrever
      (guard `guard-immutables.py`). **Esta entrega vem ANTES do código de W05.**
- [x] `docs/governance/glossary.md` (em inglês, ADR 0014): **painel de regência**, **pedido de
      decisão**, **ruling**, **veredito normalizado**, **portão do regente** (coluna "Cycle 072").
      Critério: `grep -c 'Cycle 072' docs/governance/glossary.md` → 5 e `check-language.sh` verde.
- Evidência: `ls docs/adr/0027-*.md`; a linha no índice (`grep -c 'adr-0027' docs/records/decisoes.jsonl`
  → 1); `scripts/check-adr.sh` verde; o `grep -c 'Cycle 072'` → 5.
- **Depende de**: T02 (plano). **Bloqueia**: W05 e W08.

### Sessão Worker01 [21d8d2] — jornada viva (FR26), depois de T09

`[[TASK id=072-T08 kind=docs cycle=072 attempt=1]]`

- [x] `docs/journeys/072-painel-de-regencia.md` (skill `living-journey`): o caminho passo a passo do
      regente (ux-design §3), as **imagens geradas por um script versionado** do build real
      (`docs/journeys/scripts/captura-072.sh`) e a **heurística datada ≥** a data da captura, com
      severidade e status por achado; o documento cita a spec e traz o marcador **F11**.
- [x] Se o ambiente **não** renderizar a tela real: entregar o script e a heurística e declarar a
      captura como **pendente** (D-072-7) — **nunca** inventar imagem nem reaproveitar captura velha.
      O que F1/F9 **não** cobrem (a tela renderizada por JavaScript) é a razão de existir desta
      jornada — declarado em **D-072-8**.
- [x] Somar `docs/journeys/*.md` ao glob `documentos.jornadas` de `painel/projetos/exemplo.json`
      (hoje só `docs/jornada/*.md`; a skill usa o plural em inglês — `skills/living-journey/SKILL.md:30`).
- Evidência: `ls docs/journeys/072-*.md`; `grep -c 'F11' docs/journeys/072-*.md` ≥ 1; `check-links.sh`
  verde (as imagens/links relativos resolvem).
- **Depende de**: T09 e as telas de W04/W05 (a captura precisa do alvo existir).

### Sessão Worker01 [21d8d2] — artefatos vivos do fechamento

`[[TASK id=072-T10 kind=docs cycle=072 attempt=1]]`

- [x] `CHANGELOG.md` `[Unreleased]` (entrada "ciclo 072") e `docs/roadmap.md` (linha do ciclo 072,
      com a **rodada 2 declarada infra**). Critério: `grep -c 'ciclo 072' CHANGELOG.md` ≥ 1;
      `grep -c '072' docs/roadmap.md` ≥ 1.
- [x] Conferir que `specs/072-painel-de-regencia/` traz os artefatos condicionais do plano no mesmo PR
      (`plan.md`, `tasks.md`, `data-model.md`, `contracts/`, `ux-design.md` apontador,
      `adr-0027-rascunho.md`, `qa-report.md`).
- Evidência: saída dos `grep` e `ls specs/072-painel-de-regencia/`.
- **Depende de**: T09. **Fecha antes** do gate humano.

## Fechamento — revisão, segurança, mutação e DoD

### Worker06 — revisão e segurança em contexto fresco + `qa-report.md`

`[[TASK id=072-T06 kind=review cycle=072 attempt=1]]`

- [x] Revisão **em contexto fresco**, por quem não executou (Teorema 2), do diff integrado contra o
      plano, os 25 FR e a tabela **"Nomes fixados"**: veredito no `qa-report.md`. Procurar os
      anti-padrões (`anti-patterns`, 23 itens), com atenção a "cópia com perdas" do conferidor e a
      `abertura`/`GD` virando coluna.
- [x] **Passo de segurança** proporcional à classe (média: rotas POST novas, gatilho que passa a
      recusar escrita na base herdada, leitura/escrita de arquivo local): confirmar que nenhuma rota
      POST aceita fora de `127.0.0.1`, que o *ruling* grava `autor` do formulário (não inferido do
      agente que pediu) e o recusa quando fora de `regencia.pessoas`, que
      `grep -rn '\.env\|settings.local.json' painel/` não acha caminho de **leitura**, e que as dívidas
      herdadas de segurança (**D-072-3**, CSRF/autoria; **D-072-4**, `data()`; **D-072-5**, `custo.py`)
      ficam **declaradas** — não silenciadas nem vendidas como pagas. Veredito no `qa-report.md`.
- [x] Colar no `qa-report.md` a saída real de **cada** linha da DoD do plano (**`Ran 15 tests`**, os 13
      nomeados, as 2 provas de FR16, os 2 negativos de FR20, os pares comando → resultado, as
      regressões) e as dívidas **D-072-1..8** como dívida. Anotar ali a **supersessão declarada** de
      `Ran 13 tests` → `Ran 15 tests` (condição do gate do plano), para que a divergência com a spec
      fique **visível**, não silenciosa.
- [x] `[[DONE id=072-T06 outcome=delivered|blocked|failed]]` ao terminar.
- **Depende de**: W03, W04, W05, W07, T08, T09, T10 integrados.

## Rodada de correção — reservas R1/R2 do T06 (decisão do regente, 24/10)

> Veredito do T06: **aprovado com duas reservas bloqueantes** (R1 — `_pasta_do_chamado` duplicado
> mata FR9 na rota e F3 é vácuo; R2 — `check-boundary` vermelho com a jornada em `docs/journeys/`).
> O regente confirmou ambas e decretou **uma** rodada de correção, sem novo gate (regra das duas
> rodadas). A reverificação (T06 attempt=2) cobre SÓ R1 e R2.

### Worker04 — R1: rota de transição sem crash, F3 com teor

`[[TASK id=072-T12 kind=fix cycle=072 attempt=1]]`

- [x] Remover a definição duplicada de `_pasta_do_chamado` em `painel/server.py` (`:400` devolve
      `(pasta, rel)`; `:582` devolve string e **sombreia** a primeira), mantendo a correta e
      corrigindo `_arquivos_do_gate` (`:430`).
- [x] Tornar o F3 **não vácuo** em `painel/tests/test_regencia.py`: transição válida (de G1 para G2
      com o arquivo G2 presente) → **200** com `{"permitido": true}`; sem o arquivo → **422** com
      "falta" no motivo; o 422 **nunca** vem de exceção (nenhum Traceback no stderr do servidor).
- [x] Suíte **24/24** e antiga **48/48**.
- Commit: "ciclo 072: R1 — rota de transição sem crash, F3 com teor".

### Worker01 — R2: jornada em docs/jornada/ (boundary.json)

`[[TASK id=072-T13 kind=fix cycle=072 attempt=1]]`

- [x] `git mv` de `docs/journeys/072-painel-de-regencia.md`, `scripts/` e `img/` para
      `docs/jornada/` (mesma estrutura); corrigir todos os links e o glob em
      `painel/projetos/exemplo.json`.
- [x] Rodar o bloco do check-boundary e do check-links (verdes).
- Commit: "ciclo 072: R2 — jornada em docs/jornada/ (boundary.json)".
- Nota do Gerente (24/10, ressalva do W01 aceita): os **comandos de evidência da DoD** em
  `plan.md` §Verification e `spec.md` §Acceptance criteria passam a apontar `docs/jornada/` — o
  texto histórico do T08 acima fica como está (registra o despacho como foi feito).

### Worker02 — contagem de FR: 27, não 25

`[[TASK id=072-T14 kind=fix cycle=072 attempt=1]]`

- [x] `spec.md` tem **27 FR** (FR1–FR27): corrigir onde o número aparece — `plan.md` e o cabeçalho
      do `qa-report.md`, **uma linha cada**.
- Commit citando "ciclo 072".

### Worker06 — reverificação R1/R2 (após a integração dos três acima)

`[[TASK id=072-T06 kind=review cycle=072 attempt=2]]`

- [x] Reverificar **SÓ R1 e R2**: reexecutar o F3 e o check-boundary; anexar ao qa-report a seção
      "### reverificação R1/R2" com a saída. Depois: `scripts/check-conformance.sh 072` e
      `--ticked-only` (verdes) — e o Gerente fecha com `[[DONE 072-rodada-1]]`.

## Condições do gate (rodada curta, 25/10 — aprovado com condições pelo crítico process-guardian)

`[[TASK id=072-condicoes-do-gate kind=fix cycle=072 attempt=1]]`

- [x] **T15 (Worker05, dono da fila)**: `exemplo.json` ganha `regencia` (pessoas, fila_decisoes) e
      `frentes`; README documenta as três chaves; build real com UM POST de pedido e UM de ruling
      válidos (200 + duas linhas no JSONL, colados aqui) e um ruling com autor fora de pessoas
      (422); `valida_pedido` recusa id duplicado e id com formato de portão derivado, com teste;
      risco "ruling fecha o item errado em silêncio" registrado como fechado.
      **Entregue: `11d295b` — os 5 itens fechados; build real com as saídas coladas no qa-report
      (200/200/422, fila vazia no GET seguinte); `TestF11IdDoPedido` (função pura + rota 422);
      divergências declaradas no README (`frentes` é mapa; `fila_decisoes` no nível de topo).**
- [x] **T16 (Worker04, dono do kanban)**: `chamado` do POST de transição só aceita `^[\w.-]+$` e
      nunca `..` (422, com teste — hoje `chamado=".."` lista a raiz); arredondamento do aviso
      "LEITURA VELHA" unificado (banner de cima × de dentro: 1H60M contra 1 h 59 min), com teste.
      **Entregue: `39c2957` + `c8632db` (evidência), integrado em `bbfab80` — decisão: FECHADA
      (não existe D-072-9). Suíte 24→26 (2 testes novos: TestT16ChamadoNaoNavega,
      TestT16LeituraVelhaConcorda); 26 passed + 48 passed.**
- [x] **T17 (Worker01, dono da jornada)**: heurística datada ganha, por acréscimo, o quadro
      estreito (~190px, G0–G9 empilhados — severidade, rodada 2) e o banner 1H60M; nova captura
      pós-T16 se o script rodar. **Entregue: `02e434f`, integrado em `1998e3e` — bloco novo
      "Avaliação heurística — revisitada em 2026-10-25" (+20/−0, nenhuma linha existente tocada)
      com R7 (quadro estreito, Média, rodada 2) e R8 (banner 1H60M, Baixa, T16). Captura nova
      declarada PENDENTE do T16 — agora desbloqueada (T16 integrado em `bbfab80`), pedida ao W01.**
      **Captura entregue: `6f91826` (W01, base `d71cee6` por ff-only) — regerada do build real pós-T16;
      o banner `1H60M` não aparece mais (`LEITURA VELHA: 15H35M`, coerente: floor(15,58h)=15,
      round(35,1min)=35) — R8 FECHADO no build; R7 reproduz igual (232px, coluna única) e segue para a
      rodada 2; a foto de 24/10 foi sobrescrita pela regeração (nome fixo do script) — o achado
      permanece no texto (jornada R8 + qa-report § 072-T17-captura). Evidência: qa-report §
      "072-T17-captura".**
- [x] **T18 (Worker02)**: plan § Dívidas ganha a dívida do método (living-journey × docs/jornada/)
      e a D-072-9 se o T16 declarar em vez de fechar. **Entregue: `ae1fb84` (item 1, integrado em
      `85b1b7f`); item 2 resolvido por decisão do T16 — FECHADA, a D-072-9 não existe. T18
      encerrado.**
- [ ] **T19 (Gerente)**: caixas das entregas marcadas com hash de cada uma (§ "Entregas e
      hashes") e linha de status de fechamento no topo do qa-report. **Entregue.**
- [ ] **Reverificação (Worker06, depois de T15–T18)**: as quatro condições, curto; depois
      check-conformance 072 nos dois modos e `[[DONE 072-condicoes]]`.

## Entregas e hashes (T19, 25/10 — as caixas acima marcadas, com o hash de cada uma)

> A pedido do gate (crítico process-guardian): as caixas das tarefas entregues ficam marcadas e
> o hash de cada entrega fica registrado aqui — o `--ticked-only` não pode passar por omissão.
> V0b não é entrega (são as três regras de convivência, vigentes); TAIL:gate é do regente.

| Tarefa | Entregue em | Evidência |
|---|---|---|
| V0 (T03b) — testes reconciliados | `42e24f4` (vermelho capturado; integrado em `2b0b768`) | reconciliação da DoD no plan: `2d9ef37` (supersessão 13→15→24) |
| T03 — domínio puro + FR5 | `da3f724` | qa-report § 072-T03 |
| T04 — kanban (rotas + tela) | `0a9a44a` (F3 movido para depois de `_sobe()`: `2d4a8c5`) | qa-report § 072-T04 |
| T05 — fila (registro + rotas + tela) | `2826278` | qa-report § 072-T05 |
| T07 — gatilhos append-only | `61e78b5` | qa-report § 072-T07 |
| T09 — ADR 0027 + índices + glossário | `fe74587` (ADR e índices, MAESTRO) · `d8c63b6` (glossário, integrado em `d8aa60f`) | qa-report § 072-T09 |
| T11 — "ruling sem destino" | `573a6f5` | qa-report § 072-T11 |
| T08 — jornada viva | `3cbd9f1` (base `2d4a8c5`) | qa-report § 072-T08 |
| T10 — CHANGELOG + roadmap | `f9f0f0d` | qa-report § 072-T10 |
| T06 attempt=1 — revisão + segurança + mutação | veredito no qa-report (aprovado com R1/R2 bloqueantes) | qa-report §§ revisão/segurança/mutação |
| T12 — R1 (rota de transição, F3) | `d18b5b2` (integrado em `8b08112`) | qa-report § 072-T12 |
| T13 — R2 (jornada em docs/jornada/) | `7b0c946` | qa-report § 072-T13 |
| T14 — contagem de FR (27) | `f0c2b39` | qa-report § 072-T14 |
| T06 attempt=2 — reverificação R1/R2 | `e0ff6f2` (HEAD `ccbceef`) | qa-report § Reverificação R1/R2 |
| T16 — chamado sem navegação + LEITURA VELHA | `39c2957` + `c8632db` (evidência; integrado em `bbfab80`) | qa-report § 072-T16 · suíte 24→26 |
| T17 — R7/R8 na heurística datada | `02e434f` (integrado em `1998e3e`) + captura `6f91826` | qa-report § 072-T17 · § 072-T17-captura (R8 fechado no build pós-T16) |
| T18 — dívida do método no plan | `ae1fb84` (integrado em `85b1b7f`) | plan § Dívidas declaradas |
| T15 — id do pedido protegido + exemplo/README | `11d295b` | qa-report § Rodada de correção 2 · `TestF11IdDoPedido` |

## Rodada de correção 2 — condição do gate (process-guardian, contexto fresco)

> O gate do 072 foi aprovado **com condições**. Esta é a condição do dono da fila (Worker05).

### Worker05 — o id do pedido protegido (risco fechado)

`[[TASK id=072-T15 kind=fix cycle=072 attempt=1]]`

- [x] `painel/projetos/exemplo.json`: `regencia.pessoas` (nomes fictícios), `fila_decisoes` (caminho
      padrão) e `frentes`.
- [x] `painel/README.md`: documenta as três chaves.
- [x] Build real: 1 `POST` de pedido e 1 de *ruling* válidos (200; duas linhas no `JSONL`) + 1
      *ruling* com autor fora de `pessoas` (422) — saídas coladas no `qa-report.md`.
- [x] `valida_pedido` recusa id duplicado e id no formato de portão derivado (`chamado+gate`), com
      teste (`TestF11IdDoPedido`).
- [x] Risco "ruling fecha o item errado em silêncio" registrado como **FECHADO** no `qa-report.md`.
- Suíte: regência **26** (24 + 2 novos) · antiga **48**. Commit citando "ciclo 072".

## Closing tail — MANDATORY, one line each, never delete

<!-- TICK ONLY WHILE WRITING THE EVIDENCE, never in advance: the box records what happened.
     Do not delete a line to say it does not apply: write `n/a: <reason>` on it.
     check-conformance.sh requires the evidence of every non-n/a step in qa-report.md. -->

- [x] **TAIL:review** — independent review in **fresh context**, by whoever did not execute
  (Theorem 2). Evidence: the verdict, in `qa-report.md`. Aqui: revisar os 25 FR contra o diff
  integrado (kanban, fila, parser FR5, gatilho FR17) e contra as anti-regras 1–8.
- [x] **TAIL:security** — security pass proportional to the risk class. Classe **média**: duas rotas
  POST novas, gatilho que passa a recusar escrita na base herdada, leitura/escrita de arquivo local
  (agora também **backup** em `painel/dados/backup/`). Evidence: the verdict, in `qa-report.md`, com as
  dívidas herdadas (D-072-3/4/5) declaradas.
- [x] **TAIL:mutation** — every gate this cycle created or changed was **broken on purpose and seen
  refusing**, quebrando a **CONDIÇÃO** (não o nome) de FR10 (normalização), FR12 (permanência na
  fila), FR9 (transição sem arquivo), FR16 (append) e FR17 (o gatilho **com `WHEN`** — inclusive
  provando que o fechamento do passo continua passando), e **colando os nomes dos testes que falham**.
  Evidence: the mutation and its output, in `qa-report.md`.
- [x] **TAIL:gate** (aberto por delegação em 2026-10-25 — `decisao-072-gates-delegados`, ADR 0026; crítico `process-guardian` em contexto fresco: APPROVE_WITH_CONDITIONS, quatro condições fechadas em `d71cee6` e reverificadas pelo Worker06; verificações de git e varredura de segredos pela sessão regente, limpas) — DoD green → guardian verdict → **human merge gate (not delegable on the
  origin; delegated this round to the regent session with an independent critic, ADR 0026)**;
  promotion via `scripts/promote-main.sh` (records `gate-main-<sha>` automatically, ADR 0009).
