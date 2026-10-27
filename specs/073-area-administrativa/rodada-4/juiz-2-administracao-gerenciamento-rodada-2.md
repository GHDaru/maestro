# Rodada 4 — Juiz 2: ADMINISTRAÇÃO E GERENCIAMENTO DE AGENTES — segunda rodada (contexto fresco, 26/10/2026, sobre HEAD faca232)

**Veredito: barra NÃO atingida.** Cinco das 16 peças chegam a 9 (P2, P5, P9, P11, P13). As outras 11 ficam em 8.

A cobertura está completa:
- Os 15 ENTRA têm tela. A auditoria administrativa é só uma casca: uma linha de exemplo e uma linha "—" nas três telas da Administração.
- As 25 plataformas têm ficha em `pesquisa/`.
- O OpenRouter saiu de `workflow-04`. Hoje a fonte cita LiteLLM e Langfuse (`workflow-04-consumo-por-agente.html:59-62`).

A segunda rodada fechou a maior parte das lacunas que nomeei na primeira. Nenhuma peça caiu. Quase nenhuma repete a mesma lacuna, e é isso que o diagnóstico final registra. O que impede o 9 são inconsistências novas, geradas pelas próprias correções, e quatro lacunas antigas fechadas só em parte.

| Peça | Nota r1 | Nota r2 | Lacuna da r1 | Fechada? | Evidência |
|---|---|---|---|---|---|
| P1 Inventário de plataformas e fichas | 7 | 8 | Fichas de observabilidade rasas; "custo" do Langfuse apoiado em marketing; OpenRouter sem ficha | **Parcial.** Langfuse custo, AgentOps custo e rastro foram rebaixados a `parcial`. OpenRouter saiu. As fichas não ganharam fontes. | `pesquisa/langfuse.md:57,73`; `plataformas.md:93-98,124-130,245-248`; `workflow-04-consumo-por-agente.html:59-62` |
| P2 Inventário do Maestro | 7 | 9 | Ledger parado no 064 não declarado; `arquivo:linha` | **Fechada.** | `inventario-maestro.md:73,75,76,121-125` (ledger); `:87,:90` (`SendMessage`/`ListAgents`, `contatos()` em `server.py:479`) |
| P3 Confronto e decisão | 6 | 8 | Auditoria e custo como NÃO PRECISA; cadastro de agentes sem onde operar; chaves em DEPOIS | **Parcial.** Auditoria e custo viraram ENTRA. Os totais fecham: 15+6+11=32. Cadastro de agentes continua NÃO PRECISA. | `confronto-decisao.md:64,74,177-185`; `:59,145` |
| P4 Lacunas declaradas | 7 | 8 | Não declara área somente leitura nem ledger parado | **Parcial.** A declaração existe, mas espalhada. | Ausente em `confronto-decisao.md:225-251`; presente em `inventario-maestro.md:121`, `administracao-01-catalogo.html:176`, `workflow-03:138`, `workflow-04:156-164` |
| P5 Mapa de contextos | 6 | 9 | Orçamento em contexto errado; § 6.5 só com o catálogo; endereço sem invariante | **Fechada.** | `mapa-de-contextos.md:80-84,274,300,303-305,343,349-353`; relação 5 em `:161-168` |
| P6 administracao-01-catalogo | 6 | 8 | Não cadastra; Modelo sem campos; "por projeto"; contagem "—"; sem agentes nem papéis | **Parcial.** Falta o objeto agente. | `administracao-01-catalogo.html:153-186,188-211,213-237,245-247` |
| P7 administracao-02-politicas | 7 | 8 | Escopo, precedência, quem edita, rastro, formulário | **Quase fechada.** Falta escopo na tabela de regras e há conflito de precedência. | `administracao-02-politicas.html:115-155,229-267,269-318,320-344` |
| P8 administracao-03-orcamento | 6 | 8 | Só instantâneo em %; sem teto por escopo; sem limiar; "Ajustar" é exemplo | **Parcial.** O limiar ficou sem desenho. | `administracao-03-orcamento.html:121-159,195-204,206-230` |
| P9 workflow-01 sessão de agente | 6 | 9 | Derrubar habilitado; subir em sessão viva; formulário pobre | **Fechada.** | `workflow-01-sessao-de-agente.html:98-127,129-152,154-160,162-178` |
| P10 workflow-02 estado do agente vivo | 6 | 8 | Sem tarefa, modelo e consumo na linha; sem alerta de parada | **Parcial.** Abriu uma contradição nova. | `workflow-02-estado-do-agente-vivo.html:75-123,126-135` |
| P11 workflow-03 tarefa aberta | 6 | 9 | Ledger parado; "travada" sem regra; sem tokens | **Fechada.** | `workflow-03-tarefa-aberta.html:79,115-120,122-134,136-140` |
| P12 workflow-04 consumo por agente | 5 | 8 | Agente × sessão; coluna duplicada; sem dólar, janela, ranking; OpenRouter | **Parcial.** Agente × sessão continua mal resolvido. | `workflow-04-consumo-por-agente.html:93-153,155-164,86-89 × 166-170` |
| P13 mensageria-01 | 7 | 9 | Tamanho da fila e idade da mais antiga | **Fechada.** | `mensageria-01-caixa-de-entrada.html:36-39,55-82,86-93` |
| P14 mensageria-02 | 7 | 8 | Sem correlação com tarefa e custo | **Não fechada.** Há um defeito novo nos exemplos. | `mensageria-02-livro-de-mensagens.html:48-58,66,93` |
| P15 mensageria-03 | 7 | 8 | Registro de nomes não é cadastro administrável | **Parcial.** | `mensageria-03-roteamento.html:44-79,81-92`; `administracao-01-catalogo.html:192-201` |
| P16 mensageria-04 | 7 | 8 | Sem ligação com permissão por agente | **Não fechada.** Há um erro factual novo. | `mensageria-04-protocolo.html:165-167` × `plataformas.md:231-232` |

