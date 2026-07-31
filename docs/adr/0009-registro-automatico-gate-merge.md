# ADR 0009 — Registro automático do gate de merge no índice de decisões

- **Status**: Aceito · **Data**: 2026-07-31 · **Origem**: retro do ciclo 008
  (primeiro run do `retro.sh`)

## Contexto

O primeiro run da retro executável revelou uma lacuna: os qa-reports de ciclos já
promovidos mantinham "aguarda aprovação humana" aberto — o gate foi exercido (no chat),
mas nenhum artefato registrou o fechamento. O estado do gate vivia fora do repositório.
É exatamente o tipo de correção recorrente que a retro deve converter em regra executável
(modelo operacional §5 e §12: o que é mecânico vira hard gate/automação, não disciplina).

## Decisão

1. **O índice `docs/registro/decisoes.jsonl` é a fonte do estado dos gates de merge.**
2. **O registro é automático**: `scripts/promover-main.sh`, após a confirmação humana e
   antes do push, anexa `gate-main-<sha>` (data, título do commit promovido) via
   `registrar-decisao.sh` e o commita — impossível esquecer, impossível divergir.
3. **qa-reports históricos não são reescritos** (artefato histórico); o fechamento dos
   gates passados foi registrado retroativamente no índice (`gate-003-merge` …
   `gate-007-merge`).
4. `retro.sh` passa a cruzar as pendências dos qa-reports com o índice: ciclo com
   `gate-NNN-*` registrado aparece como fechado.

## Alternativas consideradas

- **Editar os qa-reports ao promover** — reescreve artefato histórico e depende de
  disciplina; rejeitada.
- **Só documentar a regra (sem automação)** — viola o §12 (garantia vem de tornar
  executável, não de memória); rejeitada.

## Consequências

- (+) Estado de gate auditável por máquina, dentro do repo, à prova de esquecimento.
- (+) O ciclo retro → regra → automação fechou em **um ciclo** (achado 008 → regra 009).
- (−) `promover-main.sh` ganha um commit extra por promoção (aceitável; é rastreabilidade).

## Registro

Modelo operacional **v1.3.0** (§12); `docs/registro/README.md` (formato `gate-main-*`).
