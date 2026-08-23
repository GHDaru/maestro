# Plan 062 — Fechar a v0.3.0

- **Spec**: `spec.md` · **Lane**: plena · **Date**: 2026-08-22

## Constitution Check (governance/principles.md)

| Principle | Compliance |
|---|---|
| I. Spec-driven | ✅ Cinco FRs; o FR3 é o mecanizável e ganha portão, os outros são conferidos pelo `check-version.sh` que já existe. |
| II. Human-governed orchestration | ✅ O corte foi **pedido** pelo Steward; a tag e a promoção passam pelo portão humano. |
| III. Reversibility / risk gates | ✅ Tudo é texto reversível — **menos a tag**, que é o único artefato público. Por isso ela é o último passo e seu estado é **verificado**, não presumido. |
| IV. Test-first / verifiable DoD | ✅ O FR2 é provado por mutação em cada um dos quatro lugares; o FR3 ganha comparação contra a saída real do instalador. |
| V. Context economy / boundary | ✅ Nenhum portão novo: o FR3 entra no `check-installed.sh`, que já roda o instalador. |
| VI. Living artifacts | ✅ A nota de release declara o que a versão **não** tem, como as duas anteriores. |
| VII. Light governance / YAGNI | ✅ O corte não inventa processo: repete o de 045 e 050. |
| VIII. Intelligible communication | ✅ A nota diz o que mudou para quem **usa**, não a lista de commits. |

## Artifacts of this cycle (declare all five — silence is not a decision)

<!-- Read by scripts/check-conformance.sh. Declaring =yes means the file MUST exist here.
     What each one is for: docs/governance/artifacts.md -->

| Artifact | Declaration | Why |
|---|---|---|
| `research.md` | `ART:research=no` | Os fatos são cinco `grep` e estão na spec. |
| `data-model.md` | `ART:data-model=no` | Nenhuma entidade. |
| `contracts/` | `ART:contracts=no` | Nenhuma interface entre partes. |
| `checklist.md` | `ART:checklist=no` | Quatro critérios de aceite, provados por mutação. |
| `ux-design.md` | `ART:ux-design=no` | Não toca tela. |

## How

**FR1 — o corte.** `## [Unreleased]` vira `## [0.3.0] — <data>`, ganha a nota de release
(o que ela é · o que ela não tem), e um `## [Unreleased]` novo e vazio entra acima. Os 18 itens
já estão escritos e verificados ciclo a ciclo; a nota **não** os repete, ela os resume para quem
vai instalar.

**FR2 — os quatro lugares.** README, roadmap, `plugin/maestro/README.md` e o próprio CHANGELOG.
O `check-version.sh` já compara os quatro contra a versão do CHANGELOG; a mutação é trocar cada
um por `0.2.0` e ver o portão reprovar — quatro mutações, uma por lugar.

**FR3 — o exemplo que envelhece calado.** A receita publica um `install-options.json` de
exemplo com `"maestro_version": "0.2.0"`. É a mesma família do ciclo 060: um fato dito numa
página e produzido por um programa. O `check-installed.sh` já grava esse arquivo na instalação
de referência — passa a comparar **as chaves e a versão** do exemplo publicado com o real.
O `installed` (data) é ignorado por construção: é diferente a cada execução.

**FR4 — a tag.** Criada localmente e publicada por último. O resultado do `git push` é
**lido**; a nota de release afirma o estado que foi lido. Se falhar, a dívida entra na nota e
no índice de achados, como a da v0.1.0 já está.

**FR5 — o roadmap.** Linha `F26 — v0.3.0`, no formato das duas anteriores.

## Verification (DoD)

| Comando | Esperado |
|---|---|
| `check-version.sh` | verde com `0.3.0` |
| **mutações 1–4**: cada lugar declarando `0.2.0` | `check-version.sh` reprova, nomeando o lugar |
| **mutação 5**: exemplo da receita com versão velha | `check-installed.sh` reprova |
| **mutação 6**: exemplo da receita com chave que o instalador não grava | `check-installed.sh` reprova |
| **contraprova**: exemplo correto | passa |
| `[Unreleased]` novo | existe e está vazio |
| `git ls-remote --tags` | o que a nota afirma sobre a tag é o que isto devolve |
| os 14 portões bloqueantes · `--ticked-only` · plugin · build | verdes |
