# Rodada 4 — Juiz 1: CONTROLE — quarta leitura (contexto fresco, 27/10/2026, sobre HEAD 1bbf171)

## Veredito

**Barra não atingida, por uma célula.** 15 das 16 peças chegam a 9 ou mais. P1 fica em 8. P5 e P12 sobem para 9. A causa de P1 é de execução, não de desenho: uma marca da matriz está sem a fonte que o Darú exigiu em D1.

**Funcionalidades ENTRA: atendidas.** Totais 16/5/11 = 32. O ENTRA 4 agora é "declarar teto + avisar, com emissor desenhado" (`administracao-03-orcamento.html:109-125`, `:226-246`; `confronto-decisao.md:28-31`). A política allow/deny/ask é o 5º ENTRA da Administração no mapa (`mapa-de-contextos.md:308-313`). Recusar e suspender seguem como DEPOIS.

**Plataformas: 25 analisadas** (`plataformas.md:64-91`). Não reabri as fichas, só as que a linha de orçamento e taxa cita.

## Tabela

| Peça | Nota r3 | Nota r4 | Pedido da r3 | Fechado? | Evidência |
|---|---|---|---|---|---|
| P1 Plataformas | 8 | **8** | Marcar por célula se o `sim` corta ou só avisa, mantendo as 26 linhas (D1) | **Quase.** A linha ficou única e cada `sim`/`parcial` ganhou `corta`, `avisa` ou `avisa?`. As citações que conferi batem. Falta a fonte da marca de Flowise: a tabela de fontes tem 15 linhas e só 12 são `corta`; o texto diz "13 `corta`" (`plataformas.md:165`, `confronto-decisao.md:30`). A 13ª é o Flowise, cuja ficha só lista "rate limit" entre os controles de segurança (`flowise.md:28`). D1 manda `avisa?` com motivo quando a ficha não dá fonte. | `plataformas.md:69` (célula do Flowise `parcial (corta)`), `:105-119`, `:165`; `flowise.md:28`; conferidos `claude-code.md:62`, `kiro-crew.md:36`, `prefect.md:35`, `temporal-web-ui.md:86`, `windmill.md:29` |
| P2 Inventário | 9 | 9 | — | Mantida | Citações de `claude-code.md` batem, inclusive `:59`, `:61`, `:62` |
| P3 Confronto | 9 | 9 | — | Mantida; D1, D2, D3 registrados; taxa desdobrada como DEPOIS | `confronto-decisao.md:28-31`, `:77`, `:193`, `:297`, `:312` |
| P4 Lacunas | 9 | 9 | — | Mantida; dívida do ponto de execução do derrubar declarada | `workflow-01-sessao-de-agente.html:178` |
| P5 Mapa de contextos | 8 | **9** | Dar casa à política allow/deny/ask no mapa | **Sim.** § 6.5 lista os "cinco ENTRA da Administração" com a política e a ferramenta MCP como escopo (D2); verbete em `:302`; 16 de 16. | `mapa-de-contextos.md:302`, `:308-313`, `:384-385`, `:408-409`; `:38` |
| P6 mensageria-01 | 9 | 9 | — | Mantida; aviso `msg-0418` com `data-fonte` em `painel/custo.py` | `mensageria-01-caixa-de-entrada.html:59`, `:62`, `:110` |
| P7 mensageria-02 | 9 | 9 | — | Mantida; id igual ao da caixa; remetente é o painel | `mensageria-02-livro-de-mensagens.html:122-126` |
| P8 mensageria-03 | 9 | 9 | — | Mantida; "De onde vêm os nomes" cita o catálogo e a relação 3 | `mensageria-03-roteamento.html:85-86` |
| P9 mensageria-04 | 9 | 9 | — | Mantida; cada ferramenta aponta para a regra MCP (D2) | `mensageria-04-protocolo.html:88`, `:95`, `:100`, `:105`, `:110` |
| P10 administracao-01 | 9 | 9 | — | Mantida; filtro e formulário com "Agente (perfil)"; preço e "quem pode usar" desabilitados para a sessão dona | `administracao-01-catalogo.html:142`, `:196`, `:203-205`, `:278-288` |
| P11 administracao-02 | 9 | 9 | — | Mantida; regra MCP com âncora; `deny` não sobrescritível (guard de imutáveis, arquivo existe) | `administracao-02-politicas.html:169-179`, `:263-266`; `scripts/hooks/guard-immutables.py` |
| P12 administracao-03 | 8 | **9** | Marcar o DEPOIS na tabela de tetos; dizer qual processo emite o aviso (D3) | **Sim, os dois.** "avisar (hoje) · recusar DEPOIS · suspender DEPOIS" nas três linhas; precedência "o menor teto aplicável" sem glosa; seção "Quem emite o aviso" com processo (`painel/custo.py`), gatilho, endereço, idade do relógio e "aviso atrasado, nunca perdido"; corte DEPOIS. | `administracao-03-orcamento.html:129-176` (`:148`, `:158`, `:168`), `:226-246` |
| P13 workflow-01 | 9 | 9 | — | Mantida; ressalva da fonte do stop/rm fechada (ficha corrigida da documentação oficial, citada com aspas) | `workflow-01-sessao-de-agente.html:167-169`; `claude-code.md:59`, `:61` |
| P14 workflow-02 | 9 | 9 | — | Mantida (amostra rápida) | `workflow-02-estado-do-agente-vivo.html:133-135` |
| P15 workflow-03 | 9 | 9 | — | Mantida (amostra rápida) | `workflow-03-tarefa-aberta.html:130-131` |
| P16 workflow-04 | 9 | 9 | — | Mantida; linha de exemplo do aviso com `data-fonte` em `painel/custo.py` | `workflow-04-consumo-por-agente.html:171` |

