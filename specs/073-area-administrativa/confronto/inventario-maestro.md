# Inventário do Maestro — as 26 funcionalidades, com o que já existe hoje (ciclo 073, rodada 2, passo 1)

> A coluna **"estado no Maestro"** do confronto. Para cada uma das **26 funcionalidades** da
> tabela fixa (a mesma da matriz `pesquisa/plataformas.md`), diz o que o método **já faz e onde** —
> `arquivo:linha`, script, comando ou documento. Evidência concreta, não impressão: linha sem
> evidência **não** vira `tem`.

- **Data**: 2026-10-25 · **Ciclo**: 073 (área administrativa) · **Rodada**: 2 (confronto) · **Passo**: 1 (inventário)
- **Autor**: Worker05 · **Objeto**: o próprio repositório `GHDaru/maestro` (read-only)
- **Como foi feito**: busca dirigida em `docs/governance/`, `docs/adr/`, `docs/records/`,
  `docs/agents/`, `docs/handbook/`, `docs/diagramas/`, `scripts/` (+ `scripts/hooks/`),
  `.claude/agents/`, `.claude/commands/`, `skills/`, `painel/`, `.github/`, `mods/`. Cinco varreduras
  por área; toda afirmação `tem`/`parcial` abaixo traz o caminho e a linha.
- **Revisado**: 2026-10-26 (rodada 4, correção 1 — achados P2 dos juízes 1 e 3): `SendMessage`/
  `ListAgents` como mecanismos de primeira classe, o fallback por arquivo commitado e a cópia do
  DONE, o ciclo de vida do ref, «allow/ask são executáveis no harness», o livro de ponto parado no
  064 e os `arquivo:linha` revalidados. Os vereditos **não mudaram** (tem 8 · parcial 16 · não tem 2).
- **Revalidado**: 2026-10-26 (rodada 4, correção 2 — decisão 8): as citações a `claude-code.md`
  foram conferidas contra o HEAD, que andou com a correção da matriz (`:47→:61`, `:49→:63`,
  `:65→:79`, `:68→:82`, `:71→:84`); a regra «citação de ficha é revalidada no mesmo commit que muda
  a ficha» fica no README do protótipo. O *mailbox* JSON por agente e o `crossSessionInbound` do
  harness entram como parte do transporte real (linha *mensagem entre agentes*, abaixo).

## Legenda — e a força do veredito

Mesma notação normalizada da matriz (`pesquisa/plataformas.md` §Legenda), aplicada ao repositório:

| Símbolo | Significa |
|---|---|
| **tem** | existe um mecanismo **usável hoje**; a evidência está ao lado |
| **parcial** | existe **incompleto**: só declarado (contrário ao executável), só como read-model do painel, só uma forma mais estreita, ou objeto nomeado e não construído |
| **não tem** | busca dirigida sem fonte — com a força declarada entre parênteses: **(afirmado)** quando um documento afirma a ausência/fora de escopo; **(não encontrado)** quando nenhum documento afirma nada e a busca não achou mecanismo |

> A matriz marca `não` só quando **a fonte afirma** a ausência, e `—` quando **não há fonte**. Aqui
> a "fonte" é o repositório: em `não tem (afirmado)` a ausência está documentada; em
> `não tem (não encontrado)` a ausência é conclusão da varredura, de força menor — quem ler o
> confronto deve tratá-la como piso, não como prova.

## Totais

**tem 8 · parcial 16 · não tem 2** (de 26). O método cobre a maior parte da tabela, mas quase sempre
**em parte**: dois terços das funcionalidades estão em `parcial`, e o que falta por inteiro é o
**ciclo de vida** (CONTROLE: pausar, retomar).

---

## CONTROLE (6 funcionalidades) — `tem 1 · parcial 3 · não tem 2`

