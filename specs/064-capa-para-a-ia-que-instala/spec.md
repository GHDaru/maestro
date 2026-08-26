# Spec 064 — Capa para a IA que instala

- **Status**: Em execução · **Raia**: leve · **Data**: 2026-08-26
- **Origem**: pedido do Steward — "atualize o readme, as orientações de capa para a IA
  instalar o maestro".

> **Raia**: leve. **Ambiguidade** baixa (o defeito é medido, não inferido); **raio** contido
> a uma página e a um portão; **irreversibilidade** baixa (texto e uma comparação a mais).
> Leve não afrouxa revisão independente nem `TAIL:mutation` — o ciclo mexe num portão.

## O quê e por quê

O README tem duas seções endereçadas a uma IA — "Se você é uma IA e acabou de abrir este
repositório" e "Instalar o Maestro no seu projeto", esta última com um bloco que começa
literalmente em "Para uma IA que leu isto". **Nenhuma das duas serve a uma IA que vá
instalar.**

Medido em 2026-08-26, no comando que o README publica:

```
$ ./bin/maestro init <dir> </dev/null
maestro: no terminal to ask about which agent. Declare it (agent), or pass --yes to accept 'claude'.
exit=2 · arquivos escritos: 0
```

Sessão de agente **não tem terminal**. O README publica só a forma interativa, então a IA que
seguir a página ao pé da letra não instala nada — e o erro que ela recebe não se parece com um
erro de instalação. A receita (`docs/receitas/instalar-o-maestro.md`) já diz `--yes` e já
explica a recusa desde o ciclo 057; o README ficou para trás. É o anti-padrão 23 na forma
mais barata: a porta nova foi aberta numa página e a outra nunca soube.

Outros quatro defeitos medidos na mesma página:

- **Os ids do `--ai` não aparecem** — o README manda consultar `maestro agents`, uma ida e
  volta a mais para um agente. O ciclo 060 mostrou o que um id errado custa: o leitor para no
  passo 0 com `error: unknown agent 'cursor'`.
- **A tabela das cinco camadas e os comandos de verificação estavam sob a seção C** ("só as
  skills"), descrevendo o caminho A. Quem escolheu C recebia instrução do que não instalou.
- **A verificação apontava `check-agents.sh`**, que mede uma camada, onde o portão da
  instalação inteira é `check-install.sh` — o que a receita usa, e o único que reprova
  enquanto o `CLAUDE.md` não apontar para o método.
- **"Handbook — 12 capítulos"**, e `docs/handbook/` tem 13 capítulos numerados.

E o defeito de fundo, que é o do método e não o da página: **o portão de ids lia só a
receita**. O README podia publicar um id que o instalador recusa e nada reprovava.

## Requisitos funcionais

- **FR1**: O README DEVERÁ publicar, como primeira forma do comando, a que funciona **sem
  terminal** (`--ai <id> --yes`), dizendo o código de saída e a mensagem de quem omite `--yes`.
- **FR2**: O README DEVERÁ publicar a tabela dos ids que o `--ai` aceita, e essa tabela
  DEVERÁ ser comparada por portão contra `scripts/install-agents.tsv`, nas duas direções.
- **FR3**: QUANDO o README deixar de publicar a tabela de ids, O SISTEMA DEVERÁ **reprovar** —
  ausência não é aprovação (anti-padrão 16).
- **FR4**: O README DEVERÁ separar as duas situações de uma IA que chega — instalar em outro
  projeto × trabalhar no método aqui — antes de qualquer instrução.
- **FR5**: A verificação pós-instalação publicada DEVERÁ ser `check-install.sh`, rodado de
  dentro do projeto alvo.

## Critérios de aceite (DoD)

- `scripts/check-installed.sh` compara os ids das **duas** páginas e sai 0.
- Cada contagem que o README anuncia é conferida contra uma instalação real (o portão de
  contagens já lê o README) — subagentes, skills, scripts, portões, comandos e templates.
- As três mutações do portão de ids reprovam: id fantasma, tabela ausente, id esquecido.
- `check-flags.sh` verde: toda flag que o README promete existe no parser, e vice-versa.
- Os 14 portões bloqueantes verdes, mais `check-conformance.sh --ticked-only`.
