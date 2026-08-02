# 06 — Papéis e responsabilidades: os contrapesos sem o time

> **Capturado em** 2026-08 · última revisão 2026-08-02 · ciclo 026 (migrado ao padrão v2)
>
> **Delega-se tudo, menos o A.** E o humano responde pela **política, pelos gates e pelos
> critérios** — não por conferir cada item, senão vira gargalo.

## 1. Objetivos

Ao fim deste capítulo você será capaz de:

1. **Explicar** por que "decide ≠ executa ≠ verifica" é contrapeso estrutural, e não
   formalidade de organograma;
2. **Aplicar** RACI (*Responsible, Accountable, Consulted, Informed* — executa, responde,
   é consultado, é informado) a uma matriz de um humano com N agentes;
3. **Distinguir** ser responsável **pela política** de ser responsável **por cada
   instância** — e reconhecer a armadilha do funil;
4. **Avaliar** se um papel prescrito existe de fato ou é só texto no documento.

## 2. O problema

Num time, decidir, executar e verificar são pessoas diferentes — e é essa separação que
cria o contrapeso. Quem escreveu não aprova; quem aprova não confere sozinho.

Você é **uma** pessoa com N agentes. Os três papéis colapsam naturalmente na mesma cabeça e
o contrapeso some sem que ninguém decida acabar com ele. Pior: some em silêncio, com a
sensação de estar indo mais rápido — porque de fato está, até o primeiro erro caro.

## 3. A ideia central

> **Papel é modo de trabalho, não cargo.** O que não se delega é o **A** — responder pelas
> consequências. Todo o resto vai para agentes, desde que quem verifica nunca seja quem
> executou.

## 4. A regra vigente

1. **Exatamente um responsável final (A) por tarefa**, e ele é **humano, sempre**.
2. **R (executa) → agente**: spec, plano, código, testes, documentação.
3. **C (verifica) → agente independente, em contexto fresco** — nunca o mesmo que executou.
4. **I (informado) → registro**: changelog, índice de decisões, trilha de execução.
5. **O humano é A pela política, pelos gates e pelos critérios**, não por item: desenha os
   trilhos (`permitir/negar/perguntar`, Definição de Pronto verificável, critérios da spec)
   e faz amostragem.
6. **Indelegáveis**: aprovar spec, aprovar plano, aprovar merge, autorizar deploy ou
   migração.
7. **Papel prescrito sem executável não conta** — se o modelo cita um papel, tem de existir
   um agente que o entregue.

## 5. Fundamentos

### 5.1 RACI adaptado a humano × agentes

RACI dá o vocabulário mínimo para separar quem faz de quem responde. A adaptação que
importa é uma só: **o A não migra**. Um agente raciocina, executa e revisa — e não tem o
que perder se errar. Responsabilidade sem consequência não é responsabilidade.

### 5.2 A armadilha do funil

Se o humano é A **e** confere à mão cada saída de agente, ele recriou "fazer tudo sozinho",
agora com uma etapa extra de leitura. O ganho da Inteligência Artificial (IA) evapora e o
humano vira o gargalo do próprio sistema.

A saída não é confiar mais: é **mudar o objeto da responsabilidade**. Ser A pela política
significa decidir uma vez por *classe* de ação e responder por essa decisão. Ser A por item
significa decidir N vezes e não responder direito por nenhuma.

### 5.3 Independência é estrutura, não promessa

"O revisor deve ser imparcial" é intenção. Tirar do revisor a capacidade de editar é
estrutura. A independência do C se sustenta em duas coisas verificáveis: **contexto fresco**
(ele não viveu os becos sem saída de quem escreveu) e **ferramentas restritas** (ele não
consegue consertar, só apontar).

### 5.4 Abordagens avaliadas

| Abordagem | O que oferece | Veredito |
|---|---|---|
| **Matriz RACI/RASCI** | quem executa, responde, é consultado e informado, por tarefa | **Adotado** — adaptado a humano × agentes |
| **Regra "um Accountable"** | responsabilidade não se dilui | **Adotado** — o humano é o A único |
| **Papéis Scrum** (Product Owner, Scrum Master, time) | papéis de time cross-funcional | **Parcial** — o Product Owner vira Steward; o resto é cerimônia de papel para quem opera sozinho |
| **Time T-shaped** | largura de habilidades com profundidade | **Reinterpretado** — o agente cobre a largura; o humano guarda a profundidade da decisão |
| **"Aprovo tudo" / "aprovo nada"** | simplicidade | **Rejeitado** — o primeiro vira funil; o segundo descobre o erro quando já é irreversível |

