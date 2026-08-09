# Spec 045 — A quarta ocorrência vira forma, e a v0.1.0 é fechada

- **Status**: Concluída · **Raia**: plena · **Data**: 2026-08-07
- **Origem**: decisão do Steward — resolver `achado-044-quarta-ocorrencia` e **fechar a
  primeira versão**. O changelog declara "versionamento semântico" desde o ciclo 001 e o
  repositório tem **zero** versões fechadas e **zero** tags em 44 ciclos.

> **Raia**: plena. **Ambiguidade** baixa (a correção foi pré-comprometida pelo achado-043 e
> o corte é bookkeeping); **raio** amplo (muda o template que todo ciclo futuro usa, e a
> tag é pública); **irreversibilidade** média — uma tag empurrada é vista por terceiros.

## O quê e por quê

**A correção.** Marcar caixa antes de a evidência existir aconteceu **quatro vezes** entre
os ciclos 042 e 044, em **dois tokens diferentes** (`TAIL:` e os critérios de aceite), com o
mesmo autor e a mesma intenção. O `achado-043` pré-comprometeu que a quarta mudaria o
diagnóstico de disciplina para **forma**, e é isso que este ciclo faz.

O diagnóstico: a spec declara **critérios**; o `qa-report` declara **se eles valeram**.
Marcar na spec duplica a função do relatório — princípio VI — e é exatamente o que permite a
caixa virar plano. Uma caixa convida a ser marcada; a forma correta é não ter caixa.

**O corte.** A v0.1.0 não é um marco de completude, é uma **linha de base**: o ponto em que
alguém pode dizer "instalei esta versão" e a frase significar alguma coisa. Sem tag, o
método é sempre "o que estiver no `main` hoje".

## Requisitos funcionais

- **FR1**: QUANDO uma spec for escrita, O SISTEMA DEVERÁ apresentar os critérios de aceite
  **sem caixas de marcação**, porque quem responde "valeu?" é o relatório.
- **FR2**: QUANDO uma spec do ciclo 045 em diante contiver caixa nos critérios, O SISTEMA
  DEVERÁ falhar, nomeando a duplicação de função.
- **FR3**: QUANDO a versão for fechada, O SISTEMA DEVERÁ registrar no `CHANGELOG.md` uma
  seção `[0.1.0]` datada, com uma nota de release que declare **o que a versão é e o que
  ela reconhecidamente não tem**.
- **FR4**: QUANDO a versão for fechada, O SISTEMA DEVERÁ existir como **tag anotada** na
  linha principal — o changelog descreve, a tag identifica.

## Fora de escopo

- Reorganizar as onze subseções repetidas do `[Unreleased]` acumuladas em 44 ciclos. É
  edição em massa num arquivo de 500 linhas **no mesmo fôlego** de um corte de versão — o
  anti-padrão 18 mora aí. Vira achado com gatilho.
- Retroagir a regra sem-caixa às 44 specs existentes. Piso no 045; a dívida fica declarada.
- Publicar o backend do companion. Depende do Steward e nunca esteve pronto — entra na nota
  de release como limite conhecido, que é mais honesto que adiar o marco.

## Critérios de aceite (DoD)

<!-- Sem caixas: esta seção diz o que deve valer; se valeu, quem diz é o qa-report. -->
- O `spec-template.md` e o `new-cycle.sh` apresentam critérios sem caixa, com a razão escrita.
- `scripts/check-conformance.sh` falha numa spec ≥045 com caixa nos critérios, e foi visto
  falhando.
- `CHANGELOG.md` tem `[0.1.0]` datada com nota de release, e um `[Unreleased]` vazio acima.
- A tag `v0.1.0` é anotada e aponta para a linha principal — **depois** do gate humano,
  nunca antes: é o único critério deste ciclo que a promoção resolve, não o commit.
- `achado-044-quarta-ocorrencia` fechado no índice.

## Clarify

1. Por que remover a caixa em vez de instruir a não marcá-la? Porque instruir já foi tentado
   — o `tasks-template` ganhou o aviso no ciclo 043 e eu errei no ciclo 044, noutro token.
   Uma forma que não oferece a caixa não depende de ninguém lembrar.
