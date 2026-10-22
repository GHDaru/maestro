---
gate: G0
papel: reproducao
objeto: specs/070-conferidor-ordem-veredito/spec.md @ 6741315
veredito: REPRODUZIDO
por: Hindiana Office
data: 2026-10-09 09:19 -0300
data_objeto: 2026-10-09 07:41:51 -0300
---

# G0 do 070: reproduzido

Reproduzido pela Office, que não é autora. A pasta specs/099-filtros-multiselecao do hindiana 82a79b9 foi copiada para uma área de rascunho, com dois G6 válidos:
- G6-tela-b865c4a.md: PASSA, data 2026-10-09 07:34, de 3ac1c87b;
- G6-tela-fb901a1.md: FALHA, data 2026-10-09 02:42. O data_objeto foi alinhado ao git (00:55:30) só na cópia, para o arquivo ficar válido.

| Conferidor (hindiana, scripts/maestro/conferir_chamado.py) | Linha G6 |
|---|---|
| b1c0108, antes da correção | `G6 BARRADO G6-tela-fb901a1.md: FALHA`: pega o mais antigo, que é o último na ordem alfabética |
| 8adb545a, a correção do 070 | `G6 PASSOU G6-tela-b865c4a.md: PASSA`: pega o mais recente pela data |

O defeito é o descrito na spec: o veredito vigente era escolhido pela ordem alfabética do nome do arquivo.
