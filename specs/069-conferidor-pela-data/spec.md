# Spec 069 — Conferidor pela data (o veredito vigente é o mais novo, não o último no alfabeto)

> **Spec retroativa.** O código já existe: branch `067-painel-chamados`, trecho `2796cbf..aa0efd1`,
> 21 commits de 09/10/2026 pela equipe do projeto Hindiana. Lá o trabalho foi o **chamado 070**
> ("conferidor: ordem do veredito"), rodado com o padrão completo de gates G0–G3. Esta spec registra
> o QUÊ e o PORQUÊ que o código obedece, para que o plano, a revisão em contexto fresco e o portão
> humano tenham contra o que medir. Nada aqui foi inventado além do que o trecho faz.

- **Status**: Implementado retroativamente (Hindiana chamado 070, `aa0efd1`); ciclo 069 pela decisão do Darú (decisao-066-daru-20-10, mapa de integração) · **Raia**: plena · **Data**: 2026-10-20
- **Origem**: bug encontrado em 09/10/2026 pela Hindiana Office ao fechar o G6 do chamado 099 do
  Hindiana: havia dois vereditos de tela válidos, `G6-tela-b865c4a.md` (PASSA, mais novo) e
  `G6-tela-fb901a1.md` (FALHA, mais antigo), e o painel mostrava a **FALHA** — o conferidor tomava
  como vigente o último arquivo na ordem alfabética do nome, e o hash no nome não tem ordem
  temporal (`00-chamado.md`, `G0-reproducao.md`). Reproduzido por quem não é autor, com os dois
  conferidores lado a lado: `b1c0108` barra, `8adb545a` passa.

> **Numeração.** No Hindiana este trabalho é o chamado **070**; no Maestro é o ciclo **069**, pelo
> mapa de integração do Darú. A pasta `specs/070-conferidor-ordem-veredito/` **mantém o nome**: os
> arquivos de gate a referenciam pelo id (`objeto: specs/070-conferidor-ordem-veredito/spec.md @
> 6741315`) e são evidência imutável — renomear quebraria a referência e reescreveria história.
> A pasta do ciclo Maestro é esta, `specs/069-conferidor-pela-data/`, e aponta para aquela.

> **Raia**: plena, não leve. É uma correção, mas não "cabe numa frase": muda a regra que decide
> o estado de seis gates (GD, G4 a G9) em todo chamado de todo projeto instalado — **raio** amplo;
> a prova é um par vermelho/verde (`6741315` → `d2822ef`) e três vereditos independentes (G1,
> G3 código, G3 critério) mais dois runner2; e o ciclo é o primeiro do repositório Maestro cuja
> evidência é o próprio padrão de arquivos de gate do Hindiana, o que pede plano e `qa-report.md`
> para a conformidade medir. **Ambiguidade** baixa (R1–R4 em EARS, sem lacuna);
> **irreversibilidade** baixa (`git revert` em dois arquivos; GD classe A). Não é infra: nenhum
> ambiente, dado ou migração.

## Glossário deste ciclo

| Termo | O que é aqui |
|---|---|
| **Veredito vigente** | Nos gates de veredito único (GD, G4 a G9), o único arquivo de gate que decide o estado quando há mais de um válido. Antes: o último na ordem alfabética do nome. Agora: o de maior `data:` no cabeçalho. |
| **Ordem alfabética × ordem por data** | O nome `G6-tela-<hash>.md` ordena pelo hash, que é aleatório; a `data:` do cabeçalho ordena pelo tempo. O bug era usar a primeira como se fosse a segunda. |
| **Hash certo** | O hash em `objeto: <caminho> @ <hash>` do veredito. Ele precisa existir no repositório (regra do 068) e é o que o vigente carrega: o estado do gate é lido do veredito mais novo **sobre o seu hash**, nunca de um veredito antigo sobre outro hash. |
| **Data legível** | `data:` que casa com `RE_DATA` (`AAAA-MM-DD HH:MM ±ZZZZ`). "ontem à noite" não é legível. |
| **FALHA_ESPERADA** | Veredito do gate G2 (vermelho): o runner2 rodou o teste novo **na base, sem a correção**, e ele falhou pelo motivo certo. É a prova de que o teste veio antes do fix. |
| **runner2** | Segunda execução da suíte por quem não é autor, em clone limpo, registrada com `numeros: "<suite> passados/falhos/erros"`; só conta com 0 falhos e 0 erros. |
| **EARS** (*Easy Approach to Requirements Syntax*) | Forma "QUANDO <condição> O SISTEMA DEVERÁ <comportamento>" usada em R1–R4 do chamado e nos critérios abaixo. |
| **CLI** (*command-line interface*, linha de comando) | O conferidor do Hindiana (`scripts/maestro/conferir_chamado.py`), corrigido no mesmo chamado (`8adb545a`), fora deste repositório. |

