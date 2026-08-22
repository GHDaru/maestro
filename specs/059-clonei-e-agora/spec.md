# Spec 059 — "Clonei, e agora?" — a porta explicada, para gente e para IA

- **Status**: Concluída · **Raia**: plena · **Data**: 2026-08-17
- **Origem**: o Steward leu a instrução de instalação e perguntou *"não entendi, preciso
  instalar? e o que faz o `agents`? e o `init`?"* — e depois *"quando clono, vou ter a pasta,
  mas não vou instalar na pasta do maestro, vou instalar em outra, como fazer?"*

> **Raia**: plena. **Ambiguidade** média — o que confunde não é dedutível do código, veio de
> alguém tropeçando; **raio** amplo mas de leitura (README, receita, e um portão novo);
> **irreversibilidade** baixa. Não é infra: nada muda no que é escrito no disco de terceiro.

## O quê e por quê

A instalação **funciona** e está mal explicada, e isso foi medido do jeito mais direto
possível: a pessoa que conduz este repositório leu as instruções e não soube o que fazer.

Três confusões, todas legítimas:

1. **"Preciso instalar?"** — o texto lista três comandos como se os três fossem obrigatórios.
   Não são: `git clone` **é** ter o Maestro; `agents` é **consulta** e não escreve nada;
   só o `init` instala. Ninguém diz isso.
2. **"O que faz o `agents`?"** — o README o apresenta como passo 2 de 3, no meio do bloco de
   instalação, o que sugere que é obrigatório e que faz alguma coisa acontecer.
3. **"Clonei, mas quero instalar em OUTRA pasta"** — a distinção **ferramenta × projeto** não
   está escrita em lugar nenhum. O clone é a ferramenta; o alvo é outro. Os dois sentidos
   (chamar de dentro do projeto, ou de dentro do clone apontando para fora) funcionam, e
   nenhum está documentado.

E há a lacuna gêmea, que o Steward também nomeou: **uma IA que abre este repositório não tem
instrução nenhuma.** O `CLAUDE.md` diz o que fazer para quem **instala** o método num projeto;
o repositório do próprio Maestro não diz nada para quem **chega** nele — o que ler primeiro,
como saber o estado, o que é imutável, como abrir um ciclo.

**E existe um buraco de portão do mesmo tamanho do que o ciclo 058 fechou.** O
`check-flags.sh` confere que toda flag documentada existe. **Subcomando, não.** O README pode
anunciar `maestro deploy` e nada percebe — a mesma classe de mentira, na porta que acabou de
ser construída.

## Requisitos funcionais

- **FR1**: O README DEVERÁ dizer, antes dos comandos, que **o clone é a ferramenta e o alvo é
  outro projeto** — e mostrar as **duas** formas de apontar para fora.
- **FR2**: O README DEVERÁ separar o que **é necessário** do que é **consulta**: `init`
  instala; `agents` só lista e pode ser pulado.
- **FR3**: O README DEVERÁ conter um bloco **endereçado a uma IA que abre este repositório**:
  o que ler antes de agir, o comando que responde "qual é o estado", o que **nunca** reescrever
  e por quê, e como abrir um ciclo.
- **FR4**: QUANDO a documentação anunciar um subcomando de `maestro`, O SISTEMA DEVERÁ
  **reprovar** se ele não existir no despachante — e reprovar também o subcomando que existe e
  não é anunciado, no texto de referência.
- **FR5**: O bloco para IA DEVERÁ apontar apenas para arquivos e comandos **que existem** —
  conferido, não afirmado.

## Fora de escopo

- Reescrever a receita `docs/receitas/instalar-o-maestro.md`. Ela já ganhou o caminho curto no
  ciclo 058; o que falta é a **capa**, que é onde a pessoa chega primeiro.
- Um `CLAUDE.md` diferente para o repositório do Maestro. Ele já existe e já carrega o bloco
  do método; o que falta é o **README**, que é o que uma IA lê quando não há sessão configurada.
- Tornar `maestro` instalável no `PATH` por pacote — segue fora, como no 058.

## Critérios de aceite (DoD)

<!-- Sem caixas: esta seção diz o que deve valer; se valeu, quem diz é o qa-report. -->
- O README responde as três confusões acima, cada uma explicitamente.
- As duas formas de instalar em outra pasta estão escritas, e **as duas foram executadas**.
- O bloco para IA existe, e cada arquivo e comando que ele cita foi verificado no disco.
- O portão reprova subcomando anunciado e inexistente, **e** subcomando existente e não
  anunciado no texto de referência — cada um **visto falhando**.
- Bateria completa, plugin e build verdes.

## Clarify

1. O bloco para IA vai no README ou num arquivo próprio? → **No README**. Um arquivo próprio
   depende de a IA saber que ele existe; o README é o que ela abre sem ser mandada.
2. Ele repete o `CLAUDE.md`? → **Não.** O `CLAUDE.md` é a instrução de quem **segue** o método;
   o bloco é a orientação de quem **chega no repositório do método**. Duplicar seria criar a
   segunda fonte que o Princípio VI proíbe — o bloco **aponta** para ele.
