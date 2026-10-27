# Rodada 4 — Juiz 2: ADMINISTRAÇÃO E GERENCIAMENTO DE AGENTES — quarta leitura (contexto fresco, 27/10/2026, sobre HEAD 1bbf171)

**Veredito: barra atingida para a minha dimensão.** As 16 peças ficam em 9 ou mais. P8, P10, P15 e P16 subiram de 8 para 9. As 12 que estavam em 9 não regrediram na amostra. Cobertura: 16 ENTRA com tela e 25 plataformas com ficha, como na leitura anterior. Não repeti essa contagem.

Os quatro pedidos foram atendidos à luz das decisões D1, D2 e D3 do Darú. Fiz as conferências com Read e Grep, com arquivo e linha. Não rodei scripts, então o 11/0 do verificador e o verde da conformance estão no `qa-report.md:1553-1574` e eu não os reproduzi.

| Peça | Nota r3 | Nota r4 | Pedido da r3 | Fechado? | Evidência |
|---|---|---|---|---|---|
| P1 Pesquisa e fichas | 9 | 9 | — | Mantido | `plataformas.md:69` ganhou a marca por célula (D1). A linha traz `corta`, `avisa` e `avisa?` (sem fonte para a distinção). Não conferi a fonte de cada célula, e o 13/1/2 do `qa-report.md:1548` não foi recontado. |
| P2 Inventário do Maestro | 9 | 9 | — | Mantido | Sem mudança relevante. Amostra por busca. |
| P3 Confronto e decisão | 9 | 9 | Verbete "limite de orçamento" (ressalva) | **Fechado** | `confronto-decisao.md:240` agora diz "declarado + aviso", com emissor = ingestão de consumo e corte depois. O ENTRA 4 em `:76` diz "declarar o teto + avisar", com o corte em DEPOIS. A taxa saiu como linha própria em `:77`. |
| P4 Lacunas declaradas | 9 | 9 | — | Mantido | Sem regressão na amostra. |
| P5 Mapa de contextos | 9 | 9 | — | Mantido | `mapa-de-contextos.md:302` registra a política declarativa com escopo por agente e por ferramenta MCP, "sem tela própria". É a D2 aplicada. |
| P6 administracao-01-catalogo | 9 | 9 | Filtro e formulário com "Agente (perfil)" (ressalva) | **Fechado** | `administracao-01-catalogo.html:142` (filtro) e `:196` (formulário). A tabela de perfis segue em `:288`. |
| P7 administracao-02-politicas | 9 | 9 | Deny não sobrescritível (ressalva) | **Fechado** | `administracao-02-politicas.html:263-266`: o passo "mais específico" não vale para as imutáveis, e o `deny` é `guard-immutables.py`, fora da política. |
| P8 administracao-03-orcamento | 8 | **9** | Cortar a glosa da precedência; marcar recusar e suspender como DEPOIS; desenhar o emissor (D3) | **Fechado** | Precedência (`:173-176`): "o menor teto aplicável… Não há recorte por escopo… não a lógica da política". Efeito ao estourar (`:148,158,168`): "avisar (hoje) · recusar DEPOIS · suspender DEPOIS". Seção "Quem emite o aviso" (`:226-246`): `painel/custo.py` ao ingerir, enfileira na outbox para a sessão dona e o regente, com idade do relógio e "aviso atrasado, nunca perdido". O corte segue DEPOIS (`:242-244`). `painel/custo.py` e `painel/fila_outbox.py` existem no disco. |
| P9 workflow-01 | 9 | 9 | — | Mantido | Worker02 em `:117-119` é "caída", com `reiniciar…` e `derrubar…` desabilitados. Coerente com as outras telas. |
| P10 workflow-02 | 8 | **9** | Cartões coerentes com a tabela, cartão "caída", Worker02 igual nas telas | **Fechado** | Cinco cartões (`:65-69`) com "1+1+0+1+1 = 4", declarado em `:71`. A tabela tem quatro linhas (`:88-123`). Worker02 `[31f7bf]` é "caída" e sem tarefa em `workflow-02:116-118` e `workflow-01:117-119`; em `workflow-03:103-104` é "sem tarefa aberta". A linha caída leva às mensagens endereçadas a ela (`:122`). |
| P11 workflow-03 | 9 | 9 | `data-fonte` de desde/tentativas/tokens | **Fechado** | `workflow-03:77-79` declaram "parado no ciclo 064… valor vivo «— (ledger parado no 064)»". |
| P12 workflow-04 | 9 | 9 | Linha de exemplo do aviso (D3) | **Fechado** | `workflow-04:171` traz o aviso de teto vindo de `painel/custo.py`, para a sessão dona e o regente, marcado "exemplo". O cartão do teto segue "— (nenhum teto declarado)" em `:87`, e a seção `:165-172` reconcilia. |
| P13 mensageria-01 | 9 | 9 | Ids iguais entre telas (ressalva) | **Fechado** | `msg-0417` é "Segue o inventário…", de Worker05 para Worker03, em `mensageria-01:67-71` e `mensageria-02:111-116`. A `msg-0418` (aviso) em `mensageria-01:59-63` e `mensageria-02:122-127`. |
| P14 mensageria-02 | 9 | 9 | Linha de exemplo do aviso (D3) | **Fechado** | `mensageria-02:122-127`: emissor "painel · ingestão de consumo (painel/custo.py)", endereçado aos dois destinatários, `data-fonte` no módulo; "o emissor não é uma sessão". |
| P15 mensageria-03 | 8 | **9** | Caminho de volta para o registro que publica os nomes (relação 3) | **Fechado** | `mensageria-03:85-86`: "De onde vêm os nomes… catálogo da Administração, seção Agentes (perfis)… relação 3 do mapa". Aponta para `administracao-01-catalogo.html` e cita `.claude/agents/*.md`. |
| P16 mensageria-04 | 8 | **9** | Ligar cada ferramenta MCP à política allow/deny/ask por agente (D2) | **Fechado** | Coluna "regra de política que autoriza a chamada (escopo ferramenta MCP)" em `mensageria-04:88`; as três ferramentas apontam para `administracao-02-politicas.html` (`:95,100,105`). A regra existe em `administracao-02-politicas.html:169-179`: `registrar_peca` com `ask` para Worker, `allow` para o regente por delegação, `deny` para sessão de outro projeto; âncora `id="regra-ferramenta-mcp"`. Era a lacuna que se repetia desde a r1. |

