# 08 — Entregáveis e artefatos: o que merece existir

> **Capturado em** 2026-08 · última revisão 2026-08-03 · ciclo 028 (migrado ao padrão v2)
>
> **Todo artefato custa duas vezes** — escrever e manter. Só sobrevive o que é **consumido
> por alguém a jusante, com algo que falha alto quando ele envelhece** — ou o que é
> imutável por construção.

## 1. Objetivos

Ao fim deste capítulo você será capaz de:

1. **Aplicar** o teste do consumidor + forcing function para decidir se um artefato deve
   existir;
2. **Distinguir** artefato vivo (consumido), imutável (registro de um ponto no tempo) e
   morto (sem consumidor);
3. **Identificar** duplicação de função entre artefatos — a origem silenciosa do apodrecimento;
4. **Avaliar** um catálogo de documentação alheio e dizer o que cortar, com critério.

## 2. O problema

A lista canônica de documentos é enorme: requisitos de produto, spec, plano, registro de
decisão, RFC, documento de design, jornada, manual de operação, changelog, diagramas de
arquitetura. Cada um parece útil — e todos "dão contexto e direção".

O problema é que "dar direção" **não distingue nada**: um documento de design também dá
direção e apodrece igual. Sem critério, a pasta de documentação cresce até o dia em que
ninguém confia em nenhum arquivo dela — e aí o custo já foi pago duas vezes, sem retorno.

## 3. A ideia central

> **O que mantém um artefato vivo é mecânico, não editorial.** Ou alguém a jusante o
> consome e falha alto quando ele está velho, ou ele é imutável. Não havendo nenhum dos
> dois, é cerimônia de papel — corte.

## 4. A regra vigente

1. **Manter só artefato com consumidor + forcing function**, ou imutável por natureza.
2. **Não criar artefato cuja função já é servida por um vivo**: requisitos de produto
   avulsos duplicam a spec; documento de design avulso duplica plano + registro de decisão.
3. **Registro de decisão (ADR) é imutável**: mudou de ideia? Novo registro que **supera** o
   anterior. Editar o mérito apaga a memória.
4. **Jornada vive por gate**: capturas geradas do build real e heurística revisada **no
   mesmo pull request**.
5. **Changelog com forcing function**: a integração contínua falha se a mudança não escrever
   nele.
6. **Artefato efêmero é legítimo** — a lista de tarefas serve ao ciclo e pode ser
   descartada depois.

## 5. Fundamentos

### 5.1 O teste em duas perguntas

*Quem consome este artefato?* e *o que quebra, alto, quando ele fica velho?* A spec passa:
o agente gera código dela; spec velha vira código errado. O teste passa: a integração
contínua o executa; teste velho fica vermelho. Um documento de design avulso não passa
nenhuma das duas — e por isso apodrece, por melhor que seja.

### 5.2 Imutabilidade é a outra forma de sobreviver

Um registro de decisão não precisa de atualização porque **descreve um instante**: o que se
sabia, o que se decidiu, o que se aceitou como custo. Ele nunca fica "desatualizado" — no
máximo, fica superado, e o sucessor o diz explicitamente. É a única categoria de documento
que envelhece sem apodrecer.

### 5.3 Duplicação é como o apodrecimento começa

Dois artefatos que servem à mesma função competem: um é atualizado, o outro fica para trás
e continua parecendo válido. O leitor não sabe qual vale. Por isso o critério de corte não
é só "tem consumidor?", mas também "**alguém vivo já faz isso?**".

### 5.4 Catálogo avaliado

| Artefato | Consumidor | Forcing function | Veredito |
|---|---|---|---|
| **Spec** | o agente, que gera código dela | código errado se estiver velha | **Essencial** |
| **Plano** | quem implementa; Constitution Check | divergência com a implementação | **Essencial** |
| **Tarefas** | quem implementa | efêmero — descartável após o uso | **Essencial (efêmero)** |
| **Código + testes** | integração contínua | vermelho | **Essencial** |
| **Registro de decisão (ADR)** | decisões futuras, quem chega depois | **imutável** | **Essencial** |
| **Jornada** | gate do pull request | falha se as capturas não forem regeradas | **Essencial (por gate)** |
| **Changelog** | quem lê a release | a integração contínua falha sem entrada | **Essencial (com gate)** |
| **Índice de decisões** | consulta por máquina | append-only, validado por script | **Essencial** |
| **Definição de Pronto/Pronto para começar** | agente e gate de merge | bloqueia o merge | **Essencial** |
| Requisitos de produto avulsos | — (duplica a spec) | nenhuma | **YAGNI** |
| Documento de design / RFC avulso | — (duplica plano + ADR) | nenhuma | **YAGNI** |
| Diagramas de arquitetura | humano, na leitura | nenhuma | **Depois, se doer** |
| Painel de métricas | — | nenhuma | **YAGNI** |

