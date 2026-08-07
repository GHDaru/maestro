# Relatório de QA 039 — Fronteira interna e portão para os perfis de agente

- **Data**: 2026-08-06 · **Raia**: plena · **Veredito**: aprovado

## Fitness functions (DoD)

| Check | Esperado | Resultado |
|---|---|---|
| `scripts/check-roles.sh` | verde, com as 4 condições novas | ✅ `13 documented / 13 on disk / stated 13` |
| `scripts/check-boundary.sh` | verde, agora em domínios internos | ✅ 289 toolkit · 79 guia · 5 compartilhados · 37 páginas |
| `scripts/check-retro.sh` | verde e coerente depois das correções | ✅ 1 achado aberto (era 2) |
| `check-agents` · `check-install` · `check-language` · `check-links` · `check-chapters` · `check-cycle` | verde | ✅ |
| `node publicar/build.mjs` | verde | ✅ 37 páginas |
| `scripts/package-plugin.sh --verify` | verde | ✅ 32 arquivos |
| `scripts/check-evals.sh` | **vermelho** (dívida do 037) | ⚠️ inalterado |

## Prova de que o portão dos perfis acusa (princípio IV, corolário C2)

Escrito antes de tocar em `docs/agents/` e visto falhar nas quatro condições — cada uma um
ramo distinto, não a mesma falha quatro vezes.

**1. Agente no disco, ausente do índice** (`security` removido do índice):

```
✗ agent on disk and ABSENT from the index: security
  checked: 12 documented / 13 on disk / stated 13
```

**2. Índice apontando para agente inexistente** (`qa` → `fantasma`):

```
✗ agent on disk and ABSENT from the index: qa
✗ index documents an agent that does not exist: fantasma
```

**3. Tool nova no disco fora da linha do índice** — o caso caro, porque é o princípio III
vazando em silêncio. `review` ganhou `Edit`:

```
✗ review holds 'Edit' on disk and the index row does not list it
```

**4. Total declarado em prosa ficando velho** (13 → 12 no texto):

```
✗ the index claims 12 executable agents; there are 13 on disk
```

Os quatro estados foram desfeitos depois da prova.

## Prova de que o `check-boundary.sh` continua acusando após a reescrita

Reescrever um portão exige reprovar que ele ainda discrimina. `docs/agents/` removido dos
caminhos compartilhados — e a mensagem já reflete a razão nova da invariante:

```
✗ 2 page(s) published from the toolkit without being declared shared —
   a machine-facing document is going out to readers unannounced:
    docs/agents/perfis.md  (owner: toolkit)
    docs/agents/comunicacao.md  (owner: toolkit)
```

## Cobertura dos requisitos

- **FR1** (reversão registrada sem editar o original) — ✅ ADR 0018 criado; o 0017 recebeu
  status "Superado pelo ADR 0018" com o corpo intacto; índice com a linha de superação.
- **FR2**, **FR3**, **FR4**, **FR5** — ✅ provados em (1), (2), (3) e (4) acima.

## Correções de registro feitas neste ciclo

O índice é append-only, então dois erros foram corrigidos por linha nova, não por edição:

1. **`fecha` auto-referente.** A primeira linha do ciclo apontava `fecha` para o próprio
   `id`, fechando um achado que nunca foi aberto. Corrigida por
   `achado-039-registro-corrigido`, que narra o fato real: `docs/agents/` não tinha portão,
   e este ciclo entregou um.
2. **`achado-038` perdeu o objeto.** Ele dizia que, *depois da divisão*, os 22 caminhos de
   código citados pelo livro ficariam sem portão. Sem divisão, o cenário não ocorre e os
   caminhos seguem conferíveis no mesmo repositório. Fechado por `adr-0018-fecha-achado-038`.

Sem essas duas linhas, a dívida de retro contaria um achado inexistente e um achado sobre
um futuro cancelado — o índice mediria ficção.

## O que este ciclo NÃO faz

- **Não reestrutura `docs/`.** A auditoria achou três incômodos menores e a recomendação foi
  não mexer: `docs/livro/` e `docs/jornada/` têm um arquivo cada mas são citados por 11 e 6
  arquivos, e renome em massa já virou o anti-padrão 18 aqui. Custo real, ganho estético.
- **Não desfaz a duplicação de `plugin/maestro/`** (32 arquivos). É duplicação **com**
  forcing function — a forma mitigada — e ela acusou no ciclo 037 quando `/eval` nasceu.
- **Não compara `perfis.md` com o disco.** O vínculo estrutural vive no `README.md`, que já
  existe para isso; checar a prosa seria medir a palavra em vez do fato.
- **Não toca na dívida do 037.** As linhas de base de eval continuam pendentes.

## Gate pendente

- Promoção `dev` → `main`: aguarda aprovação humana. São três ciclos acumulados no `dev`
  (037, 038, 039), um deles com portão vermelho declarado.
