---
gate: abertura
tipo: bug
escopo: correcao
aberto_por: Hindiana Office
origem: chamado 099, G6-tela-b865c4a.md (PASSA) e G6-tela-fb901a1.md (FALHA)
data: 2026-10-09 07:41 -0300
autores: Assistente
---

# 070: conferidor escolhe o veredito vigente pela ordem alfabética

O conferidor (painel e linha de comando) escolhe o veredito vigente dos gates de veredito único pela ordem alfabética do nome do arquivo, não pela data. No 099, o G6 antigo (FALHA) vencia o novo (PASSA). Os requisitos R1 a R4 da spec.md corrigem.
