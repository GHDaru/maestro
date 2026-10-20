---
gate: GD
papel: risco
classe: A
objeto: specs/070-conferidor-ordem-veredito/spec.md @ 6741315
veredito: A
por: Hindiana Office
data: 2026-10-09 08:49 -0300
data_objeto: 2026-10-09 07:41:51 -0300
---

# GD do 070: classe A

Ferramenta interna do Maestro, o conferidor e o painel. Não toca produto, dado nem produção, e é reversível por commit. Corrige o veredito vigente, que era escolhido pela ordem alfabética do arquivo, para ser escolhido pela data.

Origem: pedido da Office à Assistente em 09/10, por volta das 07:38, depois do G6 do 099.

Fato de método: a GD veio depois do G3. A Office pediu a correção sem abrir a GD, e a falha é da Office.

Condições:
- G1 com 1 crítico (correção);
- G3 com a tabela SHALL (R1 a R4) sem lacuna;
- runner2 por não autor.
