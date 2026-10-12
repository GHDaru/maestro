# Spec 065 — O método se cobra sozinho e bate o ponto

> **Renumerado de 064 para 065** em 2026-10-12, ao rebasear sobre a `dev`: o número 064 já era
> o ciclo `064-capa-para-a-ia-que-instala`. O ADR 0021 e a fase F29 estavam livres e ficaram.
> O livro `docs/records/tarefas.jsonl` é só-acréscimo: os eventos deste ciclo **continuam com
> `cycle: "064"` e ids `064-*`** — `report-tasks.py --cycle 064` é a consulta que os acha.

- **Status**: Implementado; revisão independente R1 reprovou → R2 aprovou com ressalvas, tratadas; gate humano concedido em 2026-10-12 · **Raia**: plena · **Data**: 2026-10-12
- **Origem**: conversa do Darú com o Claude em 12/10/2026. Duas demandas:
  1. *"Eu desejo que o método se auto cheque, e não que eu pergunte."*
  2. *"Quero ver quanto estou gastando. Quando o gerente passa uma tarefa, a sessão que recebe
     registra um start task, e quando termina, um stop task."*

> **Raia**: plena. **Ambiguidade** média (o protocolo de etiquetas é novo); **raio** amplo — o
> instalador escreve no `.claude/settings.json` de terceiros, e o hook `Stop` passa a rodar em
> todo fim de resposta de todo projeto instalado; **irreversibilidade** baixa (remover o hook e
> o plugin desfaz tudo; o livro de ponto só acrescenta linhas).

## Glossário deste ciclo

| Termo | O que é aqui |
|---|---|
| **Hook clássico** (settings hook) | Programa que o Claude Code roda num **processo separado** quando um evento acontece. Configurado no `.claude/settings.json`. Recebe um JSON (*JavaScript Object Notation*, notação de objetos JavaScript) pela entrada padrão e responde pelo código de saída e pela saída padrão. |
| **Mod** | Plugin cujo código JavaScript/TypeScript roda **dentro** do processo do Claude Code, inscrito em eventos (`tool.call`, `session.receive`, `turn.step`…). Disponível a partir do Claude Code 2.1.287. |
| **Livro de ponto** (task ledger) | `docs/records/tarefas.jsonl`: um evento por linha, só acrescentado, nunca reescrito. |
| **Etiqueta** | A linha `[[TASK ...]]` ou `[[DONE ...]]` que o gerente e as sessões escrevem nas mensagens. É o contrato entre eles. |
| **JSON Lines (JSONL)** | Um objeto JSON por linha — o formato do `decisoes.jsonl` e do livro de ponto. |

## O quê e por quê

### 1. O método só se checava quando alguém perguntava

O corolário C13 diz que *"estou seguindo o método?"* não se responde de memória. Hoje ele é
cumprido de duas formas, e as duas têm furo:

| Mecanismo | Furo |
|---|---|
| Texto no `CLAUDE.md` ("rode `check-conformance.sh`") | Depende de o agente lembrar e obedecer. |
| Hook `SessionStart` (`session-state.sh`) | Mede **uma vez**, no início. Horas depois, quando o agente diz "terminei", nada mede nada. |

**O momento certo de cobrar é o fim da resposta** — o evento `Stop` —, porque é ali que o
trabalho seria entregue. Nesse momento o hook roda `check-conformance.sh --ticked-only NNN`, **só para o ciclo mais
novo** (o que está sendo escrito; ciclos antigos são história fechada e não se corrigem). É a
metade do portão que cobra apenas o que o próprio ciclo afirmou (ciclo 061). Se houver uma
caixa `TAIL` (a cauda de fechamento do ciclo) marcada sem evidência, o Claude Code **não deixa o
agente parar**; o motivo do bloqueio são as linhas ✗ reais do portão, sem remédio fixo.

### 2. Não existe registro de quanto custa cada tarefa

Numa arquitetura com um gerente distribuindo tarefas para várias sessões, não há como
responder: quanto custou implementar versus auditar? Quantas tentativas até aprovar? Quanto
foi gasto em retrabalho? O livro de ponto responde a isso com fatos gravados no momento em
que aconteceram, nunca reconstruídos depois.

