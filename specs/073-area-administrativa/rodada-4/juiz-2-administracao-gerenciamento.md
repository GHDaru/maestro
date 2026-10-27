# Rodada 4 — Juiz 2: ADMINISTRAÇÃO E GERENCIAMENTO DE AGENTES (contexto fresco, 26/10/2026, sobre HEAD 83c386e)

Veredito: **barra não atingida**. Os 13 ENTRA têm tela (21 e 26 cobertos de forma indireta, como
objeto e condição); as 25 plataformas têm ficha; uma plataforma citada fora das 25 (OpenRouter, em
`workflow-04`) não tem ficha.

| Peça | Nota | Maior lacuna | Evidência |
|---|---|---|---|
| P1 Inventário de plataformas | 7 | As 9 fichas de observabilidade têm 2 a 5 URLs; "custo por sessão" do Langfuse apoiado em página de marketing; só o LiteLLM rodou; OpenRouter citado sem ficha. | `pesquisa/langfuse.md:56-57`; `plataformas.md:18`; `workflow-04-consumo-por-agente.html:53` |
| P2 Inventário do Maestro | 7 | Os `arquivo:linha` conferidos batem; mas "custo = tem" e "tarefa aberta" apoiam-se no livro de ponto, que parou no ciclo 064 — o inventário não registra isso. | `confronto/inventario-maestro.md:70-72`; `done-073-rodada-3.md:73-74` |
| P3 Confronto e decisão | 6 | Administração fica com 1 ENTRA de 6; "auditoria" (trilha de mudança de chave, papel, modelo com `changed_by`, que o LiteLLM tem) e "cadastro de agentes" viram NÃO PRECISA sem dar ao administrador onde operar; "custo" NÃO PRECISA embora o painel só mostre tokens; "chaves" em DEPOIS. | `confronto/confronto-decisao.md:48,53,63,51,136`; `inventario-maestro.md:72`; `litellm.md:95` |
| P4 Lacunas declaradas | 7 | Não declara que a área inteira é somente leitura nem que o ledger de custo está parado. | `confronto-decisao.md:163-175`; `administracao-catalogo.html:73` |
| P5 Mapa de contextos | 6 | "Limite de orçamento" no Workflow (§ 2 l. 75, § 6.3 l. 247) e na Administração nas telas, divergência declarada e não corrigida; o cabeçalho das telas cita "§ 6.5: os três ENTRA da Administração" e o § 6.5 lista só o catálogo; em `workflow-04` a coluna "agente" lista sessões (a colisão que o § 7 diz evitar). | `mapa-de-contextos.md:75-76,247,295`; `README.md:44-48`; `administracao-orcamento.html:65` |
| P6 administracao-catalogo | 6 | Não cadastra nada ("lê, não edita"); linha do Modelo sem campos (provedor, preço, quem pode usar); "por projeto" ausente; contagem de agentes "—"; não há tela de agentes nem de papéis. | `administracao-catalogo.html:73,123-127,158` |
| P7 administracao-politicas | 7 | Faltam escopo (agente, papel, projeto), precedência, quem edita e rastro da mudança; "Propor regra" sem formulário. | `administracao-politicas.html:110-150,198-200` |
| P8 administracao-orcamento | 6 | Os dois números reais são instantâneo de 25/10 da sessão do regente em % do semanal; sem teto em tokens ou dólar por projeto, agente ou modelo; sem limiar de alerta; "Ajustar teto" é exemplo. | `administracao-orcamento.html:87,93,147` |
| P9 workflow-01 sessão de agente | 6 | "Derrubar" habilitado em cada linha com a tela dizendo que aguarda gate humano; "subir" em sessão viva; formulário "subir" pede só o nome, sem modelo, perfil ou worktree (o que o lançador recebe). | `workflow-01-sessao-de-agente.html:92-94,124,133`; `scripts/multi-session.py:91-92` |
| P10 workflow-02 estado do agente vivo | 6 | Lista sem tarefa aberta, modelo nem consumo (três telas para ver uma sessão); detecção de processo só rótulo; sem alerta de sessão parada. | `workflow-02-estado-do-agente-vivo.html:69-75` |
| P11 workflow-03 tarefa aberta | 6 | Fonte `tarefas.jsonl` parada desde o 064; "travada" sem regra; não mostra tokens da tarefa. | `workflow-03-tarefa-aberta.html:61,66` |
| P12 workflow-04 consumo por agente | 5 | Mistura agente e sessão; "tokens da sessão" e "consumo por agente" repetem o mesmo valor; um modelo por linha; sem dólar, janela de tempo ou ranking; fonte cita OpenRouter sem ficha. | `workflow-04-consumo-por-agente.html:53,79-82,87-90` |
| P13 mensageria-01 | 7 | Falta tamanho da fila outbox por sessão e idade da mais antiga (para o administrador). | — |
| P14 mensageria-02 | 7 | Rastro de mensagens sem correlação com tarefa e custo. | — |
| P15 mensageria-03 | 7 | O registro de nomes não é cadastro administrável. | — |
| P16 mensageria-04 | 7 | MCP bem citado; A2A "—" com motivo; falta ligação com permissão por agente. | — |

(P13 a P16 lidos só em cabeçalhos, tabelas e botões — fora do centro da dimensão.)

## O que muda para 9

1. **Mapa (P5)**: decidir se o limite de orçamento é do Workflow ou da Administração e ajustar § 2, § 6.3 e § 6.5; a coluna "agente" de `workflow-04` mostra agentes, não sessões.
2. **Confronto (P3)**: reabrir "auditoria" (trilha administrativa com `changed_by`) e "custo" (dólar por agente); se ficarem fora, justificar por escrito contra o que a referência entrega.
3. **Administração (P6, P7, P8)**: cada tela mostra o fluxo de escrita mesmo sem executá-lo: catálogo com formulário "cadastrar" e campos do Modelo; políticas com escopo e precedência; orçamento com teto por projeto, agente e modelo, e limiar de alerta.
4. **Workflow (P9 a P12)**: `workflow-01` desabilita o derrubar nas linhas e acrescenta modelo e perfil ao "subir"; `workflow-02` junta tarefa aberta, modelo e consumo na mesma linha; `workflow-04` tira a coluna duplicada, traz custo, janela e quebra por modelo, e troca OpenRouter por plataforma com ficha.
5. **Fontes (P1, P2)**: aprofundar as fichas de observabilidade ou rebaixar as células "sim" apoiadas em marketing; declarar no inventário que o ledger parou no 064.