## O quê e por quê

### 1. O estado calculado só vale se a regra que o calcula for a certa

O ciclo 068 trocou o estado digitado pelo estado derivado dos arquivos. Isso é um ganho só se as
regras forem corretas; uma regra errada vira um estado errado **com cara de verdade**, pior que
o digitado, porque ninguém desconfia. No 099 um G6 aprovado apareceu barrado. Este ciclo fecha a
regra: o tempo é dado pelo cabeçalho, não pelo nome do arquivo.

### 2. Um veredito sem data não pode decidir

Se a data é o que ordena, um veredito sem data legível não tem lugar na fila; tratá-lo como "o
mais antigo" (R3) garante que ele nunca vence um veredito datado. Hoje `valida` já o rejeita por
"falta 'data'"; a regra fica declarada e testada para não depender desse acaso.

### 3. A trilha conta a história na ordem em que aconteceu

A trilha é lida pela IA (*inteligência artificial*) e por auditoria; uma linha do tempo em ordem
de nome não é linha do tempo. R4 fixa a ordem por data.

### 4. Vermelho antes do verde, e evidência que viaja

Pela primeira vez neste repositório o par "teste falhando na base → correção que o faz passar"
está assinado por não autores, arquivo a arquivo. A pasta do chamado entra como evidência, não
como documentação.

## Requisitos funcionais (FR, de *functional requirement*)

- **FR1 — Vigente = maior data do cabeçalho, sobre o hash certo.** QUANDO um gate de veredito
  único tiver mais de um veredito válido, `painel/chamados.py` DEVERÁ tomar como vigente o de
  maior `data:`; em empate de data, o de commit de arquivo mais recente; persistindo, o de nome
  maior. O estado do gate sai desse veredito e do hash que ele cita.
- **FR2 — Sem data legível nunca vence.** QUANDO um veredito não tiver `data:` legível, o
  conferidor DEVERÁ tratá-lo como o mais antigo (menor que qualquer data real).
- **FR3 — Trilha em ordem de data.** `trilha()` DEVERÁ devolver os eventos (commits e vereditos)
  ordenados por `quando`, não por nome de arquivo.
- **FR4 — Teste vermelho antes da correção.** O teste que prova FR1 DEVERÁ existir num commit
  anterior ao da correção e falhar na base (`6741315` falha sobre `2796cbf`; `d2822ef` passa),
  com o vermelho registrado por não autor (`G2-vermelho-W13-6741315.md`, `FALHA_ESPERADA`).
- **FR5 — A pasta do chamado viaja como evidência imutável.** `specs/070-conferidor-ordem-veredito/`
  DEVERÁ entrar no Maestro com seus dez arquivos (abertura, spec, G0, GD, G1, G2, G3 código,
  G3 critério, dois G3 runner2) sem edição; o `qa-report.md` do 069 os cita, não os reescreve.

## Fora de escopo

