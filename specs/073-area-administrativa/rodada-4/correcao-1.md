# Rodada 4 — correção 1 (consolidação dos três juízes pela sessão regente, 26/10/2026)

> Três juízes em contexto fresco (controle; administração e gerenciamento; intercomunicabilidade)
> sobre HEAD 83c386e: **barra não atingida** nos três. Nenhuma peça em 9. Os 13 ENTRA têm tela, as
> 25 plataformas têm ficha; o que falta é teor. Esta é a **primeira** rodada de correção; se a
> segunda não mudar o diagnóstico, o laço para e o Darú decide (regra das duas rodadas).
> Pareceres completos: `juiz-1-controle.md`, `juiz-2-administracao-gerenciamento.md`,
> `juiz-3-intercomunicabilidade.md`.

## Decisões da regente (não negociáveis nesta rodada)

1. **Limite de orçamento é da Administração** (define e guarda o teto); o Workflow de sessões só
   mede e exibe o consumo contra o teto. Corrigir o mapa (§ 2, § 6.3, § 6.5) e as citações das telas.
2. **Identidade de sessão é sempre `nome · ref · projeto`**, em toda tela que cite uma sessão, com
   o aviso "o ref muda ao reiniciar" onde houver ação. O verificador ganha a **regra 5**: toda
   menção a sessão (nomes do catálogo: Gerente, WorkerNN, MAESTRO, Office, Assistente) tem de vir
   seguida de ref no formato `[xxxxxx]`, salvo em tabela marcada `data-rotulo="colisão de nomes"`.
3. **Colisão de endereço é diferente de colisão de termo.** O mapa ganha o invariante "endereço
   ambíguo é recusado, nunca resolvido" e uma tabela de colisões de endereço (nome em N refs, nome
   em dois projetos, ref obsoleto após reinício), separada das cinco colisões de termo do § 7.
4. **Entram no confronto, como DEPOIS com gatilho escrito** (não como ENTRA desta rodada): recibo
   de entrega (ack), reentrega, dead-letter, broadcast/cópia, estabilidade de ref, pausar/retomar
   (retomar existe no Claude Code: `claude --resume`; o gatilho é o teto executável), limite de
   taxa, alertas (inclusive "mensagem desviada"). **Entram como ENTRA desta rodada**: auditoria
   administrativa (histórico de mudanças com `changed_by`, como seção nas três telas da
   Administração) e custo estimado em dólar por agente (coluna em `workflow-04`, fonte = tabela de
   preços do modelo no catálogo, marcada "estimado").
5. **Toda ação de escrita diz quem autoriza**: humano (gate), regente por delegação, ou sessão
   dona. O "derrubar" só existe atrás de uma confirmação que mostra tarefa aberta, worktree, o que
   fica salvo e como religar; o Gerente não pode ser derrubado pela tela.
6. **"Não encontrado na documentação lida"** substitui "lacuna de mercado" na leitura da matriz; a
   matriz ganha a distinção "limite que corta" × "alerta que só avisa" como nota de coluna.

## Tarefas por dono (uma rodada; commit "ciclo 073: correção 1 da rodada 4 — <fatia>")

### Worker03 [ad66d6] — Mensageria (P6 a P9 dos juízes 1 e 3)
- `mensageria-01`: cada linha com carimbo, remetente `nome · ref · projeto`, destinatário
  **pretendido × resolvido**, estado (não lida/lida), e uma linha de exemplo "chegou aqui, era para
  outro projeto"; contagem de não lidas; "Drenar outbox" diz quem pode (a sessão dona ou o regente).
- `mensageria-02`: colunas hora, id, ordem; estados enviada/entregue/lida/falhou; fonte real
  nomeada (o livro de mensagens, não `tarefas.jsonl`); mensagens além de tags; quem pode ver o
  livro de outra sessão.
- `mensageria-03`: a tabela de endereços lista os refs colidentes com projeto e vivo/morto; caso
  "Gerente em dois projetos" com RECUSA; caso "ref mudou no reinício" (antigo → novo); "Fila" sai da
  tabela de endereços; confirmação humana antes de entregar a destino não resolvido.
- `mensageria-04`: dizer por qual canal a mensagem trafega hoje (harness `SendMessage`/`ListAgents`,
  fallback por arquivo commitado) e que o MCP não a carrega; mostrar o que o A2A exibiria (agent
  card, pares), mesmo desabilitado; "Registrar status" e "Chamar estado_atual" com quem autoriza.

### Worker04 [4d000a] — Administração (P10 a P12 dos juízes 1 e 2; preâmbulo R8 já em curso)
- `administracao-01-catalogo`: formulário "cadastrar" (mesmo sem executar) com campos do Modelo
  (provedor, preço por milhão de tokens, quem pode usar, por projeto); unicidade de nomes declarada;
  ligação com a tabela de roteamento e com a política; seção "histórico de mudanças" com
  `changed_by`; contagem de agentes com fonte ou "—" com motivo.
