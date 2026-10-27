# Rodada 4 — Juiz 3: INTERCOMUNICABILIDADE — quarta leitura, regressão (contexto fresco, 27/10/2026, sobre HEAD 1bbf171)

## Veredito

**Barra mantida: as 16 peças seguem em 9. Nenhuma regrediu.**

A correção 3 trouxe o aviso de teto, o ponteiro MCP → política e a igualdade de ids entre caixa e livro. Os três pontos entraram sem quebrar a identidade `nome · ref · projeto`, o roster, a ordem do livro nem o invariante do endereço ambíguo.

- **Identidade e roster.** Cruzei todas as menções `Nome [ref]` das 11 telas. Cada nome tem um ref só: Worker05 `[78d88f]`, Worker03 `[ad66d6]`, Worker06 `[c85948]`, Worker04 `[4d000a]`, Gerente `[31ee4d]`, MAESTRO `[7c8d05]`, Office `[b7e3a2]` e `[c9f1d4]`.
- **Worker02.** `Worker02 [31f7bf] · 410_MAESTRO` nas quatro telas do Workflow (`workflow-01:117`, `-02:116`, `-03:103`, `-04:132`); nas outras sete não aparece.
- **Ids e remetentes iguais.** Caixa e livro têm as mesmas seis linhas, `msg-0413` a `msg-0418`; remetentes, destinatários e horas batem uma a uma. A caixa vai da mais nova à mais antiga e o livro da mais antiga à mais nova, declarado em cada tela (`mensageria-01:36`, `mensageria-02:36-37`).
- **Estados de entrega.** O livro mostra o transporte (entregue ou falhou) e a caixa a leitura (lida ou não lida); `mensageria-02:136` mantém a separação.
- **Aviso de teto.** `msg-0418` é a mesma mensagem nas duas telas (`mensageria-01:59-64`, `mensageria-02:122-129`): destinatários `Worker03 [ad66d6] · 410_MAESTRO` e `MAESTRO [7c8d05] · 410_MAESTRO (regente)`; remetente "painel · ingestão de consumo (painel/custo.py)", com `data-fonte` no módulo; o emissor não é uma sessão e a tela diz isso (`mensageria-02:126,137`). `workflow-04:171` e `administracao-03:113-114,229-241` falam o mesmo.
- **Ponteiro MCP → política.** `administracao-02:169-178` tem a regra com a âncora `#regra-ferramenta-mcp`, e `mensageria-04:88-110` aponta para ela em cada ferramenta; "não duplica a regra, só aponta" (`:105,110`); `ask` para Worker, `allow` para o regente por delegação e `deny` para sessão de outro projeto nas duas telas.
- **Endereço ambíguo.** `mensageria-03:37-39` mantém "recusado, nunca resolvido" e "oferece a ref nova"; `msg-0415` mostra `nenhum — colisão de endereço`; a isenção `data-rotulo="colisão de nomes"` segue em `:45`.
- **Relação 3, caminho de volta.** `mensageria-03:85-86` aponta para o catálogo, seção "Agentes (perfis)".

## Tabela

