# Tasks: Receptor do grupo Ola

## P1 — Entrega e deduplicação
- [ ] T1-01 [Verify] Testes vermelhos de P1.1 a P1.4 (202 novo, 200 duplicada, texto vazio, tipo desconhecido)
- [ ] T1-02 [Impl] `painel/receptor_ola.py`: rota, validação, SQLite com `INSERT OR IGNORE`, fila e thread
## P2 — Entrada fechada
- [ ] T2-01 [Verify] Testes vermelhos de P2.1 a P2.5 (401, 400 por campo, 403 de IP, 429 com Retry-After, 413)
- [ ] T2-02 [Impl] Bearer com compare_digest e dois tokens, lista de IPs, limite de frequência, limite de tamanho
## P3 — Texto é dado
- [ ] T3-01 [Verify] Teste: texto com "comando" é guardado literal; o log não tem texto, nome, remetente nem token
- [ ] T3-02 [Impl] Log só com metadados
## TLS e operação
- [ ] T4-01 [Impl] `painel/tls_lan.py` (CA, certificado com SAN de IP e DNS, `maestro-lan-ca.crt`)
- [ ] T4-02 [Verify] Chamada TLS verificando a CA (sem `verify=False`) contra 192.168.15.12:8793
- [ ] T9-01 [Verify] Suíte inteira com 0 failed e 0 errors; runner2 por quem não é o autor (Office)
- [ ] T9-02 [Verify] Chamada real do n8n: 202, depois 200 duplicada (SC-002)
