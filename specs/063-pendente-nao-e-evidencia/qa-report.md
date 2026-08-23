# QA report 063 — "Pendente" não é evidência

- **Date**: 2026-08-23 · **Lane**: plena · **Verdict**: DoD verde; aguardando parecer e portão humano

## Fitness functions (DoD)

| Check | Expected | Result |
|---|---|---|
| 20 instalações seguidas | `maestro_version` = `0.3.0` nas vinte | ✅ antes da correção: **1 em 10** devolvia `0.3.0\nunknown` |
| **mutação**: `TAIL:review` marcado com "não executada" | reprova | ✅ nos ciclos 061 e 062 |
| **contraprova**: evidência legítima com a palavra no **meio** (ciclo 060) | passa | ✅ |
| **contraprova**: ciclo 042, ausência declarada **abaixo do piso** | passa | ✅ |
| **mutação**: piso 999 | reprova nomeando o ciclo mais novo | ✅ |
| **mutação**: piso `abc` | recusa rodar | ✅ |
| **mutação**: 061 escreve `TAIL:mutation — n/a` | reprova | ✅ — antes passava, porque nenhum commit do 061 diz "spec 061" |
| **mutação**: números por extenso nas duas páginas | reprova | ✅ "announces no count this gate can read" — antes imprimia `✓` |
| **mutação**: `8 portoes`, sem acento | reprova | ✅ e `6 SKILLS` em caixa alta é lido |
| **mutação**: tipo repetido na versão recém-lançada | reprova | ✅ — era o buraco que o corte abria |
| **mutação**: `### Adicionado (ciclo 062)` para driblar | reprova | ✅ "not a Keep a Changelog type" |
| **mutação**: abrir ciclo novo com `TAIL:gate` marcado atrás | continua cobrando | ✅ |
| **mutação**: plugin dessincronizado | reprova | ✅ |
| **mutação**: flag no parser sem `# Usage` · `# Usage` com flag inexistente | reprovam | ✅ nos dois sentidos |
| **mutação**: script fora do índice · índice com script inexistente | reprovam | ✅ |
| 14 portões bloqueantes · `--ticked-only` · plugin · build | verdes | ✅ — o `check-language.sh` reprovou primeiro, e o vocabulário virou `PT-DATA` marcado |
| `check-cycle` · `check-retro` | verdes | ✅ |

## Os 18 achados da revisão independente, e o que aconteceu com cada um

**Aplicados (15):** 1 (corrida da versão), 2 (`achado-055` não fechado), 3 (`--ticked-only`
sempre-vermelho), 4 (quatro buracos do portão de contagens), 5 (checagem do plugin some),
6 (dispensa comprável + anti-padrão 21), 7 (`pendente` e "não executada" como evidência),
8 (apagar a linha `TAIL:`), 9 (regra do CHANGELOG vacuosa), 10 e 16 (números errados nos
textos), 12 (tag apontando para nota superada), 13 (índice de scripts), 14 (flags dos
`check-*.sh`), 15 (silêncio do `check-chapters`).

**Latente, fechado por reescrita (1):** 17 — o glob não-citado deixou de existir quando a
seção 6 parou de depender do ciclo mais novo.

**Rejeitado com medição (1):** **11 — as contagens de arquivo da receita estão certas.**
A revisão mediu com `install-maestro.sh --ai claude`, que **não** escreve `CLAUDE.md`; a
árvore publicada documenta o que o `maestro init` deixa, e `init` passa `--write-block`
(estabelecido no ciclo 060, e é o que o portão da árvore mede). Medido nos dois caminhos:

| Comando | Total em disco | Escritos |
|---|---|---|
| `install-maestro.sh --ai claude` (+ README do usuário) | 81 | 80 |
| **`maestro init --ai claude`** (+ README do usuário) | **82** | **81** |
| `maestro init --ai codex` (diretório vazio) | **53** | 53 |

A receita diz "81 escritos, 82 no total" e "codex escreve 53". Confere. O sub-ponto **válido**
dentro do achado 11 foi aplicado: `arquivos` não estava no vocabulário do portão e agora está.

**Confirmado com número corrigido (1):** 18 — as contagens que a revisão declarou conferentes
conferem. E no achado 15 a revisão estava certa e eu errado: são **quatro** skills que nenhum
capítulo numerado cita (`constitution-check`, `diagnose-before-fix`, `fight-the-pile-up`,
`living-journey`) — minha primeira contagem incluía apêndices, que a regra não olha.

## Closing tail — the evidence