## O que fica aberto

**P1: 8. Falta de execução, uma célula, sem decisão de produto.** Duas saídas, ambas dentro de D1: acrescentar a linha do Flowise à tabela de fontes (só se a ficha disser que o limite barra, e hoje não diz); ou trocar a marca para `avisa?` com o motivo "ficha só lista rate limit entre controles", passando a contagem a 12 `corta` · 1 `avisa` · 3 `avisa?` em `plataformas.md:165` e `confronto-decisao.md:30`. A segunda é a mais honesta. A marca do n8n (`corta`, `n8n.md:30`) é defensável, mas mais fraca que as de 429.

## Ressalvas dos 9 (não mudam a nota)

- **P13** fechada. **P11** em parte: a tela admite o `deny` não sobrescritível; a regra geral pode colidir com o harness em escopos diferentes (não verificado; declarada como decisão de projeto, basta). **P9** `estado_atual` "qualquer sessão chama" (`:171`) convive com o ponteiro à política: tensão pequena. **P6** e **P10** sem mudança. **P12, nova (D3)**: `painel/custo.py` hoje indexa transcritos em `dados/custo.db` (`custo.py:1-6`, `:21-24`), não lê o ledger nem grava na fila — a comparação com o teto e o enfileiramento são código novo, e a tela os rotula "desenhado", corretamente; falta dizer como não repetir o aviso a cada ingestão depois do cruzamento (pergunta para a implementação).

## Limites do que li

- Não rodei scripts; gate 11/0 e conformance pelo `andamento.md:110-123` e `qa-report.md:1530-1590`.
- Inteira: `administracao-03-orcamento.html`. Trechos: `administracao-02-politicas.html` (`:150-179`, `:252-271`), `workflow-01` (`:160-181`). Por busca: `administracao-01`, as quatro de Mensageria, `workflow-02/03/04` (P14 e P15 por amostra).
- Matriz: `plataformas.md:60-135`, `:160-168`; linha de orçamento/taxa conferida contra 6 fichas; nas outras só a existência do trecho. Mapa: `:34-47`, `:296-325` e greps.
- Não li o README, o glossário, o confronto inteiro nem os pareceres dos juízes 2 e 3. De `custo.py` li o cabeçalho e os nomes de função.

DIAGNÓSTICO: **mudou.** Os fios de decisão (D1, D2 e D3) fecharam. Na r3 faltava desenho em três peças. Agora falta uma marca de célula na matriz, o Flowise sem fonte, que um passo de edição resolve e que não é decisão de produto.
