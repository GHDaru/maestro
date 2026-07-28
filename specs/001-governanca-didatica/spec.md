# Spec 001 — Governança didática (camada de onboarding)

- **Status**: Em revisão (aguardando aprovação — DoR) · **Raia**: Plena · **Data**: 2026-07-28
- **Origem**: feedback do mantenedor — a governança está "pesada, um amontoado de siglas
  sem dicionário e sem storytelling".
- **Abordagem** (clarify): **híbrida** — este ciclo entrega a *camada didática nova*; a
  reescrita narrativa dos 12 capítulos fica para ciclos futuros (fora de escopo).

## O quê e por quê (valor)

Hoje um leitor novo cai direto num compêndio denso: siglas sem expansão (DoD, RACI, DoR,
ADR, YAGNI, DORA, WIP, CI…), 12 capítulos sem fio narrativo e referências a "a Constituição"
que apontam para o repositório de origem. Resultado: alta barreira de entrada, baixa
didática.

**Valor**: reduzir o tempo-para-entender do Maestro criando uma **porta de entrada
narrativa** e um **glossário**, sem reescrever (ainda) o conteúdo de referência que já
funciona. Serve a jornada **"primeiro contato com a metodologia"**.

## Jornada servida

**J1 — Onboarding de um novo leitor (humano ou agente)**: chega ao repo → lê um guia curto
que conta a história (dor → jornada → sistema) → entende o mapa e para onde ir → ao
encontrar uma sigla, tem a expansão na primeira ocorrência e um glossário para consulta.

## Requisitos funcionais (critérios de aceite testáveis)

- **FR1 — Guia "Comece por aqui"**: existe `docs/comece-por-aqui.md`, narrativo e curto
  (≤ ~2 páginas), na sequência **dor → jornada → sistema → como usar**, terminando com um
  mapa de leitura que aponta para princípios, modelo e handbook. Linkado no `README.md`.
- **FR2 — Glossário**: existe `docs/governance/glossario.md` definindo **100% das siglas**
  usadas nos documentos de governança e handbook. Cada verbete: sigla, expansão, 1 frase de
  significado no contexto Maestro, e link ao capítulo/elemento onde é tratada.
- **FR3 — Expansão na 1ª ocorrência**: em cada documento de `docs/governance/` e
  `docs/handbook/`, toda sigla é expandida na **primeira vez** que aparece no corpo do texto
  (ex.: "Definition of Done (DoD)"), com link ao glossário na primeira ocorrência do doc.
- **FR4 — Rebasing de referências (follow-up #1)**: toda referência a "a Constituição" e a
  "Princípio IV/V/VII" nos documentos migrados passa a apontar para
  `docs/governance/principios-maestro.md` (usando o mapa de linhagem já registrado nele).
  **Nenhuma referência dangling** para a constituição da plataforma de origem.
- **FR5 — PDFs regenerados**: o `maestro-compendio-governanca.pdf` e o `maestro-handbook.pdf`
  são regenerados incluindo o guia e o glossário; o compêndio ganha o guia como abertura da
  Parte I e o glossário como apêndice.

## Fora de escopo (explícito)

- Reescrita narrativa do corpo dos 12 capítulos (abordagem híbrida → ciclos futuros, um
  capítulo por vez).
- Alinhar os templates do Spec Kit do maestro à fork `GHDaru/spec-kit` (follow-up próprio).

## Critérios de aceite (Definition of Done desta feature)

- [ ] Toda sigla presente nos docs está no `glossario.md` (cobertura 100%); nenhuma sigla
      nova sem verbete.
- [ ] Nenhuma sigla aparece pela primeira vez, em qualquer doc de governança/handbook, sem
      expansão.
- [ ] `grep` por "Constituição" / "Princípio IV|V|VII" nos docs migrados não retorna
      referência ao repositório de origem (só a `principios-maestro.md`).
- [ ] `comece-por-aqui.md` existe, é narrativo e está linkado no `README.md`.
- [ ] PDFs regenerados e commitados; CHANGELOG atualizado.

## Riscos / ambiguidades resolvidas

- Escopo poderia inflar para "reescrever tudo" → **contido** pela decisão híbrida.
- Expansão de siglas poderia poluir → limitada à **primeira ocorrência por doc**.

## Apetite

Um ciclo curto. Se estourar, corta-se FR5 (PDFs) antes de FR1–FR4 (o conteúdo é o núcleo).