- **TAIL:review** — revisão independente em contexto fresco, **do próprio ciclo 063**.
  **REPROVOU: 18 defeitos, 5 deles introduzidos por este ciclo.** Décimo parecer seguido a
  reprovar. Os que eu mesmo criei:

  1. **Eu abri um buraco mais barato que o que fechei.** Tornar `soft` a exigência dos quatro
     artefatos deixou o `continue` no lugar: `rm qa-report.md` fazia o modo **bloqueante**
     pular o ciclo inteiro — cauda, evidência, tudo — e sair `0`, com as quatro caixas
     marcadas. É exatamente o defeito 057–060 que o modo existe para pegar. Fechado com uma
     asserção que não depende dos outros artefatos: caixa marcada + sem `qa-report` = falha.
  2. **A regra do `pendente` era contornável de cinco jeitos** (`ainda não executada`,
     `não executadas`, `(pendente)`, `> pendente`, `NÃO EXECUTADA`) **e reprovava a verdade**
     (`Todo o repositório foi varrido…`). Vocabulário sozinho é a ferramenta errada. Agora há
     um **piso de tamanho medido** — 65 caracteres é a menor evidência legítima das 54 deste
     repositório, 20 é a maior falsa, o piso está em 40 — que não depende de palavra nenhuma.
  3. **Reintroduzi a classe de bytes.** O `sed` de limpeza tinha `—` e `–` dentro de colchetes:
     em locale C são seis bytes soltos, e `• pendente` perdia dois deles e passava. É o `[├└]`
     do ciclo 060, no ciclo que o cita. Trocado pelo **complemento** `[^[:alnum:]]`, que não
     precisa de classe multibyte, e os acentos por alternação.
  4. **O botão do piso só travava para cima do ciclo mais novo**, então `=63` (o ciclo em
     andamento) desculpava tudo já escrito e imprimia sucesso. Agora o botão **só aperta**.
  5. **Um dos três chamadores não passava o número do ciclo**, então a regra era retroativa
     por essa via, contra o FR3. Virou `is_skeleton()`, que é o teste certo para uma razão
     curta e legítima.

  E fora do que eu escrevi: o índice de scripts marcava **três** scripts como "não viajam" e
  eles viajam; o portão de contagens cobrava qualquer `<número> <substantivo>` da prosa, então
  uma frase histórica **verdadeira** o deixava vermelho; o guarda de vacuidade do CHANGELOG
  contava cabeçalhos de versão em vez de seções; e sobravam **quatro** ocorrências vivas do
  anti-padrão 21, uma delas alimentando uma mensagem que este ciclo acabara de escrever.

- **TAIL:security** — classe de risco **baixa**, com um ponto que subiu e desceu: a correção do
  achado 1 mexe no que o instalador **escreve em disco de terceiro**. O valor agora é validado
  por forma (`^[0-9]+\.[0-9]+\.[0-9]+$`) antes de entrar no JSON, então uma leitura estranha
  vira `unknown` em vez de conteúdo arbitrário — mais restrito que antes, não menos. O `awk` lê
  o CHANGELOG como dado, sem `system()`. O extrator de contagens recebe o caminho por `argv` e
  não interpola nada em comando. A tag pública foi **removida**, não empurrada.

- **TAIL:mutation** — dezesseis mutações e quatro contraprovas, todas com o resultado esperado
  (tabela acima). Duas coisas merecem registro: a correção ingênua do `is_placeholder`
  reprovaria a evidência **legítima** do ciclo 060, que contém "pendente" no meio de uma frase —
  por isso a regra é ancorada; e ela reprovaria quatro ciclos históricos (042–045) que
  escreveram a ausência quando ela era verdade — por isso tem piso.

- **TAIL:gate** — pendente. DoD verde; falta o parecer independente e o portão humano.

## Dívida declarada, não apagada

- **Quatro skills que nenhum capítulo numerado ensina** — registrado como achado. O portão
  agora as **nomeia** em vez de pular em silêncio, mas não reprova: cobrir uma skill é decisão
  editorial que este ciclo não tomou.
- **A contagem `53` do `--ai codex`** não é comparada: a instalação de referência é `claude`.
  A estrutura do codex já é provada noutro ponto do mesmo portão ("a codex install carries no
  Claude-only format"); a contagem, não.
- **As versões lançadas antes da v0.3.0** continuam com repetição de tipo (a v0.1.0 repete
  `### Changed` e `### Added` quatro vezes cada). Reescrever entrada lançada é reescrever
  registro histórico.
