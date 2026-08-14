# QA report 053 — Peças de apresentação: o fluxo v5 e o caderno de desenvolvimento

- **Date**: 2026-08-14 · **Lane**: leve · **Verdict**: aprovado após correção do parecer

## Fitness functions (DoD)

| Check | Expected | Result |
|---|---|---|
| números afirmados nas peças | conferem com o disco | ✅ `ls .claude/agents \| wc -l` = 13 · `ls .claude/commands \| wc -l` = 12 · `ls -d skills/*/ \| wc -l` = 6 · `ls .specify/templates \| wc -l` = 12 · `ls scripts/check-*.sh \| wc -l` = 16 · bloqueantes na CI = 13 |
| limiares da retro citados | 4 achados abertos / 6 ciclos | ✅ `scripts/check-retro.sh:20-21` |
| `scripts/check-links.sh` | verde | ✅ |
| `scripts/check-boundary.sh` | verde — nenhum órfão | ✅ as duas peças caem em `guide`, já declarado |
| bateria de 16 portões | verdes salvo os declarados abaixo | ✅ |
| `scripts/package-plugin.sh --verify` | em dia | ✅ 33 arquivos |
| `node publicar/build.mjs` | build do livro verde | ✅ 38 páginas, links internos OK |
| esqueleto do HTML | tags balanceadas, **nenhum recurso externo**, 18 slides | ✅ conferido, e reconferido pela revisão |

### Os vermelhos, declarados

- `check-retro.sh` — **vermelho por dívida real, e não deste ciclo**:
  `achado-047-cinco-absorcoes-sem-destino` completou **6 ciclos** aberto, que é o limite.
  A retro passou de recomendada a devida; é o próximo ciclo, não um item deste. Registrado
  aqui para que a dívida não passe como ruído de bateria.

## Closing tail — the evidence

- **TAIL:review** — revisão independente em contexto fresco, por quem não executou, com a
  instrução de **refutar**. Reprovou o ciclo: **oito grupos de defeito**, todos da mesma
  família — **afirmação sem lastro no disco**, que é o que o anti-padrão 13 vira num ciclo
  de documentação. Os quatro que mais custariam:

  1. O caderno mandava rodar `scripts/check-installed.sh` "no seu repositório". Esse script
     **não é instalado** (não está na lista do `install-maestro.sh:217`) e é um meta-portão
     da fonte: ele instala num `mktemp -d`. O certo é `check-install.sh`, que o próprio
     instalador indica. → corrigido.
  2. O caderno dizia que a instalação **escreve** o bloco de método no `CLAUDE.md`. Ela
     **imprime** o bloco (`--block >> CLAUDE.md`); quem acrescenta é o humano. Pior: essa é
     exatamente a conflação que o `check-install.sh` existe para impedir — *copiar arquivo
     não é instalar*. → corrigido, com a distinção agora dita em voz alta no slide.
  3. A lacuna 01 da peça 06 afirmava que "não existe fila nem critério de entrada". O
     `docs/roadmap.md` tem fases ordenadas por dependência (§7) e uma tabela de **gatilhos
     abertos**, cada decisão adiada com a condição que a reabre. Existe fila; o que não
     existe é dono por item e elo com o ciclo que abre. → reescrita para conceder o que há
     antes de pedir o que falta.
  4. A lacuna 02 citava `grep -riE "caracteriza" docs/ skills/` como devolvendo zero — e a
     própria página fazia o comando devolver três. Evidência morta na chegada. → o comando
     agora aponta para `skills/ .specify/templates/ .claude/`, que é onde a ausência
     importa, e o texto assume que a página é o único lugar onde a palavra aparece.

  Mais: o diagrama pintava **seis** caixas mudadas sob uma legenda que dizia "três novas e
  uma movida"; o `README.md` dos diagramas anunciava um código de cores "comum a todas as
  peças" que a 06 contradiz; o `check-agents` estava descrito como outro portão; o cartão de
  instalação invertia quem vira `.maestro-new`; o `--yes` do `promote-main.sh` aparecia no
  slide sobre o passo que **não** se delega; a ordem gravar-depois-mover estava trocada; e os
  rótulos do Mermaid estavam sem acento. Todos corrigidos.

  O parecer também **acertou uma acusação processual**: as caixas `TAIL:review` e
  `TAIL:gate` estavam marcadas no `tasks.md` enquanto este relatório ainda era um esqueleto
  com `<a preencher>`. É o defeito nomeado no próprio template, e ele voltou. Marcadas de
  novo só agora, com a evidência escrita — que é a única condição que as autoriza.

  Nada foi refutado nas categorias de contagem, comportamento, links e autocontenção: os
  números conferem, `promote-main.sh` de fato recusa com a conformidade vermelha e grava o
  `gate-main-<sha>`, e o HTML não fala com a rede.

- **TAIL:security** — superfície de execução nula: as duas peças são documentos e não entram
  na superfície instalável (`check-boundary.sh` confirma que caem em `guide`). O único vetor
  que um HTML entregue teria é recurso externo, e a revisão independente confirmou **zero**
  ocorrência de `http`, `src=`, `@import`, `url(` ou `fetch` — abrir o arquivo não fala com a
  rede. O script embutido só navega entre slides e alterna o tema.

- **TAIL:gate** — DoD verde, portões verdes salvo o `check-retro` declarado acima com motivo,
  plugin em dia e build do livro verde. **Aguarda o gate humano** — a promoção `dev` → `main`
  não é deste relatório.

## Requirement coverage

- **FR1** — a peça 06 diz "proposta, não vigente" no título, no primeiro parágrafo e na linha
  do índice, e aponta a 05 como o processo em vigor em cada um dos três. Confirmado pela
  revisão independente, que procurou e não achou leitura em que a página passe por adotada.
- **FR2** — a tabela marca *temos / novo / movido / parcial* passo a passo, e a legenda agora
  cobre as quatro; cada lacuna cita evidência que sobrevive a quem for conferir (comando com
  escopo, §7 e a tabela de gatilhos do roadmap, §6 e §10 do modelo operacional).
- **FR3** — o caderno percorre raia → spec → plan → tasks → implement → DoD → portões →
  revisão → gate → retro; todo número foi conferido por comando antes de escrito, e reconferido
  contra o disco pela revisão.
- **FR4** — `docs/diagramas/README.md` e `docs/handbook/README.md` listam as peças novas, e o
  primeiro passou a declarar onde a peça 06 **não** segue a convenção das demais.

## Pending gate

- Promoção `dev` → `main` aguarda aprovação humana.
