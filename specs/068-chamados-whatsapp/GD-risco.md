---
gate: GD
papel: risco
objeto: specs/068-chamados-whatsapp/spec.md @ 4d62287
veredito: B
por: Hindiana Office
data: 2026-10-06 13:49 -0300
data_objeto: 2026-10-06 13:46:43 -0300
---

# GD: classe de risco do chamado 068 (chamados pelo WhatsApp)

**Classe: B.** Tooling interno do Maestro, reversível, que não toca o código nem o banco do produto hindiana nem a produção.

Por que não é A:
- passa a guardar dado pessoal do cliente (telefone e conteúdo das mensagens) num repositório e num serviço nossos;
- abre um endpoint na rede interna chamado pelo n8n e pelo Evolution, com HMAC, lista de IPs e janela de 5 minutos;
- envia mensagens automáticas a clientes reais.

Por que não é C:
- o Gilsiley já decidiu os pontos estruturais na própria spec: repositório próprio, só números cadastrados, respostas em três pontos e rede nos dois sentidos;
- não há divergência do Excel nem efeito no produto.

Condições da classe B (obrigatórias):
1. O G1 tem 2 críticos: W06 (segurança, LGPD: retenção, quem lê, nada de telefone ou mensagem no git) e W11 (fluxo e texto ao cliente).
2. Nenhum segredo (chave do HMAC, credenciais do n8n e do Evolution) em repositório. A configuração e os endereços internos ficam com o Gilsiley.
3. A **primeira mensagem real a um cliente** (go-live do orquestrador) exige ordem escrita do Gilsiley, registrada em G8-ordem.md. Até lá, só números de teste.
4. Retenção e apagamento do dado do cliente definidos na spec antes do G1 passar. Se a crítica do W06 achar lacuna de LGPD que só o Gilsiley pode decidir, a classe sobe para C.
