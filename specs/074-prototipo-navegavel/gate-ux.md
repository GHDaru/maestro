# Gate de UX do ciclo 074 — decidido por delegação (ADR 0026), 27/10/2026, sobre ef72e04

**Decisão da regente: APROVADO COM AJUSTES** — o Gerente aplica os ajustes abaixo no
`ux-design.md` (e os dois toques na `spec.md`) **no mesmo commit** do `plan.md`; não há nova
rodada de gate de UX. Crítico em contexto fresco: `process-guardian` (Sonnet). Gate de spec:
ajustes B1, B2, S1, S2, S3, S5, S6 conferidos como aplicados em `ef72e04`.

## As três decisões declaradas na seção 9

1. **Tela inicial com `data-contexto="regencia"` — ACEITA.** Declarar que a inicial é a vista do
   contexto Regência (o verificador (d) exige um dos cinco valores).
2. **Quebra em 768px e barra inferior com "3 a 6 itens" — ACEITA COM AJUSTE.** O briefing fixa seis
   itens; o design system (§ 4, "3 a 5") cede. O valor **não** é token consumido em `@media`
   (variável CSS não vale em media query): é constante comentada em `tokens.css` e em `app.js`,
   marcada **provisória até a captura do build real em 360 px** (a jornada viva confere se
   "Administração" cabe a 12 px). O `design-system.md` do 073 **não é editado** durante o
   julgamento do 073: a emenda (quebra, trilha de contexto, aviso de simulação, "3 a 6") vira
   **tarefa do plano do 074**.
3. **Chips de filtro e segmentos são botões de escrita — ACEITA.** Consequência mecânica do S1;
   filtro de frente e segmento de período levam `data-autoriza="humano"` e `data-simulado="sim"`.

## Bloqueantes aceitos (texto do crítico, a aplicar)

- **B-UX1 — § 5.** Acrescentar: "Botão irreversível declara `data-irreversivel="sim"` e
  `data-confirma="<id da confirmação>"`. Botão com `data-acao="derrubar"` declara
  `data-alvo="nome · ref · projeto"`. A verificação (h) falha se `data-alvo` começar por
  `Gerente`. A verificação (i) falha se o id de `data-confirma` não existir ou se a confirmação
  não tiver `data-perde` e `data-reverte`."
- **B-UX2 — § 3, J2 passo 3.** "cartão parado em G3 → painel de detalhe na própria tela (expansão;
  botão `data-acao="detalhar"`, `data-autoriza="humano"`, `data-simulado="sim"`,
  `data-efeito="mostra o veredito normalizado e o original ao lado"`)".

## Secundários aceitos

- **S-a** contagem única de fragmentos: **15** (a inicial é um deles) na `spec.md` FR3 e no `ux-design.md`.
- **S-b** origem do projeto `maestro`: `repos[0].nome` de `painel/projetos/exemplo.json`; declarar
  a diferença para o roster `410_MAESTRO` do 073 (retrato datado).
- **S-c** tabela ENTRA: segunda coluna prefixada "ENTRA"; J1 ganha o passo 6 ("item Regência: a
  frase-chave mostra 2 decisões"); J5: botão renomeado para "Enviar ao endereço ambíguo" (ou
  efeito descrito como resolução pelo ref) **e** passagem pela confirmação `data-perde`/`data-reverte`;
  J3: **reiniciar entra na lista de irreversíveis do § 5** (ref novo; contexto só volta por `--resume`).
- **Coluna "decisão que serve"** em § 2 para toda tela; as só-leitura dizem "só leitura".
- **Anatomia mínima** (estados e atributos) da trilha de contexto e do aviso de simulação no
  próprio `ux-design.md`; a entrada no design system é tarefa do plano (ver decisão 2).
- **S-d** Princípio VIII: expandir FR/NFR na primeira ocorrência do `ux-design.md`; podar DDD, JSON,
  CSS não usados; expandir UX antes do título; `spec.md` expande ENTRA.
- **S-e** glossário (`docs/governance/glossary.md`, inglês, "Cycle 074"): frase-chave, trilha de
  contexto, aviso de simulação, e as quatro ações "Propor regra", "Endereçar por ref",
  "Registrar ruling", "Drenar outbox" como verbos sobre termos — tarefa do plano (Worker01).
- **S-f** § 2.3 diz que "Políticas" e "Orçamento" são rótulos curtos de "política declarativa" e
  "limite de orçamento"; "Ajustar teto" remete a "limite de orçamento".
- Auditoria (linha 5 da tabela): Políticas e Catálogo levam uma linha de fixture do histórico
  visível ao crítico.

## Parecer do crítico (síntese)

Veredito APROVAR COM AJUSTES. Papel semântico por tela presente e antes do componente; cinco
jornadas dentro de três cliques a partir da inicial; tabela ENTRA completa (15 + 3 + ENTRA 16)
e coerente com o confronto e o README do 073. Bloqueantes: atributos de (h)/(i) não nomeados;
J2 passo 3 sem destino. Secundários: contagem 14 × 15; origem de `maestro`; decisão do humano
ausente em cinco telas; papéis novos sem anatomia nem entrada no catálogo; J1.6, J5 e J3;
numeração da tabela; siglas FR/NFR/UX/ENTRA; glossário sem os termos novos; rótulos curtos.
Rótulos amostrados: 10 no glossário, 4 fora (os termos novos). Idioma correto. Não leu o mapa
§ 6, o ux-design do 072 nem a skill `living-journey`.
