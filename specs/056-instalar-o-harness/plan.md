# Plan 056 — Instalar o harness: a regra deixa de depender de leitura

- **Spec**: `spec.md` · **Lane**: infra · **Date**: 2026-08-16

## Constitution Check (governance/principles.md)

| Principle | Compliance |
|---|---|
| I. Spec-driven | ✅ Sete FRs; os de recusa (FR2, FR4) e o de prova (FR6) são exatamente o que a mutação exercita. |
| II. Human-governed orchestration | ✅ O guarda **não decide** nada de conteúdo: recusa três escritas que o método já proíbe por escrito e aponta a via correta. Nenhuma regra nova nasce aqui. |
| III. Reversibility / risk gates | ✅ É o eixo do ciclo. `--no-hooks` desliga; a camada é feita de arquivos comuns (sem symlink, lição do 052); `settings.json` alheio nunca é sobrescrito — sem conflito acrescenta, com conflito **recusa e imprime**; o guarda falha **aberto** para não travar repositório de terceiro. |
| IV. Test-first / verifiable DoD | ✅ O guarda nasce com casos que ele deve bloquear **e** casos que ele deve deixar passar, executados contra a cópia instalada pelo `check-installed.sh`. Guarda que nunca foi visto bloqueando não é guarda. |
| V. Context economy / boundary | ✅ O `@`-import é escolha de orçamento, medida e escrita: constituição **sim** (~1.518 tokens), modelo operacional **não** (~4.551). `scripts/hooks/` cai no domínio `toolkit`, já declarado. |
| VI. Living artifacts | ✅ O `SessionStart` imprime estado **medido na hora**; não há segunda cópia para envelhecer. O bloco do `CLAUDE.md` continua **gerado** das skills em disco, nunca escrito à mão. |
| VII. Light governance / YAGNI | ✅ Escopo do guarda deliberadamente igual ao das imutabilidades **já declaradas**. Segredo e `push --force` ficam fora, nomeados: regra nova + cobrança nova no mesmo ciclo esconde qual das duas errou. |
| VIII. Intelligible communication | ✅ Cada recusa diz a **via correta**, não só o "não": ADR novo que supersede, `record-decision.sh`, linha nova de estado. E o resumo do instalador declara que ligou a camada. |

## Artifacts of this cycle (declare all five — silence is not a decision)

<!-- Read by scripts/check-conformance.sh. Declaring =yes means the file MUST exist here.
     What each one is for: docs/governance/artifacts.md -->

| Artifact | Declaration | Why |
|---|---|---|
| `research.md` | `ART:research=no` | O mecanismo está na referência pública de hooks e foi conferido; o estado do repositório foi medido antes da spec e está na tabela dela. |
| `data-model.md` | `ART:data-model=no` | Nenhuma entidade nova com relações. |
| `contracts/` | `ART:contracts=yes` | Há **duas interfaces reais**: o JSON que o Claude Code entrega ao hook e o que o hook devolve para bloquear; e a forma da fusão do `settings.json` alheio. Interface entre partes é o caso que o catálogo prevê. |
| `checklist.md` | `ART:checklist=no` | Os critérios de aceite são executáveis e viram asserção; a lista seria a mesma tabela escrita duas vezes. |
| `ux-design.md` | `ART:ux-design=no` | Não toca tela. |

## How

**A camada.** `scripts/hooks/guard-immutables.py` (PreToolUse) e `scripts/hooks/session-state.sh`
(SessionStart), mais `.claude/settings.json` que os liga. Em inglês, porque `scripts/` é
superfície instalável (ADR 0014) e o `check-language.sh` cobre.

**O guarda.** Lê o JSON do evento na entrada padrão, olha o caminho alvo e recusa três coisas:
corpo de ADR **que já existe** (ADR novo passa), `docs/records/decisoes.jsonl` (a via é o
`record-decision.sh`) e card de ideia do ecossistema. Erro interno → **permite**, e escreve o
motivo em `stderr`: guarda quebrado não trava repositório alheio, e quem impede que ele passe
despercebido é o portão, não ele mesmo.

**O estado.** `session-state.sh` roda o que já existe — `check-conformance.sh`,
`check-retro.sh`, `git status` — e imprime o resultado. Nenhum fato novo: os mesmos fatos,
carregados em vez de lembrados.

**A fusão.** Sem `settings.json` no destino: escreve. Com, e sem `hooks`: acrescenta. Com
`hooks` já configurados: **recusa** e imprime o trecho a colar. Nunca `cp` por cima.

**O `@`-import.** O bloco gerado ganha `@docs/governance/principles.md`. Custo medido: 6.072 B,
~1.518 tokens por carregamento, em todo sessão daquele repositório. O `operating-model.md`
(18.207 B, ~4.551 tokens) **não** entra — declarado no fora de escopo com o número.

## Verification (DoD)

| Comando | Esperado |
|---|---|
| instalar em pasta limpa | harness ligado, e o resumo diz |
| **mutação 1**: guarda contra `docs/adr/0001-*.md` existente | bloqueia, apontando "novo ADR que supersede" |
| **mutação 2**: guarda contra `docs/records/decisoes.jsonl` | bloqueia, apontando `record-decision.sh` |
| **mutação 3**: guarda contra card de ideia | bloqueia |
| **contraprova 1**: guarda contra `specs/NNN/spec.md` | **permite** |
| **contraprova 2**: guarda contra ADR **novo** | **permite** |
| **mutação 4**: instalar sobre `settings.json` alheio com hooks | **recusa**, imprime o trecho, e o arquivo alheio fica intacto |
| **contraprova 3**: instalar sobre `settings.json` alheio **sem** hooks | acrescenta, preservando o resto |
| `--no-hooks` | instala o resto e diz que pulou |
| `scripts/check-installed.sh` | asserções novas verdes contra a cópia instalada |
| bateria de 16 portões · plugin · build | verdes |