| Funcionalidade | Estado | Evidência no Maestro (arquivo:linha) | Nota |
|---|---|---|---|
| subir/derrubar sessão ou agente | **parcial** | `scripts/multi-session.py:140` (`wt … new-tab`), `:33` (`NAMES = ["Gerente", "Worker01"…]`), `:46` (um *worktree* por worker) | só **subir**; **derrubar** não existe — declarado fora de escopo em `specs/072-painel-de-regencia/spec.md:229` ("Controle de PID — subir/derrubar sessão") |
| pausar | **não tem (não encontrado)** | — | nenhum mecanismo; só a linha de pesquisa em `specs/073-area-administrativa/spec.md:48` |
| retomar | **não tem (não encontrado)** | — | sem retomada de sessão no método; o lançador tem `--resume` (`scripts/multi-session.py:19`), que **reabre janelas**, não o estado do trabalho. **Na plataforma, retomar existe**: `claude attach <id\|name>` e "Resume via `SendMessage` with agent ID/name" — `specs/073-area-administrativa/pesquisa/claude-code.md:61`; `companion/README.md:52` só tem `/historico?sessao=` (chat), fora do método |
| limites de orçamento e de taxa | **parcial** | orçamento: `docs/governance/operating-model.md:118-120` ("fixed time and variable scope"); orçamento de **contexto** por agente `docs/agents/perfis.md:10`; teto de consumo registrado `docs/records/decisoes.jsonl:172` ("Teto de consumo da sessao regente: 40 % do semanal") | **taxa** (*rate limit*) não existe em lugar nenhum |
| políticas allow/deny/ask | **parcial** | declarado: `docs/governance/principles.md:37` ("Declarative policy `allow / deny / ask`"); allowlist/deny registrados `docs/records/decisoes.jsonl:155`; **deny executável**: `scripts/hooks/guard-immutables.py:149` (`"permissionDecision": "deny"`); **allow/ask são executáveis no harness**: blocos `permissions.allow` / `ask` / `deny`, `permissions.defaultMode` e `permissionMode` por agente — `specs/073-area-administrativa/pesquisa/claude-code.md:63` | **corrigido na rodada 4**: o mecanismo **existe** (o harness do Claude Code executa `allow`/`ask`/`deny`); o que falta é a **política escrita neste repositório** — o `.claude/settings.json` versionado não tem bloco `permissions`, logo nenhuma regra `allow`/`ask` *nossa* roda hoje. A leitura anterior («allow/ask não são executáveis») olhava só o `settings.json` versionado e errava o alvo (juiz 1, P2) |
| aprovação humana | **tem** | `docs/governance/operating-model.md:200` ("Non-negotiable human gates, always…"), tabela por classe de risco `:186-198`; confirmação no terminal `scripts/promote-main.sh:55`; delegação `docs/adr/0026-gate-humano-por-delegacao-de-politica.md`; fila recusa ruling sem autor humano `painel/regencia/fila.py:60` | — |

---

## ADMINISTRAÇÃO (6 funcionalidades) — `tem 3 · parcial 3 · não tem 0`

| Funcionalidade | Estado | Evidência no Maestro (arquivo:linha) | Nota |
|---|---|---|---|
| cadastro de agentes | **tem** | `docs/agents/README.md:14-40` (índice perfil ↔ executável; "**13 agentes executáveis**": `:40`); 13 arquivos em `.claude/agents/`; invariantes `scripts/check-agents.sh:8,35` e `scripts/check-roles.sh:14-23` | é **registro** verificável, não processo vivo (o mesmo perfil do mercado: "quase nunca processo vivo") |
| papéis e permissões RBAC | **parcial** | papéis/RACI `docs/governance/operating-model.md:67-93`; **RBAC** (*Role-Based Access Control*) é termo de glossário `docs/governance/glossary.md:13`; permissões = allowlist de `tools` por agente + invariante read-only `docs/agents/README.md:26-27`, checado em `scripts/check-agents.sh:31-40` | sem **motor** RBAC; a autorização vive **fora** do modelo (`.claude/agents/security.md:13`) — declarado, não construído |
| cadastro de skills/ferramentas/modelos | **parcial** | skills como pastas `skills/<nome>/SKILL.md` (6), catálogo gerado `scripts/install-maestro.sh:99-104`, coerência `scripts/check-install.sh:126-135`; ferramentas por agente (coluna *Tools*) checadas `scripts/check-roles.sh:126-134` | sem registro de **modelos**: o modelo é escolhido por sessão `scripts/multi-session.py:91-92` |
| chaves e segredos | **parcial** | política: token **fora** do repositório, em escopo de usuário `docs/records/decisoes.jsonl:155`, `scripts/multi-session.py:12-13`; segredo lido por sessão e só rotacionado `:159`; classe de risco `docs/governance/operating-model.md:193`; o agente `security` varre segredos | sem **cofre** de chaves nem gate de varredura — só o lembrete em prosa `.claude/commands/dod.md:13` |
| configuração por projeto | **tem** | instalador grava `.maestro/install-options.json` e `manifest.tsv` `scripts/install-maestro.sh:492-526,177-184`; merge de settings por alvo `scripts/hooks/merge-settings.py:5-13`; painel: `painel/projetos/exemplo.json`; fronteira `boundary.json` (ADR 0018) | — |
| auditoria | **tem** | índice append-only `scripts/record-decision.sh:46-50` + imutabilidade `scripts/hooks/guard-immutables.py:44-49`; conferência `scripts/check-adr.sh`; trilha por chamado `painel/chamados.py:357`, rota `painel/server.py:787`; auditoria do método `painel/auditoria_metodo.py:41` | — |

