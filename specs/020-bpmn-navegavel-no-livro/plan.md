# Plan 020 — BPMN navegável no livro

- **Spec**: `spec.md` · **Raia**: leve · **Data**: 2026-08-02

## Constitution Check (principios-maestro.md)

| Princípio | Conformidade |
|---|---|
| I. Spec-Driven | ✅ spec antes do código; requisitos em EARS (*Easy Approach to Requirements Syntax*) |
| II. Orquestração humano-governada | ✅ nenhum gate automatizado; a promoção continua pedindo o "sim" |
| III. Reversibilidade / gates de risco | ✅ mudança de publicação, reversível por `git revert`; nada de dado ou infra |
| IV. Test-First / DoD verificável | ✅ os dois portões novos **provados falhando** antes de valer |
| V. Economia de contexto / fronteira | ✅ o motor continua um arquivo; nenhuma dependência nova |
| VI. Artefatos vivos | ✅ o desenho passa a apontar para as normas; template de plano atualizado ao princípio VIII |
| VII. Governança leve / YAGNI | ✅ HTML+CSS do próprio tema; nenhuma biblioteca de diagrama |
| VIII. Comunicação inteligível | ✅ BPMN, DoD, DoR e EARS por extenso na primeira ocorrência de cada texto |

## Como

1. **Consertar antes de enfeitar** (skill `diagnostico-antes-do-fix`): a imagem não aparecia
   porque o motor nunca a copiava. Copiar as imagens referenciadas e **estender o portão**
   para `<img src>` — a causa da falha silenciosa era o portão medir só `<a href>`.
2. **Extrair `resolverHref(href, srcDir)`** da regra `link_open` e aplicá-la também sobre o
   HTML bruto embutido no Markdown (`resolverHtmlBruto`). Assim o mesmo `href="../x.md"`
   funciona no GitHub (leitura da fonte) e no livro (vira `x.html`).
3. **Terceiro portão**: `.md` relativo que sobrar no HTML publicado é falha. Sem isso, um
   bloco não reescrito voltaria a passar verde — a mesma classe de erro do item 1.
4. **Desenhar o BPMN em HTML semântico** (`.bpmn-raia` / `.bpmn-no` / `.bpmn-gate` /
   `.bpmn-art`), com cores derivadas das variáveis do tema por `color-mix`, para funcionar
   nos dois temas sem duplicar paleta. Humano ganha barra sólida à esquerda: a paleta é
   ouro+verde, e cor sozinha não distinguiria humano de agente.
5. **Manter a imagem** logo abaixo, rotulada como versão para apresentação e impressão.

## Verificação (DoD)

```bash
node publicar/build.mjs                 # exit 0, imagem em site/, links OK
# prova dos portões (temporária, revertida em seguida):
#   imagem inexistente no Markdown           -> exit 1, "[img] imagem-inexistente.png"
#   resolverHtmlBruto desligado no motor     -> exit 1, 38 × "[md cru] ../..."
node scratchpad/click.mjs               # 4 nós clicados em Chromium -> capítulo certo
node scratchpad/shot.mjs                # captura do bloco nos dois temas
```
