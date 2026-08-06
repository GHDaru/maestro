# Relatório de QA 038 — Divisão em dois repositórios (fatia 1)

- **Data**: 2026-08-06 · **Raia**: infra · **Veredito**: aprovado

## Fitness functions (DoD)

| Check | Esperado | Resultado |
|---|---|---|
| `scripts/check-boundary.sh` | verde: fronteira decidível | ✅ 282 toolkit · 79 guia · 5 espelhos · 37 páginas |
| `scripts/check-links.sh` | verde | ✅ |
| `scripts/check-language.sh` | verde (o script novo é instalável) | ✅ |
| `scripts/check-agents.sh` · `check-roles.sh` · `check-install.sh` | verde | ✅ |
| `scripts/check-cycle.sh` | verde, raia infra justificada | ✅ |
| `scripts/check-retro.sh` | verde | ✅ |
| `scripts/check-chapters.sh` | verde | ✅ |
| `node publicar/build.mjs` | verde | ✅ 37 páginas |
| `scripts/check-evals.sh` | **vermelho** (dívida do ciclo 037) | ⚠️ inalterado, como esperado |

## Prova de que o portão acusa (princípio IV, corolário C2)

O portão foi escrito **antes** da classificação e visto falhar nas três invariantes. Não é
a mesma falha três vezes — cada uma é um ramo distinto.

**1. Arquivo que ninguém reclama** (`docs/novo/orfao.md`, criado só para isto):

```
✗ 1 file(s) claimed by nobody — the split cannot be executed:
    docs/novo/orfao.md
```

**2. Página publicada vinda do toolkit sem espelho** — `docs/governance/` removido da lista
de espelhados. É a invariante que justifica o ciclo inteiro, e ela nomeia exatamente o que
se perderia:

```
✗ 4 published page(s) come from the toolkit and are NOT mirrored —
   the guide's site would lose them on the day of the split:
    docs/governance/principles.md  (owner: toolkit)
    docs/governance/axioms.md  (owner: toolkit)
    docs/governance/operating-model.md  (owner: toolkit)
    docs/governance/glossary.md  (owner: toolkit)
```

**3. Dupla reivindicação** — `docs/governance/` reivindicado também pelo guia:

```
✗ 4 file(s) claimed by both repositories:
    docs/governance/axioms.md
    docs/governance/glossary.md
    …
```

Os três estados foram desfeitos depois da prova; o portão voltou a verde.

## Cobertura dos requisitos

- **FR1** (um dono por arquivo) — ✅ 361 arquivos rastreados classificados, 0 órfãos,
  0 duplos. Provado em (1) e (3).
- **FR2** (espelho tem fonte no toolkit) — ✅ 5 caminhos espelhados, todos do toolkit.
- **FR3** (página publicada tem origem reclamada) — ✅ 37 páginas: 28 do guia, 9 espelhadas.
  Provado em (2).
- **FR4** (fonte única) — ✅ `boundary.json`; nenhum script carrega lista própria.

## O que este ciclo NÃO entrega

- **Nenhum arquivo mudou de lugar.** Por decisão (princípio III): divisão de repositório é
  irreversibilidade alta, então a fatia 1 entrega o critério e a fatia 2 executa. Custo de
  desfazer hoje: apagar dois arquivos.
- **O mecanismo de espelhamento não existe ainda.** `boundary.json` declara *o que* é
  espelhado; *como* (submódulo git ou script + portão) é a fatia 2. Um espelho sem forcing
  function seria a cópia manual que o Steward rejeitou no gate.
- **Nada resolve a evidência do livro.** Os 22 caminhos de código que os capítulos citam
  ficarão em outro repositório, sem portão que os confira. Dívida nomeada no ADR 0017, sem
  solução desenhada — dizer o contrário seria promessa.
- **`maestro-guia` não é o nome decidido.** É proposta em `boundary.json`; nada depende dela.

## Gate pendente

- Promoção `dev` → `main`: aguarda aprovação humana.
- **Gate da fatia 2** (separado): aprovar o nome do repositório do guia, autorizar a criação
  do remoto e a mudança física. Pré-condição: `check-boundary.sh` verde — que é o que este
  ciclo entrega.
