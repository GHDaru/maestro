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

- **TAIL:review** — pendente para este ciclo. Os 18 achados tratados aqui vieram da revisão
  independente dos ciclos **061 e 062**; este ciclo ainda não passou por uma.

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
