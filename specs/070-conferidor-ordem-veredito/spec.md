---
gate: abertura
tipo: bug
escopo: correcao
aberto_por: Hindiana Office
origem: chamado 099, G6-tela-b865c4a.md (PASSA) e G6-tela-fb901a1.md (FALHA)
data: 2026-10-09 07:41 -0300
autores: Assistente
---

# 070: conferidor escolhe o veredito vigente pela ordem alfabética do arquivo

## Problema

Nos gates de veredito único (GD, G4 a G9), o conferidor do painel (`painel/chamados.py`) e o da linha de comando (hindiana `scripts/maestro/conferir_chamado.py`) tomam como vigente o último veredito válido pela ordem alfabética do nome do arquivo. O hash no nome não tem ordem temporal: no 099, `G6-tela-b865c4a.md` (PASSA, mais novo) vem antes de `G6-tela-fb901a1.md` (FALHA, mais antigo), e o painel mostra a FALHA.

## Requisitos (EARS)

- **R1.** Quando um gate de veredito único tiver mais de um veredito válido, o conferidor SHALL tomar como vigente o de maior `data` do cabeçalho.
- **R2.** Quando dois vereditos válidos tiverem a mesma `data`, o conferidor SHALL desempatar pela data do commit do arquivo (a mais recente vence) e, persistindo o empate, pelo nome do arquivo.
- **R3.** Se um veredito válido não tiver `data` legível, o conferidor SHALL tratá-lo como o mais antigo.
- **R4.** O conferidor SHALL manter a lista de vereditos exibida na trilha em ordem de data, não de nome.

## Fora do escopo

G1 e G3 (vários vereditos por papel e por hash), que já ordenam por data dentro do hash.

## Critério de aceite

Teste com `G6-tela-b865c4a.md` PASSA (data 21:00) e `G6-tela-fb901a1.md` FALHA (data 20:00): o G6 sai `ok`. Na base 2796cbf o mesmo teste sai `bad`.
