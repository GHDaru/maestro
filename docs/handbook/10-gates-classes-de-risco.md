# 10 — Gates humanos e classes de risco

> **Capturado em** 2026-08 · última revisão 2026-08-03 · ciclo 030 (migrado ao padrão v2)
>
> **Gate uniforme está sempre errado**: pesado em tudo vira funil, leve em tudo deixa o
> irreversível escapar. O peso escala com **irreversibilidade × impacto**.

## 1. Objetivos

Ao fim deste capítulo você será capaz de:

1. **Explicar** os dois fracassos simétricos do gate uniforme;
2. **Classificar** uma ação na taxonomia de risco e dizer que gate ela merece;
3. **Aplicar** a alavanca da reversibilidade para **rebaixar** a classe de uma ação;
4. **Distinguir** o eixo que decide **processo** (raia) do eixo que decide **gate**.

## 2. O problema

Você barateou os gates mecânicos e guardou o humano para o que é irredutível. Falta decidir
**quando** ele age — e a resposta ingênua é "sempre", que reproduz o gargalo que se queria
evitar.

Aprovar a correção de um erro de digitação e aprovar uma migração destrutiva com o mesmo
rito produz um dos dois desastres: ou o humano aprova tanta coisa que passa a carimbar sem
ler, ou o rito é afrouxado para todos e a ação irreversível escorre junto com o trivial.

## 3. A ideia central

> **Gate proporcional ao risco.** Automatize o baixo, escale o alto, bloqueie o
> catastrófico — e prefira **rebaixar a classe** da ação a acrescentar mais uma aprovação.

## 4. A regra vigente

1. **Gate proporcional pela taxonomia** (constituição, princípio III; modelo operacional §8).
2. **Indelegáveis, sempre humanos**: aprovar spec, aprovar plano, aprovar merge, autorizar
   implantação ou migração.
3. **Autorização fora do modelo**: quem decide permissão é a política, não a Inteligência
   Artificial (IA) — dado que chega de fora é hostil por padrão.
4. **Reversibilidade rebaixa a classe**: cópia de segurança, execução a seco, ambiente de
   homologação e exclusão lógica movem a ação para baixo na escada — e o gate fica mais leve.
5. **Ação em lote, entre inquilinos ou administrativa fica bloqueada** para agente: exige
   fluxo humano formal.
6. **Fases com gate valem em qualquer granularidade** — do ciclo à tarefa de minutos.

## 5. Fundamentos

### 5.1 Os dois fracassos simétricos

**Pesado em tudo** → o humano vira funil e, pior, carimbo: quem aprova duzentos itens por
dia não aprova nenhum de verdade. **Leve em tudo** → a ação irreversível passa sem que
ninguém tenha olhado, e o relatório perfeito não traz o dado de volta.

### 5.2 A taxonomia

| Classe | Exemplo | Agente sozinho? | Gate |
|---|---|---|---|
| Leitura | explorar, buscar | ✅ | nenhum |
| Leitura sensível | dados pessoais, segredos | ⚠️ política e máscara | revisão |
| Criação reversível | feature numa branch | ✅ | no merge |
| **Alteração** | refatoração ampla, contrato | ❌ | aprovação com resumo |
| **Exclusão ou efeito externo** | apagar dados, publicar, chamar terceiro | ❌ | confirmação forte |
| **Financeira ou irreversível** | implantar, migração destrutiva | ❌ | dupla aprovação |
| **Lote, entre inquilinos, administrativa** | migração em massa | ❌ **bloqueado** | fluxo humano formal |

### 5.3 Dois eixos, mesma física

`ambiguidade × raio × irreversibilidade` decide quanto **processo** a mudança recebe (a
raia). `irreversibilidade × impacto` decide quanto **gate** a ação recebe. Processo é para
construir; gate é para agir — e os dois compartilham o fator que mais pesa.

### 5.4 Abordagens avaliadas

| Abordagem | O que oferece | Veredito |
|---|---|---|
| **Política declarativa `permitir/negar/perguntar`** | decidir por classe, não por instância | **Adotado** |
| **Taxonomia de classes de risco** | gradua o gate | **Adotado** — base deste capítulo |
| **Aprovação humana para alto risco** | humano no ponto consequente | **Adotado** — os quatro indelegáveis |
| **Menor privilégio e autorização declarativa** | permissão fora do modelo | **Adotado** |
| **Gate uniforme** | simplicidade aparente | **Rejeitado** — funil ou catástrofe |

