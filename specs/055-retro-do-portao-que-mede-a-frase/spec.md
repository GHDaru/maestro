# Spec 055 — Retro: o portão que mede a frase vira prova por mutação

- **Status**: Concluída · **Raia**: plena · **Data**: 2026-08-16
- **Origem**: **o gatilho disparou e ficou disparado**. O `check-retro.sh` está vermelho
  desde o ciclo 053 — `achado-047-cinco-absorcoes-sem-destino` com **8 ciclos** de idade (7 quando o vermelho começou),
  um acima do limite. Cada ciclo novo empurrava a dívida em vez de pagá-la.

> **Raia**: plena. **Ambiguidade** média — o achado é conhecido, o que fazer com ele não era;
> **raio** amplo (portão de conformidade, template instalável, catálogo de anti-padrões,
> protocolo do índice); **irreversibilidade** baixa.

## O quê e por quê

Duas coisas saíram da apuração, e elas são de naturezas diferentes.

**A primeira é o achado aberto, e ele não podia fechar.** O remédio do 047 — reclassificar
cinco ideias de `absorver` para `observar`, cada uma com gatilho — **foi executado no próprio
047** e está no disco: as cinco estão `observar` com gatilho, e o `check-ecosystem.sh` está
verde. O que sobrou no texto do achado foi *"a skill de fatiamento continua não existindo"* —
e a ausência dela passou a ser governada por um gatilho que **não disparou** ("primeira
intenção grande real que não caiba em um ciclo"). Ou seja: o achado virou gatilho e ficou
sem nada **no mundo** que o fechasse — o mecanismo `fecha` esteve disponível o tempo todo, e
o que faltou foi a **decisão** de usá-lo, não o evento. Ele envelheceu sete ciclos e a dívida
de retro passou a medir **calendário**, não dívida.

**A segunda é o padrão que mais se repetiu, de longe.** Em **seis dos nove ciclos 046–054**
— 046, 047, 048, 049, 050 e 054 — a revisão independente achou a mesma coisa: **portão que
mede a frase e não o fato**. (A primeira versão desta frase dizia "seis ciclos seguidos" e
listava o 053, que **não enviou portão nenhum** — o defeito dele foi de afirmação em
documentação. Corrigido pelo parecer: o conjunto estava mal rotulado *e* subcontado, porque
048, 051 e 052 também mexeram em portão.) O anti-padrão 13 já está catalogado desde muito
antes — e continuou acontecendo. Norma catalogada sem função de força é a definição do problema que este método
existe para atacar. O que separa os ciclos em que o defeito foi pego dos ciclos em que ele
passou não é a atenção de ninguém: é se **alguém quebrou o portão de propósito e olhou**.

A mutação já é praticada — e é praticada porque quem executa lembra. Memória não é
testemunha (corolário C13).

## Requisitos funcionais

- **FR1**: QUANDO um achado for remediado **convertendo-o em gatilho**, O SISTEMA DEVERÁ
  oferecer forma de fechá-lo no ato, nomeando o gatilho — em vez de deixá-lo aberto
  esperando um evento que, por construção, pode nunca vir.
- **FR2**: A cauda de fechamento DEVERÁ ter um quarto passo, `TAIL:mutation`: a prova de que
  cada portão criado ou alterado no ciclo foi **visto reprovar**.
- **FR3**: QUANDO o ciclo tocar um portão, O SISTEMA DEVERÁ **recusar** `n/a` no
  `TAIL:mutation` — a dispensa existe para quem não mexeu em portão, não para quem mexeu e
  não quis provar. "Tocar um portão" é lido do **diff**, e "portão" inclui o que é portão na
  prática: `scripts/check-*.sh`, `scripts/package-plugin.sh`, `publicar/build.mjs`,
  `publicar/sumario.json` (o **conjunto declarado**, cujo ponto cego foi o defeito do 054),
  `boundary.json` e os *workflows* da CI. `companion/` fica de fora: é outro domínio.
- **FR3b**: A recusa DEVERÁ valer **como o passo for escrito**: `N/A`, `n/a —`, `n/a:` — a
  grafia não pode comprar a dispensa. E o piso da regra DEVERÁ **falhar** quando for posto
  acima do ciclo mais novo, ou quando não for número: botão que desliga tudo e ainda imprime
  sucesso não é botão, é interruptor.
- **FR4**: QUANDO `TAIL:mutation` se aplicar, O SISTEMA DEVERÁ exigir a evidência no
  `qa-report.md`, como já faz com os outros três.
- **FR5**: O catálogo de anti-padrões DEVERÁ ganhar o defeito que este conjunto de ciclos
  produziu e que ainda não estava lá: **abrir uma porta nova e não estender o guarda**.
- **FR6**: O passo novo DEVERÁ existir em **toda** cópia que o executor consome — template,
  gerador (`new-cycle.sh`, nas duas saídas), template de `qa-report`, catálogo de artefatos e
  o bloco que o instalador escreve em repositório de terceiro. Passo obrigatório presente em
  uma cópia e ausente nas outras **é** o anti-padrão 22, que este ciclo cita como motivo.
- **FR7**: A leitura do passo DEVERÁ casar a **linha da cauda**, não qualquer frase que
  mencione o token — e isso vale para os quatro passos, não só o novo.

## Fora de escopo

- Criar a skill de fatiamento. O gatilho dela não disparou, e criá-la agora seria construir
  contra hipótese — exatamente o que o veredito `observar` decidiu não fazer.
- Retroatividade **do `TAIL:mutation`**: vale a partir deste ciclo. Ciclo velho é evidência,
  não alvo — mesmo precedente do `check-cycle.sh` e do próprio `check-conformance.sh`.
  > O **FR7 é retroativo de propósito**, e isso é declaração, não descuido: ancorar a leitura
  > da cauda rejulga os 13 ciclos no piso. O parecer cobrou a omissão desta linha. Os 13
  > foram reconferidos e passam — e passam por desenho, não por sorte.
- Cobrar mutação de quem altera outros arquivos executáveis (`install-maestro.sh`,
  `promote-main.sh`). São candidatos legítimos e ficam de fora até haver dor: o defeito
  medido está nos portões.

## Critérios de aceite (DoD)

<!-- Sem caixas: esta seção diz o que deve valer; se valeu, quem diz é o qa-report. -->
- `achado-047` fechado no índice, com o gatilho nomeado e o motivo escrito; `check-retro.sh`
  verde.
- `docs/records/README.md` descreve a forma "achado que virou gatilho".
- `TAIL:mutation` no template instalável, e o `check-conformance.sh` cobrando os três casos:
  ausente, `n/a` indevido (o ciclo tocou portão) e aplicável sem evidência.
- Cada uma dessas três reprovações **vista falhando** — este ciclo mexe num portão, então
  ele é o primeiro obrigado pela própria regra que cria.
- Anti-padrão 23 no catálogo, com o ciclo de origem.

## Clarify

1. Fechar o `achado-047` é declarar resolvido o que não foi feito? → **Não**: o que foi
   decidido *foi* feito (a reclassificação). O que não foi feito está registrado como estado
   `observar` com gatilho, que é o mecanismo próprio do catálogo — e é auditável lá, não
   aqui.
