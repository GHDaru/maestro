# Spec 044 — O `/speckit.plan` defere à tabela de declaração

- **Status**: Concluída · **Raia**: plena · **Data**: 2026-08-07
- **Origem**: `achado-042-speckit-plan-contraditorio`, levantado pela revisão independente
  do ciclo 042. Decisão do Steward no passo 3 da sequência de correções: **emendar o
  comando**, registrando a divergência.

> **Raia**: plena. **Ambiguidade** baixa (a contradição é textual e localizada); **raio**
> amplo (o comando é copiado para todo repositório que instala o método); **irreversibilidade**
> baixa — é texto, e a reversão é um commit.

## O quê e por quê

Quem instalava o Maestro recebia **duas ordens contraditórias**:

| Peça instalada | O que manda |
|---|---|
| `.specify/templates/plan-template.md` | **declarar** os cinco artefatos condicionais (`ART:<nome>=yes\|no` com razão) |
| `.claude/commands/speckit.plan.md` | **gerar** `research.md`, `data-model.md`, `contracts/` e `quickstart.md` — incondicionalmente |

E nada dizia qual vencia. Um agente obediente segue a que leu por último, que é a definição
do anti-padrão 22 aplicada a nós mesmos: metade do defeito foi consertada no ciclo 042 (a
regra passou a ser entregue) e a outra metade — o comando exigindo — sobreviveu.

O `quickstart.md` é pior que contraditório: é um **sexto** artefato que não existe no
catálogo nem no conjunto de tokens. Ninguém saberia o que fazer com ele.

## Requisitos funcionais

- **FR1**: QUANDO o `/speckit.plan` executar as fases 0 e 1, O SISTEMA DEVERÁ produzir
  **apenas** os artefatos declarados `=yes` na tabela do plano.
- **FR2**: QUANDO um artefato for declarado `=no`, O SISTEMA DEVERÁ tratar a razão escrita
  na tabela como o registro daquela decisão — e não gerar o arquivo.
- **FR3**: QUANDO o comando mencionar `quickstart.md`, O SISTEMA DEVERÁ declarar que ele
  **não** é produzido no Maestro, com a razão (função já servida pela jornada e pelas
  receitas — princípio VI).
- **FR4**: QUANDO uma peça vendorizada divergir do upstream, O SISTEMA DEVERÁ registrar a
  divergência em `.specify/UPSTREAM.md`, mudando o estado da peça na tabela.

## Fora de escopo

- Adicionar `quickstart` ao conjunto de tokens `ART:`. Seria criar o artefato para poder
  declará-lo ausente — cerimônia sobre cerimônia.
- Revisar os outros comandos `speckit.*`. Eles leem os templates adaptados e herdam o método
  por eles; só este mandava gerar arquivo por conta própria.
- Sincronizar com o upstream 0.4.3 ou com o fork. Sync é deliberada e entra por spec própria
  (regra 1 do `UPSTREAM.md`).

## Critérios de aceite (DoD)

- [x] As fases 0 e 1 do comando deferem à tabela, com o token citado em cada ponto.
- [x] O comando declara que `quickstart.md` não é produzido, com a razão.
- [x] `.specify/UPSTREAM.md` move `speckit.plan.md` de *Verbatim* para **Adaptado**, com o
      ciclo e o que mudou.
- [x] `UPSTREAM.md` ganha a regra **"divergência declarada, nunca silenciosa"**, com este
      caso como precedente escrito.
- [x] `achado-042-speckit-plan-contraditorio` fechado no índice.

## Clarify

1. Emendar arquivo vendorizado não fere a regra 1 do `UPSTREAM.md`? **Não.** A regra proíbe
   reinstalar por cima e absorver novidade por acidente; ela **exige** que a adaptação entre
   por spec e seja registrada. É exatamente o que este ciclo faz — e o precedente agora está
   escrito como regra 2, para o próximo caso não precisar desta discussão.
