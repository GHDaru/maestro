# 04 — Fluxo agentic e economia de contexto

> **Capturado em** 2026-08 · última revisão 2026-08-03 · ciclo 024 (migrado ao padrão v2)
>
> **O inimigo não é a falta de contexto — é o acúmulo.** Quatro práticas que parecem
> soltas contornam a mesma restrição física: a janela é finita e degrada enquanto enche.

## 1. Objetivos

Ao fim deste capítulo você será capaz de:

1. **Explicar** por que explorar→planejar→codar, subagentes, `/clear` e revisor fresco são
   a **mesma** ideia, e não quatro boas práticas independentes;
2. **Distinguir** contexto *que sustenta* (objetivo, invariantes, contratos) de ruído — e
   descartar só o segundo;
3. **Aplicar** a fronteira certa ao fatiar trabalho entre agentes, sem cair no ótimo local;
4. **Avaliar** quando resetar contexto é higiene e quando é amnésia.

## 2. O problema

A janela de contexto de um agente é finita, e o desempenho **degrada à medida que ela
enche**: instruções antigas somem, o agente repete o que já tentou e erra mais. A intuição
manda alimentar mais — "cole o repositório inteiro, assim ele entende". É o contrário:
cada beco sem saída, cada arquivo irrelevante, cada tentativa abandonada continua ocupando
lugar e **afogando o sinal**.

O sintoma clássico aparece na terceira hora de sessão: o agente que começou preciso passa
a inventar, a esquecer a regra dada no começo, a "consertar" o que já estava certo. Não
ficou pior — ficou cheio.

## 3. A ideia central

> **Contexto é orçamento, não depósito.** Cada prática do fluxo agentic é uma forma de
> gastar esse orçamento com o que sustenta a decisão e jogar fora o resto.

## 4. A regra vigente

1. **Planejar comprime.** Na raia plena, a exploração vira plano antes de virar código — o
   plano é a exploração destilada no que importa.
2. **Subagente lê em janela separada** e devolve só o resultado. O principal fica magro.
3. **Agente estreito** (Princípio V): cada um com escopo, ferramentas e saída definidos.
   Quem só julga **não recebe permissão de escrever**.
4. **Revisão em contexto fresco é item de Definição de Pronto (DoD)**, em todas as raias —
   quem revisa não pode carregar os becos sem saída de quem escreveu.
5. **Preserve o que sustenta, descarte o ruído.** O contexto integrador é a spec.
6. **Economia medida, não afirmada**: ao fatiar contexto grande, estime o quanto se poupou;
   economia consistentemente baixa é sinal de **corte errado**, não de contexto pequeno.

## 5. Fundamentos

### 5.1 Uma restrição, quatro respostas

| Prática | O que faz com o orçamento |
|---|---|
| explorar → **planejar** → codar | comprime a exploração no essencial antes de gastar janela com código |
| **subagentes** | leem em janela própria; ao principal volta o resumo |
| **`/clear`** | descarta ruído entre tarefas não relacionadas |
| **revisor fresco** | começa com orçamento inteiro e vê só diff + critério |

### 5.2 O limite: reset demais é amnésia

Resetar tudo esquece o básico; delegar tudo produz **ótimo local** — o subagente otimiza a
fatia e quebra o todo. A disciplina madura não é "menos contexto", é **contexto certo**:
objetivo, invariantes e contratos ficam; caminhos abandonados vão embora.

### 5.3 Por que a fronteira importa mais que o tamanho

Fatiar por quantidade ("metade dos arquivos para cada agente") produz duas fatias que não
se encaixam. Fatiar por **fronteira** — um contexto delimitado, um contrato, uma camada —
produz fatias que se encaixam por construção. Quando a economia de contexto sai baixa, é
quase sempre porque o corte atravessou uma costura em vez de segui-la.

### 5.4 Práticas avaliadas

| Prática | O que oferece | Veredito |
|---|---|---|
| **explorar-planejar-codar-commitar** (Claude Code) | separa pesquisa de execução | **Adotado** (raia plena) |
| **Escritor/Revisor em contexto fresco** | revisor sem viés de quem escreveu | **Adotado** — é a revisão independente da DoD |
| **Subagentes** | investigação e verificação em janela isolada | **Adotado** — cortados por fronteira |
| **Revisão adversarial do diff** | modelo fresco tenta refutar o "pronto" | **Adotado** — gate antes do merge |
| **`/clear` e compactação** | descarte de ruído entre tarefas | **Adotado** — higiene de contexto |
| **Um agente generalista gigante** | simplicidade aparente | **Rejeitado** — janela cheia degrada; prompt cresce sem limite |

