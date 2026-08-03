# 01 — O princípio central: quem decide o quê

> **Capturado em** 2026-08 · última revisão 2026-08-01 · ciclo 016 (migrado ao padrão v2)
>
> **IA para explorar, propor e escrever; humano para especificar, decidir e aprovar;
> testes, gates e revisão independente para validar.**

## 1. Objetivos

Ao fim deste capítulo você será capaz de:

1. **Explicar** por que a capacidade de raciocinar de um agente não substitui o gate humano;
2. **Distinguir** registro *ex-post* de gate *ex-ante* — e dizer quando cada um basta;
3. **Aplicar** a reversibilidade como alavanca: converter ação irreversível em delegável;
4. **Identificar** os quatro gates indelegáveis no seu próprio fluxo de trabalho.

## 2. O problema

A pergunta que abriu este método foi provocativa: *se um agente **é capaz** de tomar
qualquer decisão — inclusive registrar alternativas e racional impecáveis — **o que ainda
exige o humano?***

É uma pergunta honesta, e a resposta preguiçosa ("humano decide porque sim") não sobrevive
a ela. Sem uma resposta boa, a organização cai num dos dois extremos: **aprova tudo** (e o
humano vira gargalo, anulando o ganho da IA) ou **aprova nada** (e descobre o erro quando
ele já é irreversível).

## 3. A ideia central

> **O gate humano não mede a qualidade do raciocínio do agente — ele localiza a
> responsabilidade.** E o que torna uma ação irreversível segura de delegar não é a
> aprovação: é convertê-la em reversível.

## 4. A regra vigente

1. **A intenção vive na especificação**, não no código nem no prompt. O humano dirige e
   refina; o agente escreve.
2. **Quem executa não é quem verifica.** A verificação passa por um revisor independente,
   em **contexto fresco** — segregação de funções aplicada a agentes.
3. **Prove, não declare.** "Pronto" exige evidência que o agente gere e um gate confira.
4. **O humano decide a política, não a instância** — `permitir / negar / perguntar` por
   classe de ação, e a política vai ao registro.
5. **Ação irreversível exige reversibilidade engenheirada antes de delegar.**
6. **Gates indelegáveis, sempre**: aprovar a spec · aprovar o plano · aprovar o merge ·
   autorizar deploy/migração.

## 5. Fundamentos

### 5.1 Capacidade não é *accountability*

Capacidade de **raciocinar** não é o mesmo que **responder pelas consequências**. Um
agente pode produzir a melhor análise da mesa e ainda assim não ter o que perder se ela
estiver errada. O gate humano existe para que a responsabilidade tenha nome — não para
duvidar do raciocínio.

### 5.2 *Ex-post* não impede dano *ex-ante*

Um registro auditável é **ex-post**: descreve a decisão depois de tomada. Um gate é
**ex-ante**: barra antes de executar. Para ação **irreversível**, auditar não impede o
dano — o relatório perfeito de um dado apagado não traz o dado de volta.

### 5.3 A alavanca real: reversibilidade

Daí a virada que sustenta o método: o gate humano sempre foi um **proxy** de *"torne
reversível, ou olhe antes"*. Onde existe backup, execução a seco (*dry-run*), homologação
e exclusão lógica (*soft-delete*), a ação **muda de classe de risco** e passa a ser
delegável. Reversibilidade compra velocidade.

### 5.4 Frameworks avaliados

| Abordagem | O que oferece | Veredito |
|---|---|---|
| **Human-in-the-loop / mixed-initiative** (Horvitz) | Humano no ponto de decisão para ações consequentes | **Adotado** — espinha do princípio |
| **Política declarativa `permitir/negar/perguntar`** (OpenAI Agents; Open Policy Agent) | Decidir *classes* de ação, não cada instância | **Adotado** — a responsabilidade sobe para a política |
| **ADR — Registro de Decisão de Arquitetura** (Nygard) | Decisão + contexto + alternativas + consequências | **Adotado** — protocolo de registro |
| **Padrões de reversibilidade** (backup, dry-run, staging, soft-delete, checkpoint/rewind do git) | Tornar o irreversível reversível | **Adotado** — requisito da Definição de Pronto (DoD) em infraestrutura |
| **Taxonomia de classes de risco** | Gradua o gate por risco | **Adotado** — mapa dos gates humanos |

