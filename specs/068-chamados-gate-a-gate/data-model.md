# Data model 068 — Chamados gate a gate

> Fonte: `painel/chamados.py` (`GATES`, `PASSA`, `BARRA`, `OBRIG`, linhas 17-37; `confere`,
> 112-230; `le_chamados`, 236-294; `trilha`, 347-420) e `painel/custo.py` (`ESQUEMA`, 20-25),
> lidos em `120a32c`. Padrão do 066 mantido: os **arquivos do projeto são a fonte de verdade**;
> o que o painel devolve é projeção calculada na hora (em memória, cache de 120 s) — nada do
> chamado vai para SQLite (*Structured Query Language lite*, banco em um arquivo). O único
> banco novo, `painel/dados/custo.db`, é índice reconstruível dos transcripts.
>
> Siglas: ADR (*Architecture Decision Record*, registro de decisão de arquitetura) · JSON
> (*JavaScript Object Notation*) · IA (*inteligência artificial*) · ISO 8601 (formato de data
> e hora com fuso).

## 1. Agregado `Chamado` (raiz)

Um chamado é a pasta `specs/<id>/` com `00-chamado.md`. `confere` devolve a raiz com os gates
dentro; `le_chamados` acrescenta a origem no git.

| Campo | Tipo | Origem |
|---|---|---|
| `id` | texto | nome da pasta `specs/<id>/` |
| `titulo` | texto | primeiro `# ` de `00-chamado.md` |
| `tipo`, `escopo`, `severidade`, `aberto_por`, `aberto_em`, `origem` | texto | cabeçalho de `00-chamado.md` (`tipo` decide se G0 se aplica; `escopo: correcao` baixa G1 para 1 APPROVE) |
| `autores` | lista | cabeçalho `autores:` separado por vírgula — quem **não pode** criticar em G1/G3 |
| `gates` | lista de `Gate` (§2) | sempre os 12 de `GATES`, na ordem |
| `onde` | id de gate ou `entregue` | primeiro gate cujo estado não é `ok` nem `na` |
| `estado_atual` | `ok · bad · run · falta` | estado do gate `onde` |
| `com_quem` | texto | dono (`GATES`) do gate `onde` |
| `falta` | lista de texto | o que falta no gate `onde` |
| `desde` | ISO 8601 | data mais recente entre todos os vereditos (ou abertura) |
| `desvios` | inteiro | soma de itens com erros em todos os gates |
| `pendencias` | lista de `{gate, texto}` | todo `pendente:` de gate válido (§2.3) |
| `fonte`, `commit`, `commit_em` | texto | repositório, número de commits e o mais recente (`le_chamados`) |
| `registro` | `padrão · manual` | `padrão` quando derivado dos arquivos; `manual` quando vem do JSON de chamados manuais (§5) |

## 2. Entidade `Gate` (dentro de `Chamado`)

| Campo | Tipo | Origem |
|---|---|---|
| `gate` | `abertura · G0 · GD · G1 … G9` | `GATES` (12 entradas; `PREFIXO` mapeia `abertura` → `00-chamado`) |
| `nome`, `dono` | texto | `GATES` — **`dono` de G8 é um nome próprio do Hindiana (dívida 1 do plano)** |
| `estado` | `ok · bad · run · falta · na` | §2.1 |
| `detalhe` | texto | explicação em uma linha |
| `falta` | lista de texto | o que falta para passar |
| `pendente` | lista de texto | `pendente:` dos itens válidos deste gate |
| `itens` | lista de `Veredito` (§3) | todos os arquivos `G<n>-*.md` do gate, válidos ou não |
| `desvios` | inteiro | itens com `erros` não vazio |

### 2.1 Vocabulário de estado

`ok` PASSOU · `bad` BARRADO · `run` EM CURSO · `falta` sem entregável · `na` não se aplica (G0
quando `tipo` ≠ `bug`). Por gate simples: `PASSA[gate]` → `ok`, `BARRA[gate]` → `bad`, outro
veredito → `run`. G1, G2, G3, GD e abertura têm regra própria (§2.2).