## Ressalvas da r3: o que mudou

- Precedência de regras e deny não sobrescritível: fechada (`administracao-02:263-266`).
- Ids entre telas da Mensageria: fechada (P13).
- Verbete "limite de orçamento": fechada (`confronto-decisao.md:240`).
- Filtro do catálogo com "Agente (perfil)": fechada (`administracao-01-catalogo.html:142,196`).

## O que fica aberto

Nada abaixo de 9. Três observações que não baixam nota:

- **`workflow-03` — cartões do resumo.** Somam em curso 2, travada 1, entregue 0 (`:64-66`); a tabela tem 2 tarefas (`:85-101`) e a linha de Worker02 sem tarefa (`:103-109`), com uma em curso, não duas. Marcado "exemplo"; um ajuste de dois dígitos resolve.
- **Cabeçalhos "ciclo 073, rodada 3"** na migalha e no comentário de `administracao-03` (`:8,55`): rótulo desatualizado, sem efeito no conteúdo.
- **`workflow-03:103-109`.** Worker02 numa tabela de "tarefas abertas" como linha toda em "—": coerente com as outras telas, mas não é tarefa.

## Limites do que não li

- Não rodei `verifica-prototipo.py`, `check-conformance.sh` nem `git`. Usei o `qa-report.md:1553-1574` como declaração.
- Li `andamento.md` só por busca. Do `qa-report.md` só a seção da correção 3 (`:1530-1593`).
- Não abri o código de `painel/custo.py`; só confirmei que ele e `fila_outbox.py` existem.
- Da `plataformas.md` li só a linha de orçamento e taxa. A ficha `claude-code.md:59/61` não foi aberta.
- Do confronto, do mapa e do README li por busca. Nas telas li o corpo, não o CSS; sem renderizar.
- Os 12 que estavam em 9 foram amostra por busca. Ignorei `specs/074-*/` e `prototipo/`.

**DIAGNÓSTICO: mudou.** P8, P10, P15 e P16 passaram de 8 para 9; cada pedido foi atendido por uma decisão do Darú (D3 em P8, texto da regente em P8 e P10, D2 em P16, relação 3 em P15). As quatro ressalvas menores também fecharam. Nenhuma peça regrediu na amostra. Resta só um descompasso numérico de exemplo entre cartões e tabela no `workflow-03`.