## O que ainda falta para 9

**P1 (8).**
- As nove fichas de observabilidade têm de 2 a 5 linhas com URL (Langfuse: 5; AgentOps, Arize, Comet, CrewAI, Dify, Flowise, LangSmith: 3; AutoGen: 2). A correção rebaixou células em vez de aprofundar fontes.
- O critério de `plataformas.md:245-246` ("sim exige fonte que descreva o mecanismo") não foi aplicado de modo uniforme. O `sim` de auditoria do Langfuse se apoia em "audit logs listados entre os controles" (`langfuse.md:47`), uma lista de itens de página de segurança. É o mesmo tipo de apoio que rebaixou o custo (`:57`).
- Ação: rebaixar esse `sim` a `parcial`, ou abrir a página que documenta o mecanismo.
- Continua valendo que só LiteLLM e Claude Code rodaram.

**P3 (8).**
- Cadastro de agentes e RBAC seguem NÃO PRECISA por "já coberto" (`confronto-decisao.md:59,145`). Na r1 pedi justificar contra o que a referência entrega, e o texto não faz esse contraste. O Portkey cadastra com `sim`, e 11 plataformas têm `sim` em cadastro de agentes.
- O administrador continua sem lugar para ver ou operar os 13 agentes (perfil, ferramentas, papel). É o objeto central da dimensão e nenhuma tela o mostra.
- Cosmético: o título "ACRESCENTADAS (6)" (`:104`) lista 5 linhas. A sexta, a taxa, está na tabela de CONTROLE (`:51`), que por sua vez se intitula "(6)" mas tem 7 linhas (`:45-51`).

**P4 (8).**
- As lacunas existem, mas dispersas. Faltam em `confronto-decisao.md:225-251` (Limites), que não menciona nem o ledger parado nem a área inteira somente leitura (a busca por "064" e "somente leitura" não acha nada ali).
- Consolidar as duas declarações nessa seção.

