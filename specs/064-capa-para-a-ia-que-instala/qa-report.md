# QA report 064 — Capa para a IA que instala

- **Data**: 2026-08-26 · **Raia**: leve · **Veredito**: DoD verde depois da revisão
  independente, que **reprovou** a primeira entrega. Falta o portão humano.

## Fitness functions (DoD)

| Verificação | Esperado | Resultado |
|---|---|---|
| 14 portões bloqueantes | todos código 0 | verde |
| `check-installed.sh` — ids em tabela | as duas páginas × `install-agents.tsv` | `✓ instalar-o-maestro.md … (4)` e `✓ README.md … (4)` |
| `check-installed.sh` — `--ai` em comando | as **três** páginas, o comando e não só a tabela | `✓ instalar-o-maestro.md (3)` · `✓ README.md (2)` · `✓ index.html (1)` |
| `check-installed.sh` — âncoras do README para si | resolvem | `✓ every README anchor into itself resolves to a heading (1)` |
| `check-installed.sh` — contagens | conferidas contra instalação real | 13 subagentes · 6 skills · 13 scripts · 9 portões · 12 comandos · 12 templates |
| `check-flags.sh` | toda flag que a página promete existe no parser | verde |
| `check-conformance.sh --ticked-only` | caixa marcada tem evidência | verde |
| `package-plugin.sh --verify` | plugin em sincronia | verde |

## Cauda de fechamento — a evidência

- **TAIL:review** — revisão independente em contexto fresco, por quem não escreveu o ciclo,
  sobre o commit `245abe2`: **reprovou a promoção**, com nove achados, dois deles bloqueantes.
  Sete corrigidos neste ciclo, dois registrados como dívida declarada. Detalhe abaixo.

#### O parecer

Veredito: **reprova a promoção** — nove achados, dois bloqueantes. Conferi os três
mais graves eu mesmo antes de aceitar o parecer; todos confirmam. Disposição de cada um:

| # | Achado | Disposição |
|---|---|---|
| 1 | O bloco publicado clonava para `/tmp/maestro` com as três linhas **soltas**: quando o clone falha porque o caminho existe, o `cd` e o `init` rodam mesmo assim, contra o que já estivesse lá. `/tmp` é gravável por qualquer um. **E o TAIL:security deste ciclo examinou exatamente isso e concluiu o contrário** | **corrigido** — comando encadeado por `&&`, clone para `~/maestro-toolkit` |
| 2 | `site/index.html` — a capa que o GitHub Pages serve — continuava publicando a forma sem `--yes`, que é a que o ciclo existe para aposentar. Nenhum portão lia essa página | **corrigido** — página alinhada, e agora sob portão (achado 3) |
| 3 | O portão de ids lia a **tabela** e não o **comando**. `--ai cursor` no bloco que o agente copia passava verde em tudo | **corrigido** — portão novo, três páginas |
| 4 | A evidência de FR4 citava `check-links.sh`, que descarta todo alvo `#…`. A âncora resolvia; a evidência é que era vácua | **corrigido** — portão novo de âncora para a própria página |
| 5 | "12 → 13 capítulos" foi corrigido à mão, sem função de forçamento | **dívida declarada** — `achado-064-contagem-de-capitulos-sem-portao` |
| 6 | "`init` faz quatro perguntas" — faz três; quatro são os passos | **corrigido** |
| 7 | `spec.md` e `qa-report.md` diziam que `check-flags` compara a prosa "nas duas direções"; compara em uma | **corrigido** — o texto passa a dizer o que o portão faz |
| 8 | "O que cai no seu projeto" só vale para `--ai claude`, e a página publica quatro ids | **corrigido** — a tabela diz de qual instalação fala |
| 9 | O extrator de tabela é frágil a indentação, negrito, maiúscula e cerca | **dívida declarada** — `achado-064-extrator-de-tabela-e-fragil-a-formatacao` |

O parecer também registrou o que verificou e achou **correto**: as três mutações da entrega
anterior reproduzem; ausência de tabela reprova nas duas páginas; não há caminho em que a
ausência vire silêncio pelo lado do fixture; FR1 medido (código 2, zero arquivos, mensagem
literal); o comando publicado funciona sem terminal, inclusive contra o clone público;
`check-install.sh` sai 0 nas quatro instalações; instalação sobre um `CLAUDE.md` existente
anexa em vez de sobrescrever; as contagens batem; e a bateria inteira está verde.

- **TAIL:security** — a primeira redação deste campo estava **errada** e a revisão a derrubou
  com um executável plantado; o defeito era meu e foi corrigido na raiz. Classe de risco do que
  sobra: baixa. Detalhe abaixo.

#### O que aconteceu