- `administracao-02-politicas`: precedência (deny > ask > allow), padrão (default-deny), escopo
  (agente, papel, projeto), quem edita, histórico; fluxo do `ask` até a fila de decisões e o ruling
  humano; ligação com o bloco `permissions` do `settings.json` (Claude Code e Kiro têm ask = sim:
  corrigir as referências); o que allow/deny/ask faz com envio de mensagem.
- `administracao-03-orcamento`: teto por projeto, agente e modelo; unidade (tokens e dólar
  estimado); efeito ao estourar (recusar, avisar, suspender) com quem autoriza; limiar de alerta;
  "consumo corrente" com idade do relógio; a taxa rebaixada formalmente a DEPOIS com motivo;
  histórico de mudanças.

### Worker05 [78d88f] — Workflow de sessões (P13 a P16 dos três juízes)
- `workflow-01`: derrubar só por confirmação (tarefa aberta, worktree, o que fica salvo, como
  religar); botões nas linhas desabilitados; sem "subir" em sessão viva (vira "reiniciar", com
  aviso de ref novo); "subir" com modelo, perfil de agente e worktree (o que o lançador recebe);
  Gerente protegido; identidade `nome · ref · projeto`.
- `workflow-02`: linha com tarefa aberta, modelo e consumo; ações para "bloqueado" (abrir o pedido
  de decisão) e "esperando" (ver a caixa de entrada); alerta de sessão parada com limiar; "caída"
  correlacionada com mensagens endereçadas a ela.
- `workflow-03`: regra de "travada" (limiar de tempo sem DONE); tokens da tarefa; cancelar e
  reatribuir com quem autoriza; declarar que `tarefas.jsonl` parou no ciclo 064.
- `workflow-04`: agente ≠ sessão (uma linha por agente, sessões agrupadas); remover a coluna
  duplicada; custo estimado em dólar (fonte: preço do modelo no catálogo); janela de tempo;
  quebra por modelo; ranking; o teto exibido é o da Administração; declarar o risco de
  subcontagem do piso; trocar OpenRouter por plataforma com ficha.

### Worker02 [31f7bf] — confronto, mapa, verificador (P3, P4, P5; preâmbulo R9 já em curso)
- `confronto-decisao.md`: as decisões 4 acima (DEPOIS com gatilho e os dois ENTRA novos:
  auditoria administrativa e custo estimado); corrigir a base de "roteamento" (Windmill não é
  endereçamento por nome) e a de "colisão" (Kiro × Claude Code com o mesmo critério); pausar/retomar
  justificado como "sem fonte", não "mercado não tem"; contagem ENTRA/NÃO PRECISA/DEPOIS refeita.
- `mapa-de-contextos.md`: decisão 1 (orçamento na Administração: § 2, § 6.3, § 6.5); decisão 3
  (invariante de endereço ambíguo + tabela de colisões de endereço); dono do ponto de execução do
  controle (os hooks e o `settings.json`) e a relação Workflow → Regência (derrubar e ask viram
  pedido de decisão).
- `verifica-prototipo.py`: regra 5 (identidade `nome · ref · projeto`), com mutação e fixture.

### Worker05 e Worker06 — inventário e matriz (P1, P2)
- Worker05: `inventario-maestro.md` com `SendMessage`/`ListAgents` como mecanismos de primeira
  classe, o fallback por arquivo commitado, a cópia do DONE, o ciclo de vida do ref, "allow/ask
  são executáveis no harness" (`claude-code.md:49`), o ledger `tarefas.jsonl` parado no 064, e
  `arquivo:linha` revalidados (`contatos()` em `server.py:479`).
- Worker06: `plataformas.md` com a leitura "não encontrado na documentação lida"; Kiro "não" → "—"
  (`kiro-crew.md:55`); ficha do Claude Code com busca explícita por mailbox/agent teams (URL);
  nota de coluna "corta × avisa" nos limites; fichas de observabilidade com mais fontes ou células
  "sim" apoiadas em marketing rebaixadas a "parcial".

### Worker01 [9a1b27] — README e glossário
- README do protótipo: tabela de identidade (`nome · ref · projeto`), as duas tabelas de colisão
  (termo × endereço), os dois ENTRA novos, a navegação; glossário: "colisão de endereço" e "ref de
  sessão" como termos (inglês, Cycle 073).

## Depois da correção
Gerente integra, roda o verificador (11 telas, 0 achados, regra 5 incluída), conformance 073 nos
dois modos, e manda `[[DONE 073-correcao-1]]` para "MAESTRO [7c8d05]". Os três juízes voltam em
contexto fresco sobre o novo HEAD. Se alguma peça seguir abaixo de 9 com o mesmo diagnóstico pela
segunda vez, o laço para e o Darú decide.
