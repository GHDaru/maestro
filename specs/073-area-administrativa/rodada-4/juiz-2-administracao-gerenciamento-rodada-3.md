# Rodada 4 — Juiz 2: ADMINISTRAÇÃO E GERENCIAMENTO DE AGENTES — terceira leitura (contexto fresco, 27/10/2026, sobre HEAD 4e421a4)

**Veredito: barra NÃO atingida.** Doze das 16 peças chegam a 9 e quatro ficam em 8: P8, P10, P15 e P16. Nenhuma peça caiu.

A cobertura está completa:
- Os 16 ENTRA têm tela, incluindo o cadastro de agentes como leitura do catálogo de perfis. Os totais 16/5/11 = 32 fecham por contagem de linhas (`confronto-decisao.md:130-147,149-157,168-182,188-208`).
- As 25 plataformas têm ficha em `pesquisa/`. A auditoria do Langfuse foi rebaixada a `parcial` (`langfuse.md:47`).
- A tabela de agentes do catálogo lista 13 perfis. Conferi nome e ferramentas contra `.claude/agents/*.md`, e batem. O perfil não declara `model:`, então o "—" com motivo na coluna de modelo padrão é verdadeiro.

A regente fechou os três itens que eu mandei vigiar na segunda leitura:
- O cadastro de agentes virou objeto, na seção "Agentes (perfis)" (`administracao-01-catalogo.html:276-382`).
- O limiar de alerta virou coluna da tabela de tetos (`administracao-03-orcamento.html:136,145,155,165`).
- A correlação da mensagem com a tarefa virou coluna (`mensageria-02:55`). O custo ficou declarado como "— (ledger parado no 064)", conforme a decisão 7.

O que ainda segura quatro peças é pequeno e de texto. Três delas repetem a lacuna que nomeei na segunda leitura (P10, P15, P16). A P8 tem lacunas novas, criadas pela própria correção.

