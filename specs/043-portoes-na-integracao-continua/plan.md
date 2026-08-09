# Plano 043 — Os portões entram na integração contínua

- **Spec**: `spec.md` · **Raia**: infra · **Data**: 2026-08-07

## Constitution Check (governance/principles.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-driven | Spec antes; os quatro FR saíram do achado da revisão do 042, não de ideia. |
| II. Orquestração governada | A divisão bloqueante × consultivo foi **decisão do Steward**, não minha — é ela que define o que trava o trabalho de todo mundo. |
| III. Reversibilidade / gates | Raia infra: bloco de reversibilidade abaixo. Privilégio mínimo declarado (`contents: read`), nenhum segredo, nenhuma escrita. |
| IV. Test-first / DoD verificável | O job foi **simulado localmente comando a comando** antes de existir, e a simulação reprovou — o `check-conformance` pegou o esqueleto vazio deste próprio ciclo. |
| V. Economia de contexto / fronteira | Um job, uma responsabilidade. Nada de matriz, nada de cache elaborado, nada de `/eval` (que precisa de chave). |
| VI. Artefatos vivos | O job **consome** os mesmos scripts que já existem — nenhuma lógica duplicada em YAML, que é onde ela apodreceria fora de vista. |
| VII. Governança leve / YAGNI | Nenhum portão novo. O ciclo só muda **quando** os existentes rodam. |
| VIII. Comunicação inteligível | CI (*continuous integration*, integração contínua) e SHA por extenso na primeira ocorrência de cada artefato. |

## Artefatos deste ciclo (declarar os cinco — silêncio não é decisão)

| Artefato | Declaração | Por quê |
|---|---|---|
| `research.md` | `ART:research=no` | nenhuma incógnita: os portões existem, o formato de workflow é conhecido |
| `data-model.md` | `ART:data-model=no` | não há entidade nem relação — é infraestrutura de verificação |
| `contracts/` | `ART:contracts=no` | o contrato é o código de saída dos scripts, que já existe e não muda |
| `checklist.md` | `ART:checklist=no` | a DoD da spec cobre; checklist próprio seria cerimônia |
| `ux-design.md` | `ART:ux-design=no` | nenhuma tela é tocada |

## Como

**Um job, dois passos de natureza diferente.** O que separa não é importância, é se o
vermelho significa "o repositório está inconsistente consigo mesmo" ou "há trabalho em voo":

| Passo | Portões | Bloqueia? |
|---|---|---|
| estrutural | `check-agents` · `check-roles` · `check-install` · `check-language` · `check-links` · `check-evals` · `check-boundary` · `check-conformance` · `check-chapters` · `package-plugin --verify` · build do livro | **sim** |
| consultivo | `check-cycle` · `check-retro` | não — emite `::warning::` |

**O job consome os scripts, não os reimplementa.** Lógica de verificação em YAML é lógica
que ninguém roda localmente e que apodrece sem sintoma. O workflow é um laço de três linhas.

**Dois detalhes que só aparecem em CI**, e que a simulação local revelou:

- o build do livro precisa de `npm ci --prefix publicar` (usa `markdown-it`), e o repositório
  tem *lockfile* — então a instalação é determinística;
- numa branch de pull request **não existe `main` local**, e o `check-cycle` compara contra
  ele. Daí `MAESTRO_TRACE_BASE=origin/main` mais o `git fetch` correspondente.

**Endurecimento de brinde**: o job de `CHANGELOG` que já existia termina um pipe em
`grep -q` — a forma exata do anti-padrão 21. Hoje funciona porque o *runner* não usa
`pipefail`; um dia usará. Capturado em variável antes de casar.

## Bloco de reversibilidade (obrigatório na raia infra)

| Item | Como |
|---|---|
| **Desfazer** | remover o job `gates` de `.github/workflows/ci.yml` — um commit, sem migração e sem estado |
| **Raio se der errado** | o job fica vermelho e **impede merge**; não corrompe nada, não escreve no repositório, não toca em segredo |
| **Ensaio antes** | o job foi executado localmente, passo a passo, com os mesmos comandos e a mesma ordem |
| **Sem proteção de branch** | nenhuma regra do GitHub exige este job ainda, então mesmo vermelho ele **não** trava ninguém sem uma segunda decisão humana |

O último item é o que torna esta mudança de irreversibilidade média e não alta: o poder de
bloquear só existe quando o Steward ligar a proteção de branch, que é decisão separada.

## Verificação (DoD)

```bash
# simulação do passo bloqueante, na ordem exata do job
for s in check-agents check-roles check-install check-language check-links \
         check-evals check-boundary check-conformance check-chapters; do scripts/$s.sh; done
scripts/package-plugin.sh --verify
npm ci --prefix publicar && node publicar/build.mjs
# simulação do passo consultivo
MAESTRO_TRACE_BASE=origin/main scripts/check-cycle.sh; scripts/check-retro.sh
```
