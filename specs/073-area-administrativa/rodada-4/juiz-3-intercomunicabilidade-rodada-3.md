# Rodada 4 — Juiz 3: INTERCOMUNICABILIDADE — terceira leitura (contexto fresco, 27/10/2026, sobre HEAD 4e421a4)

## Veredito

**Barra atingida na dimensão INTERCOMUNICABILIDADE: as 16 peças ficam em 9.**

Todos os pedidos de "O que ainda falta para 9" da rodada 2 foram atendidos nos arquivos do HEAD. As peças que já estavam em 9 não regrediram. Os pedidos eram de consistência, e todos foram fechados:
- citações `arquivo:linha` revalidadas;
- roster único e ref único por nome;
- livro de mensagens na ordem do título;
- Windmill fora do roteamento;
- aviso do teto endereçado;
- agente separado de sessão.

O que sobra são resíduos de 8 a 9 que não decidem a nota. Estão listados abaixo, para o regente ver o que é cosmético. Nenhum é lacuna de desenho.

Regra 6 em `prototipo/verifica-prototipo.py`:
- **Roster.** `ROSTER` está em `:143-152` com os oito nomes e refs que a regente fixou.
- **Cada menção.** `record_identity` (`:365-373`) acusa nome do roster com ref diferente.
- **Por tela.** `finish()` (`:375-387`) acusa um ref colado a mais de um nome, e `main` o chama por tela (`:401`).
- **Cerca.** Roda onde a regra 5 roda, nos nós de texto e nos atributos (`:251-253`, `:289-290`, `:324-325`). A isenção é só a tabela `data-rotulo="colisão de nomes"` (`identity_exempt`, `:225-232`). A marca `data-exemplo` não isenta.
- **Fixture e mutação.** O `qa-report.md:1429-1529` registra a fixture boa (0 achados) e a ruim (`Worker05 [4d000a]` e `Office`/`Assistente` no mesmo `[b7e3a2]`). A mutação mostra 9 achados com a regra viva e 7 com ela cega, e os 2 que somem são os da regra 6. A prova no corpus pré-correção dá 28 achados contra 0 no HEAD. Eu não reexecutei nada disso; li o script e o relatório.
- **Ambiguidade de endereço.** A não verificação por script está declarada em `qa-report.md:1521-1524`, `mapa-de-contextos.md:400-403` (§ 8) e `prototipo/README.md:167-169`. Pela decisão da regente, isso vale como fechado.

## Tabela

