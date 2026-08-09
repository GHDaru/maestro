# Relatório de QA 044 — O `/speckit.plan` defere à tabela de declaração

- **Data**: 2026-08-07 · **Raia**: plena · **Veredito**: aprovado **depois de reprovado**

## Fitness functions (DoD)

| Check | Esperado | Resultado |
|---|---|---|
| `scripts/package-plugin.sh --verify` | verde | ✅ 32 arquivos — **estava vermelho**, ver G1 |
| `scripts/check-language.sh` · `check-install.sh` · `check-links.sh` | verde | ✅ |
| `scripts/check-conformance.sh` | verde | ✅ 042, 043 e 044 |
| `grep "ART:research=yes" .claude/commands/speckit.plan.md` | a fase 0 defere | ✅ e agora **antes** dos passos |
| `grep "speckit.plan.md" .specify/UPSTREAM.md` | estado Adaptado | ✅ |

## Closing tail — a evidência

- **TAIL:review** — revisão independente em contexto fresco, por subagente com a instrução
  de `.claude/agents/review.md`, lendo o **arquivo inteiro** e não só o diff. **Veredito:
  "Do not merge as-is."** Seis lacunas, uma bloqueante e três da mesma classe que o ciclo
  existia para eliminar. Todas corrigidas antes deste relatório; detalhe abaixo.
- **TAIL:security** — passagem executada. O que muda aqui é **texto que instrui agentes**, e
  num sistema agêntico instrução é código, então não dispensei. Conferido: nenhuma edição
  **amplia** o que um agente é autorizado a fazer — as três mudanças de comportamento são
  todas restritivas (deferir, não pular, não produzir); o único caminho novo citado é
  `scripts/check-conformance.sh`, que já existe e é somente-leitura; nenhum segredo, rede ou
  credencial entra. O rebuild do plugin tocou **um** arquivo
  (`plugin/maestro/commands/speckit.plan.md`) e a contagem seguiu 32 — nada foi arrastado
  junto na redistribuição.
- **TAIL:gate** — pendente: promoção `dev` → `main` aguarda aprovação humana.

## O achado bloqueante estava fora do meu diff

`plugin/maestro/` é **build commitado** e é o caminho B de distribuição (`/plugin install`).
Editei a fonte e não reconstruí — então o plugin continuava entregando exatamente o texto
que este ciclo existe para apagar:

```
$ scripts/package-plugin.sh --verify
✗ plugin out of date with the sources. Differences:
   Files /tmp/…/maestro/commands/speckit.plan.md and plugin/maestro/commands/speckit.plan.md differ
```

E esse comando é um passo **bloqueante** da CI que eu mesmo escrevi no ciclo 043, uma hora
antes. A causa de eu não ter visto: a lista de verificação do meu próprio plano **não
incluía** o portão que guarda edição de comando vendorizado. Corrigido nos dois lugares — o
plugin foi reconstruído e a DoD do plano passou a citar o portão.

## As três lacunas da mesma classe que o ciclo combatia

A revisão foi precisa ao dizer que estas eram as que mais importavam: **o remédio
reintroduziu a doença**.

| # | O que eu fiz | Correção |
|---|---|---|
| G2 | escrevi "cada item abaixo roda só se o token for `yes`" — e o item 3 é a atualização do contexto do agente, que **não tem token**. Um agente lê, não acha token, e pula. Duas ordens no mesmo arquivo, sem dizer qual vence | o texto agora diz "itens 1 e 2"; o item 3 **sempre roda**, explicitamente |
| G3 | deixei intacta a linha upstream *"Skip if project is purely internal"* dentro de um item já governado por `ART:contracts=yes` — um segundo decisor competindo com a tabela | a linha virou orientação para **declarar `=no` na tabela**, com o aviso de que o portão reprova `=yes` sem arquivo |
| G4 | pus o portão da fase 0 **depois** dos passos que mandam gerar. Ordem primeiro, ressalva depois: quem executa de cima para baixo já despachou os subagentes e escreveu o arquivo | o portão subiu para o topo da fase, com a razão escrita: *"an order issued first and qualified afterwards is followed first and qualified never"* |

Também absorvi: o `Phase 2` pendurado (resíduo upstream, agora nomeado em vez de silenciado),
a citação da regra no `new-cycle.sh` que apontava para o número antigo depois da renumeração
do `UPSTREAM.md`, e a afirmação do `UPSTREAM.md` que era mais larga que o fato — o
`speckit.tasks` e o `speckit.implement` ainda **leem** `quickstart.md` se existir, o que é
inofensivo; a divergência é sobre **produzir**.

## O que a revisão confirmou

Ela verificou a alegação da spec em vez de aceitá-la: leu **todos** os comandos
`speckit.*` e confirmou que nenhum outro manda criar os artefatos — todas as referências são
leituras tolerantes (`IF EXISTS`, "Not all projects have all documents"). E confirmou que a
renumeração das regras do `UPSTREAM.md` é internamente consistente e que a regra 2 nova não
contradiz a 1.

## Cobertura dos requisitos

- **FR1** ✅ agora de fato — G3 e G4 eram o que impedia, e o plugin era onde não valia.
- **FR2** ✅ a razão escrita na tabela é o registro da decisão.
- **FR3** ✅ no comando **e** no plugin, com a razão (função servida pela jornada e receitas).
- **FR4** ✅ `UPSTREAM.md`: linha na tabela + regra "divergência declarada, nunca silenciosa".

## Lição para a retrospectiva — e uma decisão que não é minha

A revisão marcou o critério de aceite `- [x] achado-042 … fechado no índice` como **falso no
momento em que foi escrito** — o achado estava aberto, e a tarefa correspondente (`T7`)
estava corretamente **desmarcada**. Spec e tarefas se contradiziam.

Isso é a **quarta ocorrência** de caixa marcada antes de a evidência existir. Desta vez não
foi na cauda — eu tinha aprendido a lição no token errado, e cometi o mesmo erro nos
critérios de aceite da spec.

O `achado-043-caixa-marcada-antes` **pré-comprometeu** o que fazer numa quarta: *"muda o
diagnóstico para a ordem de escrita dos artefatos do ciclo"*. A revisão apontou isso e
deixou a chamada para o humano, porque a decisão foi tomada com antecedência justamente para
não ser relitigada caso a caso.

**Diagnóstico que eu proponho**: a spec declara **critérios**; o `qa-report` declara se eles
valem. Marcar na spec duplica a função do relatório — princípio VI — e é o que permite a
caixa virar plano. As caixas da spec deveriam nascer e permanecer **desmarcadas**.
Registrado como `achado-044-quarta-ocorrencia`, aberto, aguardando decisão do Steward.

## Pendência de gate

- Promoção `dev` → `main`: aguarda aprovação humana.