**P6 (8).**
- A tabela de linhas (`administracao-01-catalogo.html:106-129`) tem as colunas Nome, Tipo, Onde vive, Invariante e Consultar. A linha do Modelo não tem provedor, preço, quem pode usar nem projeto, e o formulário (`:167-175`) os tem. `workflow-04:77` e `administracao-03:124` dizem que o preço sai "da tabela do Modelo, no catálogo", e essa tabela não existe na tela.
- A unicidade cobre skill, ferramenta e modelo (`:192`). O texto ao lado (`:199`) diz que o catálogo publica os nomes para endereçar mensagens, e esses nomes são de sessões e agentes, que o catálogo não registra.
- Os `data-fonte` da navegação continuam rotulando "limites de orçamento e de taxa" (`:65`), embora a taxa seja DEPOIS.

**P7 (8).**
- A tabela de regras (`administracao-02-politicas.html:119`) não tem coluna de escopo nem de precedência. O escopo está só em três cartões (`:246-267`), então não dá para ver a que agente, papel ou projeto cada regra se aplica.
- Há dois critérios de precedência sem conciliação: "deny > ask > allow, o mais restritivo vence" (`:231-232`) e "o mais específico vence" entre arquivos (`:263-264`).
- A base citada para "mais restritivo" é a permissão de acesso a agentes do LiteLLM (`litellm.md:55`), que não tem `ask`. A extrapolação deveria vir marcada como decisão de projeto.
- O botão "propor regra (exemplo)" (`:222`) convive com um formulário real (`:294-318`).

**P8 (8).**
- O limiar de alerta foi só descrito. O valor está declarado "DEPOIS" (`administracao-03-orcamento.html:201`) e a tabela de tetos (`:128`) não tem coluna de limiar. A correção 1 pedia limiar no desenho.
- Os três escopos de teto (projeto, agente, modelo) não dizem qual vale quando conflitam.
- O cabeçalho está desatualizado: "ENTRA: limites de orçamento e de taxa" e "juiz: Controle" (`:57-61`), quando a taxa é DEPOIS e o juiz 2 também avalia esta tela. O mesmo `data-fonte` está nas três telas da Administração.

**P10 (8).**
- O botão "reiniciar a sessão" no alerta (`workflow-02-estado-do-agente-vivo.html:133`) está habilitado e sem "quem autoriza". Isso contradiz a decisão 5 e o `workflow-01`, onde "reiniciar…" está desabilitado e atrás de confirmação.
- O estado "caída" (`:115`) não está entre os quatro cartões do resumo (`:65-68`). Esses cartões somam 2+1+1+0, e a tabela tem uma linha "trabalhando".
- Os exemplos divergem entre telas. Worker02 aparece "caída com 073-T3" aqui e "sem tarefa" em `workflow-01:117-118` e `workflow-03:103-104`.

**P12 (8).**
- Agente × sessão está feito pela metade. O mapa define agente como perfil registrado (`mapa-de-contextos.md:293,335`), mas a coluna "agente" traz nomes de slot de sessão ("Worker05 [78d88f] · [c4d5e6] (agente — sessões agrupadas)", `workflow-04-consumo-por-agente.html:107`). Duas sessões do mesmo perfil com nomes diferentes não somam, e o perfil nunca aparece.
- O teto contradiz a si mesmo. O cartão do resumo mostra "60% (exemplo)" com barra (`:86-89`), e a seção de baixo diz "nenhum teto declarado" (`:166-170`).
- A Administração guarda teto em tokens e dólar, e o Workflow exibe em %.

**P14 (8).**
- A correlação com tarefa e custo segue ausente. A única ligação é o texto do `[[TASK id=…]]` na coluna de mensagem.
- Defeito novo nos exemplos: `Worker01 [9a1b27]` (`:93`) e `Worker03 [9a1b27]` (`:67`) têm o mesmo ref na mesma tela. É a colisão que o invariante do mapa proíbe, e o exemplo a mostra como normal.