---

## GERENCIAMENTO (8 funcionalidades) — `tem 3 · parcial 5 · não tem 0`

| Funcionalidade | Estado | Evidência no Maestro (arquivo:linha) | Nota |
|---|---|---|---|
| lista de agentes vivos com estado | **parcial** | painel: `painel/server.py:60` (`v_board`), rota `/api/board` `server.py:711`, estados `server.py:27` (`ESTADOS_SESSAO = ("trabalhando", "esperando", "sem tarefa", "bloqueado")`), UI `painel/index.html:273` | é **read-model do painel**, alimentado por *heartbeat* de status (`painel/ingest.py:156`), não por detecção de processo; "mapa de sessões" (§2.4) segue fora de escopo `specs/072-painel-de-regencia/spec.md:226` |
| tarefa aberta | **parcial** | livro de ponto: "**One active task per session**" `docs/governance/task-ledger.md:185`; `start` sem `stop` = órfã `scripts/report-tasks.py:221`; kanban por portão `painel/server.py:369` (`v_kanban`), rota `server.py:793` | não há objeto "tarefa aberta" **por agente**; o cartão visível é o do portão/chamado — o campo do mapa de sessões não foi construído. **O livro de ponto parou no ciclo 064** (`docs/records/tarefas.jsonl`, últimas linhas `064-F7`/`064-F6`): do 065 em diante, o vínculo sessão ↔ tarefa só sai do transcrito e é **piso** |
| última atividade | **tem** | `painel/server.py:77` (`"idade_min": idade`), histórico de status `server.py:82`; UI `index.html:311`; por fase `server.py:504`; livro de ponto com `ts` `docs/governance/task-ledger.md:110` | — |
| consumo por agente/sessão/modelo | **parcial** | por **sessão**: `painel/custo.py:1-8` ("Custo por sessão… grava só em dados/custo.db"), `:52` (`indexa`), `:124` (`janela`); por **modelo**: `docs/governance/task-ledger.md:118,127` (`tokens_by_model`), relatório `scripts/report-tasks.py:9` | **por agente** não há. A quebra por modelo sai do livro de ponto, **parado no 064** — do 065 em diante a única fonte é o *usage* do transcrito (`message.usage`), que é **piso** |
| custo | **tem** | `docs/governance/task-ledger.md:129` ("`cost_usd` — spend between `start` and `stop`, in US dollars"); relatório `scripts/report-tasks.py:2` ("how much am I spending?"), `:254-261` | o painel (`painel/custo.py`) mostra só **tokens**, não dólar; e o `cost_usd` do livro de ponto **para no ciclo 064** (`docs/records/tarefas.jsonl`) — o `tem` vale para o mecanismo, não para um número vivo de hoje (juiz 2, P2) |
| filas e workers | **tem** | fila de decisões: rotas `painel/server.py:791,823`, domínio `painel/regencia/fila.py:95` (`ordena_fila`), registro `painel/fila_registro.py:90`; *outbox* SQLite `painel/fila_outbox.py:109` (`FilaOutbox`); workers = sessões `scripts/multi-session.py:33` | — |
| rastro/replay de sessão | **parcial** | trilha: `painel/chamados.py:357` ("cada passo com documento, quem, quando, hash e tokens"); histórico `painel/server.py:82`; livro de ponto `docs/governance/task-ledger.md:114-119` | **replay** não existe |
| alertas | **parcial** | dívida de achados `scripts/check-retro.sh:61-66`; alerta no início de sessão `scripts/hooks/session-state.sh:52-59`; escalada `scripts/hooks/stop-conformance.py:106-110`; aviso de CI `.github/workflows/ci.yml:139`; painel "parado" `painel/server.py:78`, leitura velha `painel/regencia/normalizacao.py:84` | sem **subsistema** de alerta/notificação; são gates que falham e avisos inline |

---

## INTERCOMUNICAÇÃO (6 funcionalidades) — `tem 1 · parcial 5 · não tem 0`

