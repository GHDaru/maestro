# Plan 047 — Catálogo do ecossistema

- **Spec**: `spec.md` · **Lane**: plena · **Date**: 2026-08-10

## Constitution Check (governance/principles.md)

| Principle | Compliance |
|---|---|
| I. Spec-driven | ✅ `spec.md` antes deste plano; FR1–FR7 em EARS, seis deles com portão. |
| II. Human-governed orchestration | ✅ O veredito sobre uma fonte externa é decisão humana; o catálogo e o portão medem coerência, nunca decidem por ninguém. |
| III. Reversibility / risk gates | ✅ Só arquivos de texto e um portão. O índice de estado é append-only: mudar de veredito é uma linha nova, nunca uma edição. |
| IV. Test-first / verifiable DoD | ✅ `check-ecosystem.sh` escrito antes da migração e visto acusar por mutação em cada requisito — e ele já nasce **vermelho** contra o conteúdo real (duas absorções que nunca aconteceram). |
| V. Context economy / boundary | ✅ `docs/ecosystem/` é `toolkit` e `shared` (publicado no livro, parte "Bastidores"): é memória do método **e** resposta à pergunta "está no livro?". |
| VI. Living artifacts | ✅ É o ponto do ciclo: o portão falha quando o destino declarado não existe, então o catálogo não pode envelhecer em silêncio. As quatro fichas antigas ganham nota de "migrado para", sem serem apagadas. |
| VII. Light governance / YAGNI | ✅ Sem ranking, sem nota agregada, sem rejulgar o que já foi julgado. O card é curto; a lista de fontes é uma linha por fonte. |
| VIII. Intelligible communication | ✅ Vocabulário fechado de quatro vereditos (`adotar` · `absorver` · `observar` · `descartar`), definido uma vez no índice e usado em todo lugar. |

## Artifacts of this cycle (declare all five — silence is not a decision)

<!-- Read by scripts/check-conformance.sh. Declaring =yes means the file MUST exist here.
     What each one is for: docs/governance/artifacts.md -->

| Artifact | Declaration | Why |
|---|---|---|
| `research.md` | `ART:research=no` | Não há incógnita técnica: o material já existe no repositório (ADR 0005, ADR 0008, apêndice C, `upstream-decomposicao.md`). O trabalho é de forma e de verificação, não de pesquisa. |
| `data-model.md` | `ART:data-model=yes` | Há entidades e relações de verdade — **fonte**, **ideia** e **estado** —, com cardinalidade (uma fonte gera N ideias; uma ideia tem N estados ao longo do tempo, o corrente é o último) e um vocabulário fechado. É exatamente o caso que `docs/governance/artifacts.md` prevê, e é o que o portão lê. |
| `contracts/` | `ART:contracts=no` | Nenhuma interface de rede, rota ou evento. O formato do `estado.jsonl` é contrato, e vive no `data-model.md` — duplicá-lo aqui violaria o Princípio VI. |
| `checklist.md` | `ART:checklist=no` | Os critérios de aceite da spec já são a lista, e cada um tem portão ou evidência no `qa-report.md`. |
| `ux-design.md` | `ART:ux-design=no` | Não toca tela. A superfície é markdown lido no GitHub e no site, e o site já tem seu padrão editorial (`docs/livro/guia-editorial.md`). |

## How

### O objeto: três artefatos, não um

```
docs/ecosystem/
  README.md        índice: como funciona, vocabulário de veredito, estado corrente
  fontes.md        UMA linha fina por fonte: owner/repo · o que é · licença · observado em
  ideias/NNN-<slug>.md   UM card por IDEIA — imutável, datado (o MOMENTO)
  estado.jsonl     append-only: id da ideia -> veredito corrente (o ESTADO)
```

**Momento × estado é a decisão central.** Um card diz "em 2026-07-30, olhando o Superpowers
na versão X, julgamos que worktree por task valia ser absorvido, por estas razões". Isso é
verdade para sempre. O veredito de **hoje** é outra coisa, muda, e mora no índice — cuja
última linha por id é o estado corrente, exatamente como `docs/records/decisoes.jsonl`.
Misturar os dois força uma escolha entre reescrever a história e mentir sobre o presente.

### As sete dimensões (o padrão multidimensional)

| # | Dimensão | Pergunta | Reprova sozinha? |
|---|---|---|---|
| 1 | Conflito com princípio | qual princípio, e é insanável? | **sim** |
| 2 | Licença e redistribuição | dá para copiar, ou só citar? | **sim** |
| 3 | Função já servida | duplica algo que já temos (Princípio VI)? | não |
| 4 | Custo de contexto | quantos tokens/overhead custa carregar? | não |
| 5 | Reversibilidade | quanto custa sair depois (lock-in)? | não |
| 6 | Maturidade e evidência | o que **nós** observamos, em que versão — não stars de terceiros | não |
| 7 | Dor real hoje | a dor que isso resolve existe aqui, agora (YAGNI)? | não |

Sem nota agregada: duas dimensões reprovam sozinhas, e uma média as diluiria.

### O portão (`scripts/check-ecosystem.sh`)

1. Toda fonte em `fontes.md` tem `owner/repo`, licença e data de observação (FR1, FR6).
2. Todo card tem a anatomia obrigatória e as sete dimensões (FR2).
3. Todo card tem estado no índice, e todo estado tem card (FR3) — nos dois sentidos.
4. Estado `adotar`/`absorver` ⇒ **o destino declarado existe no disco** (FR4).
5. Estado `observar` ⇒ gatilho de reavaliação não vazio (FR5).
6. Lista vazia é falha, nunca aprovação (lição do 046).

### Ordem

O portão primeiro; depois a migração das quatro origens; e o portão **fica vermelho** até
worktree-por-task e standards-por-camada voltarem ao estado honesto. A correção é no
conteúdo, jamais uma exceção no portão.

## Verification (DoD)

| Comando | Esperado |
|---|---|
| `scripts/check-ecosystem.sh` | vermelho antes da correção do conteúdo, verde depois |
| mutações no clone descartável | uma por requisito, todas acusadas |
| `scripts/check-boundary.sh` | verde com `docs/ecosystem/` classificado e declarado shared |
| `scripts/check-language.sh` | verde (o catálogo é livro/memória: português, como os ADRs) |
| `scripts/check-install.sh` · `check-links` · `check-conformance 047` | verdes |
| `node publicar/build.mjs` | verde, com o índice publicado |
