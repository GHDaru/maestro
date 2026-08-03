# ADR 0012 — Distribuição do Maestro em três camadas

- **Status**: Aceito · **Data**: 2026-08-01 · **Ciclo**: 019 · **Decisor**: Steward

## Contexto

Uma Inteligência Artificial (IA) tentou instalar o Maestro e concluiu que "não tinha"
(ciclo 018): o instalador existia mas era invisível. Corrigida a visibilidade, ficou a
pergunta seguinte do Steward: **precisamos de um padrão? qual a da comunidade? como fazer
um instalador como o do Spec Kit?**

Levantamento (agente `research-curator`, 2026-08):

| Padrão | O que faz | Alcance | Custo |
|---|---|---|---|
| **`npx skills add <owner>/<repo>`** (vercel-labs/skills) | instala **só skills**, layout `skills/<nome>/SKILL.md` | 75+ agentes | zero — nosso layout **já** é esse |
| **Plugin do Claude Code** (`.claude-plugin/plugin.json` + marketplace) | agentes + skills + comandos, com versão e atualização | Claude Code | baixo — manifesto + empacotamento |
| **CLI próprio** (Spec Kit: `uvx --from git+… specify init`) | controle total, assets no wheel, funciona offline | universal | ~6.900 linhas de Python + publicação em índice |

## Decisão

**Três camadas, do completo ao leve** — não uma escolha única:

1. **A — script `install-maestro.sh`** (recomendado): leva o método **inteiro** (agentes,
   skills, scripts, comandos, templates, governança) para qualquer projeto e qualquer
   assistente. É o caminho canônico.
2. **B — plugin do Claude Code**: `plugin/maestro/` gerado das fontes por
   `scripts/package-plugin.sh`, publicado pelo `.claude-plugin/marketplace.json` do
   próprio repositório. Entrega agentes + skills + comandos com versão e atualização.
3. **C — `npx skills add GHDaru/maestro`**: as 6 skills em 75+ agentes. **Já funciona sem
   nenhuma mudança** — nosso layout coincide com o padrão da comunidade.

**Não construímos um CLI próprio** (estilo Spec Kit).

## Alternativas consideradas

- **CLI Python/Node próprio**: daria `maestro init` elegante e funcionamento offline, mas
  custa milhares de linhas, publicação em índice de pacotes e manutenção de release —
  para entregar o que um script de 90 linhas já entrega. Violaria YAGNI.
- **Só `npx skills add`**: instalaria **1/5 do método** (as skills) e deixaria de fora
  agentes, scripts, templates e governança. Daria a impressão falsa de "Maestro instalado".
- **Só o plugin do Claude Code**: amarraria o método a um assistente, contra a tese de que
  o Maestro é agnóstico de ferramenta.

## Consequências

- (+) Cada público entra pela porta do seu tamanho; nenhuma camada exclui a outra.
- (+) A camada C saiu de graça — o padrão da comunidade validou nosso layout.
- (+) Versão e atualização automáticas para quem usa Claude Code (camada B).
- (−) **Duplicação controlada**: o plugin espera `agents/` e `commands/` na raiz, nossas
  fontes vivem em `.claude/`. Mitigado por `package-plugin.sh --verify`, que falha
  quando o pacote diverge das fontes (provado falhando antes de aceito).
- (−) Três caminhos exigem três documentações — todas no `README.md`, sem duplicar conteúdo.

## Registro

`scripts/package-plugin.sh` · `.claude-plugin/marketplace.json` · `plugin/maestro/` ·
`README.md` (os três caminhos) · ciclo `specs/019-distribuicao-e-templates/`.