| Peça | Nota r2 | Nota r3 | Pedido da r2 | Fechado? | Evidência |
|---|---|---|---|---|---|
| P1 `plataformas.md`, `claude-code.md`, `kiro-crew.md` | 8 | 9 | Reescrever `plataformas.md:155` e `:227-228` como "não encontrado na documentação lida"; revalidar linhas das fichas | Sim | `plataformas.md:164` e `:238-240` agora dizem "não encontrado na documentação lida", e a contagem é de `sim`. Caixa de entrada com `parcial` para Claude Code e Maestri (`:88`). A2A com 5 `sim` (`:87`, `:242`). A ficha do Claude Code tem mailbox, inbox socket e `crossSessionInbound` em `claude-code.md:40-53,81,84,94-99`. Tabela da ficha: retomar `:61`, allow/ask `:63`, mensagem `:79`, roteamento `:82`, colisão `:84`. |
| P2 `inventario-maestro.md` | 8 | 9 | Refazer citações `:48,50,87,90`; citar mailbox JSON e `crossSessionInbound` como transporte real | Sim | `inventario-maestro.md:53` (`claude-code.md:61`), `:55` (`:63`), `:92` (`:79,82,88` e `:40-53`, mais fallback e cópia do DONE), `:95` (`:82`), `:112` (`:61`). Todas batem com a ficha. Ref que muda no reinício em `:95`. "Limites" em `:124-141`: ledger parado no 064, ponto de execução, derrubar, somente leitura. |
| P3 `confronto-decisao.md` | 8 | 9 | Corrigir citações `:49,86,88,96,102`; título "(6)" × 5 linhas | Sim | Citações em `:57,94,96,104,110,173` apontam para `:61`, `:82` e `:84`, corretas. Título `ACRESCENTADAS NA CORREÇÃO 1 (5)` em `:112`, com 5 linhas (`:118-121`). Totais 16/5/11 = 32 em `:186-202`. |
| P4 Lacunas declaradas | 8 | 9 | Tirar "mensagem desviada" de `alertas`; declarar o DEPOIS real | Sim | `confronto-decisao.md:182` ("a peça é a notificação ativa"; a mensagem desviada "sai daqui", já tem tela). "Limites" em `:266-281`: ponto de execução, ledger parado no 064, somente leitura. Ack, reentrega, dead-letter e broadcast com gatilho em `:118-121,180`. |
| P5 `mapa-de-contextos.md` | 8 | 9 | Alinhar `:353` com `mensageria-03:75`; regra do endereço ambíguo ou declarar a não verificação | Sim, pela decisão 1 | O mapa `:358` recusa o ref morto e oferece o ref novo. `mensageria-03:77` diz "RECUSA e oferece a ref nova", então a divergência acabou. A não verificação está declarada em § 8 (`:400-403`). A relação 6 do núcleo compartilhado está em `:246` (era 5). |
| P6 `mensageria-01` | 8 | 9 | Padronizar roster; remetente diferente do destinatário na linha de desvio; coluna id | Sim | Coluna id em `:47`. Refs do roster em `:60,68,76,84` (`Worker05 [78d88f]`, `Gerente [31ee4d]`, `Worker06 [c85948]`, `Worker03 [ad66d6]`). Desvio por colisão: `Worker06` envia a `Office [b7e3a2]`, com 2 refs listados e "resolvido: nenhum" (`:76-77`). Desvio de projeto em `:84-85`. |
| P7 `mensageria-02` | 7 | 9 | Inverter a ordem ou mudar o título; sem `[9a1b27]` duplicado | Sim | Título "da mais antiga à mais nova" (`:36,47`). Linhas 07:05 → 09:14 e ordem 8 → 12 (`:65-117`). `Worker01 [9a1b27]` aparece uma vez (`:81`) e `Worker03 [ad66d6]` nas demais. Acrescentou tarefa derivada de `[[TASK]]` (`:55`), custo "— (ledger parado no 064)" (`:59`) e leitura restrita ao projeto (`:124`). |
| P8 `mensageria-03` | 8 | 9 | Tirar Windmill; decidir recusa × confirmação; nome nu na coluna "pretendido" | Sim | Nenhum Windmill na tela. A referência é Claude Code com `SendMessage`/`ListAgents` (`:35-36,124-127`) e Kiro × Claude Code na colisão (`:126-127`). Coluna "nome pretendido (nu, digitado)" (`:49,57,63,69,75`) e refs na coluna ao lado (`:50`). Ref morto: "RECUSA e oferece a ref nova" (`:76-78`). Isenção pela cerca declarada na tela (`:45`). |
| P9 `mensageria-04` | 9 | 9 | Nota extra: inbox socket e recusa do harness | Mantida | Canal real, fallback, outbox e MCP "não carrega mensagem" (`:41-76`). A2A com 5 `sim` (`:169`, confere com `plataformas.md:87`). `registrar_peca` com "quem autoriza" (`:166-168`). A nota extra da r2 era opcional e continua sem a tela citar o inbox socket. |
| P10 `administracao-01-catalogo` | 9 | 9 | — | Mantida | Nomes únicos e a ligação com `mensageria-03` em `:226-239`. Identidade em `:218-220`. |
| P11 `administracao-02-politicas` | 9 | 9 | — | Mantida | allow/deny/ask sobre o envio de mensagem em `:297-310`. |
| P12 `administracao-03-orcamento` | 8 | 9 | Dizer para quem vai o aviso do teto, ou apagar `administracao-02:289-290` | Sim | `administracao-03:112-116`: o aviso é mensagem endereçada à sessão dona (`nome · ref · projeto`) e a `MAESTRO [7c8d05] · 410_MAESTRO`, pela Mensageria (`mensageria-02`). Recusar e suspender viram DEPOIS (`:117-121`). A frase de `administracao-02:306-308` agora é verdadeira. |
| P13 `workflow-01` | 9 | 9 | — | Mantida | Identidade `nome · ref · projeto` em `:99,108,117`. "Reiniciar" com ref novo em `:154-158`. Derrubar distingue `claude stop` de `claude rm` (`:167`, bate com `claude-code.md:59`) e passa pelo pedido de decisão da Regência (`:169`). |
| P14 `workflow-02` | 9 | 9 | — | Mantida | Identidade em `:87,96,105,114`. Citações `claude-code.md:79` e `:79,82` (`:102,120`) estão corretas. Alerta como mensagem endereçada, com ref relido (`:129`). "Reiniciar a sessão" desabilitado e apontando para `workflow-01` (`:133-135`). |
| P15 `workflow-03` | 9 | 9 | — | Mantida | Destinatário e despachante em `nome · ref · projeto` (`:85-103`), incluindo `MAESTRO [7c8d05]`. O `[[TASK]]` amarra o ref lido (`:113`). Cancelar mostra o que se perde (`:130`). |
| P16 `workflow-04` | 8 | 9 | Separar agente de sessão: linha do agente sem ref | Sim | Coluna "agente (perfil)" com `dev-implementer (agente — perfil, sem ref)` (`:97,106,118,129`) e sessões `nome · ref · projeto` na coluna ao lado (`:109-110,121,132`). O reinício aparece como `Worker05 [78d88f] → [c4d5e6]`. Cartão "teto vigente" reconciliado com a seção "teto" (`:86-89,165-170`). |

