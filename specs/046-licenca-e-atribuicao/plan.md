# Plan 046 — Licença e atribuição do que é redistribuído

- **Spec**: `spec.md` · **Lane**: plena · **Date**: 2026-08-10

## Constitution Check (governance/principles.md)

| Principle | Compliance |
|---|---|
| I. Spec-driven | ✅ `spec.md` escrita antes deste plano; FR1–FR5 em EARS, cada um com um teste no portão. |
| II. Human-governed orchestration | ✅ A escolha da licença é decisão humana e foi tomada pelo humano ("Mantenha MIT"). O agente executa o texto e o portão, não escolhe o licenciamento. |
| III. Reversibility / risk gates | ⚠️ Parcial e declarado: publicar sob MIT é **irreversível para o que já foi baixado** — quem obteve uma cópia sob MIT a mantém sob MIT. O que é reversível é o futuro (relicenciar dali para frente). A raia é plena por raio, não por irreversibilidade; o gate humano continua sendo o merge. |
| IV. Test-first / verifiable DoD | ✅ `check-licensing.sh` foi escrito e **visto acusar** em três condições distintas antes de qualquer correção (evidência no `qa-report.md`). |
| V. Context economy / boundary | ✅ `LICENSE` e `THIRD-PARTY-NOTICES.md` entram no `boundary.json` como `toolkit` — arquivos de raiz, como `README.md` e `CHANGELOG.md`; o portão novo já era coberto pelo prefixo `scripts/`. **Não** entram em `shared`: ali só vai o que o site publica. |
| VI. Living artifacts | ✅ O portão falha quando o manifesto e o `LICENSE` divergem, e quando um upstream nomeado em `UPSTREAM.md` não estiver atribuído — as notas não podem envelhecer em silêncio. |
| VII. Light governance / YAGNI | ✅ Escopo cortado no mínimo que a obrigação exige: sem SBOM, sem auditoria das dependências de build, sem parecer jurídico (todos declarados fora de escopo com o porquê). |
| VIII. Intelligible communication | ✅ Os arquivos instalados são **renomeados** no destino, porque um `LICENSE` na raiz alheia comunicaria algo falso sobre o projeto de destino. |

## Artifacts of this cycle (declare all five — silence is not a decision)

<!-- Read by scripts/check-conformance.sh. Declaring =yes means the file MUST exist here.
     What each one is for: docs/governance/artifacts.md -->

| Artifact | Declaration | Why |
|---|---|---|
| `research.md` | `ART:research=no` | A incógnita era factual e de uma consulta só (qual a licença e o titular do `github/spec-kit`): resolvida no próprio ciclo e registrada em `THIRD-PARTY-NOTICES.md`, que é o artefato permanente. Um `research.md` seria a mesma informação num lugar que ninguém consome. |
| `data-model.md` | `ART:data-model=no` | Não há entidade nem relação: o ciclo produz três arquivos de texto e um portão de shell. |
| `contracts/` | `ART:contracts=no` | Nenhuma interface nova. O portão lê arquivos do disco; não expõe rota, porta nem evento. |
| `checklist.md` | `ART:checklist=no` | Os critérios de aceite da `spec.md` já são a lista, e cada um deles é verificado por `check-licensing.sh`. Uma segunda lista seria a cópia com perda que este repositório nomeou como antipadrão 22. |
| `ux-design.md` | `ART:ux-design=no` | Não toca tela alguma. A superfície de interação é a saída do portão no terminal, coberta pelo Princípio VIII acima. |

## How

1. **`LICENSE` na raiz** — texto MIT íntegro, `Copyright (c) 2026 GHDaru`. Sem licença, o
   padrão legal é *todos os direitos reservados*: mais restritivo que a licença que
   recusamos.
2. **`THIRD-PARTY-NOTICES.md`** — atribui `github/spec-kit` (speckit 0.4.3, fork
   `GHDaru/spec-kit @ 0117a7b`, MIT, *Copyright GitHub, Inc.*), separando **verbatim** de
   **modificado**, e declara o que é ideia citada e não redistribuída (EARS) e o que é
   dependência só de build.
3. **`scripts/check-licensing.sh`** — quatro invariantes, uma por requisito verificável:
   FR1 o `LICENSE` existe; FR4 o que o manifesto declara é o que o `LICENSE` diz; FR5 todo
   upstream nomeado em `.specify/UPSTREAM.md` tem atribuição **com linha de copyright**;
   FR3 o instalador carrega os dois arquivos.
4. **`install-maestro.sh`** — `copy_as()`, que copia renomeando:
   `LICENSE` → `docs/governance/MAESTRO-LICENSE` e
   `THIRD-PARTY-NOTICES.md` → `docs/governance/MAESTRO-THIRD-PARTY-NOTICES.md`.
   Renomear é o requisito, não um detalhe: preserva a obrigação sem mentir sobre o destino.
5. **Glossário** — EARS, BMAD e SBOM, que apareceram em documentos nossos sem registro.
6. **ADR 0020** — a escolha e o que ela custa. Apache-2.0 foi considerada e recusada
   (concessão de patente vs. cerimônia de `NOTICE`); a ausência de concessão de patente fica
   escrita como consequência aceita, não como esquecimento.
7. **CI** — `check-licensing` entra no job `gates` como **bloqueante**. Portão que só roda
   quando alguém lembra não é *forcing function*; seria a norma sem forma que este
   repositório já nomeou.
8. **`docs/adr/README.md`** — achado do próprio ciclo: o índice estava congelado desde o
   0017 (faltavam 0018 e 0019, e o 0017 constava "Aceito" tendo sido superado).

**Ordem deliberada**: o portão foi escrito **antes** das correções e foi observado vermelho.
Um portão escrito depois do conserto nunca provou que sabe acusar.

## Verification (DoD)

| Comando | Esperado |
|---|---|
| `scripts/check-licensing.sh` | verde, e antes das correções vermelho nas três condições |
| `scripts/check-install.sh` | verde |
| `scripts/check-boundary.sh` | verde com os arquivos novos classificados |
| `scripts/check-language.sh` | verde (arquivos instaláveis em inglês) |
| `scripts/check-conformance.sh 046` | verde |
| `scripts/package-plugin.sh --verify` | verde |