**Por que mod e não hook clássico**: só o mod tem os eventos `session.receive` (uma mensagem
chegou de outra sessão) e `session.send` (uma mensagem vai sair), e só ele recebe os tokens
de **cada requisição ao modelo** (`turn.step`), com o modelo que respondeu e, quando for o
caso, o subagente.

## O que já existe nesta branch (protótipo testado)

| Arquivo | O que faz | Idioma (decisão de arquitetura, *Architecture Decision Record* ou ADR, 0014) |
|---|---|---|
| `scripts/hooks/stop-conformance.py` | Hook `Stop`: mede e, se vermelho, bloqueia o encerramento **uma vez**; na segunda, deixa parar e avisa o humano (`systemMessage`). Mede **só o ciclo mais novo**, usa `$CLAUDE_PROJECT_DIR` como raiz (o `cwd` do evento é só reserva) e monta o motivo com as linhas ✗ reais do portão. Falha aberta, com aviso. | inglês |
| `.claude/settings.json` | Ganha a entrada `Stop` (timeout de 120 s). | — |
| `scripts/record-task.py` | Grava um evento no livro de ponto: valida campos e vocabulário, e acrescenta com `O_APPEND`, **repetindo a escrita até sair a linha inteira** (no Linux e no macOS, sessões concorrentes não se misturam — medido com 30 linhas de ~2 KB simultâneas; **no Windows não há essa garantia**, porque lá o `O_APPEND` do Python é posicionar no fim e depois escrever; sem `flock`, que não existe no macOS nem no Git Bash do Windows). | inglês |
| `mods/maestro-ledger/` | O mod: bate o ponto de entrada no `[[TASK]]`, soma os tokens de cada requisição, bate o de saída no `[[DONE]]`, grava o veredito de auditoria e marca como interrompida a tarefa aberta quando a sessão termina. | inglês |
| `mods/maestro-ledger/hooks/ledger.test.ts` | 14 testes que rodam contra o motor real do Claude Code (`claude plugin test`). | inglês |

## Medido antes de escrever

Tudo rodado no Claude Code **2.1.296**, com a saída guardada:

| Fato | Como se sabe |
|---|---|
| Hook `Stop`: verde → silêncio; `TAIL` marcada sem `qa-report.md` → `decision: block`; segunda tentativa → deixa parar e avisa o humano; projeto sem o método → silêncio; entrada quebrada → falha aberta | os 5 casos simulados via stdin |
| **Ao vivo**: uma sessão real (`claude -p`, Haiku) disse "terminei"; o hook bloqueou; o agente investigou, achou o `qa-report.md` apagado, tentou restaurar (sem permissão), relatou; o hook deixou parar e avisou o humano. Custo do teste: US$ 0,017 | `stream-json` da sessão |
| **Defeito achado pelo primeiro teste**: o `check-conformance.sh` corta as linhas de evidência por **bytes**, partindo caracteres acentuados ao meio. Com decodificação estrita, o hook caía na falha aberta e **nunca checava nada** — em silêncio | corrigido com `errors="replace"`; o comentário no código registra |
| Mod: 14 testes passando (eram 7 no protótipo) | `claude plugin test mods/maestro-ledger` |
| Mod: **7 mutações**, todas reprovando. A M6 (um `[[DONE]]` de outra tarefa fecha a tarefa ativa) **sobreviveu** ao primeiro teste; o teste foi fortalecido até reprová-la | tabela no `qa-report.md` |
| Mod **ao vivo**: os totais gravados batem **exatamente** com o relatório do próprio Claude Code (2 requisições; 4 de entrada; 350 de saída; 71.578 de cache lido; 23.396 de cache gravado; US$ 0,005827) | `claude -p --plugin-dir mods/maestro-ledger` |
| Gravador: 50 gravações **simultâneas** de 2 KB cada → 51 linhas, 51 JSONs válidos, 51 ids distintos | teste de concorrência |
| **Defeito do instalador**: um projeto com os hooks da v0.3.0 recebe `CONFLICT` ao atualizar para os hooks novos — o instalador conflita **consigo mesmo** de novo, como no ciclo 056 | `merge-settings.py <settings da v0.3.0> <settings novo>` → `CONFLICT` |

## O protocolo das etiquetas (o contrato gerente ↔ sessões)

