# Decisions: Receptor do grupo Ola

## ADR-001: CA própria na LAN agora, com certificado público pelo DNS do Cloudflare como evolução

### Context
O n8n (192.168.15.9) e o receptor (192.168.15.12) estão na mesma LAN. O desenvolvedor do n8n quer a verificação TLS ligada, sem `Ignore SSL Issues`, e aceita uma CA própria configurada no ambiente. O domínio `ola-webhook.ghdaru.com.br` pode ser reservado no Cloudflare, mas ainda não existe.

### Options considered
1. **CA própria ("Maestro LAN CA")**: a CA assina o certificado do receptor com SAN de IP e de DNS. O n8n confia na CA por `NODE_EXTRA_CA_CERTS`.
   - Prós: funciona hoje e não depende de terceiros nem de token do Cloudflare.
   - Contras: é preciso configurar a CA no container e renovar a cada 1 ano.
2. **Certificado público (Let's Encrypt, desafio DNS-01 no Cloudflare)** para `ola-webhook.ghdaru.com.br`, com registro A para o IP interno.
   - Prós: confiável em qualquer cliente, sem configurar CA.
   - Contras: exige token de API do Cloudflare nesta máquina e um cliente ACME; expõe no DNS público um IP privado; renovação a cada 90 dias.
3. **HTTP simples na LAN**.
   - Contras: o requisito pede HTTPS e o token iria em claro na rede doméstica.

### Decision
Escolhemos a **CA própria** porque atende o requisito do desenvolvedor (TLS verificado) hoje, sem segredo novo de terceiros. O certificado já leva o SAN `ola-webhook.ghdaru.com.br`: quando o domínio for criado, migrar para a opção 2 não muda a URL.

### Consequences
- **Boa:** TLS verificado desde o primeiro dia.
- **Boa:** a chave privada da CA e a do servidor ficam fora do git (`painel/dados/tls/`).
- **Ruim:** o n8n precisa montar `maestro-lan-ca.crt` no container e reiniciar.
- **Ruim:** a URL por IP depende de o IP 192.168.15.12 não mudar; é preciso reservar o IP no roteador.