## O que fica aberto

Nenhuma peça ficou abaixo de 9, então não há falta de desenho nem decisão de produto pendente para levar ao Darú nesta dimensão. Há quatro resíduos que não mudam a nota; ficam registrados para quem quiser limpar:

1. **Roster × reinício entre telas.** `mensageria-03:76` mostra `Worker01 [9a1b27]` como ref morto, enquanto `mensageria-02:81` o mostra vivo. O roster é declarado como dado de exemplo de 26/10, e a regra 6 é por tela. O efeito é só leitura cruzada de exemplos, não contradição dentro de uma tela.
2. **Contagem do rodapé do confronto.** `confronto-decisao.md:193` ainda diz "26 da tabela fixa + 6 acrescentadas", e o título da seção diz (5). A conta fecha em 32 (a sexta é a taxa, na tabela principal), mas a explicação ficou implícita.
3. **Efeito "recusar" nas linhas da tabela de tetos.** `administracao-03:146-166` ainda lista "avisar · recusar · suspender" como efeitos por linha. A caixa de cima (`:117-121`) já os declara DEPOIS. É redação, não contradição de endereço.
4. **Ligação ref antigo → recusa.** `workflow-01:156` diz que o ref antigo "deixa de resolver", mas não aponta para a recusa de `mensageria-03:76-78`. Já era resíduo na r2, quando P13 estava em 9.

A ambiguidade de endereço continua sem verificação por script. É decisão fixa da regente (decisão 1), está declarada no README, no mapa § 8 e no `qa-report`, e fica coberta só pela leitura fresca. Se um dia for decisão de produto virar fitness function, isso é novo escopo.

## Limites do que não li

- **Não reexecutei** `verifica-prototipo.py`, a mutação nem os scripts de conformance. Os números (11 telas, 0 achados, 9 contra 7 achados na mutação, 28 contra 0 no corpus anterior) vêm do `qa-report.md:1429-1529` e do `andamento.md`.
- **Li inteiros:** `juiz-3-...-rodada-2.md`, `correcao-2.md`, `verifica-prototipo.py`, `mensageria-01`, `02` e `03`. Também li `mensageria-04` e `administracao-03` a partir da linha 28, e `workflow-04` a partir da linha 50.
- **Li em parte:** `workflow-01` (85-192), `workflow-02` (75-160), `workflow-03` (65-152), `inventario-maestro.md` (86-155), `mapa-de-contextos.md` (225-406) e `claude-code.md` (36-100). As seções 1 a 5 do mapa não foram lidas, então não conferi a correção da linha `:89-90`, só a relação 6 e o § 8.
- **Só por busca de trechos:** `administracao-01` e `administracao-02`, `confronto-decisao.md`, `plataformas.md` e `prototipo/README.md`.
- **Não li:** `kiro-crew.md`, `fixtures/tela-bom.html` e `tela-ruim.html`, `done-073-correcao-2.md` (não consta no diretório; usei `andamento.md` e o `qa-report`), o glossário e as outras 23 fichas. As 25 plataformas não foram reavaliadas uma a uma.
- **No código só conferi** `contatos()` (`painel/server.py:479`), `norm_sessao` (`painel/ingest.py:199`) e a existência de `sessao_destino` em `painel/fila_outbox.py` (`:52,103,131,148-152`).

DIAGNÓSTICO: mudou. Na rodada 2 as lacunas eram de consistência, com citações defasadas, refs de exemplo contraditórios, ordem do livro e referência cruzada pendente. Na rodada 3 todas estão fechadas, e o que sobra são quatro resíduos de redação sem efeito sobre a nota.
