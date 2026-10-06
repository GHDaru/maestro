# Plan: Receptor do grupo Ola

**Feature Branch**: `069-receptor-grupo-ola` · **Spec**: `/specs/069-receptor-grupo-ola/spec.md`

## Summary
Um servidor HTTPS da biblioteca padrão, `painel/receptor_ola.py`, com uma rota POST. Ele valida IP, Bearer, tamanho, frequência e JSON, grava no SQLite com deduplicação pela chave primária, responde 202 ou 200 e enfileira numa thread. O script `painel/tls_lan.py` gera a CA e o certificado.

## Technical Context (repo scan)
- Python 3.12, só biblioteca padrão (`http.server`, `ssl`, `sqlite3`, `hmac`, `json`), como o painel. O `cryptography` 50 já está instalado e serve só para gerar a CA e o certificado.
- Arquivos: `painel/receptor_ola.py`, `painel/tls_lan.py`, `painel/tests/test_receptor_ola.py`. A configuração fica em `projetos/hindiana.json`, na chave `receptor_ola`.

## Approach
1. `tls_lan.py` gera, em `painel/dados/tls/`, a CA (10 anos), o certificado do servidor (1 ano, SAN de IP e DNS) e o `maestro-lan-ca.crt`, que é público e vai para o n8n.
2. `receptor_ola.py` faz a validação na ordem IP → tamanho → frequência → Bearer → JSON → campos → listas permitidas. Depois `INSERT OR IGNORE`: se gravou responde 202, senão 200 duplicada. Uma fila em memória e uma thread marcam `enfileirada`.
3. O token é lido de `OLA_WEBHOOK_TOKEN` (e `_ANTERIOR`) no ambiente do usuário Windows ao iniciar.

## Interfaces / APIs
`POST /webhook/ola/mensagens` e `GET /saude`. Os status e os corpos estão na FR-004 da spec.

## Data Model
Banco `painel/dados/ola_grupo.db`, tabela `mensagens`:
- chave primária (`instancia`, `message_id`);
- colunas `grupo`, `remetente`, `nome`, `texto`, `tipo`, `from_me`, `data_hora`, `recebido_em`, `estado` (`pendente`, `enfileirada`) e `bruto` (JSON).

## Security/privacy
- Bearer com `compare_digest` e dois tokens na rotação.
- Lista de IPs, bind só no IP da LAN, TLS da CA própria.
- O log não leva texto, nome, remetente nem token.
- O dado fica fora do git, com retenção de 90 dias (default).
- O texto nunca é interpretado.

## Observability
Log JSON por linha em `painel/dados/logs/receptor-ola-AAAAMMDD.log`. O `/saude` só diz se o serviço está no ar.

## Test strategy
`unittest` sobe o servidor numa porta livre com TLS e CA de teste e chama via `http.client`. Um teste por cenário:
- P1.1–P1.4;
- P2.1–P2.5;
- P3.1;
- log sem texto e sem token.

## Rollout
1. Gerar a CA e o certificado.
2. O Gilsiley gera o token na variável de ambiente e o digita na credencial do n8n.
3. O Gilsiley libera o firewall, porta 8793, origem 192.168.15.9.
4. Subir o receptor.
5. O n8n monta a CA e cria o nó com timeout de 10 s e 3 tentativas.
6. Chamada real: 202 e repetição 200.

## Risks + mitigations
- **IP muda (DHCP):** reservar o IP no roteador ou migrar para o DNS (ADR-001).
- **Receptor parado:** o n8n registra a falha (4xx/5xx). Tarefa agendada ao logon (com ok do Gilsiley).
- **Volume desconhecido:** limite de 120/min com 429 e `Retry-After`; medir na primeira semana.
