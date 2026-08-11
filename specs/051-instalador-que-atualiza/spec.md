# Spec 051 — O instalador que atualiza

- **Status**: Em andamento · **Raia**: plena · **Data**: 2026-08-11
- **Origem**: achado `achado-050-upgrade-sem-force-nao-entrega`, aberto no fechamento da
  v0.2.0 pela revisão independente, e pedido direto do Steward para corrigi-lo.

> **Raia**: plena. **Ambiguidade** média (o que é "atualizar" sem destruir trabalho alheio é
> decisão de desenho); **raio** amplo (roda dentro de repositórios de terceiros e **apaga**
> arquivos); **irreversibilidade** alta o bastante para exigir cuidado — daí a raia.

## O quê e por quê

`install-maestro.sh` pulava qualquer destino que já existisse. Um diretório **sempre** existe
depois da primeira instalação, então **reinstalar não entregava nada**. Quem instalou a
v0.1.0 ficou com o `/speckit.constitution` que mandava *sobrescrever a constituição*, e
continuaria com ele.

Verificado em 2026-08-11, a saída documentada é pior que o problema:

| Comando | Resultado observado |
|---|---|
| `install-maestro.sh <alvo>` (2ª vez) | `= exists (kept)` para tudo — zero arquivos entregues |
| `install-maestro.sh <alvo> --force` | `cp -r src dst` com `dst` já sendo diretório **aninha**: aparece `.claude/agents/agents/` |

O `--force` que a nota de release da v0.2.0 recomendou como contorno **corrompe o layout**.

A causa não é um flag: é falta de fato. Sem registro do que **nós** escrevemos, "difere da
origem" não distingue **versão antiga** de **arquivo que o projeto editou** — e um instalador
que erra essa distinção ou não entrega nada, ou destrói trabalho alheio.

## Requisitos funcionais

- **FR1**: QUANDO o instalador rodar, O SISTEMA DEVERÁ registrar um **manifesto** com o hash
  de cada arquivo que ele escreveu.
- **FR2**: QUANDO um arquivo instalado estiver **inalterado desde a última instalação** e
  diferir da origem, O SISTEMA DEVERÁ atualizá-lo — é versão velha, não trabalho de ninguém.
- **FR3**: QUANDO um arquivo instalado tiver sido **modificado pelo projeto**, O SISTEMA
  DEVERÁ mantê-lo e oferecer a versão nova ao lado, como `<arquivo>.maestro-new`.
- **FR4**: QUANDO o método deixar de enviar um arquivo que já enviou, O SISTEMA DEVERÁ
  removê-lo do destino **se ainda estiver inalterado**, e mantê-lo se tiver sido modificado.
- **FR5**: QUANDO o destino for um diretório que já existe, O SISTEMA DEVERÁ escrever
  **arquivo a arquivo** e nunca aninhar um diretório dentro de si mesmo.
- **FR6**: QUANDO a instalação for anterior ao manifesto, O SISTEMA DEVERÁ **não sobrescrever
  nada** e dizer isso explicitamente — sem manifesto não há como distinguir velho de editado.

## Fora de escopo

- **Migrar conteúdo** (reescrever um arquivo do projeto para o formato novo). O instalador
  entrega arquivos; conciliar edição é decisão humana, e é para isso que serve o
  `.maestro-new` ao lado.
- **Versionar a instalação** (guardar de qual release veio). O manifesto guarda hashes, que
  é o que responde a pergunta que importa: *este arquivo ainda é o que eu escrevi?*

## Critérios de aceite (DoD)

<!-- Sem caixas: esta seção diz o que deve valer; se valeu, quem diz é o qa-report. -->
- `scripts/check-installed.sh` ganha o cenário de **upgrade** e cobre FR2 a FR5, com cada um
  visto vermelho antes da correção.
- Reinstalar sem mudança nenhuma é **idempotente** e diz `already current`.
- `--force` sobrescreve arquivo a arquivo e **não** aninha diretório.
- O caminho anterior ao manifesto preserva tudo e explica por quê.

## Clarify

1. **Por que hash e não data de modificação?** Porque `mtime` muda com um `touch`, com um
   `git checkout` e com a cópia; conteúdo é o fato.
2. **Por que remover o que não é mais enviado?** Porque foi assim que o
   `.specify/memory/constitution.md` — apagado no ciclo 048 — continuaria em toda instalação
   antiga, mandando um agente sobrescrever a constituição. Instalação que só acumula carrega
   os erros do método para sempre.
