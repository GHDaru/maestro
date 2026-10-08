---
tipo: excecao
papel: office
objeto: specs/068-chamados-whatsapp/GD-risco.md @ 17df3eb
por: Hindiana Office
data: 2026-10-08 13:15 -0300
---

# Exceção do Office: construir P1 a P5 com a GD em curso

**O quê.** P1 a P5 do 068 podem ser construídos assim que o G1 der PASSOU no conferidor, mesmo com a GD (classe C) ainda EM CURSO.

**Por quê.** A GD ficou em C por duas decisões de LGPD do Gilsiley, que é o controlador do dado:
- a base legal do tratamento (art. 7º);
- a retenção de 12 meses no git (art. 16).

Essas decisões dizem respeito a dado real de cliente. Construir com número de teste e dado sintético não trata dado de ninguém e pode ser desfeito.

**Limites.**
1. Só números de teste e dado sintético. Nenhum telefone, nome ou mensagem de cliente real, nem em teste nem em fixture.
2. O G8, que é a primeira mensagem a cliente real, continua travado até a GD passar com `adr` e `decisao_gilsiley`.
3. O Gilsiley pode revogar a exceção a qualquer momento. Se ele revogar, a construção para onde estiver.

**Avisado ao Gilsiley** em 08/10 às 13:16, no chat da Hindiana Office.