| Peça | Nota r2 | Nota r3 | Pedido da r2 | Fechado? | Evidência |
|---|---|---|---|---|---|
| P1 Pesquisa e fichas | 8 | 9 | Rebaixar o `sim` de auditoria do Langfuse ou abrir a página do mecanismo | **Fechado** pelo rebaixamento. As fichas continuam curtas e só LiteLLM e Claude Code rodaram, o que a peça declara. | `langfuse.md:47`; `plataformas.md:132,156` |
| P2 Inventário do Maestro | 9 | 9 | Nota: "auditoria/custo: tem" × `parcial` do confronto sem declarar | **Mantido.** A distinção custo "mecanismo × número vivo" agora está dita no próprio inventário. O cadastro de agentes (`:64`) é coerente com o ENTRA 16. | `inventario-maestro.md:64,81,124-141` |
| P3 Confronto e decisão | 8 | 9 | Contrastar o cadastro de agentes com o que a referência entrega; dar ao administrador onde ver os agentes; títulos "(6)" | **Fechado.** Portkey `sim` e 11 plataformas são citados. O "já coberto" é refutado ("confundia registro com tela"). A tela dos perfis existe. Os títulos conferem (7 linhas em CONTROLE, 5 em ACRESCENTADAS). | `confronto-decisao.md:67,135,163-166,112-122,51-59`; `administracao-01-catalogo.html:276-382` |
| P4 Lacunas declaradas | 8 | 9 | Consolidar ledger parado e área somente leitura em "Limites" | **Fechado.** A seção traz as quatro lacunas: ponto de execução, caminho do derrubar, ledger no 064, somente leitura. | `confronto-decisao.md:274-286`; `inventario-maestro.md:124-141` |
| P5 Mapa de contextos | 9 | 9 | Nota: `:243` citava "relação 5" | **Fechado.** O mapa registra a troca para relação 6 e a troca de "o único ponto" por "o ponto executável". Entrada de `agente (perfil)` no glossário do mapa. | `mapa-de-contextos.md:91,246,304,395-397` |
| P6 administracao-01-catalogo | 8 | 9 | Tabela do Modelo; unicidade cobrindo agentes; `data-fonte` da navegação; objeto agente | **Fechado.** A tabela do Modelo tem provedor, preço, quem pode usar e projeto. Preço e "quem pode usar" ficam desabilitados para a sessão dona. A unicidade inclui o agente (perfil). O `data-fonte` da navegação diz "limite de orçamento" sem "taxa". | `administracao-01-catalogo.html:65,153-182,201-207,228,276-382` |
| P7 administracao-02-politicas | 8 | 9 | Escopo na tabela de regras; precedência conciliada e marcada como decisão de projeto; botão de exemplo | **Fechado.** Há coluna Escopo e regra de modelo de exemplo (`:161-168`). Precedência em dois passos, declarada decisão de projeto (`:243-252`). O botão "propor regra (exemplo)" sumiu; o formulário ficou (`:238,312-336`). | `administracao-02-politicas.html:121-168,243-252,312-336` |
| P8 administracao-03-orcamento | 8 | **8** | Coluna de limiar; precedência entre tetos; cabeçalho e `data-fonte` | **Parcial.** Limiar e cabeçalho fechados (`:57-61` sem "taxa"; limiar na tabela). A precedência foi escrita com uma glosa que contradiz a decisão. A coluna "Efeito ao estourar" ainda oferece recusar e suspender. | `administracao-03-orcamento.html:136,145-166,171-175` × `:109-126` |
| P9 workflow-01 | 9 | 9 | Notas: texto "todos desabilitados", regente × Gerente, nome duplicado | **Mantido.** Derrubar com `stop` × `rm` e passagem pelo pedido de decisão (`:164-170`); reiniciar desabilitado (`:159`); subir com formulário e "quem autoriza" (`:129-152`). As notas de r2 seguem, sem bloquear. | `workflow-01-sessao-de-agente.html:127,129-152,159,164-178` |
| P10 workflow-02 | 8 | **8** | Reiniciar habilitado; "caída" fora dos cartões; Worker02 divergente entre telas | **Parcial (1 de 3).** O botão está desabilitado e aponta para o workflow-01. Os cartões do resumo seguem contradizendo a tabela. Worker02 segue "caída com 073-T3" aqui e "sem tarefa" nas outras telas. | `workflow-02-estado-do-agente-vivo.html:133-135` (fechado); `:65-68` × `:86-122`; `:114-118` × `workflow-01:117-118`, `workflow-03:103-104` |
| P11 workflow-03 | 9 | 9 | Nota: tabela cita `tarefas.jsonl` como fonte | **Mantido.** Regra de "travada", pedido de decisão, "cancelar" mostra o que se perde, ledger parado declarado. A nota segue: os `data-fonte` de `desde`/`tentativas`/`tokens` ainda apontam para `tarefas.jsonl` (`:70,77-79`), embora o rodapé o declare parado. | `workflow-03-tarefa-aberta.html:116-120,130,136-139` |
| P12 workflow-04 | 8 | 9 | Agente × sessão; teto "60%" × "nenhum teto"; % × tokens/US$ | **Fechado.** A coluna "agente" é o perfil sem ref, com as sessões (nome · ref · projeto) agrupadas dentro. O cartão do teto mostra "— (nenhum teto declarado)", reconcilia com a seção de baixo e declara que comparar contra um piso pode estourar sem aviso. A unidade é tokens ou US$ estimado. | `workflow-04-consumo-por-agente.html:55-56,86-89,106-134,165-171` |
| P13 mensageria-01 | 9 | 9 | — | **Mantido.** Contagem e idade da mais antiga do relógio (`:36-39`). | `mensageria-01-caixa-de-entrada.html:36-39,56-87` |
| P14 mensageria-02 | 8 | 9 | Correlação com tarefa e custo; refs duplicados na tela | **Fechado.** Coluna `tarefa` derivada da tag `[[TASK]]`, coluna `custo` declarada como "— (ledger parado no 064)". Livro em ordem coerente com o título. Nenhum ref repetido sob dois nomes. Leitura restrita ao projeto declarada. | `mensageria-02-livro-de-mensagens.html:36,55,59,64-118,124-125` |
| P15 mensageria-03 | 8 | **8** | Apontar para o registro que publica os nomes (relação 3) | **Não fechado.** A tela de roteamento não menciona Administração nem catálogo (busca sem resultado). O catálogo aponta para o roteamento, mas o caminho de volta não existe. Windmill saiu e a recusa com oferta do ref novo entrou. | `mensageria-03-roteamento.html:44-82`; `administracao-01-catalogo.html:233-239,382` |
| P16 mensageria-04 | 8 | **8** | Ligação com permissão por agente; erro factual do A2A | **Parcial.** O A2A corrigido ("5 `sim`"). `registrar_peca` ganhou "quem autoriza". Nenhuma ligação com a política (qual agente chama qual ferramenta MCP). A lacuna é a mesma da r1 e da r2. | `mensageria-04-protocolo.html:166-169`; sem referência a `administracao-02` |

## O que fica aberto

