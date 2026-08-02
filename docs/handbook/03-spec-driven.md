# 03 — Desenvolvimento dirigido por especificação

> **Capturado em** 2026-08 · última revisão 2026-08-02 · ciclo 023 (migrado ao padrão v2)
>
> **A especificação é a fonte de verdade — não o código, não o prompt.** O que muda não é
> escrever mais documento: é inverter quem depende de quem.

## 1. Objetivos

Ao fim deste capítulo você será capaz de:

1. **Explicar** por que a documentação tradicional apodrece e por que a spec dirigida
   por especificação não apodrece — pela inversão de dependência, não por disciplina;
2. **Escrever** um requisito em EARS (*Easy Approach to Requirements Syntax*, sintaxe
   simples para requisitos) que uma máquina consiga verificar;
3. **Decidir** a raia de uma mudança por `ambiguidade × raio × irreversibilidade`;
4. **Avaliar** quando escrever spec é desperdício — e o que fazer nesse caso.

## 2. O problema

No fluxo tradicional a fonte de verdade é o código, e o documento *descreve* o código.
Ele está a jusante: quando o código muda, o documento fica errado e ninguém percebe. Todo
projeto conhece o resultado — a pasta de documentação que ninguém abre porque ninguém
confia.

Com agentes de Inteligência Artificial (IA), o problema muda de escala. Um prompt vago não
gera uma dúvida: gera **código**. O agente preenche o silêncio adivinhando milhares de
requisitos que você nunca disse, e o resultado compila, passa no teste e erra a intenção —
o modo de falha mais caro que existe, porque parece sucesso.

## 3. A ideia central

> **Inverta a dependência: a spec deixa de descrever o código e passa a gerá-lo.** Quem
> quer código novo muda a spec primeiro — a obsolescência para de ser opcional e passa a
> quebrar a geração.

## 4. A regra vigente

1. **A intenção mora na spec**, não no código nem no prompt. Fluxo:
   `specify → clarify → plan → tasks → implement`.
2. **A spec diz o quê e por quê**; o plano diz **como**. Misturar os dois é o começo do
   amontoado.
3. **Critério de aceite em EARS**: `QUANDO ‹condição› O SISTEMA DEVE ‹comportamento
   observável›`. Se não dá para observar, não é critério — é desejo.
4. **Nem toda mudança merece spec.** O valor escala com
   `ambiguidade × raio de impacto × irreversibilidade`. Baixos os três, spec é cerimônia.
5. **Três raias** (modelo operacional §3): *leve* (o pull request é o artefato; bug exige
   teste que reproduz) · *plena* (o fluxo inteiro) · *infra* (plena + reversibilidade).
6. **Desempate**: na dúvida, plena. Infraestrutura e migração **nunca** são leves.

## 5. Fundamentos

### 5.1 Inversão de dependência aplicada a documento

É o mesmo movimento da inversão de dependência em arquitetura: o que estava a jusante
passa a estar a montante. Documento a jusante apodrece porque errar não custa nada;
documento a montante não apodrece porque errar **quebra a geração**. Não é uma questão de
gente mais disciplinada — é de posição no fluxo.

### 5.2 EARS: a frase que a máquina consegue conferir

EARS existe para tirar a ambiguidade da frase de requisito sem virar linguagem formal. O
padrão que adotamos:

```
QUANDO uma skill existe em skills/ e não é citada na instrução,
O SISTEMA DEVE falhar — skill invisível é skill que não existe.
```

Repare no que a frase entrega: uma **condição observável** e um **comportamento
observável**. Dela sai um teste quase sozinho. Compare com "o sistema deve ter boa
cobertura de skills" — que não se prova nem se refuta.

### 5.3 A raia: quanto processo esta mudança merece

Spec para tudo é burocracia; spec para nada é adivinhação. A raia resolve com três
perguntas: *quão ambíguo é o que se quer? · quanto do sistema isso alcança? · dá para
desfazer?* Corrigir um typo tem os três baixos — o pull request basta. Migrar um banco
tem irreversibilidade alta — nem que a mudança seja de uma linha.

### 5.4 Ferramentas avaliadas

| Ferramenta | Modelo | Veredito |
|---|---|---|
| **GitHub Spec Kit** | uma spec por feature; fases com gate | **Adotado** — base do fluxo; casa com constituição e ciclos numerados |
| **OpenSpec** (Fission-AI) | *delta* (propor → aplicar → arquivar), leve | **Descartado como segunda ferramenta** — a ideia do delta foi absorvida como raia leve (ADR 0005) |
| **Kiro, Tessl, "specs as source of truth"** | variações de desenvolvimento dirigido por spec assistido | **Observados** — mesmo princípio, sem adoção (ADR 0008) |
| **Superpowers** (GHDaru) | disciplina de leis mandatórias | **Absorvido em parte** — EARS e o rigor das Iron Laws (ADR 0008) |
| **Prompt ad-hoc** | sem spec | **Rejeitado** — produz código que compila e erra a intenção |

## 6. ⭐ Na prática — o ciclo real

