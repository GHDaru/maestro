# Relatório de QA 045 — A quarta ocorrência vira forma, e a v0.1.0 é fechada

- **Data**: 2026-08-09 · **Raia**: plena · **Veredito**: aprovado **depois de reprovado**

## Fitness functions (DoD)

| Check | Esperado | Resultado |
|---|---|---|
| `scripts/check-conformance.sh` | verde, com a regra nova | ✅ 042–045 |
| caixa nos critérios de uma spec ≥045 | vermelho | ✅ visto acusar nas **quatro** grafias |
| seção de critérios não localizável | vermelho | ✅ visto acusar |
| `record-decision.sh` citando placeholder | recusa | ✅ `exit=1` |
| os outros dez portões · `package-plugin --verify` · build | verde | ✅ |

## Closing tail — a evidência

- **TAIL:review** — revisão independente em contexto fresco, por subagente com a instrução
  de `.claude/agents/review.md`. **Veredito: "do not promote as-is."** Quatro bloqueantes,
  e o pior deles contra o próprio ciclo. Todos corrigidos antes deste relatório.
- **TAIL:security** — n/a: nenhuma superfície de risco. O ciclo mexe em texto de template,
  numa condição de portão somente-leitura e no changelog; nenhum segredo, rede, credencial
  ou permissão entra, e a tag é anotada e local até o gate humano.
- **TAIL:gate** — pendente: promoção `dev` → `main` aguarda aprovação humana, e a tag
  `v0.1.0` vem **depois** dela.

## O portão que eu escrevi falhava aberto

O achado mais duro: a correção era subtrativa e correta, mas o portão que devia torná-la
**estrutural** cobria **uma** grafia de caixa. A revisão construiu quatro variantes e rodou:

| Variante | Antes | Depois |
|---|---|---|
| `- [ ]` na coluna 0 | ✗ pega | ✗ pega |
| `  - [ ]` indentada | ✓ **passava** | ✗ pega |
| `* [ ]` estrela | ✓ **passava** | ✗ pega |
| `+ [ ]` mais | ✓ **passava** | ✗ pega |
| título diferente | ✓ **passava** | ✗ pega — *"has no acceptance-criteria section the gate can locate"* |

É o corolário **C5** — *"um portão cobre a família inteira ou não cobre nada"* — violado
dentro do ciclo que cita esse documento. E a última linha é a pior: o portão **não
distinguia "limpo" de "não olhei"**, que é a falha que este repositório já nomeou duas vezes
no cabeçalho do mesmo arquivo.

Segundo bloqueante da mesma família: eu usara `\|` numa expressão básica do `sed`, que é
**extensão GNU**. Em `sed` BSD a faixa nunca abriria e o portão ficaria verde em toda spec,
para sempre — invisível na integração contínua, que roda Linux, e visível só no laptop de
quem instalasse. Trocado por `sed -nE`.

## A quinta ocorrência, num log que não se retira

A revisão achou duas linhas do índice de decisões citando como registro um `qa-report.md`
que ainda estava em branco — inclusive uma declarando a release **aceita** antes da
promoção, antes da tag e com a conformidade vermelha.

É o mesmo defeito das quatro anteriores, agora num arquivo **append-only**, onde não dá para
apagar discretamente. A resposta foi a mesma do ciclo 045 para a quarta: **forma**. O
`record-decision.sh` passa a recusar uma linha cujo `registro` aponte para arquivo com
placeholder:

```
error: 'specs/045-fechar-v0-1-0/qa-report.md' is still a placeholder — write the record before citing it.
       A line that cites evidence which does not exist cannot be taken back.
```

As duas linhas ficam onde estão — o índice é imutável — e passam a ser verdadeiras a partir
deste relatório. A correção está registrada por linha nova, como manda o protocolo.

## A nota de release estava com números errados

O texto que gente de fora lê dizia **"doze portões executáveis — nove estruturais"**, e o
mesmo arquivo, dezessete linhas abaixo, dizia **onze** e **oito**. Nem entre si os dois
fechavam. Corrigido para o vocabulário estabelecido: **onze portões, oito bloqueando na
integração contínua** ao lado do `package-plugin --verify` e do build.

E dizia *"Onze portões verdes na promoção"* no passado, sendo que a promoção não aconteceu e
a conformidade estava vermelha. Reescrito no tempo certo: **"os onze precisam estar verdes
para a promoção acontecer"**.

Mais: a data era **2026-08-07** e hoje é **2026-08-09** — erro meu, repetido nos ciclos 040 a
044. Corrigido a partir daqui e **não reescrito para trás**; o próprio limite entrou na nota
de release, porque uma versão que esconde os próprios erros de registro não é linha de base.

## O que a revisão confirmou

Ela verificou cada número da nota contra o repositório: treze agentes, seis skills, oito
princípios, cinco axiomas / sete teoremas / treze corolários, vinte e dois anti-padrões, um
caso de eval provado por ablação e um aposentado, 35/40, quatro das sete classes de risco
nunca ocorridas — **todos verdadeiros**. E confirmou que o `[Unreleased]` ficou corretamente
vazio acima da versão, que a regra de piso funciona e que o script não tem `grep -q`
terminando pipe.

## Cobertura dos requisitos

- **FR1** ✅ template e gerador, ambos alcançando o método instalado.
- **FR2** ✅ **agora de fato** — a família inteira e o caso "não encontrei".
- **FR3** ✅ nota de release presente **e** factualmente correta, o que não era verdade na
  primeira escrita.
- **FR4** ⏳ por desenho: a tag vem depois do gate humano. A spec dizia "foi empurrada" no
  passado — corrigido, porque asseverar critério antes da evidência é a tese deste ciclo.

## Lição para a retrospectiva

**Cinco ocorrências, três tokens, e a terceira resposta estrutural em três ciclos.** A
progressão importa: instrução (043) → forma no artefato (045) → forma no script que grava
(045). O que não mudou foi eu; o que mudou foi o número de lugares onde o erro é possível.

Se houver uma sexta, o diagnóstico deixa de ser sobre a forma de cada artefato e passa a ser
sobre **quem escreve o registro**: talvez a linha de fechamento não deva ser escrita por
quem executou o ciclo.

## Pendência de gate

- Promoção `dev` → `main`: aguarda aprovação humana. Depois dela, a tag `v0.1.0`.
