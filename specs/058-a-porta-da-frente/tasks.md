# Tasks 058 — A porta da frente

## Verification first
- [x] T0 — tentar responder "como instalo o Maestro?" lendo o disco, e registrar o que a
      documentação diz de errado: `--forcar` inexistente, "não sobrescreve" desatualizado, e o
      `# Usage` sem as flags de dois ciclos.

## Implementation
- [x] T1 — `bin/maestro`: despachante, banner com versão lida do CHANGELOG, uso sem argumento.
- [x] T2 — `maestro init`: quatro passos, tabela do 057, sem TTY não pergunta, verifica no fim.
- [x] T3 — `scripts/check-flags.sh`: flags do parser × flags documentadas, nos dois sentidos.
- [x] T4 — corrigir as três mentiras, e documentar as flags do `maestro`.
- [x] T5 — `bin/` no `boundary.json` e no `check-language.sh`; portão novo na CI.
- [x] T6 — porta rápida na capa do site.
- [x] T7 — asserções em `check-installed.sh` para o `init` não-interativo.

## Closing tail — MANDATORY, one line each, never delete
<!-- TICK ONLY WHILE WRITING THE EVIDENCE, never in advance: the box records what happened.
     Do not delete a line to say it does not apply: write `n/a: <reason>` on it.
     check-conformance.sh requires the evidence of every non-n/a step in qa-report.md. -->
- [x] TAIL:review — independent review in fresh context, by whoever did not execute
- [x] TAIL:security — security pass proportional to the risk class
- [x] TAIL:mutation — every gate created or changed here, broken on purpose and seen refusing
- [x] TAIL:gate — DoD green -> guardian verdict -> human merge gate (not delegable)

## Após o parecer — 19 achados
- [x] T8 — `cd "$HERE"` fazia todo caminho relativo cair **dentro do repositório do Maestro**,
      com "✓ installed" na tela. O diretório do usuário passa a ser capturado antes.
- [x] T9 — `maestro check` media o repositório do Maestro e dava verde alheio; agora resolve e
      **nomeia** o alvo. `init` sem alvo recusa instalar o método dentro do método.
- [x] T10 — sem terminal e sem `--yes` ele **recusa** em vez de responder sozinho; `--ai` como
      último argumento deixou de matar o script em silêncio; dois alvos recusam.
- [x] T11 — `--ai` inválido é validado **antes** de criar diretório; `--dry-run` não escreve
      (nem o `decisoes.jsonl`) e não emite veredito.
- [x] T12 — `version()` sem cano terminando em `grep -m1` (anti-padrão 21, 5ª aparição).
- [x] T13 — o portão: prosa com parênteses deixou de ser lida como parser, flags curtas passam
      a contar, cada fonte é conferida por si, `mktemp` com `trap`, e ele deixou de **morrer em
      silêncio** quando a documentação ficava vazia.
- [x] T14 — a quarta cópia da mentira: o `README.md`, agora coberto pelo portão.
