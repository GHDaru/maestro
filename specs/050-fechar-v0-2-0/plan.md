# Plan 050 — Fechar a v0.2.0

- **Spec**: `spec.md` · **Lane**: plena · **Date**: 2026-08-11

## Constitution Check (governance/principles.md)

| Principle | Compliance |
|---|---|
| I. Spec-driven | ✅ `spec.md` antes deste plano; FR1–FR4 em EARS, dois deles com portão e dois com evidência no relatório. |
| II. Human-governed orchestration | ✅ O número da versão é decisão humana e foi tomada pelo Steward; a criação da tag pública também é dele, por necessidade e por princípio. |
| III. Reversibility / risk gates | ⚠️ Parcial e declarado: **anunciar uma versão não se desanuncia**. O que é reversível é o conteúdo (git); o anúncio, não. Por isso a nota declara os limites em vez de escondê-los. |
| IV. Test-first / verifiable DoD | ✅ `check-version.sh` foi escrito **antes** do corte, visto verde em 0.1.0 e visto **vermelho no estado intermediário real** — CHANGELOG já em 0.2.0, os outros três ainda em 0.1.0. |
| V. Context economy / boundary | ✅ `scripts/` já é `toolkit`; nada muda de domínio. O portão não viaja, e a razão está na spec. |
| VI. Living artifacts | ✅ É o ponto do ciclo: a versão deixa de ser quatro cópias mantidas em acordo pela memória. |
| VII. Light governance / YAGNI | ✅ Sem reorganizar o CHANGELOG, sem tocar na versão da constituição (1.3.0, que é outra coisa), sem inventar processo de release. |
| VIII. Intelligible communication | ✅ A nota diz o que a versão **não** tem antes de dizer como é verificada, e nomeia a tag não publicada em vez de deixar o leitor descobrir. |

## Artifacts of this cycle (declare all five — silence is not a decision)

<!-- Read by scripts/check-conformance.sh. Declaring =yes means the file MUST exist here.
     What each one is for: docs/governance/artifacts.md -->

| Artifact | Declaration | Why |
|---|---|---|
| `research.md` | `ART:research=no` | Nenhuma incógnita: o que entrou na versão está nos quatro `qa-report.md` e no CHANGELOG. |
| `data-model.md` | `ART:data-model=no` | Nenhuma entidade. O ciclo escreve prosa e compara quatro strings. |
| `contracts/` | `ART:contracts=no` | Nenhuma interface. O "contrato" é o formato de cabeçalho de versão do Keep a Changelog, que já é convenção pública. |
| `checklist.md` | `ART:checklist=no` | Os critérios de aceite são a lista; a nota de release é o próprio entregável. |
| `ux-design.md` | `ART:ux-design=no` | Não toca tela. A superfície é o `README.md`, cuja forma já é a do padrão editorial. |

## How

1. **`scripts/check-version.sh`** (16º portão) — a versão da declaração mais nova do
   CHANGELOG (`## [X.Y.Z]`, nunca `[Unreleased]`) contra `README.md`, o cabeçalho do roadmap
   e o README empacotado. Lugar que **não** declara versão também falha: silêncio numa das
   primeiras coisas que alguém lê é tão ruim quanto divergência.
2. **A nota de release**, nas três partes que a v0.1.0 estabeleceu — o que é · o que
   reconhecidamente não tem · como é verificada. A parte do meio é a que custa escrever, e é
   a que faz a nota valer.
3. **O corte nas quatro declarações**, com o plugin reempacotado (o README dele é gerado).
4. **A tag local** no commit da versão, e o comando de publicação escrito para quem tiver
   rede — porque este ambiente não tem.

## Verification (DoD)

| Comando | Esperado |
|---|---|
| `scripts/check-version.sh` | verde antes do corte (0.1.0), vermelho no meio, verde depois (0.2.0) |
| mutações FR2/FR3 | acusadas, inclusive lugar que deixa de declarar |
| bateria completa + `check-installed` + plugin + build | verdes |
| `git tag -l` | `v0.2.0` presente localmente, apontando para o commit da versão |
