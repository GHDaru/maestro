# Plan 058 — A porta da frente: `maestro init`

- **Spec**: `spec.md` · **Lane**: infra · **Date**: 2026-08-17

## Constitution Check (governance/principles.md)

| Principle | Compliance |
|---|---|
| I. Spec-driven | ✅ Sete FRs; os de recusa (FR3, FR6) são o que a mutação exercita, e o FR5 obriga o próprio comando a provar em vez de afirmar. |
| II. Human-governed orchestration | ✅ `init` **pergunta** quando há alguém para responder e **não pergunta** quando não há: o humano decide, o agente não é obrigado a fingir que é um. |
| III. Reversibility / risk gates | ✅ Nada de novo é escrito no alvo: `init` chama o instalador, que já não sobrescreve, tem `--dry-run` e guarda de symlink. O comando novo não ganha poder novo. |
| IV. Test-first / verifiable DoD | ✅ O portão de flags nasce **acusando** — encontrou quatro divergências reais na primeira execução, três delas anteriores a este ciclo e uma dele mesmo. |
| V. Context economy / boundary | ✅ `bin/` entra no `boundary.json` como `toolkit` e no `check-language.sh`: é a primeira frase em inglês que alguém lê. |
| VI. Living artifacts | ✅ `init` **não reimplementa** nenhum passo — despacha para o script que já é dono dele. E o portão de flags impede que a documentação envelheça longe do código, que é como as três mentiras nasceram. |
| VII. Light governance / YAGNI | ✅ Um despachante e um portão. Distribuição por gerenciador de pacotes fica **fora**, nomeada: é custo de manutenção próprio, e o gatilho é alguém pedir. |
| VIII. Intelligible communication | ✅ É o ponto do ciclo. Quatro passos numerados, a tabela de agentes na tela, o veredito no fim, e um banner que carrega a versão — banner com versão errada é a primeira coisa que alguém nota. |

## Artifacts of this cycle (declare all five — silence is not a decision)

<!-- Read by scripts/check-conformance.sh. Declaring =yes means the file MUST exist here.
     What each one is for: docs/governance/artifacts.md -->

| Artifact | Declaration | Why |
|---|---|---|
| `research.md` | `ART:research=no` | O modelo (`specify init`) já foi medido no ciclo 057 e está citado; os três defeitos de documentação foram medidos antes da spec e estão na tabela dela. |
| `data-model.md` | `ART:data-model=no` | Nenhuma entidade nova: `init` consome a tabela de agentes do 057 e não cria estado próprio. |
| `contracts/` | `ART:contracts=no` | Nenhuma interface entre partes: o despachante chama scripts com os argumentos que eles já aceitam. |
| `checklist.md` | `ART:checklist=no` | Os critérios são executáveis e viram asserção. |
| `ux-design.md` | `ART:ux-design=no` | Não é interface gráfica. O desenho de terminal — quatro passos, tabela, veredito — está descrito aqui e provado pela execução não-interativa. |

## How

**`bin/maestro`** — despachante puro. `init`, `check`, `cycle`, `conformance`, `retro`,
`promote`, `agents`, `version`; cada um chama o script existente. Sem argumento, imprime o que
sabe fazer.

**`maestro init`** — quatro passos: (1) escolher o agente, com a tabela do 057 impressa;
(2) o destino, criando se preciso; (3) instalar com `--write-block`; (4) **rodar
`check-install.sh` dentro do alvo** e dizer o veredito, saindo diferente de zero se falhar.
Sem TTY não pergunta: usa o declarado, e `--yes` responde por quem não está lá.

**`scripts/check-flags.sh`** (17º portão, bloqueante na CI) — compara as flags que o `case`
aceita com as documentadas, em **dois modos**: referência (`# Usage`, `usage()`) nos dois
sentidos; prosa (receita, README) só no sentido "toda flag citada existe". O extrator ignora o
`-*)` (que recusa, não aceita), lê listas com atalho curto (`--yes|-y`) e **exige que o padrão
do `case` não tenha espaços** — sem isso, prosa com parênteses era lida como parser e uma flag
inventada se auto-anulava. Flags de **outros** comandos citados na documentação (`ln -s`) são
uma lista declarada e visível, não um regex frouxo.

**A porta rápida** — a capa do site ganha "Instalar agora" e três comandos, ao lado de "Entrar
no livro". O livro convence; a porta serve quem já foi convencido.

## Verification (DoD)

| Comando | Esperado |
|---|---|
| `maestro` sem argumento | lista os subcomandos, sai 0 |
| `maestro init <dir> --ai claude --yes` sem TTY | instala, escreve o bloco, **verifica**, e não pergunta nada |
| `maestro init … --ai codex --no-hooks --yes` | idem, sem camada de hooks |
| `maestro init … --ai <inválido>` | recusa, exit 2, nada escrito |
| **mutação 1**: flag no parser sem documentação | portão **reprova** |
| **mutação 2**: flag documentada e inexistente | portão **reprova** |
| **mutação 2b**: `--forcar` de volta na receita **e** no README | reprova nos dois |
| **mutação 2c**: `# Usage` esvaziado (a mentira nº 3) | reprova |
| **mutação 2d**: flag curta `-q)` sem documentação | reprova |
| **mutação 3**: subcomando reimplementando passo | revisão independente cobra (não é mecanizável) |
| capa do site | "Instalar agora" leva à receita em **um** clique |
| bateria de 17 portões · plugin · build | verdes |
