# Princípios do Maestro (constituição da metodologia)

> Fonte de verdade das convenções do **Maestro**. Prevalece sobre qualquer outra prática
> deste repositório. **Todo agente e humano DEVE ler este documento antes de qualquer
> trabalho.** Emendas via ADR + bump de versão.
>
> **Versão**: 1.0.0 · **Ratificada**: 2026-07-22

Maestro é a metodologia de **1 humano regendo N agentes de IA**: a especificação é a fonte
de verdade, os agentes executam, o humano decide/aprova/verifica. Estes são os princípios
inegociáveis; o **modelo operacional** (`modelo-operacional.md`) os operacionaliza e o
**handbook** (`../handbook/`) os fundamenta.

## Princípios

### I. Spec-Driven (a spec é a fonte de verdade)
Nenhum código nasce sem especificação. A spec é o **input que gera** o código, não a sua
descrição — por isso não apodrece. Fluxo `specify → clarify → plan → tasks → implement`.
Mudança de escopo volta à spec antes de virar código.

### II. Orquestração humano-governada (1 rege N)
Papéis são **modos de trabalho** numa matriz humano×agentes (RACI). Delega-se
**Responsible/Consulted/Informed** a agentes; o **Accountable é sempre humano** e responde
**pela política, gates e critérios — não por cada item**. Verificação por **agente
independente em contexto fresco** (quem executa não verifica).

### III. Reversibilidade e gates proporcionais ao risco (NON-NEGOTIABLE)
O gate humano escala com **irreversibilidade × impacto** (taxonomia: leitura → …→
irreversível → bloqueado). O que torna o irreversível seguro de delegar é a
**reversibilidade engenheirada** (backup, dry-run, staging, soft-delete), que **rebaixa a
classe de risco**. Política declarativa `allow / deny / ask`; autorização fora do LLM.

### IV. Test-First e DoD verificável ("prove, não declare")
Testes nascem com (ou antes) o código. "Pronto" é **verificável autonomamente** (pass/fail
que o agente gera e um hook confere); o trabalho é **converter julgamento em check**. Verde
local ≠ certo global — coerência global e "a coisa certa" ficam com o humano. CI e testes
de arquitetura (fitness functions) são gate desde a fundação.

### V. Economia de contexto e corte por fronteira
A janela de contexto é finita e degrada ao encher: preserve o **contexto integrador (a
spec)**, descarte o ruído. Paralelize **por bounded context** (DDD/hexagonal) — bons cortes
tornam a orquestração segura. Menor autonomia que resolve (workflow antes de agent).

### VI. Artefatos vivos e rastreabilidade
Um artefato só existe se é **input consumido com forcing function** (ou imutável, como o
ADR). Não duplicar função já servida. A rastreabilidade **spec ↔ PR ↔ testes ↔ journey**
é a memória durável do projeto — emerge do workflow, sem ferramenta pesada.

### VII. Governança leve que aprende (YAGNI)
A governança **aprende sem inchar**: núcleo firme (esta constituição) + periferia evoluível
(modelo/handbook, versão própria) + memória append-only (ADRs) + **retro → regra
versionada**. **YAGNI** poda o que não paga. Complexidade além do necessário é justificada
por escrito ou removida.

## Governança

Esta constituição prevalece; emendas sobem versão semântica (MAJOR: remoção/redefinição;
MINOR: novo princípio/expansão; PATCH: clarificação) e são registradas em ADR. Toda decisão
material de metodologia vira ADR.

## Nota de linhagem (migração)

Os documentos migrados de `ghdaru`/`flowbuilder` citam "a Constituição" e "Princípio IV/V/
VII" referindo-se à constituição **da plataforma** de origem. No Maestro, esses papéis
correspondem aos princípios acima (mapa aproximado: IV→III+IV, V→IV, VII→II+VI). A
reescrita fina dessas referências para apontar a este documento é **follow-up** registrado
no ADR 0007.
