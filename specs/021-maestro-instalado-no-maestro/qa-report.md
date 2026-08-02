# QA-report 021 — Maestro instalado no próprio Maestro

- **Data**: 2026-08-02 · **Raia**: plena · **Veredito**: **APROVADO** (DoD verde)

## Fitness functions (DoD)

| Check | Esperado | Resultado |
|---|---|---|
| `verificar-instalacao.sh` **antes** da correção | falhar com achados reais | ✅ exit 1 — `AGENTS.md não manda consultar as skills`, `skill 'jornada-viva' … não é citada` |
| `verificar-instalacao.sh` depois | exit 0 | ✅ camadas + instrução + 6/6 skills visíveis |
| `verificar-papeis.sh` com a linha do princípio VIII removida | exit 1 | ✅ `a constituição tem 8 princípios; o template de plano checa 7` |
| `verificar-papeis.sh` restaurado | exit 0 | ✅ `8 princípios → 8 linhas no template` |
| `verificar-agentes.sh` | exit 0 | ✅ 13 agentes, frontmatter, read-only sem Write/Edit |
| **Ponta a ponta** — repositório vazio | falha → passa | ✅ instalar (18 arquivos) → check **falha com 7** → `--bloco >> CLAUDE.md` + symlink → check **passa** → `novo-ciclo.sh 001` cria os 4 artefatos |
| `instalar-maestro.sh --bloco` | lista as skills do disco | ✅ 6 skills, nome + primeira frase, sem corte no meio da palavra |
| `empacotar-plugin.sh --verificar` | sincronizado | ✅ após reempacotar (a skill mudou) |
| `node publicar/build.mjs` | exit 0 | ✅ 35 páginas + sumário |

## Cobertura dos requisitos

- **FR1** (camadas): ✅ 7 caminhos essenciais verificados.
- **FR2** (instrução não muda): ✅ exige constituição + skills + fluxo + raias em cada
  `CLAUDE.md`/`AGENTS.md` encontrado.
- **FR3** (skill invisível): ✅ foi o achado que motivou o ciclo; hoje falha o check.
- **FR4** (bloco gerado): ✅ `--bloco` lê `skills/*/SKILL.md`.
- **FR5** (princípios × template): ✅ implementado e provado falhando.
- **FR6** (o Maestro passa no próprio check): ✅ exit 0.

## Achados

1. **Três derivas, uma causa** (skill `diagnostico-antes-do-fix`): `AGENTS.md` mudo,
   `jornada-viva` invisível e Constitution Check em I–VII são o mesmo defeito — lista
   escrita à mão que ninguém compara com o disco. Corrigido na estrutura (fonte única +
   geração), não no texto; ADR 0013.
2. **O princípio VIII não era checável havia oito ciclos.** A constituição mudou no 013 e
   o executável do Constitution Check (skill, dois agentes, template) ficou para trás. É o
   anti-padrão 15 (artefato que congela) aplicado a uma *norma*, não a um plano.
3. **Referências de princípio erradas no modelo operacional**: quatro linhas citavam
   "(P. VII)" para semântica de interface e documentação viva — a numeração é de outra
   constituição (a do FlowBuilder). Corrigidas para P. VI / seção do próprio modelo.
   Nenhum check cobre esse tipo de citação cruzada; fica registrado como candidato à
   próxima retro **com dono**: verificar citações `P. N` contra os títulos da constituição.

## Pendência de gate

- promoção dev → main aguarda aprovação humana.
