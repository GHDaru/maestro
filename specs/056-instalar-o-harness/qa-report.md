# QA report 056 — Instalar o harness

- **Date**: 2026-08-17 · **Lane**: infra · **Verdict**: aprovado após correção do parecer

## Fitness functions (DoD)

| Check | Expected | Result |
|---|---|---|
| instalação limpa | camada instalada, resumo declara | ✅ dois hooks + `settings.json`, ambos `-rwxr-xr-x` |
| reinstalar | não conflitar consigo | ✅ `= already current` |
| `settings.json` alheio **sem** hooks | acrescenta, preserva o resto | ✅ `model` e `permissions` intactos |
| `settings.json` alheio **com outros** hooks | recusa, arquivo byte a byte intacto, *snippet* válido | ✅ sha256 igual; *snippet* passa em `json.tool` |
| `settings.json` **não gravável** | instalação **completa**, manifesto escrito | ✅ (antes: morria no arquivo 78 e órfãava tudo) |
| `--no-hooks` sobre instalação existente | não apaga hooks vivos | ✅ `left as they were` |
| `--dry-run` | nada escrito, contadores em zero, tempo futuro | ✅ |
| guarda: ADR **commitado** · `decisoes.jsonl` · card commitado | recusa | ✅ ✅ ✅ |
| guarda: symlink para ADR commitado | recusa | ✅ |
| guarda: caminho em maiúsculas | recusa | ✅ |
| guarda: ADR **novo** · `specs/**` · `docs/handbook/**` | permite | ✅ ✅ ✅ |
| guarda: `docs/adr/` de **outro repositório** | não julga | ✅ |
| `session-state.sh` em repo **sem commit** | uma linha coerente | ✅ (antes: `branch: HEAD` + `?` em duas linhas) |
| bateria de 16 portões · plugin · build | verdes | ✅ |

## Closing tail — the evidence

- **TAIL:review** — revisão independente em contexto fresco, instruída a refutar e a executar
  os ataques. **Reprovou o ciclo: 24 achados, 9 bloqueantes.** Um ciclo de raia infra que
  instala em repositório de terceiro, entregue por mim com nove buracos. Os que mais doem:

  1. **O instalador podia morrer no meio e órfãar a instalação para sempre.** A escrita do
     `settings.json` era um redirect cru sob `set -e`. Com o arquivo somente-leitura, o script
     morria **depois de 78 arquivos e antes do manifesto**; a execução seguinte via
     "instalação anterior ao manifesto", gravava um manifesto **vazio** e desconhecia os 77
     arquivos do método — para sempre. É exatamente a falha que o manifesto do ciclo 051
     existe para impedir, reintroduzida pelo bloco novo.
  2. **`--no-hooks` numa instalação existente APAGAVA os hooks** e deixava o `settings.json`
     apontando para arquivos que não existem mais — e o resumo dizia "skipped". Toda escrita
     naquele repositório passaria a invocar comando inexistente.
  3. **Um espaço no caminho do projeto desligava o guarda em silêncio.** O comando não estava
     entre aspas: em `~/My Projects/…` o hook saía 127, que o `PreToolUse` trata como erro
     não-bloqueante. O guarda ficava inerte enquanto o `CLAUDE.md` instalado no mesmo
     repositório afirmava que ele protegia.
  4. **Reinstalar sempre conflitava com a própria instalação anterior** — o `settings.json` é
     escrito por `cp` e nunca entra no manifesto, então o merge via os nossos próprios hooks e
     recusava. O harness não podia ser atualizado nunca.
  5. **O guarda bloqueava autoria legítima de ADR.** Ele tratava "o arquivo existe" como
     imutável; escrever um ADR em duas chamadas — corrigir um erro de digitação, preencher
     Consequências — era recusado a partir da segunda.
  6. **Três bypasses por symlink**, todos executados pelo revisor: `normpath` é lexical e não
     resolve link. O instalador aprendeu essa lição no ciclo 052; o guarda, não.
  7. **O portão provava o script e nunca a fiação.** Apagar o `settings.json` ou o
     `session-state.sh` deixava **tudo verde**: um guarda que ninguém chama passava no portão
     que existe para provar que ele é chamado.
  8. **O bloco escrito no `CLAUDE.md` do destino afirmava a proteção mesmo quando ela não era
     instalada** (`--no-hooks`, conflito, símlink). Norma sem função de força, invertida em
     função de força inexistente afirmada — o defeito que a spec diz combater.
  9. **O *snippet* "exato para colar" era JSON inválido** — 7 `{` contra 8 `}`.

  Mais quinze menores, todos corrigidos: bypass em filesystem insensível a maiúsculas;
  sobre-bloqueio de outros repositórios e *checkouts* aninhados; contadores mentindo em
  `--dry-run`; o `estado.jsonl` declarado append-only e **não** guardado, com a recusa do card
  apontando justamente para ele; a justificativa do `Bash` cobrindo um artefato e usada para
  três; `session-state.sh` emitindo duas linhas quebradas em repositório sem commit; o
  `chmod +x` que não alcançava o `.py`; a asserção casando espaço de `json.dump` em vez de
  parsear; o helper de merge sendo enviado a destinos que nunca o chamam; os números do
  `@`-import fora da spec e discordando entre si (4.550 × 4.551 × 4.552); campos errados no
  contrato (`ask`, `source`, `path`); a promessa falsa de "byte a byte" no merge; as caixas
  T1–T7 desmarcadas com o trabalho pronto; e um *drive-by* não declarado.

  **Não refutado**: as recusas do merge (CONFLICT deixa o arquivo idêntico por sha256), a
  normalização de travessias comuns, o conjunto de falsos positivos, a concordância entre
  `WRITE_TOOLS` e o *matcher*, o caminho do `@`-import, e o comportamento de falhar aberto.