## 6. ⭐ Na prática — o ciclo real

**O changelog só sobrevive porque a integração contínua o cobra.** O gate é literal —
qualquer mudança sem entrada no arquivo derruba a verificação:

```yaml
- name: Require a CHANGELOG.md entry
  run: |
    if git diff --name-only "$base"...HEAD | grep -qx 'CHANGELOG.md'; then ...
    else
      echo "::error::Toda PR deve adicionar uma entrada em [Unreleased] no CHANGELOG.md
            (ou aplicar o label 'skip-changelog')."
      exit 1
```

Repare no que o gate tem de honesto: existe uma **válvula de escape declarada**
(`skip-changelog`). Forcing function sem escape vira burocracia contornada por fora; com
escape nomeado, o desvio fica registrado.

**A imutabilidade dos registros de decisão é verificável.** Dos dez registros do
repositório, nove têm **um único commit** desde que nasceram:

```
$ for f in docs/adr/00*.md; do echo "$(basename $f): $(git log --oneline -- $f | wc -l)"; done
0004-modelo-operacional.md: 1
...
0008-avaliacao-ecossistema-sdd.md: 2
```

O único com dois commits é o 0008 — e o segundo commit mudou **a linha de status** (de
proposta para aceito, quando o Steward aprovou), não o mérito. É a exceção que confirma a
regra: o conteúdo da decisão nunca foi reescrito.

**O índice de decisões é o artefato mais barato de manter do repositório** porque ninguém o
mantém à mão: `promote-main.sh` escreve a linha do gate sozinho, e
`record-decision.sh` valida JSON, campos obrigatórios e unicidade do identificador antes
de anexar. Trinta e oito linhas, nenhuma editada depois de escrita.

**E a prova de que o catálogo é seguido**: vinte e seis dos vinte e oito ciclos têm os
quatro artefatos completos (spec, plano, tarefas, relatório de qualidade). Os dois que não
têm são os ciclos abertos agora, com os artefatos ainda em esqueleto — o que também é
informação, e não maquiagem.

## 7. Erros e anti-padrões

- **Artefato sem consumidor** — nasce bonito, morre calado, continua parecendo válido.
- **Duplicar função** — dois documentos para a mesma coisa; um sempre fica para trás.
- **Editar registro de decisão no mérito** — apaga a memória do projeto; o certo é superar.
- **Forcing function sem válvula declarada** — vira contorno por fora, e o contorno não
  fica registrado.
- **Jornada como documento solto** — sem gate no pull request, apodrece como qualquer outro.

## 8. Verificação

1. Alguém propõe um documento de requisitos de produto além da spec. Aplique o teste das
   duas perguntas e diga o que acontece com ele em três meses.
2. Por que um registro de decisão não precisa ser atualizado — e o que se faz quando a
   decisão muda?
3. Seu changelog está sempre desatualizado. Que mudança **mecânica** conserta isso, e por
   que pedir disciplina não conserta?

## 9. O que roubar

- **Antes de criar documento, nomeie o consumidor.** Se não houver, não crie.
- **Prefira o imutável ao "vivo por esforço"** — registro de decisão custa uma escrita e
  zero manutenção.
- **Ponha a forcing function no mesmo pull request** — o que não é cobrado na hora não é
  cobrado nunca.
- **Declare a válvula de escape**: gate sem saída legítima é gate contornado às escondidas.

---

**Conexões**: [03 — Spec-Driven](03-spec-driven.md) (a spec é o arquétipo do input
consumido) · [09 — DoR/DoD](09-definition-of-ready-done.md) (checklists verificáveis) ·
[11 — rastreabilidade](11-rastreabilidade.md) (o que liga spec, pull request, testes e
jornada) · [12 — governança leve](12-governanca-leve.md) (o registro imutável) ·
[Diário da jornada](../research/jornada-aprendizado-modelo-operacional.md) `[7]`.

**Fontes**: M. Nygard, *Documenting Architecture Decisions* —
https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions ·
S. Brown, *C4 model* — https://c4model.com/ ·
L. Mezzalira, *Documenting software architecture* —
https://lucamezzalira.medium.com/how-to-document-software-architecture-techniques-and-best-practices-2556b1915850 ·
[Modelo operacional](../governance/operating-model.md) §6 ·
[Princípios](../governance/principles.md) (VI — artefatos vivos).
