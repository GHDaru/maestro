# Plan 057 — O agente é escolha declarada, não suposição do instalador

- **Spec**: `spec.md` · **Lane**: infra · **Date**: 2026-08-17

## Constitution Check (governance/principles.md)

| Principle | Compliance |
|---|---|
| I. Spec-driven | ✅ Sete FRs; os de recusa (FR3, FR7) e o de silêncio proibido (FR5) são o que a mutação exercita. |
| II. Human-governed orchestration | ✅ O agente vira **escolha explícita de quem instala**, gravada em arquivo. Hoje o instalador decide por todo mundo, calado — que é o oposto. |
| III. Reversibility / risk gates | ✅ Nada é sobrescrito: o bloco só é escrito com `--write-block`, e mesmo assim **acrescenta se não houver, recusa se houver outro** — a regra que o `settings.json` ganhou no 056. `--ai` desconhecido recusa antes de tocar em disco. |
| IV. Test-first / verifiable DoD | ✅ Cada recusa nasce com mutação, e o FR7 é um portão novo que compara **bloco instalado × bloco gerado**. |
| V. Context economy / boundary | ✅ Nenhum domínio novo: a tabela vive em `scripts/`, já `toolkit`. O que muda é **onde** o arquivo é escrito, não o conteúdo. |
| VI. Living artifacts | ✅ É o ponto do FR7: hoje o bloco instalado e o bloco gerado podem divergir em silêncio — mesma família do `check-version.sh`, um fato dito em dois lugares sem nada comparando. |
| VII. Light governance / YAGNI | ✅ **Quatro** agentes, não os 27 do upstream: o custo de um agente não é a linha, é **testar** que a instalação funciona lá. E `script: sh\|ps` do upstream fica fora, sem uso e sem dor. |
| VIII. Intelligible communication | ✅ `--ai list` mostra a tabela sem ler código; a recusa por id inválido **lista os válidos**; e o resumo diz **por que** o harness não foi instalado, em vez de omiti-lo. |

## Artifacts of this cycle (declare all five — silence is not a decision)

<!-- Read by scripts/check-conformance.sh. Declaring =yes means the file MUST exist here.
     What each one is for: docs/governance/artifacts.md -->

| Artifact | Declaration | Why |
|---|---|---|
| `research.md` | `ART:research=no` | O modelo do upstream foi medido e está citado na spec (arquivo, campos, mapeamento de 27 agentes). Nada em aberto. |
| `data-model.md` | `ART:data-model=yes` | Há entidade e relações de verdade: **agente** (id, nome, arquivo de instrução, diretório de comandos, suporta harness) e a **escolha gravada**, que aponta para um id da tabela. É a tabela que o instalador lê e o portão confere. |
| `contracts/` | `ART:contracts=no` | Nenhuma interface entre partes além da tabela, que é o `data-model`. |
| `checklist.md` | `ART:checklist=no` | Os critérios já são executáveis e viram asserção. |
| `ux-design.md` | `ART:ux-design=no` | Não toca tela. |

## How

**A tabela.** `scripts/install-agents.tsv` — cinco colunas, comentário explicando cada uma.
Os arquivos de instrução foram **lidos do upstream vendorizado**, não inventados. Onde o
formato de comandos não foi verificado, a célula é `-` e **nada é instalado ali**: derramar
`.claude/commands` num repositório de Copilot é enviar arquivo que ninguém lê (anti-padrão 22).

**A escolha.** `--ai <id>`, padrão `claude`. Id fora da tabela → recusa listando os válidos.
`--ai list` imprime a tabela. A escolha é gravada em `.maestro/install-options.json`, ao lado
do manifesto, com a forma do `init-options.json` do upstream mais o que é nosso
(`harness`, `maestro_version`).

**O harness.** Instalado só quando a coluna diz `yes`. Para os outros, o resumo diz
*"hooks são mecanismo do Claude Code"* — e o bloco gerado, que desde o 056 já consulta
`HOOKS_ACTIVE`, cai sozinho na redação honesta.

**O bloco.** Continua sendo **impresso** por padrão. `--write-block` acrescenta ao arquivo do
agente escolhido **se não houver bloco do Maestro**, e **recusa** se houver um diferente.

**O portão (FR7).** `check-install.sh` passa a comparar o bloco que está no arquivo de
instrução com `install-maestro.sh --block`. Divergência reprova.

## Verification (DoD)

| Comando | Esperado |
|---|---|
| `--ai list` | imprime as quatro linhas |
| `--ai inexistente` | **recusa**, listando os válidos, sem tocar em disco |
| `--ai claude` | comandos em `.claude/commands`, harness instalado |
| `--ai copilot` · `cursor` · `generic` | bloco apontado ao arquivo daquele agente, **sem** comandos, **sem** harness, e o resumo diz o motivo |
| `.maestro/install-options.json` | legível depois, com o id escolhido |
| `--write-block` em arquivo sem bloco | acrescenta |
| `--write-block` com bloco **diferente** | **recusa**, arquivo intacto |
| `check-install.sh` com bloco divergente | **reprova** (FR7) |
| mutação de cada recusa acima | vista falhando |
| bateria de 16 portões · plugin · build | verdes |
