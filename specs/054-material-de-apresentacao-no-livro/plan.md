# Plan 054 — Material de apresentação dentro do livro

- **Spec**: `spec.md` · **Lane**: plena · **Date**: 2026-08-14

## Constitution Check (governance/principles.md)

| Principle | Compliance |
|---|---|
| I. Spec-driven | ✅ Seis FRs; os de reprovação (FR2, FR3, FR4, FR6) são exatamente o que a mutação prova, um a um. |
| II. Human-governed orchestration | ✅ O que entra no livro continua sendo declaração explícita no `sumario.json`; o motor publica o que foi declarado, nunca o que encontrou varrendo pastas. |
| III. Reversibility / risk gates | ✅ `site/` é regenerado a cada build e não é fonte; reverter é reverter o commit. O risco real é **quebrar um portão bloqueante**, e é por isso que a raia é plena e a mutação é obrigatória. |
| IV. Test-first / verifiable DoD | ✅ **seis** reprovações escritas e **vistas falhando** antes de o ciclo fechar (a primeira versão dizia três, e uma delas não reprovava de fato — a revisão executou e mostrou). Portão nunca visto vermelho não é portão (anti-padrão 16). |
| V. Context economy / boundary | ✅ **depois da correção.** A primeira versão dizia "nenhuma fronteira nova" e estava errada: material é um **segundo canal de publicação**, e o `check-boundary.sh` lia só o primeiro — um arquivo do `toolkit` declarado como material ia para o site com o portão dizendo tudo certo. O portão passou a ler os dois canais, e a mutação prova. |
| VI. Living artifacts | ✅ O material é publicado **do arquivo de origem**, não de uma cópia: editar o deck e rodar o build é tudo o que existe. Não há segunda cópia para envelhecer. |
| VII. Light governance / YAGNI | ✅ Um campo novo no `sumario.json` e ~40 linhas no motor. Nenhum formato novo, nenhuma dependência nova, nenhuma configuração. |
| VIII. Intelligible communication | ✅ **depois da correção.** A revisão conferiu e nenhuma das três mensagens dizia o que fazer — só o que houve. Cada uma ganhou a linha `→ ...` com a ação. O material publicado ganha a volta para o livro, que é o que um leitor perdido procura. |

## Artifacts of this cycle (declare all five — silence is not a decision)

<!-- Read by scripts/check-conformance.sh. Declaring =yes means the file MUST exist here.
     What each one is for: docs/governance/artifacts.md -->

| Artifact | Declaration | Why |
|---|---|---|
| `research.md` | `ART:research=no` | Nenhuma incógnita: o motor foi lido inteiro antes do plano, e as três restrições (reescrita de links, portão de links, limpeza de `site/`) estão nomeadas abaixo. |
| `data-model.md` | `ART:data-model=no` | Nenhuma entidade nova com relações: `material` é um campo de lista no `sumario.json`, com a mesma anatomia de um item (`arquivo`, `titulo`, `teaser`). |
| `contracts/` | `ART:contracts=no` | A única interface é o próprio `sumario.json`, cujo contrato está descrito em "How" e é lido por um consumidor só. |
| `checklist.md` | `ART:checklist=no` | Critérios de aceite curtos, e seis deles provados por mutação — a lista de verificação seria a mesma tabela, escrita duas vezes. |
| `ux-design.md` | `ART:ux-design=no` | Reusa o cartão (`.s-card`) e o cabeçalho de seção (`.s-parte`) do tema. **Introduz uma afinidade nova**, a volta `↩ livro`: sete linhas de CSS embutidas, e embutidas por necessidade — o material não carrega `assets/estilo.css`, senão deixaria de ser autocontido. A revisão cobrou a versão anterior desta linha, que dizia só "reusa". Um `ux-design.md` para um link de volta seria cerimônia; a decisão fica registrada aqui. |

## How

Três restrições do motor, todas descobertas lendo `publicar/build.mjs` antes de escrever:

1. **`resolverHref` manda para o GitHub tudo que não seja `.md` publicado** (`:60`). Um link
   para o material precisa ser reconhecido **pelo caminho de origem** e virar `<slug>.html`.
2. **O portão de links compara `basename(href)` com o conjunto `paginas`** (`:187`, `:198`).
   O material tem de entrar nesse conjunto, ou todo link para ele reprova o build.
3. **A limpeza apaga todo `.html` no topo de `site/` menos a capa** (`:133`). Material
   publicado na raiz é regenerado a cada build — é o comportamento certo, e não precisa de
   exceção.

Sobre isso, a implementação:

- `sumario.json` ganha `materiais: [{ arquivo, titulo, teaser }]`, com `arquivo` apontando
  para um `.html` do repositório.
- O slug do material entra **no mesmo mapa de colisão dos itens**, porque disputa o mesmo
  espaço de nomes em `site/` (FR3).
- Material declarado e ausente do disco **falha o build** (FR4), com o caminho na mensagem.
- A publicação **envolve** o fragmento num documento mínimo (`<!doctype>`, charset, viewport,
  título vindo **só** do `titulo` do `sumario.json`) e injeta **uma** âncora fixa de volta
  para `sumario.html` (FR5). O arquivo de origem não é alterado: o livro é adapter, a fonte é
  uma só — a mesma tese que o cabeçalho do motor declara. Ler também o `<title>` do arquivo
  dava **duas** fontes para o mesmo nome, e elas já divergiam na primeira tentativa.
- O mapa de colisão passa a conter também `index` e `sumario`, que existem em `site/` sem
  serem itens (FR3), e o `check-boundary.sh` passa a ler `materiais` (FR6).
- `resolverHref` passa a resolver caminho de material para `<slug>.html`, e `paginas` passa a
  contê-lo (FR1, FR2).
- O sumário ganha a seção **Material**, com os mesmos cartões das partes.

## Verification (DoD)

| Comando | Esperado |
|---|---|
| `node publicar/build.mjs` | verde; **39** páginas (38 + o material) |
| mutação 1: apontar o material para caminho inexistente | build **falha** nomeando o caminho |
| mutação 2: material com slug de página existente | build **falha** nomeando a colisão |
| mutação 3: link `.html` **em bloco HTML** para página não publicada | build **falha** como link quebrado |
| mutação 4: material chamado `index.html` | build **falha** — a capa mantida à mão não é sobrescrita |
| mutação 5: material chamado `sumario.html` | build **falha** — em vez de publicar e descartar calado |
| mutação 6: material de domínio `toolkit` | `check-boundary.sh` **falha** nomeando o arquivo |
| bateria de 16 portões · plugin | verdes salvo `check-retro` (dívida do achado 047, declarada) |
