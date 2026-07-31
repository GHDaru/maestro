# Apêndice A — Estudo do repositório `maestro-02`

> **Data do estudo**: 2026-07-31 · **Fonte**: [`GHDaru/maestro-02`](https://github.com/GHDaru/maestro-02)
> (fork de `sharpdeveye/maestro`, commit `00f9115`, v2.0.0, licença MIT)
> **Pergunta do estudo**: o que este repositório contribui para a nossa metodologia?

## O que é (e o que não é)

Apesar do nome, **não é a nossa metodologia** — é um projeto homônimo e independente:
um toolkit de *"workflow fluency for AI coding agents"*. A coincidência de nome é feliz:
ele ataca o mesmo problema (agentes sem estrutura repetem os mesmos erros) pelo **outro
lado** — nós construímos o *método* (governança, papéis, gates); ele constrói o
*instrumento* (skills, memória, telemetria) instalável em qualquer agente.

**Anatomia** (141 arquivos, 3 entregáveis):

| Peça | O que faz |
|---|---|
| `source/skills/` | 1 skill-núcleo (`agent-workflow`, com 7 referências de domínio) + 24 comandos (`/diagnose`, `/fortify`, `/streamline`, `/reflect`…) |
| `mcp-server/` | Servidor MCP (stdio + HTTP): 25 prompts, 10 tools, 8 resources — as skills viram serviço, sem copiar arquivo |
| `maestro-extension/` | Extensão VS Code: wave-engine, context-slicer, token-budget, sidebar |

Distribui as **mesmas skills para 10 providers** (Claude Code, Cursor, Gemini CLI, Codex,
Kiro…) a partir de uma única fonte (`source/` + build multi-provider) — arquitetura
fonte-única → adaptadores, a mesma do nosso `publicar/` (markdown → site/PDF).

## As 6 ideias que contribuem para o Maestro

### 1. Memória persistente como camada explícita (`.maestro/`)

```text
.maestro/
├── context.md       ← contexto do projeto (versionado)
├── decisions.jsonl  ← log de decisões append-only
├── audit.jsonl      ← toda invocação: duração, tokens, custo estimado
└── sessions/        ← resumos de sessão (gitignored)
```

O que nós fazemos com specs/ADRs/retro, ele faz com um diretório-padrão **legível por
máquina** (JSONL). A ideia forte: **decisão e auditoria como dados estruturados**, não só
prosa — abre consulta programática ("últimas 5 decisões" entram no contexto do próximo
comando). *Contribuição:* candidato a formato do nosso protocolo de registro auditável
(decisões consultáveis por agente, não só por humano).

### 2. Trilha de auditoria com custo por invocação

Cada comando loga `{"command","duration_ms","cost_estimate_usd","exit_status"}`. É a
instrumentação que adiamos (DORA/telemetria, YAGNI) — mas em versão **barata**: um JSONL
append-only, sem painel. *Contribuição:* quando nosso gatilho de medição disparar, este é
o primeiro degrau — não um dashboard.

### 3. `/reflect` — a retro executável

Analisa o histórico de comandos e produz um scorecard: quais skills funcionam, quais
falham, taxa de conclusão, custo total. **É a nossa retro transformada em comando** — hoje
a nossa depende de memória humana; com audit.jsonl ela vira consulta. *Contribuição
direta:* a F3 futura pode ganhar um `scripts/retro.sh` que lê nossos artefatos de ciclo e
pré-computa o material da retro.

### 4. Wave-engine — fases com validação entre elas

Todo comando de construção roda em ondas tipadas (`map → validate → scaffold → test`;
comandos de correção: `audit → validate → apply → verify`), com `ValidationResult`
(passed/issues/suggestions) **entre cada fase**. É o nosso ciclo
spec→plan→implement→verify em miniatura, embutido *dentro de um único comando* — a
confirmação independente de que **fases com gate são o padrão que converge**, em qualquer
granularidade. *Contribuição:* vocabulário para descrever nossos gates em nível de task
(não só de ciclo).

### 5. Context-slicer — economia de contexto medida

Em vez de injetar o contexto inteiro, fatia só as seções relevantes ao comando ativo e
**reporta a economia** (`tokenEstimate` vs `fullTokenEstimate`, % savings). Nosso
Princípio V ("cada agente estreito") com **número**. *Contribuição:* o conceito de medir
a economia de contexto — hoje afirmamos, não medimos.

### 6. Anti-patterns como catálogo de primeira classe ("workflow slop")

O skill-núcleo lista explicitamente o que NÃO fazer (não despeje o codebase no contexto;
não use multi-agente para problema de agente único; não repita o mesmo prompt esperando
resultado diferente; não entregue sem avaliação). Nós registramos o que não adotamos
(modelo operacional §10), mas não temos um **catálogo de anti-padrões de execução**.
*Contribuição:* candidata a skill `anti-padroes` nascida das nossas retros.

## Onde ele NÃO nos serve

- **Não tem papéis nem gates humanos** — o operador é um dev individual; não há RACI,
  classes de risco, DoR/DoD, nem o A indelegável. É instrumento, não governança.
- **Não é spec-driven** — os comandos melhoram workflows existentes; nada nasce de spec.
- Adotá-lo por atacado repetiria o erro que descartamos no BMAD/Superpowers (ADR 0008):
  segunda fonte de verdade de processo.

## Síntese — vereditos (mesmo critério do ADR 0008)

| Ideia | Veredito | Destino no Maestro |
|---|---|---|
| Decisões/auditoria em JSONL consultável | 🔄 absorver | protocolo de registro auditável (spec futura) |
| Audit trail com custo por invocação | 👁 observar | 1º degrau da telemetria, quando o gatilho de medição disparar |
| Retro executável (`/reflect`) | 🔄 absorver | `scripts/retro.sh` na evolução da F3 |
| Wave (fases+validação intra-comando) | 🔄 absorver conceito | vocabulário de gates em nível de task |
| Context-slicing medido | 🔄 absorver conceito | medir economia de contexto (Princípio V com número) |
| Catálogo de anti-padrões | 🔄 absorver | skill `anti-padroes` alimentada por retros |
| Adoção integral do toolkit | ❌ descartar | conflito com ferramenta única (ADR 0005/0008) |

> Este apêndice é um **estudo**, não uma decisão: as absorções acima entram no funil como
> candidatas (specs futuras), seguindo a regra de que nada entra ad-hoc. Registro da
> avaliação de ecossistema: [ADR 0008](../adr/0008-avaliacao-ecossistema-sdd.md) e
> [ficha de pesquisa](../research/avaliacao-ecossistema-sdd.md).
