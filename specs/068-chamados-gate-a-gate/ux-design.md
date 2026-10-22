# UX design 068 — Chamados gate a gate (apontador)

> **Ciclo retroativo**: as duas vistas novas — a tabela chamado × gate ("Tabela (board)") e a
> trilha do chamado com custo por passo — já existem em `painel/index.html` (commits `e38a09c`
> e `80ab222`, 03–09/10/2026). O papel semântico de cada objeto está escrito uma vez só, no
> desenho do painel de regência (branch `066-painel-de-regencia`, `ux-design.md` §2 — a ser
> renumerado 072): **Gate** (coluna), **Chamado em gate** (cartão com dono e idade), **Veredito
> normalizado**, **Cadeia de evidência G0→G9**, **Veredito vigente** por gate. Não se duplica
> aqui (Princípio VI). O apontador do v0 está em `specs/066-painel-de-coordenacao-v0/ux-design.md`.

## O que o 068 já cumpre do desenho

| Objeto do desenho | Onde está no 068 | Evidência |
|---|---|---|
| Gate como coluna; chamado como linha | vista "Tabela (board)" | `index.html` (+287), commit `e38a09c` |
| Estado derivado, nunca digitado (ok / bad / run / falta / na) | `chamados.py` `confere` | `test_chamados.py`, 6 testes |
| Veredito vigente = o de maior data no hash certo | `chamados.py:189-190` | regra (d) do conferidor |
| Registro manual **rotulado** como tal | `registro="manual"`, "registro manual" na tela | `chamados.py:289`, `index.html:607,666` |
| Cadeia de evidência com o texto do gate | trilha do chamado (`/api/chamados/<id>/trilha`) | `chamados.py:383`, `index.html:656` (`esc()`) |
| Custo por passo ao lado da evidência | `custo.janela()` na trilha | `chamados.py:395-398` |

## O que fica para o 072

Veredito normalizado único (APPROVE/OK/PASSA/PASSOU → aprovado), arrasto entre colunas só com
evidência, idade do cartão e fila de decisões. E a dívida visual apontada pela segurança: o estado
**digitado** de um chamado manual aparece na mesma cor de um estado derivado — precisa de selo
distinto.

## Portão de UX deste ciclo

- `grep -c 'registro manual' painel/index.html` ≥ 1 — o que foi digitado se declara digitado;
- `python -m unittest discover -s painel/tests -p test_chamados.py` → 6 OK — o estado que a
  tela mostra é o que as regras do conferidor calculam.
