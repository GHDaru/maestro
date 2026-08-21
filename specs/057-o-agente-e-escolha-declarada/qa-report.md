# QA report 057 — O agente é escolha declarada

- **Date**: 2026-08-17 · **Lane**: infra · **Verdict**: aprovado após correção do parecer

## Fitness functions (DoD)

| Check | Expected | Result |
|---|---|---|
| `--ai list` | imprime as quatro linhas | ✅ |
| `--ai list` **com alvo** | recusa (listar não é instalar) | ✅ (antes: imprimia e saía 0 — instalação virava no-op com sucesso) |
| `--ai <desconhecido>` | recusa listando os válidos | ✅ exit 2 |
| `--ai` seguido de flag · tabela ausente | erro nomeado | ✅ |
| CRLF na tabela | **não** desliga a camada | ✅ (antes: `harness` virava `yes\r` e o Claude perdia os hooks em silêncio) |
| `--ai claude` | comandos, agentes e harness | ✅ |
| `--ai copilot` · `cursor-agent` · `codex` | bloco no arquivo do agente; **sem** `.claude/*` | ✅ os três, `check-install.sh` verde neles |
| `.maestro/install-options.json` | JSON válido, com o **fato** | ✅ escrito por escritor de JSON, não `printf` |
| `.specify/init-options.json` | concorda com a nossa escolha | ✅ (antes: dizia `claude` em toda instalação) |
| `--write-block` repetido | `already current` | ✅ (antes: recusava a **própria** saída) |
| `--write-block` com bloco diferente | recusa, arquivo intacto | ✅ |
| `--write-block` / opções **através de symlink** | recusa | ✅ (antes: escrevia **fora** do alvo) |
| bloco por último no arquivo · heading seguinte com `M` | comparação correta | ✅ |
| `--dry-run` | nada escrito, contadores em zero | ✅ |
| bateria de 16 portões · plugin · build | verdes | ✅ |

## Closing tail — the evidence

- **TAIL:review** — revisão independente em contexto fresco, instruída a refutar e a executar.
  **Reprovou o ciclo: 16 achados.** Os que mais doem:

  1. **Reabri o buraco do ciclo 052.** `--write-block` e a escrita do arquivo de opções eram
     as **duas únicas** escritas do script que não passavam pelo `escapes_via_symlink`. O
     revisor provou: com `AGENTS.md` apontando para fora, o bloco foi acrescentado **fora do
     alvo**, e o resumo disse "appended", com `refused 0`.
  2. **A recusa que dá nome ao ciclo gritava lobo contra o próprio produto.** A extração do
     bloco era um `sed` de faixa que **nunca terminava** quando o bloco era a última coisa do
     arquivo — então `sed '$d'` comia a última linha real. Resultado: instalar duas vezes com
     `--write-block` recusava a própria saída byte a byte idêntica, e inflava `refused` a cada
     execução limpa.
  3. **Uma instalação correta de Copilot ficava vermelha para sempre.** O `check-install.sh`
     tinha `CLAUDE.md AGENTS.md` no código, ignorando o campo `instruction` que este mesmo
     ciclo criou "para o projeto não precisar da tabela para saber onde está a instrução".
  4. **`.claude/agents` continuava indo para todo agente** — a spec abre acusando exatamente
     isso, e eu só tinha tratado `.claude/commands`.
  5. **Um CRLF na tabela desligava a camada inteira do 056**, com o resumo explicando que o
     Claude Code não roda hooks. O leitor do manifesto, 90 linhas acima, tira `\r` e explica
     por quê; o leitor novo não tirava.
  6. **Dois arquivos, o mesmo fato, contradizendo** — no ciclo cujo FR7 é sobre isso:
     `.maestro/install-options.json` dizia `codex` e o `.specify/init-options.json` enviado
     ao lado dizia `claude`.
  7. **"Lido do upstream" era falso em duas das quatro linhas**: o `generic` do upstream não
     mapeia arquivo nenhum, e o id do Cursor lá é `cursor-agent`. E "27 agentes" eram 26.
  8. **Quatro dos seis "invariantes" do `data-model` não eram cobrados por nada** — eram
     frases. Uma linha de quatro campos fazia o agente sumir de `--ai list` **e** de
     `--ai <id>`, sem aviso.
  9. **O ramo `copy_as` para diretório de comandos não-Claude morria** com um subdiretório:
     `hash_of` num diretório, sob `pipefail`, matava a instalação **sem manifesto** — a falha
     que o manifesto existe para impedir, num ramo que nenhuma linha da tabela exercitava.
  10. **Nenhum teste** havia sido escrito para nada deste ciclo, enquanto a spec dizia
      "acrescentar é uma linha **e um teste**".

  Corrigidos também: o motivo do FR5 sobrescrito pelo ramo `--no-hooks`; o campo `harness`
  gravando a flag em vez do fato; a dica `ln -s CLAUDE.md AGENTS.md` impressa para agentes que
  não usam nenhum dos dois; JSON sem escape; e o `AGENTS.md` simbólico fazendo o portão
  reportar a mesma divergência duas vezes.

  **Não refutado**: `--ai` chegando a `awk`/`grep` como padrão (é comparação literal — o
  revisor tentou `.*`, `claude$`, metacaracteres e barra invertida), nenhuma regressão dos
  consertos do 056, e o parser de argumentos reescrito não introduziu caminho destrutivo.

