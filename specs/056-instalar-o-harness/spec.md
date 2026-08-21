# Spec 056 — Instalar o harness: a regra deixa de depender de leitura

- **Status**: Concluída · **Raia**: infra · **Data**: 2026-08-16
- **Origem**: pedido do Steward — "precisamos ter um instalador para que o Maestro seja
  instalado no ambiente" —, com o relato de um agente de outro repositório que montou à mão
  `@`-import e hooks, e mediu o custo.

> **Raia**: infra, e infra **nunca é leve** mesmo parecendo pequena. **Ambiguidade** média:
> o mecanismo é conhecido, o que instalar por padrão num repositório de terceiro não era.
> **Raio**: todo repositório que instala o método, e — no caso do `PreToolUse` — o
> comportamento de **todos os agentes** que rodam lá. **Irreversibilidade**: é a mais alta
> que este instalador já teve; um hook mal escrito não estraga um arquivo, trava o trabalho.

## O quê e por quê

Instalar o Maestro hoje copia arquivos e **imprime** um bloco para o humano colar no
`CLAUDE.md`. Tudo o que o método exige chega como **texto que alguém precisa ler e lembrar**.

Medido neste repositório, antes de escrever qualquer coisa:

| Fato | Evidência |
|---|---|
| O `install-maestro.sh` não menciona `settings.json` nem `hooks` | `grep` devolve zero |
| O `CLAUDE.md` do próprio Maestro não tem um único `@`-import | `grep '^@'` devolve zero |
| Três artefatos são **declarados imutáveis** — corpo de ADR, linhas passadas de `decisoes.jsonl`, cards de ideia | `docs/governance/artifacts.md`, `docs/records/README.md` |
| **Nada mecânico impede reescrevê-los** | nenhum `check-*.sh` verifica imutabilidade; os que tocam esses caminhos conferem forma e índice |

O terceiro e o quarto, juntos, são o defeito que este repositório caça desde o ciclo 042 —
norma sem função de força — instalado no centro da própria governança. Um agente que reescreva
o corpo de um ADR não viola portão nenhum: viola só a frase que ele deveria ter lido.

Um hook `PreToolUse` **bloqueia a chamada da ferramenta**. É a primeira coisa neste método que
recusa *antes* de o dano existir, em vez de auditar depois.

## Requisitos funcionais

- **FR1**: O SISTEMA DEVERÁ instalar uma **camada de harness** — os scripts de hook e a
  configuração que os liga — junto com o resto do método.
- **FR2**: QUANDO um agente tentar escrever num artefato declarado imutável (corpo de ADR já
  existente, `docs/records/decisoes.jsonl`, card de ideia do ecossistema), O SISTEMA DEVERÁ
  **bloquear a chamada** e dizer qual é a via correta (novo ADR que supersede;
  `scripts/record-decision.sh`; linha nova de estado).
- **FR3**: QUANDO a sessão começar, O SISTEMA DEVERÁ imprimir o **estado medido** do método —
  ciclo em curso, conformidade, achados abertos com idade, dívida de retro, ramo e limpeza da
  árvore — em vez de deixar o agente reconstruir isso de memória (corolário C13).
- **FR4**: QUANDO o repositório de destino **já tiver** `.claude/settings.json`, O SISTEMA
  DEVERÁ preservá-lo: acrescenta o que falta quando não há conflito, e **recusa** quando há,
  imprimindo exatamente o que acrescentar à mão. Configuração de terceiro não se sobrescreve.
- **FR5**: O bloco de método DEVERÁ carregar a constituição por `@`-import, e o custo desse
  carregamento DEVERÁ estar **escrito aqui** — contexto automático é imposto a toda sessão
  daquele repositório, e imposto sem número é imposto sem decisão.
  > **Custo, medido em disco por `wc -c`, com o método declarado**: a estimativa de tokens é
  > **bytes ÷ 4**, aproximação grosseira e suficiente para decidir — não é contagem de
  > tokenizador. `docs/governance/principles.md` = **6.072 B ≈ 1.518 tokens**, e entra.
  > `docs/governance/operating-model.md` = **18.207 B ≈ 4.552 tokens**, e não entra.
- **FR6**: O guarda DEVERÁ ser **provado por um portão**, não pela confiança de que foi
  escrito certo: um caso que ele deve bloquear e um que ele deve deixar passar, executados
  contra a cópia instalada.
- **FR7**: O SISTEMA DEVERÁ oferecer `--no-hooks`, e **dizer no resumo** quando instalou a
  camada de harness. Mudança de comportamento de todos os agentes de um repositório não pode
  chegar em silêncio.

## Fora de escopo

- Bloquear segredo, `push --force` e caminho fora do repositório. São candidatos legítimos e
  **não** entram agora: o guarda começa nas três imutabilidades que o método **já declara**,
  onde a regra existe e só falta cobrança. Regra nova e cobrança nova no mesmo ciclo é como se
  descobre tarde que a regra estava errada.
- `@`-import do `operating-model.md` (**≈ 4.552 tokens**, mesmo método de medida do FR5). É
  referência consultada sob demanda, não regra que precisa estar sempre carregada. Fica de
  fora **com o número declarado**, para a decisão ser revisitável.
- Levar hooks no plugin (`plugin/maestro/`). O plugin distribui agentes, comandos e skills; o
  harness é do repositório, não do pacote.

## Critérios de aceite (DoD)

<!-- Sem caixas: esta seção diz o que deve valer; se valeu, quem diz é o qa-report. -->
- Numa pasta limpa, instalar entrega o harness ligado, e o resumo diz que entregou.
- O guarda **bloqueia** escrita em corpo de ADR existente, em `decisoes.jsonl` e em card de
  ideia; e **deixa passar** escrita em `spec.md`, `plan.md` e num ADR novo.
- Instalar sobre um `.claude/settings.json` alheio **não o destrói**: acrescenta sem conflito,
  recusa com conflito, e imprime o que fazer.
- `--no-hooks` instala tudo menos a camada de harness, e diz isso.
- Cada uma dessas recusas é **vista falhando** (`TAIL:mutation`), e as asserções vivem no
  `check-installed.sh`, que roda contra a cópia instalada.
- O custo do `@`-import está escrito, medido em bytes e tokens.
- Bateria completa, plugin e build verdes.

## Dívida herdada que este ciclo tocou, declarada

- `docs/handbook/07-cerimonias-cadencia.md` teve a data de revisão corrigida
  (`2026-08-07 → 2026-08-17`, ciclo `042 → 055`). **A correção pertence ao ciclo 055**, que
  acrescentou o anti-padrão 23 e não atualizou o cabeçalho. Ela aparece aqui porque o
  `check-chapters.sh` compara **datas de commit**, e a data do commit do 055 só passou a
  existir depois que o 055 fechou — então aquele ciclo passou com a bateria verde e deixou o
  portão vermelho para o seguinte. É defeito de desenho do portão, não descuido, e está
  registrado como achado. Consertar aqui em silêncio seria o que o parecer chamou de
  *drive-by* num diff de raia infra.

## Clarify

1. O guarda falha aberto ou fechado? → **Aberto em erro interno, e barulhento**: um guarda
   quebrado não pode travar o repositório alheio. O que impede o guarda quebrado de passar
   despercebido não é ele mesmo — é o portão do FR6, que o executa e exige que ele bloqueie.
2. Hooks por padrão ou por opção? → **Por padrão, declarado no resumo, com `--no-hooks`**.
   Copiar arquivo não é instalar (ciclo 048): se a regra é do método, ela chega ligada.
