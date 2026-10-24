# UX design — ciclo 066 · Painel de regência

- **Status**: proposta · **Data**: 2026-10-19 · **Agente**: `ux-semantics`
- **Insumos**: `insumo-hindiana.md`, `plano-integracao-linha-paralela.md`, painel v0
  (`painel-controle`, proposta de 01/10 — board de agentes, fluxo de peças, DORA, higiene do
  git, estado-ia). **Este documento não reescreve a v0**: nomeia os papéis das quatro telas
  novas e declara quais papéis da v0 são consumidos.
- **Consumido por**: `dev-implementer` (implementa o papel), `qa` (evidência de jornada),
  `tech-writer` (jornada viva em `docs/journeys/066-painel-de-regencia.md`).

Siglas usadas: UI (*User Interface*, interface), UX (*User Experience*, experiência de uso),
DoD (*Definition of Done*, definição de pronto), ADR (*Architecture Decision Record*),
VM (*Virtual Machine*, máquina virtual), YAML (*YAML Ain't Markup Language*, formato do
cabeçalho de veredito), A2A (*Agent-to-Agent*, protocolo de ligação entre agentes),
TAIL (cauda de fechamento do ciclo: `TAIL:review/security/mutation/gate`).

## 0. Lei de ferro deste documento

```
NENHUM NÚMERO, SELO OU CARTÃO NASCE SEM FONTE — A UI PROJETA, NÃO DECIDE
```

O painel é um **read-model**: projeção de arquivos de gate, mensagens, transcripts e eventos
append-only (princípio 1 da v0). Ele **nunca promove, nunca decide, nunca inventa**. Quem
decide é o regente; o painel só torna visível o que já existe e aponta onde falta.

## 1. Papéis consumidos (já existem — não reimplementar)

| Papel (v0 / método) | Onde vive | Uso neste ciclo |
|---|---|---|
| **Sessão com estado** (trabalhando/esperando/bloqueado/sem sinal) | board de agentes, `eventos` tipo status | reaproveitado no Mapa de sessões |
| **Selo de evidência** (hash, runner2, merge, deploy) | fluxo de peças | reaproveitado no cartão de chamado e na trilha G0→G9 |
| **Número com fonte ao lado; "—" com instrução quando falta** | DORA | regra universal de toda métrica do painel |
| **Lista de remoção para aprovação** (nada apaga sozinho) | higiene do git | modelo do papel "ação sugerida, nunca executada" |
| **Estado derivado para a IA** (`/api/estado-ia`) | estado-ia | fonte do "endereço atual" e "tarefa aberta" da sessão |
| **Decisão registrada** (id, quando, como desfazer) | tela Decisões/ADRs | evolui para o papel **Pedido de decisão** (§2.3) |

## 2. Papéis introduzidos, tela a tela (o que cada objeto É)

### 2.1 Kanban por frente — "onde está cada chamado"

| Objeto | Papel semântico | Anatomia obrigatória | Fonte |
|---|---|---|---|
| Coluna | **Gate** (G0 Reprodução … G9 Pospush): etapa do padrão "um gate, um entregável" | nome, sigla, limite de idade | `padrao-chamado.md` |
| Cartão | **Chamado em gate**: o chamado está no último gate com veredito vigente aprovado | id do chamado, frente, **dono do gate atual** (papel + sessão), veredito normalizado do gate atual, idade no gate, selo de evidência | `specs/NNN-*/G*-*.md` via `conferir_chamado.py` (veredito vigente = maior data válida) |
| Veredito normalizado | **Ruling técnico canônico** (`aprovado` ⇐ APPROVE/OK/PASSA/PASSOU · `devolvido` ⇐ RETURN/REPROVE/FALHA · `vermelho provado` ⇐ FALHA_ESPERADA · `em curso` ⇐ PENDENTE/REPRODUZIDO · `inválido` ⇐ cabeçalho reprovado) | valor canônico **e** valor original visível (nunca esconder a palavra do arquivo) | cabeçalho YAML do gate; `*-veredito.md` sem YAML entra pelo segundo parser |
| Arrasto de cartão | **Proposta de transição**: pedido de que alguém registre o próximo gate | só habilitado se existe arquivo do gate de destino com cabeçalho válido; caso contrário o cartão mostra o que falta | mesma do veredito |
| Marcador "builder ≠ crítico" | **Independência provada** (Princípio II) | autor da peça e autor do veredito; vermelho quando iguais | cabeçalho (`por`, `autor_da_peca`) |
| Marcador "integrado = criticado" | **Identidade de patch**: o que entrou na rc é o que foi criticado | patch-id do merge × patch-id do hash criticado; "—" com motivo quando não calculado | `git patch-id --stable` (hoje à mão — a UI nomeia o objeto e mostra "não conferido") |
| Filtro por frente | **Contexto delimitado** (bounded context) do trabalho | frente, pasta (`specs/NNN` ou pasta da frente) | `projetos/<nome>.json` |