**P8 (8) — falta de desenho; o texto desvia da decisão da regente.**
- **Precedência de tetos.** A decisão 6 diz "o menor teto aplicável vence". A tela escreve "vence o menor teto aplicável — o recorte mais estreito (modelo antes de agente, agente antes de projeto) e, no empate de escopo, o menor valor" e acrescenta "é a mesma lógica da política" (`administracao-03-orcamento.html:171-175`). São duas regras diferentes. Com projeto a 100 e agente a 500, "menor teto" dá 100 e "recorte mais estreito" dá 500. A correção é de texto: cortar a glosa e deixar só o menor valor entre os tetos aplicáveis.
- **Coluna "Efeito ao estourar".** A coluna oferece "avisar · recusar · suspender" nas linhas de projeto, agente e modelo (`:146,156,166`). Na mesma tela, o cartão de cima declara recusar e suspender como DEPOIS (`:109-126`). O fecho é marcar essas opções com "DEPOIS" na tabela, ou reduzir a coluna a "avisar".
- Não é decisão de produto. A regente já decidiu e o texto ficou por conformar.

**P10 (8) — falta de desenho.**
- Os quatro cartões do resumo somam 2+1+1+0, com "bloqueado 0" e "sem tarefa 1" (`workflow-02:65-68`). A tabela tem uma linha trabalhando, uma esperando, uma bloqueada e uma caída (`:86-122`). Não há linha "sem tarefa", e "caída" não tem cartão.
- Worker02 aparece "caída com 073-T3 · revisão" (`:114-118`). Se tem tarefa aberta, `workflow-03` deveria listá-la, mas lá a linha de Worker02 diz "sem tarefa aberta" (`workflow-03:103-104`). `workflow-01:117-118` também diz "sem tarefa".
- Um exemplo coerente em três telas, mais um cartão para "caída", fecha o assunto.

**P15 (8) — falta de desenho (uma linha).**
- A tela de roteamento resolve nome em ref e recusa bem. Falta dizer de onde vêm os nomes. O catálogo aponta para o roteamento; o roteamento não aponta de volta para "Agentes (perfis)" no catálogo.

**P16 (8) — falta de desenho, com um ponto que é decisão de produto.**
- As três ferramentas MCP e o "quem autoriza" cobrem leitura e escrita. Falta ligar a ferramenta MCP à política allow/deny/ask por agente.
- Desenhar o ponteiro para `administracao-02` é trivial. Mas nenhum documento decide se as chamadas MCP entram sob a política por agente. Essa decisão é do Darú, e sem ela o ponteiro só pode dizer "não decidido".
- Esta é a lacuna que repete pela terceira vez (r1, r2, r3).

## Ressalvas que não bloqueiam nenhuma nota

- **Precedência de regras (`administracao-02:243-252`).** O passo "o mais específico decide qual regra se aplica" deixa um `allow` de agente vencer um `deny` de projeto. Para as imutáveis isso não vale, porque o `deny` é um gancho fora da política. Mas a tela não diz que há `deny` não sobrescritível.
- **Ids entre telas da Mensageria.** A mesma mensagem tem id diferente entre telas: "Segue o inventário…" é `msg-0421` em `mensageria-01:57` e `msg-0417` em `mensageria-02:110`. O desvio de 07:20 sai de Worker05 em uma e de Worker01 na outra.
- **Glossário proposto.** O verbete "limite de orçamento" ainda diz "executável (não só declarado)" (`confronto-decisao.md:222`), o oposto da decisão 2.
- **Filtro do catálogo.** O filtro por tipo e o formulário "cadastrar" não incluem "Agente (perfil)" (`administracao-01-catalogo.html:138-142,191-195`).

## Limites do que não li

- Não rodei `git`, `verifica-prototipo.py` nem `check-conformance.sh`. Não confirmei que o HEAD é `4e421a4`, nem "11 telas, 0 achados, seis regras". A regra 6 do verificador, sua fixture e a mutação 28→0 não foram abertas.
- `done-073-correcao-2.md` não existe. Usei `andamento.md` (só trechos por busca). Não li o `qa-report.md`.
- Não abri código. A única conferência real foi a lista de ferramentas dos perfis em `.claude/agents/*.md`.
- Das 25 fichas, li só trechos de `langfuse.md` e linhas de `plataformas.md`. Não conferi uma a uma as revalidações de `claude-code.md`.
- Li `confronto-decisao.md` por inteiro. Do inventário, do mapa e do README li só trechos por busca.
- Nas telas li o corpo e o rodapé, não o CSS e o `<head>`. Julguei tudo pelo HTML, sem renderizar.

**DIAGNÓSTICO: mudou.** Das 11 peças que estavam em 8 na segunda leitura, sete subiram a 9 (P1, P3, P4, P6, P7, P12, P14). Os três itens que mandei vigiar foram fechados. Das quatro peças que seguem em 8, três repetem a lacuna da segunda leitura (P10, P15, P16). A P8 tem lacunas novas, criadas pelas correções. Nenhuma das quatro exige decisão de produto, exceto o ponto de P16 sobre MCP sob a política por agente. As outras três são edições de texto.
