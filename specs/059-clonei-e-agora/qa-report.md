# QA report 059 — "Clonei, e agora?"

- **Date**: 2026-08-17 · **Lane**: plena · **Verdict**: aprovado após correção do parecer

## Fitness functions (DoD)

| Check | Expected | Result |
|---|---|---|
| instalar **de dentro do projeto** (`maestro init .`) | funciona | ✅ executado antes de documentado — 81 arquivos escritos, clone do Maestro byte a byte intacto |
| instalar **de dentro do clone** apontando para fora | funciona | ✅ executado — 81 arquivos |
| `export PATH` + `maestro init .` | funciona | ✅ executado |
| `maestro` por **symlink** no PATH | funciona | ✅ **depois da correção** — antes morria com exit 127 e banner `v?` |
| árvore publicada × instalação real (`--ai claude`) | camadas e contagens iguais | ✅ 13 agentes · 12 comandos · 6 skills · 12 templates · 9 `check-*.sh` · manifesto 76 + 5 = **81 escritos** |
| árvore com outro agente | declarada como menor | ✅ `--ai codex` escreve **53**, sem `.claude/` |
| cada arquivo e comando do bloco para IA | existe | ✅ 12 de 12 conferidos |
| **mutação 1**: `cd /x && maestro deploy` em bloco de código | reprova | ✅ |
| **mutação 2**: `sudo maestro deploy` | reprova | ✅ |
| **mutação 3**: `` `maestro deploy` `` em crase | reprova | ✅ |
| **contraprova**: prosa em português começando a linha com "maestro" | **não** reprova | ✅ |
| **mutação 4**: subcomando existente fora do `usage()` | reprova | ✅ |
| **mutação 5**: `usage()` anuncia subcomando inexistente | reprova | ✅ |
| **mutação 6**: `plugin/maestro/README.md` anuncia subcomando fantasma | reprova | ✅ |
| 14 portões bloqueantes · plugin · build | verdes | ✅ plugin **reempacotado** |

## Closing tail — the evidence

- **TAIL:review** — revisão independente em contexto fresco. **Reprovou: 19 achados.** Os que
  mais importam:

  1. **O plugin ficou fora de sincronia — e eu tinha consertado exatamente isso um commit
     antes.** O ciclo editou o `README.md`, que é **empacotado**, e não reempacotou. O commit
     `a8c5b4d` do ciclo 058 existe só para isso, na mesma branch. A lição estava a um `git log`
     de distância e não foi aplicada.
  2. **Marquei as quatro caixas da cauda sem `qa-report` nenhum** — pela terceira vez nesta
     sessão, no ciclo cujo próprio README publica *"caixa marcada não é testemunha"*.
  3. **O portão novo era cego para a forma mais comum de anunciar um comando.** Ele ancorava
     em início de linha e crase, então `cd /x && maestro deploy` dentro de um bloco de código
     passava verde — e é a forma que o **próprio README usa** duas seções acima. Pior: ele
     reprovava prosa em português que começasse a linha com "maestro". Trocado por
     "comando é o que está em bloco de código ou entre crases".
  4. **Ele chamava de inexistente um subcomando real**: `maestro help` funciona, e o arm
     `""|-h|--help|help)` era invisível porque a extração exigia que a **primeira** alternativa
     fosse minúscula.
  5. **A lista de fontes do portão era a lista antiga** — só README e receita —, enquanto
     `plugin/maestro/README.md` (a cópia que vai para o usuário) e um ADR também anunciam a
     porta. É o **anti-padrão 23**, no ciclo que cita o anti-padrão 23.
  6. **`maestro` por symlink no PATH estava quebrado.** `BASH_SOURCE` sem `readlink` fazia o
     `HERE` apontar para o diretório do link: banner impresso, versão `v?`, e morte com exit
     127 logo depois. E é a forma mais comum de pôr algo no PATH.

  Mais quatro afirmações falsas **que eu escrevi neste ciclo**: *"você não promove"* (o
  `--yes` pula a pergunta, e o bloco é endereçado a quem acharia a flag); *"sem `--ai` instala
  para o Claude Code"* (sem terminal ele **recusa** — e os blocos de copiar-e-colar omitiam
  `--ai`, então em CI a receita documentada não instalava nada); *"23 erros já cometidos aqui,
  cada um com o ciclo de origem"* (oito trazem ciclo; os outros vieram de retrospectivas e de
  catálogo externo adaptado); e o bloco de imutabilidade prometendo proteção que o guarda
  **não dá** — `estado.jsonl` não é guardado, o `Bash` é isento, e o padrão é `NNN-slug.md`,
  não `*.md`. Os dois limites agora estão escritos ao lado da regra.

  E os números: a árvore era de `--ai claude` sob um título que diz "qualquer agente" (com
  `codex` não existe `.claude/` nenhum); "82 arquivos" contava o arquivo do próprio usuário; a
  árvore omitia dois scripts com `└──` fechando como se estivesse completa; e o README passou a
  ter **três** contagens de portões diferentes, num arquivo cuja tese é que um fato dito em dois
  lugares só continua igual se algo comparar.

  **Não refutado**: as duas formas de instalar (executadas pelo revisor, 81 arquivos cada, com
  o clone do Maestro intacto), a existência de todos os 12 caminhos do bloco para IA, o que o
  `new-cycle.sh` emite, "seis dos nove ciclos 046–054", "oito princípios", e a ausência de
  anti-padrão 21 no código novo.

- **TAIL:security** — classe de risco baixa: o ciclo é texto mais um portão de leitura, e nada
  muda no que é escrito em disco de terceiro. Um item **real** apareceu: o bloco para IA
  afirmava que promover exige humano, o que é falso com `--yes` — orientação de segurança
  errada endereçada justamente a quem tem meios de encontrar a flag. Corrigido para dizer que a
  flag existe e é de quem já decidiu. A correção do `readlink` **reduz** superfície: o script
  deixa de executar com um `HERE` errado.

- **TAIL:mutation** — o ciclo altera `check-flags.sh`. Sete mutações, todas **vistas
  reprovando** (três formas de anúncio, duas de `usage()`, uma no plugin) e **uma contraprova**
  que precisa passar: prosa em português começando a linha com "maestro" não pode reprovar o
  build. As mutações 1–3 e 6 só existem porque o parecer mostrou que a versão anterior passava
  verde nelas.

- **TAIL:gate** — DoD verde, os 14 portões bloqueantes verdes, plugin **em dia** e livro em 39
  páginas. Os três consultivos (`cycle`, `retro`, `conformance`) são vermelhos por desenho
  enquanto o ciclo está aberto. **Aguarda o gate humano.**

## Requirement coverage

- **FR1/FR2** — a distinção ferramenta × projeto abre a seção; as duas direções estão escritas
  e executadas; `agents` saiu do bloco numerado.
- **FR3** — o bloco para IA existe, com seis itens, apontando e não repetindo.
- **FR4** — o portão confere subcomandos nos dois modos, e a prosa deixou de ser confundida
  com comando.
- **FR5** — os 12 caminhos citados foram conferidos um a um; e os que **não** são cobertos
  pelo guarda passaram a ser declarados junto.

## Limite declarado

- **A linha de versão do README continua dizendo "dezesseis portões, treze bloqueando"**,
  porque é citação datada da **v0.2.0**. Hoje são 17 e 14. A frase se acerta no próximo corte;
  reescrevê-la faria a capa descrever o HEAD alegando ser a versão publicada.

## Pending gate

- Promoção `dev` → `main` aguarda aprovação humana.
