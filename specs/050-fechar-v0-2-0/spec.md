# Spec 050 — Fechar a v0.2.0

- **Status**: Em andamento · **Raia**: plena · **Data**: 2026-08-11
- **Origem**: decisão do Steward — *"fechamos v0.2.0"*, depois de constatar que a v0.1.0
  aponta para um ponto já ultrapassado em quatro ciclos.

> **Raia**: plena. **Ambiguidade** baixa (o que entrou na versão é factual e está no
> CHANGELOG); **raio** amplo (a versão é o que o mundo lê primeiro);
> **irreversibilidade** média — uma versão anunciada não se desanuncia.

## O quê e por quê

Desde a v0.1.0 (2026-08-09) entraram **quatro ciclos** — 046, 047, 048 e 049 —, e com eles
quatro portões executáveis, a licença, o catálogo do ecossistema e a verificação da cópia
instalada. Continuar chamando isto de v0.1.0 é a mesma classe de defeito que os quatro
ciclos passaram consertando: o registro sobrevivendo ao fato.

Ao preparar o corte, um segundo fato apareceu: **a versão é declarada em quatro lugares** —
o cabeçalho do CHANGELOG, o `README.md`, o cabeçalho do roadmap e o README empacotado no
plugin — e **nada garantia que concordassem**. Quatro cópias de um fato mantidas em acordo
pela memória é a forma que este repositório já encontrou cinco vezes: o índice de perfis, o
índice de ADRs, a tabela de proveniência, a cópia instalada, e agora a versão.

Há ainda um fato desconfortável que a nota precisa declarar: **a tag `v0.1.0` nunca chegou
ao GitHub**. Ela existe no clone deste ambiente e o remoto tem zero tags — o push de tag
recebe 403 do proxy de saída, enquanto o push de branch passa. Uma versão que existe no
CHANGELOG e não existe como tag pública é meia versão, e omitir isso da nota seria
publicidade.

## Requisitos funcionais

- **FR1**: QUANDO uma versão for fechada, O SISTEMA DEVERÁ registrar uma nota de release que
  diz o que a versão **é**, o que ela **reconhecidamente não tem** e **como ela é verificada**.
- **FR2**: QUANDO o repositório declarar uma versão em mais de um lugar, O SISTEMA DEVERÁ
  falhar se as declarações divergirem.
- **FR3**: QUANDO um lugar que costuma declarar a versão deixar de declará-la, O SISTEMA
  DEVERÁ falhar — silêncio num desses lugares é tão ruim quanto divergência.
- **FR4**: QUANDO a tag da versão não puder ser publicada por este ambiente, O SISTEMA DEVERÁ
  declarar isso na nota de release, e não tratar a versão como completa.

## Fora de escopo

- **Criar a tag no GitHub.** O push de tag é bloqueado pelo proxy deste ambiente (403), e a
  orientação é reportar o host barrado em vez de contornar. A tag é o passo humano.
- **Reorganizar o CHANGELOG inteiro.** Edição em massa junto de corte de versão é o
  anti-padrão 18. As subseções repetidas do bloco `[Unreleased]` já foram consolidadas no
  ciclo 048, quando o próprio ciclo ia criar mais duas.
- **Julgar se o número está certo.** `0.2.0` e não `0.1.1` é decisão humana sobre o que
  mudou; o portão mede coerência, nunca mérito (anti-padrão 13).

## Critérios de aceite (DoD)

<!-- Sem caixas: esta seção diz o que deve valer; se valeu, quem diz é o qa-report. -->
- A nota de release da `0.2.0` tem as três partes, e a lista do que **não** tem inclui a tag
  não publicada, o companion, os evals com um caso, os pisos de ciclo e as duas raias
  semeadas e não feitas.
- `scripts/check-version.sh` cobre FR2 e FR3 e foi **visto acusar por mutação** em cada um —
  inclusive o estado real intermediário deste ciclo, com o CHANGELOG já em 0.2.0 e as outras
  três declarações ainda em 0.1.0.
- As quatro declarações concordam, e o portão entra na CI como bloqueante.
- A tag local é criada apontando para o commit da versão, e o comando para publicá-la fica
  escrito para quem tiver rede.

## Clarify

1. **Por que 0.2.0 e não 0.1.1?** Porque entraram quatro portões, uma licença e um catálogo —
   funcionalidade nova, compatível para trás. Em versionamento semântico isso é *minor*.
2. **Por que o portão não viaja?** A versão do projeto que instalou o método é dele, e ele a
   declara onde quiser. O portão lê caminhos que só fazem sentido aqui (`docs/roadmap.md`,
   `plugin/maestro/README.md`); enviá-lo seria enviar um portão que mede o repositório errado.