Vinte e dois ciclos escritos assim; **quatorze** já com requisitos em EARS (o padrão entrou
no ciclo 008, depois da avaliação do ecossistema registrada no ADR 0008):

```
$ grep -l "O SISTEMA DEVE" specs/*/spec.md | wc -l
14
```

O trecho abaixo mostra o caminho inteiro de **uma frase** — da spec ao executável, no ciclo
021. Primeiro o requisito, escrito antes de existir código:

> **FR3**: QUANDO uma skill existe em `skills/` e não é citada na instrução, O SISTEMA DEVE
> falhar — skill invisível é skill que não existe.

Depois o executável que nasceu dele, em `scripts/verificar-instalacao.sh` — a condição da
frase virou laço, o comportamento virou saída e código de saída:

```bash
for d in skills/*/; do
  nome="$(basename "$d")"
  ... grep -q "$nome" "$f" && citada=1
  [[ "$citada" -eq 1 ]] || alerta "skill '$nome' existe mas não é citada em CLAUDE.md/AGENTS.md"
done
```

E, no mesmo ciclo, a primeira execução — o check nasceu **vermelho**, apontando uma deriva
de três ciclos que ninguém tinha visto:

```
✗ skill 'jornada-viva' existe mas não é citada em CLAUDE.md/AGENTS.md
✗ 2 problema(s): o método está no disco, mas não está instalado de fato.
```

Este é o teste do capítulo: se a frase da spec não vira comando, ela não era um requisito —
era uma intenção bem-escrita. E repare no efeito da inversão: para mudar o comportamento
do check, alguém precisa **mudar a spec**; o documento não tem como ficar para trás.

O outro lado da regra é onde somos mais duros com nós mesmos. Das 22 specs, **19 estão
marcadas como plena e só 2 como leve** — e isso provavelmente diz mais sobre o hábito de
quem escreve do que sobre o risco do que foi feito. A raia existe para graduar processo;
quando quase tudo cai na mais pesada, ou o trabalho é mesmo todo ambíguo e de raio largo,
ou a régua não está sendo aplicada. Fica aqui como o que é: um dado desconfortável do
próprio repositório, à espera da retrospectiva.

## 7. Erros e anti-padrões

- **Spec que descreve solução** — "criar tabela X com colunas Y". Isso é plano. A spec diz
  o problema e o que se observa quando ele está resolvido.
- **Critério não verificável** — "deve ser rápido", "deve ser intuitivo". Sem número, sem
  comando, sem observável, não entra (skill `dod-verificavel`).
- **Spec escrita depois** para satisfazer o processo — documento a jusante de novo, com
  custo de cerimônia e zero benefício.
- **Raia plena para tudo** — cerimônia de papel (anti-padrão 11): processo que não muda
  decisão nenhuma.
- **Raia leve por conveniência** — "é rapidinho" não é análise de risco. Infra nunca é leve.

## 8. Verificação

1. Reescreva em EARS: *"o site precisa ter bons links"*. Qual condição e qual
   comportamento observável você escolheu — e como um comando confere isso?
2. Uma mudança de uma linha altera o script que promove para a linha principal. Aplique
   `ambiguidade × raio × irreversibilidade` e diga a raia, justificando cada fator.
3. Por que a spec dirigida por especificação não apodrece? Responda **sem** usar a palavra
   "disciplina".

## 9. O que roubar

- **Escreva o critério antes do código, em forma de frase conferível** — é o que separa
  requisito de desejo.
- **Gradue o processo pelo risco, não pelo tamanho**: três raias resolvem o falso dilema
  entre burocracia e improviso.
- **Faça a spec ser input de alguma coisa** (geração, check, revisão). Documento que não
  alimenta nada volta a apodrecer, por melhor que seja o time.
- **Na dúvida, plena** — e infraestrutura nunca leve. Regra de desempate barata evita
  discussão cara.

---

**Conexões**: [01 — o princípio central](01-principio-central.md) (a intenção é do humano) ·
[04 — contexto e fluxo agentic](04-fluxo-agentic-contexto.md) (a spec é o contexto que
sobrevive ao `/clear`) · [09 — Definition of Ready / Done](09-definition-of-ready-done.md)
("spec pronta" é a Definição de Pronto para começar) ·
[10 — gates e classes de risco](10-gates-classes-de-risco.md) (a raia decide o gate) ·
[Diário da jornada](../research/jornada-aprendizado-modelo-operacional.md) `[2]`.

**Fontes**: GitHub, *Spec-driven development with AI* (2025-09) —
https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/ ·
GitHub Spec Kit — https://github.com/github/spec-kit ·
OpenSpec (Fission-AI) — https://github.com/Fission-AI/OpenSpec ·
*Spec Kit vs OpenSpec* — https://intent-driven.dev/knowledge/spec-kit-vs-openspec/ ·
[ADR 0005](../adr/0005-raias-de-trabalho-e-specs-de-infra.md) (raias) ·
[ADR 0008](../adr/0008-avaliacao-ecossistema-sdd.md) (ferramenta única; EARS absorvido).
