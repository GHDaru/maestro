# UX design NNN — [TÍTULO]

- **Spec**: `spec.md` · **Data**: [AAAA-MM-DD] · **Agente**: `ux-semantica`

<!--
  PAPEL ANTES DE COMPONENTE (Iron Law do agente ux-semantica): pergunte "qual é o PAPEL
  deste objeto?" — do papel deriva a anatomia obrigatória, nunca o contrário.
  Papel já catalogado -> consuma o componente. Papel novo -> entra PRIMEIRO no catálogo
  (linha com anatomia) + componente comum + teste; só então é usado na tela.
-->

## Jornada(s) servida(s)

- [`docs/journeys/NNN-<slug>.md`] — o que o usuário quer conseguir aqui.

## Papéis semânticos consumidos (já catalogados)

| Papel | Componente do catálogo | Onde aparece |
|---|---|---|
|  |  |  |

## Papéis introduzidos (novos — exigem catalogação antes do uso)

| Papel | Anatomia obrigatória | Por que não deriva de um existente |
|---|---|---|
|  |  |  |

## Estados obrigatórios

- [ ] **Vazio** — o que se vê quando não há dado (e o que fazer a seguir)
- [ ] **Carregando** — feedback, sem salto de layout
- [ ] **Erro** — o que houve **e** como resolver
- [ ] **Sem permissão** — quando aplicável

## Acessibilidade (não é etapa final)

- [ ] Rótulo acessível em todo controle sem texto visível
- [ ] Foco de teclado visível e ordem previsível
- [ ] Contraste suficiente nos dois temas (quando houver)

<!-- GATE: humano aprova o ux-design antes da implementação (DoR, se houver interface). -->