## 6. ⭐ Na prática — o ciclo real

O princípio virou código no `scripts/promote-main.sh`, o script que promove o trabalho
para a linha principal. Ele executa o **mecânico** (mover a referência, empurrar com nova
tentativa em caso de falha de rede, registrar a decisão) e **não decide nada**:

```
$ scripts/promote-main.sh
abortado: árvore de trabalho suja — commite ou limpe antes de promover.
```

Guardas verificados no ciclo 006, com o hash da linha principal **inalterado** depois da
tentativa: aborta com árvore suja; aborta se não há avanço; sem `--yes`, pede confirmação
explícita. Só depois do "sim" humano ele age — e então registra sozinho:

```
gate registrado: gate-main-e32023f
ok: 'main' promovido para 6d7ab7b.
```

Repare na divisão exata do princípio: **automatizar a execução** do ritual é economia de
atenção; **automatizar a decisão** seria violar o Princípio II. O script materializa a
fronteira.

## 7. Erros e anti-padrões

- **Gate uniforme** — aprovar tudo com o mesmo rigor. Vira funil (e, pior, carimbo: quem
  aprova 200 itens por dia não aprova nenhum).
- **Confundir auditoria com controle** — registrar decisão irreversível não a torna segura.
- **Delegar o A** (o *Accountable* do RACI) — delega-se executar, consultar e informar;
  responder, nunca.
- **Esperar confiança estatística** — "quando eu confiar no agente, delego". A confiança
  perfeita não chega; a reversibilidade, sim.

## 8. Verificação

1. Um agente propõe apagar 10 mil registros e anexa um registro de decisão impecável.
   Isso basta? Justifique usando *ex-ante × ex-post*.
2. Sua equipe quer delegar a migração de um banco. Que três mudanças **rebaixam a classe
   de risco** dessa ação — e por que elas valem mais que uma aprovação a mais?
3. Cite os quatro gates indelegáveis e explique o que cada um protege.

## 9. O que roubar

- **Decida a política, não o item**: `permitir / negar / perguntar` por classe de ação é o
  que faz a supervisão parar de crescer com o volume.
- **Antes de pedir aprovação, pergunte se dá para tornar reversível** — quase sempre é mais
  barato que o gate.
- **Automatize a execução do ritual, nunca a decisão** — e faça o script registrar a
  decisão humana, para o estado do gate não viver fora do repositório.

---

**Conexões**: [03 — Spec-Driven](03-spec-driven.md) (onde a intenção vive) ·
[04 — contexto](04-fluxo-agentic-contexto.md) (revisor fresco) ·
[10 — gates e risco](10-gates-classes-de-risco.md) (a taxonomia) ·
[13 — decisões de engenharia](13-decisoes-de-engenharia.md) §5.7 ·
[Diário da jornada](../research/jornada-aprendizado-modelo-operacional.md) `[1]`.

**Fontes**: Anthropic, *Building effective agents* —
https://www.anthropic.com/engineering/building-effective-agents ·
Claude Code, *Best practices* — https://code.claude.com/docs/en/best-practices ·
E. Horvitz, *Principles of Mixed-Initiative UI* —
https://www.microsoft.com/en-us/research/publication/principles-mixed-initiative-user-interfaces/ ·
M. Nygard, *Documenting Architecture Decisions* —
https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions ·
OWASP, *LLM01 Prompt Injection* — https://genai.owasp.org/llmrisk/llm01-prompt-injection/ ·
[Princípios do Maestro](../governance/principles.md) (III — reversibilidade e gates).
