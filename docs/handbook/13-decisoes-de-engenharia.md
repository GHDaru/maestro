# 13 — Decisões de engenharia de software (por que o Maestro é assim)

> **Capturado em** 2026-08 · última revisão 2026-08-01 · ciclo 013
> *Capítulo-piloto do novo padrão editorial ([guia](../livro/guia-editorial.md)).*

## 1. Objetivos

Ao fim deste capítulo você será capaz de:

1. **Nomear** as decisões de engenharia que sustentam o Maestro e a data em que foram tomadas;
2. **Explicar** o problema que cada uma resolve e o efeito colateral que provoca;
3. **Avaliar** se uma decisão continua pagando o próprio custo no seu contexto;
4. **Aplicar** o mesmo formato (decisão → porquê → efeito → custo) às suas próprias escolhas.

## 2. O problema

Um método herda decisões técnicas silenciosas. Alguém escolheu Desenvolvimento Guiado por
Especificação (SDD), alguém escolheu testes primeiro, alguém escolheu registrar decisões —
e três meses depois ninguém sabe **por quê**. O time então (a) segue a regra sem entender,
virando burocracia, ou (b) abandona a regra na primeira fricção, perdendo o benefício.

Pior: sem o **porquê** registrado, não dá para saber quando a regra **parou** de valer.
Uma decisão só é revogável se o critério que a justificou estiver escrito.

## 3. A ideia central

> **Toda decisão de engenharia tem um preço; adotá-la sem escrever o preço é contrair
> dívida sem contrato.**

Por isso cada decisão abaixo declara quatro coisas: **quando** foi tomada, **por que**,
**o que faz** e **o que provoca** — inclusive o efeito indesejado que aceitamos.

## 4. A regra vigente

Toda decisão material de metodologia vira **ADR** (Registro de Decisão de Arquitetura) —
imutável, com contexto, alternativas, decisão e consequências. Este capítulo é o
**mapa didático** desses registros: a versão que se lê para *entender*, não para auditar.

### 4.1 O quadro completo

| # | Decisão | Quando | Registro |
|---|---|---|---|
| 1 | Spec-Driven Development (a spec é a fonte de verdade) | 2026-07-22 | Princípio I |
| 2 | Uma ferramenta de spec só (Spec Kit); OpenSpec descartado | 2026-07-22 | ADR 0005 |
| 3 | Raias de trabalho (leve/plena/infra) | 2026-07-22 | ADR 0005 |
| 4 | Testes primeiro, cobertura pragmática (feliz + falha) | 2026-07-22 | Princípio IV |
| 5 | Fitness functions (arquitetura testada na integração contínua) | 2026-07-22 | Princípio IV/V |
| 6 | Corte por fronteira (DDD / hexagonal) | 2026-07-22 | Princípio V |
| 7 | Reversibilidade engenheirada (gate ∝ risco) | 2026-07-22 | Princípio III |
| 8 | ADR imutável + append-only | 2026-07-22 | Princípio VII |
| 9 | Forcing function no changelog (bloqueia na CI) | 2026-07-22 | ADR 0006 |
| 10 | YAGNI como poda ativa | 2026-07-22 | Princípio VII |
| 11 | Registro consultável por máquina (JSONL) | 2026-07-31 | ADR 0009 |
| 12 | Sintaxe EARS nos critérios de aceite | 2026-07-31 | ADR 0008 |
| 13 | Vendorização (templates como fonte nossa) | 2026-07-31 | ciclo 009 |
| 14 | Iron Laws (enforcement linguístico nas skills) | 2026-07-31 | ciclo 011 |

## 5. Fundamentos — decisão por decisão

### 5.1 Spec-Driven Development — a spec é a fonte de verdade

- **Por quê**: quando o agente reescreve o código a cada iteração, o código deixa de ser o
  artefato durável. A intenção precisa morar em algo que **gera** o código, não que o descreve.
- **O que faz**: nenhum código nasce sem especificação aprovada; o fluxo é
  `specify → clarify → plan → tasks → implement`.
- **O que provoca**: ✅ documentação que não apodrece (é input, não subproduto);
  ⚠️ **custo de entrada** — escrever spec para mudança trivial é cerimônia de papel. Foi
  exatamente essa dor que gerou a decisão 3 (raias).

### 5.2 Uma ferramenta de spec só

- **Por quê**: o OpenSpec oferecia um modelo *delta* atraente para mudanças pequenas. Manter
  duas ferramentas de SDD dobraria a carga cognitiva e a manutenção.
