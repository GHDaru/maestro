# Plan 055 — Retro: o portão que mede a frase vira prova por mutação

- **Spec**: `spec.md` · **Lane**: plena · **Date**: 2026-08-16

## Constitution Check (governance/principles.md)

| Principle | Compliance |
|---|---|
| I. Spec-driven | ✅ Oito FRs (quatro deles vindos do parecer); os de reprovação são provados por mutação — e este ciclo é o primeiro obrigado pela regra que cria. |
| II. Human-governed orchestration | ✅ A retro é cerimônia humana: o `retro.sh` só pré-computa e não escreve nada. Fechar o achado é decisão registrada com motivo, não limpeza automática de fila. |
| III. Reversibility / risk gates | ✅ O ciclo **aperta** um portão e fecha um achado; nada apaga. A linha de fechamento é append-only, e desfazer é linha nova. |
| IV. Test-first / verifiable DoD | ✅ É o ponto do ciclo. A regra nova **é** a exigência de teste-primeiro aplicada ao próprio portão: quebrar de propósito e ver reprovar. |
| V. Context economy / boundary | ✅ Nada muda de domínio. O `TAIL:mutation` entra na superfície instalável pelo template, que já é território `toolkit` compartilhado. |
| VI. Living artifacts | ✅ O anti-padrão 23 entra com o ciclo de origem; o `docs/records/README.md` ganha a forma que faltava. Nenhum artefato novo para envelhecer. |
| VII. Light governance / YAGNI | ✅ Um token, uma função curta, um anti-padrão, uma seção de protocolo. O escopo de portão começou estreito demais — o parecer atravessou a lacuna com `boundary.json` e `sumario.json` — e agora cobre o que **é portão na prática**, com `companion/` explicitamente fora. |
| VIII. Intelligible communication | ✅ A mensagem de recusa diz o que fazer — *"break it on purpose and show it failing"* —, e o texto do template carrega a evidência (seis dos nove ciclos, nomeados) em vez de pedir obediência. |

## Artifacts of this cycle (declare all five — silence is not a decision)

<!-- Read by scripts/check-conformance.sh. Declaring =yes means the file MUST exist here.
     What each one is for: docs/governance/artifacts.md -->

| Artifact | Declaration | Why |
|---|---|---|
| `research.md` | `ART:research=no` | O material da retro é pré-computado pelo `retro.sh` e os seis casos estão nos `qa-report.md` dos ciclos 046–054. Nada a investigar. |
| `data-model.md` | `ART:data-model=no` | Nenhuma entidade: `TAIL:mutation` é mais um token na cauda existente. |
| `contracts/` | `ART:contracts=no` | Nenhuma interface nova; o contrato do índice de decisões ganha uma **forma** documentada, não um campo. |
| `checklist.md` | `ART:checklist=no` | Cinco critérios, três deles provados por mutação; a lista seria a mesma tabela escrita de novo. |
| `ux-design.md` | `ART:ux-design=no` | Não toca tela. |

## How

**O achado.** Fechado com linha `fecha` apontando para ele, o gatilho citado no título e o
motivo escrito: o remédio foi executado no 047, o resíduo virou gatilho, e gatilho não gera
evento de fechamento. A forma entra em `docs/records/README.md` para não depender de eu ter
pensado nisso hoje.

**A regra.** `TAIL:mutation` no `.specify/templates/tasks-template.md` — o artefato que o
executor consome, que é onde um passo obrigatório tem de morar (anti-padrão 22). O
`check-conformance.sh` passa a cobrá-lo a partir do ciclo 055, com três reprovações:

1. token ausente do `tasks.md`;
2. `n/a` num ciclo que **tocou** portão — e o "tocou" é lido do **diff**: os commits que
   citam `spec NNN` mais, para o ciclo em escrita, a árvore de trabalho. Ler o plano seria
   medir a frase dentro do portão feito para impedir isso;
3. aplicável e sem evidência no `qa-report.md` — reusa a máquina que já existe.

O conjunto de caminhos que conta como portão está numa constante nomeada e cobre o que é
portão **na prática** — `scripts/check-*.sh`, `package-plugin.sh`, `build.mjs`,
`sumario.json`, `boundary.json`, *workflows* da CI —, com `companion/` fora por ser outro
domínio. A primeira versão listava dois caminhos e o parecer atravessou a lacuna.

**O que o parecer arrancou depois disso**, cada um com mutação própria: `n/a` escrito `N/A`
ou separado por travessão comprava a dispensa; o piso podia ser posto em 999 (ou num
disparate como `abc`) e o portão imprimia sucesso; a atribuição por commit era
sensível a maiúscula, discordando do `check-cycle.sh`; e bastava abrir o **próximo** ciclo
para a árvore de trabalho do atual parar de contar. Além disso, o passo obrigatório existia
só no template — anti-padrão 22, o mesmo que o ciclo alega combater — e o gerador continuava
emitindo três.

**O anti-padrão 23** registra o defeito do ciclo 054, que é irmão do outro: porta nova aberta
sem estender o guarda que vigiava a antiga.

## Verification (DoD)

| Comando | Esperado |
|---|---|
| `scripts/check-retro.sh` | **verde** — zero achados abertos (o índice nunca esteve em zero no 047: eram três) |
| `scripts/check-conformance.sh` | verde com `TAIL:mutation` cobrado a partir de 055 |
| mutação 1: remover `TAIL:mutation` do `tasks.md` deste ciclo | `✗ tasks.md has no TAIL:mutation` |
| mutação 2: trocar por `n/a: nao mexi em portao` (mentira — o ciclo mexe) | `✗ TAIL:mutation says n/a, but this cycle changed a gate` |
| mutação 3: apagar a evidência do `qa-report.md` | `✗ TAIL:mutation … absent from qa-report.md` |
| mutação 4: `n/a` escrito `N/A:` e `n/a —` | **reprova igual** — a grafia não compra dispensa |
| mutação 5: `MAESTRO_MIN_CYCLE_MUTATION=999` | **falha** dizendo que o piso ficou acima do ciclo mais novo |
| mutação 6: `MAESTRO_MIN_CYCLE_MUTATION=abc` | **falha** de saída, sem aritmética quebrada |
| mutação 7: commit citando `(Spec 055)` com maiúscula | ainda é atribuído ao ciclo |
| mutação 8: abrir o ciclo 056 com a mudança de portão do 055 ainda por commitar | 055 **continua** cobrado |
| mutação 9: linha de tarefa citando `TAIL:review` em prosa | **não** é lida como a linha da cauda (FR7) |
| contraprova A: ciclo 054 e anteriores | **não** são cobrados de `TAIL:mutation` |
| contraprova B: `n/a` legítimo em ciclo sem portão | aceito, com o motivo impresso |
| `scripts/new-cycle.sh 056 <slug>` + `check-conformance.sh 056` | o ciclo nasce com o passo, não nasce vermelho |
| bateria de 16 portões · plugin · build | verdes |