### 2.2 Jornada do chamado — "o que provou e quem julgou"

| Objeto | Papel semântico | Anatomia obrigatória | Fonte |
|---|---|---|---|
| Trilha G0→G9 | **Cadeia de evidência** de um chamado (spec ↔ PR ↔ testes ↔ jornada, Princípio VI) | dez posições, cada uma: `aprovado` / `devolvido` / `vermelho provado` / `vazio` / `inválido` | arquivos `G*-*.md` |
| Posição de gate | **Veredito vigente** daquele gate | quem julgou (papel + sessão), data do veredito, data do objeto, hash julgado, arquivo de evidência (link), motivo de invalidez se houver | cabeçalho YAML |
| Gate humano (G7, G8) | **Portão do regente** — pendência do humano, não do agente | mesmo que posição, mais "aguarda desde", e link para a fila de decisões | mensagem/memória hoje; passa a exigir registro (§3) |
| Pospush (G9) | **Deploy registrado** (merge ≠ deploy, v0) | hash publicado × `src_candidata` × alembic; divergência em vermelho | `push-*.md`, `eventos` tipo deploy |
| Histórico de devoluções | **Retrabalho visível** (G3 é o gate que mais volta) | contagem de idas e voltas por gate, com links | todos os vereditos do gate, não só o vigente |

### 2.3 Fila de decisões — "o que está esperando por mim"

| Objeto | Papel semântico | Anatomia obrigatória | Fonte |
|---|---|---|---|
| Item da fila | **Pedido de decisão**: pergunta escalada ao humano com registro estruturado | id, **quem pediu** (papel + sessão), pergunta, opções (a/b, i/ii) com descrição, recomendação, **prazo**, **idade**, o que destrava (chamados/sessões presas em "aguardo o GO"), **destino da resposta** (para quem volta), status | registro de decisão (novo, §5); AskUserQuestion do transcript; `decisao-*.md` |
| Idade | **Tempo de espera do humano** — a dor de 16/10 (07:04 → tarde) e as esperas de 7 h e 24 h | horas desde o pedido, do relógio do sistema, nunca digitada | timestamp do registro |
| Portão humano pendente | **Gate do regente** (G7 aceite, G8 ordem, `TAIL:gate`) | chamado, gate, desde quando, evidência que o sustenta (link) | arquivos de gate + `tasks.md` do ciclo |
| Ruling | **Decisão registrada com volta**: a resposta, por quem, quando, e para onde foi encaminhada | texto, opção escolhida, autor humano, data, destinatário, link para o merge/ADR que a cita | registro de decisão (append) |
| Ordem da fila | **Prioridade por prazo e bloqueio** (o que estoura antes e trava mais vem primeiro) | prazo, nº de itens destravados | derivada |

### 2.4 Mapa de sessões — "quem está vivo e onde"

| Objeto | Papel semântico | Anatomia obrigatória | Fonte |
|---|---|---|---|
| Sessão | **Sessão viva com papel** (Office, Gerente, Gerente02, Assistente, Worker NN) | nome, papel, **endereço/ref atual**, projeto, worktree (cwd), tarefa aberta, última atividade (relógio), estado da v0 | transcripts (`customTitle`, `agentName`, `cwd`, `timestamp`), `sessoes.json`, `hindiana.json` |
| Alerta "sessão parada" | **Sem sinal acima do limiar** (`limiar_parado_min`) | desde quando, limiar aplicado | derivada da última atividade |
| Alerta "sessão caída" | **Papel sem sessão viva** (a Office caiu 2× em 16/10) | papel órfão, última sessão conhecida, hora da queda | ausência de transcript ativo para o papel |
| Alerta "mensagem desviada" | **Entrega a destinatário errado** (13/10, 14/10: 9–10 mensagens para outro projeto) | remetente, destinatário pretendido × real, projeto real, hora, resumo | livro de mensagens (novo, §5) — até existir: "—, livro de mensagens não configurado" |
| Nome duplicado | **Ambiguidade de endereço** ("Hindiana Office" em 3 refs) | lista de refs com o mesmo nome e qual está viva | transcripts × contatos |
| Abrir agente / ligar via A2A | **Ação de regência** — fora deste ciclo; só o objeto é nomeado | — | ciclo futuro (072 no mapa de renumeração) |