Cada etiqueta fica **sozinha na sua linha** (espaços nas pontas não importam; texto antes ou
depois na mesma linha a anula). Valor com espaço vai entre aspas duplas e pode conter `]`. Se a
mensagem tiver várias, conta a **primeira** `[[TASK]]` e a **última** `[[DONE]]`: a atribuição
verdadeira abre a mensagem e a entrega verdadeira a fecha, então um exemplo do protocolo citado
no meio do texto é ignorado.

```text
[[TASK id=064-T03 kind=implement attempt=2 cycle=064 redoes=064-T03#1]]
[[DONE id=064-T03 outcome=delivered]]
[[DONE id=064-A01 outcome=delivered target=064-T03 verdict=rejected reason="no mutation evidence"]]
```

| Campo | Onde | Valores |
|---|---|---|
| `id` | TASK, DONE | obrigatório; o mesmo id em todas as tentativas |
| `kind` | TASK | `spec` · `plan` · `implement` · `test` · `review` · `audit` · `fix` · `docs` · `research` |
| `attempt` | TASK | inteiro ≥ 1 (não "first/second") |
| `cycle` | TASK | o `NNN` do ciclo |
| `redoes` | TASK | a tentativa reprovada que esta refaz (`064-T03#1`) |
| `outcome` | DONE | `delivered` · `blocked` · `failed` (o mod grava sozinho `interrupted` e `superseded`) |
| `target` · `verdict` · `reason` | DONE de `audit`/`review` | `verdict`: `approved` · `approved_with_notes` · `rejected` |

**Separação deliberada**: *tentativa* (quantas vezes), *resultado* (a sessão conseguiu fazer?)
e *veredito* (o trabalho foi aceito?) são três campos diferentes. O veredito **nunca** vem de
quem executou: vem da tarefa de auditoria, que aponta para a avaliada (Princípio II — quem
executa não verifica). O mod **impõe**: só tarefas `audit` ou `review` gravam veredito. O
gravador exige `by` num `verdict`, e o relatório só conta vereditos de tarefas `audit`/`review` **cuja `session` é a do `start` dessa tarefa** (quem julgou é quem rodou a auditoria). Um `target` terminado em `-cycle` (ex.: `064-cycle`) é o **veredito do ciclo inteiro**: o relatório o mostra à parte, na seção *Cycle verdicts*, com o último veredito válido e o histórico, e não o conta na aprovação de primeira.

**Eventos gravados**: `assigned` (sessão do gerente, ao enviar) · `start` (sessão executora, ao
receber) · `stop` (ao devolver, com `requests`, `tokens_in`, `tokens_out`,
`tokens_cache_read`, `tokens_cache_write`, `tokens_subagents`, `tokens_by_model`, `cost_usd`,
`duration_s`) · `verdict` (sobre o `target`).

## Requisitos funcionais (FR, de *functional requirement*)

- **FR1 — Hook `Stop` no instalador.** O bloco *Harness* do `scripts/install-maestro.sh` DEVERÁ
  copiar `scripts/hooks/stop-conformance.py` (arquivo por arquivo, como os outros dois), e o
  `.claude/settings.json` de origem já traz a entrada. O `--no-hooks` DEVERÁ preservá-lo como
  preserva os outros dois (a lista `for kept in ...`).
- **FR2 — Atualizar não é conflito.** O `scripts/hooks/merge-settings.py` DEVERÁ ganhar o
  veredito `UPGRADE`: quando os hooks existentes forem **exatamente** os de uma versão
  anterior do Maestro (lista versionada dentro do próprio arquivo, começando pela v0.3.0), o
  instalador substitui só a chave `hooks` e mantém o resto. Hooks de terceiros continuam
  `CONFLICT`. Medido hoje: `CONFLICT`.
- **FR3 — O gravador viaja com o método.** `scripts/record-task.py` DEVERÁ ser instalado com os
  demais scripts. A regra de permissão de execução do instalador (`scripts/*.sh` e
  `scripts/hooks/*`) DEVERÁ incluir `scripts/*.py`.
