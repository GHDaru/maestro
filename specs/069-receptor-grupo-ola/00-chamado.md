---
gate: abertura
tipo: melhoria
escopo: feature
severidade: normal
aberto_por: Gilsiley
origem: chat da Hindiana Assistente, 06/10/2026 (pedido do desenvolvedor do n8n)
data: 2026-10-06 17:40 -0300
autores: Assistente
triado_por: Hindiana Office
---

# 069: receptor HTTPS das mensagens do grupo Ola (n8n → aplicação interna)

Chamado interno do Maestro. Fica ao lado da 068 (chamados pelo WhatsApp, que descarta grupos) e não a substitui.

## Pedido (resumo fiel)

Um endpoint HTTP POST que recebe do n8n as mensagens do grupo Ola (`120363413483485664@g.us`, instância `whatsapp-daru`), em JSON, com:
- `Authorization: Bearer <token>`;
- validação, aceitando `texto` vazio;
- deduplicação por `instancia` + `message_id`;
- resposta 200/202 `{"accepted": true, "message_id": …}`, 400 para dado inválido e 401 para autenticação inválida;
- processamento demorado em segundo plano;
- texto tratado como conteúdo externo, nunca como comando.

Entregáveis: a URL, o token por meio seguro (fora do chat e do código), um exemplo de chamada e resposta, e os limites.

## Respostas do desenvolvedor do n8n (06/10)

- O n8n roda na VM Docker 192.168.15.9, na mesma LAN 192.168.15.0/24 desta máquina (192.168.15.12).
- Ele prefere um certificado válido com a verificação TLS ligada; aceita uma CA própria configurada no ambiente. `Ignore SSL Issues` não serve como definitivo. O domínio `ola-webhook.ghdaru.com.br` pode ser reservado, mas ainda não existe.
- Credencial Header Auth (Bearer); o token é digitado direto na credencial; a rotação se faz trocando só a credencial.
- Proposta dele: timeout de 10 s; até 3 tentativas com 5 s de intervalo, em falha de conexão, timeout e 5xx; 429 com `Retry-After` a combinar; 4xx registrado e sem nova tentativa.
- Só esse grupo e essa instância. O `tipo` é uma string livre e o receptor trata tipos desconhecidos. Sem mídia nesta etapa. `fromMe` vem e deve ser preservado. `data_hora` vem em UTC (Z), com a hora da mensagem. O `remetente` é uma string, não necessariamente um telefone (pode ser LID). `resposta_a` ainda não é enviado. Volume não medido. Basta responder `accepted` + `message_id`.

## Escolhas que eram do Gilsiley, seguidas pelo recomendado (ele pode mudar)

- Processo: este chamado com gates, a Assistente implementa, e a Office registra o GD e despacha crítica + runner2 antes de ligar o n8n de verdade.
- Processamento: só guardar e enfileirar (estado `pendente`), sem resposta ao grupo e sem IA por enquanto.
