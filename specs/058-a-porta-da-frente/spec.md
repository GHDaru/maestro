# Spec 058 — A porta da frente: `maestro init`

- **Status**: Rascunho · **Raia**: infra · **Data**: 2026-08-17
- **Origem**: pedido do Steward — *"quero algo similar ao spec-kit: uso um instalador, depois
  chamo `maestro init` e sigo o passo a passo"* — mais dois defeitos que apareceram ao tentar
  responder "como eu instalo o Maestro?".

> **Raia**: infra. **Ambiguidade** média — o modelo é conhecido (`specify init`), mas o que um
> passo a passo interativo deve perguntar não é dedutível. **Raio**: é a **primeira coisa** que
> qualquer pessoa nova executa; errar aqui erra na porta. **Irreversibilidade** baixa — cria
> arquivos e chama o instalador, que já é reversível e não sobrescreve.

## O quê e por quê

**Hoje o Maestro não tem porta.** Para instalar é preciso clonar, achar
`scripts/install-maestro.sh`, saber que existe `--ai list`, saber que existe `--write-block`,
e depois lembrar de rodar `check-install.sh`. Nada disso está numa tela só. No site, chegar até
a receita são **quatro cliques**, pela trilha que se anuncia como *"~1 dia"*.

O upstream resolveu isso com um verbo: `specify init` — banner, perguntas, estrutura criada,
próximos passos impressos. É a mesma informação que já temos, com uma ordem e um rosto.

**E medir a documentação para responder "como instalo?" achou três mentiras**, todas da família
que este método persegue — um fato dito em dois lugares sem nada comparando:

| Onde | Diz | É |
|---|---|---|
| `docs/receitas/instalar-o-maestro.md` | *"use `--forcar`"* | a flag é `--force`; quem segue a receita toma erro |
| a mesma receita | *"o script **não sobrescreve**"* | desde o ciclo 051 ele **atualiza**, com manifesto |
| o `# Usage` do `install-maestro.sh` | três formas de uso | não cita `--ai`, `--no-hooks` nem `--write-block` |

Nenhum dos 16 portões pega isso: nada confere que a documentação de uma flag corresponde às
flags que existem.

## Requisitos funcionais

- **FR1**: O SISTEMA DEVERÁ oferecer um comando único — `maestro` — com `init` entre os
  subcomandos, e `maestro` sem argumento DEVERÁ imprimir o que ele sabe fazer.
- **FR2**: `maestro init` DEVERÁ conduzir um **passo a passo**: identidade visual, escolha do
  agente (lida da **mesma** tabela do ciclo 057, nunca uma segunda lista), destino, instalação,
  bloco de método, e verificação — terminando com o que fazer a seguir.
- **FR3**: O SISTEMA DEVERÁ ser **executável sem humano**: toda pergunta tem forma de flag
  (`--ai`, `--yes`), e sem terminal interativo ele **não pergunta** — usa o declarado ou
  recusa. Ferramenta que só funciona com alguém digitando não pode ser testada, e o que não é
  testado não é portão.
- **FR4**: Cada subcomando DEVERÁ **chamar o script que já existe**, nunca reimplementar. Uma
  segunda implementação do mesmo passo é o anti-padrão 22 com outro nome.
- **FR5**: `maestro init` DEVERÁ terminar rodando a verificação e **dizer o veredito** — não
  basta instalar e declarar sucesso (*prove, não afirme*).
- **FR6**: O SISTEMA DEVERÁ ter um portão que compare as **flags que o parser aceita** com as
  **documentadas**, e os dois sentidos **não valem para os mesmos documentos**:
  - **texto de referência** (`# Usage`, `usage()`) — é o contrato do comando: **os dois
    sentidos**, flag aceita tem de estar listada, flag listada tem de existir;
  - **prosa** (a receita, o README) — mostra um **subconjunto** de propósito e cita mais de um
    comando: **um sentido**, toda flag que ela nomeia tem de existir em algum parser. É o
    sentido que produziu a mentira nº 1 e o que custa uma mensagem de erro ao leitor.
  > Exigir os dois sentidos em toda parte forçaria uma capa que documenta tudo, ou uma lista de
  > exceções que ninguém manteria. O parecer do ciclo cobrou a versão anterior desta frase.
- **FR7**: O site DEVERÁ ter uma **porta rápida** — a instalação alcançável da capa, sem passar
  por uma trilha de um dia.

## Fora de escopo

- Distribuição por gerenciador de pacotes (`uv tool install`, `npm -g`, *tap* de Homebrew).
  O caminho deste ciclo é clonar e chamar `./bin/maestro`; empacotar é decisão de distribuição
  com custo de manutenção próprio, e o gatilho é alguém pedir.
- Instalar o `maestro` dentro do projeto de destino. Ele é a **porta**, e a porta fica do lado
  de fora; o que o projeto recebe continua sendo `scripts/`.
- `maestro` para agentes que não o Claude além do que a tabela do 057 já resolve.

## Critérios de aceite (DoD)

<!-- Sem caixas: esta seção diz o que deve valer; se valeu, quem diz é o qa-report. -->
- `maestro` sem argumento lista os subcomandos e sai com sucesso.
- `maestro init <dir> --ai <id> --yes` instala, escreve o bloco, verifica e imprime o veredito,
  **sem nenhuma pergunta**, em terminal não interativo.
- `maestro init` com `--ai` inválido recusa antes de tocar em disco.
- Nenhum subcomando reimplementa passo que já existe em `scripts/`.
- O portão de flags reprova nos dois sentidos, **visto falhando** em cada um.
- As três mentiras da tabela acima estão corrigidas, **e uma quarta cópia foi achada**: o
  `README.md` — a primeira página — repetia `--forcar` e o "não sobrescreve", e o portão não a
  olhava. O portão passa a cobrir as **quatro** fontes.
  > **Limite declarado**: o portão mede **flags**. A mentira nº 2 ("não sobrescreve") é
  > **prosa sobre comportamento**, não uma flag — foi corrigida em três arquivos e **não é
  > coberta por portão nenhum**. Prosa que descreve comportamento continua dependendo de
  > revisão, e dizer isso é melhor que fingir cobertura.
- Da capa do site, a instalação está a **um** clique.
- Bateria completa, plugin e build verdes.

## Clarify

1. O banner é enfeite? → **Não, e não é neutro**: ele é o que diz *"isto tem dono e tem
   versão"*. Imprime nome e versão lida do `CHANGELOG`, então também é verificação — banner com
   versão errada é a primeira coisa que alguém nota.
2. `init` pergunta ou recebe flags? → **Os dois, e flags vencem**. Sem TTY, não pergunta.
