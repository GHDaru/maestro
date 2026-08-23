# Spec 062 — Fechar a v0.3.0

- **Status**: Rascunho · **Raia**: plena · **Data**: 2026-08-22
- **Origem**: o Steward pediu para **ampliar a tag**. O `[Unreleased]` acumulou **18 itens de
  11 ciclos** (051–061) sobre uma v0.2.0 de 2026-08-11 — e nenhuma tag existe no repositório,
  nem a da v0.1.0 nem a da v0.2.0.

> **Raia**: plena. **Ambiguidade** baixa (o conteúdo já está escrito e verificado ciclo a
> ciclo); **raio** amplo (a versão é afirmada em quatro lugares e viaja no instalador);
> **irreversibilidade** média — uma tag publicada é pública, e o `git tag` é o único artefato
> deste ciclo que sai do repositório.

## O quê e por quê

**Medido antes de escrever:**

| Fato | Como se sabe |
|---|---|
| 18 itens em `[Unreleased]`, de 11 ciclos | `grep -cE '^- \*\*'` na região; ciclos 051–061 citados |
| A versão declarada hoje é a **0.2.0**, de 2026-08-11 | `check-version.sh` |
| **Nenhuma** tag existe | `git tag -l` devolve vazio |
| A versão é afirmada em **quatro** lugares | `check-version.sh`: CHANGELOG, README, roadmap, plugin |
| A receita publica um exemplo de JSON com `"maestro_version": "0.2.0"` | `docs/receitas/instalar-o-maestro.md:75` |

### Por que 0.3.0 e não 0.2.1

O intervalo 051–061 não é correção de defeito: entram o instalador que **atualiza**, a escolha
declarada de agente (`--ai`), a porta da frente (`bin/maestro init`), a camada de hooks, e três
portões novos (`check-flags`, e as duas comparações que o `check-installed` ganhou). Comportamento
novo, compatível para trás — **minor**, pelo versionamento semântico.

### A dívida que a nota tem de declarar

A v0.2.0 já registrou que **a tag da v0.1.0 nunca chegou ao GitHub**. Isso continua verdade, e
agora vale para duas versões. Publicar uma tag depende de rede que este ambiente não tem
garantida: se o `git push --tags` falhar, a nota **diz que falhou** em vez de afirmar um
lançamento que não aconteceu. Uma nota de release que anuncia uma tag inexistente é o mesmo
defeito que este método persegue desde o ciclo 042, aplicado ao próprio lançamento.

## Requisitos funcionais

- **FR1**: O `CHANGELOG.md` DEVERÁ ter `[Unreleased]` renomeado para `[0.3.0]` com data, uma
  nota de release dizendo **o que a versão é** e **o que ela reconhecidamente não tem**, e um
  `[Unreleased]` novo e vazio acima dela.
- **FR2**: Os quatro lugares que declaram versão DEVERÃO declarar `0.3.0` — e o
  `check-version.sh` DEVERÁ provar isso, não a memória.
- **FR3**: O exemplo de `install-options.json` publicado na receita DEVERÁ mostrar a versão
  corrente, e algo DEVERÁ compará-lo com o que o instalador realmente grava.
- **FR4**: A tag `v0.3.0` DEVERÁ ser criada. QUANDO a publicação falhar, o ciclo DEVERÁ
  registrar a falha como dívida declarada — nunca afirmar que a tag existe no remoto.
- **FR5**: O roadmap DEVERÁ ganhar a linha da v0.3.0, como tem para a v0.1.0 e a v0.2.0.

## Critérios de aceite

- `check-version.sh` verde com `0.3.0`, e vermelho se qualquer um dos quatro lugares ficar para trás.
- O `[Unreleased]` novo existe e está vazio — um ciclo seguinte tem onde escrever.
- O exemplo da receita é conferido contra a saída real do instalador, não contra o texto.
- O estado da tag no remoto é **verificado**, e o que a nota diz sobre ela é o que foi verificado.