- **TAIL:security** — classe de risco: **a mais alta que este instalador já teve**. Ele passa
  a escrever configuração que muda o comportamento de **todos os agentes** de um repositório
  alheio. Superfície e mitigação: (a) `settings.json` de terceiro **nunca** é sobrescrito —
  quatro estados, três deles recusa; (b) a escrita é atômica (`tmp` + `mv`) e **não pode
  matar a execução**, que era o vetor real de dano; (c) o guarda é confinado ao repositório —
  o revisor provou que ele julgava `docs/adr/` de outros *checkouts*, e não julga mais;
  (d) `escapes_via_symlink` cobre o caminho do `settings.json`. **Limites declarados**: o
  `Bash` não é guardado (com razão positiva só para o índice de decisões), o `estado.jsonl`
  não é guardado (não tem script de append; virou achado), e o guarda **falha aberto** de
  propósito — quem impede que isso passe é o portão, não ele.

- **TAIL:mutation** — o ciclo mexe em `check-installed.sh`, portanto a prova é obrigatória.
  Executadas em cópia da árvore, cada uma **vista reprovar**: guarda que permite tudo → 3 ✗;
  guarda que bloqueia tudo → 2 ✗; guarda apagado → ✗; guarda sem bit de execução → ✗;
  **`settings.json` apagado → ✗**; **`settings.json` sem o `PreToolUse` → ✗**;
  **`session-state.sh` apagado → ✗**. As três últimas são as asserções que o parecer
  provou não existirem: antes delas, o harness podia ser inteiramente desconectado com a
  bateria verde.

- **TAIL:gate** — DoD verde, 16 portões verdes, plugin em dia, livro em 39 páginas, e o
  método **instalado no próprio Maestro**: o `CLAUDE.md` deste repositório passou a carregar o
  bloco gerado, com o `@`-import da constituição. **Aguarda o gate humano.**

## Requirement coverage

- **FR1/FR7** — camada instalada com o resto, `--no-hooks` disponível e o resumo declara o
  estado real em sete formas distintas.
- **FR2** — recusa nos três artefatos, sempre nomeando a via correta.
- **FR3** — `SessionStart` imprime estado medido; o portão agora exige que ele exista e rode.
- **FR4** — `settings.json` alheio preservado; quatro estados, provados um a um.
- **FR5** — `@`-import da constituição, com custo e **método de medida** escritos na spec.
- **FR6** — o guarda é provado por portão nas duas direções, e agora a **fiação** também.

## Achados abertos neste ciclo

- `achado-056-portao-de-capitulos-nao-dispara-no-proprio-ciclo` — o `check-chapters.sh`
  compara datas de **commit**, que só existem depois do ciclo fechar. O 055 passou verde e
  deixou o vermelho para o 056.
- **`docs/ecosystem/estado.jsonl` é declarado append-only e não tem guarda nem script de
  append.** Guardá-lo hoje bloquearia a única via de registro. Fica nomeado no próprio guarda
  e aqui, em vez de meio-consertado.

## Pending gate

- Promoção `dev` → `main` aguarda aprovação humana (055 e 056).