| Funcionalidade | Estado | Evidência no Maestro (arquivo:linha) | Nota |
|---|---|---|---|
| mensagem entre agentes | **tem** | **harness (o transporte real)**: `SendMessage` (por ID/nome) e `ListAgents` — `specs/073-area-administrativa/pesquisa/claude-code.md:79,82,88`; o harness **documenta o transporte**: *mailbox* JSON por agente (*agent teams*) e *inbox socket* por sessão (*cross-session messaging*, com `crossSessionInbound`) — `specs/073-area-administrativa/pesquisa/claude-code.md:40-53`; **regra de endereçamento e cópia do DONE**: «endereçar sempre com o ref do ListAgents; cópia de cada DONE para MAESTRO» `specs/066-painel-de-regencia/andamento.md:112-113`; **fallback por arquivo commitado** (se o envio falhar duas vezes) `specs/066-painel-de-regencia/andamento.md:139-140`; eventos de motor `mods/maestro-ledger/hooks/register.ts:140,172` (`session.receive` / `session.send`); *outbox* entre sessões `painel/fila_outbox.py:121,140`; protocolo `[[TASK]]`/`[[DONE]]` `docs/governance/task-ledger.md:28-31` | o mecanismo é **de primeira classe no harness** (`SendMessage`/`ListAgents`), não efeito colateral do ledger; o método **prefere artefato a chat** `docs/agents/comunicacao.md:6` ("agentes comunicam por **artefatos**, não por chat") — e, quando o envio falha, a mensagem **vira artefato commitado** |
| protocolos (A2A, MCP) | **parcial** | **MCP** (*Model Context Protocol*) implementado: `painel/mcp_painel.py:2` (servidor MCP, stdio, JSON-RPC 2.0) com 3 ferramentas (`estado_atual`, `registrar_status`, `registrar_peca`); termo no glossário `docs/governance/glossary.md:34` | **A2A** (*Agent-to-Agent*) só **nomeado**, nunca construído `specs/066-painel-de-regencia/ux-design.md:81` |
| caixa de entrada | **parcial** | comportamento de inbox no *drain* do outbox `painel/fila_outbox.py:140`; hooks leem e marcam lidas `painel/hooks/workflow_session_start.py:158-162`; a tela "Fila" é caixa de entrada de **decisões** `painel/index.html:845` | nenhuma feição/rota **nomeada** "caixa de entrada" — **não encontrado na documentação lida** nas 25 plataformas (nenhuma fonte, e um `—` não é um `não`: `pesquisa/plataformas.md`) |
| roteamento por nome/ref | **parcial** | destinatário por **nome livre**: `painel/server.py:479` (`contatos()`), `painel/fila_outbox.py:151` (`sessao_destino`); canonização `painel/ingest.py:199` (`norm_sessao`); **por ref**: `ListAgents` é do harness `specs/073-area-administrativa/pesquisa/claude-code.md:82`; **ciclo de vida do ref** — o ref **muda a cada reinício** e o antigo deixa de resolver: `specs/066-painel-de-regencia/insumo-hindiana.md:16` (casos de 13/10 e de 16/10) | sem tabela de resolução de nome no repositório; o roteamento por *ref* **existe no harness** (`ListAgents`), não no método; houve incidente real de nomes cruzados `specs/066-painel-de-regencia/qa-report.md:35`. `arquivo:linha` **revalidado na rodada 4**: era `:469`, é `painel/server.py:479` (juiz 3, P2) |
| livro de mensagens | **parcial** | há **registros append-only**: eventos `painel/ingest.py:66,78`; registro da fila `painel/fila_registro.py:76` (abre em `"a"`); livro de ponto `docs/records/tarefas.jsonl` | nenhum "livro de mensagens" **unificado/configurável**; a tela declara a ausência `specs/072-painel-de-regencia/spec.md:230` ("—, livro não configurado") |
| colisão de nomes | **parcial** | incidente registrado e regra adotada (endereçar por *ref*) `specs/066-painel-de-regencia/qa-report.md:35`; guarda de colisão de **ids de pedido** na fila `painel/regencia/fila.py:52-56` (recém-nascida, ciclo 072), rota `painel/server.py:625` | sem controle de colisão de **nomes** de sessão/agente/skill; débito declarado (prefixar no lançador). **Colisão de endereço ≠ colisão de termo**: o nome nu que já foi válido vira **endereço obsoleto** depois do reinício (`specs/066-painel-de-regencia/insumo-hindiana.md:16` — "Hindiana Office" em 3 refs, 2 offline) e a regra é **recusar**, nunca resolver (decisão 3 da regente) |

---

## Leitura — o que o confronto deve olhar (a cruz do W03 com a matriz)

1. **O Maestro é forte exatamente onde a documentação lida não mostra nada.** O grupo
   INTERCOMUNICAÇÃO é o mais fraco da matriz (**14 %**; caixa de entrada e livro de mensagens
   **não encontrados na documentação lida**). Aqui, ele é
   **5 parciais + 1 tem**: o método já opera à mão (artefato, *outbox*, `[[TASK]]`/`[[DONE]]`,
   mensagem por nome e por *ref*) o que nenhuma das 25 plataformas entrega pronto na documentação
   lida. É a convergência que o achado do W05 previu — **ausência de documento, não de pesquisa**.
