# 11 — Rastreabilidade: a memória que sobrevive ao reset

> **Capturado em** 2026-08 · última revisão 2026-08-02 · ciclo 031 (migrado ao padrão v2)
>
> **O agente esquece; o repositório não.** Rastreabilidade devolve *o quê* e *o porquê* sem
> re-derivar — e **emerge** do fluxo, sem matriz que ninguém mantém.

## 1. Objetivos

Ao fim deste capítulo você será capaz de:

1. **Explicar** por que rastreabilidade deixa de ser burocracia e vira infraestrutura
   quando quem executa reseta o contexto;
2. **Distinguir** o sentido para frente (a intenção foi construída e verificada?) do sentido
   para trás (deste sintoma até o porquê);
3. **Construir** o elo por convenção — spec numerada, commit que a cita, registro de
   decisão, gate registrado — sem ferramenta dedicada;
4. **Avaliar** quando uma matriz formal de rastreabilidade é desperdício.

## 2. O problema

Daqui a três meses um teste quebra. Quem vai investigar — humano ou agente — chega com
**memória zero**: não viveu a discussão, não sabe qual requisito aquele teste protege, não
sabe se o comportamento atual é a intenção ou um resíduo.

Sem rastro, a única saída é re-derivar: ler código, adivinhar propósito, decidir de novo o
que já tinha sido decidido. Foi assim que o requisito original se perdeu — não por
desleixo, mas porque nada ligava o sintoma à intenção.

## 3. A ideia central

> **Artefatos ligados são a memória durável do projeto.** O contexto do agente é volátil por
> construção; o elo entre spec, commit, verificação e decisão é o que sobrevive.

## 4. A regra vigente

1. **Elo obrigatório na Definição de Pronto**: spec numerada ↔ commit ↔ verificação ↔
   jornada, explícitos.
2. **Convenção em vez de ferramenta**: a spec numera, o commit cita, o teste nomeia o
   requisito, o registro de decisão guarda o porquê.
3. **Registro de decisão é imutável e superável** — nada fica preso, tudo fica rastreável.
4. **O gate vira linha**: cada promoção registra identificador, data e título no índice de
   decisões.
5. **Otimize o sentido para trás** (sintoma → causa → porquê): é ele que encurta a
   recuperação.
6. **Nenhuma matriz de rastreabilidade** — se o elo não emerge do fluxo, ele não é mantido.

## 5. Fundamentos

### 5.1 Por que isso é estrutural com agentes

Num time humano, parte da memória fica nas pessoas. Com agentes, **não fica em lugar
nenhum**: cada sessão nova começa do zero, por desenho. A rastreabilidade deixa de ser boa
prática de auditoria e passa a ser o único mecanismo de continuidade.

### 5.2 Dois sentidos, dois usos

**Para frente**: esta spec virou código? esse código tem verificação? — é cobertura de
intenção. **Para trás**: este sintoma vem de qual mudança, que atendia qual requisito,
decidido por quê — é recuperação, a métrica de estabilidade do capítulo 02.

### 5.3 Emergente, não construído

Ninguém constrói "um sistema de rastreabilidade". O elo aparece quando cada artefato cita o
próximo, e a Definição de Pronto força a citação. É subproduto do fluxo — e por isso não
tem custo de manutenção separado.

### 5.4 Abordagens avaliadas

| Abordagem | O que oferece | Veredito |
|---|---|---|
| **Matriz formal de rastreabilidade** | rastreio requisito × teste | **Rejeitado** — pesada; ninguém mantém |
| **Vínculo nativo entre commit, pull request e spec** | elo barato, dentro do fluxo | **Adotado** — a spec numera, o commit cita |
| **Registro de decisão ligado a componentes** | decisão → sistema | **Parcial** — o registro sim; diagramas ficam para depois |
| **Documentação como código, com referências cruzadas** | links versionados | **Adotado** — capítulos, receitas e registros se citam |
| **Índice legível por máquina** | consulta e auditoria | **Adotado** — `decisoes.jsonl`, append-only |

## 6. ⭐ Na prática — o ciclo real

