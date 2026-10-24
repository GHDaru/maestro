# ADR 0026 — Gate humano por delegação de política, com crítico independente

- **Status**: Aceito · **Data**: 2026-10-24 · **Ciclo**: 072 (vale a partir do gate do 070)
- **Supersede**: nada; **emenda** `docs/governance/operating-model.md` § 8 ("nenhum desses gates é delegável a um agente") para o caso descrito abaixo. **Superado por**: —
- **Origem**: mensagem do Darú em 24/10/2026 na sessão MAESTRO: "Peço que os 'meus' gates sejam assumidos por você. Chame um subagente par seu para ajudar a criticar e tomar a decisão. E prossiga sem parar." Registrada como `decisao-072-gates-delegados` em `docs/records/decisoes.jsonl`. O crítico do gate do 070 (agente `process-guardian`, contexto fresco, 24/10) apontou que a delegação contradizia a letra do § 8 e pediu base escrita: este ADR.
- **Implementação**: imediata, por esta regra; verificável pelos registros que ela exige.

## Contexto

O Princípio II diz que o **Accountable é sempre humano, e responde pela política, pelos gates
e pelos critérios, não por cada item**. O operating-model § 8, escrito antes de haver uma sessão
regente com orçamento próprio e sete construtores, fixou os gates DoR, plano e merge como "não
delegáveis a um agente" — uma regra pensada para impedir que **quem executa** se aprove. Em
22/10 e 24/10 o dono do método passou a conduzir ciclos inteiros por uma sessão regente (MAESTRO),
que não executa (delega a Workers e subagentes) e que recebe pareceres de revisão, segurança e
mutação em contexto fresco. A espera pelo tique humano em cada gate, com o humano ausente, parou
a linha — a dor registrada no `ux-design.md` § 2.3 ("tempo de espera do humano", 7 h e 24 h).

Siglas: ADR (*Architecture Decision Record*); DoR (*Definition of Ready*); DoD (*Definition of
Done*); TAIL (as quatro caixas de fechamento em `tasks.md`).

## Opções avaliadas

- **(a) Manter a letra do § 8.** Nenhum gate sem tique humano. Seguro e lento; com o humano
  ausente, a linha para e o orçamento das sessões abertas se perde.
- **(b) Delegar os gates à sessão regente por decisão explícita e registrada do humano, com
  crítico independente em contexto fresco antes de cada decisão e registro de cada gate aberto.**
  Preserva o espírito do Princípio II (quem executa não aprova; o humano responde pela política) e
  destrava a linha. Custo: um parecer por gate e uma linha de decisão por gate.
- **(c) Delegar sem crítico.** Mais rápido; perde a independência que o § 8 queria proteger.

## Decisão

**(b).** Um gate humano (DoR da spec, aprovação do plano, `TAIL:gate`, merge na `dev`) pode ser
decidido pela sessão regente **quando, e só quando**:

1. o humano delegou **por escrito**, com a decisão registrada em `docs/records/decisoes.jsonl`
   (aqui: `decisao-072-gates-delegados`), e a delegação não foi revogada;
2. a sessão regente **não executou** o trabalho julgado (delegou a Workers ou subagentes);
3. um **crítico independente em contexto fresco** (agente `process-guardian`, `review` ou
   `security`, só leitura) emitiu parecer antes da decisão, e o parecer está no `qa-report.md`
   do ciclo, com as condições que impôs e o que foi feito com cada uma;
4. **cada gate aberto por delegação gera uma linha** em `decisoes.jsonl` com o ciclo, o gate, o
   veredito do crítico e o hash julgado;
5. a **promoção para a `main`** (`scripts/promote-main.sh`) continua exigindo a delegação
   explícita para aquele ciclo, nos mesmos termos, e registra `gate-main-<sha>` como sempre.

O § 8 do operating-model passa a ler-se com esta exceção; a próxima revisão do documento
incorpora o texto (versão MINOR). Revogar é uma linha de decisão do humano, sem ADR.

## Ressalvas do gate do 070 (registradas aqui, porque o ADR 0025 já estava commitado)

O crítico do gate do 070 aceitou o ADR 0025 **com ressalva**, e o método não reescreve o corpo
de um ADR commitado; a ressalva fica aqui e o status do 0025 passa a "Aceito com ressalva (ADR
0026)":

- **As quatro tabelas do workflow são dado primário, não projeção.** O ADR 0022 diz que o
  painel é projeção reconstruível dos arquivos; o 0025 faz de `rodadas`, `passos`, `transicoes` e
  `fila` o único registro de quem entrou e saiu de cada passo, num arquivo fora do git. A exceção
  ao 0022 fica **restrita a essas quatro tabelas**, e antes de qualquer coisa depender delas o
  ciclo 072 entrega backup e lock de ingest (dívida 10 do plano do 070).
- **"Separação de escritores" ainda não é verdade.** `ingere()` copia as quatro tabelas para
  um arquivo temporário e troca por `os.replace`; uma escrita de hook entre a cópia e a troca se
  perde, e no Windows uma conexão aberta faz a troca falhar. A condição 1 do 0025 descreve a
  intenção, não o estado; o estado está nas dívidas 5 e 10.
- **Correção de texto do 0025 § Consequências**: onde se lê "FR2 e FR3 sem teste nomeado",
  leia-se "FR2 ausente e FR3 invertido" (revisão em contexto fresco do 070, achados 2 e 3).
- **Os hooks não entram em nenhum `settings.json` vivo** (Maestro ou Hindiana) até o 072 fechar
  as dívidas 6, 7 e 10; instalá-los hoje gravaria saídas `skip` como se fossem evidência.
  Verificação: `grep -rl workflow_ .claude/settings*.json` vazio.

## Consequências

- A linha anda com o humano ausente, sem perder a independência: quem julga não executou e um
  crítico leu antes.
- Mais duas linhas por ciclo no índice de decisões e um parecer a mais no qa-report.
- O humano continua responsável pela política e pode revogar a qualquer momento; o histórico
  mostra exatamente quais gates foram abertos por delegação e com que parecer.

## Como desfazer

Uma linha em `decisoes.jsonl` revogando `decisao-072-gates-delegados` devolve todos os gates ao
tique humano; um ADR posterior supersede este se a regra se mostrar ruim. Nada no código muda.
