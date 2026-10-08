# Servidor de Entrada — Chamados pelo WhatsApp (068)

Serviço HTTP na rede interna que recebe webhooks do n8n (Evolution API),
valida assinatura HMAC-SHA256, conduz a conversa de abertura e cria
chamados no repositório.

## Configuração

Variáveis de ambiente (Windows: `setx`):

| Variável | Descrição |
|---|---|
| `MAESTRO_WEBHOOK_SEGREDO` | Segredo HMAC atual (obrigatória) |
| `MAESTRO_WEBHOOK_SEGREDO.ANTERIOR` | Segredo HMAC anterior (opcional, para rotação) |
| `MAESTRO_ENTRADA_DB` | Caminho do banco `entrada.db` (default: `painel/dados/entrada.db`) |

Configuração em `painel/projetos/hindiana.json`, bloco `entrada`:

```json
{
  "ip": "127.0.0.1",
  "porta": 8790,
  "ips_n8n": ["10.0.0.50"],
  "segredo_env": "MAESTRO_WEBHOOK_SEGREDO"
}
```

## Rotação do segredo HMAC (NFR-008)

A aplicação aceita dois segredos ao mesmo tempo — o atual e o anterior —
para trocar o segredo sem parar a entrada.

**Procedimento de troca:**

1. **Pôr o novo como atual e o velho como anterior:**
   ```
   setx MAESTRO_WEBHOOK_SEGREDO <novo_segredo>
   setx "MAESTRO_WEBHOOK_SEGREDO.ANTERIOR" <segredo_atual>
   ```
2. **Reiniciar o serviço.**
3. **Trocar no n8n** (workflow de saída) para o novo segredo.
4. **Aguardar 24 h** sem chamada assinada com o velho (contado no log).
5. **Apagar o anterior:**
   ```
   setx "MAESTRO_WEBHOOK_SEGREDO.ANTERIOR" ""
   ```
6. **Reiniciar o serviço.**

A aplicação assina a saída só com o segredo atual. O log registra qual
dos dois validou (`atual` ou `anterior`), sem o valor do segredo.

## Ferramenta de contatos (P4)

```
python painel/entrada/contatos.py add --telefone 55... --nome "Mauricio" --empresa "Neogrid"
python painel/entrada/contatos.py list
python painel/entrada/contatos.py rm c-0001
```

O telefone nunca entra no repositório git — fica em `dados/entrada.db`,
fora do `.gitignore`.

## Segurança

- HMAC-SHA256 com `hmac.compare_digest` (não vaza timing)
- Janela de 5 min no horário do evento
- Lista de IPs permitidos (só o n8n)
- `evento_id` lembrado por 7 dias (idempotência)
- Logs só com metadados (NFR-011): horário, rota, evento_id, contato,
  status HTTP, duração. Nunca o texto, o telefone ou o segredo.
