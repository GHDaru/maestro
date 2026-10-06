---
gate: abertura
tipo: melhoria
escopo: feature
severidade: normal
aberto_por: Gilsiley
origem: chat da Hindiana Assistente, 06/10/2026
data: 2026-10-06 13:30 -0300
autores:
triado_por: Hindiana Office
---

# 068: chamados pelo WhatsApp (Evolution/n8n), com retorno ao cliente em cada etapa

Chamado interno do Maestro, não do produto Hindiana.

## Pedido (Gilsiley, 06/10)

> "Aqui, vamos criar um webhook que o n8n ou o evolution irá passar para nossa aplicação que está na rede interna. De forma que padronizemos a um repositório para os 'chamados' e desenhos o fluxo que devolverá para o whats o acompanha para o 'cliente' em cada gate."

Decisões dele no mesmo chat: repositório próprio `chamados`; só números cadastrados abrem chamado; o cliente responde pelo WhatsApp no G0, no G1 e no G7; a rede enxerga nos dois sentidos.

Spec, ADR, plan e tasks estão nesta pasta. O G1 é de feature, com 2 críticos (W06 em segurança e dados, W11 em fluxo e texto), despachados pela Office em 06/10. Nesta pasta vale o padrão do chamado sobre a regra dos 4 arquivos do Spec Kit.
