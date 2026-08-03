# 09 — Pronto para começar e Pronto de verdade

> **Capturado em** 2026-08 · última revisão 2026-08-02 · ciclo 029 (migrado ao padrão v2)
>
> **A Definição de Pronto (DoD) *é* o gate.** Um gate barato é o que se verifica sozinho —
> e mesmo verde, ele não garante que era a coisa certa.

## 1. Objetivos

Ao fim deste capítulo você será capaz de:

1. **Escrever** critério de aceite verificável autonomamente, com o comando que o prova;
2. **Converter** julgamento subjetivo ("código limpo", "boa experiência") em check;
3. **Explicar** o que a DoD verde **não** garante — e quem assume esse resto;
4. **Aplicar** a segunda lei: provar o check falhando antes de confiar nele.

## 2. O problema

Baratear o gate é a única forma de escapar do gargalo humano (capítulo 07). Mas gate barato
exige critério que uma máquina consiga julgar — e quase todo critério que escrevemos
naturalmente é subjetivo.

"Código limpo", "bem testado", "documentação adequada": cada um entende uma coisa, ninguém
consegue provar, e a discussão vai para o gate humano, que era justamente o recurso escasso.
Pior: a sensação de rigor é alta, porque a lista parece exigente.

## 3. A ideia central

> **Critério sem comando não é critério — é desejo.** E check que você nunca viu acusar não
> é check: é esperança.

## 4. A regra vigente

1. **Todo critério de aceite vem com o comando que o prova.** Não dá para automatizar?
   Marque explicitamente como gate humano — vago não fica.
2. **Prove o check falhando** antes de confiar nele: quebre o mundo de propósito e veja o
   vermelho.
3. **Pronto para começar (DoR)** é a mesma ideia a montante: a spec e o plano estão
   completos o bastante para o agente executar **sem adivinhar**.
4. **DoD reduzida na raia leve**; **bloco de reversibilidade obrigatório** na raia de
   infraestrutura.
5. **Puxe o global para dentro da DoD**: jornada atualizada, teste ponta a ponta,
   rastreabilidade — senão o verde é só local.
6. **O humano guarda o irredutível**: se era a coisa certa, e se o conjunto maior continua
   de pé.

## 5. Fundamentos

### 5.1 A propriedade que torna o gate barato

Verificável **autonomamente**: o agente produz a evidência e um script confere, sem
depender de você estar na sala. É o "prove, não declare" do capítulo 01 virado máquina.

### 5.2 Converter julgamento em check

| Julgamento | Vira |
|---|---|
| "código limpo" | análise estática, limite de complexidade, fitness function de dependência |
| "boa experiência de uso" | captura gerada do build real + heurística datada com severidade |
| "seguro" | varredura de segredos, revisão de injeção e autorização |
| "documentado" | gate no pull request: entrada no changelog, jornada regenerada |

O que não converte fica explicitamente humano — e isso é uma resposta honesta, não uma
falha.

### 5.3 Verde é necessário, não suficiente

Uma DoD verde garante a **peça local**. Ela não garante duas coisas:

- **coerência global** — a jornada inteira ainda funciona; é o ótimo local reaparecendo no
  nível da qualidade;
- **a coisa certa** — nenhum teste conserta requisito errado.

A primeira se ataca puxando o global para dentro da DoD. A segunda fica com o humano
responsável, sempre.

### 5.4 Abordagens avaliadas

| Abordagem | O que oferece | Veredito |
|---|---|---|
| **DoR / DoD** (Scrum, Kanban) | portões de entrada e saída | **Adotado** — como checklists verificáveis |
| **Ênfase em integração** × **pirâmide de testes** | onde investir teste | **Mais integração** — rota e contrato pegam o "todo" melhor que só unidade |
| **Teste antes (TDD)** | vermelho antes do verde | **Adotado** — bug exige teste que reproduz |
| **Portões automáticos na integração contínua** | bloqueio sem humano | **Adotado** — fitness functions, análise estática, varredura de segredos |
| **Cobertura como meta numérica** | percentual de linhas | **Rejeitado** — gameável; usamos "caminho feliz + falha por caso de uso" |

## 6. ⭐ Na prática — o ciclo real