### 2.2 Regras que decidem o estado (`confere`)

| Gate | Passa quando | Barra quando |
|---|---|---|
| `abertura` | cabeçalho com `gate, tipo, aberto_por, data, origem` | — (fica `falta`) |
| `GD` | item válido com `classe`; se `classe: C`, exige `adr` **e** decisão do dono | — (`run` "classe C sem ADR ou decisão") |
| `G1` | 2 APPROVE no mesmo hash, de não autores (1 se `escopo: correcao`); exige `spec.md` | — (`run` até somar) |
| `G2` | algum `FALHA_ESPERADA` | `INVALIDO` |
| `G3` | no hash do veredito **mais recente**: `codigo` APPROVE, `criterio` APPROVE, `runner2` OK | qualquer `REPROVE`, `RETURN`, `FALHA` nesse hash; ou só itens que não contam |
| `G7` | `ACEITO`; `ADIADO` só **com** `pendente:` | `RECUSADO` |
| `G8` | `ORDEM`; com pendências abertas exige `pendencias_aceitas` (senão `run`) | `SEM_ORDEM` |
| `G0, G4, G5, G6, G9` | `PASSA[gate]` | `BARRA[gate]` |

### 2.3 Pendências

`pendente:` num item válido **não impede** o gate de passar; o texto entra em
`Chamado.pendencias` e trava o G8 até `pendencias_aceitas` (teste
`test_pendente_passa_o_gate_mas_trava_o_g8_ate_ser_aceita`).

## 3. Entidade `Veredito` (item de gate)

Um arquivo `G<n>-*.md` com cabeçalho YAML-like entre `---` (`cabecalho`).

