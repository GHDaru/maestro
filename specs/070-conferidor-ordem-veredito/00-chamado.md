---
gate: abertura
tipo: bug
aberto_por: Assistente
data: 2026-10-09 07:40 -0300
origem: painel
autores: Assistente
---

# 070: conferidor toma veredito vigente pela ordem alfabética

O conferidor (painel e CLI) seleciona o veredito vigente de um gate pelo
último arquivo na ordem alfabética, não pela data do cabeçalho. Quando dois
críticos emitem vereditos sobre o mesmo hash, o de maior data deveria vencer,
mas o de nome alfabeticamente maior é tomado como vigente.

**Sintoma:** G6 com b865c4a PASSA (21:00) e fb901a1 FALHA (20:40) resulta
BARRADO — fb901a1 vence por ordem alfabética.