A primeira redação examinou o caminho `/tmp/maestro`, raciocinou que "o `git clone` recusa um
destino existente" e concluiu "nada a fazer". A recusa do clone é verdadeira e **irrelevante**:
as linhas não estavam encadeadas, então a linha seguinte executava
`/tmp/maestro/bin/maestro` de qualquer forma. A revisão provou com um executável plantado —
`PWNED: código de terceiro executado`, com o bloco saindo `0`. Foi eu quem introduziu o
caminho fixo, e a nota de segurança que deveria pegá-lo argumentou a favor dele.

Corrigido na raiz, não no sintoma: as três linhas agora são uma só, encadeada por `&&`, e o
clone vai para dentro da `$HOME` — que não é gravável por outro usuário da máquina. Classe de
risco do que sobra: **baixa**; a página não pede credencial, não expõe entrada de rede e não
executa código de terceiro.

- **TAIL:mutation** — dois portões novos neste ciclo, cada um quebrado de propósito e visto
  reprovando, com contraprova antes e depois; mais as três mutações da entrega anterior,
  repetidas e ainda reprovando. Tabelas abaixo.

#### As mutações

Dois portões novos neste ciclo, além do que a entrega anterior estendeu. Cada um quebrado de
propósito e visto reprovando, com contraprova antes e depois:

**Portão do `--ai` em comando** (três páginas):

| Mutação | O que o portão imprimiu |
|---|---|
| o comando do README manda usar `cursor` | `✗ README.md hands you '--ai cursor', and the installer refuses it` |
| a capa publicada manda usar `cursor` | `✗ index.html hands you '--ai cursor', and the installer refuses it` |
| a receita perde todo `--ai` | `✗ instalar-o-maestro.md hands out install commands and names no --ai at all` |

A primeira é literalmente o defeito que a revisão encontrou: antes, essa mutação saía **verde**
em `check-installed`, `check-flags` e `check-links` ao mesmo tempo.

**Portão das âncoras do README para si**: `](#instalar-o-maestro-no-seu-projeto)` trocado por
uma âncora inexistente →
`✗ README links to '#esta-ancora-nao-existe' on its own page, and no heading there produces that anchor`.
Antes desta mudança, a mesma mutação saía verde em `check-links.sh`, `check-installed.sh` e
`check-language.sh`.

Contraprova das duas, com as páginas intactas: `✓ … every --ai it hands you is one the
installer accepts` nas três, e `✓ every README anchor into itself resolves to a heading (1)`.

Também repetidas as três mutações da entrega anterior (id fantasma, tabela ausente, id
esquecido), todas ainda reprovando.

- **TAIL:gate** — portão humano concedido pelo Darú em 2026-10-13, no chat ("aprovo o gate do ciclo 064 (capa) e do 065, promova a dev para a main"): a `dev` com os três commits deste ciclo e os do ciclo 065 foi promovida para a `main` por `scripts/promote-main.sh`, que registra o gate em `decisoes.jsonl`. CI da `dev` verde no `8d38e8f`.

## Cobertura dos requisitos

- **FR1** — a página abre com o comando que funciona sem terminal e diz o que acontece sem a
  flag: código 2, zero arquivos, `no terminal to ask about which agent`.
- **FR2** — tabela de ids comparada nas duas direções contra `install-agents.tsv`.
- **FR3** — tabela ausente reprova, nas duas páginas.
- **FR4** — a bifurcação existe e a âncora resolve **sob portão** (não mais sob uma evidência
  que não media nada).
- **FR5** — a verificação publicada é `check-install.sh`, de dentro do projeto alvo.
- **FR6** — comando encadeado por `&&`; clone em `~/maestro-toolkit`, fora de `/tmp`.
- **FR7** — `site/index.html` publica a mesma forma, com a razão do `--yes` escrita.
- **FR8** — todo `--ai <valor>` das três páginas é comparado contra o TSV.
- **FR9** — âncoras do README para si mesmo sob portão.

## Achados abertos por este ciclo

- `achado-064-contagem-de-capitulos-sem-portao` — nenhuma contagem de capítulos anunciada numa
  página é comparada contra `docs/handbook/`. Tem uma pergunta de modelagem real: o PDF foi
  commitado em 2026-07-27, antes do capítulo 13 existir, então "capa + 12 capítulos" é
  **verdade** sobre o PDF e mentira sobre o diretório. Um portão ingênuo reprovaria as duas
  frases verdadeiras. Corrigido à mão, neste ciclo, o único que falava do diretório
  (`site/roadmap.html`).
- `achado-064-extrator-de-tabela-e-fragil-a-formatacao` — indentação, negrito, maiúscula e
  cerca fazem o extrator descrever a página errado, nas duas direções.

Um erro de processo, sem achado porque não é do repositório: usei `git checkout README.md`
para desfazer uma mutação com a reescrita ainda **não estagiada**, e `git checkout <path>`
restaura do índice — apagou o trabalho. Refeito a partir do rascunho; daí em diante, mutação
com cópia de arquivo. A revisão independente recebeu a mesma instrução e a seguiu.

## Portão pendente

- A promoção `dev` → `main` aguarda aprovação humana.