## 6. ⭐ Na prática — o ciclo real

O princípio virou **formato de arquivo**. Os treze subagentes do Maestro somam 267 linhas
no total — média de vinte por agente, o menor com dezessete:

```
$ wc -l .claude/agents/*.md | tail -1
  267 total
$ ls .claude/agents/*.md | wc -l
13
```

Vinte linhas não é minimalismo estético: é o tamanho de um papel que cabe inteiro na
cabeça de quem executa, sem gastar janela com o que ele não vai usar.

A separação de papéis aparece na **declaração de ferramentas**, não numa recomendação de
comportamento. Quem julga não pode consertar:

```
$ grep -H "^tools:" .claude/agents/review.md .claude/agents/dev-implementer.md
.claude/agents/review.md:tools: Read, Grep, Glob, Bash
.claude/agents/dev-implementer.md:tools: Read, Write, Edit, Bash
```

O `review` não tem `Write` nem `Edit` — e isso é **verificado**, não confiado:
`scripts/check-agents.sh` falha se um agente somente-leitura ganhar permissão de
escrita. Foi essa fitness function que acusou, no ciclo 019, a diferença entre 12 e 13
agentes quando um papel novo entrou.

O contrato de cada agente também é explícito sobre o que **não** fazer, exatamente para não
inflar contexto com julgamento supérfluo — do arquivo do `review`:

> Aponte **apenas lacunas de correção ou requisito** — não preferências de estilo (um
> revisor que caça tudo induz over-engineering).

E a honestidade sobre o limite: nem todos os treze papéis são acionados em todo ciclo. Uma
varredura nos registros dos 23 ciclos mostra `qa` citado em quinze arquivos, `dev` e
`review` em seis, `tech-writer` e `agent-designer` em três. O toolkit oferece treze
janelas separadas; o trabalho real usa as que a raia pede — o que é a regra funcionando,
não o inventário sendo desperdiçado.

## 7. Erros e anti-padrões

- **Despejo de contexto** (anti-padrão 1) — colar o repositório inteiro. Fatie pela
  fronteira, não pela quantidade.
- **Reset preguiçoso** (anti-padrão 3) — `/clear` como reflexo: perde o que sustenta junto
  com o ruído.
- **Multi-agente para problema de agente único** (anti-padrão 4) — orquestração custa
  handoff; só compensa quando há fronteira de verdade.
- **Autor revisando o próprio trabalho** (anti-padrão 6) — contexto contaminado; o viés é
  estrutural, não moral.
- **Ótimo local** — cada fatia perfeita, o conjunto quebrado. É o preço de cortar na
  costura errada.

## 8. Verificação

1. Um agente começa preciso e, uma hora depois, passa a repetir tentativas já descartadas.
   O que aconteceu com o orçamento — e qual das quatro práticas ataca esse caso?
2. Por que dar `Write` ao agente de revisão quebra a independência mesmo que ele "só use
   quando for óbvio"? Responda em termos de estrutura, não de confiança.
3. Você fatiou uma tarefa em quatro e a economia de contexto ficou em 10%. O que isso
   sugere sobre o corte — e o que você faz antes de tentar de novo?

## 9. O que roubar

- **Trate contexto como orçamento**: toda prática de fluxo agentic é decisão de gasto.
- **Escreva papéis curtos** — se o prompt do agente não cabe numa tela, o papel está
  fazendo coisa demais.
- **Tire a ferramenta, não peça bom comportamento**: quem não deve escrever não recebe
  permissão de escrever. E verifique isso por script.
- **Meça a economia ao fatiar.** Economia baixa é diagnóstico de fronteira errada — o
  remédio é replanejar o corte, não aumentar a janela.

---

**Conexões**: [03 — Spec-Driven](03-spec-driven.md) (a spec é o contexto que sobrevive ao
reset) · [05 — orquestração](05-orquestracao.md) (o ótimo local e o *reduce* cognitivo) ·
[06 — papéis e RACI](06-papeis-raci.md) (o revisor independente é um papel, não um favor) ·
[09 — DoR/DoD](09-definition-of-ready-done.md) (revisão fresca é item obrigatório) ·
[Diário da jornada](../research/jornada-aprendizado-modelo-operacional.md) `[3]`.

**Fontes**: Claude Code, *Best practices* —
https://code.claude.com/docs/en/best-practices ·
Anthropic, *Building effective agents* —
https://www.anthropic.com/engineering/building-effective-agents ·
[Apêndice A](apendice-a-maestro-02.md) (context-slicer: economia medida) ·
[Princípios do Maestro](../governance/principles.md) (V — economia de contexto).