2. **O buraco é o ciclo de vida.** CONTROLE tem só **1 `tem`** de 6: **pausar e retomar não existem**
   no método, e subir/derrubar é meio. Isso espelha a matriz (CONTROLE **20 %**).
   Antes de comprar ciclo de vida de fora, note que **retomar existe na plataforma** (o harness
   reabre a sessão por `claude attach` / `--resume` — `specs/073-area-administrativa/pesquisa/claude-code.md:61`)
   e que **pausar também não foi encontrado na documentação lida** — ausência de fonte, não prova de
   que ninguém tem.
3. **Onde o mercado é maduro (ADMINISTRAÇÃO, 51 %), o Maestro é `parcial`.** RBAC, cadastro de
   skills/modelos e segredos existem como **declaração + verificação**, sem motor. É a maior
   distância entre "o que o mercado vende" e "o que o método tem executável" — e é onde a rodada 2
   mais precisa decidir *comprar, copiar ou continuar à mão*.
4. **GERENCIAMENTO é read-model, não processo.** O que aparece (agentes vivos, tarefa, última
   atividade, custo por sessão) vive no `painel/` — e o painel se declara explicitamente *"read-model
   local … nunca promove e nunca decide"* (`docs/governance/glossary.md:79`). O que **não** existe em
   lado nenhum é *consumo por agente* — igual à matriz (3 `sim` em 25).

## Limites da varredura (declarados)

- **O livro de ponto parou no ciclo 064.** `docs/records/tarefas.jsonl` termina em `064-F7`/`064-F6`
  (12/10/2026): as funcionalidades que se apoiam nele — *tarefa aberta*, *consumo por
  agente/sessão/modelo* e *custo* — valem **até o 064**; do 065 em diante o número só sai do
  transcrito da sessão (`message.usage`) e é **piso, não total**. Declarado aqui porque duas linhas
  com veredito (`tem`/`parcial`) se apoiam nessa fonte (juiz 2, P2).
- **O ponto de execução do controle não está desenhado.** Um hook do harness barra o **uso de
  ferramenta** (`scripts/hooks/guard-immutables.py:149`), mas não o **gasto de modelo**; o bloco
  `permissions` (`allow`/`ask`/`deny`) é o ponto declarado, e o repositório não tem política escrita
  nele. «Recusar a chamada seguinte» e «suspender a sessão» saem de ENTRA e viram DEPOIS com gatilho.
  Declarado aqui na mesma rodada em que a tela o desenha (juiz 1, P4; decisão 2 da regente).
- **O caminho de aprovação do derrubar não está desenhado como execução.** A tela `workflow-01`
  desenha o **pedido de decisão à Regência** (relação 5 do mapa) e o **Ruling** do humano; **quem
  roda o comando** de derrubar no harness — o ponto de execução — segue dívida declarada.
- **A área é somente leitura nesta rodada.** O ciclo 073 é pesquisa e desenho: nada nesta área
  executa ação — os controles das telas abrem confirmação ou pedido de decisão, nunca executam.
  Declarado nas seções «Limites» e repetido no rodapé das telas (juiz 2, P4).
- **Varredura dirigida**, não exaustiva: não li o livro capítulo a capítulo, nem `.specify/`,
  `companion/` (citado de passagem) ou `publicar/`. Os caminhos varridos estão no cabeçalho.
- **`não tem (não encontrado)` é piso, não prova** — vale a força menor que a matriz reserva a `—`.
  Só `pausar` e `retomar` caem nessa classe; as demais linhas têm evidência.
- **Segredos**: respeitado o limite do despacho — **não** abri `.env` nem `settings.local.json`; li
  apenas o `.claude/settings.json` versionado (que não tem bloco `permissions` nem segredo).
- **Sem software novo**: este inventário é documento; nada foi construído nem rodado (o ciclo 073 é
  de pesquisa).
- **Siglas expandidas na primeira ocorrência** (Princípio VIII): RBAC (*Role-Based Access Control*),
  RACI (*Responsible, Accountable, Consulted, Informed*), A2A (*Agent-to-Agent*), MCP (*Model
  Context Protocol*), LLM (*Large Language Model*), ADR (*Architecture Decision Record*), DoD
  (*Definition of Done*), UI (*User Interface*), CI (*Continuous Integration*), PID (*Process
  Identifier*).
