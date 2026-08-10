# QA report 046 — Licença e atribuição do que é redistribuído

- **Date**: 2026-08-10 · **Lane**: plena · **Verdict**: aprovado após reprovação e correção

## Fitness functions (DoD)

| Check | Expected | Result |
|---|---|---|
| `scripts/check-licensing.sh` | verde no repositório íntegro | ✅ `✓ licence present, manifest agrees, upstreams attributed, notices travel with the copy.` |
| `scripts/check-install.sh` | verde | ✅ |
| `scripts/check-boundary.sh` | verde, com os dois arquivos de raiz classificados | ✅ 324 toolkit / 79 guide, zero órfãos |
| `scripts/check-language.sh` | verde, incluindo os dois arquivos novos na superfície instalável | ✅ |
| `scripts/check-links.sh` · `check-agents` · `check-roles` · `check-evals` · `check-chapters` | verdes | ✅ |
| `scripts/package-plugin.sh --verify` | verde | ✅ `plugin in sync with the sources (33 files)` — 32 antes, +1 pelos avisos empacotados |
| `node publicar/build.mjs` | verde | ✅ |
| `scripts/check-cycle.sh` | verde | ✅ |
| `scripts/check-conformance.sh 046` | verde | ✅ (evidência abaixo) |

### O portão foi visto acusar — dez mutações, cada uma quebrando o repositório de verdade

Executadas num clone descartável (`scratchpad/mut`, apagado ao fim); o repositório de
trabalho não foi mutado. Cada linha é um estado em que a obrigação do MIT está genuinamente
rompida:

| Mutação | O que quebra | Portão |
|---|---|---|
| A — remover a linha de copyright do `github/spec-kit` | atribuição sem titular | ✗ `attributed with no holder: 'github/spec-kit'` |
| A2 — remover a do `obra/superpowers` | idem, no outro projeto | ✗ nomeando `obra/superpowers` |
| A3 — remover as duas | nada é atribuído a ninguém | ✗ duas linhas, uma por projeto |
| C — novo upstream vendorizado (GPL) sem atribuição | licença estranha entra na redistribuição | ✗ `named in .specify/UPSTREAM.md but absent` |
| J — renomear o upstream para prosa ("Spec Kit (by GitHub)") | a lista de upstreams fica vazia | ✗ `the gate found nothing to check, which is not the same as finding nothing wrong` |
| B — apagar `copy_as "LICENSE"` do instalador | a obrigação deixa de viajar | ✗ `the installer copies the method but not: LICENSE` |
| I — apagar o instalador inteiro | canal de redistribuição inauditável | ✗ `is missing — the installer is one of the two redistribution channels` |
| K — plugin empacotado sem os avisos | o outro canal sai nu | ✗ `the packaged plugin ships without: …` |
| L — manifesto declara `Apache-2.0` | alegação sem licença | ✗ `a claim is not a licence` |
| M — sem `LICENSE` | todos os direitos reservados | ✗ `worse than the licence we rejected` |
| N — sem `.specify/UPSTREAM.md` | não há lista de upstreams | ✗ `without the provenance file there is no list` |
| controle — clone íntegro | — | ✓ exit 0 |

## Closing tail — the evidence

- TAIL:review — revisão independente em contexto fresco, por quem não executou. Veredito:
  **NÃO PROMOVER COMO ESTÁ** — quatro bloqueantes. Três eram **vacuidade demonstrada** no
  portão novo, cada um com uma mutação que deixava o repositório quebrado e o portão verde:
  (1) a checagem de copyright casava com a **própria prosa** do arquivo (`Copyright ` sem
  âncora, com `-i`), então apagar o único titular passava; (2) FR5 não era "todo upstream" —
  o nome `spec-kit` estava **hard-coded**, então um upstream GPL novo entrava em silêncio, e
  renomear o existente fazia o laço rodar zero vezes com o resumo ainda dizendo "upstreams
  attributed" (antipadrão 16 na forma literal); (3) FR3 era satisfeito pelo **comentário** do
  instalador, e o bloco inteiro era um `if [[ -f ]]` sem `else` — apagar o instalador dava
  exit 0. O quarto era de cobertura: o **plugin**, o segundo canal de redistribuição que o
  ADR 0020 nomeia no Contexto, continuava sem aviso nenhum na Decisão. Mais quatro relevantes
  e três menores. **Todos corrigidos**; a mutação A ainda passou na primeira correção
  (a linha ancorada era satisfeita pelo titular de *outro* projeto), e o invariante virou
  **por projeto**: toda seção `## owner/repo` precisa do seu próprio titular. As dez mutações
  foram re-executadas — a tabela acima é o resultado depois da correção.