- **O que faz**: Spec Kit é o motor único; a boa ideia do concorrente foi **absorvida como
  conceito** (a raia leve), não como segunda ferramenta.
- **O que provoca**: ✅ um lugar só para procurar; ⚠️ dependência de um upstream — mitigada
  depois pela decisão 13 (vendorização).

### 5.3 Raias de trabalho (leve / plena / infra)

- **Por quê**: o valor de uma spec escala com `ambiguidade × raio de impacto ×
  irreversibilidade`. Quando os três são baixos, a spec é papel.
- **O que faz**: bug/typo → raia **leve** (o pull request é o artefato); feature ambígua →
  **plena** (ciclo completo); infra/migração → **infra** (plena + gates de reversibilidade).
- **O que provoca**: ✅ processo proporcional, sem funil; ⚠️ exige **julgamento** na
  classificação — mitigado pela regra "na dúvida, é plena; infra nunca é leve".

### 5.4 Testes primeiro, cobertura pragmática

- **Por quê**: "pronto" precisa de evidência que uma máquina confira. E meta numérica de
  cobertura é gameável — produz teste inútil.
- **O que faz**: pelo menos **um caso feliz e um de falha** por caso de uso; bug exige um
  teste que o reproduza **antes** do reparo (vermelho → verde).
- **O que provoca**: ✅ verificação autônoma, sem depender de opinião; ⚠️ testes não medem
  se a *jornada* foi servida — daí "verde local ≠ certo global" e o gate humano.

### 5.5 Fitness functions

- **Por quê**: regra de arquitetura que vive só em documento é violada em silêncio.
- **O que faz**: as regras viram **teste executável** na integração contínua (ex.: nosso
  `verificar-agentes.sh` prova que nenhum agente somente-leitura tem permissão de escrita).
- **O que provoca**: ✅ arquitetura que se defende sozinha; ⚠️ falso senso de segurança —
  a função testa o que foi codificado, não o que foi esquecido.

### 5.6 Corte por fronteira (DDD / arquitetura hexagonal)

- **Por quê**: a janela de contexto é finita. Paralelizar por arquivo gera conflito; por
  **contexto delimitado** (bounded context), gera independência.
- **O que faz**: o plano corta o trabalho por fronteira de domínio; cada agente carrega só
  a sua fatia (Princípio V).
- **O que provoca**: ✅ paralelismo seguro e contexto econômico; ⚠️ **cortar bem é difícil**
  — corte ruim aparece como economia de contexto baixa (cap. 04 §6b) ou retrabalho.

### 5.7 Reversibilidade engenheirada

- **Por quê**: a pergunta errada é "quando confio no agente?". A certeza estatística nunca
  chega. A pergunta certa é "**quanto custa desfazer?**".
- **O que faz**: backup, execução a seco (dry-run), reversão documentada; gate proporcional
  à classe de risco. Reversibilidade **rebaixa** a classe de risco.
- **O que provoca**: ✅ velocidade com segurança — erra-se barato, logo corre-se rápido;
  ⚠️ custo de engenharia antecipado (escrever o rollback antes de precisar dele).

### 5.8 ADR imutável e append-only

- **Por quê**: decisão editada perde o valor de prova; o histórico é a memória do projeto.
- **O que faz**: ADR nunca se edita no mérito — decisão nova **supera** a anterior; o índice
  de decisões é somente-anexação.
- **O que provoca**: ✅ auditabilidade real; ⚠️ acúmulo — exige índice e curadoria para não
  virar arquivo morto (foi o que motivou a decisão 11).

### 5.9 Forcing function no changelog

- **Por quê**: "documentar depois" é onde a documentação morre.
- **O que faz**: a integração contínua **falha** se o `CHANGELOG.md` não mudou, com escape
  explícito (etiqueta `skip-changelog`).
- **O que provoca**: ✅ documentação viva por construção; ⚠️ atrito em mudança trivial —
  por isso o escape existe e é **explícito** (quem usa, declara).

### 5.10 YAGNI como poda ativa

- **Por quê**: governança tende a inchar; toda regra nova parece barata isoladamente.
- **O que faz**: só entra o que dói agora; a retrospectiva **poda** o que não paga o custo.
- **O que provoca**: ✅ método que cabe na cabeça; ⚠️ risco de subestimar necessidade real —
  mitigado pelo mecanismo de **gatilho** (decisão adiada com condição escrita de revisão).

### 5.11 Registro consultável por máquina

- **Por quê**: a retrospectiva descobriu que o estado dos gates vivia fora do repositório —
  prosa não é consultável por agente.
