# Spec 061 — Retro: a caixa marcada sem testemunha

- **Status**: Rascunho · **Raia**: plena · **Data**: 2026-08-22
- **Origem**: **o gatilho disparou**. O `check-retro.sh` está vermelho com **5 achados
  abertos** (limite 4), e o `achado-055` está com **5 de 6 ciclos** de idade. O ciclo 060
  indexou três achados novos em vez de segurá-los para manter o número verde — a dívida está
  à vista de propósito, e esta é a hora de pagá-la.

> **Raia**: plena. **Ambiguidade** média — os cinco achados são conhecidos, o remédio de dois
> deles não era; **raio** amplo (portão de conformidade, portão de capítulos, superfície
> instalável, CHANGELOG); **irreversibilidade** baixa — tudo é texto e portão.

## O quê e por quê

**Medido antes de escrever** (`scripts/retro.sh`, `check-retro.sh`, `git log`):

| Fato | Como se sabe |
|---|---|
| 5 achados abertos, limite 4 | `check-retro.sh` vermelho |
| O mais antigo tem 5 de 6 ciclos | `achado-055`, aberto no ciclo 055, ciclo corrente 060 |
| A cauda foi marcada antes da evidência em **4 ciclos seguidos** | 057, 058, 059, 060 — cada `qa-report.md` diz isso no próprio texto |
| O plugin ficou fora de sincronia em **4 ciclos seguidos** | 057, 058, 059, 060 — idem |
| Os 19 ciclos passam no `check-conformance.sh` **hoje** | e ele é **consultivo**: nada barra |

### O padrão que se repetiu, e é um só

Nos ciclos **057, 058, 059 e 060** a revisão independente achou a mesma dupla: **as quatro
caixas `TAIL` marcadas sem `qa-report.md` existir**, e **o plugin não reempacotado**. Quatro
vezes. Não é desatenção de um dia: é que **nada cobra**.

O `check-conformance.sh` é o único portão que leria a evidência da cauda, e ele é **consultivo
por desenho** — porque o `new-cycle.sh` emite um `qa-report.md` de esqueleto, e um portão
bloqueante ficaria vermelho durante toda a vida de todo ciclo. A razão é boa. O efeito é que
a caixa marcada não tem testemunha nenhuma até o parecer humano.

Mas há uma metade da regra que é **checável a qualquer momento e nunca fica vermelha num
ciclo em andamento**: *se você marcou, a evidência tem de existir*. Um ciclo aberto e sem
caixa marcada passa. Um ciclo que marcou passa se tiver a evidência. Só reprova quem afirmou
sem ter. Essa metade pode bloquear sem incomodar ninguém — é anti-padrão 13 lido ao contrário:
em vez de medir a frase, medir se a frase tem lastro.

O plugin é o mesmo defeito noutra roupa: `package-plugin.sh --verify` **existe** e **roda na
CI** (`ci.yml:89`), então o defeito nunca chegou a `main`. O que ele consumiu foi tempo de
revisão, quatro vezes. Ele é mecanizável no mesmo lugar: quem marca `TAIL:gate` está dizendo
"a bateria passou", e a bateria inclui o plugin.

### O achado que não podia fechar sozinho

O **`achado-055`** diz que o `plan-architect` — na superfície **instalável** — manda consumir
uma *linguagem ubíqua* que não existe em projeto nenhum, e que o roadmap a mantém como
"se/quando houver domínio". O gatilho dele **disparou** (o método foi para código de produto
no FlowBuilder). Duas saídas honestas foram registradas em 055: criar o artefato, ou tirar a
promessa. Este ciclo escolhe: **tirar a promessa da instrução e deixar o artefato como
opcional declarado** — instrução que aponta para arquivo inexistente é o anti-padrão 22 (cópia
instalada que promete o que não entrega) aplicado a texto de agente.

### O portão que não consegue disparar dentro do próprio ciclo

O **`achado-056`**: `check-chapters.sh` compara a data de **commit** do `SKILL.md` com a data
de revisão do capítulo. A data de commit só existe **depois** que o ciclo fecha — então o
ciclo que desatualiza um capítulo passa verde e deixa o vermelho para o seguinte. Aconteceu
entre 055 e 056. É defeito de desenho, não de uso: o portão é **estruturalmente incapaz** de
disparar dentro do ciclo que o causa. Uma alteração não commitada é uma alteração de **hoje**.

## Requisitos funcionais

- **FR1**: QUANDO uma caixa `TAIL:<passo>` estiver marcada e não for `n/a`, O SISTEMA DEVERÁ
  **bloquear** se o `qa-report.md` do ciclo não trouxer a evidência daquele passo. QUANDO
  nenhuma caixa estiver marcada, O SISTEMA DEVERÁ passar — um ciclo em andamento não é
  violação. *(Fecha `achado-060-cauda-marcada-antes-da-evidencia`.)*
- **FR2**: A verificação de FR1 DEVERÁ rodar na **integração contínua**, como portão
  bloqueante, sem tornar bloqueante o resto do `check-conformance.sh`.
- **FR3**: QUANDO um `SKILL.md` estiver alterado e **não commitado**, O SISTEMA DEVERÁ tratá-lo
  como alterado **hoje** ao comparar com a data de revisão do capítulo — de modo que o ciclo
  que desatualiza o capítulo veja o vermelho. *(Fecha `achado-056`.)*
- **FR4**: A instrução instalável do `plan-architect` NÃO DEVERÁ exigir artefato que o método
  não entrega. QUANDO a linguagem ubíqua existir no projeto, O SISTEMA DEVERÁ consumi-la;
  quando não existir, DEVERÁ dizer o que fazer em vez de apontar para o vazio.
  *(Fecha `achado-055`.)*
- **FR5**: As contagens que o `README.md` e a receita afirmam (subagentes, skills, scripts,
  comandos, templates, portões instalados) DEVERÃO ser comparadas com uma instalação real.
  *(Fecha `achado-060-numeros-do-README-sem-portao`.)*
- **FR6**: O bloco `[Unreleased]` do `CHANGELOG.md` DEVERÁ ter **uma** seção por tipo, e algo
  DEVERÁ ler essa estrutura. *(Fecha `achado-060-changelog-com-quatro-secoes-adicionado`.)*

## Critérios de aceite

- Os cinco achados abertos aparecem **fechados** no índice, cada um por uma linha nova com o
  campo `fecha` nomeando-o — nunca por prosa.
- `check-retro.sh` volta ao verde por **dívida paga**, não por limite afrouxado.
- Cada portão criado ou alterado é visto **reprovar** numa mutação, e visto **passar** numa
  contraprova — um portão que só sabe reprovar reprova tudo.
- Um ciclo recém-aberto pelo `new-cycle.sh`, sem caixa marcada, **passa** no portão do FR1.
