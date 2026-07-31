# ADR 0008 — Avaliação do ecossistema SDD: manter Spec Kit único, absorver EARS e práticas do Superpowers

- **Status**: Aceito (aprovado pelo Steward em 2026-07-31 — "pode incorporar todas as
  sugestões"; absorções materializadas na spec 008) · **Data**: 2026-07-30
- **Ciclo**: spec 007 · **Pesquisa**: `docs/research/avaliacao-ecossistema-sdd.md`

## Contexto

O Maestro adotou o Spec Kit (motor SDD) e descartou o OpenSpec (ADR 0005), mas o restante
do ecossistema — Superpowers, BMAD, Kiro, Taskmaster, Agent OS, GSD, Tessl — nunca havia
passado pelo crivo. O Steward perguntou explicitamente "foi avaliado?". A pesquisa 007
fichou 7 ferramentas com fontes primárias.

## Decisão

1. **Manter o Spec Kit como ferramenta SDD única** (reafirma ADR 0005). Nenhum framework
   integral concorrente entra: **BMAD descartado** (substituiria o modelo; cerimônia
   scrum-like já rejeitada; custo de token alto), **Kiro descartado como ferramenta**
   (proprietária, lock-in de IDE), **Superpowers não adotado por atacado** (segunda fonte
   de verdade de processo).
2. **Absorver ideias com destino concreto**:
   - **EARS** (Kiro) — sintaxe `QUANDO <condição> O SISTEMA DEVE <comportamento>` vira a
     forma recomendada de critério de aceite → skill `dod-verificavel` + `spec-template`
     (na F4 de vendorização).
   - **Worktree isolado por task + rigor mandatório** (Superpowers) → candidatos a
     script/skill na F3 futura, quando houver dor real de paralelismo (registrar em retro).
   - **Standards por camada** (Agent OS) → template `docs/standards/` apenas quando o
     Maestro reger codebase de produto (gatilho, não agora — YAGNI).
3. **Observar com gatilho explícito**: Taskmaster (>20 tasks paralelas/multi-projeto),
   GSD (nenhuma lacuna hoje — raia leve cobre), Tessl (maturidade + case de produção),
   Agent OS (onboarding em legado grande).
4. A ficha de pesquisa + este ADR são a **resposta canônica** a "isso foi avaliado?" —
   linkados no roadmap §6.

## Alternativas consideradas

- **Adotar Superpowers integral**: melhor biblioteca de skills do mercado, mas criaria dois
  processos mandatórios concorrentes; o ganho real (disciplina TDD, subagente com review
  fresco, clarify socrático) já existe no Maestro com outro nome.
- **Adotar BMAD**: papéis prontos, mas é o *nosso* modelo reimplementado com cerimônia que
  já rejeitamos; trocaria governança testada por vocabulário scrum.
- **Não avaliar nada (status quo)**: deixaria a afirmação "trazemos de todas as fontes"
  sem lastro e a pergunta do Steward sem resposta auditável.

## Consequências

- (+) Resposta auditável e linkável para "já avaliamos X?"; re-litígio vira link.
- (+) Duas melhorias concretas entram no funil com destino nomeado (EARS; worktree/rigor).
- (+) Vereditos "observar" têm gatilho — reavaliação é evento, não ansiedade.
- (−) Fichamento foi por fontes primárias sem instalar cada ferramenta; se um gatilho
  disparar, a reavaliação deve incluir hands-on (spec própria).

## Fontes

Ver a ficha completa: `docs/research/avaliacao-ecossistema-sdd.md` (links primários por
ferramenta: github.com/obra/superpowers, github.com/bmad-code-org/BMAD-METHOD,
kiro.dev/docs/specs, github.com/eyaltoledano/claude-task-master,
github.com/buildermethods/agent-os, + comparativos 2026).