## 3. Jornada servida — o regente às 07:00, depois de uma noite de agentes

Objetivo: em **5 segundos** saber *o que me espera* e *quem morreu*; em 5 minutos, decidir.

| Passo | O que o regente faz | O que precisa estar visível | Tela |
|---|---|---|---|
| 1 | abre o painel | **contador da fila de decisões com a idade da mais velha**, nº de sessões caídas, nº de mensagens desviadas — sem rolar, sem clicar | cabeçalho de todas |
| 2 | olha a fila | itens ordenados por prazo; cada um com pergunta, opções, recomendação, o que destrava | Fila de decisões |
| 3 | responde o primeiro | escolhe opção ou escreve; o painel **registra o ruling** com autor humano e destino e mostra "encaminhado a …" | Fila → ruling |
| 4 | confere quem está vivo | sessões por papel; caída/parada/desviada em vermelho; endereço atual | Mapa de sessões |
| 5 | vê o fluxo da frente | cartões por gate; o que parou em G3 com idade; o que espera G7/G8 dele | Kanban |
| 6 | audita um chamado antes do aceite | trilha G0→G9, quem julgou, hash, evidência, builder ≠ crítico, patch-id | Jornada do chamado |
| 7 | concede G7/G8 | registra o ruling pela fila (passo 3), não pelo cartão | Fila |

Estados de cada tela (todos declarados, todos com cara própria):

- **vazio**: "nenhum chamado nesta frente" / "fila vazia — última decisão às HH:MM" (vazio é
  informação, não erro);
- **carregando**: fonte sendo reingerida; mostra a hora da última ingestão
  (`meta.ingerido_em`) — se > 1 h, o painel se declara **defasado** no cabeçalho;
- **erro de fonte**: arquivo ausente, cabeçalho inválido, parser desconhecido → "—" com o
  motivo e o caminho; nunca um valor padrão;
- **sem permissão**: ação que exige o humano (ruling, G7, G8, `TAIL:gate`) aparece a um
  agente como somente leitura, com o aviso "portão do regente".

## 4. O que a UI NUNCA faz (anti-regras, verificáveis)

1. **Não promove.** Arrastar um cartão sem arquivo de gate válido é recusado na origem; o
   cartão mostra "falta G3-*.md com cabeçalho válido".
2. **Não decide pelo humano.** A recomendação é texto do agente que pediu; o botão de
   resposta grava `autor = humano` e nunca é pré-marcado.
3. **Não inventa número.** Fonte ausente → "—" com motivo e caminho. Sem "0", sem "n/a".
4. **Não esconde pergunta.** Pergunta sem ruling fica na fila até existir ruling registrado;
   não há "dispensar", só "responder" ou "devolver a quem pediu" (também registrado).
5. **Não digita hora.** Toda idade e todo carimbo vêm do relógio do sistema ou do timestamp
   do registro; datas escritas à mão em arquivos aparecem com selo "declarada".
6. **Não unifica apagando.** O veredito original permanece ao lado do normalizado.
7. **Não escreve em arquivo do projeto, não lê `.env`, não guarda host/token** (v0 §2.6).
8. **Não marca "conferido" o que foi calculado à mão.** Patch-id sem script = "não
   conferido", não verde.

## 5. Glossário — termos a acrescentar em `docs/governance/glossary.md`

