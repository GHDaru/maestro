# QA report 060 — A árvore que não mente

- **Date**: 2026-08-22 · **Lane**: plena · **Verdict**: aprovado após correção do parecer

## Fitness functions (DoD)

| Check | Expected | Result |
|---|---|---|
| link do README para a receita | resolve no GitHub **e** no site | ✅ título ASCII; `id="o-que-fica-no-seu-projeto-depois"` presente em `site/instalar-o-maestro.html` |
| `node publicar/build.mjs` | a árvore aparece no livro | ✅ 39 páginas; `grep -rl 'meu-app/' site/` → `instalar-o-maestro.html` |
| a árvore vive num lugar só (FR1) | uma cópia | ✅ `grep -rln 'meu-app/'` → **1** arquivo fora de `specs/` (o plugin foi reempacotado) |
| **mutação 1**: receita documenta `evals2/`, que nada cria | reprova | ✅ "documenta 'evals2/', que a instalação não cria" |
| **mutação 2**: receita deixa de citar `evals/` | reprova | ✅ "a instalação cria 'evals/' e a receita nunca menciona" |
| **mutação 3**: a árvore some da receita | reprova | ✅ "documenta nada" |
| **mutação 4**: receita deixa de citar `CLAUDE.md` | reprova | ✅ |
| **mutação 5**: título da receita renomeado | reprova a âncora do README | ✅ |
| **mutação 6**: receita regride para `--ai cursor` | reprova | ✅ nos **dois** sentidos numa só mutação |
| **mutação 7**: receita deixa de listar `codex` | reprova | ✅ |
| **mutação 8**: instalador ganha `gemini`, receita calada | reprova | ✅ |
| contagens publicadas × instalação real | iguais | ✅ 81 escritos / 82 em disco · `codex` 53 e **sem** `.claude/` · 9 `check-*.sh` · 13 agentes · 12 comandos · 6 skills · 12 templates |
| 13 portões bloqueantes (fora `check-installed`) | verdes | ✅ |
| `check-installed.sh` | verde | ✅ |
| `package-plugin.sh --verify` | em sincronia | ✅ 33 arquivos |
| `node publicar/build.mjs` | verde | ✅ 39 páginas, links internos OK |
| `check-cycle` · `check-conformance` (consultivos) | verdes | ✅ |
| `check-retro` (consultivo) | **vermelho, de propósito** | ⚠️ 5 achados abertos, limite 4. Os três deste ciclo foram indexados **em vez de** guardados fora do índice para manter um número verde: suprimir achado para não acender o gatilho é o defeito que o gatilho existe para pegar. **A retrospectiva está devida** — e o `achado-055` está com 5 de 6 ciclos. |

## Closing tail — the evidence

- **TAIL:review** — revisão independente em contexto fresco. **Reprovou: 20 achados.** Todos
  aplicados. Os que teriam custado mais caro:

  1. **A receita mandava usar ids que o instalador recusa.** `--ai cursor` e `--ai generic`
     morreram no ciclo 057, viraram `cursor-agent` e `codex`, e a receita nunca soube. Quem
     seguisse a página batia em `error: unknown agent 'cursor'` **no passo 0** — antes de
     qualquer coisa. Três ciclos de portões verdes sobre uma página que não instalava. Virou
     o T5: os dois conjuntos passam a ser comparados, como o `check-flags` faz com flags.
  2. **O passo 4 rodava os portões no diretório errado.** Depois do passo 2 o leitor está no
     clone do Maestro; os quatro comandos devolviam verde **do repositório do método**. É o
     `cd "$HERE"` do ciclo 058 outra vez, agora escrito em prosa em vez de em bash.
  3. **O portão da árvore media a instalação errada.** Comparava com `$TARGET`, que este mesmo
     script suja com `docs/adr`, `docs/records` e `docs/ecosystem` (fixture do guard) e onde a
     linha 50 escreve `CLAUDE.md` — então a asserção de `CLAUDE.md` **nunca podia falhar**, e
     tirar `docs/` do instalador deixaria o portão verde. Passou a ter fixture própria, feita
     por `maestro init` (que é o que a árvore documenta) e medida no instante em que nasce.
  4. **`[├└]` não é classe de caracteres**, é conjunto de **bytes**: em UTF-8 não casava nada
     e o portão dizia "nenhuma árvore encontrada". E `[a-zA-Z._-]` descartava todo nome com
     **dígito** — um `evals2/` documentado e inexistente era invisível. Alternação e classe
     com dígitos; a mutação 1 acima existe só para provar isso.
  5. **O plugin ficou fora de sincronia — pela quarta vez seguida.** Reempacotado.
  6. **As quatro caixas da cauda marcadas sem `qa-report`** — pela quarta vez nesta sessão.

- **TAIL:security** — classe de risco: **documentação mais leitura de arquivos do próprio
  repositório**. Nada aqui escreve em disco de terceiro, abre rede ou lê segredo. As duas
  fixtures novas nascem sob `mktemp -d` com `trap … EXIT`. O `python3` embutido no portão de
  âncoras recebe caminho e alvo como **argv**, nunca interpolados no fonte. Superfície nova de
  execução: zero.

- **TAIL:mutation** — oito mutações, todas reprovando (tabela acima). Duas encontraram defeito
  **meu**, escrito nesta sessão: o `echo` do portão novo com crases dentro de aspas duplas
  (`--ai: command not found`), e o cabeçalho da tabela — cuja primeira célula é `` `--ai` `` —
  lido como se fosse um id, o que fez o portão acusar *"a receita manda usar --ai --ai"*.
  Ancorar o id em letra descarta o cabeçalho e nada mais.

- **TAIL:gate** — pendente. DoD verde; falta o portão humano.

## Achados abertos deste ciclo

- **`achado-060-a-cauda-marcada-antes-da-evidencia`** — quarta ocorrência seguida de marcar as
  quatro caixas antes de existir `qa-report.md`. O `check-conformance.sh` é consultivo, então
  nada barra. Ou ele passa a bloquear, ou a caixa não é testemunha de nada.
- **`achado-060-changelog-com-quatro-secoes-adicionado`** — `[Unreleased]` tem quatro `###
  Adicionado` empilhados, um por ciclo. O formato Keep a Changelog pede **uma** por seção; do
  jeito que está, um leitor não distingue release de diário. Nenhum portão lê a estrutura.
- **`achado-060-o-banner-do-README-contava-portoes`** — resolvido aqui tirando a contagem
  duplicada, mas a classe continua: o README afirma números (13 agentes, 6 skills, 13 scripts)
  que ninguém compara com o disco. O `check-installed` já mede todos eles; falta ligar.
