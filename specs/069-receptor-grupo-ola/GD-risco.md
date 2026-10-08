---
gate: GD
papel: risco
objeto: specs/069-receptor-grupo-ola/spec.md @ fbdd9be
veredito: C
por: Hindiana Office
data: 2026-10-08 13:02 -0300
data_objeto: 2026-10-06 17:41:47 -0300
---

# GD: classe de risco do chamado 069 (receptor do grupo Ola)

**Classe: C.**

O receptor é tooling interno do Maestro, só na LAN, sem resposta ao grupo e sem IA. Por isso a Assistente sugeriu a classe B. Mesmo assim fica em C, porque guarda as mensagens do grupo do cliente com o nome e o número de quem participa (spec, linha 62, e NFR-008). Isso cai nas mesmas duas decisões de LGPD que fizeram a 068 subir para C (maestro 09461a2):
- a base legal para tratar esse dado (art. 7º);
- o prazo de retenção e a base dele (art. 16). O NFR-008 diz "90 dias, a confirmar com o Gilsiley junto da 068".

As duas são do Gilsiley, como controlador.

## Fatos de método

- A spec (fbdd9be), o vermelho (e08ef31) e o verde (70123d6) foram feitos pela mesma autora em dois minutos, entre 17:41 e 17:43 de 06/10. Isso foi antes deste GD e antes de qualquer G1.
- O pacote de implantação (28fecbc e 8b516c3) e o pedido ao especialista também vieram antes da GD. Não houve implantação: o LXC ainda não existe, e o código foi só copiado para o painel local, desligado.
- A Assistente confirmou em 08/10, às 13:01, que o receptor nunca foi ligado: não há processo, nada escuta na porta 8793, e o token e a regra de firewall não foram criados. Ela registrou o desvio como próprio e aceitou as quatro condições.

## Condições (obrigatórias)

1. **O G1 tem 2 críticos que não são a autora:** W06 para segurança, LGPD e TLS com CA própria, e um segundo para o fluxo com o n8n. As bases legais entram como pendentes do Gilsiley, como na 068.
2. **O G3 tem crítica de código por não autor e runner2 por não autor**, em clone limpo, com 0 failed e 0 errors.
3. **Nenhum segredo em repositório.** Isso vale para o token do n8n e para a chave privada da CA e do certificado (dados/tls). A configuração e os endereços são do Gilsiley.
4. **Ligar o receptor exige ordem escrita do Gilsiley**, registrada em G8-ordem.md, depois das bases legais e dos gates 1 e 3. Ligar aqui é gerar o token, liberar o firewall e o n8n passar a enviar. Até lá, só mensagens de teste.