| Termo | Definição | Evitar |
|---|---|---|
| **Painel de regência** | read-model local onde um humano vê fila de decisões, sessões, chamados por gate e jornada de evidência; nunca promove nem decide | "dashboard de métricas" |
| **Pedido de decisão** | pergunta escalada ao humano com id, quem pediu, opções, recomendação, prazo, o que destrava e destino da resposta | "pendência", "aguardo o GO" |
| **Ruling** | resposta registrada do humano (ou da Office, por delegação) a um pedido de decisão, com autor, data e destinatário | decisão só em mensagem/memória |
| **Veredito normalizado** | mapeamento canônico aprovado / devolvido / vermelho provado / em curso / inválido, exibido ao lado do original | reescrever o arquivo de gate |
| **Vermelho provado** | `FALHA_ESPERADA`: o teste vermelho do G2 falhou como previsto; não é devolução | contar como reprova |
| **Portão do regente** | G7 aceite, G8 ordem e `TAIL:gate`: gates que só o humano registra | "aprovação automática" |
| **Identidade de patch** | prova por `git patch-id --stable` de que o integrado é o criticado | "merge foi conferido" sem patch-id |
| **Mensagem desviada** | mensagem entregue a sessão de outro projeto ou outro papel que o pretendido | "erro de rota" sem registro |
| **Sessão caída** | papel sem sessão viva, com última sessão conhecida | "offline" genérico |
| **Livro de mensagens** | registro append-only de destinatário pretendido × real por mensagem | — |

## 6. Acessibilidade (declarada aqui, não no fim)

- Todo controle só-ícone (arrastar, responder, abrir evidência) tem rótulo acessível com o
  verbo e o objeto ("responder pedido D-014").
- Estado nunca é só cor: `aprovado` / `devolvido` / `vermelho provado` / `vazio` / `inválido`
  têm texto ou glifo além da cor; contraste mínimo 4.5:1.
- Foco visível e ordem de tabulação pela ordem da fila (o item mais urgente primeiro).
- Idade exibida como "há 7 h 12 min" **e** como carimbo absoluto no atributo do elemento.
- Tabelas com cabeçalho semântico; cartões como lista, não como div solta.

## 7. Fitness functions do gate de UX (executáveis, sem julgamento)

| # | Verificação | Como |
|---|---|---|
| F1 | todo número/selo na tela tem `data-fonte` com comando ou caminho que o produziu | grep no HTML renderizado: elementos `.metrica` sem `data-fonte` = 0 |
| F2 | cartão em Gn exige arquivo `Gn-*.md` com cabeçalho válido | teste: fixture com G3 ausente → cartão fica em G2 e exibe "falta G3" |
| F3 | arrasto sem evidência é recusado na API | teste: `POST /transicao` sem arquivo → 422 com motivo |
| F4 | pedido de decisão sem ruling nunca sai da fila | teste: fixture com 3 pedidos, 1 ruling → fila lista 2 |
| F5 | ruling exige `autor` humano e `destino` | teste: ruling sem destino → recusado |
| F6 | normalização cobre todos os valores observados (APPROVE, OK, PASSA, PASSOU, RETURN, REPROVE, FALHA, FALHA_ESPERADA, PENDENTE, REPRODUZIDO, NÃO PASSA) e qualquer outro cai em `inválido` com o original | teste tabela-dirigida |
| F7 | idade nunca vem de campo digitado | grep: nenhum cálculo de idade lê `data:` do YAML sem o selo "declarada" |
| F8 | "—" sempre acompanhado de motivo | teste: render com fonte ausente → texto contém "—" e "motivo:" |
| F9 | nenhum elemento só-ícone sem `aria-label` | grep no HTML: `<button` sem texto e sem `aria-label` = 0 |
| F10 | ingestão defasada > 1 h é anunciada no cabeçalho | teste: `meta.ingerido_em` antigo → cabeçalho contém "defasado" |
| F11 | jornada viva: `docs/journeys/066-*.md` existe, capturas geradas por script versionado, heurística datada ≥ data da captura | `skills/living-journey` |
| F12 | ingestão nunca abre `.env` nem grava host/token | testes já existentes da v0 continuam verdes |

## 8. Fora deste ciclo (nomeado, não desenhado)

Abrir agente pela UI e ligá-lo via A2A; controle de PID (subir/derrubar sessão — risco alto,
spec própria); memória do host; livro de mensagens como fonte (aqui só consumido — quando
ausente, a tela declara "—, livro não configurado").

**Handoff**: → `dev-implementer` (papéis §2, anti-regras §4) · → `qa` (jornada §3, F1–F12).
