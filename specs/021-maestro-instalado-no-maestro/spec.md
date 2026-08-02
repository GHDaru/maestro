# Spec 021 — Maestro instalado no próprio Maestro

- **Status**: Concluída · **Raia**: plena · **Data**: 2026-08-02
- **Origem**: pedido do Steward — "vamos instalar o Maestro no próprio Maestro".

## O quê e por quê

O método se instala em outros repositórios desde o ciclo 018, mas nunca foi instalado
**aqui**. Instalar no próprio repositório é o teste mais barato que existe: se o Maestro
não passa no seu próprio instalador, ninguém deveria confiar nele nos outros.

E não passou. A auto-instalação achou três derivas silenciosas, todas da mesma família —
**lista escrita à mão que ninguém compara com o disco**:

1. `AGENTS.md` (o arquivo que a maioria dos assistentes lê) ficou sem a regra "skills
   primeiro", presente no `CLAUDE.md` desde o ciclo 011;
2. a skill `jornada-viva`, criada no ciclo 018, nunca entrou na instrução — três ciclos
   existindo no disco e **invisível** para a Inteligência Artificial (IA);
3. o Constitution Check da skill e de dois agentes dizia "I–VII"; a constituição tem VIII
   desde o ciclo 013 — oito ciclos de planos sem onde marcar o princípio.

Nada disso quebrava build. Apenas a IA seguia menos método do que o repositório declarava.

## Requisitos funcionais

- **FR1**: QUANDO `verificar-instalacao.sh` roda num repositório, O SISTEMA DEVE checar as
  camadas do método (agentes, skills, scripts, templates, governança) e falhar se faltar.
- **FR2**: QUANDO existe `CLAUDE.md` ou `AGENTS.md`, O SISTEMA DEVE exigir que ele aponte
  para a constituição, mande consultar as skills, descreva o fluxo e cite as raias —
  arquivo presente e mudo é pior que ausente, porque parece instalado.
- **FR3**: QUANDO uma skill existe em `skills/` e não é citada na instrução, O SISTEMA DEVE
  falhar — skill invisível é skill que não existe.
- **FR4**: QUANDO alguém instala o método, O SISTEMA DEVE oferecer o bloco de instrução
  **gerado das skills do disco** (`instalar-maestro.sh --bloco`), não um texto fixo.
- **FR5**: QUANDO a constituição ganha um princípio, `verificar-papeis.sh` DEVE acusar se o
  template de plano continuar checando menos princípios do que existem.
- **FR6**: O repositório do Maestro DEVE passar em `verificar-instalacao.sh` com código 0.

## Fora de escopo

- Publicar o backend do companion (pendência do Steward, desde o ciclo 015).
- Migrar o capítulo 02 ao padrão editorial v2 — é o ciclo seguinte, com o método já
  auto-instalado.
- Corrigir os `specs/` antigos que citam "I–VII": são registro histórico, não norma viva.

## Critérios de aceite (DoD)

- [x] `scripts/verificar-instalacao.sh` **provado falhando** neste repositório: 2 achados reais
- [x] Depois da correção, exit 0 aqui
- [x] Prova ponta a ponta: instalar num repositório vazio → check **falha** (7 achados) →
      colar o bloco `--bloco` + symlink → check **passa** → `novo-ciclo.sh 001` funciona
- [x] `verificar-papeis.sh` **provado falhando** ao remover a linha do princípio VIII
- [x] Constitution Check cobre I–VIII na skill, nos dois agentes e no template
- [x] ADR 0013 escrito e registrado em `decisoes.jsonl`

## Clarify

1. Duas cópias (CLAUDE/AGENTS) ou uma? → **uma**: `AGENTS.md` vira link simbólico. Cópia
   escrita à mão diverge; a pergunta não é se, é quando.
2. Gerar o `CLAUDE.md` inteiro? → **não**, só o bloco do método. O que o projeto tem de
   particular é do humano.