| Peça | Nota r3 | Nota r4 | Mudou na correção 3? | Regrediu? | Evidência |
|---|---|---|---|---|---|
| P1 `plataformas.md`, `claude-code.md`, `kiro-crew.md` | 9 | 9 | Sim (marca `corta`/`avisa`; ficha corrigida) | Não | Não reli as fichas; `qa-report` e `andamento` dizem que nenhum símbolo da matriz mudou. |
| P2 `inventario-maestro.md` | 9 | 9 | Não confirmado | Não | Não reconferi as citações do inventário após a mudança de `claude-code.md:59/:61`. |
| P3 `confronto-decisao.md` | 9 | 9 | Sim (D1, D2, D3) | Não | `:211` 32 = 26 + 6 e `:216,220` 16 + 5 + 11 = 32 íntegros. |
| P4 Lacunas declaradas | 9 | 9 | Sim (ENTRA 4 reescrito) | Não | "Efeito de hoje = avisar" bate com `administracao-03:135,148`; o corte continua DEPOIS. |
| P5 `mapa-de-contextos.md` | 9 | 9 | Sim (§ 6.5) | Não | Só pelo `andamento.md:122`; relação 3 coerente com `mensageria-03:86`. |
| P6 `mensageria-01` | 9 | 9 | Sim | Não | Ids e remetentes iguais ao livro (`:59-104`); caixa "De onde vêm os nomes" e linha de aviso. |
| P7 `mensageria-02` | 9 | 9 | Sim | Não | Ordem 8 → 13 com horas crescentes (`:66-123`); aviso `msg-0418`; leitura restrita ao projeto; nota em `:137`. |
| P8 `mensageria-03` | 9 | 9 | Sim (nota da relação 3) | Não | Recusa e ref novo (`:37-39`); tabela de colisão isenta; sem Windmill. |
| P9 `mensageria-04` | 9 | 9 | Sim (coluna de política MCP) | Não | `:88-110`; aponta, não duplica. |
| P10 `administracao-01-catalogo` | 9 | 9 | Sim ("Agente (perfil)") | Não | `:221` `Worker04 [4d000a]`, igual a `administracao-02:349` e `administracao-03:190`. |
| P11 `administracao-02-politicas` | 9 | 9 | Sim (regra MCP) | Não | `:169-178`, âncora `#regra-ferramenta-mcp`. |
| P12 `administracao-03-orcamento` | 9 | 9 | Sim ("Quem emite o aviso") | Não | `:113-114`, `:226-245`; recusar e suspender DEPOIS por linha (`:148,158,168`). |
| P13 `workflow-01` | 9 | 9 | Sim (Worker02, `stop` × `rm`) | Não | `:117`; reiniciar com ref novo em `:156-157`. |
| P14 `workflow-02` | 9 | 9 | Sim (cartão "caída") | Não | `:116` Worker02 igual ao `workflow-01`. |
| P15 `workflow-03` | 9 | 9 | Sim (`data-fonte` do ledger) | Não | `:103`; `MAESTRO [7c8d05]` em `:96`. |
| P16 `workflow-04` | 9 | 9 | Sim (linha do aviso) | Não | `:171` aviso para `Worker05 [78d88f]` e `MAESTRO [7c8d05]`; Worker02 em `:132`. |

## Os quatro resíduos da r3

1. Roster × reinício entre telas: não tocado, cosmético (o Worker01 saiu do livro; a leitura cruzada ficou mais leve).
2. Rodapé do confronto (26 + 6): fechado (`confronto-decisao.md:211,216,220`).
3. "Recusar" nas linhas da tabela de tetos: fechado (`administracao-03:148,158,168`).
4. Ref antigo → recusa em `workflow-01:156`: não tocado, cosmético.

## O que fica aberto

Nenhuma peça abaixo de 9. Observação, não falha: o remetente do `msg-0418` é um emissor de sistema, não `nome · ref · projeto`; está declarado com `data-fonte`. Se o verificador precisar conhecer "emissor de sistema" como categoria, é escopo novo.

## Limites do que não li

- Não reexecutei o verificador, a mutação nem o conformance ("11 telas, 0 achados" vem do `andamento.md:123,135`).
- Li o parecer da r3, `correcao-3.md`, `andamento.md:105-164`, `mensageria-01` (30-129), `mensageria-02` (30-157), `mensageria-03:28-58`. Por busca: `mensageria-04`, `administracao-01/02/03`, `workflow-01/04`; nas 11 telas a lista cruzada de `Nome [ref]`.
- Não li `plataformas.md`, `claude-code.md`, `kiro-crew.md`, `inventario-maestro.md`, `mapa-de-contextos.md`, o README, o glossário nem o diff dos commits. Não conferi `painel/custo.py`.

DIAGNÓSTICO: manteve. A correção 3 mexeu em 13 peças e acrescentou o aviso de teto, o ponteiro MCP e a igualdade caixa × livro sem regressão de intercomunicabilidade. Das 16 peças, 16 seguem em 9. Dos quatro resíduos da r3, dois foram fechados e dois seguem como redação cosmética.