- **TAIL:security** — classe de risco alta: o ciclo decide **onde** escrever em repositório de
  terceiro. Superfície e mitigação: (a) as duas escritas novas passaram a respeitar o guarda
  de symlink — era o vetor real, e estava aberto; (b) `--ai` é comparado por **igualdade
  literal** em `awk`, nunca interpretado como padrão; (c) o arquivo de opções é gerado por
  escritor de JSON, então aspas e barras invertidas em qualquer campo não produzem mais um
  arquivo ilegível; (d) id desconhecido recusa **antes** de tocar o disco. **Limite
  declarado**: o `--dry-run` ainda cria `docs/records/decisoes.jsonl` no alvo — defeito
  anterior a este ciclo, confirmado pelo revisor em `git show HEAD`, e não corrigido aqui para
  não virar *drive-by* num diff de raia infra.

- **TAIL:mutation** — o ciclo mexe em `check-install.sh` e `check-installed.sh`, então a prova
  é obrigatória. Vistas reprovando: `--ai` desconhecido · linha removida da tabela · bloco
  divergente · gerador ausente (**diz que não comparou**, em vez de passar quieto) · linha de
  quatro campos · `harness=YES` fora do vocabulário · id duplicado · CRLF · instalação codex
  carregando formato do Claude · `--write-block` não idempotente.

  **E a mutação achou um defeito meu, de novo.** O teste de idempotência falhava sozinho:
  eu havia escrito `... | grep -q 'already current'` — `grep -q` fechando um cano sob
  `pipefail`, que faz o instalador tomar SIGPIPE e a condição ler `false` para sempre. É o
  **anti-padrão 21**, quarta aparição neste repositório, escrita por mim dentro do ciclo cujo
  portão existe para pegar essa classe. Corrigido capturando numa variável.

- **TAIL:gate** — DoD verde, 16 portões verdes, plugin em dia, livro em 39 páginas, e os
  quatro agentes instalam e passam no `check-install.sh` dentro do alvo. **Aguarda o gate
  humano.**

## Requirement coverage

- **FR1/FR6** — `--ai <id>` e `--ai list`; a escolha gravada e legível depois.
- **FR2** — a tabela é a fonte, e agora é **validada** por portão, não por prosa.
- **FR3** — id desconhecido recusa antes de escrever; `--ai list` com alvo também.
- **FR4** — comandos, agentes e bloco nos caminhos do agente; nada onde a célula é `-`.
- **FR5** — harness só onde a tabela permite, com o motivo certo — inclusive o caso incômodo
  de uma camada **viva** herdada de instalação anterior, que agora é declarada em vez de negada.
- **FR7** — bloco instalado × bloco gerado **para aquele agente**, com extração correta.

## Pending gate

- Promoção `dev` → `main` aguarda aprovação humana.