- **FR4 — O mod é distribuído como plugin, não copiado.** O `.claude-plugin/marketplace.json`
  DEVERÁ ganhar uma segunda entrada, `maestro-ledger`, com `source: ./mods/maestro-ledger`. O
  instalador **NÃO DEVERÁ** instalar o plugin: `claude plugin install` grava nas configurações
  do usuário, fora do projeto-alvo. Quando o agente for o Claude Code, o resumo final DEVERÁ
  imprimir o passo exato:

  ```bash
  claude plugin install maestro-ledger --marketplace GHDaru/maestro --scope project
  ```

  e avisar que exige Claude Code 2.1.292 ou mais novo (o `--marketplace` no shell) e mods
  ativos (2.1.287 ou mais novo).
- **FR5 — O protocolo é instalável.** Um documento `docs/governance/task-ledger.md`, em inglês,
  DEVERÁ descrever as etiquetas, o vocabulário e os eventos, e o bloco instalado no
  `CLAUDE.md` DEVERÁ apontar para ele numa linha. Quem distribui tarefas é ensinado ali a
  etiquetar.
- **FR6 — O relatório responde "quanto estou gastando".** Um `scripts/report-tasks.py` DEVERÁ ler o livro de ponto e imprimir: tokens e custo por `kind`, por
  ciclo e por modelo; **taxa de aprovação de primeira** (tarefas aprovadas na tentativa 1);
  **custo do retrabalho** (tentativas ≥ 2); taxa de cache (`cache_read` ÷ entrada total);
  **órfãs** (`start` sem `stop`).
- **FR7 — Portões.** O `check-installed.sh` DEVERÁ verificar o hook `Stop` instalado e
  executável e o `record-task.py` presente. O `check-language.sh` DEVERÁ passar nos arquivos
  novos. A integração contínua (CI, de *continuous integration*) DEVERÁ rodar `claude plugin validate` e `claude plugin test`
  em `mods/maestro-ledger` quando houver Claude Code no runner; quando não houver, a ausência
  é **declarada** no `qa-report.md`, nunca silenciosa.

## Limites declarados (para ninguém confundir com cobertura total)

- **Sessões na nuvem** (`claude.ai/code`) não carregam plugins habilitados no
  `.claude/settings.json` do repositório (documentação: *Install and manage plugins*, aba
  *Cloud session*). O mod **não roda lá**. Se o hook `Stop`, que é de settings, roda lá,
  **não foi verificado** neste ciclo.
- **Sessões WSL** (*Windows Subsystem for Linux*, o Linux dentro do Windows) no Desktop não carregam plugins: o mod não roda lá.
- **Recarregar o mod** (hot reload) perde a tarefa ativa, que é uma variável do módulo. O livro
  mostra um `start` sem `stop` — uma órfã visível, nunca um `stop` inventado.
- **`session.end`** tem 1,5 s no total para todos os mods. O registro `interrupted` é melhor
  esforço; o relatório (FR6) acha as órfãs de qualquer jeito.
- **Uma tarefa ativa por sessão.** Um `[[TASK]]` de **outra sessão** nunca substitui uma tarefa
  aberta: é recusado, com registro no log (qualquer sessão da máquina pode mandar mensagem, e o
  nome do remetente é o que ela escrever). Só a pessoa substitui — no terminal, pelo Remote
  Control ou como anfitriã de um `claude -p` —, e a anterior fecha como `superseded`. A próxima
  tentativa do **mesmo** id é trabalho novo: fecha a anterior como `superseded` e abre a nova.
  Um `[[DONE]]` de outro id é ignorado, com registro.
- **A etiqueta de quem julga não é autenticada.** Com a sessão sem tarefa aberta, outra sessão pode
  abrir uma tarefa `kind=audit` e emitir veredito. O relatório só conta vereditos cuja `session` é a
  do `start` da tarefa auditora, mas isso não prova quem escreveu. E essa checagem supõe ids de
  sessão **distintos por executor**: em sessões aninhadas eles se repetem (medido neste ciclo).
- **Colar o documento do protocolo com uma tarefa aberta** troca a tarefa: um exemplo `[[TASK …]]`
  sozinho na linha (em bloco de código) vindo **da pessoa** é, para o mod, uma atribuição, e a
  pessoa pode substituir. Evite colar exemplos com tarefa aberta, ou cite o exemplo no meio da frase.