- G1 e G3 (vários vereditos por papel e por hash): já ordenavam por data dentro do hash (068).
- O conferidor CLI do Hindiana (`8adb545a`): corrigido lá, no repositório dele; aqui só se cita.
- Sincronizar automaticamente as duas cópias da regra — dívida declarada no 068, mantida.
- Mudar o critério de PASSA/BARRA de qualquer gate: só a **escolha** do vigente muda.
- Adotar o padrão de arquivos de gate como padrão do Maestro — é a ambiguidade da última seção.

## Artefatos condicionais que o plano DEVERÁ declarar (`docs/governance/artifacts.md`)

| Artefato | Declaração | Motivo em uma linha |
|---|---|---|
| `data-model.md` | `ART:data-model=no` | Nenhuma entidade nova: Chamado, Gate e Veredito são os do 068; muda uma regra de seleção. |
| `contracts/` | `ART:contracts=no` | Nenhuma rota nova nem campo novo na resposta; `/api/chamados` e `/trilha` devolvem o mesmo esquema, com outro conteúdo. |
| `ux-design.md` | `ART:ux-design=no` | A ordem da trilha é comportamento de um objeto que já existe (desenho do 068), não objeto novo nem tela nova. |
| `research.md` | `ART:research=no` | Nenhuma incógnita: o defeito foi reproduzido e a regra está em EARS. |
| `checklist.md` | `ART:checklist=no` | A DoD (*Definition of Done*, definição de pronto) abaixo cobre o que há para checar. |

## Para o plano — modelo de domínio (obrigatório desde o 067)

Esta spec não carrega os tokens `DOM:*`; o plano os declara. O que o plano DEVERÁ decidir:

1. **Agregado**: `Chamado`, inalterado desde o 068 (`DOM:aggregate` sem mudança).
2. **Invariantes no domínio**: a regra de ordem é a função pura `ordem_veredito(item, commit_de)`
   (`painel/chamados.py:115-118`), que devolve a tupla `(data do cabeçalho ou MINIMO, commit do
   arquivo ou MINIMO, nome)`; `confere` a aplica em `validos = sorted(...)` (`:151`). Nada na
   borda (HTTP, SQLite).
3. **Glossário**: `changed` — entra **veredito vigente** com a definição por data.
4. **Portas**: `none` — nenhuma porta nova; `commit_de` já era parâmetro de `confere`.

## Critérios de aceite

- `python -m unittest discover -s painel/tests -p test_chamados.py` → `Ran 10 tests`, `OK`,
  exit 0 (6 do 068 + 4 deste ciclo; o runner2 mediu 22 com `test_painel.py` junto).
- Os quatro testes novos, na classe `TestOrdemDoVeredito` (`painel/tests/test_chamados.py:88`):
  `test_mais_novo_vence_mesmo_vindo_antes_no_alfabeto` (FR1, `:99`),
  `test_empate_de_data_desempata_pelo_commit_do_arquivo` (FR1 desempate, `:104`),
  `test_r4_trilha_em_ordem_de_data_nao_de_nome` (FR3, `:110`),
  `test_r3_veredito_sem_data_legivel_nao_vence` (FR2, `:128`).
- WHEN `G6-tela-b865c4a.md` é PASSA às 21:00 e `G6-tela-fb901a1.md` é FALHA às 20:40 THE SYSTEM
  SHALL dar ao G6 o estado `ok`; na base `2796cbf` o mesmo cenário dá `bad`.
- WHEN dois vereditos válidos têm a mesma `data:` THE SYSTEM SHALL escolher o de commit de arquivo
  mais recente (`commit_de`).
- WHEN um veredito tem `data: ontem à noite` THE SYSTEM SHALL não o tomar como vigente.
- WHEN a trilha tem dois vereditos de G6 THE SYSTEM SHALL listá-los por data
  (`["G6-tela-fb901a1.md", "G6-tela-b865c4a.md"]`), não por nome.