- **O que faz**: `decisoes.jsonl` — uma linha de dados por decisão, anexada
  automaticamente pelo script de promoção.
- **O que provoca**: ✅ agente lê "as últimas 5 decisões" sem carregar os ADRs;
  ⚠️ duplicidade aparente (prosa + índice) — resolvida pela regra "o ADR é a fonte, o
  índice é o ponteiro".

### 5.12 Sintaxe EARS

- **Por quê**: critério de aceite em prosa é interpretável; em EARS, é testável.
- **O que faz**: `QUANDO ‹condição› O SISTEMA DEVE ‹comportamento observável›`.
- **O que provoca**: ✅ critério vira teste quase 1:1; ⚠️ não serve para critério
  estrutural ("o arquivo existe") — para esses, usa-se o par (comando, esperado).

### 5.13 Vendorização

- **Por quê**: os templates que os comandos leem eram genéricos do upstream — sem nossas
  raias, sem EARS, sem verificação constitucional.
- **O que faz**: o conteúdo passa a ser **fonte nossa**, adaptado; o upstream entra por
  decisão registrada, nunca por reinstalação automática.
- **O que provoca**: ✅ as decisões empacotadas moram no nosso pacote; ⚠️ **assumimos a
  manutenção** — novidade do upstream exige comparação deliberada.

### 5.14 Iron Laws

- **Por quê**: skill que descreve é racionalizável; skill que **comanda** fecha a brecha.
- **O que faz**: cada skill abre com sua lei inegociável e as desculpas explicitamente
  bloqueadas.
- **O que provoca**: ✅ compliance alto sem supervisão; ⚠️ rigidez — por isso a lei é
  **estreita** (uma regra por skill), e a exceção é decisão humana registrada.

## 6. ⭐ Na prática — o ciclo real

A decisão 11 (registro consultável) não nasceu de teoria: nasceu do **primeiro uso** do
`scripts/retro.sh`, no ciclo 008. Ao rodar, ele revelou que os relatórios de qualidade dos
ciclos 003 a 007 ainda diziam "aguarda aprovação humana" — os gates tinham sido exercidos
na conversa, mas nenhum artefato registrava o fechamento.

O ciclo seguinte transformou o achado em regra executável (ADR 0009): o
`scripts/promover-main.sh` passou a **anexar automaticamente** a decisão do gate antes de
publicar. A primeira promoção depois disso auto-registrou:

```
gate registrado: gate-main-f9f2896
ok: 'main' promovido para 6a293bb.
```

Ciclo completo, em duas etapas: **ferramenta encontrou a falha → falha virou regra →
regra virou automação**. É o Princípio VII (governança que aprende) com evidência datada.

## 7. Erros e anti-padrões

- **Adotar prática por prestígio** — "todo mundo usa DDD". Sem a dor nomeada, a prática
  vira cerimônia (anti-padrão 11).
- **Decisão sem preço escrito** — registrar só o benefício produz método que ninguém
  consegue revogar depois.
- **Regra sem gatilho de revisão** — decisão adiada ("observar") sem condição escrita vira
  ansiedade permanente ou esquecimento.
- **Fitness function como prova de correção** — ela prova o que foi codificado; a jornada
  continua sendo julgamento humano (verde local ≠ certo global).

## 8. Verificação

1. Escolha duas decisões do quadro §4.1 e diga, sem consultar: que problema cada uma
   resolve e **que efeito indesejado** aceitamos junto.
2. A decisão 3 (raias) existe porque a decisão 1 provocou um custo. Explique a cadeia.
3. Uma regra do seu contexto parou de pagar o custo. Que evidência você usaria para
   propor a poda — e onde registraria a revogação?

## 9. O que roubar

- O formato **decisão → porquê → o que faz → o que provoca** para qualquer escolha técnica:
  registrar o efeito indesejado é o que torna a decisão revogável depois.
- **Gatilho escrito** para toda decisão adiada — transforma "observar" em evento, não em
  ansiedade.
- **Reversibilidade antes de confiança**: engenheirar o desfazer compra mais velocidade do
  que esperar certeza sobre o agente.
- **Forcing function com escape explícito**: bloquear na automação, mas deixar uma saída
  que exige declaração — atrito onde importa, sem tirania.

---

**Conexões**: cap. 03 (spec-driven) · cap. 09 (definições de pronto) · cap. 10 (gates) ·
cap. 12 (governança leve) · [registros de decisão](../adr/README.md) ·
[guia editorial](../livro/guia-editorial.md).
