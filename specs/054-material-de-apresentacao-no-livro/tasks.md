# Tasks 054 — Material de apresentação dentro do livro

## Verification first
- [x] T0 — ler o motor inteiro e nomear as três restrições que o material atravessa
      (reescrita de href, portão de links, limpeza de `site/`) antes de escrever código.

## Implementation
- [x] T1 — `materiais` no `sumario.json`, com o caderno de desenvolvimento.
- [x] T2 — no motor: publicar o material envolvido em documento mínimo, com a volta para o
      sumário injetada na publicação (nunca no arquivo de origem).
- [x] T3 — o material entra no mapa de colisão de slug e no conjunto `paginas`.
- [x] T4 — `resolverHref` resolve caminho de material para a página publicada.
- [x] T5 — material declarado e ausente do disco falha o build.
- [x] T6 — seção **Material** no sumário do livro.
- [x] T7 — **mutação**: quebrar de propósito as três reprovações (ausente, colisão, link
      para material não declarado) e ver cada uma falhar. Portão nunca visto vermelho não é
      portão.

## Closing tail — MANDATORY, one line each, never delete
<!-- TICK ONLY WHILE WRITING THE EVIDENCE, never in advance: the box records what happened.
     Do not delete a line to say it does not apply: write `n/a: <reason>` on it.
     check-conformance.sh requires the evidence of every non-n/a step in qa-report.md. -->
- [x] TAIL:review — independent review in fresh context, by whoever did not execute
- [x] TAIL:security — security pass proportional to the risk class
- [x] TAIL:gate — DoD green -> guardian verdict -> human merge gate (not delegable)

## Após o parecer
- [x] T8 — fechar o buraco que este ciclo abriu: `index` e `sumario` no mapa de colisão.
- [x] T9 — `check-boundary.sh` passa a ler `materiais` (o canal novo tinha ficado sem guarda).
- [x] T10 — mensagens de erro dizem o que fazer; contraste da volta em AA; nome do material
      com uma fonte de verdade só.
- [x] T11 — mutações 4, 5 e 6, todas vistas falhando em cópia da árvore.