A DoD deste método não vive num documento: vive em **seis portões executáveis**. Quatro
scripts dedicados —

```
$ ls scripts/verificar-*.sh
check-agents.sh  check-chapters.sh  check-install.sh  check-roles.sh
```

— mais dois dentro do gerador do livro (`process.exit(1)` para colisão de endereço e para
link ou imagem quebrada) e onze testes automatizados no companion.

**A segunda lei em ação, com data.** O `check-install.sh` nasceu no ciclo 021 e a
primeira execução foi vermelha, acusando deriva de três ciclos. O `check-chapters.sh`
(ciclo 022) foi provado falhando em **quatro** modos — e o quarto só apareceu porque
insistimos: ao quebrar a datação, o capítulo **saía do check** em silêncio, porque o
detector procurava uma frase em vez da estrutura. Um check que passa quando o mundo está
quebrado é pior que nenhum: ele dá licença.

**O que a lei impede está escrito na própria skill**, com as desculpas fechadas por
antecipação:

> **Violar a letra desta regra é violar o espírito dela.** Isso NÃO é desculpa: "é difícil
> de automatizar" — então marque explicitamente como gate humano; vago não fica. "Todo
> mundo entende o que significa" — se não há comando, cada um entende uma coisa.

**E o limite do verde, medido.** O capítulo 02 mostrou que nove defeitos escaparam para a
linha principal em dezessete promoções, todos com a verificação verde no momento do merge.
Nenhum foi pego por revisão; todos foram pegos quando alguém **escreveu o check que
faltava**. É a demonstração empírica de que verde é necessário e não suficiente — e de que
a resposta certa ao escape não é revisar com mais cuidado, é ampliar a família coberta pelo
portão (anti-padrão 16).

## 7. Erros e anti-padrões

- **Critério não verificável** — "deve ser rápido", "deve ser intuitivo".
- **Check nunca visto falhar** (segunda lei) — esperança com nome de verificação.
- **Check que mede o proxy** (anti-padrão 13) — a frase em vez do fato.
- **Meta numérica gameável** (anti-padrão 9) — cobertura vira alvo e para de medir.
- **Confiar no verde local** — a peça passa, a jornada quebrou.
- **Esconder o gate humano** — dizer que é automático o que na verdade depende de alguém
  olhar.

## 8. Verificação

1. Converta em critério verificável: *"a documentação precisa estar adequada"*. Qual comando
   prova, e o que ele deve acusar quando o mundo estiver quebrado?
2. Um check novo passou de primeira. Por que isso é motivo de desconfiança, e o que você faz
   antes de confiar nele?
3. Nove defeitos escaparam com o gate verde. Explique por que "revisar melhor" é a resposta
   errada — e qual é a certa.

## 9. O que roubar

- **Escreva o comando junto com o critério.** Se não houver comando, ou vire gate humano
  explícito, ou o critério não entra.
- **Quebre o mundo de propósito** antes de confiar num check novo.
- **Puxe o global para dentro do gate** — jornada, ponta a ponta, rastreabilidade.
- **Guarde para o humano o que é irredutível**: se era a coisa certa. Isso não automatiza, e
  fingir que sim é o pior dos erros.

---

**Conexões**: [01 — o princípio central](01-principio-central.md) ("prove, não declare") ·
[02 — a evidência](02-dora-space.md) (os nove defeitos escapados) ·
[07 — cerimônias](07-cerimonias-cadencia.md) (gate barato é como se escala) ·
[10 — gates e classes de risco](10-gates-classes-de-risco.md) (onde o humano tem de agir) ·
[Receita — escrever critério verificável](../receitas/escrever-criterio-verificavel.md) ·
[Diário da jornada](../research/jornada-aprendizado-modelo-operacional.md) `[8]`.

**Fontes**: Claude Code, *Best practices* — https://code.claude.com/docs/en/best-practices ·
DORA, *four keys* — https://dora.dev/guides/dora-metrics-four-keys/ ·
K. C. Dodds, *The Testing Trophy* ·
[Modelo operacional](../governance/operating-model.md) §7 ·
[Skill `verifiable-dod`](https://github.com/GHDaru/maestro/blob/main/skills/verifiable-dod/SKILL.md).
