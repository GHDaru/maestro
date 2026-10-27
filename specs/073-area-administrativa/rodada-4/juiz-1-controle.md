# Rodada 4 — Juiz 1: CONTROLE (contexto fresco, 26/10/2026, sobre HEAD 83c386e)

Veredito: **barra não atingida**. Nenhuma peça em 9 ou mais; nota máxima 8. Os 13 ENTRA têm tela
(nenhum "não coberto"), mas o nº 1 (derrubar) e o nº 4 (taxa) são cobertos só no nome. As 25
plataformas têm ficha.

| Peça | Nota | Maior lacuna | Evidência |
|---|---|---|---|
| P1 Inventário de plataformas | 7 | "Pausar" tem 19 de 25 células "—"; a matriz não separa limite que corta de alerta que só avisa. | `pesquisa/plataformas.md:67`, `:85`, `:181-183` |
| P2 Inventário do Maestro | 8 | Diz que allow/ask "não são executáveis" lendo só o `settings.json` versionado; o harness do Claude Code já executa `permissions.allow/ask/deny`. | `confronto/inventario-maestro.md:46`, `:117-118`; `pesquisa/claude-code.md:49` |
| P3 Confronto e decisão | 7 | Pausar/retomar em DEPOIS por "o mercado quase não tem", argumento sobre células "—" que contraria a regra 2 do próprio documento; o teto executável (ENTRA 4) é o que cria a necessidade de suspender; a taxa foi cortada em silêncio. | `confronto/confronto-decisao.md:118-119` vs `:17-20`; `:88` vs `:150` |
| P4 Lacunas declaradas | 7 | Não declara que nenhuma tela define o ponto de execução nem o caminho de aprovação humana do derrubar. | `inventario-maestro.md:111-119`; `plataformas.md:222-235` |
| P5 Mapa de contextos | 6 | Não diz onde mora a autoridade de controle (dono dos hooks); falta a relação Workflow → Regência (derrubar ou ask virando pedido de decisão); limite de orçamento em Workflow no mapa e em Administração na tela. | `confronto/mapa-de-contextos.md:75-76`, `:247`; `administracao-orcamento.html:58`; `README.md:44-48` |
| P6 mensageria-01 caixa de entrada | 8 | "Drenar outbox" muda estado e não diz quem pode drenar a caixa de outra sessão. | `mensageria-01-caixa-de-entrada.html:75` |
| P7 mensageria-02 livro de mensagens | 8 | Falta dizer quem pode ver ou filtrar mensagens de outras sessões. | `mensageria-02-livro-de-mensagens.html:86-87` |
| P8 mensageria-03 roteamento | 8 | Recusa de nome ambíguo é bom controle; falta confirmação humana antes de entregar a uma sessão errada (não se desfaz). | `mensageria-03-roteamento.html:36-37`, `:83` |
| P9 mensageria-04 protocolo | 8 | "Registrar status" e "Chamar estado_atual" são escrita e leitura sem dizer quem autoriza. | `mensageria-04-protocolo.html:114-115`, `:108` |
| P10 administracao-catalogo | 8 | O modelo é só linha de registro, sem ligação com a política (qual modelo cada sessão pode usar). | `administracao-catalogo.html:122-128` |
| P11 administracao-politicas | 6 | Sem ordem de precedência, padrão (default-deny) nem escopo; sem o caminho do ask até a fila de decisões e o ruling; as referências "sem ask" omitem Claude Code e Kiro, que têm ask = sim. | `administracao-politicas.html:172-187`, `:198-200`; `claude-code.md:49` |
| P12 administracao-orcamento | 6 | Limite só "declarado"; efeito ao estourar e taxa como "—"; "consumo corrente 19 %" é valor de 25/10 sem idade do relógio (F7); 40 % é cota semanal do regente, não teto por agente ou sessão. | `administracao-orcamento.html:87`, `:93`, `:100`, `:126`, `:147` |
| P13 workflow-01 sessão de agente | 5 | Derrubar sem gate desenhado; botão habilitado em cada linha e outro desabilitado embaixo (contradição); não mostra o que se perde (tarefa aberta, worktree), a reversibilidade nem a confirmação; "subir" em sessão já viva; nada protege derrubar o Gerente. | `workflow-01-sessao-de-agente.html:93`, `:103`, `:113`, `:133` |
| P14 workflow-02 estado do agente vivo | 7 | "bloqueado" e "esperando" não levam a nenhuma ação (abrir o pedido de decisão ou derrubar). | `workflow-02-estado-do-agente-vivo.html:81`, `:100-103` |
| P15 workflow-03 tarefa aberta | 8 | Respeita "não fecha tarefa"; falta cancelar ou reatribuir. | `workflow-03-tarefa-aberta.html:108-111` |
| P16 workflow-04 consumo por agente | 7 | Consumo é piso (soma de `message.usage`) e a tela diz que não bloqueia nada; contradiz a tela de orçamento (aqui "nenhum teto", lá 40 %). | `workflow-04-consumo-por-agente.html:106`, `:116-117` |

## O que precisa mudar para 9

- **P13**: desenhar o gate do derrubar: confirmação humana mostrando tarefa aberta e worktree, reversibilidade (o que fica salvo e como religar), proteção contra derrubar o Gerente, remover os botões habilitados nas linhas e o "subir" em sessão viva.
- **P12**: efeito ao estourar (recusar, avisar ou suspender), escopo por sessão e por projeto, unidade (tokens ou dólar), idade do relógio; taxa desenhada ou rebaixada formalmente a DEPOIS no confronto.
- **P11**: precedência, padrão e escopo; fluxo do ask até a fila de decisões e o ruling humano; ligação com o bloco `permissions` do `settings.json`; corrigir as referências que omitem Claude Code e Kiro.
- **P5**: nomear o dono do ponto de execução do controle e a relação Workflow → Regência (ask e derrubar); reconciliar o contexto do limite de orçamento (mapa § 6.3 contra a tela).
- **P3**: justificar pausar/retomar como "sem fonte", não "mercado não tem"; reconhecer que retomar existe no Claude Code (`claude attach`) e que o teto executável cria a necessidade de suspender; taxa como DEPOIS ou desenhada.
- **P1**: separar "corta" de "só avisa" no limite (ou coluna de ponto de execução).
- **P2**: reexaminar allow/ask à luz do harness do Claude Code.
- **P4**: declarar que ponto de execução e aprovação do derrubar não estão desenhados.
- **P14 e P16**: ligar bloqueado/esperando a uma ação; reconciliar o teto com o orçamento e declarar o risco de subcontagem do piso.
- **P6 a P10 e P15**: declarar quem autoriza cada ação de escrita; em P8, confirmação antes de entregar a sessão errada.

Limite declarado pelo juiz: não leu `verifica-prototipo.py` em detalhe nem fichas além de
`claude-code.md` e `windmill.md`.