## 6. ⭐ Na prática — o ciclo real

**O C independente é uma linha de configuração.** Dos treze subagentes, três não têm
permissão de escrever — e são exatamente os que julgam:

```
$ for f in .claude/agents/*.md; do grep -q "^tools:.*\(Write\|Edit\)" "$f" || basename "$f"; done
guardiao-processo.md
review.md
security.md
```

Não é recomendação de conduta: o `review` **não consegue** corrigir o que aponta. E isso é
cobrado por fitness function — `scripts/verificar-agentes.sh` falha se um agente
somente-leitura ganhar `Write` ou `Edit`.

**O A humano deixa rastro.** Cada promoção para a linha principal exige o "sim" do Steward,
e o script registra o gate sozinho no índice de decisões:

```
$ grep -c '"id": "gate-main' docs/registro/decisoes.jsonl
21
```

Vinte e uma decisões de merge com nome e data, dentro de 38 decisões registradas ao todo. O
A não é declaração de organograma — é uma linha por decisão, num arquivo que só cresce.

**E o teste mais duro: papel prescrito × papel existente.** No ciclo 018 descobrimos que o
modelo operacional prescrevia o papel de interface **havia catorze ciclos** sem nenhum
agente que o entregasse. A resposta não foi criar o agente e seguir em frente: foi criar o
agente **e a verificação** que impede a lacuna de voltar:

```
$ scripts/verificar-papeis.sh
  ok: Spec-agent → spec-agent.md
  ok: UX-agent → ux-semantica.md
  ...
✓ todo papel prescrito tem executável; todo artefato essencial tem template.
```

Papel que só existe no documento é papel que ninguém exerce — e o documento continua
parecendo correto, que é o pior dos dois mundos.

## 7. Erros e anti-padrões

- **Delegar o A** — delega-se executar, consultar e informar; responder, nunca.
- **Autor revisando o próprio trabalho** (anti-padrão 6) — o viés é estrutural; contexto
  fresco e ferramentas restritas resolvem, boa vontade não.
- **Ser A por item** — o funil: o humano vira revisor de esteira e o sistema para de
  escalar.
- **Papel de enfeite** — cargo no documento, sem agente, sem ferramenta e sem saída
  definida.
- **Cerimônia de papel** (anti-padrão 11) — importar papéis de time grande para quem opera
  sozinho.

## 8. Verificação

1. Um agente revisa o código que ele mesmo escreveu e aponta três problemas reais. Por que
   isso ainda **não** é revisão independente?
2. Você aprova 40 saídas de agente por dia e sente que está no controle. Diga por que isso
   é o funil — e o que muda quando você passa a ser A pela política.
3. O modelo operacional cita um papel de segurança. Que comando você roda para saber se
   esse papel **existe** de verdade?

## 9. O que roubar

- **Escreva quem é o A antes de começar** — um por tarefa, humano, nomeado.
- **Implemente independência tirando ferramenta**, não pedindo isenção.
- **Suba o nível da sua responsabilidade**: política, gates e critérios em vez de itens.
- **Cheque se cada papel do seu documento tem executável.** Se não tiver, ou crie o
  executável, ou tire o papel do documento — as duas coisas são honestas; deixar como está,
  não.

---

**Conexões**: [01 — o princípio central](01-principio-central.md) (accountability
indelegável e política de delegação) · [04 — contexto](04-fluxo-agentic-contexto.md) (o
revisor fresco implementa o C) · [05 — orquestração](05-orquestracao.md) (quem faz o
*reduce*) · [09 — DoR/DoD](09-definition-of-ready-done.md) (critério verificável é o que
permite delegar o C) · [10 — gates e risco](10-gates-classes-de-risco.md) ·
[Diário da jornada](../research/jornada-aprendizado-modelo-operacional.md) `[5]`.

**Fontes**: Anthropic, *Building effective agents* —
https://www.anthropic.com/engineering/building-effective-agents ·
Matriz RACI (prática consolidada de atribuição de responsabilidades) ·
[Modelo operacional](../governance/modelo-operacional.md) §4 (papéis e RACI) ·
[Perfis dos agentes](../agents/perfis.md).