- A regra do conferidor, por linha de `painel/chamados.py`: `MINIMO` (`:112`), `ordem_veredito`
  (`:115-118`), `validos = sorted(..., key=lambda i: ordem_veredito(i, commit_de))` (`:151`),
  `v = validos[-1]["veredito"]` nos gates de veredito único (`:219`), `eventos.sort(key=lambda e:
  _utc(e["quando"]) ...)` na trilha (`:393`). `grep -c 'ordem_veredito' painel/chamados.py` → `2`.
- `ls specs/070-conferidor-ordem-veredito/` → exatamente estes 10 arquivos: `00-chamado.md`,
  `spec.md`, `G0-reproducao.md`, `GD-risco.md`, `G1-W11.md`, `G2-vermelho-W13-6741315.md`,
  `G3-codigo-W10.md`, `G3-criterio-W01-d2822ef.md`, `G3-runner2-W13-d2822ef-8adb545a.md`,
  `G3-runner2-W13-98a62a1.md`.
- `grep -c 'veredito: FALHA_ESPERADA' specs/070-conferidor-ordem-veredito/G2-*.md` → `1`.
- `grep -c 'veredito: APPROVE' specs/070-conferidor-ordem-veredito/G3-*.md` → `≥ 2` (medido: 2,
  código W10 e critério W01; os runner2 trazem `veredito: OK`).
- `grep -c 'escopo: correcao' specs/070-conferidor-ordem-veredito/00-chamado.md` → `1` e
  `grep -c 'classe: A' specs/070-conferidor-ordem-veredito/GD-risco.md` → `1`.
- Par vermelho/verde: `git log --format=%h -1 6741315` existe e é ancestral de `d2822ef`
  (`git merge-base --is-ancestor 6741315 d2822ef` → exit 0).
- `scripts/check-language.sh` → verde; `scripts/check-conformance.sh 069` → verde após plano,
  tasks e `qa-report.md`.

## Limites declarados

- **Desempate por nome (R2, terceiro elemento)** não tem teste próprio; coberto indiretamente pelo
  teste de empate. O G3 critério registra isso; o plano decide se paga aqui ou declara.
- **FR2 já era atendido na base** por `valida` rejeitar data ilegível; o teste `6ea2347` fixa a
  regra em `ordem_veredito` para não depender de `valida`. Não é vermelho/verde — é cinto e
  suspensório, declarado.
- **FR3 já era atendido na base** (`eventos.sort` existia em `2796cbf`); o teste `98a62a1` é
  mutante verificado (sem o sort, falha), não correção.
- **Fato de método, registrado no GD**: a GD veio depois do G3 — a Office pediu a correção antes
  de abrir a GD e assume a falha. Fica como achado de retro, não se apaga.
- **`G3-criterio-W01-d2822ef.md`** tem `objeto: ... @ 98a62a1` no cabeçalho e `d2822ef` no nome;
  o corpo explica (98a62a1 só acrescenta testes). Arquivo imutável; declarado, não corrigido.

## Ambiguidades para o Darú

1. **O Maestro adota o padrão de arquivos de gate do Hindiana (G0–G9, um arquivo por gate, com
   cabeçalho conferível) como padrão seu?** Este ciclo é a prova de que ele funciona dentro do
   repositório Maestro: cada veredito é um arquivo assinado por não autor, o vermelho é um arquivo,
   o runner2 é um arquivo, e `painel/chamados.py` deriva o estado deles. Hoje o Maestro exige
   `tasks.md` com a cauda `TAIL:*` e `qa-report.md` com a evidência; o padrão Hindiana cobre o mesmo
   com forcing function mais forte (Princípio VI), mas são dois formatos para uma função. Opções
   que a spec não escolhe: (a) adotar, com ADR (*Architecture Decision Record*, registro de decisão
   de arquitetura) e piso de ciclo; (b) aceitar os dois, com `qa-report.md` apontando para os
   arquivos de gate; (c) manter só o formato atual e tratar a pasta 070 como exceção importada.
   → [decisão do Darú]

<!--
  GATE (DoR — não delegável): esta spec só vira plano depois da aprovação do Darú.
  Handoff: spec-agent → (aprovação) → plan-architect.
-->