- TAIL:security — passe proporcional à classe de risco (escrita em repositório de terceiro).
  Quatro superfícies examinadas. **(a) Injeção por prosa**: os dois arquivos passam a ser
  lidos dentro de `docs/governance/` de repositórios alheios e dentro do pacote do plugin —
  diretórios que agentes leem. Varredura por linha em forma de diretiva (`you must`,
  `ignore previous`, `run`, `curl`, `bash`, URL executável): **nenhuma**; os únicos links são
  as duas URLs dos projetos upstream. O bloco de instrução do instalador não manda ler
  nenhum dos dois. **(b) Caminhos**: origem e destino de `copy_as()` são literais fixos, sem
  interpolação de entrada; `MODE` só aceita três valores. **(c) Injeção de regex**: o campo
  `license` do manifesto era interpolado cru num padrão `grep` — corrigido para `-F` sobre a
  primeira linha do `LICENSE` (achado 11 da revisão). **(d) CI**: nenhuma permissão nova,
  nenhum segredo; o job `gates` segue com `contents: read`. **Risco declarado e não
  mitigável por portão**: MIT não concede patente — registrado no ADR 0020 como consequência
  aceita.
- TAIL:gate — DoD verde (tabela acima), nove portões bloqueantes + `package-plugin --verify`
  + build do livro verdes, `check-conformance.sh 046` verde. **Aguarda o gate humano** de
  promoção `dev` → `main`, que não é delegável; `promote-main.sh` registra o
  `gate-main-<sha>` quando ocorrer.

## Requirement coverage

- **FR1** — `LICENSE` com texto MIT íntegro e `Copyright (c) 2026 GHDaru`. Portão: bloco 1;
  mutação M.
- **FR2** — `THIRD-PARTY-NOTICES.md` atribui `github/spec-kit` (speckit 0.4.3, fork
  `GHDaru/spec-kit @ 0117a7b`, MIT, *Copyright GitHub, Inc.*) com o aviso de permissão
  **reproduzido por inteiro**, e `obra/superpowers` (MIT, *Copyright (c) 2025 Jesse
  Vincent*), acrescentado pela revisão. Verbatim separado de modificado. Portão: mutações
  A/A2/A3.
- **FR3** — os dois canais: instalador (`copy_as`, renomeando) e plugin (`build()` copia os
  dois). Portão: blocos 4 e 5; mutações B, I, K.
- **FR4** — manifesto × licença, com `grep -F`. Portão: bloco 2; mutação L.
- **FR5** — upstreams extraídos **genericamente** de `## Origens`, e lista vazia é falha.
  Portão: bloco 3; mutações C, J, N.

## Achados registrados neste ciclo

- **O índice `docs/adr/README.md` estava congelado desde o 0017**: faltavam os ADRs 0018 e
  0019, e o 0017 constava "Aceito" tendo sido superado pelo 0018 desde o ciclo 039. Anti-padrão
  15, sem portão que cubra. Corrigido aqui; o portão fica como dívida declarada.
- **A afirmação "reproduzido sob github/spec-kit" era falsa** quando escrita: nada estava
  reproduzido ali. Corrigida reproduzindo o texto, não reescrevendo a frase.
- **Os links relativos do aviso quebravam no destino instalado** (`docs/governance/LICENSE`
  não existe; o arquivo chama-se `MAESTRO-LICENSE`). Trocados por nomes em código com a nota
  do nome instalado — `check-links.sh` não pegava, porque valida a origem, onde resolvem.

## Pending gate

- Promoção `dev` → `main` aguarda aprovação humana.