| Campo | Origem | Regra que o usa |
|---|---|---|
| `arquivo` | nome do arquivo | ordem (`sorted`) decide `validos[-1]` nos gates simples |
| `papel` | `papel:` (`codigo · criterio · runner2` em G3) | regra (f) |
| `veredito` | `veredito:` | `PASSA`/`BARRA`/regras de G1–G3 |
| `por` | `por:` | regra (b): em G1/G3 não pode estar em `autores` |
| `data`, `data_objeto` | `data:` (`AAAA-MM-DD HH:MM [±hhmm]`, padrão `-0300`) | regra (c): não anterior ao objeto nem posterior ao commit do arquivo (+2 min) |
| `objeto`, `hash` | `objeto: <caminho> @ <hash>` (7–40 hex, sem `*` nem `` ` ``) | regra (a): hash existe no repositório (`data_hash`) |
| `numeros` | `numeros: "<suite> p/f/e, ..."` | regra (e): toda trinca com `0/0` no fim (`numeros_limpos`) |
| `pendente`, `pendencias_aceitas` | cabeçalho | §2.3 |
| `transcrito_por` | cabeçalho | informativo |
| `erros` | lista de texto calculada por `valida` + `confere` | **vazio = o veredito conta**; não vazio = listado, não muda o estado |

Campos obrigatórios (`OBRIG`): abertura `gate, tipo, aberto_por, data, origem`; GD
`gate, classe, por, data`; demais `gate, objeto, veredito, por, data`.

## 4. Vista `Trilha` (derivada de `Chamado`, `trilha`)

Não é agregado: é calculada por `id` a partir do cache de chamados, do `git log` (commits
com `Chamado: <id>` ou os `apelidos` do cabeçalho) e de `custo.db`.

| Campo | Conteúdo |
|---|---|
| `id`, `titulo`, `onde` | da raiz |
| `eventos[]` | ordenados por `quando`; cada um: `quando` (ISO 8601), `quem` (sessão), `origem` (`commit · arquivo de gate`), `atividade` (`ATIV` por prefixo do assunto, ou `<gate> <papel>`), `gate`, `hash`, `titulo`; eventos de gate trazem `veredito`, `arquivo`, `numeros`, `nao_conta` (= `erros`), `documento` (texto inteiro); `tokens` quando o índice tem a janela |
| `metricas` | `eventos`, `vereditos`, `reprovacoes`, `aprovacoes`, `rodadas_g3` (hashes distintos com veredito em G3), `nao_contam`, `horas_abertura_ate_ultimo_passo`, `tokens` (`saida, cache_lido, entrada, turnos`), `por_gate`, `por_quem`, **`nota`** (custo é estimativa por janela) |
| `apelidos_usados` | os termos buscados no `git log` |

Janela de custo: da ação anterior da **mesma sessão** neste chamado (ou 90 min antes) até o
evento; `custo.janela(db, quem, ini, fim)`.

## 5. Chamado manual (`chamados_manuais`, JSON)

Chamados anteriores ao padrão, **digitados** — a única exceção ao estado derivado, rotulada
`registro: manual`. Campos lidos de `painel/projetos/chamados-manuais-exemplo.json`: `id`,
`tipo`, `titulo`, `aberto_em`, `escopo`, `severidade`, `aberto_por`, `origem`, `estado`,
`pendente`, `nota`. Entra na lista só se o `id` não tiver pasta derivada; some quando ganha.

## 6. Índice de custo (`painel/dados/custo.db`, `custo.ESQUEMA`)

| Tabela | Chave | Campos | Função |
|---|---|---|---|
| `arquivos` | `caminho` | `offset` (bytes já lidos), `sessao`, `ultimo_id` (última mensagem vista — deduplicação do streaming) | **o offset**: a próxima corrida começa daqui |
| `sessoes` | `sessao` (nome do `.jsonl`) | `titulo` (`custom-title`), `nome` (canônico: `Worker09` → `W09`), `pasta` | junção com a trilha por `nome` |
| `uso` | `(sessao, minuto)` | `turnos`, `entrada`, `saida`, `cache_lido`, `cache_escrito` | soma por minuto (`timestamp[:16]`), acumulada com `ON CONFLICT … DO UPDATE` |

Tudo é reconstruível: apagar `custo.db` e rodar `custo.py` de novo recria o índice do zero.
**Não** guarda conteúdo de mensagem — só contagens, título e caminho.

## 7. Relações

- `Chamado 1 → 12 Gate` (sempre os 12, estado `na`/`falta` quando vazio) · `Gate 1 → n Veredito`.
- `Veredito.hash` ↔ commit do repositório (`data_hash`), nunca chave de banco.
- `Trilha.eventos[].quem` ↔ `sessoes.nome` (junção por nome canônico, sem chave estrangeira).
- `Chamado.registro = manual` não tem `gates` calculados; a tela mostra o `estado` digitado.

## 8. Invariantes que os testes provam (`painel/tests/test_chamados.py`)

| Invariante | Teste |
|---|---|
| G3 passa com `codigo` + `criterio` APPROVE + `runner2` OK no mesmo hash (f) | `test_passa_com_codigo_criterio_e_runner2_limpo_no_mesmo_hash` |
| runner2 com errors ≠ 0 não conta (e) | `test_runner2_com_errors_nao_conta` |
| autor como crítico, data anterior ao objeto e negrito no objeto não contam (a, b, c) | `test_critico_autor_veredito_antes_do_objeto_e_negrito_nao_contam` |
| REPROVE barra o G3 (f) | `test_reprove_barra` |
| `escopo: correcao` passa G1 com 1 APPROVE (g) | `test_correcao_passa_com_um_approve` |
| `pendente:` passa o gate e trava G8 até `pendencias_aceitas` (FR3) | `test_pendente_passa_o_gate_mas_trava_o_g8_ate_ser_aceita` |

Sem teste nomeado (dívida 2 do plano): data posterior ao commit do arquivo (c), hash do
veredito mais recente (d), classe C sem ADR (FR4).