Um exemplo completo, do fim para o começo — o caminho que alguém percorreria daqui a três
meses.

**Começa por uma linha de registro** (o gate que autorizou aquilo entrar):

```json
{"id": "gate-main-0021b20", "data": "2026-08-02",
 "titulo": "Gate de merge: feat(livro): BPMN navegável … (spec 020)",
 "status": "aceita", "registro": "commit 0021b20"}
```

**A linha aponta para o commit**, e o commit cita a spec — vinte e oito commits do
repositório trazem a referência `spec NNN` no assunto:

```
$ git log --oneline --grep="spec 021"
12332c3 feat(metodo): o Maestro instalado no próprio Maestro (spec 021, ADR 0013)
```

**A spec abre a pasta do ciclo**, com os quatro artefatos: o que se queria (`spec.md`), como
seria feito com o Constitution Check (`plan.md`), o que foi feito (`tasks.md`) e o que foi
provado (`qa-report.md`). **E o registro de decisão** (ADR 0013, citado no mesmo assunto)
guarda o porquê — inclusive as alternativas descartadas e o custo aceito.

Quatro saltos, nenhuma ferramenta: linha do gate → commit → ciclo → decisão. É o sentido
**para trás** funcionando, e cada elo existe porque algum passo do fluxo o obriga —
`promote-main.sh` escreve a linha, o padrão de mensagem cita a spec, `new-cycle.sh` cria a
pasta, a Definição de Pronto exige o relatório.

**O elo mais frágil está declarado**: a citação `spec NNN` no assunto do commit é
**convenção**, não check. Nenhum portão a exige hoje. Ela se sustentou em vinte e oito
commits por hábito — e hábito é exatamente o que o método diz não confiar (a lição do ciclo
021). Fica registrado aqui como candidato a portão, não como virtude.

## 7. Erros e anti-padrões

- **Matriz que ninguém mantém** — rastreabilidade que virou projeto próprio já morreu.
- **Elo por memória** — "todo mundo cita a spec" dura até o dia cansado.
- **Registro de decisão editado no mérito** — apaga a memória que justificava o elo.
- **Otimizar só o sentido para frente** — bonito em auditoria, inútil no incidente.
- **Guardar o porquê fora do repositório** — conversa de chat não é rastro.

## 8. Verificação

1. Um teste quebra e ninguém lembra o requisito que ele protege. Descreva o caminho de
   volta no seu repositório — e diga qual elo falta.
2. Por que a rastreabilidade é mais crítica com agentes do que com um time humano estável?
3. Nosso elo mais frágil é uma convenção de mensagem de commit. Escreva o critério
   verificável que a transformaria em portão.

## 9. O que roubar

- **Numere a unidade de trabalho** e faça todo o resto citar esse número.
- **Registre o gate como dado**, não como lembrança — uma linha por decisão.
- **Prefira convenção barata a ferramenta pesada** — mas saiba quais elos são convenção, e
  admita que dependem de hábito.
- **Otimize o caminho de volta**: sintoma → mudança → requisito → porquê, em poucos saltos.

---

**Conexões**: [04 — contexto](04-fluxo-agentic-contexto.md) (o reset que torna isto
necessário) · [08 — artefatos](08-entregaveis-artefatos.md) (o que liga o quê) ·
[09 — DoR/DoD](09-definition-of-ready-done.md) (a Definição de Pronto força o elo) ·
[10 — gates](10-gates-classes-de-risco.md) (o gate que vira linha) ·
[12 — governança leve](12-governanca-leve.md) (a memória imutável) ·
[Diário da jornada](../research/jornada-aprendizado-modelo-operacional.md) `[11]`.

**Fontes**: DORA, *four keys* (recuperação: do sintoma à causa) —
https://dora.dev/guides/dora-metrics-four-keys/ ·
L. Mezzalira, *Documenting software architecture* —
https://lucamezzalira.medium.com/how-to-document-software-architecture-techniques-and-best-practices-2556b1915850 ·
[Modelo operacional](../governance/operating-model.md) §8–§9 ·
[Protocolo do índice de decisões](../records/README.md).
