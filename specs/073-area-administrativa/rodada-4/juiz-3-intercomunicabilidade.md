# Rodada 4 — Juiz 3: INTERCOMUNICABILIDADE (contexto fresco, 26/10/2026, sobre HEAD 83c386e)

Veredito: **barra não atingida**. 13 ENTRA com tela, mas 21 (mensagem entre agentes: sem tela de
envio), 22 (A2A só "—") e 26 (colisão de termo, não de endereço) cobertos só parcialmente. 25
plataformas com ficha; "analisada" significa documentação lida — só LiteLLM e Claude Code rodaram.

| Peça | Nota | Maior lacuna | Evidência |
|---|---|---|---|
| P1 Inventário de plataformas | 7 | "0 sim em 25" para caixa de entrada e livro é contagem de "—" (nenhuma fonte), e a rodada 1 o chama de "lacuna de mercado" contra a própria legenda; Kiro recebeu "não" com base em página que não cobre inbox; a ficha do Claude Code não investiga o mailbox de agent teams. | `plataformas.md:42,88,90,140,210-213`; `kiro-crew.md:55`; `claude-code.md:16-17,67` |
| P2 Inventário do Maestro | 6 | `SendMessage`/`ListAgents` numa única nota de célula; o fallback por arquivo commitado e a cópia do DONE ao MAESTRO não capturados; o transporte real (harness) fora do inventário; `contatos()` está em `server.py:479`, citado como `:469`. | `inventario-maestro.md:83-88`; `andamento.md:112,139-140` |
| P3 Confronto e decisão | 6 | Os seis ENTRA certos, mas faltam, nem como DEPOIS: recibo de entrega (ack), reentrega, dead-letter, broadcast/cópia, estabilidade de ref após reinício; a referência de roteamento (Windmill, tag de worker group) não é endereçamento por nome; Kiro e Claude Code avaliados com critérios diferentes na precedência. | `confronto-decisao.md:75,77,97,99`; `windmill.md:49,51`; `claude-code.md:70` |
| P4 Lacunas | 6 | Não declara o entregue-ou-não da mensagem nem o ciclo de vida do ref; o DEPOIS de "alertas" empurra o alerta "mensagem desviada" que o ux-design 066 já pedia. | `plataformas.md:222-235`; `confronto-decisao.md:122`; `ux-design.md:79` |
| P5 Mapa de contextos | 6 | Falta o invariante central da Mensageria: endereço ambíguo é recusado, nunca resolvido; as cinco colisões do § 7 são de termo, a dor real é colisão de endereço ("Gerente" em dois projetos, "Hindiana Office" em três refs); o verificador só trava duas das cinco. | `mapa-de-contextos.md:59,287-296`; `README.md:104` |
| P6 mensageria-01 | 5 | Só a idade da mais antiga; cada linha sem carimbo, ref do remetente, projeto; sem contagem de não lidas; mostra só o destinatário resolvido, não pretendido × real — não mostra a mensagem que caiu na caixa errada em 24/10. | `mensageria-01…html:43-69,72-73` |
| P7 mensageria-02 | 5 | Sem hora, id ou ordem verificável; entrega resumida a "drenada", sem ack nem falha; só tags `[[TASK]]`/`[[DONE]]`; cita `tarefas.jsonl` como fonte, que o glossário diz não ser o livro. | `mensageria-02…html:33,38,59-65,84` |
| P8 mensageria-03 | 6 | Recusa a ambiguidade (certo), mas "2 refs" sem listar refs, projeto, vivo/morto; "Gerente → 1 ref → entrega" é exatamente o que falhou; não existe ref obsoleto nem reinício; mistura "Fila" (termo) com endereço e diz "termo tem prioridade", contradizendo a recusa. | `mensageria-03…html:59-75,107` |
| P9 mensageria-04 | 7 | MCP explicado (três ferramentas reais), A2A "—" com motivo; mas o ENTRA 22 tinha lacuna "A2A construído"; nenhuma das três ferramentas MCP envia ou lê mensagem e a tela não diz por onde a mensagem trafega hoje. | `mensageria-04…html:41-65,98-112`; `confronto-decisao.md:73` |
| P10 administracao-catalogo | 8 | Não diz que nomes de skill/agente/modelo são únicos nem que o catálogo alimenta a tabela de roteamento (relação 3 do mapa). | `:63-65,102` |
| P11 administracao-politicas | 8 | Não define o que allow/deny/ask faz com envio de mensagem (quem pode endereçar a quem). | `:67` |
| P12 administracao-orcamento | 8 | Estourar o teto não gera mensagem endereçada a ninguém. | `:122,144` |
| P13 workflow-01 | 6 | Coluna ref sem projeto, sem ref anterior, sem aviso de que o ref muda ao reiniciar; "Gerente" sozinho; "subir" sobre sessão viva não distinguido de reinício. | `:78-82,87-98` |
| P14 workflow-02 | 6 | Sessão só por nome; sem ref nem projeto; "caída" não correlacionada com mensagens a ela endereçadas. | `:70,84` |
| P15 workflow-03 | 6 | Despachante como nome nu; `[[TASK]]` não amarra o destinatário ao ref. | `:84` |
| P16 workflow-04 | 7 | Não lido; nota por amostragem. | — |

## O que muda para 9

- **P1**: "mercado vazio" vira "não encontrado na documentação lida"; Kiro "não" → "—"; ficha do Claude Code com busca explícita por mailbox/agent teams, com URL.
- **P2**: `SendMessage`/`ListAgents` como mecanismos de primeira classe com arquivo:linha ou doc; fallback por arquivo commitado e cópia do DONE; ciclo de vida do ref; revalidar `arquivo:linha`.
- **P3/P4**: acrescentar, ao menos como DEPOIS com gatilho: ack, reentrega, dead-letter, broadcast/cópia, estabilidade de ref; corrigir a base de roteamento (Windmill) e a de colisão (Kiro × Claude Code).
- **P5**: invariante "endereço ambíguo é recusado"; separar colisão de termo de colisão de endereço; regra executável no verificador para o endereço ambíguo.
- **P6**: cada linha com carimbo, ref do remetente, projeto, pretendido × resolvido; contagem de não lidas; linha "chegou aqui, era para outro projeto".
- **P7**: colunas hora, id, ordem; estados enviada, entregue, lida, falhou; fonte real nomeada; mensagens além de tags.
- **P8**: listar refs colidentes com projeto e vivo/morto; caso de duas refs em projetos diferentes; transição "ref mudou no reinício"; remover "Fila" da tabela de endereços.
- **P9**: dizer por qual canal a mensagem trafega hoje e que o MCP não a carrega; mostrar o que o A2A exibiria (agent card, pares) mesmo desabilitado.
- **P13 a P15**: identidade padronizada `nome · ref · projeto` em toda tela que cita uma sessão.