**P15 (8).**
- A tela de roteamento recusa e confirma bem. Ela não aponta para o registro que publica os nomes (relação 3 do mapa). E o catálogo só registra skill, ferramenta e modelo, não sessão nem agente.

**P16 (8).**
- Erro factual novo: a tela diz "LiteLLM é a única referência `sim` entre as 25" para A2A (`mensageria-04-protocolo.html:167`). A matriz tem cinco `sim` em protocolos (Copilot Studio, Agent 365, AgentCore, LiteLLM, CrewAI AMP; `plataformas.md:87`), e a leitura da matriz diz "5 fichas" (`:231`).
- A lacuna da r1 continua: não há ligação com permissão por agente (qual agente pode chamar qual ferramenta MCP). O "quem autoriza" (`:165-166`) cobre só leitura e escrita.

**Notas sobre as peças que passaram (9), sem bloquear.**
- P2: o inventário diz "auditoria: tem" (`inventario-maestro.md:64`), e o confronto diz "parcial" para a auditoria administrativa (`confronto-decisao.md:64`). A divisão é legítima, mas não vem declarada. O mesmo vale para "custo: tem" (`inventario-maestro.md:76`) contra o `parcial` do confronto (`:74`).
- P5: `mapa-de-contextos.md:243` ainda cita "relação 5" para o núcleo compartilhado, que agora é a relação 6.
- P9: o texto "por isso todos estão desabilitados" (`workflow-01-sessao-de-agente.html:127`) é impreciso, porque "subir" fica habilitado. O texto chama de "sessão regente" a linha do Gerente (`:113,171`), e o regente é o MAESTRO. O subir não diz que recusa nome duplicado.
- P11: a tabela ainda cita `tarefas.jsonl` como fonte de "desde", "tentativas" e "tokens" (`workflow-03-tarefa-aberta.html:70,79`), embora o aviso do rodapé (`:138`) declare o livro parado.

## Limites do que não li

- Só tenho Read, Grep e Glob. Não rodei `git`, `verifica-prototipo.py` nem `check-conformance.sh`. Não confirmei que o HEAD é `faca232`, nem os resultados "11 telas, 0 achados" e "76,4 M de tokens" do `done-073-correcao-1.md`.
- Não abri o código citado (`server.py:479`, `fila_outbox.py`, `multi-session.py`). As citações `arquivo:linha` do inventário e do confronto foram aceitas como estão.
- Das 25 fichas, li por inteiro só `langfuse.md`. As demais entraram por busca (`litellm.md:55`, contagem de linhas com URL), e a matriz entrou por `plataformas.md`. Não reabri URLs externas.
- Não li `README.md` do protótipo, o glossário, o `qa-report.md` nem o `spec.md`. Não li as linhas 1-47 das telas de workflow e mensageria (CSS e cabeçalho), nem o cabeçalho da `mensageria-01` além das linhas 36-39.
- Julguei os wireframes pelo HTML, sem renderizá-los. Nada do que digo sobre contraste, ordem visual ou navegação foi observado.
- A auditoria administrativa só tem estrutura e exemplo. Não há fonte viva para avaliar, e a tela diz isso (`administracao-01-catalogo.html:229`).

**DIAGNÓSTICO: mudou.** As lacunas da r1 foram fechadas em nove das 16 peças (fechadas, ou fechadas com nota, em P2, P5, P9, P11, P13 e o grosso de P3, P4, P7 e P12), e as que restam são sobretudo contradições criadas pelas correções: P10, o teto de P12, o A2A de P16, os exemplos de P14, o cabeçalho de P8 e a tabela do catálogo sem preço (P6). Três lacunas antigas seguem abertas e, se não mudarem na rodada seguinte, repetem o diagnóstico da r1: o cadastro de agentes como objeto operável (P3, P6), o limiar de alerta sem desenho (P8) e a correlação das mensagens com tarefa e custo (P14), junto com a ligação com permissão por agente (P16). Pela regra das duas rodadas, estas são as lacunas a vigiar.