- **`--scope user` é perigoso**: o mod executa o `scripts/record-task.py` do repositório aberto.
  Instale só com `--scope project`, em repositórios em que você confia.
- **Um `specs/NNN-*` novo e vazio** faz o hook `Stop` medir o ciclo novo e silenciar uma `TAIL`
  marcada sem evidência no anterior. A CI, que roda `--ticked-only` em todos os ciclos, ainda pega.
- **`cost_usd`** em plano por assinatura é o equivalente em preço de API (*Application Programming Interface*, a interface de programação paga por uso; o mesmo número do
  `/cost`). Os **tokens** são exatos em qualquer plano e são a medida principal.
- **O hook `Stop` mede artefatos, não qualidade** — o mesmo limite do script que ele chama.
- **A troca entre sessões** (`session.receive`/`session.send`) foi testada no kit de testes do
  motor, **não ao vivo** — isso exige duas sessões na mesma máquina (roteiro abaixo).

## Roteiro de teste na máquina do Darú

1. Na branch, `claude plugin validate mods/maestro-ledger` e `claude plugin test mods/maestro-ledger` → 14 pass.

   Regra de todos os passos com etiqueta: a `[[TASK …]]` e a `[[DONE …]]` ficam **cada uma
   sozinha na sua linha**; texto na mesma linha anula a etiqueta.

2. **Auto-checagem**: num clone de teste, **marque uma caixa `TAIL`** do `tasks.md` do ciclo mais
   novo (ex.: `- [x] TAIL:review`) e **então** apague o `qa-report.md` desse ciclo. O hook só
   mede o ciclo mais novo e só cobra caixa marcada: sem caixa marcada ele fica em silêncio.
   Abra `claude`, peça "responda só: terminei". Esperado: o Claude **não para** e começa a
   investigar a evidência ausente.
3. **Ponto, sessão única**: `claude --plugin-dir mods/maestro-ledger`, envie o prompt abaixo, em
   várias linhas (a etiqueta de abertura na primeira linha e a de fechamento sozinha na última):

   ```text
   [[TASK id=T-01 kind=research attempt=1]]
   Leia o README e resuma em uma frase.
   Termine a resposta com a linha abaixo, sozinha na última linha:
   [[DONE id=T-01 outcome=delivered]]
   ```

   Esperado: duas linhas novas em `docs/records/tarefas.jsonl`, e os tokens batendo com o `/cost`.
4. **Ponto entre sessões**: abra **dois** terminais com `--plugin-dir`. No primeiro (gerente),
   peça para enviar à outra sessão, pelo `SendMessage`, uma mensagem cuja **primeira linha** seja
   `[[TASK id=T-02 kind=implement attempt=1]]`, seguida do pedido em linhas seguintes, e que mande
   o executor terminar com `[[DONE id=T-02 outcome=delivered]]` **sozinha na última linha**.
   Esperado: `assigned` no gerente, `start` no executor, e `stop` quando o executor responder.
5. **Veredito**: repita com uma tarefa `kind=audit` (a `[[TASK id=T-03 kind=audit attempt=1]]` na
   primeira linha) cujo fechamento, sozinho na última linha, seja
   `[[DONE id=T-03 outcome=delivered target=T-02 verdict=rejected reason="teste"]]`. Esperado: um
   evento `verdict` sobre `T-02`, com `by=T-03` e a `session` da própria auditora; o
   `scripts/report-tasks.py` só o conta se essa `session` for a do `start` de `T-03`.

## Critérios de aceite

- Projeto com os hooks da v0.3.0 → o instalador responde `UPGRADE` e instala o hook `Stop`;
  projeto com hooks de terceiros → continua `CONFLICT`.
- Repositório com `TAIL` marcada sem evidência → o hook `Stop` emite `decision: block` na
  primeira vez e `systemMessage` na segunda; repositório verde → nenhuma saída.
- `claude plugin test mods/maestro-ledger` → todos passam; cada uma das 7 mutações do
  `qa-report.md` → pelo menos um teste reprova.
- Uma sessão ao vivo com `[[TASK]]`…`[[DONE]]` → os totais de tokens gravados são iguais aos do
  relatório da própria sessão.
- `check-language.sh`, `check-installed.sh` e `package-plugin.sh --verify` verdes.
