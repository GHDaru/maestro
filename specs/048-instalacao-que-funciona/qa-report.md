# QA report 048 — A instalação que funciona onde ela cai

- **Date**: 2026-08-11 · **Lane**: plena · **Verdict**: aprovado após reprovação e correção

## Fitness functions (DoD)

| Check | Expected | Result |
|---|---|---|
| `scripts/check-installed.sh` | vermelho antes (9 citações + 2 portões), verde depois | ✅ |
| `check-agents` · `check-roles` · `check-install` · `check-language` · `check-links` · `check-evals` · `check-boundary` · `check-chapters` · `check-licensing` · `check-ecosystem` · `check-cycle` · `check-retro` | verdes | ✅ |
| `scripts/package-plugin.sh --verify` | verde | ✅ 33 arquivos |
| `node publicar/build.mjs` | verde | ✅ 38 páginas |
| `scripts/check-conformance.sh 048` | verde | ✅ |

### O portão foi visto acusar — por mutação, em clone descartável

Primeira bateria (7 mutações) contra a versão inicial. Depois da revisão, o portão foi
endurecido em cinco pontos e a bateria refeita **com as mutações que a revisão usou para
reprová-lo**:

| Mutação | O que quebra | Portão |
|---|---|---|
| link relativo quebrado **sem crases** | prosa que promete e não entrega | ✗ via `check-links` enviado |
| instalador para de enviar `glossary.md`/`axioms.md` | 14 links pendentes no destino | ✗ idem |
| `UPSTREAM.md` cita caminho inexistente | arquivo **nosso** com passe livre | ✗ `is_vendored_verbatim` estrito |
| template **nosso** cita caminho inexistente | idem | ✗ idem |
| apagar o índice de perfis **aqui** | escape hatch virando porta dos fundos | ✗ `check-roles` consulta `boundary.json` |
| comando adaptado volta a citar a constituição do upstream | o defeito original voltando | ✗ |
| instalador deixa de enviar `.specify/scripts` | comandos chamando o que não foi | ✗ |
| `check-retro` volta ao `ls` sob `pipefail` | morte silenciosa, exit 2 | ✗ |
| instalador não envia portão nenhum | ritual sem fitness function | ✗ |
| controle — clone íntegro | — | ✓ exit 0 |

## Closing tail — the evidence

- TAIL:review — revisão independente em contexto fresco, por quem não executou. Veredito:
  **NÃO PROMOVER COMO ESTÁ**, dois bloqueantes e cinco relevantes. O primeiro bloqueante é o
  que mais importa e era meu: **reapontar mecanicamente o `/speckit.constitution` fez as
  instruções destrutivas dele — "este arquivo é um TEMPLATE", "escreva de volta
  (overwrite)" — mirarem a constituição ratificada**, que é instalada em repositórios de
  terceiros e empacotada no plugin. Antes do ciclo elas miravam um resumo derivado de 27
  linhas; depois, a única fonte de verdade. Aumento de risco no ciclo que marca o Princípio
  III como ⚠️ por outro motivo. Corrigido: o comando agora manda **emendar no lugar, nunca
  regenerar**. Segundo bloqueante: a tabela do `THIRD-PARTY-NOTICES.md` voltou a mentir —
  declarava `speckit.*` "(remaining) Verbatim" enquanto este ciclo modificou dois deles.
  Relevantes: eu **enfraqueci uma instrução real para calar o portão** (as 4 citações de
  `.specify/extensions.yml` viraram prosa vaga enquanto 12 idênticas ficaram — restauradas, e
  a exceção passou a ser **declarada** com `UP:optional-path=`); `check-roles.sh` reabriu o
  escape hatch que o `check-ecosystem.sh` já tinha fechado; sete promessas quebradas
  continuavam na instalação porque o portão só lia caminhos entre crases; e o
  `is_vendored_verbatim` dava passe livre **por ausência** a todo arquivo nosso sob
  `.specify/`. Todos corrigidos e reverificados.
- TAIL:security — passe proporcional à classe de risco. **(a) O achado de segurança do ciclo
  é o bloqueante 1**: um comando instalável que manda sobrescrever a constituição é a forma
  mais barata de um método perder a fonte de verdade — corrigido antes de qualquer promoção.
  **(b) Execução**: o portão novo **roda scripts** (`install-maestro.sh` e os `check-*.sh`) —
  todos do próprio repositório, num diretório temporário criado por `mktemp -d` e removido
  por `trap`; nada vem de entrada externa. **(c) Superfície instalável**: cresceu com
  `.specify/scripts/bash/` (5 scripts do upstream, MIT, já declarados nas notas de
  terceiros) e `init-options.json`; `check-language` passou a cobri-los. **(d) Caminhos**: o
  portão só lê; nada é escrito fora do temporário.
- TAIL:gate — DoD verde (tabela acima), treze portões verdes + plugin + build.
  `check-conformance.sh 048` verde. **Aguarda o gate humano** de promoção `dev` → `main`,
  que não é delegável — e desta vez não foi pedido.

## Requirement coverage

- **FR1** — todo portão enviado roda verde num diretório vazio: dez, incluindo os dois que
  chegavam vermelhos e o `check-links.sh`, que passou a ser enviado.
- **FR2** — caminho que existe aqui e é citado por arquivo enviado tem de existir lá; **e**
  todo link relativo resolve lá, porque o `check-links.sh` agora viaja e roda no destino.
- **FR3** — `check-roles.sh` e `check-conformance.sh` dizem o que não têm para medir, e só
  saem verdes quando a ausência é legítima: o primeiro consulta o `boundary.json`, o segundo
  distingue "nenhum ciclo" de "ciclos fora do alcance do piso".
- **FR4** — uma constituição só, `docs/governance/principles.md`, com as 8 citações
  reapontadas, o resumo apagado e a divergência declarada em `UPSTREAM.md` com token
  `UP:state=`.
- **FR5** — coberto **transitivamente**: as notas citam `.specify/scripts/bash/` entre
  crases, então deixar de enviá-lo reprova no portão da cópia instalada. **Limite declarado**:
  uma declaração escrita sem crases escaparia; `check-licensing.sh` não cruza estado
  verbatim/modificado com o `UPSTREAM.md`.

## Achados registrados neste ciclo

- **Um defeito que ninguém relatou**: `check-retro.sh` morria em silêncio (exit 2, zero
  bytes) numa instalação nova — `ls` sem match falhando sob `pipefail`. Anti-padrão 21,
  terceira ocorrência.
- **Eu enfraqueci uma instrução para calar um portão.** É o inverso do que o método existe
  para fazer, e só a revisão independente viu.
- **Prosa como token de máquina**: o portão lia "Adaptado" numa tabela em português,
  contrariando a doutrina que o `check-conformance.sh` declara no próprio cabeçalho.
  Corrigido com `UP:state=verbatim|adapted`.

## Pending gate

- Promoção `dev` → `main` aguarda aprovação humana.
