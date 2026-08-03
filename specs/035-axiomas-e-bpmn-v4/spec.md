# Spec 035 — Axiomas do projeto e BPMN v4

- **Status**: Concluída · **Raia**: plena · **Data**: 2026-08-03
- **Origem**: pedido do Steward — "vamos definir um conjunto de axiomas, teoremas ou
  corolários que serão as verdades assumidas para todo o projeto" e "atualize o BPMN".

> **Raia**: plena. **Ambiguidade** alta (não havia forma dada de escrever axiomas de um
> método); **raio** amplo (a camada passa a ser referência de toda regra futura, e o desenho
> do processo é a porta de entrada do livro); **irreversibilidade** baixa. Dois fatores
> altos → plena.

## O quê e por quê

O corpo de regras chegou a oito princípios, dezoito anti-padrões e oito portões. Nesse
tamanho, "de onde vem esta regra?" começa a ter respostas diferentes conforme quem responde —
e a poda por YAGNI só tem critério negativo. Faltava a camada contra a qual uma regra nova é
**argumentada** e uma regra velha é **podada**.

O BPMN (*Business Process Model and Notation*, Notação de Modelagem de Processos de Negócio)
também ficou desatualizado em dois pontos que os ciclos 033 e 034 mudaram: os nomes em inglês
e — mais importante — a retrospectiva agora **tem gatilho**, e existe uma família inteira de
portões que o desenho não mostrava.

## Requisitos funcionais

- **FR1**: O documento de axiomas DEVE separar explicitamente **axioma** (assumido),
  **teorema** (derivado) e **corolário** (consequência imediata).
- **FR2**: QUANDO um axioma é declarado, ele DEVE vir com o teste de **independência** — o
  que quebra no método se ele for removido.
- **FR3**: QUANDO um teorema é declarado, ele DEVE trazer **evidência deste repositório**,
  incluindo a evidência desfavorável quando existir.
- **FR4**: A constituição DEVE apontar para os axiomas, sem que o Constitution Check mude de
  objeto (continua checando os oito princípios).
- **FR5**: O documento DEVE ser instalável — e portanto escrito em inglês (ADR 0014),
  passando em `check-language.sh`.
- **FR6**: O BPMN DEVE mostrar o gatilho da retro, a raia de portões e os nomes em inglês,
  nas duas versões (navegável e imagem).

## Fora de escopo

- Reescrever os princípios em função dos axiomas (a constituição segue como norma operativa).
- Ampliar o conjunto além de cinco axiomas sem dor que o justifique.

## Critérios de aceite (DoD)

- [x] `docs/governance/axioms.md` com 5 axiomas, 6 teoremas e 10 corolários
- [x] Cada axioma com teste de independência; cada teorema com evidência do repositório
- [x] `check-language.sh` verde (o documento é instalável e está em inglês)
- [x] `check-links.sh` verde após a mudança do BPMN
- [x] BPMN navegável com 7 raias; imagem regenerada do mesmo fonte
- [x] Publicado no livro (trilha Referência), site com 36 páginas

## Clarify

1. Axiomas substituem os princípios? → **não**: princípios continuam sendo a norma; axiomas
   são a camada de derivação.
2. Quantos axiomas? → **cinco**, com a regra explícita: se um princípio não deriva de nenhum,
   ou falta axioma (entra por ADR) ou sobra princípio (poda).
