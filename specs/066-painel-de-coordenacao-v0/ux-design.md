# UX design 066 — Painel de coordenação v0 (apontador)

> **Este ciclo é retroativo**: as onze telas do v0 já existem em `painel/index.html` e foram
> desenhadas em 01/10/2026 pelo painel de especialistas do Hindiana (`painel/docs/proposta.md`
> §3 lista cada uma com a fonte do dado). O papel semântico de cada objeto, derivado do
> catálogo de artefatos e da linguagem ubíqua, está escrito **uma vez só**, no ciclo que
> sucede este e o estende: `specs/066-painel-de-regencia/ux-design.md` (a ser renumerado
> 072 no mapa de integração; na branch `066-painel-de-regencia`, commit `ede9531`). O §1
> daquele documento ("consumido do v0") nomeia os objetos deste painel: sessão com estado,
> selo de evidência, número com fonte ou "—" com instrução, lista para aprovação, estado-ia
> e decisão registrada. Não se duplica aqui (Princípio VI).

## O que o v0 já cumpre do desenho

| Objeto | Onde está no v0 | Evidência |
|---|---|---|
| Sessão com estado (trabalhando, esperando, bloqueado, sem registro) e idade do sinal | board de agentes, faixa "Precisam de você agora" | `index.html`; commit `53f3e47` |
| Selo de evidência por estado da peça (exigida × presente) | fluxo de peças | `index.html`; commit `55dffa7`; `server.py` `valida_evento` |
| Número com fonte ao lado; "—" quando falta registro | DORA, tempo por fase | `index.html:437` "proxy, não é deploy"; commit `cf23e9e` |
| Lista para aprovação (nunca ação) | higiene do git | commit `b726ea7` |
| Estado derivado para a IA | `GET /api/estado-ia?sessao=` | `server.py:315-316` |

## O que fica para o 072

Kanban por gate G0–G9, jornada por chamado, fila de decisões e mapa de sessões — e a dívida de
acoplamento (`"Hindiana Office"` e `"Gilsiley"` em `server.py`). Jornada viva (captura do build
real e heurística datada) também é do 072: o v0 não tem captura versionada neste repositório.

## Portão de UX deste ciclo

Nenhum componente novo foi desenhado aqui, então o portão se reduz a duas verificações:

- `grep -c "proxy" painel/index.html` ≥ 1 — o número enganoso continua rotulado;
- `python -m unittest discover -s painel/tests -p test_painel.py` → 12 OK — as regras de
  evidência que a tela mostra são as que o servidor impõe.
