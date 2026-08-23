# Tasks 063 — "Pendente" não é evidência

## Verification first
- [x] T0 — reproduzir o achado 1 antes de qualquer coisa: 10 instalações, uma devolveu
      `"maestro_version": "0.3.0\nunknown"`.

## Implementation
- [x] T1 — `install-maestro.sh` lê a versão com `awk` (sem pipe, sem SIGPIPE) e **valida** a
      forma; `check-version.sh` recebe a mesma correção, que lá escapava por sorte. (achado 1)
- [x] T2 — `is_placeholder` ganha ausência declarada, ancorada no início, com piso em 061 e as
      duas proteções de botão. (FR1–FR4, achado 7)
- [x] T3 — `--ticked-only`: artefatos faltando viram `soft`; linha `TAIL:` apagada vira `bad`.
      (achados 3 e 8)
- [x] T4 — a checagem do plugin deixa de depender do ciclo mais novo e diz quando não olhou.
      (achado 5)
- [x] T5 — `spec NNN` **ou** `ciclo NNN` nos dois lados; `echo | grep -q` vira here-string.
      (achado 6, anti-padrão 21 sexta ocorrência)
- [x] T6 — a promessa da linguagem ubíqua sai de `perfis.md` e do `04-sipoc.md`; a linha falsa
      de fechamento é corrigida por linha nova no índice. (achado 2)
- [x] T7 — portão de contagens reescrito: acento, caixa, camada vazia, camada ausente e zero
      contagens. (achado 4)
- [x] T8 — portão do CHANGELOG cobre `[Unreleased]` **e** a versão recém-lançada, com
      vocabulário fechado de tipo. (achado 9)
- [x] T9 — `scripts/README.md` volta a nomear os 23 scripts, e o `check-flags.sh` passa a
      comparar índice × disco e a cobrir os `check-*.sh` com parser. (achados 13 e 14)
- [x] T10 — `check-chapters.sh` deixa de calar sobre skill que nenhum capítulo cita e sobre
      capítulo sem data. (achado 15)
- [x] T11 — números errados corrigidos na nota e na dívida declarada. (achados 10 e 16)
- [x] T12 — a tag `v0.3.0` removida localmente; recriada sobre a nota corrigida. (achado 12)
- [x] T13 — o achado 11 **rejeitado com medição**, e o motivo registrado no `qa-report`.

- [x] T14 — **segundo parecer** (revisão independente do próprio 063): 18 defeitos, **5
      introduzidos por mim neste ciclo**. Todos tratados; ver `qa-report.md`.
- [x] T15 — a regressão que eu criei: `soft` + `continue` fez `rm qa-report.md` pular o ciclo
      inteiro no modo bloqueante. Fechada com a asserção "caixa marcada sem qa-report".
- [x] T16 — `is_placeholder` redesenhado: piso de tamanho **medido** (40, com 65 sendo a menor
      evidência legítima e 20 a maior falsa) mais vocabulário — o vocabulário sozinho era
      contornável de cinco jeitos e **reprovava a verdade**.
- [x] T17 — `¹ não viaja` do índice de scripts passa a ser comparado com a instalação real;
      três scripts estavam marcados errado.
- [x] T18 — as quatro ocorrências vivas do anti-padrão 21 (`retro.sh`, `package-plugin.sh`,
      `check-licensing.sh`, `check-chapters.sh`) fechadas com `awk`/here-string.

## Closing tail — MANDATORY, one line each, never delete
<!-- TICK ONLY WHILE WRITING THE EVIDENCE, never in advance: the box records what happened.
     Do not delete a line to say it does not apply: write `n/a: <reason>` on it.
     check-conformance.sh requires the evidence of every non-n/a step in qa-report.md. -->
- [x] TAIL:review — independent review in fresh context, by whoever did not execute
- [x] TAIL:security — security pass proportional to the risk class
- [x] TAIL:mutation — every gate created or changed here, broken on purpose and seen refusing
- [x] TAIL:gate — DoD green -> guardian verdict -> human merge gate (not delegable)