## 6. ⭐ Na prática — o ciclo real

**O gate de merge é um script que se recusa a decidir.** O `promote-main.sh` executa o
mecânico e para diante de tudo que cheira a risco:

```
$ scripts/promote-main.sh
abortado: árvore de trabalho suja — commite ou limpe antes de promover.
```

As guardas são explícitas no código: aborta com árvore suja, aborta se a branch não existe,
aborta se não há avanço, e — sem o `--yes` — **pergunta**. O cabeçalho do arquivo declara o
limite em uma frase: o script cuida da execução, não da decisão.

Depois do "sim", ele registra o gate sozinho:

```
gate registrado: gate-main-0021b20
ok: 'main' promovido para 0cf56ab.
```

Vinte e um gates de merge registrados até aqui, cada um com identificador, data e título. O
gate deixou de ser um momento e virou **uma linha auditável**.

**A alavanca da reversibilidade aparece na prática mais banal do repositório**: todo ciclo
é um commit pequeno numa branch, promovido depois do gate. Isso mantém quase toda mudança
na classe "criação reversível" — e é por isso que o método consegue promover dezessete vezes
em três dias sem dupla aprovação: **não é gate frouxo, é ação de classe baixa**.

**E o `--yes` é honesto.** Ele existe, está documentado no cabeçalho e é usado quando o
humano já decidiu na conversa — o que preserva a semântica ("o humano decidiu") sem
teatro de confirmação. Um gate que ninguém consegue pular vira gate contornado por fora; um
gate com escape declarado mantém a decisão no lugar certo, registrada.

**O que ainda não temos**, e o capítulo não vai fingir que sim: nenhuma ação deste
repositório chegou às classes "financeira/irreversível" ou "lote/administrativa". A
taxonomia inteira está escrita, mas só as três primeiras classes foram exercitadas de fato.

## 7. Erros e anti-padrões

- **Gate uniforme** — funil ou catástrofe, nunca outra coisa.
- **Aprovar por hábito** — carimbo com aparência de controle.
- **Deixar o modelo decidir permissão** — autorização é política, não julgamento de texto.
- **Acrescentar aprovação em vez de reversibilidade** — quase sempre mais caro e menos
  seguro.
- **Gate sem escape declarado** — vira contorno por fora, e o contorno não fica registrado.

## 8. Verificação

1. Uma tarefa apaga registros de produção. Classifique-a e diga o gate. Depois diga que
   três mudanças a rebaixariam de classe — e por que isso vale mais que outra aprovação.
2. Explique a diferença entre o eixo que escolhe a raia e o eixo que escolhe o gate, e o
   que os dois têm em comum.
3. Por que a política de permissão deve viver fora do modelo, mesmo que ele "entenda" a
   regra?

## 9. O que roubar

- **Grade o gate por irreversibilidade × impacto** — e escreva a tabela antes de precisar
  dela.
- **Prefira rebaixar a classe a somar aprovação**: reversibilidade compra velocidade.
- **Bloqueie o catastrófico**, não o dificulte: lote, entre inquilinos e administrativo
  exigem fluxo humano formal.
- **Declare o escape do gate** e registre quem o usou — gate sem saída legítima é gate
  burlado.

---

**Conexões**: [01 — o princípio central](01-principio-central.md) (o gate localiza a
responsabilidade) · [03 — Spec-Driven](03-spec-driven.md) (o eixo das raias) ·
[06 — papéis e RACI](06-papeis-raci.md) (o responsável final age exatamente aqui) ·
[09 — DoR/DoD](09-definition-of-ready-done.md) (gate barato no baixo risco) ·
[11 — rastreabilidade](11-rastreabilidade.md) (o gate vira linha auditável) ·
[Diário da jornada](../research/jornada-aprendizado-modelo-operacional.md) `[9]`.

**Fontes**: Anthropic, *Building effective agents* —
https://www.anthropic.com/engineering/building-effective-agents ·
OWASP, *LLM01 Prompt Injection* — https://genai.owasp.org/llmrisk/llm01-prompt-injection/ ·
Open Policy Agent — https://www.openpolicyagent.org/docs ·
[Princípios](../governance/principles.md) (III — classes de risco) ·
[Modelo operacional](../governance/operating-model.md) §8.
