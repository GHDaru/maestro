# Tasks 021 — Maestro instalado no próprio Maestro

## Verificação primeiro
- [x] T0 — `scripts/verificar-instalacao.sh`: camadas + instrução da IA + coerência das skills
- [x] T1 — rodá-lo **antes** de qualquer correção: 2 achados reais (AGENTS.md mudo, `jornada-viva` invisível)
- [x] T2 — contagem princípios × Constitution Check em `verificar-papeis.sh`, provada falhando

## Implementação
- [x] T3 — `CLAUDE.md` reescrito: 6 skills em tabela, ramo de UI, fitness functions, artefatos vivos
- [x] T4 — `AGENTS.md` vira link simbólico para `CLAUDE.md` (fonte única)
- [x] T5 — `instalar-maestro.sh --bloco`: instrução gerada de `skills/*/SKILL.md`
- [x] T6 — instalador leva `verificar-instalacao.sh` e manda prová-lo no passo 2
- [x] T7 — Constitution Check para I–VIII na skill, em `plan-arquiteto`, em `guardiao-processo` e no `novo-ciclo.sh`
- [x] T8 — referências erradas de princípio no modelo operacional (P. VII → P. VI / §)
- [x] T9 — receita de instalação reescrita (instalar ≠ copiar) e `scripts/README.md`
- [x] T10 — ADR 0013 + linha em `decisoes.jsonl`

## Gate
- [x] T11 — DoD verde: checks proprios + prova ponta a ponta em repositório vazio
- [ ] T12 — gate de merge humano → `promover-main.sh`
